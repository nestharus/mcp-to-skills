# MCP Metadata Broker

## Overview

The MCP Metadata Broker will be a FastAPI service that exposes Metadata Catalog Protocol (MCP) descriptors and routes API consumers toward the right catalog metadata without prescribing a full UI. It is being bootstrapped so the early phases capture the high-level contract, configuration, and eventual service surface before routing and orchestration layers solidify.

## Project Structure

- `app/`: primary FastAPI application code and domain models.
- `scripts/`: helper scripts (e.g., bootstrap or operational tooling) that will support future phases.
- `docs/`: reference documentation for MCP behaviors, operational notes, and process guidance.
- `tests/`: automated tests that validate the broker, its endpoints, and integrations over time.

## Technology Stack

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic v2
- Pydantic Settings
- orjson
- tomllib (Python 3.11+ standard library TOML parser)
- uv
- Hatchling

## Development Status

The project is in its initialization phase. Core artifacts such as `scripts/start-server.py` and the `/api/metadata/v1/health` endpoint are available now, letting you exercise the configured entry points even as broader MCP metadata orchestration and caching features remain under development.

## Documentation

Detailed guides live in `docs/`:

- **[Application Lifecycle](docs/LIFECYCLE.md)** – Startup, configuration loading, health checks, and graceful shutdown behavior.
- **[Testing Guide](docs/TEST.md)** – Test tiers, fixtures, async strategies, and coverage tooling.
- **[Testing Architecture](docs/TESTING_ARCHITECTURE.md)** – Design rationale behind the unit/integration/component split and fixture layering.

### API Reference

The API surface is backed by the generated OpenAPI schema:

- **Interactive Docs** – Visit `http://localhost:8000/docs` (Swagger UI) or `/redoc` once the FastAPI server is running.
- **Schema File** – `openapi/openapi.json` (regenerate via `uv run gen_openapi --config tests/fixtures/sample_mcp.toml`).
- **Endpoints Covered** – `/api/metadata/v1/fetch` (`POST` metadata queries), `/api/metadata/v1/health` (`GET` readiness), and `/sample` (example endpoint).
- **Models** – Documents `FetchRequest` and `MetadataItem` plus validation semantics enforced in `app/contracts/metadata_contract.py`.
- **Regeneration** – Run `uv run gen_openapi` (optionally with `--allow-missing-config`) whenever endpoints or models change and commit the updated JSON so docs stay synchronized.

## Project Setup

Run `uv sync` to install dependencies, then `uv run mcp-setup` to install the pre-commit hooks defined in `.pre-commit-config.yaml`. The script automatically pulls in the dev dependency group (pre-commit, pytest, etc.) if it is missing, so no extra `uv sync --group dev` step is required. This keeps Ruff formatting and lint checks aligned with CI every time you commit while remaining an explicit opt-in step.

## Development (future steps)

1. `uv sync && uv run mcp-setup`  # Install deps and pre-commit hooks.
2. Set `MCP_CONFIG_PATH` to point at your `mcp.toml`.
2. Run the broker via the entry script (`scripts/start-server.py`) or via `uvicorn app.main:app --reload`.
3. Use `/api/metadata/v1/health` to verify the broker is responsive.


## Prereqs

- uv: `pip install uv`
- Docker (optional, for container run)
- pre-commit (pulled in via dev dependencies; see the setup script above)

## Build

# lock deps (optional now; becomes required once pylock.toml is committed)
uv lock

# generate OpenAPI (writes openapi/openapi.json)
uv run gen_openapi --config tests/fixtures/sample_mcp.toml

# generate OpenAPI without a ready MCP config (skips config existence checks)
uv run gen_openapi --allow-missing-config

Using `--allow-missing-config` skips validation of `MCP_CONFIG_PATH`, letting you create a schema before committing a real `mcp.toml` file.

## Code Quality

### Linting

Run the combined Ruff workflow (formatter first, lint second) to catch style or static-analysis issues early:

```bash
uv run lint
```

### Formatting

`uv run lint` already runs `ruff format .` before the lint step, keeping imports sorted and formatting consistent across submissions. Run formatting alone when you need a quick clean-up without linting:

```bash
uv run ruff format .
```

### Combined workflow

Before committing, run `uv run lint` so formatting and linting are handled together. Doing so locally mirrors the automated checks described below and reduces CI churn.

### CI integration

Add `uv run lint` to your CI workflow so pull requests fail if style or lint regressions slip in. Because Ruff is already configured in `pyproject.toml`, CI inherits the same rule set developers use locally.

### Pre-commit Hooks

Install the project's pre-commit hooks to automate linting and formatting whenever you create a commit. Hooks auto-install via `uv run mcp-setup`; manual install remains available with:

```bash
uv run pre-commit install
```

To validate every file (useful for CI or before opening a pull request), run:

```bash
uv run pre-commit run --all-files
```

Hooks are defined in `.pre-commit-config.yaml` and use the same Ruff version configured elsewhere in the project, ensuring consistent results across developers, local automation, and CI.

## Run (local)

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Check the health endpoint:
- <http://localhost:8000/api/metadata/v1/health>

## Run (Docker)

docker build -t mcp-metadata-broker:dev .
docker run --rm -p 8000:8000 -e MCP_CONFIG_PATH=/configs/mcp.toml -v /path/to/mcp.toml:/configs/mcp.toml:ro mcp-metadata-broker:dev

## Contributing

- Place all tests under `tests/` following the three-tier structure (`unit/`, `integration/`, `component/`) documented in `docs/TESTING_ARCHITECTURE.md`. Mirror the runtime package structure within each tier (e.g., `tests/unit/core/test_settings.py` for `app/core/settings.py`). The pytest configuration in `pyproject.toml` already sets `testpaths = ["tests"]` for automatic discovery.
