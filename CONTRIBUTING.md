# Working on the site

The site uses Jekyll 4.4 with feed and sitemap plugins. Run the commands below from the repository root.

## Issues and branches

Every change, including documentation and maintenance, needs a GitHub issue. Reuse an existing issue when it covers the work; otherwise create one before editing. Work on a dedicated branch such as `26-approachable-readme`, and reference the issue in the pull request. Include follow-up fixes on that branch when they belong to the same issue.

### Priority and readiness

Use the Work item issue form to select exactly one priority and explain why. Priorities are defined in [AGENTS.md](AGENTS.md#issue-priorities): P0 is highest priority, P1 near-term, P2 follow-up, and P3 optional exploration. Priority is separate from effort or whether an issue needs user input.

For API-created issues, include a `## Priority` section with a P0–P3 value and short rationale. GitHub forms render the equivalent field under `### Priority`; both are accepted. Confirm dependencies and required input before starting, preserve existing priority decisions, and do not invent missing content to unblock work.

## Pull request labels

Use exactly one change-type label and one priority label on each PR:

| Label | Use |
| --- | --- |
| `enhancement` | New functionality or a meaningful improvement |
| `bug` | Correcting unintended behavior |
| `documentation` | Documentation or agent guidance without a product change |
| `maintenance` | Dependencies, build tooling, or repository upkeep |
| `priority:P0`–`priority:P3` | Priority from the linked issue's Priority section |

Choose the type that describes the main result. For mixed changes, explain the supporting work in the PR description instead of adding multiple types. Take the highest priority (lowest number) when a PR addresses multiple issues; do not infer it from effort or whether input is needed. The issue body remains the source of truth. Resolve a missing or ambiguous issue priority before assigning a PR priority.

Use existing `accessibility` when relevant. Other area labels can wait until the PR volume makes them useful; do not invent labels per PR. Keep Codex assistance in the required attribution footer rather than adding another label.

For example, this labeling-guidance PR uses `documentation` and `priority:P1`; a P0 theme-control bug uses `bug`, `priority:P0`, and `accessibility` when it removes an accessibility barrier. Review labels again when the scope or linked issue priority changes, removing stale type/priority labels while preserving unrelated labels.

Filter Pull requests with `is:pr is:open label:"priority:P1"` or `is:pr label:documentation`. Verify the labels in the PR sidebar after applying them.

### Label setup

The **Repository labels** workflow runs on `main` when its workflow or setup script changes, and can also be run from Actions → Repository labels → Run workflow. It lists the existing catalog and creates only missing labels, leaving existing colors, descriptions, and unrelated labels intact. It does not label PRs automatically.

This workflow has only repository-content read and issue-label write permissions. It runs trusted default-branch code and has no PR trigger. Path-based PR labeling is unnecessary for the current volume.

For local setup with an authenticated GitHub CLI:

```sh
python3 scripts/setup_labels.py
```

The connected GitHub tool can apply labels and creates a missing label with default styling when applying it. It cannot list the complete repository catalog or set label colors/descriptions. Prefer the setup workflow to review the catalog and create missing entries with the descriptions above; it preserves any labels already created through the connector. Until that workflow has succeeded after merge, keep catalog verification open. Apply labels to the implementing PR and any other open PRs, then check the filters above. GitHub also provides manual setup under Issues → Labels → New label; see [GitHub's label instructions](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels).

## Local setup

Install Ruby 3.3, Bundler, and Python 3.9 or newer. Ruby 3.3 matches the version in [.github/workflows/pages.yml](.github/workflows/pages.yml); Python runs the link checker and its regression tests.

```sh
bundle install
python3 scripts/fetch_fonts.py
python3 scripts/prepare_portrait.py
bundle exec jekyll serve --livereload
```

Open http://localhost:4000. Restart Jekyll after changing `_config.yml`.

## Validation

Run the same checks as CI:

```sh
python3 scripts/fetch_fonts.py
python3 scripts/prepare_portrait.py
python3 -m unittest discover -s scripts -p "test_*.py"
JEKYLL_ENV=production bundle exec jekyll build --trace --baseurl ""
python3 scripts/check_links.py _site --baseurl ""
```

The link checker verifies local file targets in generated HTML. It handles directory indexes, URL dot segments, artifact boundaries, and deployment base paths. It does not check remote URLs or fragment IDs.

The build also runs Chromium/WebKit responsive and accessibility checks and uploads a browser-audit artifact with screenshots and a JSON report. See [audit coverage and local commands](docs/accessibility.md).

Also check both color themes, keyboard navigation, mobile widths, and code block scrolling on real devices. If Ruby/Jekyll or browser preview is unavailable, state which checks have not run and use CI for build verification.

### Subpath deployments

This user site is served at the domain root, so the workflow's `SITE_BASEURL` is empty. For a project site served below a path, update `SITE_BASEURL` in the workflow and pass the same path to the build and checker:

```sh
python3 scripts/fetch_fonts.py
python3 scripts/prepare_portrait.py
JEKYLL_ENV=production bundle exec jekyll build --trace --baseurl "/portfolio"
python3 scripts/check_links.py _site --baseurl "/portfolio"
```

For a matching local preview, use `bundle exec jekyll serve --baseurl "/portfolio"` and open http://localhost:4000/portfolio/. Update `url` and `baseurl` in `_config.yml` if the deployment address changes.

Site tooling must honor both root and subpath deployments. Jekyll's output files stay directly under the destination even when URLs begin with `/portfolio`; a preview server must mount them at that prefix. Use `relative_url` for site-relative template links. The [agent base-path rules](AGENTS.md#jekyll-base-paths) apply to build/preview/checker changes. Existing CI audits the configured path and an alternate root/subpath build; [local browser audit commands](docs/accessibility.md) use matching `SITE_BASEURL` and `SITE_DIRECTORY`.

## Publishing

In repository Settings → Pages, select **GitHub Actions** as the source.

Pull requests run regression tests, build Jekyll, and check internal links. GitHub Actions does not publish previews or deploy production from a PR. Public Cloudflare previews use a separate Git integration once the owner connects it; see [preview setup, verification, and removal](docs/previews.md). Merging to `main` runs the same checks, uploads the generated `_site` artifact, and deploys through the `github-pages` environment. The workflow can also be started manually; deployment runs only for `main`.

Repository rules require the `build` status check and a pull request; only squash merges are allowed. The `github-pages` environment may require approval depending on its settings. Confirm the Actions run and https://garettloghry.com after deployment.

The primary domain is garettloghry.com. Domain ownership, DNS records, the Pages custom-domain setting, and HTTPS must also be configured outside the repository; see [custom-domain setup](docs/domain.md). Changing `_config.yml` alone does not route the domain.

## Adding content

### Posts and drafts

Create `_posts/` if it does not exist. Write articles as `_posts/YYYY-MM-DD-short-title.md` with front matter:

```yaml
---
title: A real article title
description: A short summary
tags: [firmware]
---
```

The filename supplies the date. Configuration assigns the post layout, and published URLs follow `/writing/:title/`. The layout displays the title, date, and tags.

Put unpublished work in `_drafts/` and preview it with:

```sh
bundle exec jekyll serve --drafts
```

The production workflow does not enable drafts. Technical posts are the initial focus.

### Projects

Create `_projects/` if it does not exist. Add a file such as `_projects/short-name.md` with:

```yaml
---
title: Project name
description: A short summary
order: 1
technologies: [C, CAN]
repository: https://github.com/gloghry/your-project
---
```

The `repository` field is optional. Configuration assigns the project layout and URLs under `/projects/`. The indexes sort projects by `order`.

Describe the problem, constraints, implementation, and what you learned in the body. Use real, approved material; do not publish private employer information. Keep the empty states until there is actual content.

## Where things live

- `_config.yml`: site identity, canonical URL, collections, layout defaults, and publication exclusions.
- `_layouts/default.html`: shared navigation and metadata.
- `_layouts/post.html` and `_layouts/project.html`: article and project layouts.
- `assets/styles.css`: colors, typography, and responsive layout.
- `assets/theme.js`: system theme preference and saved theme selection.
- `scripts/`: generated-site link checker and regression tests.

The design uses slate-and-teal light/dark themes, with underlined links and visible focus. Atkinson Hyperlegible Next is self-hosted; there are no analytics or third-party font requests. See [font provenance and license](assets/fonts/README.md). See [design and launch notes](docs/plan.md) for decisions and open content questions.

## Portrait

Garett selected `assets/images/originals/Plandid.jpg` for the About page. Run `python3 scripts/prepare_portrait.py` before local Jekyll preview/build; CI runs this step automatically. It creates `assets/images/garett.jpg` and `_data/portrait.yml` with metadata removed except necessary orientation. Pixel data is preserved without cropping or recompression. The original is about 277 KB. Both original uploads live in `assets/images/originals/`, which is excluded from the website output; they remain in repository history. The prepared image is sized responsively in CSS and supplies intrinsic dimensions to reserve layout space.
