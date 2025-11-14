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

## Development (future steps)

1. Set `MCP_CONFIG_PATH` to point at your `mcp.toml`.
2. Run the broker via the entry script (`scripts/start-server.py`) or via `uvicorn app.main:app --reload`.
3. Use `/api/metadata/v1/health` to verify the broker is responsive.


## Prereqs

- uv: `pip install uv`
- Docker (optional, for container run)

## Build

# lock deps (optional now; becomes required once pylock.toml is committed)
uv lock

# generate OpenAPI (writes openapi/openapi.json)
uv run python tools/gen_openapi.py

# generate OpenAPI without a ready MCP config (skips config existence checks)
uv run python tools/gen_openapi.py --allow-missing-config

Using `--allow-missing-config` skips validation of `MCP_CONFIG_PATH`, letting you create a schema before committing a real `mcp.toml` file.

## Code Quality

### Linting

Run Ruff against the entire tree to catch style or static-analysis issues early:

```bash
uv run ruff check .
```

Append `--fix` to automatically apply Ruff's safe fixes:

```bash
uv run ruff check . --fix
```

### Formatting

Ruff can also format the codebase according to the configured style (line length 100, import sorting, etc.):

```bash
uv run ruff format .
```

### Combined workflow

Before committing, run the lint and format commands together (format first, lint second) so that commits stay clean. Doing so locally mirrors the automated checks described below and reduces CI churn.

### CI integration

Add `uv run ruff format .` followed by `uv run ruff check .` to your CI workflow so pull requests fail if style or lint regressions slip in. Because Ruff is already configured in `pyproject.toml`, CI inherits the same rule set developers use locally.

### Pre-commit Hooks

Install the project's pre-commit hooks to automate linting and formatting whenever you create a commit:

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
