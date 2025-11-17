## Phase 2 Research Backlog

This backlog captures research tasks identified during Phase 1 content analysis that require consulting external, authoritative sources.
Each topic is tagged with the phase/theme from `working/phase2/phase_theme_assignments.md` that will consume the outcome.

### Ruff Configuration

- **Phase**: Phase 3 – Code Standards & Architecture
- **Context**: STYLE_8 hard-codes tool versions and describes Ruff configuration at a high level, but the actual `pyproject.toml` and `.pre-commit-config.yaml` need a coherent, future-proof configuration. Related issues include:
  - "`docs/to_integrate/STYLE_8`: **Version drift**" in the Staleness and Versioning sections of `working/phase1/content_issues.md`.
  - "`docs/to_integrate/STYLE_8`: **Missing Ruff config details**" in the Gaps section.
  - STYLE_1 "Line length consistency" and "Import sorting" bullets in the Other section, which depend on concrete Ruff settings.
  - STYLE_8 environment/tooling mismatch bullets in the Env section that touch Ruff integration with `uv run lint`.
- **Research questions**:
  - Which Ruff rules and rule sets are recommended for a modern Python 3.14+ FastAPI service?
  - How should line length, import sorting, and complexity limits be configured to match project goals?
  - How should Ruff be wired into `pyproject.toml`, `.pre-commit-config.yaml`, and CI (`uv run lint`) consistently?
- **Authoritative sources**:
  - https://docs.astral.sh/ruff/
  - https://github.com/astral-sh/ruff (examples and recommended configs)
- **Deliverable**: A proposed Ruff configuration for `pyproject.toml` and pre-commit/CI, plus a short rationale suitable for `docs/code-style-guide.md`.

### Python 3.14+ Features

- **Phase**: Phase 3 – Code Standards & Architecture
- **Context**: STYLE_1 and STYLE_2 reference Python 3.14+ typing and runtime annotation features but lack concrete examples. This topic covers:
  - The STYLE_2 "Missing examples" bullet in the Gaps section about `annotationlib.get_annotations()`.
  - STYLE_1 "Python version conflict" and related bullets in the Conflicts and Versioning sections, where ADR-0001 moves the project to Python 3.14+.
  - Any remaining uncertainty around how Python 3.14+ typing features should be used in examples and style guidance.
- **Research questions**:
  - What Python 3.14+ typing and runtime annotation features are most relevant to this project (e.g., lazy annotations, PEP 649-related behavior)?
  - Are there breaking changes from earlier supported versions that should influence coding standards?
- **Authoritative sources**:
  - https://docs.python.org/3/whatsnew/
  - https://docs.python.org/3/library/typing.html
- **Deliverable**: A concise Python 3.14+ section for `docs/code-style-guide.md` with idiomatic examples and guidance.

### Testing Patterns

- **Phase**: Phase 4 – Testing & E2E
- **Context**: Testing docs reference soft assertions, async tests, fixture patterns, and mocking strategies without a single, coherent recommendation. This topic is meant to address:
  - The TEST_7 "Missing pytest-check integration" bullet in the Gaps section.
  - Testing-related STYLE_6 and STYLE_7 bullets in the Testing section that mention DI-based testing and error-handling patterns with implications for tests.
  - Overlaps between `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`, and TEST_* bullets in the Duplicates, Conflicts, and Testing sections.
- **Research questions**:
  - When should pytest-check or similar tools be preferred over plain `assert` for E2E and integration tests?
  - What are best practices for structuring async tests with `pytest-asyncio` in a FastAPI + Testcontainers context?
  - How should fixtures be scoped and named for clarity and reuse across unit, integration, and E2E layers?
- **Authoritative sources**:
  - https://docs.pytest.org/
  - https://pytest-asyncio.readthedocs.io/
  - https://github.com/okken/pytest-check
- **Deliverable**: Recommended testing patterns and examples to be integrated into `docs/testing-guide.md`.

### E2E Infrastructure

- **Phase**: Phase 4 – Testing & E2E
- **Context**: E2E documents propose using Testcontainers and Docker but do not fully specify setup, seeding, and interaction with the dual-venv environment. This topic is meant to cover:
  - E2E env bullets in the Testing section (for example, "Component test guidance stops short of true E2E once real MCP subprocess support ships").
  - E2E dependency gaps mentioned in the Gaps section and in references to `e2e-testing-guide.md` and `e2e_dependencies.md`.
  - Dual-venv and Docker/Testcontainers interactions that are hinted at in Env and Testing bullets but not fully specified.
- **Research questions**:
  - How should Testcontainers be used to manage Postgres/Redis (or similar) dependencies for FastAPI services in pytest?
  - What patterns exist for seeding and cleaning test data in such containers?
  - How can Docker/Testcontainers workflows be made to work reliably in a dual-venv (WSL + Windows) setup?
- **Authoritative sources**:
  - https://testcontainers-python.readthedocs.io/
  - https://docs.docker.com/
- **Deliverable**: E2E environment setup recommendations for `docs/testing-guide.md` and `docs/development-setup.md`.

### FastAPI Best Practices

- **Phase**: Phase 3 – Code Standards & Architecture
- **Context**: STYLE_3, api-patterns-guide, and fastapi-best-practices overlap and sometimes conflict on endpoint design, error handling, and health checks. This topic connects directly to:
  - The Conflicts section "ErrorCode mismatch" bullet for STYLE_3.
  - The Conflicts section "Domain model mismatch" and "Project structure mismatch" bullets where examples diverge from the MCP domain.
  - Testing bullets for STYLE_7 that point out missing FastAPI-specific error handling (`HTTPException`, exception handlers) and overlap with testing docs.
  - Health endpoint duplication issues mentioned in the Openapi and Health sections.
- **Research questions**:
  - What are current FastAPI best practices for error handling (including `HTTPException`, exception handlers, and error payload shape)?
  - How should health endpoints (`/livez`, `/readyz`, `/startupz`) be structured and documented?
  - What are recommended patterns for OpenAPI schema generation and validation in FastAPI projects of this size?
- **Authoritative sources**:
  - https://fastapi.tiangolo.com/
- **Deliverable**: API patterns and error-handling recommendations for `docs/api.md` and `docs/code-style-guide.md`.

### Versioning & Releases

- **Phase**: Phase 5 – Workflow, Releases, CI
- **Context**: The changesets guide assumes tooling that is not fully implemented and leaves pre-release and version drift handling underspecified. This topic is responsible for:
  - All Versioning section bullets related to STYLE_8 version drift and `changesets-guide` (tooling not implemented, pre-release handling, version drift).
  - Env section bullets about changesets commands not matching actual scripts.
  - Any Other-section notes that talk about dependency version drift mechanisms tied to context7-based lookup.
- **Research questions**:
  - What is a practical release/versioning strategy for a Python service using trunk-based development?
  - Which tools (e.g., Towncrier, Python Semantic Release) are appropriate alternatives or complements to JavaScript-oriented Changesets?
  - How should pre-release versions and build metadata be handled?
- **Authoritative sources**:
  - https://packaging.python.org/
  - https://towncrier.readthedocs.io/
  - https://python-semantic-release.readthedocs.io/
- **Deliverable**: A draft releases and versioning strategy suitable for `docs/releases-and-versioning.md`.

### CI/CD Automation

- **Phase**: Phase 5 – Workflow, Releases, CI
- **Context**: Docs describe desired CI behavior (OpenAPI checks, linting, tests) but lack detailed, authoritative patterns. This topic is intended to cover:
  - Env bullets for STYLE_8 that mention CI integration specifics and adding `uv run lint` to CI.
  - Openapi section bullets around manual OpenAPI regeneration and lack of validation/drift handling.
  - Any Workflow/CI-specific examples in Other that describe incomplete or ambiguous CI expectations.
- **Research questions**:
  - How should CI be structured for Python 3.14+ projects using `uv`, including matrix testing and caching?
  - What are best practices for enforcing OpenAPI schema freshness in CI and pre-commit?
  - How should pre-commit hooks be integrated with CI so contributors and automation share the same checks?
- **Authoritative sources**:
  - https://docs.github.com/actions
  - https://pre-commit.com/
- **Deliverable**: CI and automation recommendations to inform `docs/workflow-and-ci.md` and `.github/workflows/*` updates.

### Acceptance Criteria

Research tasks are considered complete when:

- Each topic above has produced a concrete artifact (doc section draft, config snippet, or workflow recommendation) consumable by the owning phase.
- The resulting decisions are reflected in the relevant target docs and/or configuration files.
- Any open research questions that cannot be answered are explicitly documented with rationale and deferred to a later review.

## Ruff Configuration

- Maps from content_issues.md lines 61, 74, 75, and 194–199. Each bullet includes a direct quote of the source line (inserted by script when available).
  - SOURCE-L61 → [RESEARCH: Ruff Configuration]
  - SOURCE-L74 → [RESEARCH: Ruff Configuration]
  - SOURCE-L75 → [RESEARCH: Ruff Configuration]
  - SOURCE-L194…199 → [RESEARCH: Ruff Configuration]

## Python Versions (ADR-0001)

- Coverage gaps and edge-cases from content_issues.md (tagged [RESEARCH]).

## Testing Patterns

- Consolidate patterns not covered by Migration §3; ensure parity across fixtures and markers.

## OpenAPI Guidelines Updates

- Gaps requiring specific schema examples or error models.

## Environment/Tooling Harmonization

- Align pre-commit hooks, formatter/linter versions, and CI job matrices.

## Release Policy (SemVer)

- Edge-cases around pre-release tags and backwards-compatibility statements.

## Observability & Health Checks

- Non-functional requirements for readiness/liveness probes across services.

## Python Versions (ADR-0001)

- Coverage gaps and edge-cases from content_issues.md (tagged [RESEARCH]).

## Release Policy (SemVer)

- Edge-cases around pre-release tags and backwards-compatibility statements.

## Python Versions (ADR-0001)

- Coverage gaps and edge-cases from content_issues.md (tagged [RESEARCH]).

## Release Policy (SemVer)

- Edge-cases around pre-release tags and backwards-compatibility statements.
