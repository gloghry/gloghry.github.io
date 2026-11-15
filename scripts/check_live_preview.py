"""Disposable public-HTTP check for issue #44; never merge this test."""
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import re

PREVIEW = "https://44-preview-verification.gloghry-github-io.pages.dev"


def fetch(url):
    try:
        request = Request(url, headers={
            "User-Agent": "GarettLoghry-PreviewCheck/1.0 (+https://github.com/gloghry/gloghry.github.io/issues/44)",
            "Accept": "text/html,application/xml;q=0.9,*/*;q=0.8",
        })
        with urlopen(request, timeout=20) as response:
            return response.status, response.headers, response.read().decode("utf-8")
    except HTTPError as error:
        print("HTTP failure URL:", url, "status:", error.code, flush=True)
        for name in ("server", "cf-mitigated", "cf-ray", "content-type", "via", "x-mitmproxy-blocked-reason"):
            print(name + ":", error.headers.get(name, "(absent)"), flush=True)
        body = error.read().decode("utf-8", errors="replace")
        if error.headers.get("content-type", "").startswith("text/plain"):
            print("Public error text:", body[:500], flush=True)
        title = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
        print("Error page title:", title.group(1)[:300] if title else "(none)", flush=True)
        raise


for probe in ("https://gloghry-github-io.pages.dev/",
              "https://68c123e7.gloghry-github-io.pages.dev/preview-check/",
              "https://a32107aa.gloghry-github-io.pages.dev/preview-check/"):
    try:
        probe_status, _, _ = fetch(probe)
        print("Probe", probe, probe_status, flush=True)
    except HTTPError:
        pass

status, headers, page = fetch(PREVIEW + "/preview-check/")
assert "Preview test version B." in page, "Branch alias did not serve version B"

status, old_headers, old_page = fetch("https://68c123e7.gloghry-github-io.pages.dev/preview-check/")
assert "Preview test version A." in old_page
assert "Preview test version B." not in old_page
print("PASS immutable deployment A retains version A")

for path in ("/", "/about/", "/resume/", "/preview-check/"):
    status, headers, page = fetch(PREVIEW + path)
    assert status == 200
    assert "noindex" in headers.get("X-Robots-Tag", ""), path + " missing noindex header"
    assert '<meta name="robots" content="noindex, nofollow">' in page
    assert 'rel="canonical" href="https://garettloghry.com' in page
    print("PASS preview HTTP/indexing safeguards: " + path)
for path in ("/feed.xml", "/sitemap.xml"):
    status, headers, text = fetch(PREVIEW + path)
    assert "noindex" in headers.get("X-Robots-Tag", "")
    assert ".pages.dev" in text
    print("PASS preview metadata URL/header: " + path)
status, headers, text = fetch("https://garettloghry.com/")
assert "noindex" not in headers.get("X-Robots-Tag", "").lower()
assert '<meta name="robots" content="noindex' not in text
assert "Preview test version" not in text
print("PASS production remains independent and indexable")
print("PASS preview alias updated to version B")
