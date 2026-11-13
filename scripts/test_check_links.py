"""Regression coverage for artifact boundaries and deployment base paths."""
from pathlib import Path
import tempfile
import unittest
from check_links import check


class LinkCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.checkout = Path(self.temp.name)
        self.root = self.checkout / '_site'
        self.root.mkdir()

    def write(self, path, text=''):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def test_empty_build_fails(self):
        self.assertTrue(check(self.root))

    def test_relative_link_cannot_use_checkout_file(self):
        (self.checkout / 'README.md').write_text('Excluded from publication')
        self.write('index.html', '<a href="../README.md">Bad link</a>')
        self.assertEqual(len(check(self.root)), 1)

    def test_dot_segments_clamp_at_site_root(self):
        self.write('index.html', '<a href="../../about/">About</a>')
        self.write('about/index.html', '<a href="../">Home</a>')
        self.assertEqual(check(self.root), [])

    def test_base_path_and_assets(self):
        self.write('index.html', '<a href="/portfolio/projects/">Projects</a><link href="/portfolio/assets/style.css"><script src="/portfolio/assets/theme.js"></script>')
        self.write('projects/index.html', '<a href="../">Home</a>')
        self.write('assets/style.css')
        self.write('assets/theme.js')
        self.assertEqual(check(self.root, '/portfolio/'), [])

    def test_base_path_requires_segment_boundary(self):
        self.write('index.html', '<a href="/portfolio-other/">Outside</a>')
        self.write('portfolio-other/index.html')
        self.assertEqual(len(check(self.root, '/portfolio')), 1)

    def test_missing_asset_and_external_links(self):
        self.write('index.html', '<a href="https://github.com/gloghry">GitHub</a><a href="//example.com">Other</a><a href="#main">Main</a><img src="/missing.svg">')
        self.assertEqual(len(check(self.root)), 1)

    def test_encoded_space_and_query(self):
        self.write('index.html', '<a href="/a%20file.pdf?download=1#top">PDF</a>')
        self.write('a file.pdf')
        self.assertEqual(check(self.root), [])

    def test_slash_terminated_file_url_fails(self):
        self.write('index.html', '<script src="/assets/theme.js/"></script>')
        self.write('assets/theme.js')
        self.assertEqual(len(check(self.root)), 1)

    def test_slash_terminated_directory_index_passes(self):
        self.write('index.html', '<a href="/projects/">Projects</a>')
        self.write('projects/index.html')
        self.assertEqual(check(self.root), [])

    def test_slash_semantics_with_base_path_and_query(self):
        self.write('index.html', '<script src="/portfolio/assets/theme.js/?v=1"></script>')
        self.write('assets/theme.js')
        self.assertEqual(len(check(self.root, '/portfolio')), 1)

    def test_filename_ending_in_index_is_not_directory_index(self):
        self.write('customindex.html', '<a href="sibling.html">Sibling</a>')
        self.write('sibling.html')
        self.assertEqual(check(self.root), [])

    def test_symlink_cannot_escape_artifact(self):
        external = self.checkout / 'private.txt'
        external.write_text('Not published')
        (self.root / 'escape.txt').symlink_to(external)
        self.write('index.html', '<a href="/escape.txt">Outside</a>')
        self.assertEqual(len(check(self.root)), 1)


if __name__ == '__main__':
    unittest.main()
