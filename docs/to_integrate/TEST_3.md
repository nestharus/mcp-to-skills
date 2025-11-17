Integration Tests
Integration tests validate behavior across multiple layers of the application: FastAPI routes, service layer, persistence/DB, background tasks, and infrastructure boundaries.

Categories:

* **API-level tests**: FastAPI route handlers + service layer + DB + dependencies.
* **Service-level integration tests**: service logic + DB or external components (e.g., cache, message queue).
* **Middleware integration tests**: custom middleware for auth, rate limiting, request shaping, ID injection, locale inference, feature flags, etc.

Directory structure (example):

```
tests/integration/api/
tests/integration/services/
tests/integration/middleware/
```

Tools:

* pytest
* httpx.AsyncClient or fastapi.testclient.TestClient
* SQLAlchemy test session / transaction rollbacks
* Testcontainers for real DBs or an in-memory SQLite DB for lightweight tests
* Fixtures for app, DB, and clients

Naming: `*.int.test.py`

Target performance: **< 200ms per test** (when using in-memory DB or Testcontainers with reuse).
Coverage target: **~70%** (lower than unit tests).

See `tests/integration/README.md` for patterns and examples if present.

Automated Migration (from hard to soft-style assertions)
A codemod may convert direct `assert` statements into “soft-style” aggregated checks by:

* Wrapping multiple individual conditions into a list of errors.
* Preserving `await` for async operations.
* Ensuring the final line asserts once on the aggregated errors.

Run across unit, integration, and E2E tests:

```
uv run python tools/codemod_expect_soft.py
```

After running, manually review async tests to ensure:

* All HTTP calls, DB calls, and async operations are awaited.
* Assertions on plain values use the soft-style pattern:

    * `value = await fn()`
    * `errors.append(...)` for each condition
    * `assert not errors, ";\n".join(errors)`
* Async functions never wrap assertions inside unawaited coroutines.

Nested blocks for initialization and related tests:

```python
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

@pytest.mark.asyncio
class TestDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_db(self):
        # Establish connection
        client = await create_db_client()
        yield client
        await client.close()

    class TestUserRepository:
        @pytest.mark.asyncio
        async def test_creates_and_fetches_user(self, setup_db):
            errors: list[str] = []

            # Arrange / Act via helpers...
            # push to errors for any violations

            assert not errors, ";\n".join(errors)
```

Test Structure (AAA)

Follow the Arrange–Act–Assert sequence strictly:

```python
import pytest
from myapp.logic import my_function

def test_my_function_returns_expected_result():
    # Arrange
    input_value = "test"
    expected = "TEST"

    # Act
    result = my_function(input_value)

    # Assert
    assert result == expected
```

For integration tests, expand the same structure:

```python
@pytest.mark.asyncio
async def test_get_user_success(async_client: "AsyncClient"):
    # Arrange
    user_id = await seed_user(async_client, name="Jane")

    # Act
    response = await async_client.get(f"/users/{user_id}")
    data = response.json()

    # Assert (soft-style)
    errors: list[str] = []

    if response.status_code != 200:
        errors.append(f"expected 200, got {response.status_code}")

    if data.get("name") != "Jane":
        errors.append(f"expected name 'Jane', got {data.get('name')!r}")

    assert not errors, ";\n".join(errors)
```

Patterns:

* Tests remain linear and readable.
* Traversals or cross-record checks should be extracted into helpers (generators or pure functions).
* Assertions stay in the test body; helpers return structures or iterables, not pass/fail results.
* Prefer parameterized integration scenarios when validating multiple cross-layer flows.

This aligns integration testing for FastAPI/pytest with the same AAA, soft-style, and traversal principles used across the test suite.
