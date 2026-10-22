# secure-software-development-portfolio

MSc Computer Science — Secure Software Development module e-portfolio
University of Essex Online · Paul Lecomte · Module period October 2026

A security-assessed case study of a Python transit-routing backend (RAPTOR pathfinding, gRPC + HTTP, Neo4j) and its supporting full-stack system, SwissTransitMap. Built as summative assessment evidence.

## Site structure

```
secure-software-development-portfolio/
├── README.md
├── index.html                              # Home & audit summary
├── assets/
│   ├── styles/main.css                     # Editorial stylesheet
│   ├── scripts/main.js                     # Navigation behaviour
│   └── diagrams/favicon.svg                 # Favicon
├── docs/                                   # Assessed artefacts
│   ├── learning-outcomes.html              # LO1–LO4 evidence mapping
│   ├── system-overview.html                # Scope, architecture, assets, trust boundaries, attack surface
│   ├── threat-model.html                   # STRIDE threat model
│   ├── risk-assessment.html                # Prioritised risk register
│   ├── secure-design.html                  # Design decisions, alternatives, tool justification
│   ├── implementation.html                 # Security-related code change
│   ├── security-testing.html               # Test baseline, regression tests, actual results
│   ├── critical-evaluation.html            # Strengths, limitations, trade-offs, uncertainty
│   └── references.html                     # Verified sources
├── discussions/                            # LO2 collaborative discussion summaries (templates)
│   ├── discussion-summary-1.html           # Template — awaiting real posts
│   └── discussion-summary-2.html           # Template — awaiting real posts
├── professional-development/               # LO4 professional development (templates/scaffolds)
│   ├── reflection.html                     # Reflective writing scaffold
│   ├── meeting-notes.html                  # Meeting notes template
│   ├── peer-and-tutor-feedback.html        # Feedback template
│   ├── professional-skills-matrix.html     # Skills matrix
│   └── personal-development-plan.html      # PDP
├── evidence/                               # Reproducible evidence
│   ├── README.html                         # Evidence index
│   └── test-results/
│       ├── index.html                      # Test results page
│       ├── results.md                      # Results summary
│       └── pytest-results.txt              # Raw pytest output (UTF-8)
├── tools/                                  # Validation & deployment tooling (not published)
│   ├── validate_links.py                   # Internal link / HTML structure validator
│   ├── verify_references.py                # Resolves source references at pinned commits
│   ├── check_served.py                     # Asserts every published path serves HTTP 200
│   ├── build_site.py                       # Stages the publish set (allow-list)
│   ├── site_files.py                       # Shared file-discovery helper
│   ├── check_urls.py                       # External URL reachability check
│   ├── capture_test_results.py             # Regenerates pytest output as UTF-8
│   ├── list_references.py                  # Prints all source references (audit aid)
│   └── fix_encoding.py                     # Repairs mojibake in HTML
└── .github/workflows/                      # CI + Pages deployment (not published)
    ├── validate.yml                        # Link / reference / served-path CI
    └── deploy-pages.yml                    # GitHub Actions Pages deployment
```

## Validation tooling

The portfolio ships with dependency-free Python scripts that re-verify its own claims:

| Script | Purpose | Exit code |
|---|---|---|
| `tools/validate_links.py` | Checks every HTML file for broken internal links, dead `#anchors`, missing `<title>`/`<meta charset>`/viewport/`lang`, unbalanced tags, and images without `alt`. | 0 = clean |
| `tools/verify_references.py` | Resolves every `file:line` reference in `docs/` against the pinned commit SHAs and asserts the cited line really contains the described construct. | 0 = clean |
| `tools/check_served.py` | Serves the site locally and asserts all 29 published paths return HTTP 200 with complete HTML. | 0 = clean |
| `tools/build_site.py` | Stages the exact publish set into `_site/` and asserts it matches the 29 served paths. | 0 = clean |
| `tools/capture_test_results.py` | Re-runs the backend test suite and regenerates `evidence/test-results/pytest-results.txt` as UTF-8. | 0 = tests passed |
| `tools/list_references.py` | Prints every source reference found in the docs (audit aid). | 0 = always |

Run them from the repository root:

```powershell
python tools/validate_links.py
python tools/verify_references.py
python tools/check_served.py
python tools/build_site.py
```

Latest results: **19/19 HTML files and 323 internal links valid; 26/26 source references resolve at the pinned commits; 29/29 paths served with HTTP 200; 32/32 backend tests pass.**

## What was audited

| Repository | Commit | Commit date | Audited |
|---|---|---|---|
| `fastest_path_backend` (Python routing backend) | `90a50769c4c2013f8e2f7d0241d883cc7b3befd2` | 17 July 2026 | 21 October 2026 |
| `swiss-pb-map` (SwissTransitMap full-stack system) | `610e4342f747d03b68c11bc281b7830abda047ac` | 13 February 2026 | 21 October 2026 |

All source line references in `docs/` are pinned to these SHAs and machine-verified by `tools/verify_references.py`.

## Implemented security improvement

A request-body size ceiling (`MAX_REQUEST_BODY_BYTES` = 1 MiB) on the HTTP `/path` endpoint of the Python backend, returning HTTP 413 for oversized bodies before any memory allocation. Regression tests added in `tests/test_request_limits.py`.

**Verified results:** baseline 26 tests pass; after the fix 32 tests pass (26 smoke + 6 request-limit), no regression.

The change lives in the local audit clone (`C:\Users\lecom\audit-work\backend`) and has **not** been pushed to the origin repository, per the requirement not to modify the student's repositories without authorisation.

## Local preview

This is a static HTML/CSS/JS site. No build step or paid service is required.

1. Open the portfolio folder:
   ```powershell
   cd "C:\Users\lecom\OneDrive\Images\Essex_University\year_1\module\Secure Software Developement\secure-software-development-portfolio"
   ```
2. Serve it locally (Python):
   ```powershell
   python -m http.server 8000
   ```
3. Visit http://localhost:8000/

Or simply open `index.html` directly in a browser.

## GitHub Pages deployment

This site is designed for GitHub Pages as a **project site** (published under a subpath, e.g. `https://Paul-Lecomte.github.io/secure-software-development-portfolio/`).

Deployment is automated by `.github/workflows/deploy-pages.yml` (the **GitHub Actions** build type, `build_type: workflow`):

1. Push this folder to the GitHub repository `secure-software-development-portfolio`.
2. The `Deploy to GitHub Pages` workflow runs on every push to `main`. It stages the publish set with `python tools/build_site.py _site`, then uploads and deploys it.
3. The site is published at `https://Paul-Lecomte.github.io/secure-software-development-portfolio/`.

To enable it in the repository settings, go to **Pages** and set the source to **GitHub Actions**.

`tools/build_site.py` stages an explicit allow-list of files, so only the site is published — the build tooling (`tools/*.py`), the workflow definitions (`.github/`) and repository metadata (`.gitattributes`, `.gitignore`, `_config.yml`) are **not** published. The allow-list is cross-checked against the served-path contract in `tools/check_served.py`, so the two cannot drift apart.

All internal links are relative, so they work both at the domain root and under the GitHub Pages project-site path.

## Security & privacy

Before publishing:
- No API keys, tokens, passwords or connection strings are in the frontend code.
- Test results and evidence are redacted of credentials, private IPs and personal data.
- No exploit instructions targeting third-party systems are included.

## Missing assessment evidence (to be completed by the student)

The following pages are provided as clearly marked **templates/scaffolds** and require genuine evidence before submission:

- `discussions/discussion-summary-1.html` & `discussion-summary-2.html` — real discussion-forum posts not yet supplied
- `professional-development/reflection.html` — genuine reflection not yet written
- `professional-development/meeting-notes.html` — no team meetings held (individual work)
- `professional-development/peer-and-tutor-feedback.html` — no feedback received yet
- `professional-development/professional-skills-matrix.html` — self-assessment ratings not yet filled in
- `professional-development/personal-development-plan.html` — dates/objectives not yet set

No collaboration, attendance, feedback, or discussion content has been invented. These items require clarification from the module tutor and/or genuine participation before submission.

## License

MIT License. See LICENSE.
