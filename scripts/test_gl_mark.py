"""Verify the prebuilt asset handoff without Blender or imaging dependencies."""
import hashlib
import json
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StaticMarkProvenanceTests(unittest.TestCase):
    def test_imported_files_match_reviewed_source_hashes(self):
        provenance = json.loads((ROOT/"docs/gl-mark-provenance.json").read_text())
        directory = ROOT/"assets/images/gl"
        for name, details in provenance["files"].items():
            data = (directory/name).read_bytes()
            with self.subTest(name=name):
                self.assertEqual(len(data), details["bytes"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), details["sha256"])
        png = (directory/"gl-mark.png").read_bytes()
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack_from(">II", png, 16), (provenance["width"], provenance["height"]))
        self.assertEqual(png[25], 6, "PNG fallback must retain RGBA transparency")
        webp = (directory/"gl-mark.webp").read_bytes()
        self.assertEqual(webp[:4], b"RIFF")
        self.assertEqual(webp[8:12], b"WEBP")


if __name__ == "__main__":
    unittest.main()
