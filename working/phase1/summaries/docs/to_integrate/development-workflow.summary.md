## Purpose
- Document the standard process for making, testing, and committing changes following a "Code → Test → Lint → Commit" loop, including daily development commands and pre-commit automation.

## Main Topics
- Daily development commands: running the dev server (FastAPI/uvicorn), executing tests with `uv run pytest`, and linting with `uv run lint`.
- Automated code quality: configuring and using pre-commit hooks via `.pre-commit-config.yaml`, what runs on commit, and how to handle blocked commits.
- Standard git workflow: creating feature branches, iterating on changes, running checks locally, committing, and opening PRs.
- Workflow rules: when to regenerate the OpenAPI schema and commit `openapi/openapi.json`, and when to update documentation alongside code changes.
- Testing and TDD: recommended patterns for writing tests first, mirroring `app/` structure under `tests/`, and using fixtures and markers.
- Debugging guidance: common issues (validation errors, hot reload problems, failing tests) and how to diagnose them with verbose output.

## Opinions / Guidelines
- Always run `uv run pytest` and `uv run lint` locally before committing; pre-commit hooks are not a substitute for full test runs.
- Treat pre-commit as a fast, lint-only safety net; tests are an explicit manual step before every push.
- Regenerate the OpenAPI schema with `uv run gen_openapi --config tests/fixtures/sample_mcp.toml` whenever API contracts change, and commit the updated `openapi/openapi.json`.
- Update relevant documentation in the same PR whenever workflows, commands, or public behaviors change.
- Prefer a TDD-style loop (write a failing test, then implement) for new features and bug fixes, using `tests/` structure that mirrors `app/` modules.

## Assumptions
- All commands are run via `uv` (e.g., `uv run [ELIDED]`), and contributors have uv installed and synced (`uv sync`).
- The FastAPI app runs under uvicorn with hot reload on a standard development port (commonly 8000).
- Pytest configuration in `pyproject.toml` points to `tests/` and may define markers for different test tiers.
- Ruff is the primary linting and formatting tool; other tools (black, flake8) are not part of the default workflow.
- Pre-commit is installed and configured (e.g., via an initial `uv run mcp-setup` or similar bootstrap script).
- `tests/fixtures/sample_mcp.toml` exists and is the canonical config for OpenAPI generation.

## Staleness Indicators
- References to `uv run mcp-setup` assume a bootstrap script that may not be clearly documented in `README.md` or `pyproject.toml`.
- Mentions of `tests/fixtures/sample_mcp.toml` for OpenAPI generation do not describe its contents or how to create/update it.
- The doc assumes pre-commit is already installed and enabled but may not link to installation steps for new contributors.
- References to AGENTS.md for "agent workflow" may drift if AGENTS.md evolves without corresponding updates here.
- Debugging guidance mentions Pydantic 422 validation errors without linking to Pydantic docs or providing up-to-date examples.
- No explicit guidance on running tests by marker (e.g., unit vs integration vs e2e), even if markers are defined elsewhere.

## Tags
- `workflow`, `development`, `daily-commands`, `testing`, `linting`, `pre-commit`, `git`, `tdd`, `debugging`, `fastapi`, `uvicorn`, `pytest`, `ruff`, `openapi`, `ci`, `changesets`, `versioning`

## Preliminary Target Docs
- Likely target: standalone `docs/development-workflow.md` focusing on the daily development loop and local commands.
- Cross-reference `docs/git-workflow.md` for branching, commit conventions, and PR practices.
- Cross-reference `docs/changesets-guide.md` for versioning and release workflows.
- Cross-reference `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md` for detailed testing guidance and test tier definitions.

## Red Flags
- Significant overlap with `README.md` "Code Quality" section, which already describes `uv run lint`, formatting, and pre-commit hooks.
- Overlap with `docs/to_integrate/git-workflow.md` around the "run checks before commit" step; they disagree on whether to exclude E2E tests in the default loop.
- References `uv run mcp-setup` without explaining what it does or where it is defined, even though initial setup is described in `README.md`.
- Describes pre-commit as lint-only while some sections imply broader automation; this must stay aligned with `.pre-commit-config.yaml`.
- Mandates regenerating OpenAPI on API changes but does not explain how to validate the generated schema or handle generation failures.
- Encourages TDD and mirroring `app/` in `tests/` but `docs/TESTING_ARCHITECTURE.md` may already define a more precise structure, risking conflicting advice.
- Provides debugging tips but omits common issues like dependency conflicts, environment setup, or Docker-related problems, leaving gaps for new contributors.
- Does not document how to run specific test markers (unit, integration, component, e2e), despite other docs describing these tiers.
- References AGENTS.md for agent-specific workflow without clarifying how that interacts with the general development loop.
- Requires documentation updates alongside workflow changes but does not specify which docs (README, TEST docs, workflow docs) to touch, which can lead to inconsistency.

## References
- `docs/to_integrate/development-workflow.md`
- `docs/to_integrate/git-workflow.md`
- `docs/to_integrate/changesets-guide.md`
- `README.md` (Setup and Code Quality sections)
- `AGENTS.md`
- `.pre-commit-config.yaml`
- `pyproject.toml` (pytest and tooling configuration)
- `docs/TEST.md`
- `docs/TESTING_ARCHITECTURE.md`
- `tests/fixtures/sample_mcp.toml`
- `openapi/openapi.json`
