# README.md Summary

## Purpose
Serve as the primary onboarding document for the MCP Metadata Broker, covering overview, tech stack, setup, workflows, quality tooling, API references, and contributing expectations.

## Main Topics
- Project overview + status (FastAPI broker exposing MCP descriptors, early bootstrapping phase).
- Repository layout (`app/`, `scripts/`, `docs/`, `tests/`, `openapi/`).
- Technology stack: Python 3.12+, FastAPI, Uvicorn, Pydantic v2 + Settings, orjson, tomllib, uv, Hatchling.
- Setup workflow: `uv sync`, optional `uv run mcp-setup`, configuring `MCP_CONFIG_PATH`, running via `scripts/start-server.py` or `uvicorn`.
- Documentation links: lifecycle, testing, testing architecture, OpenAPI schema.
- API usage: `/api/metadata/v1/health`, `/api/metadata/v1/fetch`, `/docs`/`/redoc`, `openapi/openapi.json` regeneration via `uv run gen_openapi` (with `--allow-missing-config`).
- Development workflow: CLI-first commands, linting (`uv run lint`), formatting (`uv run ruff format .`), tests, Docker build/run instructions.
- Contributing guidance: mirror test structure, run quality gates, keep docs synced, follow pre-commit recommendations.

## Opinions/Guidelines
- Prefer `uv run ...` commands to stay agnostic to dual-venv setup (per `AGENTS.md`).
- Use `uv run mcp-setup` to opt into pre-commit hooks intentionally rather than automatically.
- Regenerate OpenAPI schema whenever API contracts change and commit the result.
- Run formatting before linting (bundled in `uv run lint`) to match CI ordering.
- Mirror runtime modules in `tests/` and follow three-tier structure (unit/integration/component) described in other docs.
- Keep docs and code synchronized during each change set.

## Assumptions
- Developers have `uv` installed locally.
- `MCP_CONFIG_PATH` points to a TOML file unless `--allow-missing-config` is provided for schema generation.
- Docker is optional but available for container workflows.
- Ruff, pytest, and other dev dependencies are managed via `pyproject.toml` and `uv sync`.
- Contributors will reference linked docs (`docs/LIFECYCLE.md`, `docs/TEST*.md`, `AGENTS.md`) for deeper details.

## Staleness Indicators
- “Development status: initialization phase” will age quickly as more features land.
- Future-phase notes (e.g., “Development (future steps)”) imply sections require updates once MCP orchestration is implemented.
- Lacks mention of Phase 2 features teased in lifecycle doc (subprocess, JSON-RPC, caching), so cross-doc sync will be necessary later.

## Tags
`readme`, `overview`, `setup`, `onboarding`, `tech-stack`, `development`, `code-quality`, `linting`, `formatting`, `pre-commit`, `docker`, `contributing`, `api-reference`

## Preliminary Target Docs
- Remains the root README; subsections may eventually spin out to `docs/development-setup.md`, `docs/linting-guide.md`, or `CONTRIBUTING.md` for depth while README keeps a curated summary.

## Red Flags
1. Setup, linting, and API-reference sections overlap with multiple `docs/to_integrate/*.md` guides—dedupe in later phases.
2. OpenAPI and health check details repeat information already kept in schema + lifecycle doc; risk of inconsistencies.
3. No explicit mention of dual-venv nuance described in `AGENTS.md`, so new contributors may miss important context.
4. “Future steps” blur current vs planned capabilities, potentially misleading readers about what exists today.

## References
- `README.md`
- `docs/LIFECYCLE.md`
- `docs/TEST.md`
- `docs/TESTING_ARCHITECTURE.md`
- `scripts/start-server.py`
- `openapi/openapi.json`
- `pyproject.toml`
- `.pre-commit-config.yaml`
- `AGENTS.md`
