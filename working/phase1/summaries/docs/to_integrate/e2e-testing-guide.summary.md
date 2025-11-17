## Purpose
- Establish project-specific end-to-end (E2E) testing patterns for the FastAPI service using a live server process, real HTTP requests via `httpx`, soft assertions via `pytest-check`, and a dedicated `@pytest.mark.e2e` marker to distinguish slow, full-stack tests from faster integration tests.

## Main Topics
- Distinguishes E2E tests (live server, real HTTP, full process) from integration tests (in-process via `httpx.AsyncClient` + `ASGITransport`).
- Proposes fixture architecture with a `live_server` session-scoped fixture that starts `scripts/start-server.py` and an `api_client` fixture that issues real HTTP requests to `http://127.0.0.1:8008`.
- Describes organizing tests under `tests/e2e/` with all E2E tests marked using `@pytest.mark.e2e` and filtered via `pytest -m e2e` / `pytest -m "not e2e"`.
- Shows examples of E2E tests using `pytest-check` (`check.equal`, `check.is_in`, etc.) to accumulate multiple assertion failures per test run.
- Provides example test scenarios for health checks, successful metadata fetches, and validation errors against live endpoints.

## Opinions / Guidelines
- All E2E tests should use the `@pytest.mark.e2e` marker so they can be selectively included/excluded from CI and local runs.
- E2E tests should use `pytest-check` for soft assertions so that a single test can validate multiple response aspects (status, headers, body) without stopping on the first failure.
- E2E tests must be placed under a dedicated `tests/e2e/` directory to keep them distinct from unit/integration/component tests and to signal their slower nature.
- `live_server` should be session-scoped to amortize server startup cost across all E2E tests while `api_client` should reuse the same base URL and configuration.
- E2E tests should treat the application as a black box, invoking the `scripts/start-server.py` entrypoint and communicating only over HTTP to validate the compiled application stack (settings, wiring, routing, startup behavior).
- Health checks should rely on a dedicated readiness endpoint (described as `/api/metadata/v1/health` in the guide) with polling and timeouts before running the main E2E assertions.

## Assumptions
- Test stack is built on `pytest` + `pytest-asyncio` with async test support and fixtures.
- HTTP client for both integration and E2E tests is `httpx` (specifically `AsyncClient`).
- `pytest-check` is available and configured so `check.*` calls work in tests.
- The service is started via `scripts/start-server.py`, which accepts host/port/health-related CLI flags and runs a production-like app.
- There is a health endpoint at `/api/metadata/v1/health` returning a JSON payload such as `{ "status": "ok" }` with HTTP 200.
- The `@pytest.mark.e2e` marker is registered in `pyproject.toml` under `tool.pytest.ini_options.markers`.
- A `tests/e2e/` directory exists and is included in `tool.pytest.ini_options.testpaths`.

## Staleness Indicators
- The guide relies on `live_server` and `api_client` fixtures that do not exist in the actual `tests/conftest.py`, which only defines `test_settings`, `test_app`, `client`, `client_include_error_body`, and `async_client` fixtures.
- It assumes `pytest-check` is installed, but `pyproject.toml` currently lacks this dependency in any dev `dependency-groups`.
- It assumes a registered `e2e` marker, but the actual `pyproject.toml` has an empty `markers = []` list under `tool.pytest.ini_options`.
- It organizes tests under `tests/e2e/`, yet the repository only has `tests/unit/`, `tests/integration/`, and `tests/component/` directories and no `tests/e2e/`.
- The guide refers to a health endpoint at `/api/metadata/v1/health`, while `scripts/start-server.py` performs health checks against `/health`, and `app/routes/metadata_router_v1.py` defines the route at `/health` (mounted under the metadata router prefix).
- Example endpoints such as `/api/metadata/v1/fetch` match the project, but health-path usage is inconsistent with the actual router and script behavior.
- The documentation assumes tests use `pytest-check`-style soft assertions, but current tests (e.g., `tests/integration/test_metadata_router.py`) use plain `assert` statements only.
- There is conceptual overlap with `docs/to_integrate/TEST_7.md` and its summary regarding E2E concepts (health checks, live server vs client) that is not reconciled.

## Tags
- e2e
- testing
- fixtures
- pytest-check
- live-server
- httpx
- fastapi
- pytest
- asyncio
- soft-assertions
- health-checks
- black-box-testing

## Preliminary Target Docs
- Primary: Update or replace `docs/to_integrate/e2e-testing-guide.md` with a reconciled E2E guide aligned to the actual project state (fixtures, endpoints, ports, dependencies).
- Secondary: Extend `docs/TEST.md` with a dedicated section on E2E testing that references the agreed fixture patterns and markers.
- Tertiary: Reference from `docs/TESTING_ARCHITECTURE.md` to explain how the E2E layer fits into the overall test pyramid and architecture.

## Red Flags / Gaps
- Major conceptual duplication with `TEST_7.summary.md` on E2E testing (health checks, live server vs in-process testing, polling patterns) without clear ownership of which guide is authoritative.
- `live_server` and `api_client` fixtures described here are not present in `tests/conftest.py`, so the examples cannot be run as-is.
- `pytest-check` is described as required for E2E tests but is not part of the actual dev dependencies in `pyproject.toml`.
- The `@pytest.mark.e2e` marker is central to the guide but is not defined in the actual `tool.pytest.ini_options.markers` configuration.
- Health endpoint path in the examples (`/api/metadata/v1/health`) conflicts with the actual health check usage in `scripts/start-server.py` and the `/health` route in `metadata_router_v1.py`.
- The directory layout assumes `tests/e2e/` but the current repository has no such directory, making the documented test paths hypothetical.
- Suggested soft assertion style using `pytest-check` conflicts with existing tests that rely solely on standard `assert` statements.
- Overlaps and potential contradictions with `docs/TEST.md` regarding FastAPI testing patterns, fixtures, and async testing practices.
- Example fixture implementations in `docs/to_integrate/test_fixtures_soft_and_e2e.py` duplicate and diverge from existing integration fixtures, creating a risk of multiple patterns.
- Port configuration for the E2E server (`TEST_PORT = 8008`) differs from `scripts/start-server.py`'s default port (`8000`), which could cause confusion.
- The guide assumes health polling to `/api/metadata/v1/health` but the actual mounted route structure depends on how the router is included in `app/main.py`.
- No discussion of how the E2E layer interacts with the `--skip-health-check` flag in `scripts/start-server.py`, even though fixtures may perform their own polling.
- The recommended `pytestmark = pytest.mark.e2e` pattern is not used anywhere in current tests, indicating the practice is not yet adopted.
- Missing coverage of how E2E tests should configure or validate MCP configuration paths (`MCP_CONFIG_PATH`) and settings.
- No guidance on ensuring proper cleanup of server processes on test failures or interruptions beyond the basic fixture outline.

## References
- Source: `docs/to_integrate/e2e-testing-guide.md`.
- Related conceptual doc: `docs/to_integrate/TEST_7.md` and `working/phase1/summaries/docs/to_integrate/TEST_7.summary.md`.
- Configuration reference: `docs/to_integrate/e2e_dependencies.md` and `pyproject.toml` (dev dependencies, pytest config).
- Fixture reference: `docs/to_integrate/test_fixtures_soft_and_e2e.py` and actual `tests/conftest.py`.
- Runtime behavior: `scripts/start-server.py` (server startup, health checks) and `app/routes/metadata_router_v1.py` (health endpoint definition).
- Current test style: `tests/integration/test_metadata_router.py` and other tests under `tests/`.
