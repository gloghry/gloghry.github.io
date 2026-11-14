# Performance review

Issue #20 covers font/JavaScript weight, layout stability, and reduced-motion behavior.

## Current design

- Atkinson Hyperlegible Next is served locally as upright/italic variable WOFF2 files (48,188 and 52,692 bytes). Only used faces need to load; the upright face is preloaded and both use font-display: swap with system fallbacks.
- The prepared portrait is about 277 KB, preserves intrinsic dimensions/orientation, and appears only on About. Unprepared originals are excluded from site output.
- The visitor JavaScript is the small theme script; browser/axe audit packages run in CI only.
- There is no decorative animation. Reduced-motion checks verify page load and theme switching remain still.

## Measurements

The existing browser audit now uses fresh contexts for Home and About at 390 and 1440 pixels in Chromium/WebKit, for both root and subpath builds. Fonts/photos are delayed 200 ms to exercise late loading.

Each performance entry in the browser-audit artifact's report.json records:

- Response body bytes for HTML, scripts, stylesheets, fonts, and images, plus a script-only total and per-resource inventory.
- Initial-load CLS using the largest session window (under one-second gaps, at most five seconds), ignoring recent-input shifts. Supported browsers must remain at or below 0.1; Chromium must expose the observation API.
- Loaded custom-font status and swap display.
- Absence of third-party resource requests or failed responses.

WebKit may not expose layout-shift entries; its CLS is then null rather than a fabricated zero. Its image/font, resource, layout, and reduced-motion checks still run.

## Limits and follow-up

These are lab measurements from the generated site on a local CI server, not production network timings, real-user Core Web Vitals, or a Lighthouse score. Body bytes are uncompressed response content, not an estimate of GitHub Pages' compressed wire transfer. The observer covers initial load before synthetic layout mutations; later interaction/session behavior is not measured here.

Use the artifact and CI PERF log lines as the evidence for current page weight. Update the measured baseline after adding real posts, projects, embeds, or images. If field performance later becomes a concern, use Search Console/PageSpeed data rather than treating local CI timing as a user experience measurement.

References:
- https://web.dev/articles/cls
- https://developer.mozilla.org/en-US/docs/Web/API/PerformanceResourceTiming
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
