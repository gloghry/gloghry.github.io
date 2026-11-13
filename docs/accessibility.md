# Responsive and accessibility audit

Issues #9 and #10 cover layout and accessible use. Priority is separate from whether user input is needed; contact issue #14 is waiting on mailbox setup #34.

## Automated browser checks

`scripts/audit_site.cjs` serves the generated `_site` locally inside CI and checks Chromium and WebKit. It covers Home, About, Projects, Writing, and 404 pages at 320, 390, 768, 1024, and 1440 CSS pixels in both themes, plus 200% text reflow, long headings/code, portrait loading/dimensions, navigation targets, skip-link focus, keyboard theme control, preference persistence, system changes, storage failures, and no-JavaScript navigation.

Axe checks WCAG A/AA rules on all five page types at the phone width in both themes. Automated checks do not prove full accessibility or replace testing with assistive technology and real devices.

CI uploads screenshots and report.json in the **browser-audit** artifact, retained for seven days. This is a downloadable verification artifact, not a hosted branch preview (#44).

## Run locally

First follow CONTRIBUTING.md to prepare fonts/portrait and build Jekyll. With Node 22+ available:

```sh
npm install --prefix /tmp/site-audit --no-save --package-lock=false playwright@1.65.1 @axe-core/playwright@4.14.0
/tmp/site-audit/node_modules/.bin/playwright install --with-deps chromium webkit
NODE_PATH=/tmp/site-audit/node_modules node scripts/audit_site.cjs
```

## Owner feedback

Garett reported no specific readability or usability problems with the current font/palette when asked during this audit. This is feedback, not a claim of a formal assistive-technology audit.

## Manual checks

- Check on an actual phone and desktop, especially navigation, portrait placement, and long technical articles.
- Confirm focus is visible and content/navigation are understandable with a screen reader.
- Recheck reading comfort with Garett after meaningful typography or palette changes.
