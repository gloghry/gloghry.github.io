"""Regression coverage for offline font verification."""
from hashlib import sha1
import unittest

from fetch_fonts import verify


def git_blob_id(data):
    return sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


class FontVerifierTests(unittest.TestCase):
    def test_valid_woff2_data_passes(self):
        data = b"wOF2 test font data"
        verify(data, git_blob_id(data))

    def test_mismatched_git_blob_id_fails(self):
        data = b"wOF2 test font data"
        with self.assertRaises(ValueError):
            verify(data, "0" * 40)

    def test_matching_blob_id_with_invalid_signature_fails(self):
        data = b"not a WOFF2 font"
        with self.assertRaises(ValueError):
            verify(data, git_blob_id(data))


if __name__ == '__main__':
    unittest.main()
