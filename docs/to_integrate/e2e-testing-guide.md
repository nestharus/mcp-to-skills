E2E API Testing Guide

1. Overview

This guide focuses exclusively on End-to-End (E2E) testing. For a FastAPI project, E2E testing means:

The application is running as a real, live server process using the exact same scripts/start-server.py entrypoint as the Dockerfile.

Tests act as an external client, making real HTTP requests to that server (e.g., http://127.0.0.1:8008).

This validates the full, compiled application stack—including the startup script, health checks, and networking—as a "black box."

This is distinct from Integration Testing, which runs in-process using httpx.ASGITransport and does not require a live server.

2. Key Fixtures

All E2E tests rely on fixtures defined in tests/conftest.py:

@pytest.mark.e2e: The marker you must add to all E2E tests.

live_server: A session-scoped fixture that automatically runs python scripts/start-server.py in a separate process. It then waits for the server to be ready by polling the /api/metadata/v1/health endpoint.

api_client: httpx.AsyncClient: A session-scoped client that is pre-configured to make real HTTP requests to the live_server's URL.

You do not need to start the server manually; the fixture handles it.

3. Running E2E Tests

Because E2E tests are slower and require a live server, they are marked and can be run separately.

# Run ONLY the E2E tests
uv run pytest -m e2e

# Run all tests EXCEPT E2E (e.g., for pre-commit)
uv run pytest -m "not e2e"

# Run all tests, including E2E
uv run pytest


4. Writing E2E Tests

Place E2E tests in the tests/e2e/ directory.

Assertion Style: pytest-check

All assertions should use the pytest-check library for "soft-style" assertions, allowing all failures to be reported at once.

import pytest_check as check

# Use check.equal(), check.is_in(), check.is_true(), etc.
check.equal(response.status_code, 200, "Expected 200 OK")


Example E2E Test File

Here are the correct, non-conflicting examples for E2E tests.

File: tests/e2e/test_api_endpoints.py

import pytest
import pytest_check as check
from httpx import AsyncClient

# Mark all tests in this file as 'e2e' and 'asyncio'
pytestmark = [pytest.mark.e2e, pytest.mark.asyncio]


async def test_health_check_e2e(api_client: AsyncClient):
"""
Tests the health check endpoint on the live server.
"""
# Arrange: 'api_client' comes from tests/conftest.py
url = "/api/metadata/v1/health"

    # Act: This is a REAL HTTP request
    response = await api_client.get(url)
    
    # Assert
    check.equal(response.status_code, 200, "Health check should return 200")
    # This assumes your health check returns {"status": "ok"}
    check.equal(response.json().get("status"), "ok", "Health check status should be 'ok'")


async def test_metadata_fetch_e2e(api_client: AsyncClient):
"""
Tests a successful call to the /fetch endpoint on the live server.
"""
# Arrange
request_body = {
"ids": ["item-1", "item-2"],
"include": ["core", "details"]
}

    # Act: This is a REAL HTTP request
    response = await api_client.post("/api/metadata/v1/fetch", json=request_body)
    
    # Assert
    check.equal(response.status_code, 200, "Expected 200 OK")
    data = response.json()
    check.is_in("metadata", data, "Response should have 'metadata' key")
    check.is_in("errors", data, "Response should have 'errors' key")


async def test_fetch_validation_error_e2e(api_client: AsyncClient):
"""
Tests that the live server returns a 422 for invalid input.
"""
# Arrange
invalid_body = {"include": ["core"]} # Missing 'ids'

    # Act
    response = await api_client.post("/api/metadata/v1/fetch", json=invalid_body)
    
    # Assert
    check.equal(response.status_code, 422, "Expected 422 Unprocessable Entity")
    data = response.json()
    check.is_in("detail", data, "FastAPI error details should be present")
