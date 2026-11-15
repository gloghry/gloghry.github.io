# Responsive and accessibility audit

Issues #9 and #10 cover layout and accessible use; #20 adds page-weight, initial-load stability, font, and reduced-motion measurements.

## Automated browser checks

`scripts/audit_site.cjs` serves the generated `_site` locally inside CI and checks Chromium and WebKit. It honors `SITE_BASEURL` for both browser URLs and the local server mount; Jekyll's artifact directory remains independent of that URL prefix. `SITE_DIRECTORY` selects the generated-site directory and `AUDIT_OUTPUT_DIR` selects the report/screenshot destination. CI audits the configured path plus an alternate build, ensuring both domain-root and `/portfolio` deployment cases are covered. The alternate build is written outside the production artifact and is never deployed.

It covers Home, About, Projects, Writing, Copyright & credits, and 404 pages at 320, 390, 768, 1024, and 1440 CSS pixels in both themes, plus 200% text reflow, long headings/code, portrait loading/dimensions, navigation targets, skip-link focus, keyboard theme control, preference persistence, system changes, storage failures, and no-JavaScript navigation.

Issue #64 adds compact-navigation checks in both themes: Enter/Space activation, expanded state, tab access to links, Escape with focus return, outside-click closing, link navigation, and resizing between compact and desktop headers. The open menu receives an accessibility scan and screenshot; enlarged-text checks also open the menu. Below 52rem the menu collapses when JavaScript is available; wider screens retain visible links. Without JavaScript, navigation links remain visible.

Issue #77 adds checks that the PDF links from the header and About open a separate browsing context at phone and desktop widths in Chromium and WebKit. They verify the original page stays open, the new page has no opener, and the response is a PDF. CI runs these at root and subpath URLs. Browser-native PDF viewers are not exposed as ordinary pages in Playwright, so their display and download controls need owner review on real devices.

Axe checks WCAG A/AA rules on all six page types at the phone width in both themes. Automated checks do not prove full accessibility or replace testing with assistive technology and real devices.

CI uploads screenshots and report.json in the **browser-audit** artifact, retained for seven days. This is a downloadable verification artifact, not a hosted branch preview (#44).

## Run locally

Issue #18 adds the static GL sculpture and simplified favicon. Browser checks
verify the accessible home-link name, actual WebP load, 128×208 intrinsic image
dimensions, displayed mark height, visible owner name and favicon base path.
Header screenshots (`*-header.png`) cover 320, 390 and 1440 px in both themes
and browser engines. Source and regeneration details are in [gl-mark.md](gl-mark.md).

First follow CONTRIBUTING.md to prepare fonts/portrait and build Jekyll. With Node 22+ available:

```sh
npm install --prefix /tmp/site-audit --no-save --package-lock=false playwright@1.65.1 @axe-core/playwright@4.14.0
/tmp/site-audit/node_modules/.bin/playwright install --with-deps chromium webkit
NODE_PATH=/tmp/site-audit/node_modules node scripts/audit_site.cjs
```

For a subpath audit, build with the matching baseurl first and pass it to the runner:

```sh
JEKYLL_ENV=production bundle exec jekyll build --baseurl /portfolio --destination /tmp/portfolio-site
SITE_BASEURL=/portfolio SITE_DIRECTORY=/tmp/portfolio-site NODE_PATH=/tmp/site-audit/node_modules node scripts/audit_site.cjs
```

## Owner feedback

Garett reported no specific readability or usability problems with the current font/palette when asked during this audit. This is feedback, not a claim of a formal assistive-technology audit.

## Manual checks

- Check on an actual phone and desktop, especially navigation, portrait placement, and long technical articles.
- Confirm focus is visible and content/navigation are understandable with a screen reader.
- Recheck reading comfort with Garett after meaningful typography or palette changes.
