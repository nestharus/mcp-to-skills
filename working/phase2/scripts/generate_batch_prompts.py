from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

REPO_ROOT = Path(__file__).resolve().parents[3]
INDEX_CSV_PATH = REPO_ROOT / "working" / "phase2" / "issues_index.csv"
DEFAULT_BATCH_DIR = REPO_ROOT / "working" / "phase2" / "batches"


@dataclass
class Issue:
    issue_id: str
    description: str
    doc: str
    classification: str


def load_unclassified_issues(csv_path: Path) -> List[Issue]:
    issues: List[Issue] = []
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("classification", "").upper() == "UNCLASSIFIED":
                issues.append(
                    Issue(
                        issue_id=row.get("id", ""),
                        description=row.get("description_text", ""),
                        doc=row.get("doc", ""),
                        classification=row.get("classification", ""),
                    ),
                )
    return issues


PROMPT_HEADER_TEMPLATE = """# Issue Classification Batch {batch_num}

Please classify and assign an issue_type for the following
{count} issues from the Phase 1 content analysis.

## Classification Guidelines

- **RESOLVED**: Issue is addressed by migration plan
  (in `working/phase2/migration_plan.md`) or ADR decisions
  (in `docs/adr/`). Provide ADR number or migration section reference.
- **CONFLICT**: Issue requires manual resolution in Phases 3-5.
  Assign to theme (Code Standards & Architecture, Testing & E2E,
  or Workflow/Releases/CI) based on
  `working/phase2/phase_theme_assignments.md`.
- **RESEARCH**: Issue requires external research (tool versions,
  best practices). Assign to research topic (Ruff Configuration,
  Python 3.14+ Features, Testing Patterns, E2E Infrastructure,
  FastAPI Best Practices, Versioning & Releases,
  CI/CD Automation).

## Context Files

- Migration plan: `working/phase2/migration_plan.md`
- Phase assignments: `working/phase2/phase_theme_assignments.md`
- ADRs: `docs/adr/*.md`

## Issues to Classify

"""


PROMPT_FOOTER = """
## Output Format

For each issue, provide both a workflow classification and an issue_type bucket.

To process this batch, run:

  droid exec --auto high -f <this_file> > working/phase2/batch_results/<this_file_basename>.json

The resulting JSON file will be consumed by:

  uv run triage update --results-dir working/phase2/batch_results

```json
{
  "ISS-XXXX": {
    "classification": "RESOLVED|CONFLICT|RESEARCH",
    "classification_ref": "ADR-0001 | Migration §3.2 | Ruff Configuration",
    "issue_type": "Duplicates|Conflicts|Staleness|Gaps|Naming|Env|OpenAPI|"
                  "Testing|Versioning|Health|Other",
    "notes": "Brief explanation"
  }
}
```
"""


def write_batch_file(batch_issues: List[Issue], batch_num: int, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    batch_name = f"classify_batch_{batch_num:03d}.md"
    batch_path = output_dir / batch_name

    lines = [
        PROMPT_HEADER_TEMPLATE.format(batch_num=batch_num, count=len(batch_issues)),
    ]
    for issue in batch_issues:
        lines.append(f"{issue.issue_id}: {issue.description}")
        lines.append(f"Source: {issue.doc}\n")
    lines.append(PROMPT_FOOTER)

    batch_path.write_text("\n".join(lines), encoding="utf-8")
    return batch_path


def generate_batches(issues: List[Issue], batch_size: int, output_dir: Path) -> int:
    batch_count = 0
    for i in range(0, len(issues), batch_size):
        batch_issues = issues[i : i + batch_size]
        if not batch_issues:
            continue
        batch_count += 1
        write_batch_file(batch_issues, batch_count, output_dir)
    return batch_count


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate batch prompt files for issue triage.")
    parser.add_argument("--csv-path", type=Path, default=INDEX_CSV_PATH)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_BATCH_DIR)
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not args.csv_path.exists():
        raise SystemExit(f"CSV not found: {args.csv_path}")
    if args.batch_size <= 0:
        raise SystemExit("--batch-size must be a positive integer")

    issues = load_unclassified_issues(args.csv_path)
    if not issues:
        print("No UNCLASSIFIED issues found; nothing to batch.")
        return 0

    batch_count = generate_batches(issues, args.batch_size, args.output_dir)
    print(f"Generated {batch_count} batch files with {len(issues)} issues")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
