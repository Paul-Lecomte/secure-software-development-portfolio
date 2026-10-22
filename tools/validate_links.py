"""
validate_links.py — offline validator for the e-portfolio static site.

Checks every HTML file for:
  1. Broken internal links (href/src) that do not resolve to a file on disk.
  2. Broken in-page anchors (#id) that have no matching id in the target document.
  3. Missing <title>, <meta charset>, <meta viewport> and <html lang>.
  4. Unclosed / mismatched common HTML tags.
  5. Images without alt text.
  6. Relative-path assets referenced by <link> and <script>.

Run:  python tools/validate_links.py
Exit code 0 = all checks pass, 1 = problems found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from site_files import site_files

ROOT = Path(__file__).resolve().parent.parent

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Tags we deliberately do not balance-check (may legitimately contain raw text).
SKIP_BALANCE = {"script", "style", "pre", "textarea"}

HREF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
ID_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
TAG_RE = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>")
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)

problems: list[str] = []
checked_links = 0
checked_files = 0


def fail(msg: str) -> None:
    problems.append(msg)


def resolve(base: Path, href: str) -> Path | None:
    """Resolve a relative href against the file's directory; None if external."""
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        return None
    raw = unquote(parsed.path)
    if not raw:
        return base  # pure anchor
    return (base.parent / raw).resolve()


def ids_in(path: Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return {m.group(1) for m in ID_RE.finditer(text)}


def check_anchors(doc: Path, target: Path) -> None:
    fragment = urlparse("").fragment
    return


def validate_file(doc: Path) -> None:
    global checked_links
    text = doc.read_text(encoding="utf-8", errors="replace")
    rel = doc.relative_to(ROOT).as_posix()

    # --- 3. Required head elements ---
    if not re.search(r"<html[^>]*\blang\s*=", text, re.IGNORECASE):
        fail(f"{rel}: <html> is missing a lang attribute")
    if not re.search(r"<meta[^>]*charset", text, re.IGNORECASE):
        fail(f"{rel}: missing <meta charset>")
    if not re.search(r"<meta[^>]*name=[\"']viewport[\"']", text, re.IGNORECASE):
        fail(f"{rel}: missing <meta name=\"viewport\">")
    if not TITLE_RE.search(text):
        fail(f"{rel}: missing <title>")

    # --- 4. Tag balance + content model (single pass) ---
    #
    # ALLOWED_PARENTS encodes the HTML content model for the elements used in
    # this site. It catches mistakes such as a <td> placed inside a <ul>.
    ALLOWED_PARENTS: dict[str, set[str]] = {
        "td": {"tr"},
        "th": {"tr"},
        "tr": {"table", "thead", "tbody", "tfoot"},
        "li": {"ul", "ol"},
        "dt": {"dl"},
        "dd": {"dl"},
    }

    stack: list[str] = []
    for m in TAG_RE.finditer(text):
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if name in SKIP_BALANCE or name in VOID_TAGS:
            continue
        self_closing = attrs.rstrip().endswith("/")

        if closing:
            if not stack:
                fail(f"{rel}: stray closing </{name}>")
            elif stack[-1] != name:
                fail(f"{rel}: </{name}> closes <{stack[-1]}>")
                stack.pop()
            else:
                stack.pop()
            continue

        if name in ALLOWED_PARENTS:
            parent = stack[-1] if stack else None
            allowed = ALLOWED_PARENTS[name]
            if parent not in allowed:
                fail(
                    f"{rel}: <{name}> is not allowed inside <{parent}> "
                    f"(expected one of {sorted(allowed)})"
                )

        if not self_closing:
            stack.append(name)

    for leftover in stack:
        fail(f"{rel}: unclosed <{leftover}>")

    # --- 5. Images need alt text ---
    for m in IMG_RE.finditer(text):
        if not re.search(r"\balt\s*=", m.group(0), re.IGNORECASE):
            fail(f"{rel}: <img> without alt attribute: {m.group(0)[:60]}")

    # --- 1 & 2. Links ---
    for m in HREF_RE.finditer(text):
        href = m.group(1).strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        checked_links += 1
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc:
            continue  # external link — not checkable offline
        raw = unquote(parsed.path)
        if raw:
            target = (doc.parent / raw).resolve()
            if raw.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                fail(f"{rel}: broken link -> {href}")
                continue
        else:
            target = doc
        # anchor check against the resolved target document
        if parsed.fragment:
            if target.suffix.lower() in {".html", ".htm"}:
                if parsed.fragment not in ids_in(target):
                    fail(f"{rel}: anchor #{parsed.fragment} not found in {target.relative_to(ROOT).as_posix()}")


def main() -> int:
    global checked_files
    html_files = site_files("*.html")
    if not html_files:
        print("No HTML files found.")
        return 1

    for doc in html_files:
        checked_files += 1
        validate_file(doc)

    print(f"Checked {checked_files} HTML file(s) and {checked_links} internal link(s).")
    if problems:
        print(f"\n{len(problems)} problem(s) found:\n")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("All checks passed: no broken links, no structural problems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
