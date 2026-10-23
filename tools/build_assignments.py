"""
build_assignments.py — render the assignment hub pages from the content model.

Each assignment in tools/assignment_data.py becomes a page under
assignments/. The pages are generated rather than hand-written so that the
hub stays consistent as the module advances: adding an assignment, or
changing a status, is a data edit followed by a regeneration.

Run:  python tools/build_assignments.py
Exit code 0 = pages regenerated, 1 = a problem was found.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from assignment_data import ASSIGNMENTS, Assignment  # noqa: E402
from update_nav import build_nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assignments"

FOOTER = (
    '<footer class="site-footer">\n'
    '        <div class="wrap"><p>MSc Computer Science &mdash; Secure Software '
    "Development &middot; University of Essex Online &middot; October 2026.</p>"
    "</div>\n"
    "      </footer>"
)

NAV_PLACEHOLDER = "<!-- NAVIGATION -->"


def status_pill(status: str, text: str) -> str:
    """Render a status pill."""
    return f'<span class="status status-{status}">{text}</span>'


def render_strand(name: str, items: list[dict], prefix: str) -> str:
    """Render one strand: a heading and a card per artefact."""
    out = [f"          <h2>{name}</h2>", '          <ul class="strand-list">']
    for entry in items:
        href = prefix + entry["href"]
        out.append("            <li>")
        out.append('              <div class="strand">')
        out.append(
            f'                <h3>{entry["title"]} '
            f'{status_pill(entry["status"], entry["status_text"])}</h3>'
        )
        out.append(f'                <p>{entry["description"]}</p>')
        if entry["items"]:
            out.append("                <ul>")
            for bullet in entry["items"]:
                out.append(f"                  <li>{bullet}</li>")
            out.append("                </ul>")
        out.append(
            f'                <a class="btn btn-outline" href="{href}">'
            f'{entry["button"]}</a>'
        )
        out.append("              </div>")
        out.append("            </li>")
    out.append("          </ul>")
    return "\n".join(out)


def render_outcomes(assignment: Assignment, prefix: str) -> str:
    """Render the learning-outcome coverage table."""
    out = ["          <h2>Learning-outcome coverage</h2>", '          <div class="table-wrap">', "            <table>"]
    out.append("              <tr><th>Outcome</th><th>Covered by</th><th>Status</th></tr>")
    for outcome, covered, status, text in assignment["outcomes"]:
        out.append(
            f"              <tr><td>{outcome}</td><td>{covered}</td>"
            f"<td>{status_pill(status, text)}</td></tr>"
        )
    out.append("            </table>")
    out.append("          </div>")
    out.append(
        f'          <p><a href="{prefix}docs/learning-outcomes.html">'
        "See the full learning-outcome mapping &rarr;</a></p>"
    )
    return "\n".join(out)


def render_siblings(assignment: Assignment, prefix: str) -> str:
    """Render links to the other assignments in the hub."""
    out = ["          <h2>Other assignments</h2>", '          <ul class="artefact-list">']
    for other in ASSIGNMENTS:
        if other["slug"] == assignment["slug"]:
            continue
        href = f"{prefix}assignments/{other['slug']}.html"
        out.append(
            f'            <li><a href="{href}">{other["number"]} &mdash; '
            f'{other["title"]}<span>{other["summary"]}</span></a></li>'
        )
    out.append("          </ul>")
    return "\n".join(out)


def render_page(assignment: Assignment) -> str:
    """Render a complete assignment hub page."""
    slug = assignment["slug"]
    prefix = "../"  # the pages live one directory below the site root
    title = f'{assignment["number"]} &mdash; {assignment["title"]}'
    description = (
        f'{assignment["number"]} of the Secure Software Development module: '
        f'{assignment["summary"]}'
    )

    parts: list[str] = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('  <meta charset="utf-8">')
    parts.append(
        '  <meta name="viewport" content="width=device-width, initial-scale=1">'
    )
    parts.append(
        f"  <title>{title} &mdash; Secure Software Development e-Portfolio</title>"
    )
    parts.append(f'  <meta name="description" content="{description}">')
    parts.append(f'  <link rel="stylesheet" href="{prefix}assets/styles/main.css">')
    parts.append(f'  <link rel="icon" href="{prefix}assets/diagrams/favicon.svg">')
    parts.append("</head>")
    parts.append("<body>")
    parts.append('  <a class="skip-link" href="#main">Skip to content</a>')
    parts.append('  <div class="page">')
    parts.append(NAV_PLACEHOLDER)
    parts.append(
        '    <button class="menu-toggle" aria-label="Toggle navigation" '
        'aria-expanded="false" aria-controls="navWrap">&#9776;</button>'
    )
    parts.append('    <main class="main" id="main" tabindex="-1">')
    parts.append('      <header class="site-header">')
    parts.append('        <div class="wrap">')
    parts.append(f"          <h1>{title}</h1>")
    parts.append(f'          <div class="meta">{assignment["meta"]}</div>')
    parts.append("        </div>")
    parts.append("      </header>")
    parts.append('      <section class="content">')
    parts.append('        <div class="wrap">')

    # Assignment header: title, summary and status facts.
    parts.append('          <div class="assignment-header">')
    parts.append("            <div>")
    parts.append(f"              <h2>{title}</h2>")
    parts.append(f'              <p>{assignment["summary"]}</p>')
    parts.append("            </div>")
    parts.append('            <div class="assignment-facts">')
    parts.append(
        f'              {status_pill(assignment["status"], assignment["status_text"])}'
    )
    parts.append(
        f'              <span class="status status-info">{assignment["outcome"]}</span>'
    )
    parts.append("            </div>")
    parts.append("          </div>")

    parts.append('          <div class="callout callout-info">')
    parts.append(f"            {assignment['intro']}")
    parts.append("          </div>")

    for name, items in assignment["strands"]:
        parts.append(render_strand(name, items, prefix))

    parts.append(render_outcomes(assignment, prefix))
    parts.append(render_siblings(assignment, prefix))

    parts.append("        </div>")
    parts.append("      </section>")
    parts.append(FOOTER)
    parts.append("    </main>")
    parts.append("  </div>")
    parts.append(f'  <script src="{prefix}assets/scripts/main.js"></script>')
    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for assignment in ASSIGNMENTS:
        path = OUT_DIR / f'{assignment["slug"]}.html'
        page = render_page(assignment)
        # The navigation is generated by tools/update_nav.py so that every page
        # in the site exposes exactly the same set of targets.
        page = page.replace(NAV_PLACEHOLDER, build_nav(path))
        path.write_text(page, encoding="utf-8")
        written.append(path.relative_to(ROOT).as_posix())
        print(f"  wrote {path.relative_to(ROOT).as_posix()}")
    print(
        f"Generated {len(written)} assignment page(s) in "
        f"{OUT_DIR.relative_to(ROOT).as_posix()}/"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
