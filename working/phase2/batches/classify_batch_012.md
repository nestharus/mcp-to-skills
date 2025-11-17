# Issue Classification Batch 12

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


ISS-0111: **Callback section relevance**: Emphasizes callback-style patterns that are less common in idiomatic Python FastAPI code; this section may be de-emphasized or simplified.
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md

ISS-0112: **File naming vs router content**: Recommends one responsibility per file, but `metadata_router_v1.py` contains multiple route functions; expectations for router modules should be clarified.
Source: working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md

ISS-0113: **Major duplication with api-patterns-guide**: Large portions of STYLE_6 (project structure, routers, services, repositories, and DI) closely mirror `docs/to_integrate/api-patterns-guide.md`; these two documents should be merged rather than maintained separately.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0114: **Overlap with fastapi-best-practices**: Architectural and SOLID/clean-architecture advice overlaps with `docs/to_integrate/fastapi-best-practices.md`; content should be deduplicated or clearly scoped.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0115: **Aspirational vs descriptive architecture**: The guide describes a mature layered architecture that is not yet implemented here (no repositories, minimal DI, hardcoded responses in `metadata_router_v1.py`), so it currently functions as a target state rather than a description of the existing system.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0116: **Database assumption**: Assumes a relational database and SQLAlchemy sessions, but this project has no concrete database setup; guidance should be made database-agnostic or clearly marked as future work.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0117: **Missing custom exception layer**: Recommends custom business exceptions (for example, `UserNotFoundError`, `UserAlreadyExistsError`) and a centralized error-handling strategy, but the project lacks an `app/core/errors.py` or equivalent exception hierarchy.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0118: **Dependency injection not implemented end-to-end**: Shows complete DI chains (database → repository → service), while `app/core/dependencies.py` only wires settings; integrating services and repositories via DI remains future work.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0119: **Domain mismatch**: Examples reference generic User/Project domains instead of the MCP metadata domain (for example, `MetadataItem`, `FetchRequest`, and related contracts in `app/contracts/metadata_contract.py`).
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0120: **Overlap with STYLE_5**: Thin route handlers and service delegation rules are repeated in STYLE_5; these should be consolidated into a single set of routing/service guidelines.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md


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
