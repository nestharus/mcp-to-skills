from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import duckdb

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CSV_PATH = REPO_ROOT / "working" / "phase2" / "issues_index.csv"
CONFLICT_BACKLOG = REPO_ROOT / "working" / "phase2" / "conflict_backlog.md"
RESEARCH_BACKLOG = REPO_ROOT / "working" / "phase2" / "research_backlog.md"
CONTENT_ISSUES = REPO_ROOT / "working" / "phase1" / "content_issues.md"


def load_issues_table(csv_path: Path) -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(":memory:")
    conn.execute(
        "CREATE TABLE issues AS SELECT * FROM read_csv_auto(?, header=True)",
        [str(csv_path)],
    )
    return conn


def _infer_theme_and_priority(issue_type: str, classification_ref: str | None) -> tuple[str, str]:
    ref = (classification_ref or "").lower()
    theme = "General"
    if "testing" in ref or "e2e" in ref:
        theme = "Testing & E2E"
    elif "workflow" in ref or "releases" in ref or "ci" in ref:
        theme = "Workflow/Releases/CI"
    elif "code standards" in ref or "architecture" in ref:
        theme = "Code Standards & Architecture"

    issue_type_lower = (issue_type or "").lower()
    if any(k in issue_type_lower for k in ["conflicts", "openapi"]):
        priority = "High"
    elif any(k in issue_type_lower for k in ["gaps", "env", "testing"]):
        priority = "Medium"
    else:
        priority = "Low"

    return theme, priority


def generate_conflict_backlog(conn: duckdb.DuckDBPyConnection, path: Path) -> None:
    rows = conn.execute(
        "SELECT id, description_text, doc, classification_ref, issue_type, notes FROM issues "
        "WHERE classification = 'CONFLICT' "
        "ORDER BY classification_ref, id",
    ).fetchall()

    lines = [
        "# Conflict Backlog",
        "",
        f"Total conflicts: {len(rows)}",
        "",
        "| Issue ID | Issue Description | Source Doc | Theme | Priority | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for issue_id, desc, doc, ref, issue_type, notes in rows:
        theme, priority = _infer_theme_and_priority(issue_type, ref)
        lines.append(
            f"| {issue_id} | {desc} | {doc} | {theme} | {priority} | {notes or ''} |",
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generating conflict_backlog.md... {len(rows)} conflicts")


def _normalize_research_topic(classification_ref: str | None) -> str:
    ref = (classification_ref or "").lower()
    mapping = {
        "ruff": "Ruff Configuration",
        "python": "Python 3.14+ Features",
        "testing": "Testing Patterns",
        "e2e": "E2E Infrastructure",
        "fastapi": "FastAPI Best Practices",
        "version": "Versioning & Releases",
        "release": "Versioning & Releases",
        "ci": "CI/CD Automation",
    }
    for key, topic in mapping.items():
        if key in ref:
            return topic
    return classification_ref or "General"


def generate_research_backlog(conn: duckdb.DuckDBPyConnection, path: Path) -> None:
    rows = conn.execute(
        "SELECT id, description_text, doc, classification_ref, notes FROM issues "
        "WHERE classification = 'RESEARCH' "
        "ORDER BY classification_ref, id",
    ).fetchall()

    lines = ["# Research Backlog", ""]

    current_topic: str | None = None
    for issue_id, desc, doc, ref, notes in rows:
        topic = _normalize_research_topic(ref)
        if topic != current_topic:
            current_topic = topic
            lines.append(f"## {topic}")
            lines.append("")
        lines.append(f"- **{issue_id}** ({doc}): {desc} ({notes or ''})")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generating research_backlog.md... {len(rows)} research items")


def update_content_issues_summary(conn: duckdb.DuckDBPyConnection, path: Path) -> None:
    total = conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
    by_class = dict(
        conn.execute(
            "SELECT classification, COUNT(*) FROM issues GROUP BY classification",
        ).fetchall(),
    )
    resolved = by_class.get("RESOLVED", 0)
    conflict = by_class.get("CONFLICT", 0)
    research = by_class.get("RESEARCH", 0)

    header_lines = [
        "# Content Issues Summary",
        "",
        f"Total red flags tracked: {total}",
        f"RESOLVED: {resolved} (via ADRs/merges)",
        f"CONFLICT: {conflict} (see working/phase2/conflict_backlog.md)",
        f"RESEARCH: {research} (see working/phase2/research_backlog.md)",
        "",
        "> Detailed tracking in working/phase2/issues_index.csv and backlogs.",
        "",
    ]

    if path.exists():
        existing = path.read_text(encoding="utf-8").splitlines()
        start = 0
        end = len(existing)
        for i, line in enumerate(existing):
            if line.strip().startswith("# Content Issues Summary"):
                start = i
                break
        for i in range(start + 1, len(existing)):
            if existing[i].startswith("### "):
                end = i
                break
        tail = existing[end:]
    else:
        tail: list[str] = []

    path.write_text("\n".join(header_lines + tail) + "\n", encoding="utf-8")
    print("Updated content_issues.md summary section")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate rollup documents from issues_index.csv")
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not args.csv_path.exists():
        raise SystemExit(f"CSV not found: {args.csv_path}")

    conn = load_issues_table(args.csv_path)
    generate_conflict_backlog(conn, CONFLICT_BACKLOG)
    generate_research_backlog(conn, RESEARCH_BACKLOG)
    update_content_issues_summary(conn, CONTENT_ISSUES)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
