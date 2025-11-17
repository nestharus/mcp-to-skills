**Purpose**
- Define an integration testing strategy that covers API-level, service-level, and middleware tests, including directory structure, tooling, naming conventions, performance/coverage targets, and automated migration from hard to soft-style assertions.

**Main Topics**
- Integration test categories: API-level (routes + services + DB), service-level (services + external components), and middleware-focused integration.
- Recommended directory structure: `tests/integration/api/`, `tests/integration/services/`, `tests/integration/middleware/`.
- Tooling stack: pytest, `httpx.AsyncClient`, `fastapi.testclient.TestClient`, SQLAlchemy-style test sessions, Testcontainers, and in-memory SQLite.
- File naming convention for integration tests: `*.int.test.py`.
- Performance targets (for example, <200ms per integration test) and approximate coverage targets (~70% for integration layer).
- Use of a codemod (`uv run python tools/codemod_expect_soft.py`) to migrate from hard to soft-style assertions.
- Applying AAA structure and soft-style assertions to integration tests.
- Use of nested test classes with `autouse` fixtures for shared setup (such as DB connections or app instances).
- Traversal helpers for cross-record and cross-layer checks.

**Opinions / Guidelines**
- Integration tests should validate behavior across multiple layers (routes, services, persistence, and infrastructure) rather than isolated units.
- Prefer Testcontainers or in-memory SQLite for realistic but reproducible database integration tests.
- Aim for per-test runtime around or below 200ms and integration coverage around 70%.
- Maintain strict AAA structure even in integration tests and favor soft-style assertions to surface multiple issues per run.
- Extract traversal helpers for multi-record or multi-layer validations.
- Use nested test classes with `autouse` fixtures to centralize shared integration setup.
- Use a codemod to migrate assertions to soft-style patterns, then manually review especially for async tests.
- Ensure all async operations are awaited before asserting in integration tests.

**Assumptions**
- A `tests/integration/` directory exists or will be created with the proposed substructure.
- The project will introduce or already uses a database layer compatible with SQLAlchemy-style testing patterns.
- Testcontainers or an equivalent mechanism is available for spinning up real databases when needed.
- `tools/codemod_expect_soft.py` exists or will be introduced to support assertion migration.
- Fixtures for app instances, database connections, and clients are defined in `tests/conftest.py`.
- Integration tests may reference a `tests/integration/README.md` for additional conventions.

**Staleness Indicators**
- Assumes presence of `tests/integration/api/`, `tests/integration/services/`, and `tests/integration/middleware/` subdirectories that may not yet exist.
- Proposes SQLAlchemy and Testcontainers for database testing, but the current project (for example `app/services/mcp_manager.py`) has no DB layer.
- References `tools/codemod_expect_soft.py`, which may not be implemented.
- Mentions `tests/integration/README.md` as an optional reference document that might not be present.
- Introduces performance and coverage targets that are aspirational and not currently enforced in CI.

**Tags**
- `testing`, `integration`, `pytest`, `aaa`, `soft-assertions`, `fastapi`, `httpx`, `sqlalchemy`, `testcontainers`, `performance`, `coverage`, `codemod`, `middleware`, `api-testing`.

**Preliminary Target Docs**
- Primary: a consolidated `docs/testing-guide.md` or extended `docs/TEST.md` section dedicated to integration testing strategy.
- Secondary: `docs/TESTING_ARCHITECTURE.md` for documenting directory structure, naming conventions, and how integration tests relate to unit and component tests.
- Additional: CI/testing standards documentation for performance and coverage targets.

**Red Flags**
1. Proposed integration subdirectory layout (`tests/integration/api/`, `services/`, `middleware/`) is more detailed than the current `docs/TESTING_ARCHITECTURE.md`, which only mentions a flat `tests/integration/` directory.
2. The `*.int.test.py` naming convention conflicts with the `test_*.py` pattern described in existing testing docs.
3. Testcontainers is recommended but not present in `pyproject.toml` dependencies, implying extra setup not captured elsewhere.
4. SQLAlchemy-based assumptions do not match the current project, which lacks a database layer and ORM integration.
5. The codemod `tools/codemod_expect_soft.py` is referenced but may be missing, making automated migration aspirational.
6. Performance targets (<200ms) are not backed by any configured tooling (for example pytest-timeout or pytest-benchmark).
7. The ~70% integration coverage target may conflict with the global coverage settings in `pyproject.toml` (such as `fail_under = 80`).
8. Middleware integration testing guidance is forward-looking given that `app/main.py` currently has no custom middleware.
9. Repeats AAA and soft-style guidance from TEST_1 and TEST_2, highlighting the need for a single, unified description of these patterns.
10. Mentions fixtures for app/DB/clients generically without connecting them to actual fixtures like `test_app`, `client`, or `async_client` in `tests/conftest.py`.

**References**
- `docs/to_integrate/TEST_3.md`.
- `docs/TEST.md` (overlaps on overall test organization, fixtures, and coverage settings).
- `docs/TESTING_ARCHITECTURE.md` (overlaps on directory layout and test types).
- `docs/to_integrate/TEST_1.md` and `docs/to_integrate/TEST_2.md` (overlaps on AAA and soft-style assertions).
- `tests/conftest.py` and `tests/integration/` (fixtures and integration test locations).
- `tools/codemod_expect_soft.py` (referenced codemod for migrating assertions).
- `pyproject.toml` (coverage and dependency configuration).
- `app/services/mcp_manager.py` and `app/main.py` (current state of services and middleware, showing gaps with proposed integration strategy).
