#!/usr/bin/env python3
"""Check generated preview metadata and deployment headers."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.robots = []
        self.canonical = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "meta" and values.get("name") == "robots":
            self.robots.append(values.get("content", ""))
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical.append(values.get("href", ""))


def check(directory, origin, baseurl):
    directory = Path(directory)
    headers = (directory / "_headers").read_text(encoding="utf-8")
    if headers != "/*\n  X-Robots-Tag: noindex, nofollow\n":
        raise ValueError("Missing wildcard noindex header")
    pages = list(directory.rglob("*.html"))
    if not pages:
        raise ValueError("No preview HTML found")
    for page in pages:
        metadata = Metadata()
        metadata.feed(page.read_text(encoding="utf-8"))
        if not any("noindex" in content.split(", ") for content in metadata.robots):
            raise ValueError(f"Missing preview noindex: {page}")
        if (len(metadata.canonical) != 1 or
                not metadata.canonical[0].startswith("https://garettloghry.com/")):
            raise ValueError(f"Unexpected production canonical: {page}")
    atom = {"a": "http://www.w3.org/2005/Atom"}
    feed = ET.parse(directory / "feed.xml")
    self_links = [element.get("href") for element in feed.findall("a:link", atom)
                  if element.get("rel") == "self"]
    if self_links != [origin + baseurl + "/feed.xml"]:
        raise ValueError(f"Preview feed points outside the preview: {self_links}")
    sitemap = ET.parse(directory / "sitemap.xml")
    for location in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        if not location.text.startswith(origin + baseurl + "/"):
            raise ValueError(f"Sitemap URL outside preview: {location.text}")
    for private in ("AGENTS.md", "CONTRIBUTING.md", "docs", "scripts", "_drafts",
                    "assets/images/originals"):
        if (directory / private).exists():
            raise ValueError(f"Internal source published: {private}")
    print(f"Preview metadata and exclusions passed for {len(pages)} pages at {origin}{baseurl}/")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("--url", required=True)
    parser.add_argument("--baseurl", default="")
    args = parser.parse_args()
    check(args.directory, args.url, args.baseurl)


if __name__ == "__main__":
    main()
