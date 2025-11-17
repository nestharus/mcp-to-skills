# docs/LIFECYCLE.md Summary

## Purpose
Document the FastAPI application's lifecycle from configuration loading through graceful shutdown, highlighting how settings, health checks, and MCP orchestration evolve between Phase 1 stubs and future Phase 2 work.

## Main Topics
- Startup sequence: environment + TOML discovery, validation, `create_app` wiring, and lifespan startup hooks.
- Runtime behavior: health checks at `/health` and `/api/metadata/v1/health`, metadata fetch endpoint, access to `app.state.settings`.
- Shutdown sequence: signal handling, lifespan cleanup, `MCPManager.shutdown()` placeholder.
- Configuration contract: TOML layout defined by `tests/fixtures/sample_mcp.toml`, required keys (`command`, `args`, `startup_timeout_sec`), mtime caching.
- Health check usage: container probes, `scripts/start-server.py` readiness verification.
- Phase 2 preview: subprocess spawning, JSON-RPC handshake, metadata caching, glob matching, deterministic shutdown.

## Opinions/Guidelines
- Favor fail-fast validation: invalid TOML or settings raise immediately via `pydantic`.
- Cache parsed configs (path + mtime) to avoid redundant disk reads and keep startup cheap.
- Treat `create_app(settings)` (in `app/core/factory.py`) as the composition root; attach settings to `app.state.settings` for shared access.
- Ensure graceful shutdown by calling `MCPManager.shutdown()` inside lifespan teardown even while it is a no-op placeholder.
- Offer multiple health endpoints so external systems can pick generic vs API-specific probes.

## Assumptions
- `MCP_CONFIG_PATH` or `allow_missing_config=True` guides config discovery.
- Python 3.11+ stdlib (`tomllib`) parses TOML; `pydantic_settings.BaseSettings` handles env overrides.
- Uvicorn or `scripts/start-server.py` manages process lifetime and health validation.
- Phase 1 metadata responses are stubbed; Phase 2 will orchestrate real MCP subprocesses.

## Staleness Indicators
- Numerous “Phase 2” references (subprocess handling, JSON-RPC handshake, caching) require updates once implemented.
- Mentions of stubbed metadata responses will become inaccurate when real MCP orchestration lands.
- `MCPManager.shutdown()` currently described as a no-op—doc must evolve when cleanup gains behavior.

## Tags
`lifecycle`, `startup`, `shutdown`, `configuration`, `health-checks`, `fastapi`, `uvicorn`, `toml`, `settings`, `mcp-manager`

## Preliminary Target Docs
- Likely stays as `docs/LIFECYCLE.md` or merges into a future operations/deployment guide that references `docs/TEST.md` and `README.md` for cross-links.
- Should coordinate with API docs (OpenAPI + README) to avoid duplicating health check coverage.

## Red Flags
1. Heavy dependence on future Phase 2 work increases staleness risk if not promptly updated.
2. Health check guidance overlaps with README and schema docs; divergence likely without consolidation.
3. Error handling for TOML parsing or MCP initialization is only implied—no explicit remediation guidance.
4. Cache implementation details live elsewhere (`app/core/settings.py`), so readers may miss nuance without cross-reference.

## References
- `docs/LIFECYCLE.md`
- `app/core/settings.py`
- `app/core/factory.py`
- `app/services/mcp_manager.py`
- `tests/fixtures/sample_mcp.toml`
- `scripts/start-server.py`
