## Purpose
Document debugging techniques for pytest-based tests and strategies for organizing tests, covering print/logging usage, debugger integration, focused test runs, common testing patterns (error handling, type guards, transformations), and conventions for test placement.

## Main Topics
- Debugging with `print()` or logging calls inside test bodies to quickly inspect state.
- Using `breakpoint()` or `pdb.set_trace()` for interactive debugging sessions inside tests.
- Running specific tests with pytest using `-k` expressions, direct file paths, and `::` syntax for selecting functions or classes.
- Testing error handling with `pytest.raises`, including message matching.
- Testing type guards and predicate functions with explicit True/False assertions.
- Testing transformations by asserting on output shape and content.
- Test placement strategy across `tests/unit/`, `tests/component/`, `tests/integration/`, and `tests/e2e/` layers.
- Mirroring application structure in test modules (e.g., `package/module.py` → `tests/unit/test_module.py`).
- Organizing component and integration tests around feature or component boundaries.
- Creating shared fixtures in dedicated modules or directories for reuse across suites.
- Coverage expectations (for example 80%+ via pytest-cov or coverage.py) and including all relevant runtime packages.

## Opinions / Guidelines
- Use `print()` or logging for quick, disposable debugging, but avoid leaving noisy output in long-lived tests.
- Prefer `breakpoint()` (Python 3.7+) or `pdb.set_trace()` when you need to inspect state interactively.
- Narrow down failing tests by running targeted selections via `pytest -k pattern` or `pytest path::test_name`.
- Use `pytest.raises(ExceptionType, match="pattern")` to verify error handling and error messages.
- For type guards and predicates, assert explicit boolean outcomes (`assert is_valid is True` / `False`) to keep intent clear.
- For transformations, assert on the exact structure and content of the returned data rather than superficial properties.
- Mirror the application package structure under `tests/` to make it easy to find corresponding tests.
- Group component tests by feature or boundary rather than strictly by module name when it aids readability.
- Use shared fixtures modules or `tests/conftest.py` for common setup such as DB state, HTTP clients, or data builders.
- Maintain a coverage target (for example 80%+) using pytest-cov or coverage.py, and ensure all runtime packages are included.

## Assumptions
- pytest is the primary test runner for the project.
- The codebase targets Python 3.7+ so `breakpoint()` is available.
- Tests reside under a `tests/` directory at the project root.
- Application code lives under a dedicated package (examples in TEST_9 use `src/myapp/`).
- pytest-cov or coverage.py is configured for coverage reporting.
- Developers are familiar with pytest's selection mechanisms (`-k`, `::`) for focused runs.
- Shared fixtures are centralized in modules such as `tests/conftest.py` or `tests/fixtures/`.

## Staleness Indicators
- Uses generic paths like `src/myapp/user.py` and `UserService` that do not match the actual project structure (which uses an `app/` package instead of `src/myapp/`).
- Assumes a `src/`-based layout, while this project organizes application code under `app/`.
- Does not reference `tests/conftest.py`, which already serves as the central place for shared fixtures.
- Omits mention of `docs/TEST.md`, which already documents how to run tests, select subsets, and interpret failures.
- Does not reference `docs/TESTING_ARCHITECTURE.md`, which describes the unit/component/integration layering for this project.
- Repeats coverage expectations (for example 80%+) that are already recorded in `docs/TEST.md` without linking to that source of truth.
- Recommends a `tests/fixtures/` directory, but this project may rely primarily on `tests/conftest.py` instead.
- Suggests integration test categorization (client/server/middleware) that may not match the actual organization in `tests/integration/`.

## Tags
testing, pytest, debugging, test-organization, coverage, pdb, breakpoint, test-placement, fixtures, error-handling, type-guards, transformations, best-practices

## Preliminary Target Docs
- Primary: extend `docs/TEST.md` with a "Debugging Tests" section that consolidates debugging tips and targeted test run patterns.
- Secondary: reconcile and align test placement and layering guidance with `docs/TESTING_ARCHITECTURE.md` so unit/component/integration/e2e boundaries are consistently described.
- Tertiary: consider a dedicated `docs/debugging-guide.md` if debugging content grows substantially, while keeping it consistent with the main testing documents.

## Red Flags
1. Major overlap with `docs/TEST.md` on running tests: both documents describe pytest commands such as `pytest -k`, `pytest path`, and `pytest path::test_name` for focused runs.
2. Major overlap with `docs/TESTING_ARCHITECTURE.md`: both sources outline a strategy for placing unit, component, integration, and E2E tests, but TEST_9 uses generic examples while the existing docs are project-specific.
3. Directory structure mismatch: TEST_9 assumes a `src/myapp/` layout, whereas this project uses an `app/` package (for example `app/routes/metadata_router_v1.py`).
4. Coverage expectations duplication: TEST_9 promotes an 80%+ coverage target that already appears in `docs/TEST.md`, risking conflicting updates over time.
5. Shared fixtures location ambiguity: TEST_9 recommends a `tests/fixtures/` directory, but this project centralizes shared fixtures in `tests/conftest.py` (and may not have a `tests/fixtures/` package at all).
6. Integration test categorization mismatch: TEST_9 suggests organizing integration tests by client/server/middleware, which may not match the actual structure in `tests/integration/` for this project.
7. Generic testing patterns (error handling, type guards, transformations) use placeholder types rather than concrete project concepts such as `MetadataItem`, `FetchRequest`, or `MCPManager`.
8. Debugging guidance is generic Python/pytest advice and does not address FastAPI-specific concerns like debugging async tests or dependency overrides.
9. Does not mention existing pytest markers (such as `@pytest.mark.e2e`) that may be configured in `pyproject.toml` and used to select subsets of tests.
10. Recommends mirroring a `src/myapp/` structure in tests, while `docs/TEST.md` already recommends mirroring the `app/` structure (for example `tests/unit/core/test_settings.py` for `app/core/settings.py`).

## References
- `docs/to_integrate/TEST_9.md` (source document).
- `docs/TEST.md` (overlaps on running tests, debugging patterns, test organization, and coverage expectations).
- `docs/TESTING_ARCHITECTURE.md` (overlaps on test placement strategy and layering).
- `tests/conftest.py` (canonical location for shared fixtures in this project).
- `tests/unit/`, `tests/integration/`, `tests/component/` (actual test directories to align with the documented strategy).
- `app/` (actual application package structure, as opposed to `src/myapp/`).
- `pyproject.toml` (pytest configuration, markers, and coverage settings).
- `app/contracts/metadata_contract.py` (candidate for concrete examples of testing error handling and transformations).
- `app/routes/metadata_router_v1.py` (candidate for concrete examples of API-focused tests and debugging).
