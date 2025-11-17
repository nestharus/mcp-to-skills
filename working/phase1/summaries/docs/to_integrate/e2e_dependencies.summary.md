## Purpose
- Capture the proposed `pyproject.toml` configuration required to support the E2E testing patterns, focusing on dev dependencies (e.g., `httpx`, `pytest`, `pytest-asyncio`, `pytest-check`, `ruff`) and the `e2e` pytest marker definition.

## Main Topics
- Shows a `[dependency-groups]` dev section including `httpx`, `pytest`, `pytest-asyncio`, `pytest-check`, and `ruff` with specific version pins for reproducible test environments.
- Illustrates `tool.pytest.ini_options` configuration covering `testpaths`, naming patterns for test files/classes/functions, asyncio settings (`asyncio_mode = "auto"`, `asyncio_default_fixture_loop_scope = "function"`).
- Defines a custom `e2e` marker in `tool.pytest.ini_options.markers` with the description "marks tests as end-to-end (requires running server)".
- Positions these snippets as add-ons to an existing `pyproject.toml` rather than a full config (uses `[ELIDED] existing code [ELIDED]` placeholders).

## Opinions / Guidelines
- Advocates for explicit version pinning of core testing dependencies (`httpx==0.28.1`, `pytest==9.0.1`, `pytest-asyncio==1.3.0`, `pytest-check==2.5.0`, `ruff==0.14.5`) to keep CI and local runs consistent.
- Encourages grouping testing dependencies under a `dev` dependency group, assuming use of `uv` for environment management.
- Recommends configuring `pytest-asyncio` in `auto` mode with a function-scoped event loop to align with typical async FastAPI test patterns.
- Requires explicit registration of the `e2e` marker in `pyproject.toml` to avoid "unknown marker" warnings and to document the purpose of E2E tests.

## Assumptions
- Project uses `uv` and `dependency-groups` in `pyproject.toml` to manage dev/test dependencies.
- `pytest` is the standard test runner, and its configuration is centralized under `tool.pytest.ini_options` in `pyproject.toml`.
- Async tests are common, hence `pytest-asyncio` is installed and configured with `asyncio_mode = "auto"`.
- E2E tests require additional tooling (`pytest-check`, `httpx`) beyond what a minimal unit-test setup would need.
- The `e2e` marker will be the primary way to select/skip end-to-end tests in both CI pipelines and local workflows.

## Staleness Indicators
- The snippet adds `pytest-check==2.5.0` to `dependency-groups.dev`, but the actual `pyproject.toml` currently does not include `pytest-check` in any dependency group.
- It defines an `e2e` marker under `tool.pytest.ini_options.markers`, while the real `pyproject.toml` has `markers = []` (no markers configured).
- The file is written as an illustrative snippet with `[ELIDED] existing code [ELIDED]` placeholders, not a full configuration, which can be misleading when compared to the concrete structure of the actual `pyproject.toml`.
- Version pins shown here mostly match the real project (`pytest==9.0.1`, `pytest-asyncio==1.3.0`, `httpx==0.28.1`, `ruff==0.14.5`), but the doc does not confirm alignment and could drift as the project evolves.
- The snippet does not mention other dev dependencies present in the real `pyproject.toml` (e.g., `pre-commit`, `checkov`), so copying it verbatim would lose context.

## Tags
- testing
- e2e
- dependencies
- pytest
- pytest-check
- pytest-asyncio
- httpx
- configuration
- pyproject-toml
- markers

## Preliminary Target Docs
- Primary: Update the real `pyproject.toml` to include `pytest-check` in the appropriate `dependency-groups.dev` section and to define the `e2e` marker in `tool.pytest.ini_options.markers`.
- Secondary: Use this dependency/marker list as a reference block in a consolidated testing guide (e.g., `docs/TEST.md` or an updated E2E testing guide) to document the required packages for running E2E tests.
- Tertiary: Integrate the configuration details into `docs/to_integrate/e2e-testing-guide.md` so the guide includes both behavior and setup requirements.

## Red Flags / Gaps
- `pytest-check==2.5.0` is presented as a required dev dependency, but it is missing from the actual `pyproject.toml`, so current tests cannot use `check.*` without additional installation.
- The `e2e` pytest marker is defined in the snippet but not in the real `tool.pytest.ini_options.markers` list, so using `@pytest.mark.e2e` today would trigger pytest "unknown marker" warnings.
- The presence of `[ELIDED] existing code [ELIDED]` indicates this is a partial example; directly pasting it into `pyproject.toml` without merging would break or overwrite existing configuration.
- The snippet does not show how to integrate with other markers or pytest options that may exist in the project (e.g., markers for slow tests or environment-specific skips).
- It assumes familiarity with `uv` and `dependency-groups` syntax but provides no explanation, which may confuse contributors who only know standard `dependencies` tables.
- Potential drift between these pinned versions and the versions in the live `pyproject.toml` over time is not addressed, making this doc prone to becoming outdated.
- No mention of additional E2E-related tooling (coverage, reporting, etc.), so it's incomplete as a one-stop configuration reference.
- The configuration is tightly coupled to the E2E guide and fixture examples but does not reference them directly, increasing the risk that one will change without updating the other.

## References
- Source: `docs/to_integrate/e2e_dependencies.md`.
- Main consumer: `docs/to_integrate/e2e-testing-guide.md` (assumes these dependencies and markers exist).
- Actual configuration baseline: `pyproject.toml` (dev dependency groups and `tool.pytest.ini_options`).
- Fixture examples depending on this setup: `docs/to_integrate/test_fixtures_soft_and_e2e.py`.
- Broader testing docs: `docs/TEST.md` (overall testing guidance) and `docs/TESTING_ARCHITECTURE.md` (test layers and strategies).
