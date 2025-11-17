# Issue Classification Batch 17

Please classify and assign an issue_type for the following 9 issues from the Phase 1 content analysis.

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


ISS-0161: Major overlap with `docs/TESTING_ARCHITECTURE.md`: both sources outline a strategy for placing unit, component, integration, and E2E tests, but TEST_9 uses generic examples while the existing docs are project-specific.
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0162: Directory structure mismatch: TEST_9 assumes a `src/myapp/` layout, whereas this project uses an `app/` package (for example `app/routes/metadata_router_v1.py`).
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0163: Coverage expectations duplication: TEST_9 promotes an 80%+ coverage target that already appears in `docs/TEST.md`, risking conflicting updates over time.
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0164: Shared fixtures location ambiguity: TEST_9 recommends a `tests/fixtures/` directory, but this project centralizes shared fixtures in `tests/conftest.py` (and may not have a `tests/fixtures/` package at all).
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0165: Integration test categorization mismatch: TEST_9 suggests organizing integration tests by client/server/middleware, which may not match the actual structure in `tests/integration/` for this project.
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0166: Generic testing patterns (error handling, type guards, transformations) use placeholder types rather than concrete project concepts such as `MetadataItem`, `FetchRequest`, or `MCPManager`.
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0167: Debugging guidance is generic Python/pytest advice and does not address FastAPI-specific concerns like debugging async tests or dependency overrides.
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0168: Does not mention existing pytest markers (such as `@pytest.mark.e2e`) that may be configured in `pyproject.toml` and used to select subsets of tests.
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md

ISS-0169: Recommends mirroring a `src/myapp/` structure in tests, while `docs/TEST.md` already recommends mirroring the `app/` structure (for example `tests/unit/core/test_settings.py` for `app/core/settings.py`).
Source: working/phase1/summaries/docs/to_integrate/TEST_9.summary.md


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
