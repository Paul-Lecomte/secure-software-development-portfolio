"""Detect and repair double-encoded (mojibake) UTF-8 in the portfolio files.

Some files were written through a Windows-1252 round-trip, which turns UTF-8
byte sequences into visible garbage such as "â€”" (an em dash) or "â€™"
(a right single quote). This script finds those sequences and rewrites them
using proper HTML entities.

Run:  python tools/fix_encoding.py          # report only
      python tools/fix_encoding.py --write  # repair in place
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = (*ROOT.rglob("*.html"), *ROOT.rglob("*.md"), *ROOT.rglob("*.txt"))

# Mojibake sequence -> correct HTML entity (or literal).
REPLACEMENTS: list[tuple[str, str]] = [
    ("â€”", "&mdash;"),   # em dash
    ("â€“", "&ndash;"),   # en dash
    ("â€˜", "&lsquo;"),   # left single quote
    ("â€™", "&rsquo;"),   # right single quote
    ("â€œ", "&ldquo;"),  # left double quote
    ("â€", "&rdquo;"),  # right double quote
    ("â€¦", "&hellip;"),  # ellipsis
    ("â€¢", "&bull;"),    # bullet
    ("â€™", "&rsquo;"),
    ("Â ", " "),          # non-breaking space artefacts
    ("Â", ""),            # stray 'Â'
]


def main() -> int:
    write = "--write" in sys.argv
    changed: list[str] = []
    total = 0

    for path in TARGETS:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        original = text
        for bad, good in REPLACEMENTS:
            if bad in text:
                count = text.count(bad)
                total += count
                text = text.replace(bad, good)
                print(f"  {path.relative_to(ROOT).as_posix()}: {count} x {bad!r}")
        if text != original:
            changed.append(path.relative_to(ROOT).as_posix())
            if write:
                path.write_text(text, encoding="utf-8", newline="\n")

    print()
    if not changed:
        print("No mojibake found.")
        return 0
    print(f"{total} replacement(s) across {len(changed)} file(s):")
    for c in changed:
        print(f"  - {c}")
    if not write:
        print("\nRe-run with --write to apply the repairs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
