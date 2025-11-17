# Phase 1 Working Guide

## Overview
- Phase 1 focuses on producing structured summaries of existing documentation to prepare for later integration phases.
- All outputs live under `working/phase1/`, including `summaries/`, future `inventory.md`, and any tracking artifacts.
- Summaries fuel downstream aggregation scripts, so consistency across paths and filenames is mandatory.

## Summary File Convention
1. Mirror the source file's relative path under `working/phase1/summaries/`.
   - `docs/LIFECYCLE.md` → `working/phase1/summaries/docs/LIFECYCLE.summary.md`
   - `README.md` (root) → `working/phase1/summaries/README.summary.md`
2. Recreate nested directories exactly.
   - `docs/to_integrate/TEST_1.md` → `working/phase1/summaries/docs/to_integrate/TEST_1.summary.md`
3. Filename pattern: drop the original `.md`, keep the basename, append `.summary.md` (no double extensions).
4. Apply the same pattern to any future directories so scripts can glob `working/phase1/summaries/**/*.summary.md` reliably.

## Summary Structure Template
Each summary should include the following sections in order (use Markdown headings or bold labels):
- Purpose
- Main Topics
- Opinions/Guidelines
- Assumptions
- Staleness Indicators
- Tags
- Preliminary Target Docs
- Red Flags
- References (optional but recommended for traceability)

## Examples
- `docs/LIFECYCLE.md` → `working/phase1/summaries/docs/LIFECYCLE.summary.md`
- `docs/TEST.md` → `working/phase1/summaries/docs/TEST.summary.md`
- `docs/TESTING_ARCHITECTURE.md` → `working/phase1/summaries/docs/TESTING_ARCHITECTURE.summary.md`
- `README.md` → `working/phase1/summaries/README.summary.md`
- `AGENTS.md` → `working/phase1/summaries/AGENTS.summary.md`

## Future Extensions
- When summarizing `docs/to_integrate/*.md`, first create `working/phase1/summaries/docs/to_integrate/` (or deeper subfolders) before adding files.
- Keep filenames consistent (`STYLE_2.summary.md`, `linting-guide.summary.md`, etc.) so future aggregation phases can map summaries back to their sources programmatically.
- If new artifact types (e.g., inventories, issue logs) are added, reference this README to explain placement and naming conventions.
