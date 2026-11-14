#!/usr/bin/env python3
"""Build a public, non-indexable Cloudflare Pages review copy."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent


def preview_origin(value):
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname
            or not parsed.hostname.endswith(".pages.dev")
            or parsed.netloc != parsed.hostname
            or parsed.path not in ("", "/") or parsed.query or parsed.fragment):
        raise ValueError("Preview URL must be an HTTPS pages.dev origin without credentials or a path")
    return "https://" + parsed.hostname


def preview_baseurl(value):
    if value and not re.fullmatch(r"(?:/[A-Za-z0-9_-]+)+", value):
        raise ValueError("Base URL must be empty or a path such as /portfolio without a trailing slash")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=os.environ.get("CF_PAGES_URL", ""))
    parser.add_argument("--baseurl", default=os.environ.get("SITE_BASEURL", ""))
    parser.add_argument("--destination", default="_site")
    args = parser.parse_args()
    try:
        origin = preview_origin(args.url)
        baseurl = preview_baseurl(args.baseurl)
    except ValueError as error:
        parser.error(str(error))
    destination = Path(args.destination).resolve()
    environment = dict(os.environ, JEKYLL_ENV="production")
    for helper in ("fetch_fonts.py", "prepare_portrait.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / helper)],
                       cwd=ROOT, env=environment, check=True)
    # JSON is valid YAML. Keep overrides outside the source/output tree.
    with tempfile.TemporaryDirectory(prefix="site-preview-") as temporary:
        config = Path(temporary) / "preview.yml"
        config.write_text(json.dumps({
            "url": origin, "baseurl": baseurl, "preview": True,
            "production_url": "https://garettloghry.com",
        }), encoding="utf-8")
        subprocess.run([
            "bundle", "exec", "jekyll", "build", "--trace",
            "--config", str(ROOT / "_config.yml") + "," + str(config),
            "--destination", str(destination),
        ], cwd=ROOT, env=environment, check=True)
    # GitHub Pages output never gets this preview-only file.
    (destination / "_headers").write_text(
        "/*\n  X-Robots-Tag: noindex, nofollow\n", encoding="utf-8")
    subprocess.run([
        sys.executable, str(ROOT / "scripts" / "check_links.py"),
        str(destination), "--baseurl", baseurl,
    ], cwd=ROOT, check=True)
    subprocess.run([
        sys.executable, str(ROOT / "scripts" / "check_preview.py"),
        str(destination), "--url", origin, "--baseurl", baseurl,
    ], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
