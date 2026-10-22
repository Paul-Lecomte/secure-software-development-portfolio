"""Extract every source reference (file:line) from the portfolio HTML docs.

Run:  python tools/list_references.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# e.g. <code>src/config.py:31-34</code> or loader.py:598
REF_RE = re.compile(
    r"<code>([A-Za-z0-9_./-]+\.(?:py|js|jsx|ts|tsx)):(\d+)(?:-(\d+))?</code>"
)


def main() -> int:
    found = False
    for doc in sorted(ROOT.rglob("*.html")):
        text = doc.read_text(encoding="utf-8", errors="replace")
        for m in REF_RE.finditer(text):
            found = True
            rel = doc.relative_to(ROOT).as_posix()
            end = m.group(3) or m.group(2)
            print(f"{rel}\t{m.group(1)}:{m.group(2)}-{end}")
    if not found:
        print("No source references found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
