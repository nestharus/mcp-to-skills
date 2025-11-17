import subprocess
import sys
import time
from multiprocessing import Process

import httpx
import pytest
import pytest_asyncio

# --- Tier 1: Integration Test Fixtures (Fast, In-Process) ---


@pytest.fixture(scope="session")
def app():
    """
    Returns the FastAPI app instance.
    Imported here to ensure all app setup logic is complete.
    """
    from app.main import app

    return app


@pytest_asyncio.fixture(scope="function")
async def async_client(app):
    """
    Provides an HTTPX client for in-process integration testing.
    This is FAST and does not require a live server.
    """
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


# --- Tier 2: E2E Test Fixtures (Slow, Live Server) ---

# Use a different port for E2E testing
TEST_PORT = 8008
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"


def _run_server():
    """
    Helper to run the server in a separate process using the
    project's official start-server.py script.
    This ensures we test the same entrypoint as the Dockerfile.
    """
    # We use sys.executable to ensure we're using the same Python
    # interpreter that pytest is using (i.e., from the .venv)
    command = [
        sys.executable,
        "scripts/start-server.py",
        "--host",
        "127.0.0.1",
        "--port",
        str(TEST_PORT),
        "--skip-health-check",  # The fixture does its own health check
    ]

    # We run this as a subprocess
    # Note: We don't import app.main here, as the subprocess
    # handles its own environment.
    process = subprocess.Popen(command)
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()


@pytest.fixture(scope="session")
def live_server():
    """
    Starts the FastAPI server in a separate process for the entire test session.
    Waits until the server is responsive before yielding.
    """
    # Use Process to run the server in a daemon process
    server_process = Process(target=_run_server, daemon=True)
    server_process.start()

    # Wait for the server to be ready by polling the health endpoint
    ready = False
    client = httpx.Client()
    start_time = time.time()

    while not ready:
        if not server_process.is_alive():
            server_process.join()
            raise Exception("Server process failed to start. Check console for errors.")

        if time.time() - start_time > 20:  # 20-second timeout
            server_process.terminate()
            server_process.join()
            raise TimeoutError("FastAPI server (for E2E) did not start in time.")

        try:
            # This must match the health check URL in your app
            response = client.get(f"{BASE_URL}/api/metadata/v1/health")
            if response.status_code == 200:
                ready = True
            else:
                time.sleep(0.1)
        except httpx.ConnectError:
            time.sleep(0.1)

    client.close()

    # Yield the base URL so tests can use it
    yield BASE_URL

    # Teardown: Stop the server
    server_process.terminate()
    server_process.join()


@pytest_asyncio.fixture(scope="session")
async def api_client(live_server):
    """
    Provides an httpx.AsyncClient for making REAL HTTP requests
    to the live E2E server.
    """
    async with httpx.AsyncClient(base_url=live_server) as client:
        yield client
