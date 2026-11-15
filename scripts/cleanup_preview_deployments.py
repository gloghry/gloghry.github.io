#!/usr/bin/env python3
"""Report or remove expired Cloudflare Pages preview deployments."""
from datetime import datetime, timedelta, timezone
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

API = "https://api.cloudflare.com/client/v4"
GITHUB_API = "https://api.github.com"
REPOSITORY = "gloghry/gloghry.github.io"
PROJECT = "gloghry-github-io"
RETENTION = timedelta(days=7)


class ApiError(RuntimeError):
    pass


def parse_time(value):
    if not value:
        raise ValueError("missing timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return parsed.astimezone(timezone.utc)


def same_repository_pull_requests(pull_requests, repository, branch):
    matches = []
    for pull_request in pull_requests:
        head = pull_request.get("head") or {}
        base = pull_request.get("base") or {}
        head_repo = head.get("repo") or {}
        base_repo = base.get("repo") or {}
        if (head.get("ref") == branch
                and head_repo.get("full_name", "").casefold() == repository.casefold()
                and base_repo.get("full_name", "").casefold() == repository.casefold()):
            matches.append(pull_request)
    return matches


def classify(deployment, pull_requests, open_branches, production_branch, repository, now):
    """Return a conservative action and explanation for one deployment."""
    metadata = (deployment.get("deployment_trigger") or {}).get("metadata") or {}
    branch = metadata.get("branch")
    deployment_id = deployment.get("id", "unknown-id")
    environment = deployment.get("environment")

    def result(action, reason, pr=None):
        return {"action": action, "reason": reason, "id": deployment_id,
                "branch": branch or "unknown-branch", "pull_request": pr}

    if environment != "preview":
        return result("keep", f"environment is {environment or 'unknown'}, not preview")
    if not deployment_id or deployment_id == "unknown-id":
        return result("unmapped", "deployment has no ID")
    if not branch:
        return result("unmapped", "deployment has no source branch")
    if branch == production_branch:
        return result("keep", "production branch")
    if branch in open_branches:
        return result("keep", "branch has an open pull request")
    trigger = deployment.get("deployment_trigger") or {}
    if trigger.get("type") != "github:push":
        return result("unmapped", f"unsupported trigger type {trigger.get('type') or 'unknown'}")
    commit = metadata.get("commit_hash")
    if not commit:
        return result("unmapped", "deployment has no source commit")

    matches = same_repository_pull_requests(pull_requests, repository, branch)
    if not matches:
        return result("unmapped", "commit has no matching same-repository pull request")
    if len(matches) != 1:
        return result("unmapped", f"commit maps to {len(matches)} matching pull requests")
    pull_request = matches[0]
    number = pull_request.get("number")
    state = pull_request.get("state")
    if state != "closed":
        return result("unmapped", f"pull request #{number} has unsupported state {state or 'unknown'}", number)
    try:
        closed_at = parse_time(pull_request.get("closed_at"))
    except (TypeError, ValueError):
        return result("unmapped", f"pull request #{number} has no valid closure time", number)
    expires_at = closed_at + RETENTION
    if now < expires_at:
        return result("keep", f"seven-day retention ends {expires_at.isoformat()}", number)
    aliases = deployment.get("aliases")
    if aliases:
        return result("keep", "deployment still has active aliases; latest/aliased deployments are not force-deleted", number)
    return result("delete", f"pull request #{number} closed {closed_at.isoformat()} and retention elapsed", number)


def request_json(url, token, method="GET", allow_not_found=False):
    request = Request(url, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "gloghry-preview-cleanup",
    })
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read()
            status = response.status
            headers = response.headers
    except HTTPError as error:
        if allow_not_found and error.code == 404:
            return 404, None, error.headers
        detail = error.read().decode("utf-8", errors="replace")
        raise ApiError(f"{method} {url} returned HTTP {error.code}: {detail}") from error
    except (URLError, TimeoutError) as error:
        raise ApiError(f"{method} {url} failed: {error}") from error
    if not body:
        return status, {}, headers
    try:
        return status, json.loads(body), headers
    except json.JSONDecodeError as error:
        raise ApiError(f"{method} {url} returned invalid JSON") from error


def cloudflare_get(path, account_id, token, query=None, allow_not_found=False):
    url = f"{API}/accounts/{quote(account_id, safe='')}/{path}"
    if query:
        url += "?" + urlencode(query)
    status, payload, _ = request_json(url, token, allow_not_found=allow_not_found)
    if status == 404:
        return status, None
    if not payload.get("success"):
        raise ApiError(f"Cloudflare API rejected GET {path}: {payload.get('errors')}")
    return status, payload.get("result")


def cloudflare_write(method, path, account_id, token):
    url = f"{API}/accounts/{quote(account_id, safe='')}/{path}"
    status, payload, _ = request_json(url, token, method=method)
    if not payload.get("success"):
        raise ApiError(f"Cloudflare API rejected {method} {path}: {payload.get('errors')}")
    return status, payload.get("result")


def github_pages(url, token):
    while url:
        status, payload, headers = request_json(url, token)
        if status != 200 or not isinstance(payload, list):
            raise ApiError(f"GitHub API returned an unexpected response for {url}")
        yield from payload
        link = headers.get("Link", "")
        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                start, end = part.find("<"), part.find(">")
                if start >= 0 and end > start:
                    candidate = part[start + 1:end]
                    parsed = urlsplit(candidate)
                    if parsed.scheme == "https" and parsed.netloc == "api.github.com":
                        next_url = candidate
        url = next_url


def cloudflare_project(account_id, token):
    project_path = f"pages/projects/{quote(PROJECT, safe='')}"
    _, project = cloudflare_get(project_path, account_id, token)
    if not isinstance(project, dict):
        raise ApiError("Refusing cleanup: Cloudflare returned no Pages project details")
    source = project.get("source") or {}
    config = source.get("config") or {}
    owner = config.get("owner")
    repo_name = config.get("repo_name") or config.get("repo")
    actual_repository = f"{owner}/{repo_name}" if owner and repo_name else ""
    if source.get("type") != "github" or actual_repository.casefold() != REPOSITORY.casefold():
        raise ApiError(f"Refusing cleanup: Pages project source is {actual_repository or 'unknown'}, not {REPOSITORY}")
    production_branch = project.get("production_branch")
    if not production_branch:
        raise ApiError("Refusing cleanup: Cloudflare project has no production branch")
    return production_branch


def cloudflare_deployments(account_id, token):
    path = f"pages/projects/{quote(PROJECT, safe='')}/deployments"
    page = 1
    all_deployments = []
    while True:
        _, deployments = cloudflare_get(path, account_id, token, {
            "env": "preview", "page": page,
        })
        if not isinstance(deployments, list):
            raise ApiError("Cloudflare returned an unexpected deployments list")
        all_deployments.extend(deployments)
        # Use the provider's default page size; a short page is not proof
        # that pagination is complete. Stop only on an empty page.
        if not deployments:
            return all_deployments
        page += 1


def github_context(repository, token):
    escaped_repository = "/".join(quote(part, safe="") for part in repository.split("/"))
    open_url = f"{GITHUB_API}/repos/{escaped_repository}/pulls?state=open&per_page=100"
    open_branches = {
        (pull_request.get("head") or {}).get("ref")
        for pull_request in github_pages(open_url, token)
        if ((pull_request.get("head") or {}).get("repo") or {}).get("full_name", "").casefold()
        == repository.casefold()
    }
    return escaped_repository, open_branches


def pull_requests_for_commit(repository_path, commit, token):
    url = f"{GITHUB_API}/repos/{repository_path}/commits/{quote(commit, safe='')}/pulls?per_page=100"
    return list(github_pages(url, token))


def confirm_deleted(account_id, token, deployment_id):
    path = (f"pages/projects/{quote(PROJECT, safe='')}/deployments/"
            f"{quote(deployment_id, safe='')}")
    for attempt in range(3):
        status, _ = cloudflare_get(path, account_id, token, allow_not_found=True)
        if status == 404:
            return True
        if attempt < 2:
            import time
            time.sleep(attempt + 1)
    return False


def run(delete=False, now=None):
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    cloudflare_token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    github_token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", REPOSITORY)
    if repository.casefold() != REPOSITORY.casefold():
        raise ApiError(f"Refusing cleanup for unexpected repository {repository}")
    if not account_id or not cloudflare_token or not github_token:
        raise ApiError("Set CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, and GITHUB_TOKEN")
    now = now or datetime.now(timezone.utc)
    production_branch = cloudflare_project(account_id, cloudflare_token)
    repository_path, open_branches = github_context(repository, github_token)
    deployments = cloudflare_deployments(account_id, cloudflare_token)
    pull_requests_cache = {}
    failures = 0
    candidates = 0
    print(f"Project: {PROJECT}; repository: {repository}; production branch: {production_branch}")
    print(f"Mode: {'DELETE' if delete else 'DRY RUN'}; retention: {RETENTION.days} days; deployments: {len(deployments)}")
    for deployment in deployments:
        metadata = (deployment.get("deployment_trigger") or {}).get("metadata") or {}
        commit = metadata.get("commit_hash")
        if commit and commit not in pull_requests_cache:
            pull_requests_cache[commit] = pull_requests_for_commit(repository_path, commit, github_token)
        decision = classify(
            deployment, pull_requests_cache.get(commit, []), open_branches,
            production_branch, repository, now,
        )
        line = (f"{decision['action'].upper()} id={decision['id']} branch={decision['branch']} "
                f"pr={('#' + str(decision['pull_request'])) if decision['pull_request'] else 'unmapped'} "
                f"url={deployment.get('url', 'unknown-url')} aliases={deployment.get('aliases') or []} "
                f"reason={decision['reason']}")
        if decision["action"] == "delete":
            candidates += 1
            if not delete:
                print("DRY-RUN " + line)
                continue
            path = (f"pages/projects/{quote(PROJECT, safe='')}/deployments/"
                    f"{quote(decision['id'], safe='')}")
            try:
                cloudflare_write("DELETE", path, account_id, cloudflare_token)
                if confirm_deleted(account_id, cloudflare_token, decision["id"]):
                    print("CONFIRMED-DELETED " + line)
                else:
                    failures += 1
                    print("FAILED-TO-CONFIRM " + line)
            except ApiError as error:
                failures += 1
                print(f"FAILED {line} error={error}")
        else:
            print(line)
    print(f"Cleanup summary: candidates={candidates}; failures={failures}")
    return 1 if failures else 0


def main():
    delete = os.environ.get("DELETE_EXPIRED_PREVIEWS", "").lower() == "true"
    try:
        return run(delete=delete)
    except ApiError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
