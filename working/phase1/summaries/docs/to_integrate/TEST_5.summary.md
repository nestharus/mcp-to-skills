## Purpose
- Summarize coverage goals, reporting mechanisms, and mocking patterns from `docs/to_integrate/TEST_5.md`, including guidance on what to test vs. what not to test and how to generate machine-consumable coverage output.

## Main Topics
- Coverage tooling with coverage.py integrated with pytest (for example, `coverage run -m pytest`).
- Generating coverage reports in multiple formats (HTML, JSON) for humans and tools.
- Suggested coverage targets (for example, ≥80% for unit tests, ≥70% for integration tests, and around 80% overall).
- Guidance on which parts of the system to prioritize in testing (business logic, edge cases, APIs, validation) vs. areas generally not worth testing (third-party libraries, trivial boilerplate, framework internals).
- Mocking patterns using `unittest.mock` (mocks, `@patch`, `patch.object`) and pytest-mock for cleaner syntax.
- Time-related mocking patterns using libraries like freezegun and/or pytest monkeypatching to stabilize time-dependent behavior.

## Opinions / Guidelines
- Aim for strong but realistic coverage thresholds, focusing on meaningful coverage (critical paths, edge cases, error handling) rather than chasing 100% coverage.
- Prefer coverage.py as the primary coverage engine, with JSON output to support tooling and potential LLM integration.
- Treat unit test coverage expectations as stricter than integration test coverage, while still targeting a healthy overall project coverage percentage.
- Use `unittest.mock` as the baseline mocking library (works well with pytest), and add pytest-mock for projects that prefer its fixtures and syntax.
- Mock external dependencies and time-dependent behavior to keep tests deterministic and fast; avoid mocking internal business logic where possible.
- Avoid writing tests that merely assert behavior of well-tested third-party libraries or framework internals.

## Assumptions
- coverage.py and pytest are available and integrated into the project's test workflows.
- The project either already uses or can easily adopt JSON coverage output for downstream tools.
- The repository structure can be mapped to the examples (even if the example uses `apps/web` and `packages/*`, the same patterns can apply to `app/` and `tests/`).
- Developers are familiar with `unittest.mock` semantics and comfortable introducing pytest-mock when it adds value.
- A time-freezing library like freezegun can be added to dependencies if the recommended time-mocking patterns are adopted.

## Staleness Indicators
- Coverage examples assume a monorepo-style layout (for example, `apps/web`, `packages/shared_types`) that differs from the actual `app/` + `tests/` layout in this project.
- Coverage configuration may conflict or overlap with existing `[tool.coverage.*]` sections in `pyproject.toml` and the pytest-cov usage documented in `docs/TEST.md`.
- The document assumes freezegun and possibly pytest-mock are available, but these may not yet be declared in `pyproject.toml`.
- JSON coverage post-processing with tools like `jq` may be unnecessary if the project standardizes on `coverage combine` or pytest-cov-based workflows.
- Mocking examples are generic and may not reflect current project patterns around MCP calls, FastAPI routes, or service-layer abstractions.

## Tags
- testing, pytest, coverage, coverage-goals, json-output, mocking, unittest-mock, pytest-mock, freezegun, time-mocking, what-to-test

## Preliminary Target Docs
- Primary: `docs/TEST.md`, extending existing coverage sections with explicit thresholds, JSON output, and guidance on what to test vs. what to skip.
- Secondary: a dedicated mocking document (for example, `docs/mocking-guide.md`) or a major section within a consolidated `docs/testing-guide.md` that collects mocking patterns in one place.
- Coverage mechanics should be harmonized with existing pytest-cov/coverage configuration to avoid diverging command recommendations.

## Red Flags / Integration Risks
- Coverage targets (for example, explicit ≥80%/≥70% thresholds) may conflict with or overspecify expectations relative to the current `docs/TEST.md` language.
- The recommended `coverage run -m pytest` flow needs to be reconciled with any existing `uv run pytest --cov=...` guidance to avoid duplicate or competing workflows.
- Monorepo-oriented examples must be rewritten to fit this project's simpler structure; otherwise they risk confusing contributors.
- Introducing freezegun and pytest-mock requires updating dependencies and ensuring they align with existing mocking practices in `tests/`.
- Guidance on "what not to test" must be integrated carefully so it does not discourage useful tests for framework integrations that are important in this project (for example, FastAPI routing and dependency wiring).
- JSON coverage output and downstream processing for LLMs and tools should be clearly marked as optional/advanced to avoid overcomplicating the baseline workflow.
- Coverage-combine patterns that assume multiple `.coverage` files may not match the project's single-test-run usage and need adaptation.

## References
- `docs/to_integrate/TEST_5.md`
- `docs/TEST.md` (coverage expectations and test workflow)
- `pyproject.toml` (coverage configuration and dependencies)
- `tests/conftest.py` (fixtures relevant for mocking and isolation)
- `README.md` (testing commands and `uv` usage)
