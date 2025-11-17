# Issue Classification Batch 16

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


ISS-0151: Overlaps with `docs/TEST.md` fixture section: both recommend fixtures to avoid duplication, yet `docs/TEST.md` already documents project-specific fixtures such as `test_settings`, `test_app`, `client`, and `async_client`.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0152: Generic examples (`fetch_user`, `UserService`, `create_user_db`) are not aligned with the project's actual domain types such as `MCPManager`, `MetadataItem`, or metadata fetch requests.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0153: unittest-based examples may be misleading if the project relies exclusively on pytest-style tests and functions.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0154: Async testing guidance is incomplete: TEST_8 advises avoiding unnecessary async without explaining how to handle necessary async endpoints, which `docs/TEST.md` already addresses.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0155: Coverage and quality themes overlap with `docs/TEST.md`, which already documents pytest-cov usage and coverage expectations.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0156: Temporary resource management guidance uses `tempfile` and `shutil`, but `docs/TEST.md` recommends pytest's `tmp_path` fixture for temporary files and directories.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0157: Test independence advice is generic and duplicates the rationale already described in `docs/TESTING_ARCHITECTURE.md` for fixture scoping and isolation.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0158: Assertion style recommendations use plain `assert`, while some parts of the project (for example E2E tests) may prefer pytest-check for soft assertions.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0159: Mocking patterns ignore FastAPI-specific mechanisms like `app.dependency_overrides`, which are already covered in `docs/TEST.md` and better aligned with this codebase.
Source: working/phase1/summaries/docs/to_integrate/TEST_8.summary.md

ISS-0160: Major overlap with `docs/TEST.md` on running tests: both documents describe pytest commands such as `pytest -k`, `pytest path`, and `pytest path::test_name` for focused runs.
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
