"""Regenerate evidence/test-results/pytest-results.txt as UTF-8 from a pytest run."""
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

proc = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_smoke.py", "tests/test_request_limits.py", "-v"],
    cwd=BACKEND,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)
raw = proc.stdout + proc.stderr
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(raw, encoding="utf-8", newline="\n")
print("exit code:", proc.returncode)
print("last line:", raw.strip().splitlines()[-1])
print("written:", OUT, OUT.stat().st_size, "bytes")
