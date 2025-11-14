# Testing Guide

This project already ships with pytest, pytest-asyncio, and httpx so you can start writing tests immediately. The sections below outline how to structure, run, and extend the suite with FastAPI-specific tooling.

## Test Organization

- `tests/unit/`: Fastest feedback loop for functions and classes in isolation. Examples include exercising `Settings` validation in `app/core/settings.py` or checking `MetadataItem` and `FetchRequest` validators from `app/contracts/metadata_contract.py` with handcrafted payloads.
- `tests/integration/`: Ensures components cooperate correctly. Typical cases are loading `Settings` from real TOML snippets, verifying dependency wiring defined in `app/core/dependencies.py`, or calling router helpers that interact with shared services.
- `tests/component/`: End-to-end HTTP flows via the FastAPI app. Target endpoints declared in `app/routes/metadata_router_v1.py`—such as `GET /api/metadata/v1/health` or `POST /api/metadata/v1/sample`—using a client fixture to capture headers, status codes, and serialized responses.

Mirror the `app/` folder when creating test modules (e.g., `tests/unit/core/test_settings.py` for `app/core/settings.py`) so developers can quickly locate coverage gaps.

## Running Tests

Common pytest commands:

```bash
pytest                    # run the entire suite
pytest tests/unit/    # run only unit tests
pytest tests/unit/test_settings.py  # single module
pytest -v                 # verbose names and durations
pytest -k "test_settings" # pattern filter
pytest -m "slow"          # marker-based selection
```

Register custom markers under `[tool.pytest.ini_options]` in `pyproject.toml` to avoid warnings and document their intent (e.g., `slow`, `requires_db`).

## Async Testing

- `pytest-asyncio==1.3.0` is already listed in `pyproject.toml`, so async tests can be awaited seamlessly.
- Prefer explicit marks for readability:

```python
import pytest
from app.routes import metadata_router_v1

@pytest.mark.asyncio
async def test_health_handler_returns_ok():
    body = await metadata_router_v1.health_check()
    assert body == {"status": "ok"}
```

- When testing coroutine utilities (e.g., async validators or repository calls), keep the Arrange/Act/Assert flow inside the async context to avoid event-loop clashes. Newer pytest releases can auto-detect async tests, but explicit `@pytest.mark.asyncio` communicates intent.

## FastAPI Testing

Choose the correct client based on how the endpoint is implemented:

- **TestClient (`fastapi.testclient.TestClient`)**: Ideal for sync-style request handlers. Provides a `requests`-like interface and runs inside a regular test function.
- **AsyncClient (`httpx.AsyncClient`)**: Required for fully async endpoints so you can `await` `.get()`/`.post()`. Supports WebSocket testing if needed.

The project provides shared fixtures in `tests/conftest.py` that implement this Composition Root approach, bypassing `app/main.py` and instantiating FastAPI via `create_app` in `app/core/factory.py`. Tests automatically pick up `test_settings`, `test_app`, `client`, and `async_client` without explicit imports, so prefer those fixtures before creating copies in individual modules.

Mocking patterns:

- Override dependencies exposed via `get_settings` in `app/core/dependencies.py` to supply in-memory settings: `app.dependency_overrides[get_settings] = lambda: Settings(...)`.
- Use `unittest.mock` or pytest monkeypatching to intercept future MCP server calls or outbound HTTP requests so component tests remain deterministic.

Note: The shared `test_settings` fixture already passes `allow_missing_config=True`, so only override `get_settings` when you need to test specific configuration permutations.

With these fixtures in place you can assert the JSON payload of `/api/metadata/v1/health` or verify that `/api/metadata/v1/sample` returns serialized `MetadataItem` records.

### Using the Fixtures

```python
# Sync endpoint test
def test_health_endpoint(client):
    response = client.get("/api/metadata/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Async endpoint test
import pytest

@pytest.mark.asyncio
async def test_sample_endpoint(async_client):
    response = await async_client.get("/api/metadata/v1/sample")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "server"
```

## Coverage & Reporting

```bash
pytest --cov=app
pytest --cov=app --cov-report=html        # produces htmlcov/index.html
pytest --cov=app --cov-report=term-missing
```

Store shared coverage defaults in `pyproject.toml` under `[tool.coverage.run]` and `[tool.coverage.report]` (e.g., `omit = ["tests/*"]`, `fail_under = 80`). Failing the CI build when coverage dips below an agreed threshold keeps regressions visible.

## Additional Best Practices

- **Reusable fixtures**: For `Settings` tests, spin up temporary TOML files with `tmp_path` and point `Settings` to them, avoiding duplication. For metadata contracts, prebuild sample payload dictionaries reused across tests.
- **Lint before tests**: Run `uv run ruff check .` ahead of `pytest` to catch import or style regressions before they fail assertions; see `README.md` for the full lint/format workflow, and rely on `.pre-commit-config.yaml` if you prefer automated checks on every commit.
- **Parametrization**: Apply `@pytest.mark.parametrize` to cover multiple entity types in `FetchRequest` or edge cases for `MetadataItem` field validation without writing separate test functions.
- **Mirrored structure**: Keep helper modules in `tests/conftest.py` or nested `conftest.py` files that shadow the runtime package layout, making it obvious where to extend fixture logic as the service grows.

Invest in these patterns now so future MCP skills can land with tests that demonstrate expected behavior across async workflows and FastAPI interactions.
