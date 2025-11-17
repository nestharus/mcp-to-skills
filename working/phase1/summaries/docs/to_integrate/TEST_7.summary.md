## Purpose
Document E2E/API testing strategies for FastAPI services, emphasizing health/readiness endpoints, polling helpers with timeouts, and the distinction between integration tests (in-process TestClient) and true E2E tests (real Uvicorn process with httpx).

## Main Topics
- Terminology clarification: unit vs integration vs API E2E tests.
- Health/readiness endpoints as "hydration markers" to avoid `time.sleep` in tests.
- Polling helpers with bounded timeouts for async/background jobs and eventual consistency.
- `wait_for_service` utility pattern implemented with httpx against a live Uvicorn server.
- Pytest fixtures for "app is ready" checks (session-scoped) that gate E2E suites.
- Example API E2E test that polls a job endpoint until completion.
- Guidance on when to use in-process TestClient vs real Uvicorn-based E2E tests.
- Optional docker-compose integration for orchestrating multi-service E2E environments.

## Opinions / Guidelines
- API-only E2E testing is valid for backend-heavy systems; a browser UI is not required.
- Avoid `time.sleep()` and guesswork; use explicit readiness checks via health/readiness endpoints.
- Prefer health/readiness endpoints over arbitrary delays to make tests deterministic and observable.
- Use polling helpers with clear, bounded timeouts for async flows and background jobs.
- Use httpx + pytest fixtures hitting a real Uvicorn process for true E2E, reserving TestClient for faster integration-style tests.
- Implement session-scoped fixtures to manage service startup/teardown for the E2E layer.
- Follow a bounded polling pattern such as `deadline = time.time() + timeout` and loop until success or timeout.

## Assumptions
- FastAPI is the web framework for the service under test.
- Uvicorn is used as the ASGI server in production-like E2E tests.
- pytest is the primary test runner for all test layers.
- httpx is the HTTP client library used in E2E tests.
- docker-compose may be used to orchestrate dependent services for E2E environments.
- A health endpoint exists at `/healthz` or similar that signals readiness.
- Background/async jobs are part of the system and are exercised via API endpoints.

## Staleness Indicators
- Generic examples (`/jobs` endpoint, `_jobs` dict) are not tied to actual project endpoints such as `/api/metadata/v1/fetch` or `/api/metadata/v1/health`.
- References a generic `app/main.py` structure and startup flow instead of the project's actual structure (for example `app/core/factory.py` and `app/routes/metadata_router_v1.py`).
- Does not reference existing project-specific E2E fixtures (such as `live_server` or `api_client`) that are defined in `tests/conftest.py`.
- Does not acknowledge the existing `docs/to_integrate/e2e-testing-guide.md`, which already covers the same concepts with project-specific implementation details.
- Assumes helpers live in `tests/utils.py`, whereas this project may centralize helpers and fixtures in `tests/conftest.py`.
- Omits any mention of the `@pytest.mark.e2e` marker and marker usage already established in the project.
- Overlaps with `docs/to_integrate/e2e_dependencies.md` around pytest E2E markers, dependency ordering, and fixture requirements for E2E suites.

## Tags
testing, e2e, api-testing, fastapi, pytest, httpx, health-checks, polling, async, uvicorn, docker-compose, readiness, best-practices

## Preliminary Target Docs
- Primary: `docs/to_integrate/e2e-testing-guide.md` (project-specific E2E guide that already implements these patterns).
- Secondary: extend `docs/TEST.md` with a dedicated E2E section if consolidating all testing guidance into a single document.
- Tertiary: reference from `docs/TESTING_ARCHITECTURE.md` to explain the rationale for an E2E layer and its health-check/polling patterns.

## Red Flags
1. Major duplication with `docs/to_integrate/e2e-testing-guide.md`: both documents cover E2E testing for FastAPI, health checks, live server fixtures, and httpx usage, but the existing guide is project-specific while TEST_7 is generic/tutorial-style.
2. Health endpoint path mismatch: TEST_7 assumes `/healthz`, whereas the project exposes a health endpoint under the metadata API namespace (for example `/api/metadata/v1/health`).
3. Fixture naming conflict: TEST_7 suggests fixtures like `api_base_url` and `wait_for_api`, but the project already uses fixtures such as `live_server` and `api_client` in `tests/conftest.py`.
4. Generic job polling example (`/jobs`, `_jobs` dict) does not reflect the project's actual domain (MCP metadata fetching and related flows).
5. Overlap with `docs/TEST.md`: the "When to use TestClient vs real Uvicorn" guidance appears in both places, with `docs/TEST.md` already providing FastAPI-specific recommendations.
6. Missing pytest-check integration: TEST_7 uses plain `assert` statements, while `docs/to_integrate/e2e-testing-guide.md` recommends pytest-check for soft assertions in E2E tests.
7. docker-compose assumptions: TEST_7 positions docker-compose as the primary E2E orchestration tool, but the project's E2E guide focuses on using `scripts/start-server.py` directly without docker-compose.
8. No reference to the existing `@pytest.mark.e2e` marker or patterns like `pytest -m e2e`, which are already documented in the project.
9. Polling helper location ambiguity: TEST_7 suggests placing polling helpers in `tests/utils.py`, while this project appears to centralize shared helpers and fixtures in `tests/conftest.py`.
10. Eventual consistency example is too generic and would need adaptation to project-specific async scenarios such as MCP server metadata fetching with retries.

## References
- `docs/to_integrate/TEST_7.md` (source document).
- `docs/to_integrate/e2e-testing-guide.md` (major overlap, project-specific E2E guide).
- `docs/to_integrate/e2e_dependencies.md` (pytest markers and dependencies).
- `docs/TEST.md` (overlaps on TestClient vs AsyncClient and FastAPI testing guidance).
- `tests/conftest.py` (actual E2E fixtures such as `live_server` and `api_client`).
- `app/routes/metadata_router_v1.py` (actual health endpoint implementation).
- `scripts/start-server.py` (server startup script used in E2E tests).
