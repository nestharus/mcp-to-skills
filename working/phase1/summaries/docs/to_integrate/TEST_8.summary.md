## Purpose
Document general testing best practices for Python/pytest projects, focusing on test speed, independence, assertion quality, single-responsibility tests, and fixture-based setup to reduce duplication.

## Main Topics
- Keeping tests fast by avoiding unnecessary async, mocking external dependencies, and testing observable behavior instead of implementation details.
- Making tests independent so they can run alone without ordering dependencies, with clean state handled via fixtures or teardown.
- Using descriptive assertions that check specific outcomes and include helpful messages when appropriate.
- Designing tests with a single, clear responsibility rather than mixing unrelated concerns in one function.
- Reducing duplication by using pytest fixtures or unittest `setUp` methods for shared setup.
- Mocking patterns with `unittest.mock.Mock`, `return_value`, and call assertions such as `assert_called_once_with`.
- Comparing fixture-based setup (pytest style) with unittest-style setup patterns.
- Managing temporary resources with `tempfile`, `shutil`, and similar utilities.

## Opinions / Guidelines
- Mock external dependencies (databases, HTTP clients, filesystem access) to keep tests fast and deterministic.
- Avoid testing implementation details such as private methods or internal call graphs; focus on public behavior.
- Ensure each test can be run in isolation without relying on execution order or shared global state.
- Clean up state in fixtures or teardown hooks to guarantee independence between tests.
- Prefer specific assertions like `assert user.email == "john@example.com"` over vague checks like `assert user.email`.
- Add custom assertion messages when they help clarify the intent or expected behavior.
- Keep each test focused on a narrow concern; split complex scenarios into multiple targeted tests.
- Use pytest fixtures to share setup logic instead of copy-pasting or deeply nested helpers.
- When using unittest-style tests, centralize setup in `setUp` or `setUpClass` to avoid duplication.
- Use `tempfile` and related utilities (or pytest tmp path fixtures) to handle temporary files and directories safely.

## Assumptions
- pytest is the primary test runner, although unittest-based examples may also appear.
- The project targets Python 3.x and has access to `unittest.mock` for mocking.
- Developers are familiar with pytest fixtures and unittest `TestCase` patterns.
- The codebase interacts with external systems (DB, HTTP, filesystem) that should be mocked in tests.
- Tests live under a standard `tests/` directory structure at the project root.

## Staleness Indicators
- Uses generic example functions and types (`fetch_user`, `UserService`, `create_user_db`) rather than project modules such as `app/services/mcp_manager.py` or `app/contracts/metadata_contract.py`.
- Does not reference project-specific fixtures defined in `tests/conftest.py` (for example `test_settings`, `test_app`, `client`, `async_client`).
- Omits mention of `docs/TEST.md`, which already documents mocking patterns, fixture usage, and testing best practices for this project.
- Includes unittest examples even though the project appears to be organized primarily around pytest-style tests.
- Does not address FastAPI-specific testing concerns (dependency overrides, TestClient vs AsyncClient) that are documented elsewhere.
- Provides no guidance on async test patterns, which are important for FastAPI-based systems.

## Tags
testing, pytest, best-practices, mocking, fixtures, test-independence, assertions, unittest, test-speed, cleanup

## Preliminary Target Docs
- Primary: extend `docs/TEST.md` with a "Best Practices" section that incorporates these generic guidelines and aligns them with project-specific patterns.
- Secondary: reference in `docs/TESTING_ARCHITECTURE.md` to explain the rationale for test independence, fixture usage, and layering.
- Tertiary: consider extracting a standalone `docs/testing-best-practices.md` if `docs/TEST.md` grows too large, while keeping it consistent with existing guidance.

## Red Flags
1. Overlaps with `docs/TEST.md` mocking guidance: both documents describe mocking external dependencies and using `unittest.mock`, but TEST_8 stays generic while `docs/TEST.md` already covers FastAPI-specific patterns like dependency overrides.
2. Overlaps with `docs/TEST.md` fixture section: both recommend fixtures to avoid duplication, yet `docs/TEST.md` already documents project-specific fixtures such as `test_settings`, `test_app`, `client`, and `async_client`.
3. Generic examples (`fetch_user`, `UserService`, `create_user_db`) are not aligned with the project's actual domain types such as `MCPManager`, `MetadataItem`, or metadata fetch requests.
4. unittest-based examples may be misleading if the project relies exclusively on pytest-style tests and functions.
5. Async testing guidance is incomplete: TEST_8 advises avoiding unnecessary async without explaining how to handle necessary async endpoints, which `docs/TEST.md` already addresses.
6. Coverage and quality themes overlap with `docs/TEST.md`, which already documents pytest-cov usage and coverage expectations.
7. Temporary resource management guidance uses `tempfile` and `shutil`, but `docs/TEST.md` recommends pytest's `tmp_path` fixture for temporary files and directories.
8. Test independence advice is generic and duplicates the rationale already described in `docs/TESTING_ARCHITECTURE.md` for fixture scoping and isolation.
9. Assertion style recommendations use plain `assert`, while some parts of the project (for example E2E tests) may prefer pytest-check for soft assertions.
10. Mocking patterns ignore FastAPI-specific mechanisms like `app.dependency_overrides`, which are already covered in `docs/TEST.md` and better aligned with this codebase.

## References
- `docs/to_integrate/TEST_8.md` (source document).
- `docs/TEST.md` (overlaps on mocking, fixtures, best practices, and coverage tooling).
- `docs/TESTING_ARCHITECTURE.md` (overlaps on test independence and fixture usage rationale).
- `tests/conftest.py` (canonical location for project fixtures such as `test_settings` and `client`).
- `app/services/mcp_manager.py` (candidate module for concrete mocking examples).
- `app/contracts/metadata_contract.py` (candidate module for illustrating assertion and validation patterns).
- `app/core/dependencies.py` (FastAPI dependency injection definitions relevant to mocking patterns via dependency overrides).
