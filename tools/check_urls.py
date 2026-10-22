"""Check every external URL cited in the portfolio still resolves.

Run:  python tools/check_urls.py
Exit code 0 = every URL reachable (2xx after redirects).
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from site_files import site_files

ROOT = Path(__file__).resolve().parent.parent

URL_RE = re.compile(r"https?://[^\s<>\"'\)]+")
# Trailing punctuation that can be picked up from prose.
TRIM = ".,;:"

SKIP_HOSTS = {
    "localhost",
    "127.0.0.1",
}

# URLs that are expected to be unreachable until the portfolio is published.
PENDING = {
    "https://paul-lecomte.github.io/secure-software-development-portfolio",
}


def clean(url: str) -> str:
    """Strip markdown/code-span punctuation that a naive regex picks up."""
    url = url.rstrip(TRIM)
    # Markdown code spans and emphasis: `url` **url** _url_
    url = url.strip("`*_")
    return url


def fetch(url: str, timeout: int = 30) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (portfolio link checker)"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return resp.status, resp.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc)
    except Exception as exc:  # noqa: BLE001 - report any transport failure
        return 0, f"{type(exc).__name__}: {exc}"


def main() -> int:
    urls: set[str] = set()
    for path in site_files("*.html", "*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in URL_RE.finditer(text):
            url = clean(m.group(0))
            if any(host in url for host in SKIP_HOSTS):
                continue
            urls.add(url)

    print(f"Checking {len(urls)} external URL(s)\n")
    failures = []
    pending = 0
    pending_set = {p.lower().rstrip("/") for p in PENDING}
    for url in sorted(urls):
        if url.lower().rstrip("/") in pending_set:
            pending += 1
            print(f"  NEW  ---  {url}  (live once the site is published)")
            continue
        status, detail = fetch(url)
        ok = 200 <= status < 400
        print(f"  {'OK ' if ok else 'BAD'}  {status:>3}  {url}")
        if not ok:
            failures.append(f"{url} -> {status} {detail}")

    print()
    if failures:
        print(f"{len(failures)} unreachable URL(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(
        f"All {len(urls) - pending} external URLs are reachable "
        f"({pending} pending publication)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
