"""Check local page, image, stylesheet, and script targets in a Jekyll build."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src') and value:
                self.urls.append(value)


def check(root):
    errors = []
    pages = list(root.rglob('*.html'))
    if not pages:
        return ['No generated HTML found; run Jekyll first.']
    for page in pages:
        parser = Links()
        parser.feed(page.read_text())
        for url in parser.urls:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            path = unquote(parts.path)
            target = root / path.lstrip('/') if path.startswith('/') else page.parent / path
            if not target.is_file() and not (target / 'index.html').is_file():
                errors.append(f'{page.relative_to(root)}: missing {url}')
    return errors


if __name__ == '__main__':
    errors = check(Path(sys.argv[1] if len(sys.argv) > 1 else '_site'))
    for error in errors:
        print(error)
    if errors:
        sys.exit(1)
    print('All internal file targets exist.')
