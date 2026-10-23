"""
update_nav.py — regenerate the site navigation in every HTML page.

The portfolio is organised by MSc MODULE first, then by ASSIGNMENT within
each module. Every page exposes the same navigation structure so a reader can
move between modules and their assignments, whichever page they arrive from.

Navigation order on every page:
  1. Modules          — all 5 MSc modules
  2. Assignments      — assignments for the current module (context-dependent)
  3. Assessment artefacts
  4. Collaboration
  5. Professional development
  6. Evidence
  7. Repositories (external)

The navigation is generated here (rather than hand-written in 20+ files) so
the link graph cannot drift: every page gets the same targets, with paths
rewritten relative to that page's depth.

Run:  python tools/update_nav.py          (rewrite every page)
      python tools/update_nav.py --check   (report pages that are out of date)
Exit code 0 = navigation is up to date, 1 = drift found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", ".github", "_site", "_site_test", "tools", "node_modules", "__pycache__"}

# (label, target path relative to the site root)
MODULES: list[tuple[str, str]] = [
    ("Portfolio home", "index.html"),
    ("Secure Software Development", "modules/secure-software-development/index.html"),
    ("Object Oriented Programming", "modules/object-oriented-programming/index.html"),
    ("Security Risk Management", "modules/security-risk-management/index.html"),
    ("Software Engineering Project Management", "modules/software-engineering-project-management/index.html"),
    ("Research Methods &amp; Professional Practice", "modules/research-methods-and-professional-practice/index.html"),
]

# Module slug -> list of (label, target path)
MODULE_ASSIGNMENTS: dict[str, list[tuple[str, str]]] = {
    "secure-software-development": [
        ("Assessment 1 — security risks", "assignments/assessment-1.html"),
        ("Assessment 2 — critical analysis", "assignments/assessment-2.html"),
        ("Assessment 3 — secure design", "assignments/assessment-3.html"),
        ("Assessment 4 — professional practice", "assignments/assessment-4.html"),
    ],
    "object-oriented-programming": [],
    "security-risk-management": [],
    "software-engineering-project-management": [],
    "research-methods-and-professional-practice": [],
}

# Map a page's relative path to the module slug it belongs to.
def module_for(doc_rel: str) -> str | None:
    """Return the module slug for a document, or None if it is the homepage."""
    if doc_rel == "index.html":
        return None
    if doc_rel.startswith("modules/"):
        parts = doc_rel.split("/")
        if len(parts) >= 2:
            return parts[1]
    if doc_rel.startswith("assignments/"):
        return "secure-software-development"
    if doc_rel.startswith(("docs/", "discussions/", "professional-development/", "evidence/")):
        return "secure-software-development"
    return None

# (section title, [(label, target path relative to the site root), ...])
ARTEFACT_SECTIONS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "Assessment artefacts",
        [
            ("Learning outcomes", "docs/learning-outcomes.html"),
            ("System overview", "docs/system-overview.html"),
            ("Threat model", "docs/threat-model.html"),
            ("Risk register", "docs/risk-assessment.html"),
            ("Secure design", "docs/secure-design.html"),
            ("Implementation", "docs/implementation.html"),
            ("Security testing", "docs/security-testing.html"),
            ("Critical evaluation", "docs/critical-evaluation.html"),
            ("References", "docs/references.html"),
        ],
    ),
    (
        "Collaboration",
        [
            ("Discussion summary 1", "discussions/discussion-summary-1.html"),
            ("Discussion summary 2", "discussions/discussion-summary-2.html"),
        ],
    ),
    (
        "Professional development",
        [
            ("Reflection", "professional-development/reflection.html"),
            ("Meeting notes", "professional-development/meeting-notes.html"),
            ("Peer &amp; tutor feedback", "professional-development/peer-and-tutor-feedback.html"),
            ("Skills matrix", "professional-development/professional-skills-matrix.html"),
            ("Personal development plan", "professional-development/personal-development-plan.html"),
        ],
    ),
    (
        "Evidence",
        [
            ("Evidence index", "evidence/README.html"),
            ("Test results", "evidence/test-results/index.html"),
        ],
    ),
]

# External links live under their own section, after the internal ones.
EXTERNAL_LINKS: list[tuple[str, str]] = [
    ("Python backend (GitHub)", "https://github.com/Paul-Lecomte/fastest_path_backend"),
    ("SwissTransitMap (GitHub)", "https://github.com/Paul-Lecomte/swiss-pb-map"),
]

ASIDE_RE = re.compile(
    r'<aside class="nav-wrap" id="navWrap">.*?</aside>', re.DOTALL
)


def html_files() -> list[Path]:
    """Every authored HTML page, excluding tooling and build artefacts."""
    found: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).parts
        if SKIP_DIRS.intersection(rel):
            continue
        found.append(path)
    return sorted(found)


def prefix_for(doc: Path) -> str:
    """Relative path prefix from a document back to the site root."""
    depth = len(doc.relative_to(ROOT).parts) - 1
    return "../" * depth


def build_nav(doc: Path) -> str:
    """Render the navigation block for a document at the given depth."""
    prefix = prefix_for(doc)
    here = doc.relative_to(ROOT).as_posix()
    current_module = module_for(here)

    lines: list[str] = [
        '<aside class="nav-wrap" id="navWrap">',
        '      <div class="nav-inner">',
        f'        <a href="{prefix}index.html" class="nav-brand">Secure<span class="accent">SSD</span> Portfolio</a>',
    ]

    # --- 1. Modules ---
    lines.append('        <div class="nav-section-title">Modules</div>')
    lines.append('        <ul class="nav-list">')
    for label, target in MODULES:
        href = target if target.startswith("http") else prefix + target
        active = ' class="active"' if target == here else ""
        lines.append(f'          <li><a href="{href}"{active}>{label}</a></li>')
    lines.append("        </ul>")

    # --- 2. Assignments for the current module ---
    if current_module and current_module in MODULE_ASSIGNMENTS:
        assignments = MODULE_ASSIGNMENTS[current_module]
        section_title = f"Assignments &mdash; {current_module.replace('-', ' ').title()}"
        lines.append(f'        <div class="nav-section-title">{section_title}</div>')
        lines.append('        <ul class="nav-list">')
        if assignments:
            for label, target in assignments:
                href = target if target.startswith("http") else prefix + target
                active = ' class="active"' if target == here else ""
                lines.append(f'          <li><a href="{href}"{active}>{label}</a></li>')
        else:
            lines.append('          <li><span class="badge">No assignments added yet</span></li>')
        lines.append("        </ul>")

    # --- 3-6. Artefact sections ---
    for title, items in ARTEFACT_SECTIONS:
        lines.append(f'        <div class="nav-section-title">{title}</div>')
        lines.append('        <ul class="nav-list">')
        for label, target in items:
            href = target if target.startswith("http") else prefix + target
            active = ' class="active"' if target == here else ""
            lines.append(f'          <li><a href="{href}"{active}>{label}</a></li>')
        lines.append("        </ul>")

    # --- 7. Repositories ---
    lines.append('        <div class="nav-section-title">Repositories</div>')
    lines.append('        <ul class="nav-list">')
    for label, href in EXTERNAL_LINKS:
        lines.append(
            f'          <li><a href="{href}" target="_blank" rel="noopener">{label}</a></li>'
        )
    lines.append("        </ul>")
    lines.append("      </div>")
    lines.append("    </aside>")
    return "\n".join(lines)


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    stale: list[str] = []
    changed = 0

    for doc in html_files():
        text = doc.read_text(encoding="utf-8")
        match = ASIDE_RE.search(text)
        if not match:
            rel = doc.relative_to(ROOT).as_posix()
            print(f"  ! no navigation block found in {rel}")
            stale.append(rel)
            continue

        new_block = build_nav(doc)
        if match.group(0) == new_block:
            continue

        rel = doc.relative_to(ROOT).as_posix()
        stale.append(rel)
        if check_only:
            continue

        updated = text[: match.start()] + new_block + text[match.end() :]
        doc.write_text(updated, encoding="utf-8")
        changed += 1

    if check_only:
        if stale:
            print(f"{len(stale)} page(s) with out-of-date navigation:")
            for rel in stale:
                print(f"  - {rel}")
            return 1
        print(f"All pages use the current navigation ({len(html_files())} checked).")
        return 0

    print(f"Rewrote navigation in {changed} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
