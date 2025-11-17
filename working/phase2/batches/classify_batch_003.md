# Issue Classification Batch 3

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


ISS-0021: Significant conceptual overlap with `fastapi-best-practices.md`, especially around clean architecture and SOLID ideas.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0022: Assumes SQLAlchemy, DB sessions, and repository abstractions that the current project does not yet use.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0023: Describes routers/services/repositories and complex DI chains while current endpoints still use hardcoded data and minimal services.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0024: Frontend/TanStack Query alignment is assumed but not yet part of this repo’s actual scope.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0025: Domain examples (`Project`, `User`) do not match the MCP metadata domain, making direct copy-paste misleading.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0026: No concrete custom exception hierarchy (`DomainError`, `NotFoundError`, etc.) exists in the codebase yet.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0027: Pagination patterns (`Paginated[T]`, `page`/`pageSize`) are not implemented in current routes (e.g., `/fetch` just returns a list).
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0028: Testing recommendations (TestClient, dependency overrides) need to be aligned with existing pytest fixtures and docs.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0029: Versioning guidance partially duplicates what is already done (`/api/v1` metadata router), so future edits must avoid contradictions.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md

ISS-0030: Empty placeholder blocks having a single authoritative architecture overview.
Source: working/phase1/summaries/docs/to_integrate/architecture-overview.summary.md


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
