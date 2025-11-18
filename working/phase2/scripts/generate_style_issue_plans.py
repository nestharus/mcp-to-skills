from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ISSUES_CSV = ROOT / "working" / "phase2" / "issues_index.csv"
PLANS_DIR = ROOT / "working" / "phase2" / "style_plans"


STYLE_DOCS = {f"STYLE_{i}": Path("docs/to_integrate") / f"STYLE_{i}.md" for i in range(1, 9)}


def load_issues() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with ISSUES_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows.extend(reader)
    return rows


def issues_for_style(style_name: str, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    needle = f"STYLE_{style_name.split('_')[-1]}"
    return [row for row in rows if needle in row.get("doc", "")]


def render_issue_block(issues: list[dict[str, str]]) -> str:
    if not issues:
        return "No open issues in issues_index.csv for this STYLE document."

    lines: list[str] = []
    header = (
        "| id | doc | line_no | description_text | issue_type |"
        " classification | classification_ref | notes |"
    )
    sep = "|---|---|---|---|---|---|---|---|"
    lines.append(header)
    lines.append(sep)
    for row in issues:
        cells = [
            row.get("id", ""),
            row.get("doc", ""),
            row.get("line_no", ""),
            row.get("description_text", "").replace("\n", " "),
            row.get("issue_type", ""),
            row.get("classification", ""),
            row.get("classification_ref", "").replace("\n", " "),
            row.get("notes", "").replace("\n", " "),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_plan(style_key: str, issues: list[dict[str, str]]) -> str:
    style_filename = STYLE_DOCS[style_key]
    issues_block = render_issue_block(issues)
    return f"""# STYLE issues plan for {style_filename}

This plan is generated from `issues_index.csv` and is scoped to `{style_filename}`.

## Relevant issues

{issues_block}

## Instructions

For each issue listed above:

- Open `{style_filename}`.
- Confirm whether the described problem is still present.
- If it is still present, edit `{style_filename}` to resolve it, aligning with current ADRs,
  `pyproject.toml`, and the consolidated `docs/code-style-guide.md`.
- If it has already been resolved, ensure the intent of the fix remains clear and that no
  contradictory guidance remains.

Focus only on the concerns described in these issues; do not introduce unrelated changes.
"""


def main() -> None:
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_issues()

    for style_key in STYLE_DOCS:
        issues = issues_for_style(style_key, rows)
        plan_text = build_plan(style_key, issues)
        plan_path = PLANS_DIR / f"{style_key}.plan.md"
        plan_path.write_text(plan_text, encoding="utf-8")


if __name__ == "__main__":  # pragma: no cover - manual utility
    main()
