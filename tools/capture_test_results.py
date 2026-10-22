"""Regenerate evidence/test-results/pytest-results.txt as UTF-8 from pytest runs.

Captures both the baseline run (smoke tests only, i.e. the state before the
fix) and the post-fix run (smoke + request-limit tests), so that the timings
quoted in the portfolio match the captured evidence file exactly.

Run:  python tools/capture_test_results.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BACKEND = Path(r"C:\Users\lecom\audit-work\backend")
OUT = Path(
    r"C:\Users\lecom\OneDrive\Images\Essex_University\year_1\module"
    r"\Secure Software Developement\secure-software-development-portfolio"
    r"\evidence\test-results\pytest-results.txt"
)

RUNS = [
    (
        "BASELINE — tests/test_smoke.py (pre-fix behaviour, no size limit in place)",
        ["tests/test_smoke.py"],
    ),
    (
        "AFTER FIX — tests/test_smoke.py + tests/test_request_limits.py",
        ["tests/test_smoke.py", "tests/test_request_limits.py"],
    ),
]


def run(args: list[str]) -> str:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *args, "-v"],
        cwd=BACKEND,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.stdout + proc.stderr


def main() -> int:
    chunks: list[str] = []
    failures = 0

    for label, args in RUNS:
        output = run(args)
        chunks.append("=" * 78)
        chunks.append(label)
        chunks.append("=" * 78)
        chunks.append(output.rstrip())
        chunks.append("")

        summary = output.strip().splitlines()[-1] if output.strip() else "(no output)"
        print(f"{label}\n  -> {summary}\n")
        if "failed" in summary.lower() or "error" in summary.lower():
            failures += 1

    header = [
        "Raw pytest output for the request-body size ceiling (MAX_REQUEST_BODY_BYTES).",
        "Repository: fastest_path_backend @ 90a50769c4c2013f8e2f7d0241d883cc7b3befd2",
        "Python 3.12.10 (win32) | pytest 9.1.1 | Windows",
        "Encoding: UTF-8",
        "",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(header + chunks).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"written: {OUT} ({OUT.stat().st_size} bytes)")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
