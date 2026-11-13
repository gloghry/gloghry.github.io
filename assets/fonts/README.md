# Atkinson Hyperlegible Next

The site self-hosts the upright and italic variable WOFF2 fonts from the [official Google Fonts project](https://github.com/googlefonts/atkinson-hyperlegible-next/tree/7925f50f649b3813257faf2f4c0b381011f434f1). Both cover weights 200–800; code keeps the system monospace stack.

Run `python3 scripts/fetch_fonts.py` before previewing or building locally. CI runs it before Jekyll. The script downloads the unmodified files at revision `7925f50f649b3813257faf2f4c0b381011f434f1` and verifies their Git blob IDs and WOFF2 signatures. Verified existing files are reused. Downloads fail closed if the content does not match.

- Upright: `fonts/webfonts/AtkinsonHyperlegibleNext[wght].woff2` → `atkinson-hyperlegible-next-normal.woff2` (48,188 bytes)
- Italic: `fonts/webfonts/AtkinsonHyperlegibleNext-Italic[wght].woff2` → `atkinson-hyperlegible-next-italic.woff2` (52,692 bytes)

Generated WOFF2 files are ignored by Git but included in the Pages artifact. Visitors load them from this site, with no font-service requests. `font-display: swap` and system fallbacks keep text available while fonts load or if a request fails.

Copyright 2020-2024 The Atkinson Hyperlegible Next Project Authors. The unmodified [SIL Open Font License](OFL.txt) is distributed alongside the font files.
