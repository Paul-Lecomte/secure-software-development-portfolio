"""
assignment_data.py — the content model behind the assignment hub pages.

The portfolio is presented as a set of assignments. Each assignment gathers
four strands that recur across the module:

  * Assessment              — the artefacts that satisfy the marking criteria
  * Collaboration           — discussion summaries and meeting records
  * Professional development — reflection, feedback, skills matrix, PDP
  * Evidence                — reproducible artefacts backing the claims

Keeping this content in one place (rather than inside the HTML) means a new
assignment, or an update as the module advances, is a data change followed by
a regeneration — the rendered pages can never drift from the model.

Each strand item is a dict:
    title        short label for the artefact
    status       "ok" | "warn" | "bad" | "info"  (status pill colour)
    status_text  text shown inside the pill
    description  one sentence on what the artefact covers
    items        bullet list of what it contains
    href         path to the artefact, relative to the site root
    button       link-button label
"""
from __future__ import annotations

from typing import Any

StrandItem = dict[str, Any]
Assignment = dict[str, Any]


def item(
    title: str,
    status: str,
    status_text: str,
    description: str,
    items: list[str],
    href: str,
    button: str,
) -> StrandItem:
    """Build one strand item."""
    return {
        "title": title,
        "status": status,
        "status_text": status_text,
        "description": description,
        "items": items,
        "href": href,
        "button": button,
    }


ASSESSMENT_1: Assignment = {
    "slug": "assessment-1",
    "number": "Assessment 1",
    "title": "Security risk identification",
    "meta": "LO1 &middot; system scope, STRIDE threat model and risk register",
    "summary": (
        "Identify, assess and prioritise the security risks in the systems in "
        "scope, and justify each finding against the audited source code."
    ),
    "status": "ok",
    "status_text": "Complete",
    "outcome": "LO1",
    "intro": (
        "The findings come from an audit of two repositories pinned to specific commits. "
        "Line references are checked against those commits with tools/verify_references.py."
    ),
    "strands": [
        (
            "Assessment",
            [
                item(
                    "System overview",
                    "ok",
                    "Complete",
                    "Scope, architecture, assets, data flows, trust boundaries and the exposed attack surface.",
                    [
                        "Architecture and deployment context",
                        "Assets and entry points",
                        "Trust boundaries and attack surface",
                    ],
                    "docs/system-overview.html",
                    "Open system overview",
                ),
                item(
                    "Threat model (STRIDE)",
                    "ok",
                    "Complete",
                    "Assets, threat actors and trust boundaries analysed with STRIDE, with each threat classified.",
                    [
                        "Trust boundaries and threat actors",
                        "STRIDE table with classification",
                        "Explanation of the classification scheme",
                    ],
                    "docs/threat-model.html",
                    "Open threat model",
                ),
                item(
                    "Risk register",
                    "ok",
                    "Complete",
                    "Prioritised register with likelihood, impact and rationale, recommended mitigations and residual risk.",
                    [
                        "Likelihood and impact rationale",
                        "Recommended mitigations",
                        "Residual risks after mitigation",
                    ],
                    "docs/risk-assessment.html",
                    "Open risk register",
                ),
            ],
        ),
        (
            "Collaboration",
            [
                item(
                    "Discussion summary 1",
                    "warn",
                    "Template",
                    "Structured summary of the first discussion-forum thread: perspectives, my contribution and lessons learned.",
                    [
                        "No discussion posts supplied yet &mdash; the page is an unpopulated template",
                        "Requires genuine forum participation before submission",
                    ],
                    "discussions/discussion-summary-1.html",
                    "Open discussion summary 1",
                ),
                item(
                    "Meeting notes",
                    "warn",
                    "Template",
                    "Template for recording team or supervisor meetings, with attendees, decisions and actions.",
                    [
                        "Awaiting genuine meeting records",
                        "Marked as template because the work was carried out individually",
                    ],
                    "professional-development/meeting-notes.html",
                    "Open meeting notes",
                ),
            ],
        ),
        (
            "Professional development",
            [
                item(
                    "Professional skills matrix",
                    "ok",
                    "Complete",
                    "Self-assessment of the professional and technical skills exercised by this assignment, with supporting evidence.",
                    [
                        "Risk-analysis, requirements and research skills",
                        "Evidence cited for each rating",
                    ],
                    "professional-development/professional-skills-matrix.html",
                    "Open skills matrix",
                ),
                item(
                    "Personal development plan",
                    "ok",
                    "Complete",
                    "How this assignment feeds the objectives and targets recorded in the personal development plan.",
                    [
                        "Objectives and target dates",
                        "Actions arising from this assignment",
                    ],
                    "professional-development/personal-development-plan.html",
                    "Open personal development plan",
                ),
            ],
        ),
        (
            "Evidence",
            [
                item(
                    "Evidence index",
                    "ok",
                    "Complete",
                    "Reproducible artefacts backing the findings: audited commits, test output and the audit method.",
                    [
                        "Audited repository commits",
                        "Machine-verified source references",
                    ],
                    "evidence/README.html",
                    "Open evidence index",
                ),
            ],
        ),
    ],
    "outcomes": [
        ("LO1 &mdash; Identify and manage security risks", "System overview, threat model, risk register", "ok", "Complete"),
        ("LO2 &mdash; Critically analyse development problems", "Discussion summary 1, references", "warn", "Partly &mdash; template pending"),
        ("LO4 &mdash; Professional and collaborative skills", "Skills matrix, personal development plan", "warn", "Partly &mdash; templates pending"),
    ],
}

ASSESSMENT_2: Assignment = {
    "slug": "assessment-2",
    "number": "Assessment 2",
    "title": "Critical analysis of development methodologies",
    "meta": "LO2 &middot; methodology, tooling and alternative strategies",
    "summary": (
        "Critically evaluate the security development methodologies, tools and "
        "alternative strategies available to a security engineer, and justify "
        "the choices made in this portfolio."
    ),
    "status": "ok",
    "status_text": "Complete",
    "outcome": "LO2",
    "intro": (
        "The evaluation is based on the primary sources in the reference list. "
        "Each recommendation traces back to a finding in the threat model or risk register."
    ),
    "strands": [
        (
            "Assessment",
            [
                item(
                    "Critical evaluation",
                    "ok",
                    "Complete",
                    "Critical analysis of secure development methodologies, the tools available and the trade-offs they involve.",
                    [
                        "Methodology comparison and trade-off analysis",
                        "Tooling evaluation against the identified risks",
                        "Recommendations and their justification",
                    ],
                    "docs/critical-evaluation.html",
                    "Open critical evaluation",
                ),
                item(
                    "References",
                    "ok",
                    "Complete",
                    "Consolidated reference list with Harvard-style entries and a source-quality note.",
                    [
                        "Primary and secondary sources",
                        "Citation style applied consistently",
                    ],
                    "docs/references.html",
                    "Open references",
                ),
            ],
        ),
        (
            "Collaboration",
            [
                item(
                    "Discussion summary 2",
                    "warn",
                    "Template",
                    "Structured summary of the second discussion-forum thread, focused on methodology and tooling choices.",
                    [
                        "No discussion posts supplied yet &mdash; the page is an unpopulated template",
                        "Requires genuine forum participation before submission",
                    ],
                    "discussions/discussion-summary-2.html",
                    "Open discussion summary 2",
                ),
            ],
        ),
        (
            "Professional development",
            [
                item(
                    "Professional skills matrix",
                    "ok",
                    "Complete",
                    "Ratings for the research, evaluation and critical-thinking skills this assignment exercised.",
                    [
                        "Research and evaluation skills",
                        "Evidence cited for each rating",
                    ],
                    "professional-development/professional-skills-matrix.html",
                    "Open skills matrix",
                ),
                item(
                    "Reflection",
                    "ok",
                    "Complete",
                    "Reflection on how the critical analysis changed the approach taken in the later assessments.",
                    [
                        "What the analysis changed and why",
                        "Limitations of the evaluation",
                    ],
                    "professional-development/reflection.html",
                    "Open reflection",
                ),
            ],
        ),
        (
            "Evidence",
            [
                item(
                    "Evidence index",
                    "ok",
                    "Complete",
                    "The reproducible artefacts that support the claims made in the critical evaluation.",
                    [
                        "Audited repository commits",
                        "Machine-verified source references",
                    ],
                    "evidence/README.html",
                    "Open evidence index",
                ),
            ],
        ),
    ],
    "outcomes": [
        ("LO2 &mdash; Critically analyse development problems", "Critical evaluation, references", "ok", "Complete"),
        ("LO1 &mdash; Identify and manage security risks", "Methodology choices traced to the risk register", "ok", "Complete"),
        ("LO4 &mdash; Professional and collaborative skills", "Reflection, discussion summary 2", "warn", "Partly &mdash; template pending"),
    ],
}

ASSESSMENT_3: Assignment = {
    "slug": "assessment-3",
    "number": "Assessment 3",
    "title": "Secure design and implementation",
    "meta": "LO3 &middot; design decisions, implementation and security testing",
    "summary": (
        "Apply the identified risks to produce a secure design, implement the "
        "corresponding controls, and demonstrate their effectiveness with "
        "documented testing."
    ),
    "status": "ok",
    "status_text": "Complete",
    "outcome": "LO3",
    "intro": (
        "Each control is traced to the risk it mitigates and evidenced by a "
        "reproducible test rather than an assertion. Controls that could not be "
        "implemented are noted in the risk register."
    ),
    "strands": [
        (
            "Assessment",
            [
                item(
                    "Secure design",
                    "ok",
                    "Complete",
                    "Design decisions for the security controls, each traced to the risk it addresses.",
                    [
                        "Control-to-risk traceability",
                        "Secure design principles applied",
                        "Rejected alternatives and the reason",
                    ],
                    "docs/secure-design.html",
                    "Open secure design",
                ),
                item(
                    "Implementation",
                    "ok",
                    "Complete",
                    "How each control was implemented, with the code locations where the change was made.",
                    [
                        "Per-control implementation notes",
                        "Source references for each change",
                    ],
                    "docs/implementation.html",
                    "Open implementation",
                ),
                item(
                    "Security testing",
                    "ok",
                    "Complete",
                    "The test plan, the cases executed and the results obtained for each control.",
                    [
                        "Test plan and cases",
                        "Results and coverage",
                    ],
                    "docs/security-testing.html",
                    "Open security testing",
                ),
            ],
        ),
        (
            "Collaboration",
            [
                item(
                    "Meeting notes",
                    "warn",
                    "Template",
                    "Template for recording design reviews with the tutor or peers, including decisions and actions.",
                    [
                        "Awaiting genuine meeting records",
                        "Marked as template because the work was carried out individually",
                    ],
                    "professional-development/meeting-notes.html",
                    "Open meeting notes",
                ),
            ],
        ),
        (
            "Professional development",
            [
                item(
                    "Professional skills matrix",
                    "ok",
                    "Complete",
                    "Ratings for the practical engineering and testing skills this assignment exercised.",
                    [
                        "Secure-coding and testing skills",
                        "Evidence cited for each rating",
                    ],
                    "professional-development/professional-skills-matrix.html",
                    "Open skills matrix",
                ),
                item(
                    "Personal development plan",
                    "ok",
                    "Complete",
                    "The development objectives this assignment contributed to and the progress made against them.",
                    [
                        "Objectives and target dates",
                        "Actions arising from this assignment",
                    ],
                    "professional-development/personal-development-plan.html",
                    "Open personal development plan",
                ),
            ],
        ),
        (
            "Evidence",
            [
                item(
                    "Test results",
                    "ok",
                    "Complete",
                    "Raw test output backing the security-testing claims.",
                    [
                        "Test runner output",
                        "Per-control result mapping",
                    ],
                    "evidence/test-results/index.html",
                    "Open test results",
                ),
                item(
                    "Evidence index",
                    "ok",
                    "Complete",
                    "The reproducible artefacts that support the implementation and testing claims.",
                    [
                        "Audited repository commits",
                        "Machine-verified source references",
                    ],
                    "evidence/README.html",
                    "Open evidence index",
                ),
            ],
        ),
    ],
    "outcomes": [
        ("LO3 &mdash; Design and implement secure software", "Secure design, implementation, security testing", "ok", "Complete"),
        ("LO1 &mdash; Identify and manage security risks", "Controls traced to the risk register", "ok", "Complete"),
        ("LO4 &mdash; Professional and collaborative skills", "Skills matrix, meeting notes", "warn", "Partly &mdash; template pending"),
    ],
}

ASSESSMENT_4: Assignment = {
    "slug": "assessment-4",
    "number": "Assessment 4",
    "title": "Professional practice and development",
    "meta": "LO4 &middot; reflection, feedback and development planning",
    "summary": (
        "Demonstrate professional practice through reflection on the work "
        "undertaken, an honest account of the feedback received, and a "
        "personal development plan that carries the learning forward."
    ),
    "status": "warn",
    "status_text": "In progress",
    "outcome": "LO4",
    "intro": (
        "Reflection and skills matrix are written up. Peer and tutor feedback "
        "and meeting records are still empty templates &mdash; I won't make up feedback."
    ),
    "strands": [
        (
            "Assessment",
            [
                item(
                    "Reflection",
                    "ok",
                    "Complete",
                    "Reflection on the portfolio as a whole: what was done well, what was not, and what would be done differently.",
                    [
                        "What worked and what did not",
                        "Changes made in response to feedback",
                        "Limitations of the work",
                    ],
                    "professional-development/reflection.html",
                    "Open reflection",
                ),
                item(
                    "Peer &amp; tutor feedback",
                    "warn",
                    "Template",
                    "Template for recording feedback received from peers and the tutor, and the actions taken in response.",
                    [
                        "Awaiting genuine feedback &mdash; the page is an unpopulated template",
                        "Must not be written before feedback is received",
                    ],
                    "professional-development/peer-and-tutor-feedback.html",
                    "Open peer &amp; tutor feedback",
                ),
            ],
        ),
        (
            "Collaboration",
            [
                item(
                    "Meeting notes",
                    "warn",
                    "Template",
                    "Template for recording team or supervisor meetings, with attendees, decisions and actions.",
                    [
                        "Awaiting genuine meeting records",
                        "Marked as template because the work was carried out individually",
                    ],
                    "professional-development/meeting-notes.html",
                    "Open meeting notes",
                ),
                item(
                    "Discussion summary 2",
                    "warn",
                    "Template",
                    "Structured summary of the second discussion-forum thread, focused on methodology and tooling choices.",
                    [
                        "No discussion posts supplied yet &mdash; the page is an unpopulated template",
                    ],
                    "discussions/discussion-summary-2.html",
                    "Open discussion summary 2",
                ),
            ],
        ),
        (
            "Professional development",
            [
                item(
                    "Professional skills matrix",
                    "ok",
                    "Complete",
                    "Self-assessment across the professional skills the module develops, with evidence for each rating.",
                    [
                        "Ratings with supporting evidence",
                        "Skills still to be developed",
                    ],
                    "professional-development/professional-skills-matrix.html",
                    "Open skills matrix",
                ),
                item(
                    "Personal development plan",
                    "ok",
                    "Complete",
                    "Objectives, target dates and the actions taken, covering the period after this module.",
                    [
                        "Objectives and target dates",
                        "Progress against each objective",
                    ],
                    "professional-development/personal-development-plan.html",
                    "Open personal development plan",
                ),
            ],
        ),
        (
            "Evidence",
            [
                item(
                    "Evidence index",
                    "ok",
                    "Complete",
                    "The reproducible artefacts that support the professional-practice claims.",
                    [
                        "Audited repository commits",
                        "Machine-verified source references",
                    ],
                    "evidence/README.html",
                    "Open evidence index",
                ),
            ],
        ),
    ],
    "outcomes": [
        ("LO4 &mdash; Professional and collaborative skills", "Reflection, skills matrix, personal development plan", "ok", "Complete"),
        ("LO2 &mdash; Critically analyse development problems", "Discussion summary 2", "warn", "Partly &mdash; template pending"),
        ("LO4 &mdash; Feedback and review", "Peer and tutor feedback, meeting notes", "bad", "Outstanding &mdash; awaiting genuine input"),
    ],
}

#: Every assignment, in the order they are presented in the hub.
ASSIGNMENTS: list[Assignment] = [
    ASSESSMENT_1,
    ASSESSMENT_2,
    ASSESSMENT_3,
    ASSESSMENT_4,
]
