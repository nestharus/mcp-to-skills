# docs/TEST.md Summary

## Purpose
Capture the complete testing playbook for the MCP metadata broker, spanning structure, execution commands, async considerations, FastAPI-specific tooling, and coverage expectations.

## Main Topics
- Test organization into unit, integration, and component tiers mirroring `app/` structure.
- Execution guidance using `uv run pytest`, markers, filters, and coverage options.
- Async testing norms (pytest-asyncio, explicit markers, event loop handling).
- FastAPI testing techniques (TestClient vs AsyncClient, dependency overrides, fixtures in `tests/conftest.py`).
- Coverage + reporting expectations, including `pytest-cov` usage and HTML/term outputs configured via `pyproject.toml`.
- Best practices: reusable fixtures, lint-before-test workflow, parametrization, mirrored directory structure.

## Opinions/Guidelines
- Enforce the three-tier structure: `tests/unit/` for isolated logic, `tests/integration/` for cooperating components, `tests/component/` for end-to-end HTTP paths.
- Mirror runtime modules (e.g., `app/core/settings.py` ↔ `tests/unit/core/test_settings.py`) to simplify navigation.
- Use composition-root fixtures (`test_settings`, `test_app`, `client`, `async_client`) from `tests/conftest.py` that instantiate the app via `create_app` instead of `app/main.py` bootstrapping.
- Prefer explicit `@pytest.mark.asyncio` even when auto-detection works, to keep async intent visible.
- Override `get_settings` (from `app/core/dependencies.py`) in tests to inject deterministic settings payloads.
- Run linting (`uv run ruff check .` or bundled `uv run lint`) before pytest to catch style issues early; enforce coverage thresholds defined in `pyproject.toml`.

## Assumptions
- pytest, pytest-asyncio, httpx, and pytest-cov are installed per `pyproject.toml`.
- Shared fixtures in `tests/conftest.py` bypass CLI entry points and allow `allow_missing_config=True` for TOML-free runs.
- Developers rely on `uv run pytest` as the canonical invocation.
- Custom markers live under `[tool.pytest.ini_options]` inside `pyproject.toml`.
- Ruff + pre-commit are configured (reinforced in `README.md`).

## Staleness Indicators
- References to “future MCP skills/server calls” foreshadow incoming subprocess orchestration work.
- Mocking patterns for MCP JSON-RPC interactions are still aspirational, meaning sections will require expansion once implemented.
- Lacks end-to-end coverage guidance for live MCP subprocess flows expected in Phase 2.

## Tags
`testing`, `pytest`, `async`, `fastapi`, `fixtures`, `coverage`, `unit`, `integration`, `component`, `mocking`, `best-practices`

## Preliminary Target Docs
- Likely continues as `docs/TEST.md` or consolidates with to-integrate testing guides.
- Requires sync with `docs/TESTING_ARCHITECTURE.md` (structure rationale) and README (setup/contributing) to avoid repeated guidance.

## Red Flags
1. Scope overlap with `docs/TESTING_ARCHITECTURE.md`—distinguish “how” vs “why” or merge carefully.
2. Fixture instructions duplicate details already encoded in code (`tests/conftest.py`), risking drift.
3. Component test guidance stops short of true E2E once real MCP subprocess support ships.
4. Potential conflicts with `docs/to_integrate/TEST_*.md` series that may contain divergent advice.

## References
- `docs/TEST.md`
- `tests/conftest.py`
- `app/core/factory.py`
- `app/core/dependencies.py`
- `app/contracts/metadata_contract.py`
- `app/routes/metadata_router_v1.py`
- `pyproject.toml`
- `README.md`
