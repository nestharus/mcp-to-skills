# docs/TESTING_ARCHITECTURE.md Summary

## Purpose
Explain the architectural decision to house all tests under a repository-level `tests/` tree (mirroring `app/`) and justify the three-tier (unit, integration, component) strategy plus shared fixtures approach.

## Main Topics
- Decision record: tests reside at repo root (`tests/`), not inside `app/` packages.
- Rationale: separation of concerns, CI exclusion ease, alignment with packaging norms.
- Structure: dedicated `tests/unit/`, `tests/integration/`, `tests/component/` responsibilities.
- Composition-root fixtures hosted in `tests/conftest.py` using `create_app` from `app/core/factory.py`.
- Historical migration away from `app/tests/` and implications for discovery.
- Pytest configuration details (`testpaths = ["tests"]`, no `__init__.py` needed with modern pytest).

## Opinions/Guidelines
- Keep production and test code separate to avoid packaging accidental tests and to simplify tooling filters.
- Mirror runtime modules under the three folders for quick navigation (e.g., `app/services/mcp_manager.py` ↔ `tests/integration/services/test_mcp_manager.py`).
- Treat the three tiers distinctly: unit = isolated + fast, integration = cooperating components, component = HTTP-level flows through FastAPI routers.
- Build apps in fixtures via `create_app(settings)` instead of `app/main.py` CLI bootstrap to maintain deterministic contexts.
- Avoid `__init__.py` within `tests/` unless legacy tooling demands it; leave directories namespace-free for pytest auto-discovery.

## Assumptions
- Pytest ≥3.0 is available (no `__init__.py` requirement).
- `pyproject.toml` enforces `testpaths = ["tests"]` and any needed markers.
- `tests/conftest.py` exports fixtures such as `test_settings`, `test_app`, `client`, and `async_client`.
- `app/core/factory.py` exposes `create_app` for fixture wiring.
- Build tooling (e.g., Hatch) can exclude `tests/` via configuration like `tool.hatch.build.targets.wheel.exclude`.

## Staleness Indicators
- None noted; decision is historical but stable, only referencing prior `app/tests/` placement for context.

## Tags
`testing-architecture`, `adr`, `structure`, `fixtures`, `composition-root`, `pytest`, `unit`, `integration`, `component`

## Preliminary Target Docs
- Likely to remain a standalone ADR-style doc or roll into a consolidated `docs/testing-guide.md` (paired with `docs/TEST.md`).
- Should stay cross-linked from README/contributing sections when describing test layout.

## Red Flags
1. Reiterates information already present in `docs/TEST.md`; ensure boundaries between rationale vs execution remain clear.
2. Historical note about `app/tests/` could confuse newcomers who never saw that layout; consider moving to a “history” appendix.
3. Lacks guidance on exceptional cases (e.g., when an `__init__.py` might still be necessary for namespace packages).

## References
- `docs/TESTING_ARCHITECTURE.md`
- `tests/conftest.py`
- `app/core/factory.py`
- `app/main.py`
- `pyproject.toml`
