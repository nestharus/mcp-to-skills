# Issue Classification Batch 7

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


ISS-0061: Memory and concurrency deep dives (GIL behavior, pools, zero-copy, tracemalloc) might overwhelm readers at this project’s maturity level.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0062: Uses generic domains (users/items/movies) rather than the MCP metadata domain, so examples require translation.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0063: Testing recommendations (pytest + TestClient + fixtures) should be reconciled with existing `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`, and `tests/conftest.py`.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0064: Observability advice assumes external services (Prometheus, OpenTelemetry, Sentry/Honeycomb) not present in this repo, which could mislead implementers.
Source: working/phase1/summaries/docs/to_integrate/fastapi-best-practices.summary.md

ISS-0065: Overlap with `docs/to_integrate/development-workflow.md` where both describe running `uv run lint` and pytest before committing; they differ on whether to exclude E2E tests by default.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0066: Overlap with `README.md` "Code Quality" section, which also explains pre-commit hooks and `uv run lint`, risking duplicated guidance.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0067: References to an `e2e` pytest marker (`pytest -m e2e`) that may not be configured in `pyproject.toml`.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0068: Mentions of Coderabbit and Macroscope as mandatory CI checks without visible configuration in `.github/` workflows.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0069: Sonar is treated as a required PR check but there is no obvious `sonar-project.properties` or documented Sonar setup.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0070: Conventional Commits are required for final squashed commits, yet no automated enforcement (e.g., commitlint) is documented.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md


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
