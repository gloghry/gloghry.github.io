"""Protect the JPEG scan and orientation while removing portrait metadata."""
import struct
import unittest
from prepare_portrait import prepare


def segment(marker, payload):
    return bytes((0xFF, marker)) + struct.pack(">H", len(payload) + 2) + payload


def jpeg(metadata=b""):
    frame = segment(0xC0, b"\x08" + struct.pack(">HH", 600, 400) + b"\x01\x01\x11\x00")
    return b"\xff\xd8" + metadata + frame + b"\xff\xda\x00\x02scan-data\xff\xd9"


class PortraitTests(unittest.TestCase):
    def test_preserves_scan_and_dimensions(self):
        data = jpeg()
        self.assertEqual(prepare(data), (data, 400, 600))

    def test_removes_xmp_and_comments(self):
        data = jpeg(segment(0xE1, b"private XMP location") + segment(0xFE, b"private comment"))
        prepared, width, height = prepare(data)
        self.assertNotIn(b"private", prepared)
        self.assertEqual(prepared, jpeg())
        self.assertEqual((width, height), (400, 600))

    def test_retains_orientation_without_original_exif(self):
        exif = b"Exif\0\0II" + struct.pack("<HIH", 42, 8, 1)
        exif += struct.pack("<HHIHHI", 0x0112, 3, 1, 6, 0, 0) + b"private camera GPS"
        prepared, width, height = prepare(jpeg(segment(0xE1, exif)))
        self.assertNotIn(b"private", prepared)
        self.assertEqual((width, height), (600, 400))
        self.assertEqual(prepare(prepared), (prepared, width, height))

    def test_rejects_invalid_or_truncated_input(self):
        for data in (b"not a JPEG", b"\xff\xd8", b"\xff\xd8\xff\xe1\x00\x20bad"):
            with self.subTest(data=data), self.assertRaises((ValueError, IndexError, struct.error)):
                prepare(data)


if __name__ == "__main__":
    unittest.main()
