# Phase 2 Issue Triage Index

This directory contains the Phase 2 triage workflow, centered on the `issues_index.csv` table. Later phases should treat this CSV as the single source of truth for all red-flag issues identified in Phase 1 summaries.

## Table Schema (`issues_index.csv`)

- `id`: Unique issue identifier in the form `ISS-0001`, `ISS-0002`, etc. This ID is stable across phases and used in batch prompts, DuckDB queries, and backlog docs.
- `doc`: Relative path (from the repo root) to the source markdown file where the issue was found, e.g. `working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md`.
- `line_no`: 1-based line number within `doc` where the red-flag bullet appears, useful for jumping back to original context.
- `description_text`: The full text of the red-flag bullet, without any `[ISS-XXXX]` tag appended.
- `issue_type`: High-level category assigned by Droid during batch classification. Expected buckets are: `Duplicates`, `Conflicts`, `Staleness`, `Gaps`, `Naming`, `Env`, `OpenAPI`, `Testing`, `Versioning`, `Health`, `Other`.
- `classification`: Workflow status for the issue: `UNCLASSIFIED`, `RESOLVED`, `CONFLICT`, or `RESEARCH`. Scripts and rollups use this to route items into backlogs.
- `classification_ref`: Free-text pointer that ties the issue to a concrete decision or theme, such as an ADR ID, migration plan section, or research topic label.
- `notes`: Short human-readable explanation or extra context about why the issue received its classification.

Later phases should always update this table via the Phase 2 scripts (e.g. `triage` CLI, batch generator, Droid runner, rollup generator) rather than editing it manually, so that IDs remain stable and rollup documents stay consistent.

## Phase D: Ongoing Reclassification Workflow

When revisiting or expanding the triage in later phases, use this loop:

1. **Keep the table, clear batches**: Do not delete `issues_index.csv`. Instead, remove old batch prompt and result files: `rm -rf working/phase2/batches working/phase2/batch_results` and recreate `working/phase2/batch_results/`.
2. **Reset classifications**: Run the reset helper (or equivalent script) that sets `classification` to `UNCLASSIFIED` and clears `classification_ref`, `issue_type`, and `notes` for all rows.
3. **Ensure IDs exist**: If new red flags were added to summaries without IDs, run `uv run triage scan` to (re)scan summaries, assign `ISS-XXXX` IDs, and keep existing IDs stable where possible.
4. **Generate batches**: Run `uv run triage batch --batch-size N` to create fresh `working/phase2/batches/classify_batch_XXX.md` files for all `UNCLASSIFIED` issues.
5. **Run Droid over batches**: Execute `uv run python working/phase2/scripts/run_droid_batches.py` to call `droid exec --auto high -f` for each batch and write JSON outputs into `working/phase2/batch_results/`.
6. **Apply results to the table**: Run `uv run triage update --results-dir working/phase2/batch_results` so that `classification`, `classification_ref`, `issue_type`, and `notes` are populated exclusively from Droid outputs.
7. **Regenerate rollups**: Run `uv run triage rollup` to refresh `conflict_backlog.md`, `research_backlog.md`, and the summary section of `working/phase1/content_issues.md` using the updated table.

