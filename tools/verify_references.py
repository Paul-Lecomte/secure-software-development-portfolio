"""Verify every source reference in the portfolio against the pinned commits.

Each `file:line` or `file:start-end` reference in the HTML docs is resolved
against the ORIGINAL (pre-fix) commit of the corresponding repository, because
the audit observations describe the code as it was audited.

Run:  python tools/verify_references.py
Exit code 0 = every reference resolves to a real line in the pinned commit.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BACKEND = Path(r"C:\Users\lecom\audit-work\backend")
BACKEND_COMMIT = "90a50769c4c2013f8e2f7d0241d883cc7b3befd2"

FRONTEND = Path(r"C:\Users\lecom\audit-work\frontend-swiss-pb-map")
FRONTEND_COMMIT = "610e4342f747d03b68c11bc281b7830abda047ac"

# Reference file stem -> (repo root, commit, candidate paths)
REPOS: dict[str, tuple[Path, str, list[str]]] = {
    "http_server": (BACKEND, BACKEND_COMMIT, ["src/http_server.py"]),
    "config": (BACKEND, BACKEND_COMMIT, ["src/config.py"]),
    "server": (BACKEND, BACKEND_COMMIT, ["src/server.py"]),
    "loader": (BACKEND, BACKEND_COMMIT, ["src/loader.py"]),
    "server.js": (FRONTEND, FRONTEND_COMMIT, ["backend/server.js"]),
}

# Expected content of the FIRST line of each referenced range (case-insensitive).
# This asserts the reference points at the construct the prose describes.
EXPECTED_FIRST_LINE: dict[tuple[str, int], str] = {
    ("config", 31): "NEO4J_URI",
    ("server", 305): "add_insecure_port",
    ("loader", 598): "allow_pickle",
    ("loader", 922): "pickle.load",
    ("http_server", 3283): "self.rfile.read(length)",
    ("http_server", 3111): "departure_time",
    ("http_server", 3116): "max_transfers",
    ("http_server", 3106): "algorithm",
    ("server.js", 22): "helmet",
}

# Range endpoints that must also contain the expected token (last line of range).
EXPECTED_LAST_LINE: dict[tuple[str, int, int], str] = {
    ("config", 31, 34): "NEO4J_PASSWORD",
    ("http_server", 3116, 3140): "option_count",
    ("http_server", 3106, 3140): "option_count",
    ("http_server", 3111, 3140): "option_count",
    ("server.js", 22, 27): "cookieParser",
}

REF_RE = re.compile(
    r"<code>([A-Za-z0-9_./-]+\.(?:py|js|jsx|ts|tsx)):(\d+)(?:-(\d+))?</code>"
)

_cache: dict[tuple[str, str], list[str]] = {}


def blob(repo: Path, commit: str, path: str) -> list[str]:
    key = (str(repo), path)
    if key not in _cache:
        out = subprocess.run(
            ["git", "show", f"{commit}:{path}"],
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if out.returncode != 0:
            raise FileNotFoundError(f"{path} not found at {commit}")
        _cache[key] = out.stdout.splitlines()
    return _cache[key]


def resolve(stem: str) -> tuple[Path, str, list[str]] | None:
    """Map a reference file name (e.g. 'http_server.py') to its repo/commit.

    Precedence, so that 'server.js' is never captured by the backend module
    'server.py' (a different base name):
      1. exact file-name match  ('server.js' -> frontend)
      2. exact base-name match  ('http_server'  -> backend)
      3. longest suffix match   ('src/http_server.py' -> backend)
    """
    bare = stem.rsplit(".", 1)[0]

    for key, value in REPOS.items():          # 1. exact file name
        if stem == key:
            return value
    for key, value in REPOS.items():          # 2. exact base name
        if bare == key:
            return value
    for key, value in sorted(REPOS.items(), key=lambda kv: -len(kv[0])):  # 3. suffix
        if stem.endswith(key) or bare.endswith(key):
            return value
    return None


def main() -> int:
    failures: list[str] = []
    checked = 0
    seen: set[tuple[str, int, int]] = set()

    for doc in sorted(ROOT.rglob("*.html")):
        text = doc.read_text(encoding="utf-8", errors="replace")
        rel = doc.relative_to(ROOT).as_posix()
        for m in REF_RE.finditer(text):
            raw_path, start_s, end_s = m.group(1), int(m.group(2)), m.group(3)
            start = start_s
            end = int(end_s) if end_s else start
            stem = raw_path.split("/")[-1]
            checked += 1
            key = (stem, start, end)
            if key in seen:
                continue
            seen.add(key)

            resolved = resolve(stem)
            if resolved is None:
                failures.append(f"{rel}: unknown repo for reference {raw_path}")
                continue
            repo, commit, candidates = resolved

            lines = None
            used = None
            for cand in candidates:
                try:
                    lines = blob(repo, commit, cand)
                    used = cand
                    break
                except FileNotFoundError:
                    continue
            if lines is None:
                failures.append(f"{rel}: {raw_path} not found in {commit}")
                continue

            if end > len(lines):
                failures.append(
                    f"{rel}: {raw_path}:{start}-{end} exceeds file length {len(lines)}"
                )
                continue

            first = lines[start - 1].strip()
            print(f"  {rel}\n      {used}:{start}-{end}\n        first: {first[:88]}")

            exp = EXPECTED_FIRST_LINE.get((stem, start))
            if exp and exp.lower() not in first.lower():
                failures.append(
                    f"{rel}: {raw_path}:{start} expected {exp!r}, got {first!r}"
                )
            exp_last = EXPECTED_LAST_LINE.get((stem, start, end))
            if exp_last:
                last = lines[end - 1].strip()
                print(f"        last:  {last[:88]}")
                if exp_last.lower() not in last.lower():
                    failures.append(
                        f"{rel}: {raw_path}:{end} expected {exp_last!r}, got {last!r}"
                    )

    print()
    if failures:
        print(f"{len(failures)} failure(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"All {checked} source references resolve correctly at the pinned commits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
