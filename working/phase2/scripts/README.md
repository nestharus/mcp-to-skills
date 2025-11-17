# Phase 2 Triage Scripts

This package contains the automation used to extract, classify, and roll up the Phase 1 red-flag issues into a single, queryable index.

The central artifact is `working/phase2/issues_index.csv`, which tracks one row per red flag with stable `ISS-XXXX` IDs, source document/line, and Droid-sourced classification metadata.

## Data Model (issues_index.csv)

- `id`: Stable issue identifier (`ISS-0001`, `ISS-0002`, ...), also written back into the summary markdown bullets.
- `doc`: Relative path to the source summary file (e.g. `working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md`).
- `line_no`: 1-based line number of the red-flag bullet in `doc`.
- `description_text`: Text of the red-flag bullet (without the `[ISS-XXXX]` suffix).
- `issue_type`: High-level bucket assigned by Droid (Duplicates, Conflicts, Staleness, Gaps, Naming, Env, OpenAPI, Testing, Versioning, Health, Other).
- `classification`: Workflow status (`UNCLASSIFIED`, `RESOLVED`, `CONFLICT`, `RESEARCH`).
- `classification_ref`: Free-form reference to a theme, ADR, migration-plan section, or research topic.
- `notes`: Short explanation for the classification.

## Script Overview

- `extract_red_flags.py`: Scans `working/phase1/summaries/**.md` for `## Red Flags` sections, assigns or reuses `ISS-XXXX` IDs, annotates the bullets in-place, and incrementally merges results into `issues_index.csv` without dropping existing rows.
- `generate_batch_prompts.py`: Reads `issues_index.csv` and creates `working/phase2/batches/classify_batch_XXX.md` files for all `UNCLASSIFIED` issues with a standard Droid prompt and JSON output schema (including `classification` and `issue_type`).
- `run_droid_batches.py`: Convenience runner that executes `droid exec --auto high -f` for each batch file and saves the JSON output into `working/phase2/batch_results/`.
- `update_classifications.py`: Loads the batch JSON (including `issue_type`) and updates `issues_index.csv`, preserving existing rows and only overriding classification-related fields for IDs present in the results.
- `generate_rollups.py`: Uses DuckDB to query `issues_index.csv` and generate `conflict_backlog.md`, `research_backlog.md`, and the summary block at the top of `working/phase1/content_issues.md`.
- `triage_manager.py`: Thin CLI wrapper exposing `scan`, `batch`, `update`, `rollup`, `sql`, and `validate` subcommands wired to the scripts above via `uv run triage ...`.

For a full command-by-command walkthrough of the Phase A–D workflow, see `WORKFLOW.md` in this directory.
