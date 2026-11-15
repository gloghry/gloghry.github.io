# GL header mark

Website issue #18 imports Garett's approved sculpture from
[gloghry/icon PR #8](https://github.com/gloghry/icon/pull/8). Garett supplied the
sculpture reference, approved the geometry baseline, and directed its design;
Codex implemented the model, static exports, and site integration.

The source is the named `original` variant at commit
[`13223fe248db03a3f80d376c63a60251eb7df563`](https://github.com/gloghry/icon/commit/13223fe248db03a3f80d376c63a60251eb7df563).
Machine-readable provenance, image dimensions, and SHA-256 hashes are in
[gl-mark-provenance.json](gl-mark-provenance.json). The G's left back ends at its
lower bar; only its right return continues down as the square L stem, with the
compact foot extending along +Y. The approved follow-up extends total foot
length 20%, from 3.0 to 3.6, with the G and camera settings preserved. The same continuous solid supplies front,
side, and three-quarter previews.

## Static handoff

Only these prebuilt files are served by Jekyll:

- `assets/images/gl/gl-mark.webp` — 128×208 transparent optimized header image,
  4,966 bytes; approximately 68% smaller than the PNG.
- `assets/images/gl/gl-mark.png` — 128×208 RGBA fallback, 15,401 bytes.
- `assets/images/gl/favicon.svg` — simplified GL silhouette for small browser
  icons, with colors for light and dark system preferences.

The header retains the visible name inside a single home link named
“Garett Loghry — home”. The mark is redundant decoration with empty alt text.
Intrinsic dimensions reserve its aspect ratio; CSS displays it at 32×52 px,
or 28×45.5 px on the narrowest phones. WebP is preferred through `<picture>`;
PNG is the fallback. Asset and home URLs use `relative_url` for root/subpath
deployments. The Atkinson font, slate/teal themes, copy and navigation behavior
are preserved. No JavaScript or Blender runtime is added for the mark.

At 16–32 px, the full sculpture loses depth and its compact foot becomes weak.
The favicon simplifies the same G gaps, descending right upright and angled
foot. Its media query follows the browser's system color preference; an
in-page saved theme does not change a separately loaded browser favicon.

## Regenerate and update

Run offline in the **icon repository**, using Blender 4.5.3 LTS and Python 3.10+:

```sh
python3 -m gl_assets generate original --blender /path/to/blender
python3 -m venv .venv
.venv/bin/pip install -r requirements-web.txt
.venv/bin/python scripts/export_web.py generated/original
```

Review the three renders and small-size sheet before copying only the PNG,
WebP and SVG from `generated/original/web/` into `assets/images/gl/` here.
Record the reviewed source commit and file hashes in the provenance JSON.
Keep .blend/GLB, generator code, design references and review sheets in the
source repository. Never fetch or regenerate this mark during Jekyll builds.

## Validation and review

Run the normal Python regression tests, production Jekyll builds and link
checks at `/` and `/portfolio`, then the browser audit as documented in
[accessibility.md](accessibility.md). The audit verifies the home-link name,
actual WebP load, intrinsic dimensions, favicon base path, readable visible
name, and mark height at all normal audit widths, in Chromium and WebKit.
It captures `*-header.png` at 320, 390 and 1440 px in both themes, alongside
the existing accessibility, navigation, reflow and performance checks.

Review those actual-background screenshots before merging this site change.
Production remains unchanged until owner approval and merge.

The checked review bundle is [gl-mark-review/](gl-mark-review/):
[both themes at desktop/mobile sizes](gl-mark-review/headers.png), individual
header captures, and native-size favicon sheets. [validation.json](gl-mark-review/validation.json)
records the tested source commit, browser versions, viewports, build paths and
results. The baseline full root and `/portfolio` audits passed 155 scenarios each;
the site has 33 passing Python checks. The initial local cold-load failure
also occurred on the unchanged site with the host's Nimbus Sans fallback;
using the standard browser-test Liberation/Arial fallback resolved it without
changing site typography or the test threshold.

The approved longer-foot revision passes 33 Python checks, root/subpath builds
and link checks, and 16 focused Chromium/WebKit header scenarios. Its refreshed
header screenshots use the longer foot. See
[longer-foot-validation.json](gl-mark-review/longer-foot-validation.json) for the
revision, source commit and results. Full browser audits run again in PR CI.
