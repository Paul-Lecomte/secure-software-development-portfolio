"""Serve the portfolio locally and assert every published path returns HTTP 200.

Run:  python tools/check_served.py [port]
Exits non-zero if any expected path fails.
"""
from __future__ import annotations

import functools
import http.server
import socket
import sys
import threading
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent

EXPECTED = [
    "/",
    "/index.html",
    "/docs/learning-outcomes.html",
    "/docs/system-overview.html",
    "/docs/threat-model.html",
    "/docs/risk-assessment.html",
    "/docs/secure-design.html",
    "/docs/implementation.html",
    "/docs/security-testing.html",
    "/docs/critical-evaluation.html",
    "/docs/references.html",
    "/discussions/discussion-summary-1.html",
    "/discussions/discussion-summary-2.html",
    "/professional-development/reflection.html",
    "/professional-development/meeting-notes.html",
    "/professional-development/peer-and-tutor-feedback.html",
    "/professional-development/professional-skills-matrix.html",
    "/professional-development/personal-development-plan.html",
    "/evidence/README.html",
    "/evidence/test-results/index.html",
    "/evidence/test-results/results.md",
    "/evidence/test-results/pytest-results.txt",
    "/assets/styles/main.css",
    "/assets/scripts/main.js",
    "/assets/diagrams/favicon.svg",
    "/robots.txt",
    "/README.md",
    "/LICENSE",
    "/.nojekyll",
]


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else free_port()
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(ROOT)
    )
    # Silence the default per-request stderr logging.
    handler.log_message = lambda *args, **kwargs: None  # type: ignore[attr-defined]
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base = f"http://127.0.0.1:{port}"
    failures = []
    for path in EXPECTED:
        try:
            with urlopen(base + path, timeout=10) as resp:
                body = resp.read()
                status = resp.status
            print(f"  {status}  {len(body):>7} B  {path}")
            if status != 200:
                failures.append(f"{path} -> HTTP {status}")
            if path.endswith(".html") and b"</html>" not in body.lower():
                failures.append(f"{path} -> truncated HTML")
        except HTTPError as exc:
            print(f"  {exc.code}  {'-':>7}    {path}")
            failures.append(f"{path} -> HTTP {exc.code}")
        except URLError as exc:
            print(f"  ERR        {path} ({exc.reason})")
            failures.append(f"{path} -> {exc.reason}")

    server.shutdown()

    print()
    if failures:
        print(f"{len(failures)} failure(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"All {len(EXPECTED)} paths served successfully on {base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
