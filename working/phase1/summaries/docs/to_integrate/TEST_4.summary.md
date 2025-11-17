## Purpose
- Document pytest test naming conventions, organization strategies, execution commands, coverage reporting with pytest-cov, and test filtering mechanisms from `docs/to_integrate/TEST_4.md`.

## Main Topics
- Descriptive test naming patterns using a what/condition/outcome structure.
- Test organization within files (class-based vs flat function layout) and across suites (unit, integration, e2e).
- Pytest CLI usage for running all tests, subsets (by module, class, function), and specific suites.
- Coverage commands using pytest-cov, including `--cov` targets and `--cov-report` options (HTML, term-missing).
- Test selection and filtering with `-k` expressions and custom markers.
- Use of `@pytest.mark.skip` and `@pytest.mark.xfail` to manage incomplete or expected-failing tests.

## Opinions / Guidelines
- Prefer descriptive test names that clearly state what is being tested, under which condition, and the expected outcome.
- Use class-based organization (for example, `TestCreateUser`, `TestDeleteUser`) to group related behaviors when a domain area has many tests; use a flat layout for simpler modules.
- Standardize on pytest with pytest-cov as the primary test and coverage tool.
- Encourage consistent use of `--cov` with `--cov-report=term-missing` during local development for quick feedback on uncovered lines.
- Use `-k` expressions and markers for flexible selection of focused subsets during development and debugging.
- Apply `@pytest.mark.skip` for temporarily disabled tests with clear reasons, and `@pytest.mark.xfail` when a known bug or unimplemented behavior is being documented.

## Assumptions
- Pytest is the default test runner for the project.
- pytest-cov is installed and configured for coverage measurement.
- The repository follows a conventional layout with `tests/unit/`, `tests/integration/`, and `tests/e2e/` directories.
- Developers are comfortable using pytest node IDs, markers, and CLI options for targeted runs.
- Project workflows rely on `uv run pytest` and related commands even if TEST_4 does not explicitly mention `uv`.

## Staleness Indicators
- Examples reference generic modules and services (for example, `test_user_service.py`, `UserService`) rather than current project modules such as `app/contracts/metadata_contract.py` or `app/routes/metadata_router_v1.py`.
- Marker usage is described generically and may not match the markers actually configured under `[tool.pytest.ini_options]` in `pyproject.toml`.
- Commands are described directly with `pytest` rather than the `uv run pytest` workflow documented elsewhere in this repository.
- The document does not reference existing fixtures or utilities defined in `tests/conftest.py`.

## Tags
- testing, pytest, naming, organization, coverage, pytest-cov, markers, filtering, skip, xfail, cli-commands

## Preliminary Target Docs
- Primary: a consolidated testing guide (for example, `docs/testing-guide.md`) or the main `docs/TEST.md` file.
- Secondary: `docs/TESTING_ARCHITECTURE.md` for clarifying how within-file organization (classes vs functions) complements the existing directory-level testing architecture.
- Coverage and CLI command examples should be merged into the existing coverage and test-running sections rather than duplicated.

## Red Flags / Integration Risks
- Naming conventions partially overlap with the mirrored-structure guidance already present in `docs/TEST.md`, but TEST_4 introduces a more prescriptive what/condition/outcome pattern that must be reconciled.
- Within-file organization guidance (class-based vs flat) is new relative to `docs/TEST.md`, which currently focuses on directory layout; integration must avoid conflicting recommendations.
- Coverage commands using pytest-cov may duplicate or diverge from the coverage workflow already documented in `docs/TEST.md` (including specific `--cov` targets and reports).
- Marker and `-k` usage overlaps with existing mentions of custom markers; TEST_4 is more detailed, so content should be deduplicated rather than repeated.
- Skip/xfail usage is not currently emphasized in the main testing docs and will need careful integration to avoid sending mixed messages about temporarily disabled tests.
- Any mention of e2e testing and tools like Playwright must be checked against the current project tooling (for example, httpx/TestClient-based API tests) to avoid confusion.
- Generic examples such as `UserService` should be rewritten to use project-specific domains (for example, metadata routes or MCP manager behavior) during integration.
- All raw `pytest` commands should be aligned with the `uv run` workflow that the rest of the repository uses.

## References
- `docs/to_integrate/TEST_4.md`
- `docs/TEST.md` (test running and coverage sections)
- `docs/TESTING_ARCHITECTURE.md`
- `pyproject.toml` (pytest configuration, markers, coverage settings)
- `tests/conftest.py`
- `README.md` (testing and `uv` workflow references)
