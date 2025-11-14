# Testing Architecture


## Decision

All automated tests live in the repository-level `tests/` directory instead of being nested inside the runtime package. The directory mirrors the runtime modules (e.g., `app/core/settings.py` maps to `tests/unit/core/test_settings.py`).


## Rationale

- Separating `app/` (production code) from `tests/` keeps responsibilities clear and prevents accidental packaging of tests.
- CI/CD tooling can exclude the entire `tests/` tree easily—for example, `tool.hatch.build.targets.wheel.exclude = ["tests"]` in `pyproject.toml`.
- The structure matches common Python packaging practice, so onboarding contributors recognize it immediately.


## Structure

```text
tests/
├── unit/         # fast, isolated tests for individual functions/classes
├── integration/  # exercises multiple components (e.g., DI wiring, services)
└── component/    # end-to-end HTTP/API flows through FastAPI routers
```

- **Unit** tests focus on modules such as `app/core/settings.py` or `app/contracts/metadata_contract.py`.
- **Integration** tests cover wiring like `app/core/dependencies.py`, `app/services/mcp_manager.py`, and persistence adapters.
- **Component** tests drive the FastAPI stack via HTTP using fixtures described below (e.g., endpoints from `app/routes/metadata_router_v1.py`).


## Fixtures

`tests/conftest.py` hosts shared fixtures (`test_settings`, `test_app`, `client`, `async_client`). They build the application via `create_app` in `app/core/factory.py`, following a Composition Root pattern so tests bypass the CLI/bootstrap layer in `app/main.py`. This keeps suites deterministic while still exercising realistic application wiring.


## Migration Note

Early iterations placed tests under `app/tests/`. That shim has been removed in favor of the standard root-level layout described above. Historical references to the old location can be ignored.


## Pytest Configuration

`pyproject.toml` configures pytest with `testpaths = ["tests"]`, so `pytest` automatically discovers any `test_*.py` modules placed inside the structured directories. No extra flags are required to run the suite locally or in CI.

Modern pytest (3.0+) no longer requires `__init__.py` files inside test directories, so keep `tests/` (plus `unit/`, `integration/`, and `component/`) as plain directories to avoid import surprises. If legacy tooling still needs those files, leave them empty and side-effect-free so they don't interfere with discovery.
