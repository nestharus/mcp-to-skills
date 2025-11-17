# Phase 2 Triage Workflow

This guide describes how to use the Phase 2 triage tooling to maintain `issues_index.csv`, classify issues via Droid, and keep the conflict/research backlogs and `content_issues.md` in sync.

All commands are assumed to be run from the repo root using `uv`.

## Phase A – Extract and Index Red Flags

1. **Scan summaries and assign IDs**
   ```bash
   uv run triage scan
   ```
   - Scans `working/phase1/summaries/**.md` for `## Red Flags`.
   - Reuses existing `ISS-XXXX` IDs where possible and allocates new IDs for new bullets.
   - Annotates bullets in-place by appending `[ISS-XXXX]` to the red-flag lines.
   - Incrementally merges results into `working/phase2/issues_index.csv` without dropping or renumbering existing issues.

2. **Inspect the index**
   ```bash
   head working/phase2/issues_index.csv
   uv run triage sql --query "SELECT COUNT(*) FROM issues"
   ```

## Phase B – Batch Classification with Droid

1. **Generate batches for UNCLASSIFIED issues**
   ```bash
   uv run triage batch --batch-size 10
   ```
   - Creates `working/phase2/batches/classify_batch_XXX.md` for all `UNCLASSIFIED` rows.
   - Each batch includes instructions and an output schema with `classification`, `classification_ref`, `issue_type`, and `notes`.

2. **Run Droid on each batch**
   ```bash
   uv run python working/phase2/scripts/run_droid_batches.py
   ```
   - Calls `droid exec --auto high -f` for each batch file.
   - Writes JSON results to `working/phase2/batch_results/classify_batch_XXX.json`.

3. **Apply Droid results to the index**
   ```bash
   uv run triage update --results-dir working/phase2/batch_results
   ```
   - Updates `classification`, `classification_ref`, `issue_type`, and `notes` in `issues_index.csv` for all IDs found in the JSON results.
   - Existing rows not present in the results are left unchanged.

4. **Validate the index**
   ```bash
   uv run triage validate
   ```
   - Prints totals by `classification`, checks for duplicate IDs, and reports any rows with empty classifications.

## Phase C – Generate Rollups

1. **Generate conflict and research backlogs and update summary**
   ```bash
   uv run triage rollup
   ```
   - Rebuilds:
     - `working/phase2/conflict_backlog.md` (with theme and priority columns derived from `classification_ref` and `issue_type`).
     - `working/phase2/research_backlog.md` (grouped by normalized research topics such as Ruff Configuration, Testing Patterns, CI/CD Automation).
     - The `# Content Issues Summary` block at the top of `working/phase1/content_issues.md`, replacing only that summary section and leaving the detailed sections intact.

## Phase D – Ongoing Maintenance

When new red flags are added to summaries or existing ones are edited:

1. **Rescan summaries (incremental)**
   ```bash
   uv run triage scan
   ```
   - Reuses IDs for existing bullets and assigns IDs for new ones.

2. **Reset classifications if you want to reclassify everything**
   ```bash
   uv run python - << 'PY'
from __future__ import annotations

import csv
from pathlib import Path

root = Path("working/phase2/issues_index.csv")
rows = []
with root.open(encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        row["classification"] = "UNCLASSIFIED"
        row["classification_ref"] = ""
        row["issue_type"] = ""
        row["notes"] = ""
        rows.append(row)

with root.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
PY
   ```

3. **Clear old batches/results (keep the table)**
   ```bash
   rm -rf working/phase2/batches working/phase2/batch_results
   mkdir -p working/phase2/batch_results
   ```

4. **Regenerate batches and rerun Droid + updates**
   ```bash
   uv run triage batch --batch-size 10
   uv run python working/phase2/scripts/run_droid_batches.py
   uv run triage update --results-dir working/phase2/batch_results
   uv run triage rollup
   ```

## SQL Exploration

- Quick query:
  ```bash
  uv run triage sql --query "SELECT classification, COUNT(*) FROM issues GROUP BY classification"
  ```

- Interactive session (Python DuckDB shell):
  ```bash
  uv run triage sql
  ```
  - Loads `issues` from `issues_index.csv` and repeatedly prompts for SQL until you enter `exit` or `quit`.

## References

- Index: `working/phase2/issues_index.csv`
- Backlogs: `working/phase2/conflict_backlog.md`, `working/phase2/research_backlog.md`
- Summary: `working/phase1/content_issues.md`
- Migration plan: `working/phase2/migration_plan.md`
