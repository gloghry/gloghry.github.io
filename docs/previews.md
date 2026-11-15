# Pull request previews

Issue #44 adds public Cloudflare Pages review copies. Production remains on GitHub Pages at https://garettloghry.com, with DNS at Porkbun. This repository prepares the build; Cloudflare account setup and live verification are still required.

## Connect the project

After the preview configuration is merged:

1. Sign in to Cloudflare and create a **Pages** project using **Connect to Git**. Choose Pages, rather than a Workers deployment.
2. Authorize the Cloudflare GitHub integration for **only gloghry/gloghry.github.io**. Do not add a custom domain or change nameservers.
3. Use these build settings:

   | Setting | Value |
   | --- | --- |
   | Project name | A unique name such as `garettloghry-previews` |
   | Production branch | `main` (Cloudflare's mirror only) |
   | Framework preset | Jekyll |
   | Root directory | Repository root |
   | Build command | `bundle install && python3 scripts/build_preview.py` |
   | Build output directory | `_site` |
   | `RUBY_VERSION` | `3.3` |
   | `PYTHON_VERSION` | `3.11` |

   Apply runtime/build settings to both Production and Preview environments. Cloudflare supplies `CF_PAGES_URL`; do not hardcode it. Leave `SITE_BASEURL` empty for these root-hosted previews.
4. Allow the initial main-branch mirror to build, then disable **Enable automatic production branch deployments** under Settings → Builds & deployments → Configure Production deployments. This mirror also gets noindex protection from our build script.
5. Enable preview deployments for same-repository issue branches. Cloudflare can build all non-production branches, including branches without PRs; select custom branches if narrower controls become useful.
6. Leave preview visibility public, as Garett approved. Add no mailbox, GitHub, Cloudflare API, or other application secrets to build environments. This static build needs none.

Cloudflare should supply a deployment check/link on a same-repository PR. Open that link on desktop and phone. No preview integration is considered verified until an actual PR has a working link. Existing GitHub Actions build checks remain independent; preview failure does not deploy or overwrite production.

Git-connected Pages projects and Direct Upload projects have different capabilities. Use Git integration for this setup. There is no deployment-token GitHub workflow and no privileged `pull_request_target` execution.

## What gets built

`scripts/build_preview.py` runs the same verified font download and portrait preparation as production, then Jekyll with production settings and temporary preview overrides. It does not enable drafts. It validates the resulting local links and preview metadata.

- Navigation and assets remain relative and honor the configured base path.
- Canonical and Open Graph page URLs identify the corresponding production page.
- Feed and sitemap URLs stay on the preview origin, so preview browsing does not jump to production. Every response gets an `X-Robots-Tag: noindex, nofollow` rule through a generated Cloudflare `_headers` file; HTML additionally has a robots meta tag.
- The noindex protections apply to the Cloudflare main mirror too. They are generated only by the preview build, never by the GitHub Pages production build.
- Existing source exclusions remain in effect: agent/process documents, scripts, drafts, and original portrait uploads are not published by Jekyll. Those source files are still public in GitHub.

Previews are public review copies, not private storage. A branch can modify its build code, so these checks are protections against mistakes, not a security boundary against malicious changes. Review branch contents before pushing. Fork PRs are outside the automatic preview policy; review and deliberately copy approved changes into a same-repository issue branch if a preview is needed.

## Verify the first deployment

Keep #44 open while completing this checklist:

- Confirm Ruby 3.3, font preparation, portrait preparation, Jekyll build, and metadata/link checks succeed in the Cloudflare log.
- Open Home/About/Projects/Writing on phone and desktop. Check the portrait, both themes, navigation, and keyboard focus.
- Inspect response headers for `X-Robots-Tag: noindex`, view-source for the robots meta tag, and confirm canonical URLs use garettloghry.com while feed/sitemap use the preview origin.
- Push a harmless change to the PR branch and confirm the PR preview updates. Cloudflare also retains immutable older deployment URLs.
- Test removal with a disposable branch and record the tested URLs/results in #44. Do not treat a merged PR, a deleted branch, or a newly updated alias as proof that old deployments disappeared.
- Confirm https://garettloghry.com still serves production and its headers/HTML have no preview noindex rule.

CI tests generated previews at both the domain root and `/portfolio`, alongside the existing production browser audits. It cannot verify Cloudflare account permissions, live HTTP headers, PR integration, or provider deletion behavior.

## Cleanup and accidental publication

Routine cleanup is explicit: after a PR closes, remove obsolete preview deployments from Cloudflare. This implementation does not yet automate provider cleanup. Record the first tested cleanup in #44 before closing the issue.

Cloudflare's current documentation says the latest deployment for a branch cannot be deleted. A newer deployment changes the branch alias, but the older immutable deployment URL remains until explicitly deleted.

If sensitive material reaches a preview:

1. Stop further publishing from the affected branch. For urgent access restriction, enable the project's Cloudflare Access preview policy and verify each affected URL is blocked. This policy does not automatically protect the main `project.pages.dev` mirror; inspect that separately if it was affected.
2. If credentials were exposed, revoke/rotate them. Removing files or a preview cannot revoke downloaded credentials.
3. Remove the material from branch contents. Public Git history, PR diffs, build logs/artifacts, and downloaded copies require separate review; deleting a preview does not erase them. Do not rewrite Git history without a separate deliberate plan.
4. If the sensitive deployment is the latest for its branch, publish a clean replacement to that branch so the affected version is no longer latest. Confirm the clean replacement succeeds before deleting the older version. If Cloudflare still refuses deletion, keep access restricted and use provider support; do not assume `--force` bypasses every limit.
5. List deployments and delete **every affected version**, including aliased versions when necessary. With authenticated Wrangler:

   ```sh
   npx wrangler pages deployment list --project-name YOUR_PROJECT_NAME
   npx wrangler pages deployment delete DEPLOYMENT_ID --project-name YOUR_PROJECT_NAME
   ```

   For an active alias, Wrangler documents `--force`; it also skips confirmation, so inspect the deployment ID first. Never put API tokens in public commands, issues, or files.
6. Revisit each recorded immutable URL and branch alias from a signed-out browser. Confirm it no longer serves the material. Leave access restricted until all affected locations are checked.

Replacing then deleting an older preview is the proposed recovery procedure; it still needs a live disposable-deployment test. No service can guarantee removal of copies already fetched by other people.

## Local checks

After installing the usual Ruby/Bundler/Python dependencies:

```sh
bundle install
python3 scripts/build_preview.py --url https://local-review.pages.dev --destination /tmp/site-preview-root
python3 scripts/build_preview.py --url https://local-review.pages.dev --baseurl /portfolio --destination /tmp/site-preview-subpath
```

The supplied pages.dev origin is metadata for a local build, not a real deployment. For a browser audit, mount the matching directory/path using the [existing audit commands](accessibility.md). Keep preview output outside the source tree, except Cloudflare's standard `_site`, so later production builds cannot copy it.

## References

- [Cloudflare Git integration](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Preview URLs, indexing, access, and deletion limits](https://developers.cloudflare.com/pages/configuration/preview-deployments/)
- [Branch deployment controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)
- [Build runtimes](https://developers.cloudflare.com/pages/configuration/build-image/)
- [Deployment deletion API](https://developers.cloudflare.com/api/resources/pages/subresources/projects/subresources/deployments/methods/delete/)
