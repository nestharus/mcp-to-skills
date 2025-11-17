# Issue Classification Batch 15

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


ISS-0141: Health endpoint path mismatch: TEST_7 assumes `/healthz`, whereas the project exposes a health endpoint under the metadata API namespace (for example `/api/metadata/v1/health`).
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0142: Fixture naming conflict: TEST_7 suggests fixtures like `api_base_url` and `wait_for_api`, but the project already uses fixtures such as `live_server` and `api_client` in `tests/conftest.py`.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0143: Generic job polling example (`/jobs`, `_jobs` dict) does not reflect the project's actual domain (MCP metadata fetching and related flows).
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0144: Overlap with `docs/TEST.md`: the "When to use TestClient vs real Uvicorn" guidance appears in both places, with `docs/TEST.md` already providing FastAPI-specific recommendations.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0145: Missing pytest-check integration: TEST_7 uses plain `assert` statements, while `docs/to_integrate/e2e-testing-guide.md` recommends pytest-check for soft assertions in E2E tests.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0146: docker-compose assumptions: TEST_7 positions docker-compose as the primary E2E orchestration tool, but the project's E2E guide focuses on using `scripts/start-server.py` directly without docker-compose.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0147: No reference to the existing `@pytest.mark.e2e` marker or patterns like `pytest -m e2e`, which are already documented in the project.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0148: Polling helper location ambiguity: TEST_7 suggests placing polling helpers in `tests/utils.py`, while this project appears to centralize shared helpers and fixtures in `tests/conftest.py`.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0149: Eventual consistency example is too generic and would need adaptation to project-specific async scenarios such as MCP server metadata fetching with retries.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md

ISS-0150: Overlaps with `docs/TEST.md` mocking guidance: both documents describe mocking external dependencies and using `unittest.mock`, but TEST_8 stays generic while `docs/TEST.md` already covers FastAPI-specific patterns like dependency overrides.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md


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
