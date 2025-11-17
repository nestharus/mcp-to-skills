# Issue Classification Batch 11

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


ISS-0101: **Overlap with STYLE_1**: Repeats naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE) already covered in STYLE_1; these should be consolidated into a single style guide section.
Source: working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md

ISS-0102: **Overlap with api-patterns-guide**: Domain modeling patterns overlap with the schemas and generics guidance in `docs/to_integrate/api-patterns-guide.md` and should be merged or cross-referenced.
Source: working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md

ISS-0103: **Missing linting enforcement**: Recommends naming conventions but does not describe how they are enforced; this should be aligned with the actual configuration in `pyproject.toml` and the Ruff setup.
Source: working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md

ISS-0104: **Constants vs configuration**: Treats all UPPER_SNAKE_CASE values as constants without differentiating configuration that may come from environment or settings modules such as `app/core/settings.py`.
Source: working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md

ISS-0105: **Project structure mismatch**: The sample project layout (`api/routes/users.py`) does not match this repository, which uses `app/routes/metadata_router_v1.py` and MCP-focused services; examples should be updated to use the actual module structure.
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md

ISS-0106: **Service layer not integrated**: STYLE_5 assumes thin route handlers delegating to services, but `app/routes/metadata_router_v1.py` currently contains hardcoded logic and does not call `app/services/mcp_manager.py`, so the pattern is aspirational.
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md

ISS-0107: **Overlap with STYLE_6**: Function design and route handler patterns are repeated in STYLE_6's router sections; these should be consolidated into a single architecture/style document.
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md

ISS-0108: **Overlap with api-patterns-guide**: The recommendations for thin handlers and service delegation overlap heavily with `docs/to_integrate/api-patterns-guide.md` (especially sections on routers and services).
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md

ISS-0109: **Overlap with fastapi-best-practices**: Async/await and concurrency guidance overlaps with `docs/to_integrate/fastapi-best-practices.md`; duplication should be reduced.
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md

ISS-0110: **Missing complexity enforcement details**: Suggests small functions but does not specify how tools (for example, Ruff, pylint) enforce max complexity or lines; should be aligned with `pyproject.toml`.
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md


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
