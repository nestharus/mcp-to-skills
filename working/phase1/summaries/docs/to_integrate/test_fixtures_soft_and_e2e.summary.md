## Purpose
- Provide example pytest fixture implementations for a two-tier testing strategy: fast integration tests using in-process `ASGITransport`, and slower E2E tests using a live server process and real HTTP requests.

## Main Topics
- Tier 1 (integration) fixtures: an `app` fixture that imports the FastAPI application (via `app.main`) and an `async_client` fixture that wraps the app with `httpx.AsyncClient` + `ASGITransport` for fast, in-process HTTP-style testing.
- Tier 2 (E2E) fixtures: constants like `TEST_PORT = 8008` and `BASE_URL`, a `_run_server` helper that launches `scripts/start-server.py` in a subprocess, and a `live_server` session-scoped fixture that starts the server in a `multiprocessing.Process` and polls a health endpoint for readiness.
- `api_client` session-scoped fixture that provides an `httpx.AsyncClient` targeting `BASE_URL` for real HTTP E2E tests against the running server.
- Health check polling logic: repeated GET requests to `/api/metadata/v1/health` with a fixed timeout (20 seconds) and small sleep intervals between retries.
- Cleanup behavior: terminating and joining the server process when the `live_server` fixture is torn down.

## Opinions / Guidelines
- Use function-scoped fixtures for in-process integration tests to keep them fast and isolated while reusing the app and async client setup.
- Use session-scoped fixtures (`live_server`, `api_client`) for E2E tests to amortize the cost of starting the server across the entire E2E test suite.
- Start the server via the real entrypoint (`scripts/start-server.py`) with `--skip-health-check`, letting the fixture own the readiness polling.
- Implement health checks with bounded timeouts and short polling intervals to balance responsiveness and flakiness.
- Manage the server process using `multiprocessing.Process` and ensure it is terminated and joined during teardown to avoid orphaned processes.
- Keep a clear conceptual separation between integration tests (using `ASGITransport`) and E2E tests (using real network I/O) and do not mix the two patterns within the same fixtures.

## Assumptions
- Tests use `pytest` and `pytest-asyncio` for async fixtures and test functions.
- The web stack is FastAPI-based, with an importable app module (shown as `app.main`).
- `httpx` is the HTTP client library for both integration and E2E tests.
- `scripts/start-server.py` is the main entrypoint, accepts `--host`, `--port`, and `--skip-health-check` flags, and runs the same app used in production.
- There is a health endpoint at `/api/metadata/v1/health` returning 200 with `{ "status": "ok" }` when the server is ready.
- The testing environment can bind to `127.0.0.1:8008` without conflicts and can spawn additional processes.

## Staleness Indicators
- None of the Tier 2 fixtures (`live_server`, `api_client`, `_run_server`, E2E helper constants) exist in the actual `tests/conftest.py`, which only defines `test_settings`, `test_app`, `client`, `client_include_error_body`, and `async_client` fixtures.
- The Tier 1 fixtures in this example (`app`, `async_client`) duplicate functionality already provided by `tests/conftest.py`, but with different import paths and configuration (e.g., importing from `app.main` instead of using `create_app` from `app.core.factory`).
- The health endpoint path `/api/metadata/v1/health` in the polling logic does not match the actual project, where `app/routes/metadata_router_v1.py` defines `/health` and `scripts/start-server.py` performs health checks against `/health`.
- The example uses `TEST_PORT = 8008`, but `scripts/start-server.py` defines `DEFAULT_PORT = 8000`, and current tooling assumes port 8000 by default.
- The fixture patterns rely on E2E-focused dependencies and markers described in `e2e-testing-guide.md` and `e2e_dependencies.md` (e.g., `pytest-check`, `@pytest.mark.e2e`), which are not yet wired into the actual project.

## Tags
- testing
- e2e
- fixtures
- pytest
- pytest-asyncio
- httpx
- live-server
- integration-testing
- fastapi
- multiprocessing
- health-checks
- session-scope
- function-scope

## Preliminary Target Docs
- Primary: Potential basis for extending `tests/conftest.py` with E2E fixtures after reconciling with existing fixtures, endpoint paths, and port configuration.
- Secondary: Example code for `docs/TEST.md` or `docs/TESTING_ARCHITECTURE.md` to illustrate how integration vs E2E fixtures can be structured in this project.
- Tertiary: Code samples referenced from `docs/to_integrate/e2e-testing-guide.md` once the guide is aligned with the real configuration and routing.

## Red Flags / Gaps
- This file is an example/proposed fixture set and is not wired into the real test suite; none of the E2E fixtures are defined in `tests/conftest.py`.
- Tier 1 fixtures (`app`, `async_client`) diverge from existing fixtures: they import the app from `app.main` instead of using `create_app` from `app.core.factory`, and they use different base URLs (`http://test` vs `http://testserver`).
- Health polling targets `/api/metadata/v1/health`, but the actual router (`metadata_router_v1.py`) and `scripts/start-server.py` use `/health`, so the example would fail without changes.
- Uses `TEST_PORT = 8008` while the real server defaults to port 8000, which would break expectations of existing scripts and docs.
- The `_run_server` helper uses `subprocess.Popen`, while `live_server` uses `multiprocessing.Process`, resulting in two different process management patterns in the same file.
- Error handling around server startup is minimal: if the server fails to start, the health polling loop has limited diagnostics and may just time out.
- Hardcoded timeout (20 seconds) and polling interval (0.1 seconds) are not configurable and may not be optimal for CI or slower environments.
- Cleanup logic terminates and joins the process but does not handle edge cases (already-dead process, non-zero exit codes) or provide detailed logging.
- The `api_client` fixture is session-scoped and async-context-managed, which can be tricky with `pytest-asyncio` scoping and may require careful use in tests.
- The fixtures assume location and invocation details for `scripts/start-server.py` (e.g., working directory) that might not hold in all environments.
- There is no explicit connection to `@pytest.mark.e2e` in the code itself, even though the guide assumes that marker is used for E2E tests.
- The Tier terminology ("Tier 1" vs "Tier 2") is not used anywhere else in the project and may conflict with the existing test directory names (unit/integration/component).
- Dependencies implied by this file (`httpx`, `pytest-asyncio`, possibly `pytest-check`) must match `pyproject.toml`, but the doc does not verify or enforce this alignment.

## References
- Source: `docs/to_integrate/test_fixtures_soft_and_e2e.py`.
- Related docs: `docs/to_integrate/e2e-testing-guide.md` (describes how these fixtures are used) and `docs/to_integrate/e2e_dependencies.md` (lists needed dependencies and markers).
- Actual fixture baseline: `tests/conftest.py` (current integration fixture implementations).
- Runtime behavior: `scripts/start-server.py` (server entrypoint, CLI flags, health check behavior) and `app/routes/metadata_router_v1.py` (health endpoint definition).
- Broader testing context: `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`, and existing tests under `tests/`.
