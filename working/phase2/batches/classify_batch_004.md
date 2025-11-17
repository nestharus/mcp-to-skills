# Issue Classification Batch 4

Please classify and assign an issue_type for the following 10 issues from the Phase 1 content analysis.

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


ISS-0031: Unclear whether this should be a concise high-level overview or a detailed deep-dive.
Source: working/phase1/summaries/docs/to_integrate/architecture-overview.summary.md

ISS-0032: Scope overlaps with other architecture/patterns docs and may cause duplication once filled.
Source: working/phase1/summaries/docs/to_integrate/architecture-overview.summary.md

ISS-0033: No indication of how this document should relate to STYLE_6’s layered architecture guidance.
Source: working/phase1/summaries/docs/to_integrate/architecture-overview.summary.md

ISS-0034: Team may reference this file expecting guidance but find only filler content.
Source: working/phase1/summaries/docs/to_integrate/architecture-overview.summary.md

ISS-0035: Changesets tooling (`uv run changeset`, `uv run version-packages`, `uv run release`) may not yet be implemented in `pyproject.toml` `[tool.uv.scripts]` or `tools/`.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0036: The `.changeset/` directory may be missing, despite the guide assuming it exists and is used in all feature and bugfix PRs.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0037: Overlap with `docs/to_integrate/git-workflow.md` where commit conventions and release tagging are discussed separately, risking divergence.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0038: CI enforcement that fails PRs touching `app/` or `tools/` without changesets is recommended but not obviously configured in `.github/` workflows.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0039: Publishing workflow with `uv build` and `uv publish` is described without detailing how to configure credentials, indexes, or secrets.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0040: No guidance on handling pre-release versions (e.g., `1.0.0-alpha.1`), build metadata (e.g., `1.0.0+build.123`), or version conflicts.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md


## Output Format

For each issue, provide both a workflow classification and an issue_type bucket:
```json
{
  "ISS-XXXX": {
    "classification": "RESOLVED|CONFLICT|RESEARCH",
    "classification_ref": "ADR-0001 | Migration §3.2 | Ruff Configuration",
    "issue_type": "Duplicates|Conflicts|Staleness|Gaps|Naming|Env|OpenAPI|Testing|Versioning|Health|Other",
    "notes": "Brief explanation"
  }
}
```
