## 1. Overview

This document defines the consolidated documentation information architecture for the project using the Diátaxis framework (Tutorial, How-to, Reference, Explanation) and mandates that significant technical and process decisions are captured as Architectural Decision Records (ADRs) under `docs/adr/`. It incorporates Phase 1 findings and resolutions via initial ADRs 0001–0010, covering Python version (3.14+), trunk-based development, dual virtual environments, OpenAPI regeneration, Ruff standardization, E2E testing strategies, health endpoint deferral, canonical target docs, the `devpelopment-setup.md` rename, and inventory adjustment for `test_fixtures_soft_and_e2e.py`.

## 2. Target Docs List

Below are the 12 canonical target documents, each with purpose, Diátaxis type, relationships, source docs to merge, addressed red flags, and linked ADRs.

At the time of this Phase 2 IA, the following target docs already exist in the repository: `docs/development-setup.md`, `docs/LIFECYCLE.md`, `AGENTS.md`, root `README.md`, and `docs/adr/README.md` with ADRs 0001–0010. The remaining targets (`docs/code-style-guide.md`, `docs/testing-guide.md`, `docs/architecture.md`, `docs/api.md`, `docs/workflow-and-ci.md`, `docs/releases-and-versioning.md`, `docs/README.md`) are planned consolidation outputs to be created in later phases.

### 2.1 docs/README.md (Tutorial)

- **Purpose**: Central documentation hub providing a quick project overview, links to all major guides, and a short "getting started" path for new contributors.
- **Diátaxis Type**: Tutorial.
- **Relationships**: Links to all other docs under `docs/`, especially `development-setup.md`, `testing-guide.md`, `workflow-and-ci.md`, and `docs/adr/README.md` for decisions.
- **Source Docs**: `README.md`, `docs/to_integrate/README.md` (structure/navigation ideas), relevant parts of `command-reference` and `development-workflow` that describe entry points.
- **Addressed Red Flags**: Reduces duplicated onboarding content between `README.md`, `docs/to_integrate/README.md`, and scattered quick-start notes; clarifies where new users should start.
- **Linked ADRs**: References ADRs 0001–0010 indirectly via links to `docs/adr/README.md`.

### 2.2 docs/code-style-guide.md (Reference)

- **Purpose**: Single source of truth for code style and tooling, consolidating all STYLE_* guidance into a coherent, enforceable standard for Python 3.14+.
- **Diátaxis Type**: Reference.
- **Relationships**: Cross-links to `testing-guide.md` for test naming and structure, and to `workflow-and-ci.md` for linting and pre-commit hooks.
- **Source Docs**: `docs/to_integrate/STYLE_1.md`–`STYLE_8.md`, relevant portions of `fastapi-best-practices`, `linting-guide`, and any style notes from `README.md`/`AGENTS.md` that apply to code.
- **Addressed Red Flags**: Resolves STYLE document duplication and conflicts on Python version, type-hint expectations, and linting/formatting tools; sets a single line length (e.g., 120) and standardizes on Ruff.
- **Linked ADRs**: ADR 0001 (Python 3.14+), ADR 0005 (Ruff standardization).

### 2.3 docs/testing-guide.md (How-to)

- **Purpose**: Unified guide to all testing practices (unit, integration, component, E2E), including structure, fixtures, mocking, async patterns, and E2E strategies.
- **Diátaxis Type**: How-to.
- **Relationships**: Links to `code-style-guide.md` for naming and layout conventions, `development-setup.md` for local testing setup, and `workflow-and-ci.md` for how tests run in CI.
- **Source Docs**: `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`, `docs/to_integrate/TEST_1.md`–`TEST_9.md`, `docs/to_integrate/e2e-testing-guide.md`, `docs/to_integrate/e2e_dependencies.md`, and `docs/to_integrate/test_fixtures_soft_and_e2e.py` (as a code example, not a doc).
- **Addressed Red Flags**: Eliminates duplication and conflicts among multiple TEST_* files, clarifies unit vs. integration vs. E2E boundaries, fills gaps around E2E dependencies and isolation, and codifies fixture usage and soft assertions.
- **Linked ADRs**: ADR 0006 (E2E testing strategies with Testcontainers), ADR 0010 (inventory adjustment and fixture example).

### 2.4 docs/architecture.md (Explanation)

- **Purpose**: Explain the system’s overall architecture, including layers (routers/services/repositories), dependency injection, and the rationale behind core design decisions.
- **Diátaxis Type**: Explanation.
- **Relationships**: Links to `api.md` for concrete endpoint patterns, to `LIFECYCLE.md` for runtime behavior, and to relevant ADRs that shaped the architecture.
- **Source Docs**: `docs/to_integrate/architecture-overview.md`, architectural sections of `STYLE_6`, `fastapi-best-practices`, and supporting material from `LIFECYCLE.md`.
- **Addressed Red Flags**: Collapses scattered architecture narratives, removes conflicting guidance on layering and module boundaries, and makes the design rationale explicit.
- **Linked ADRs**: Links to ADR 0008 (canonical target docs) and any future architecture-specific ADRs.

### 2.5 docs/api.md (Reference)

- **Purpose**: Reference guide for API patterns and contracts, covering route structure, request/response models, error handling, versioning, and health endpoints.
- **Diátaxis Type**: Reference.
- **Relationships**: Cross-links to `architecture.md` for context, `LIFECYCLE.md` for health and lifecycle behavior, `testing-guide.md` for API testing, and `docs/adr/README.md` for API-related decisions.
- **Source Docs**: `docs/LIFECYCLE.md` (API and health-related sections), `docs/to_integrate/api-patterns-guide.md`, API-specific parts of `STYLE_3`, `STYLE_5`, `STYLE_6`, and `fastapi-best-practices`.
- **Addressed Red Flags**: Aligns API patterns, resolves conflicting recommendations on error responses and versioning, and clarifies that `/health` is interim while `/livez`, `/readyz`, `/startupz` are deferred.
- **Linked ADRs**: ADR 0004 (OpenAPI regeneration strategy), ADR 0007 (deferral of detailed health endpoint contracts).

### 2.6 docs/workflow-and-ci.md (How-to)

- **Purpose**: Describe the day-to-day development workflow and CI pipeline, including branching, pre-commit, and automated checks.
- **Diátaxis Type**: How-to.
- **Relationships**: Links to `development-setup.md` for environment preparation, `code-style-guide.md` for linting rules, `releases-and-versioning.md` for release flow, and `docs/adr/README.md` for process decisions.
- **Source Docs**: `docs/to_integrate/development-workflow.md`, `docs/to_integrate/git-workflow.md`, `docs/to_integrate/linting-guide.md`, and portions of `command-reference` related to CI and local checks.
- **Addressed Red Flags**: Resolves conflicting workflow descriptions (GitHub Flow vs. TBD), clarifies which branches are valid, and consolidates lint/test command guidance.
- **Linked ADRs**: ADR 0002 (trunk-based development), ADR 0005 (Ruff in pre-commit), ADR 0004 (OpenAPI regeneration responsibility).

### 2.7 docs/releases-and-versioning.md (How-to)

- **Purpose**: Define release and versioning strategy, including how changesets, tags, and changelogs are managed.
- **Diátaxis Type**: How-to.
- **Relationships**: Links to `workflow-and-ci.md` for integration with CI and branching, and to `docs/adr/README.md` for any future release/versioning decisions.
- **Source Docs**: `docs/to_integrate/changesets-guide.md`, relevant release notes from `development-workflow` and any existing release-related docs.
- **Addressed Red Flags**: Clarifies how releases work in a trunk-based model, removes ambiguity about branch-based release flows, and standardizes on a versioning scheme (e.g., SemVer).
- **Linked ADRs**: ADR 0002 (trunk-based development), plus any future release/versioning ADRs.

### 2.8 docs/development-setup.md (Tutorial)

- **Purpose**: Onboarding guide for setting up the development environment, with emphasis on dual virtual environments and tooling.
- **Diátaxis Type**: Tutorial.
- **Relationships**: Linked from root `README.md` and `docs/README.md` as the primary setup guide; references `workflow-and-ci.md` and `testing-guide.md` for what to do after setup.
- **Source Docs**: `docs/to_integrate/devpelopment-setup.md` (renamed), relevant parts of `command-reference`, and any setup notes embedded in other docs.
- **Addressed Red Flags**: Fixes the filename typo, consolidates scattered environment setup instructions, and removes conflicting Python version guidance.
- **Linked ADRs**: ADR 0003 (dual virtual environments), ADR 0009 (rename), ADR 0006 (Docker/Testcontainers requirements for E2E).

### 2.9 docs/adr/README.md (Reference)

- **Purpose**: Index and entry point for all ADRs, explaining the format and how to add new decisions.
- **Diátaxis Type**: Reference.
- **Relationships**: Linked from `docs/README.md`, root `README.md`, and the "Decisions" sections of major guides.
- **Source Docs**: Newly created; informed by Phase 1 decision summaries in `working/phase1/` artifacts.
- **Addressed Red Flags**: Ensures decisions are discoverable and not buried in ad-hoc docs or comments; clarifies the source of truth for contentious topics.
- **Linked ADRs**: Explicitly lists ADR 0001–0010 and will grow as new ADRs are added.

### 2.10 AGENTS.md (Reference)

- **Purpose**: Provide AI agents and automation tools with clear, up-to-date guidance on how to interact with the repo (tooling, dual venvs, testing expectations, OpenAPI regeneration).
- **Diátaxis Type**: Reference.
- **Relationships**: Complementary to `development-setup.md` and `workflow-and-ci.md`, and cross-references ADRs relevant to automation.
- **Source Docs**: Existing `AGENTS.md` plus insights from Phase 1 about agent workflows and pitfalls.
- **Addressed Red Flags**: Clarifies expectations for AI-managed tasks (tests, lint, OpenAPI), and avoids inconsistent instructions about Python versions or tooling.
- **Linked ADRs**: ADR 0003 (dual venvs), ADR 0004 (OpenAPI regeneration), ADR 0005 (Ruff), ADR 0009 (development-setup rename).

### 2.11 README.md (Tutorial)

- **Purpose**: Root-level onboarding for users and contributors, focusing on what the project does, how to try it quickly, and where to find deeper docs.
- **Diátaxis Type**: Tutorial.
- **Relationships**: Links prominently to `docs/README.md`, `development-setup.md`, and `docs/adr/README.md`.
- **Source Docs**: Existing `README.md`, trimmed and aligned with the new IA.
- **Addressed Red Flags**: Removes duplicated or stale content that conflicts with canonical docs, and resolves navigation confusion.
- **Linked ADRs**: Indirectly references ADRs via links to the ADR index.

### 2.12 docs/LIFECYCLE.md (Explanation)

- **Purpose**: Explain application lifecycle concerns such as startup, shutdown, configuration loading, and health checks.
- **Diátaxis Type**: Explanation.
- **Relationships**: Linked from `architecture.md` and `api.md` for runtime behavior, and from operations-focused onboarding if added later.
- **Source Docs**: Existing `docs/LIFECYCLE.md`, adjusted to align with deferred health endpoint contracts.
- **Addressed Red Flags**: Clarifies which lifecycle/health behaviors are current vs. planned, avoiding premature or conflicting specifications.
- **Linked ADRs**: ADR 0007 (deferral of /livez, /readyz, /startupz contracts).

## 3. Style Taxonomy

The documentation distinguishes three main style categories to reduce confusion and duplication:

- **Code Style** (`docs/code-style-guide.md`): Covers PEP 8 alignment and intentional deviations (e.g., 120-character line length), type hints for Python 3.14+ (per ADR 0001), naming conventions, imports, docstrings, comments, error handling patterns, and Ruff configuration and usage (per ADR 0005).
- **Architecture** (`docs/architecture.md`, `docs/api.md`): Describes the FastAPI-based layered architecture, SOLID and clean architecture principles, dependency injection practices, and API design patterns, including current and deferred health endpoint behaviors (per ADR 0007).
- **Workflow** (`docs/workflow-and-ci.md`, `docs/releases-and-versioning.md`): Defines Git practices (trunk-based development per ADR 0002), commit conventions, pre-commit and CI usage (per ADR 0005), release/versioning strategy, and changeset usage aligned with a trunk-centric model.

## 4. ADR Mandate

All significant technical, architectural, and workflow decisions MUST be captured as ADRs under `docs/adr/` using a lightweight Nygard-style format (Context, Decision, Consequences, References). The initial set of ADRs (0001–0010) codifies Phase 1 resolutions for Python version, branching strategy, dual environments, OpenAPI regeneration, Ruff tooling, E2E strategies, health endpoints, canonical target docs, the development setup rename, and the documentation inventory adjustment. Each major guide includes a "Decisions" section linking to relevant ADRs to make the rationale discoverable and to avoid re-encoding decisions in prose.

## 5. Non-Doc Files to Touch

The following non-documentation files are in scope for future phases to align the codebase with the IA and ADRs:

- `pyproject.toml`: Set `requires-python = ">=3.14"` (ADR 0001), configure `[tool.ruff]` for linting/formatting (ADR 0005), and ensure pytest/coverage settings support the testing strategy (ADR 0006).
- `.pre-commit-config.yaml`: Add or update Ruff hooks for `ruff check` and `ruff format` (ADR 0005).
- `tests/conftest.py`: Introduce or refine fixtures and helpers to support Testcontainers-based E2E tests and soft assertions (ADR 0006, ADR 0010).
- `.github/workflows/*`: Ensure CI uses Python 3.14+, runs Ruff and pytest consistently (ADR 0001, ADR 0005), and includes an OpenAPI drift check strategy consistent with AI-managed regeneration (ADR 0004).
- `scripts/gen_openapi.py`: Clarify AI-triggered regeneration workflow and ensure it writes to `openapi/openapi.json` (ADR 0004).
- `app/core/settings.py`: Align configuration with dual-environment assumptions where relevant (ADR 0003).
- `app/core/dependencies.py`: Maintain dependency injection patterns that match the documented architecture.
- `app/core/errors.py` (NEW): Potential central module for error types and handling conventions referenced by `api.md` and `code-style-guide.md`.
- `docs/to_integrate/` (eventual cleanup): Remove once content is fully migrated into target docs.
- `openapi/openapi.json`: Treat as the canonical API spec regenerated when API contracts change (ADR 0004).

## 6. Coverage Verification

This IA accounts for all 35 Phase 1 sources (34 markdown files plus 1 Python example file):

- STYLE documents (`docs/to_integrate/STYLE_1.md`–`STYLE_8.md`) → consolidated into `docs/code-style-guide.md`.
- Testing documents (`docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`, `docs/to_integrate/TEST_1.md`–`TEST_9.md`, `docs/to_integrate/e2e-testing-guide.md`, `docs/to_integrate/e2e_dependencies.md`) → consolidated into `docs/testing-guide.md`.
- Architecture/API documents (`docs/LIFECYCLE.md`, `docs/to_integrate/api-patterns-guide.md`, `docs/to_integrate/architecture-overview.md`, `docs/to_integrate/fastapi-best-practices.md`, relevant STYLE_* sections) → distributed across `docs/architecture.md` and `docs/api.md`.
- Workflow/versioning/linting docs (`docs/to_integrate/development-workflow.md`, `docs/to_integrate/git-workflow.md`, `docs/to_integrate/changesets-guide.md`, `docs/to_integrate/linting-guide.md`, `docs/to_integrate/command-reference.md`) → consolidated into `docs/workflow-and-ci.md`, `docs/releases-and-versioning.md`, and `docs/development-setup.md`.
- Setup docs (`docs/to_integrate/devpelopment-setup.md`) → renamed and elevated to `docs/development-setup.md`.
- Repo-level docs (`README.md`, `AGENTS.md`, `docs/to_integrate/README.md`) → root `README.md`, `docs/README.md`, and `AGENTS.md` with clear separation of concerns.
- Example code (`docs/to_integrate/test_fixtures_soft_and_e2e.py`) → referenced as a code example from `docs/testing-guide.md` and excluded from the doc inventory per ADR 0010.

## 7. Red Flag Mapping

The consolidation above addresses the major red flag categories identified in Phase 1:

- **Duplicates**: STYLE_* and TEST_* families are merged into single canonical guides, eliminating repeated, slightly divergent guidance across multiple files.
- **Conflicts**: Python version, linting/formatting tools, branching strategies, and testing strategies are aligned with ADR-backed decisions (0001–0006), resolving contradictory statements.
- **Gaps**: E2E testing strategies, dependencies, and health endpoint contracts are explicitly documented or intentionally deferred with ADRs (0006, 0007), turning implicit assumptions into explicit decisions.
- **Naming/Navigation**: The `devpelopment-setup.md` typo is corrected via `docs/development-setup.md` (ADR 0009), and all target docs are organized under a clear IA with Diátaxis tags, improving discoverability.

## 8. Diátaxis Summary Table

| Target Doc                     | Diátaxis Type | Primary Audience    | Purpose                                      | Linked ADRs          |
|--------------------------------|---------------|---------------------|----------------------------------------------|----------------------|
| docs/README.md                 | Tutorial      | New contributors    | Documentation hub and navigation             | 0001–0010 (via index) |
| docs/code-style-guide.md       | Reference     | Developers          | Code standards and tooling                   | 0001, 0005           |
| docs/testing-guide.md          | How-to        | Developers          | Testing practices and strategies             | 0006, 0010           |
| docs/architecture.md           | Explanation   | Architects          | System design and rationale                  | 0008 (+ future)      |
| docs/api.md                    | Reference     | API developers      | API contracts and patterns                   | 0004, 0007           |
| docs/workflow-and-ci.md        | How-to        | Developers          | Daily workflow and CI                        | 0002, 0004, 0005     |
| docs/releases-and-versioning.md| How-to        | Maintainers         | Release and versioning strategy              | 0002 (+ future)      |
| docs/development-setup.md      | Tutorial      | New contributors    | Development environment setup                | 0003, 0006, 0009     |
| docs/adr/README.md             | Reference     | All                 | Decision index and ADR process               | 0001–0010            |
| AGENTS.md                      | Reference     | AI agents           | Agent-specific repository guidance           | 0003, 0004, 0005, 0009 |
| README.md                      | Tutorial      | Users & contributors| Project overview and quick start             | (via ADR index)      |
| docs/LIFECYCLE.md              | Explanation   | Operators           | Application lifecycle and health behavior    | 0007                 |

## 9. Implementation Notes

Implementation is expected to proceed in later phases roughly as follows:

- **Phase 3**: Implement `docs/code-style-guide.md`, `docs/architecture.md`, and `docs/api.md`; update `pyproject.toml` to reflect ADRs 0001 and 0005.
- **Phase 4**: Implement `docs/testing-guide.md`; update `tests/conftest.py` and related fixtures/helpers per ADR 0006 and ADR 0010.
- **Phase 5**: Implement `docs/workflow-and-ci.md` and `docs/releases-and-versioning.md`; align CI workflows and pre-commit hooks with ADRs 0002, 0004, and 0005.
- **Phase 6**: Hygiene and navigation: ensure all references use `docs/development-setup.md` (the rename from `devpelopment-setup.md` has already been applied in Phase 2), create `docs/README.md`, and adjust inventories per ADR 0009 and ADR 0010.
- **Phase 7**: QA and consistency checks: ensure cross-references are correct, OpenAPI is regenerated where needed (ADR 0004), and redundant `docs/to_integrate/*` content is removed once migrated.
