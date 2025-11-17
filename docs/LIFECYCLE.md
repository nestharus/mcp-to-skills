# Application Lifecycle

## Overview

The MCP metadata broker boots, validates configuration, serves HTTP traffic, and then shuts down gracefully. This guide walks through the full lifecycle so operators understand how the FastAPI app manages state, subprocesses, and configuration.

## Startup Sequence

1. **Environment loading** – `app/core/settings.py` looks for `MCP_CONFIG_PATH` (or relies on defaults) using `pydantic_settings.BaseSettings` to locate the TOML configuration file.
2. **TOML parsing** – The file identified above is loaded via `tomllib`; `[mcp_servers.<name>]` sections are parsed into dictionaries of server definitions.
3. **Configuration validation** – Each server definition is validated to ensure it provides a `command` (string), `args` (list of strings), and `startup_timeout_sec` (positive float). Invalid entries raise `ValidationError` immediately so startup fails fast.
4. **Settings instantiation** – A `Settings` object caches the parsed `mcp_servers` map and exposes helper methods (including mtime-based caching so repeated loads reuse known-good config).
5. **App creation** – `create_app(settings)` in `app/core/factory.py` constructs the FastAPI application, wires routers, and immediately assigns the validated `settings` object to `app.state.settings` so dependencies can retrieve it without re-reading disk.
6. **Lifespan startup** – When the FastAPI lifespan hook fires, the app inspects `settings.mcp_servers`; only when one or more servers are configured does it instantiate `MCPManager` (from `app/services/mcp_manager.py`) and attach it to `app.state.mcp_manager` for later use.
7. **Server ready** – Uvicorn (or `scripts/start-server.py`, which wraps uvicorn) begins accepting connections with health and metadata routes mounted.

## Runtime Behavior

- **Health checks** – `/health` (root) and `/api/metadata/v1/health` return `{"status": "ok"}` indicating the process is responsive.
- **Metadata fetches** – `/api/metadata/v1/fetch` accepts a `FetchRequest` body and returns a list of `MetadataItem` objects. In Phase 1 these responses are stubbed but honor schema validation.
- **Settings access** – Dependencies pull from `app.state.settings` so routes and services operate on the same cached configuration.

## Shutdown Sequence

1. **Signal handling** – SIGTERM or SIGINT (Ctrl+C) triggers uvicorn's graceful shutdown.
2. **Lifespan cleanup** – FastAPI lifespan exit invokes `MCPManager.shutdown()` (no-op today, future work will close subprocesses and transports).
3. **Process termination** – Uvicorn stops accepting new connections and exits once outstanding requests finish.

## Configuration Details

- **TOML layout** – See `tests/fixtures/sample_mcp.toml` for canonical structure; each server lives under `[mcp_servers.<name>]`.
- **Required keys** – Every server section must define `command`, `args`, and `startup_timeout_sec`.
- **Optional behaviors** – Passing `allow_missing_config=True` (used in tests/scripts) bypasses file loading to simplify dry runs.
- **Caching** – `app/core/settings.py` caches config contents keyed by file path + mtime to avoid reparsing on every dependency injection.

## Health Checks

- **Endpoints** – `/health` (root) and `/api/metadata/v1/health` (namespaced) both return `{"status": "ok"}` so you can choose the scope appropriate for your monitor.
- **Launcher script** – `scripts/start-server.py` (see `perform_health_check`) polls the root `/health` endpoint to verify the instance is ready before handing control back to the terminal.
- **Containers** – When wiring container-level `HEALTHCHECK` instructions, target `/api/metadata/v1/health` so orchestrators can probe the API namespace directly.

## Phase 2 Preview

Phase 2 will build on this lifecycle by:

- Spawning MCP server subprocesses defined in the TOML configuration.
- Completing JSON-RPC initialization/handshake (e.g., `initialize`, `tools/list`).
- Caching metadata emitted by MCP servers for quick fetch responses.
- Supporting glob/pattern matching during `/api/metadata/v1/fetch` requests.
- Ensuring subprocesses terminate cleanly during shutdown to prevent orphaned workloads.
