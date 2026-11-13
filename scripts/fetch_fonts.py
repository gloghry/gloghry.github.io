"""Fetch pinned, verified fonts for local preview and GitHub Pages builds."""
from hashlib import sha1
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

REVISION = "7925f50f649b3813257faf2f4c0b381011f434f1"
SOURCE = f"https://raw.githubusercontent.com/googlefonts/atkinson-hyperlegible-next/{REVISION}/fonts/webfonts/"
FONTS = (
    ("AtkinsonHyperlegibleNext[wght].woff2", "atkinson-hyperlegible-next-normal.woff2",
     "626791adce3ab62b0a8deb7d778d91a069a65ccc"),
    ("AtkinsonHyperlegibleNext-Italic[wght].woff2", "atkinson-hyperlegible-next-italic.woff2",
     "333b0428766ff999de5cb1c0cab16dbceae27658"),
)


def verify(data, expected):
    # Git blob IDs include the type and byte length before the unmodified bytes.
    digest = sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if digest != expected or not data.startswith(b"wOF2"):
        raise ValueError("Font download does not match the pinned WOFF2 asset")


def main():
    destination = Path(__file__).resolve().parents[1] / "assets" / "fonts"
    destination.mkdir(parents=True, exist_ok=True)
    for source, filename, expected in FONTS:
        target = destination / filename
        if target.exists():
            verify(target.read_bytes(), expected)
            print(f"Verified {filename}")
            continue
        with urlopen(SOURCE + quote(source), timeout=60) as response:
            data = response.read()
        verify(data, expected)
        target.write_bytes(data)
        print(f"Downloaded and verified {filename} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
