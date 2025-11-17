You’re right that “E2E” is usually used for UI flows, but for an API-centric service, “E2E” is often just “hit the real HTTP API in something close to a production environment (docker-compose, real DB, etc.).” UI is optional; the key is that you’re exercising the full stack across a network boundary.

Here’s how I’d adapt those Playwright/hydration ideas to **FastAPI + Uvicorn + pytest** for API/E2E tests.

---

## Terminology: what’s what

For a FastAPI service, you’ll typically see:

* **Unit tests**
  Call pure Python functions, maybe override dependencies. No HTTP.

* **Integration tests**
  Use FastAPI’s `TestClient` or `httpx.AsyncClient` against the app object. May use real DB/test DB, but often still in-process (no Uvicorn, no docker).

* **API E2E tests**

    * App runs as a real process (Uvicorn or gunicorn) – often via docker-compose.
    * Tests talk to it via HTTP (e.g., `http://api:8000`) using `httpx`/`requests`.
    * Real-ish backing services (DB, cache, broker) are present.

So yes, “E2E via API only” is a thing and very common in backend-heavy systems.

---

## Core idea translated from Playwright: avoid sleeps, use explicit readiness markers

In UI tests you “wait for hydration marker, then assert”.
In API tests you “wait for readiness/health marker, then assert.”

### 1. Prefer a health/readiness endpoint over `time.sleep`

Expose something like:

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
```

Then in tests, instead of sleeping 10 seconds hoping the container is ready, poll `/healthz` until you get a 200/expected payload.

Example pytest helper:

```python
# tests/utils.py
import time
import httpx

def wait_for_service(base_url: str, timeout: float = 30.0, interval: float = 0.5) -> None:
    deadline = time.time() + timeout
    last_exc = None

    while time.time() < deadline:
        try:
            resp = httpx.get(f"{base_url}/healthz", timeout=5.0)
            if resp.status_code == 200 and resp.json().get("status") == "ok":
                return
        except Exception as exc:  # connection refused, etc.
            last_exc = exc
        time.sleep(interval)

    raise TimeoutError(f"Service at {base_url} not ready (last error: {last_exc})")
```

This is the API analogue of “web-first assertions” instead of `waitForTimeout`.

### 2. pytest fixture for “app is ready”

If your app is started by docker-compose, you usually just need the base URL and a “ready” check:

```python
# tests/conftest.py
import os
import pytest
from .utils import wait_for_service

@pytest.fixture(scope="session")
def api_base_url() -> str:
    # e.g. "http://localhost:8000" or docker-compose service host
    return os.getenv("API_BASE_URL", "http://localhost:8000")

@pytest.fixture(scope="session", autouse=True)
def wait_for_api(api_base_url: str):
    wait_for_service(api_base_url)
    yield  # tests run after this point
```

Now all tests can safely call the API without random sleeps.

---

## Example “E2E API” test with eventual consistency

Say you have an endpoint that kicks off some async work (e.g., background task) and later makes results available:

```python
# app/main.py (simplified)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

_jobs = {}

class JobRequest(BaseModel):
    payload: str

@app.post("/jobs")
def create_job(req: JobRequest):
    job_id = "some-id"  # generated in real code
    _jobs[job_id] = {"status": "pending", "result": None}
    # enqueue background work here[ELIDED]
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    return _jobs[job_id]
```

API-level E2E test that avoids `sleep` by polling with a bounded timeout:

```python
# tests/e2e/test_jobs.py
import time
import httpx

def wait_for_job_completion(base_url: str, job_id: str, timeout: float = 30.0, interval: float = 0.5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = httpx.get(f"{base_url}/jobs/{job_id}", timeout=5.0)
        resp.raise_for_status()
        body = resp.json()

        if body.get("status") == "completed":
            return body

        time.sleep(interval)

    raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")
```

```python
def test_job_flow_end_to_end(api_base_url: str):
    # Create job
    create_resp = httpx.post(
        f"{api_base_url}/jobs",
        json={"payload": "test-data"},
        timeout=5.0,
    )
    create_resp.raise_for_status()
    job_id = create_resp.json()["job_id"]

    # Wait for the asynchronous processing to finish
    job_body = wait_for_job_completion(api_base_url, job_id)

    # Assert on final result
    assert job_body["status"] == "completed"
    assert job_body["result"] == "expected-result"
```

This mirrors the “wait for hydration marker, then assert on dynamic elements” idea, but for background work / eventual consistency at the API layer.

---

## When to use TestClient vs real Uvicorn

* **Integration tests (fast, in-process):**

  ```python
  from fastapi.testclient import TestClient
  from app.main import app

  client = TestClient(app)

  def test_create_job_integration():
      resp = client.post("/jobs", json={"payload": "x"})
      assert resp.status_code == 200
  ```

  Good for most logic; no Uvicorn, no real network.

* **E2E tests (slower, but realistic):**

    * App started separately (docker-compose or a pytest fixture starting Uvicorn).
    * Tests use `httpx` against a URL.
    * Include health checks and bounded polling instead of global sleeps.

---

## Summary

* API-only E2E is valid: if your system’s primary interface is HTTP, “E2E” can just be “through the real API in a realistic environment.”
* Avoid `time.sleep()` and guessing when the app or async work is done.
* Use:

    * A **health/readiness endpoint** as your “hydration marker”.
    * **Polling helpers with timeouts** for async flows/background jobs.
    * **httpx** + pytest fixtures hitting a real Uvicorn process or docker-compose stack for true E2E.
