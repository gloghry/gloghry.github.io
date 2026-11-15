# Public résumé provenance

Website issue #12; delivery tracker gloghry/Resume#21.

## PDF download behavior

Issue #77 makes the About and header PDF links open the stable `/resume.pdf`
directly in a new tab, with an external-link icon and an accessible new-tab
announcement. The PDF response and contents are unchanged. The browser's PDF
viewer can be used to download or print the document; whether the browser opens
its viewer or downloads the file depends on browser settings. The links use
Jekyll's `relative_url` filter and honor deployment base paths.

## Public PDF source

Prepared from gloghry/Resume commit
`e88424c5027653f51c76d06b7d91b7be80e64338` (PR #25), using `make public`.
Only the explicit public PDF was copied. Issue #63 removes the duplicated HTML résumé; the header links directly to the PDF,
and `/resume/` redirects to it for existing bookmarks. Public contact: garettloghry.com and
contact@garettloghry.com; no phone or private project details.

PDF SHA-256: `b92819fd55c97a0adb9dbe2919270404fad872b81ce20eea721a518c4f042ef1`.

Status: prepared for review; final publication approval and live anonymous/mobile
download verification remain outstanding. PR #25 contains the source/build work;
this website must not receive access to private résumé records. See
CONTRIBUTING.md for manual replacement, validation and rollback instructions.
