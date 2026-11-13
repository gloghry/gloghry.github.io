# Garett Loghry's website

Minimalist portfolio and technical blog for https://gloghry.github.io, built with Jekyll. Slate-and-teal light/dark themes follow system preferences until the visitor selects a theme. No analytics or external fonts.

## Local development

Install Ruby 3.3 and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve --livereload
```

Open http://localhost:4000. Restart Jekyll after changing `_config.yml`.

## Validate

```sh
python3 -m unittest discover -s scripts -p "test_*.py"
bundle exec jekyll build --trace
python3 scripts/check_links.py _site
```

For a subpath deployment, set `SITE_BASEURL` in the workflow and use the same value with both `jekyll build --baseurl /portfolio` and `check_links.py _site --baseurl /portfolio`. The checker resolves URL dot segments inside the published artifact and rejects links outside its base path.

Pull requests run these checks. Also manually check both themes, keyboard navigation, mobile widths, and code block scrolling. Ruby/Jekyll and browser validation remain required if the development environment cannot run them.

## Publish to GitHub Pages

In repository Settings → Pages, select **GitHub Actions** as the source. Merging to `main` runs `.github/workflows/pages.yml`, builds the site, and deploys the Pages artifact. The `github-pages` environment may require approval depending on repository settings. A pull request only builds; it does not publish. Confirm the Actions run and live URL after deployment.

## Add content

Write posts as `_posts/YYYY-MM-DD-short-title.md` with front matter:

```yaml
---
title: A real article title
description: A short summary
tags: [firmware]
---
```

The filename supplies the date; articles use the post layout. Put unpublished work in `_drafts/` and preview with `bundle exec jekyll serve --drafts`.

Add projects as `_projects/short-name.md` with `title`, `description`, `order`, `technologies` (a YAML list), and optional `repository` URL in front matter. The body should describe the problem, constraints, implementation, and lessons learned. Do not add private employer information.

Navigation and metadata live in `_layouts/default.html`; colors and responsive styles in `assets/styles.css`; theme preference in `assets/theme.js`.

See [design and launch notes](docs/plan.md) for decisions and open content questions.
