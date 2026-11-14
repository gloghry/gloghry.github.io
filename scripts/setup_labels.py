#!/usr/bin/env python3
"""Create missing repository labels using an authenticated GitHub CLI."""
import json
import subprocess

REPOSITORY = "gloghry/gloghry.github.io"
LABELS = [
    ("enhancement", "a2eeef", "New functionality or a meaningful improvement"),
    ("bug", "d73a4a", "Correcting unintended behavior"),
    ("documentation", "0075ca", "Documentation or agent guidance"),
    ("maintenance", "ededed", "Dependencies, build tooling, or repository upkeep"),
    ("accessibility", "7057ff", "Removing an accessibility barrier"),
    ("priority:P0", "b60205", "Highest priority; mirrors the linked issue"),
    ("priority:P1", "d93f0b", "Near-term work; mirrors the linked issue"),
    ("priority:P2", "fbca04", "Follow-up work; mirrors the linked issue"),
    ("priority:P3", "c5def5", "Optional exploration; mirrors the linked issue"),
]


def main():
    # Paginate before creating anything so existing/customized labels are reused.
    response = subprocess.run(
        ["gh", "api", "--paginate", "--slurp",
         f"repos/{REPOSITORY}/labels?per_page=100"],
        check=True, capture_output=True, text=True,
    )
    pages = json.loads(response.stdout)
    existing = {label["name"].casefold() for page in pages for label in page}
    for name, color, description in LABELS:
        if name.casefold() in existing:
            print(f"Keep existing label: {name}", flush=True)
            continue
        subprocess.run(
            ["gh", "api", "--method", "POST", f"repos/{REPOSITORY}/labels",
             "-f", f"name={name}", "-f", f"color={color}",
             "-f", f"description={description}"],
            check=True, stdout=subprocess.DEVNULL,
        )
        print(f"Created label: {name}", flush=True)


if __name__ == "__main__":
    main()
