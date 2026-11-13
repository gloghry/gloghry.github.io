"""Prepare a portrait JPEG without changing its pixels or cropping it."""
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "Plandid.jpg"
OUTPUT = ROOT / "assets" / "images" / "garett.jpg"
DIMENSIONS = ROOT / "_data" / "portrait.yml"


def orientation(exif):
    if not exif.startswith(b"Exif\0\0"):
        return 1
    tiff = exif[6:]
    order = {b"II": "<", b"MM": ">"}.get(tiff[:2])
    if order is None:
        raise ValueError("Invalid EXIF byte order")
    offset = struct.unpack_from(order + "I", tiff, 4)[0]
    count = struct.unpack_from(order + "H", tiff, offset)[0]
    for i in range(count):
        entry = offset + 2 + 12 * i
        tag, kind, length = struct.unpack_from(order + "HHI", tiff, entry)
        if tag == 0x0112:
            if kind != 3 or length != 1:
                raise ValueError("Unsupported EXIF orientation")
            value = struct.unpack_from(order + "H", tiff, entry + 8)[0]
            if value not in range(1, 9):
                raise ValueError("Invalid EXIF orientation")
            return value
    return 1


def prepare(data):
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("Portrait must be JPEG")
    result = bytearray(data[:2])
    position, rotation = 2, 1
    width = height = None
    while position < len(data):
        if data[position] != 0xFF:
            raise ValueError("Invalid JPEG marker")
        start = position
        while data[position] == 0xFF:
            position += 1
        marker = data[position]
        position += 1
        if marker in (0xDA, 0xD9):
            if width is None or height is None:
                raise ValueError("JPEG dimensions not found")
            if rotation != 1:
                # Retain only orientation; discard original EXIF including GPS/device data.
                exif = b"Exif\0\0II" + struct.pack("<HIH", 42, 8, 1)
                exif += struct.pack("<HHIHHI", 0x0112, 3, 1, rotation, 0, 0)
                result += b"\xff\xe1" + struct.pack(">H", len(exif) + 2) + exif
            result += data[start:]
            if rotation in (5, 6, 7, 8):
                width, height = height, width
            return bytes(result), width, height
        length = struct.unpack_from(">H", data, position)[0]
        end = position + length
        if length < 2 or end > len(data):
            raise ValueError("Invalid JPEG segment length")
        payload = data[position + 2:end]
        if marker == 0xE1:
            rotation = orientation(payload) if payload.startswith(b"Exif\0\0") else rotation
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack_from(">HH", payload, 1)
        # Keep JFIF and ICC color profiles; remove comments and other application metadata.
        application = 0xE0 <= marker <= 0xEF
        keep = not application and marker != 0xFE
        keep = keep or marker == 0xE0 or (marker == 0xE2 and payload.startswith(b"ICC_PROFILE\0"))
        if keep:
            result += data[start:end]
        position = end
    raise ValueError("JPEG scan not found")


def main():
    original = SOURCE.read_bytes()
    prepared, width, height = prepare(original)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DIMENSIONS.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(prepared)
    DIMENSIONS.write_text(f"width: {width}\nheight: {height}\n")
    print(f"Portrait: {width}x{height}, {len(original)} -> {len(prepared)} bytes; pixels unchanged")


if __name__ == "__main__":
    main()
