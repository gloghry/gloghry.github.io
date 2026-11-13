"""Check internal file targets using the deployed site's URL semantics."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import posixpath
from urllib.parse import unquote, urljoin, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src') and value:
                self.urls.append(value)


def check(root, baseurl=''):
    root = root.resolve()
    base = '/' + baseurl.strip('/') if baseurl.strip('/') else ''
    errors = []
    pages = list(root.rglob('*.html'))
    if not pages:
        return ['No generated HTML found; run Jekyll first.']
    for page in pages:
        parser = Links()
        parser.feed(page.read_text())
        relative = page.relative_to(root).as_posix()
        # Jekyll serves directory index pages at a trailing-slash URL.
        if page.name == 'index.html':
            relative = relative[:-len('index.html')]
        page_url = f'https://site.invalid{base}/{relative}'
        for url in parser.urls:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            resolved = urlsplit(urljoin(page_url, url))
            # Normalize at the URL root, never relative to the checkout.
            decoded_path = unquote(resolved.path)
            requires_index = decoded_path.endswith(('/', '/.', '/..'))
            path = posixpath.normpath('/' + decoded_path.lstrip('/'))
            if base and path != base and not path.startswith(base + '/'):
                errors.append(f'{page.relative_to(root)}: outside base path {url}')
                continue
            artifact_path = path[len(base):].lstrip('/')
            target = (root / artifact_path).resolve()
            if not target.is_relative_to(root):
                errors.append(f'{page.relative_to(root)}: outside artifact {url}')
            elif not ((target / 'index.html').is_file() if requires_index
                      else target.is_file() or (target / 'index.html').is_file()):
                errors.append(f'{page.relative_to(root)}: missing {url}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='_site')
    parser.add_argument('--baseurl', default='')
    args = parser.parse_args()
    errors = check(Path(args.root), args.baseurl)
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print('All internal file targets exist.')
