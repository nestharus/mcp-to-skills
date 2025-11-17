# Issue Classification Batch 10

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


ISS-0091: **ErrorCode mismatch**: Example `ErrorCode` enum may not match actual error handling in `app/contracts/metadata_contract.py` or `app/routes/metadata_router_v1.py`—audit existing code.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0092: **Service layer gap**: No mention of existing `app/services/mcp_manager.py` or how it fits the service layer pattern described.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0093: **Router structure**: Doesn't reference existing `app/routes/metadata_router_v1.py` or explain how it aligns with recommended patterns.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0094: **Async patterns**: No mention of existing async patterns in `app/main.py` or `app/services/mcp_manager.py`—verify consistency.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0095: **TypeScript mapping table**: Mapping table is useful but may confuse Python-only developers—consider removing or moving to an appendix.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0096: **Generic naming overlap**: `TypeVar` naming guidance duplicates STYLE_1 and STYLE_2—consolidate in single style guide.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0097: **README/AGENTS alignment**: No direct conflicts with the tooling/workflow guidance in `README.md` or `AGENTS.md`, but FastAPI/testing guidance here must stay synchronized with those docs.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0098: **External module reference**: Mentions `ui_designer.shared_types`, which does not exist in this repository and appears to come from another project. Either remove or replace with a project-appropriate shared types module if one is introduced.
Source: working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md

ISS-0099: **Domain model mismatch**: Example types (`Project`, `ProjectStatus`, `DesignToken`) do not match the actual MCP metadata domain (`MetadataItem`, `FetchRequest`, etc.) defined in `app/contracts/metadata_contract.py`.
Source: working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md

ISS-0100: **Shared types assumption**: Assumes a shared types package for cross-service reuse, while this project is currently a single service with contracts living under `app/contracts/`.
Source: working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md


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
