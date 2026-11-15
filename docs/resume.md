# Public résumé provenance

Website issue #12; delivery tracker gloghry/Resume#21.

## PDF download behavior

Issue #77 changes the About and résumé PDF links to open `/resume/download/`
in a new tab, with a visible new-tab warning and `rel="noopener"`. That page
requests a same-origin download of `/resume.pdf` as `garett-loghry-resume.pdf`.
The stable PDF URL and its contents are unchanged. A visible download link
works without JavaScript and remains available if an automatic download is
blocked. Browser/user settings still control prompts, saving, and external
PDF handling; the page does not claim that a file was saved successfully.
All page, asset, and PDF links honor Jekyll's deployment base path.

## Public PDF source

Prepared from gloghry/Resume commit
`e88424c5027653f51c76d06b7d91b7be80e64338` (PR #25), using `make public`.
Only the explicit public PDF was copied. The readable page mirrors the same
reviewed source content. Public contact: garettloghry.com and
contact@garettloghry.com; no phone or private project details.

PDF SHA-256: `b92819fd55c97a0adb9dbe2919270404fad872b81ce20eea721a518c4f042ef1`.

Status: prepared for review; final publication approval and live anonymous/mobile
download verification remain outstanding. PR #25 contains the source/build work;
this website must not receive access to private résumé records. See
CONTRIBUTING.md for manual replacement, validation and rollback instructions.
