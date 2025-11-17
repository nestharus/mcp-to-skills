Soft vs. Hard Assertions (pytest)
Prefer “soft-style” assertions (aggregate failures) for pytest tests in this project.

* Soft-style assertions collect all failures and report them together at the end of the test, improving triage.
* Hard assertions (single `assert` / `pytest.fail`) are allowed only when an immediate fail-fast is essential (e.g., validating a precondition before an expensive or destructive step).
* Recommended pattern for soft-style assertions: collect error messages in a list and assert once at the end.

Example — preferred soft-style pattern:

```python
def test_user_model_soft_style() -> None:
    user = get_user_from_db()

    errors: list[str] = []

    if user.name != "Jane":
        errors.append(f"expected name 'Jane', got {user.name!r}")

    if user.age <= 18:
        errors.append(f"expected age > 18, got {user.age}")

    assert not errors, ";\n".join(errors)
```

Example — allowed but use sparingly (hard fail-fast):

```python
def test_user_model_precondition() -> None:
    user = get_user_from_db()

    # Fail-fast if user is missing entirely; following checks depend on this.
    assert user is not None

    # The rest can use soft-style if multiple conditions are checked.
```

Static analysis / lint rule nuance:

* Some linters (e.g., ruff, flake8 plugins, Sonar) may expect at least one direct `assert` or `pytest` assertion per test and may not “see” your soft-style pattern if you hide everything behind helpers.
* If a false positive appears for a test that clearly uses the soft-style pattern correctly, add a targeted disable comment at the top of the file or near the test:

```python
# noqa: S101  (or the specific rule, e.g. sonar rule ID / ruff code)
```

* Use this sparingly and only when the soft-style aggregation is used correctly and intentionally.

Async Test Patterns (FastAPI + pytest + httpx/clients)
For async tests (FastAPI endpoints, async services, async DB calls), distinguish between:

1. Async operations that produce values (e.g., `await client.get([ELIDED])`, `await service.do_work()`).
2. Plain value assertions (synchronous `assert` on the result).

Good patterns:

```python
import pytest
from httpx import AsyncClient
from myapp.main import app  # FastAPI app


@pytest.mark.asyncio
async def test_healthcheck(async_client: AsyncClient) -> None:
    # Good: await the HTTP call, then assert synchronously
    response = await async_client.get("/health")
    errors: list[str] = []

    if response.status_code != 200:
        errors.append(f"expected 200, got {response.status_code}")

    data = response.json()
    if data.get("status") != "ok":
        errors.append(f"expected status 'ok', got {data.get('status')!r}")

    assert not errors, ";\n".join(errors)
```

```python
@pytest.mark.asyncio
async def test_service_async_call(service: "MyService") -> None:
    # Await the producer, not the assertion
    result = await service.compute()

    errors: list[str] = []
    if result.total <= 0:
        errors.append(f"expected positive total, got {result.total}")
    if "summary" not in result.metadata:
        errors.append("missing 'summary' in metadata")

    assert not errors, ";\n".join(errors)
```

Avoid these patterns:

```python
@pytest.mark.asyncio
async def test_bad_unawaited_call(async_client: AsyncClient) -> None:
    # ❌ Forgetting to await async operation: response is a coroutine, not a Response
    response = async_client.get("/health")  # missing await
    # assert response.status_code == 200  # will fail in confusing ways
```

```python
@pytest.mark.asyncio
async def test_hiding_coroutines(async_client: AsyncClient) -> None:
    # ❌ Passing coroutines into helpers without awaiting inside the helper
    def check_response(resp) -> list[str]:
        # resp is a coroutine here, not the actual Response
        errors: list[str] = []
        # Any attribute access will be wrong
        return errors

    response = async_client.get("/health")  # missing await
    errors = check_response(response)
    assert not errors
```

Rule of thumb:

* If the subject is an async operation (HTTP call, DB call, background task, etc.), always await it before asserting:

    * `response = await async_client.get("/path")`
    * `result = await service.compute()`
* Assertions themselves are synchronous: assert on values, not on coroutines:

    * `assert response.status_code == 200`
    * Use the soft-style error aggregation pattern when you have multiple conditions.

Common pitfalls that lead to “hanging” or flaky async tests:

* Forgetting to await async calls (e.g., `client.get([ELIDED])` without `await`).
* Spawning background tasks (`asyncio.create_task`, FastAPI background tasks, websockets) that keep running after the test ends.
* Long/never-resolving waits (`await asyncio.sleep` with large values, `await queue.get()` without a producer).
* Leaving open resources (unclosed `AsyncClient`, DB connections, server processes) when not using properly scoped fixtures.

Quick debugging tips:

* Temporarily reduce timeouts in your app or client configuration for tests (e.g., HTTP client timeout).
* Add explicit timeouts for awaits that depend on external systems or background work.
* Search for:

    * Unawaited coroutines (often visible as warnings in test output).
    * Long sleeps / waits and queues without producers.
* Use pytest’s verbose mode (`-vv`) and, if available, logging in your FastAPI app to see which request/operation was last started before the test stalled.
