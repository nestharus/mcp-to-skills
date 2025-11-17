# ADR 0006: E2E Testing Strategies with Testcontainers

## Context

End-to-end (E2E) tests need to exercise the service against real or realistic external dependencies such as PostgreSQL, Redis, and AWS-like services. Relying on shared, manually managed instances leads to flaky tests and environment coupling. Testcontainers provides an established pattern for spinning up per-test or per-suite Docker containers.

## Decision

- Use Testcontainers (and related tooling) to manage external dependencies for E2E tests.
- Prefer isolated containers per test suite or test class, with clear data seeding and teardown.
- Provide pytest fixtures and helpers in `tests/conftest.py` (and related modules) to standardize setup.
- Use E2E tests selectively in CI to balance coverage and runtime.

## Consequences

- Improves reliability and reproducibility of E2E tests.
- Requires Docker to be available in development and CI environments.
- Increases test runtime compared to pure unit tests; E2E tests should focus on critical flows.

## References

- `tests/conftest.py` and E2E test modules under `tests/`
- `docs/testing-guide.md` (E2E section)
- `docs/development-setup.md` (Docker/Testcontainers prerequisites)
