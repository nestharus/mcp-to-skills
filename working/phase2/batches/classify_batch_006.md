# Issue Classification Batch 6

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


ISS-0051: Provides debugging tips but omits common issues like dependency conflicts, environment setup, or Docker-related problems, leaving gaps for new contributors.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0052: Does not document how to run specific test markers (unit, integration, component, e2e), despite other docs describing these tiers.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0053: References AGENTS.md for agent-specific workflow without clarifying how that interacts with the general development loop.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0054: Requires documentation updates alongside workflow changes but does not specify which docs (README, TEST docs, workflow docs) to touch, which can lead to inconsistency.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0055: Extensive overlap with `api-patterns-guide.md` on clean architecture, DI, layering, and testing; unmanaged duplication would be hard to maintain.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0056: Significant overlap with STYLE_6 for layered architecture and SRP/DIP, increasing the risk of conflicting advice.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0057: Many recommendations depend on infrastructure (DB, Redis, Celery, JWT/auth stack, observability stack) that does not exist in this repo yet.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0058: Authentication and RBAC sections are advanced and may be premature for current unauthenticated, stub endpoints.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0059: Celery and task queue patterns assume long-running/background work not yet defined in this project.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0060: Middleware and gateway optimizations (rate limiting, compression, HTTP/2 tuning) may be unnecessary overhead at current scale.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md


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
