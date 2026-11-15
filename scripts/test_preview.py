import tempfile
import unittest
from pathlib import Path

from build_preview import preview_baseurl, preview_origin
from check_preview import check


class PreviewTests(unittest.TestCase):
    def test_rejects_non_preview_origins_and_ambiguous_paths(self):
        for value in ("", "http://example.pages.dev", "https://garettloghry.com",
                      "https://user@example.pages.dev", "https://example.pages.dev/path",
                      "https://example.pages.dev?x=1", "https://example.pages.dev:443"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                preview_origin(value)
        self.assertEqual(preview_origin("https://review.pages.dev/"), "https://review.pages.dev")
        for value in ("portfolio", "/portfolio/", "/../other", "/path?x=1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                preview_baseurl(value)

    def test_detects_metadata_and_source_exposure_regressions(self):
        for baseurl in ("", "/portfolio"):
            with self.subTest(baseurl=baseurl), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                origin = "https://review.pages.dev"
                headers = "/*\n  X-Robots-Tag: noindex, nofollow\n"
                html = ('<meta name="robots" content="noindex, nofollow">'
                        '<link rel="canonical" href="https://garettloghry.com/">')
                feed = ('<feed xmlns="http://www.w3.org/2005/Atom">'
                        f'<link rel="self" href="{origin}{baseurl}/feed.xml"/></feed>')
                sitemap = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                           f'<url><loc>{origin}{baseurl}/</loc></url></urlset>')
                (root / "_headers").write_text(headers)
                (root / "index.html").write_text(html)
                (root / "feed.xml").write_text(feed)
                (root / "sitemap.xml").write_text(sitemap)
                check(root, origin, baseurl)
                for filename, broken, restore in (
                    ("_headers", "", headers),
                    ("index.html", html.replace("noindex", "index"), html),
                    ("index.html", html.replace("garettloghry.com", "review.pages.dev"), html),
                    ("feed.xml", feed.replace(origin, "https://garettloghry.com"), feed),
                    ("sitemap.xml", sitemap.replace(origin, "https://garettloghry.com"), sitemap),
                ):
                    with self.subTest(filename=filename, broken=broken):
                        (root / filename).write_text(broken)
                        with self.assertRaises(ValueError):
                            check(root, origin, baseurl)
                        (root / filename).write_text(restore)
                (root / "scripts").mkdir()
                with self.assertRaises(ValueError):
                    check(root, origin, baseurl)


if __name__ == "__main__":
    unittest.main()
