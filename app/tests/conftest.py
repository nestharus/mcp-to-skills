"""Shared pytest fixtures for the MCP Metadata Broker test suite.

These fixtures implement the Composition Root pattern by bypassing the production
entry point in ``app/main.py`` and building the FastAPI application directly via
``create_app`` from ``app/core/factory.py``. This keeps tests isolated from
environment or TOML configuration requirements enforced during production
startup.
"""

# NOTE: Additional per-suite fixtures can be placed in nested ``conftest.py``
# files under app/tests/unit, app/tests/integration, etc., mirroring whatever
# hierarchy you need for specialized scenarios.

from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.core.factory import create_app
from app.core.settings import Settings


# Function scope favors isolation at the cost of fixture creation overhead.
# Swap to ``scope="session"`` only if settings/app state are proven immutable.


@pytest.fixture
def test_settings() -> Settings:
    """Return Settings with mcp_config_path=None and allow_missing_config=True for isolated tests."""

    return Settings(mcp_config_path=None, allow_missing_config=True)


@pytest.fixture
def test_app(test_settings: Settings) -> FastAPI:
    """Create a FastAPI application wired with the shared test Settings (populates app.state.settings)."""

    return create_app(test_settings)


@pytest.fixture
def client(test_app: FastAPI) -> Iterator[TestClient]:
    """Yield a synchronous TestClient (handles async routes internally) for calls like `client.get("/api/metadata/v1/health")`."""

    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
async def async_client(test_app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Yield an AsyncClient (ASGITransport) for `await async_client.get(...)` or WebSocket tests under `@pytest.mark.asyncio`."""

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        yield test_client
