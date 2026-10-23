"""
build_site.py — assemble the exact set of files that may be published.

GitHub Pages' legacy build publishes every file in the repository, which
exposes build tooling (tools/*.py) and repository metadata (.gitattributes,
.gitignore, _config.yml) on the public site. This script copies an explicit
allow-list of files into a staging directory so that only the site itself is
published.

The allow-list is cross-checked against the paths asserted by
tools/check_served.py, so the published tree and the served-path contract
cannot drift apart.

Run:  python tools/build_site.py [output_dir]
Exit code 0 = staging directory built and consistent, 1 = problems found.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_served import EXPECTED  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Files published verbatim at the site root.
ROOT_FILES = [
    "index.html",
    "robots.txt",
    "README.md",
    "LICENSE",
    ".nojekyll",
]

# Directories published wholesale (every file beneath them).
ROOT_DIRS = [
    "assets",
    "assignments",
    "docs",
    "discussions",
    "modules",
    "professional-development",
]

# Individual files published from nested directories.
NESTED_FILES = [
    "evidence/README.html",
    "evidence/test-results/index.html",
    "evidence/test-results/results.md",
    "evidence/test-results/pytest-results.txt",
]


def expected_files() -> set[str]:
    """Map the served-path contract onto the concrete files it needs."""
    files = set(ROOT_FILES) | set(NESTED_FILES)
    for path in EXPECTED:
        rel = path.lstrip("/")
        if not rel or rel.endswith("/"):
            continue
        files.add(rel)
    return files


def collect() -> list[Path]:
    """Return every file that should be published, in a stable order."""
    found: list[Path] = []
    for rel in ROOT_FILES:
        found.append(ROOT / rel)
    for rel in NESTED_FILES:
        found.append(ROOT / rel)
    for directory in ROOT_DIRS:
        base = ROOT / directory
        found.extend(sorted(p for p in base.rglob("*") if p.is_file()))
    return found


def check_consistency(files: set[str]) -> list[str]:
    """Verify the allow-list and the served-path contract agree."""
    problems: list[str] = []

    expected = expected_files()
    for missing in sorted(expected - files):
        problems.append(f"allow-list is missing served path: {missing}")
    for extra in sorted(files - expected):
        problems.append(f"published file is not in the served-path contract: {extra}")

    # Nothing from the repository metadata or tooling may be published.
    for prefix in ("tools/", ".github/", ".git"):
        for name in sorted(files):
            if name == prefix or name.startswith(prefix):
                problems.append(f"tooling or metadata must not be published: {name}")

    return problems


def build(output_dir: Path) -> tuple[list[str], int]:
    """Copy the allow-list into output_dir and return (problems, file count)."""
    sources = collect()
    files = {p.relative_to(ROOT).as_posix() for p in sources}
    problems = check_consistency(files)

    for path in sources:
        if not path.is_file():
            problems.append(f"source file does not exist: {path.relative_to(ROOT)}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    copied = 0
    for src in sources:
        if not src.is_file():
            continue
        dst = output_dir / src.relative_to(ROOT)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1

    return problems, copied


def main() -> int:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
    problems, copied = build(output_dir)

    print(f"Staged {copied} file(s) into {output_dir}")
    print()

    if problems:
        print(f"{len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print(f"Publish set matches the {len(EXPECTED)} served paths.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
