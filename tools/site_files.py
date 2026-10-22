"""Shared file-discovery helpers for the portfolio tooling.

The repository root doubles as the site root, so every scanner must skip
build artifacts (`_site/`), VCS metadata (`.git/`), the workflow definitions
(`.github/`) and the tooling itself (`tools/`). Otherwise a locally staged
build would be scanned a second time as if it were authored source.

Run:  python tools/site_files.py   (lists the discovered site files)
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories that are never part of the authored site.
SKIP_DIRS = {".git", ".github", "_site", "tools", "node_modules"}


def site_files(*patterns: str) -> list[Path]:
    """Return repository files matching any pattern, excluding tooling/artifacts."""
    found: set[Path] = set()
    for pattern in patterns:
        for path in ROOT.rglob(pattern):
            if SKIP_DIRS.intersection(path.relative_to(ROOT).parts):
                continue
            if path.is_file():
                found.add(path)
    return sorted(found)


if __name__ == "__main__":
    for path in site_files("*.html", "*.md", "*.txt", "*.css", "*.js"):
        print(path.relative_to(ROOT).as_posix())
