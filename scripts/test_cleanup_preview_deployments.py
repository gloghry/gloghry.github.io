import unittest
from datetime import datetime, timezone

from cleanup_preview_deployments import classify


NOW = datetime(2026, 11, 15, 12, 0, tzinfo=timezone.utc)
REPOSITORY = "gloghry/gloghry.github.io"


def deployment(branch="15-writing", environment="preview", aliases=None,
               trigger_type="github:push", commit="abc123"):
    return {
        "id": "deployment-1",
        "environment": environment,
        "aliases": aliases or [],
        "deployment_trigger": {
            "type": trigger_type,
            "metadata": {"branch": branch, "commit_hash": commit},
        },
    }


def pull_request(number=27, state="closed", branch="15-writing",
                 head_repository=REPOSITORY, base_repository=REPOSITORY,
                 closed_at="2026-11-08T12:00:00Z"):
    return {
        "number": number,
        "state": state,
        "closed_at": closed_at,
        "head": {"ref": branch, "repo": {"full_name": head_repository}},
        "base": {"repo": {"full_name": base_repository}},
    }


class CleanupClassificationTests(unittest.TestCase):
    def classify(self, item=None, prs=None, open_branches=None):
        return classify(item or deployment(), prs if prs is not None else [pull_request()],
                        open_branches or set(), "main", REPOSITORY, NOW)

    def test_deletes_only_after_full_seven_day_grace_period(self):
        eligible = self.classify()
        self.assertEqual(eligible["action"], "delete")
        self.assertEqual(eligible["pull_request"], 27)

        too_early = self.classify(prs=[pull_request(closed_at="2026-11-08T12:00:01Z")])
        self.assertEqual(too_early["action"], "keep")
        self.assertIn("retention", too_early["reason"])

    def test_preserves_every_deployment_for_an_open_pr_branch(self):
        decision = self.classify(item=deployment(commit=None), prs=[], open_branches={"15-writing"})
        self.assertEqual(decision["action"], "keep")
        self.assertIn("open pull request", decision["reason"])

    def test_preserves_production_and_active_aliases(self):
        production = self.classify(item=deployment(branch="main"))
        self.assertEqual(production["action"], "keep")
        self.assertIn("production branch", production["reason"])

        aliased = self.classify(item=deployment(aliases=["15-writing.gloghry-github-io.pages.dev"]))
        self.assertEqual(aliased["action"], "keep")
        self.assertIn("aliases", aliased["reason"])

        production_environment = self.classify(item=deployment(environment="production"))
        self.assertEqual(production_environment["action"], "keep")

    def test_reports_missing_or_ambiguous_pr_mappings_without_deleting(self):
        cases = [
            ([], "no matching"),
            ([pull_request(head_repository="someone/fork")], "no matching"),
            ([pull_request(base_repository="someone/other-repo")], "no matching"),
            ([pull_request(), pull_request(number=28)], "2 matching"),
            ([pull_request(closed_at=None)], "closure time"),
            ([pull_request(closed_at="2026-11-08T12:00:00")], "closure time"),
        ]
        for prs, message in cases:
            with self.subTest(message=message):
                decision = self.classify(prs=prs)
                self.assertEqual(decision["action"], "unmapped")
                self.assertIn(message, decision["reason"])

    def test_reports_unsupported_trigger_and_missing_source_metadata(self):
        webhook = self.classify(item=deployment(trigger_type="deploy_hook"))
        self.assertEqual(webhook["action"], "unmapped")
        self.assertIn("unsupported trigger", webhook["reason"])

        no_commit = self.classify(item=deployment(commit=""))
        self.assertEqual(no_commit["action"], "unmapped")
        self.assertIn("no source commit", no_commit["reason"])

        no_branch = self.classify(item=deployment(branch=""))
        self.assertEqual(no_branch["action"], "unmapped")
        self.assertIn("no source branch", no_branch["reason"])


if __name__ == "__main__":
    unittest.main()
