## Overview

This document assigns the 12 target docs from `working/phase2/docs_ia.md` to one of three themed implementation phases: **Code Standards & Architecture**, **Testing & E2E**, and **Workflow, Releases, CI**. The goal is to provide a single, authoritative mapping so that Phase 2 and later workstreams have a clear owner for each target doc.

To satisfy the constraint that each theme owns between 3 and 6 targets, we use a **4-3-5 distribution**:

- Code Standards & Architecture: 4 targets
- Testing & E2E: 3 targets
- Workflow, Releases, CI: 5 targets

This distribution reflects the natural content groupings identified in `working/phase2/docs_ia.md` and `working/phase2/migration_plan.md`. Testing material is intentionally consolidated into a single comprehensive `docs/testing-guide.md`, while architecture- and workflow-related content naturally spread across multiple docs. To keep the themes balanced without breaking the information architecture, `docs/development-setup.md` and `docs/adr/README.md` are assigned to the **Testing & E2E** theme based on their strong ties to E2E infrastructure and testing decisions (including ADR-0006), even though they are also referenced in other phases.

Source-to-target mappings and Diátaxis types used to justify these assignments come from:

- `working/phase2/docs_ia.md`
- `working/phase2/migration_plan.md`
- `working/phase1/docs_inventory.md`

## Phase Theme Assignments Table

| Target Doc                | Theme/Phase                 | Rationale |
| ------------------------- | --------------------------- | --------- |
| `docs/code-style-guide.md` | Code Standards & Architecture | Consolidates STYLE_1–8 guidance on Python 3.14+ style, typing, Ruff-based linting, and code quality standards, aligning with ADR-0001 and ADR-0005 decisions on language level and tooling. |
| `docs/architecture.md`    | Code Standards & Architecture | Explains system architecture, layering, dependency injection, and design rationale derived from `architecture-overview` and STYLE_6, providing a single architectural narrative. |
| `docs/api.md`             | Code Standards & Architecture | Defines API patterns, contracts, error handling, and versioning based on `api-patterns-guide`, `fastapi-best-practices`, and lifecycle notes, capturing API-level architectural conventions. |
| `docs/LIFECYCLE.md`       | Code Standards & Architecture | Documents application lifecycle, startup/shutdown behavior, configuration loading, and health checks, capturing runtime architecture per ADR-0007 and related lifecycle decisions. |
| `docs/testing-guide.md`   | Testing & E2E               | Unifies all testing practices (unit, integration, component, and E2E) from TEST.md, TESTING_ARCHITECTURE, TEST_1–9, and E2E guides, implementing ADR-0006 testing strategies in a single comprehensive guide. |
| `docs/development-setup.md` | Testing & E2E             | Describes local development environment, including Docker/Testcontainers-based E2E dependencies and dual-venv setup (ADR-0003), which are critical for running the testing stack consistently. |
| `docs/adr/README.md`      | Testing & E2E               | Indexes ADRs, including testing-focused ADRs such as ADR-0006 (E2E strategy) and ADR-0010 (fixtures and test infrastructure), making testing decisions discoverable and traceable. |
| `docs/workflow-and-ci.md` | Workflow, Releases, CI      | Consolidates daily development workflow, trunk-based branching (ADR-0002), pre-commit hooks, linting (ADR-0005), and CI behavior from `development-workflow`, `git-workflow`, and `linting-guide`. |
| `docs/releases-and-versioning.md` | Workflow, Releases, CI | Defines release and versioning strategy based on `changesets-guide`, aligned with trunk-based development and CI pipelines to ensure predictable releases. |
| `docs/README.md`          | Workflow, Releases, CI      | Serves as the documentation hub and navigation entry point, guiding contributors to workflow, testing, architecture, and release docs for day-to-day work. |
| `README.md`               | Workflow, Releases, CI      | Root project onboarding and quick-start guide; the first touchpoint for users and contributors, linking into the rest of the workflow and documentation system. |
| `AGENTS.md`               | Workflow, Releases, CI      | Defines expectations for AI agents and automation, covering repository conventions, tooling, and guardrails that shape contributor workflow and CI-integrated automation. |

## Detailed Rationale by Theme

### Code Standards & Architecture (4 targets)

This theme defines **what good code looks like** and **how the system is structured**. It owns the core technical standards and architectural narratives that other themes build on.

- `docs/code-style-guide.md` brings together the STYLE_1–8 documents listed in `working/phase1/docs_inventory.md`, resolving duplicated and sometimes conflicting guidance on Python version, typing, linting, and formatting. The target codifies the move to Python 3.14+, use of Ruff, and stricter typing, aligning with ADR-0001 and ADR-0005.
- `docs/architecture.md` replaces scattered architecture descriptions (e.g., `architecture-overview`, STYLE_6) with a coherent view of layers, boundaries, and dependency injection patterns, as outlined in `working/phase2/migration_plan.md`. This gives contributors a single place to understand the overall system design.
- `docs/api.md` captures API architecture: path structure, request/response contracts, error handling, health endpoints, and versioning rules. It is fed by `api-patterns-guide`, `fastapi-best-practices`, and related pieces in `docs/LIFECYCLE.md`, making it the authoritative reference for API-level design.
- `docs/LIFECYCLE.md` documents runtime architecture: startup and shutdown sequencing, configuration loading, health checks, and process lifecycle behavior. `working/phase2/migration_plan.md` explicitly calls out lifecycle consolidation and ADR-0007 deferrals here, so this doc naturally belongs with architecture.

### Testing & E2E (3 targets)

This theme defines **how we verify that the system works**, including test strategy, E2E infrastructure, and the decisions that govern testing.

- `docs/testing-guide.md` is the single comprehensive testing reference, consolidating TEST.md, TESTING_ARCHITECTURE, TEST_1–9, and E2E-specific guides (including `e2e-testing-guide.md` and `e2e_dependencies.md`) listed in `working/phase1/docs_inventory.md`. As described in `working/phase2/migration_plan.md`, this removes dozens of overlapping sections and encodes ADR-0006 decisions on Testcontainers, fixture usage, and mocking.
- `docs/development-setup.md` is assigned to this theme because it describes the practical prerequisites for running the test suite end-to-end: Docker and other E2E dependencies, dual-venv layout, and local tooling setup. As noted in `working/phase2/docs_ia.md` section 2.8, this guide explicitly covers Docker/Testcontainers setup for E2E testing and references ADR-0006, reinforcing its Testing & E2E ownership even though it also supports general development.
- `docs/adr/README.md` indexes all ADRs, several of which are testing-focused (e.g., ADR-0006 on E2E strategy, ADR-0010 on fixtures and test architecture). `working/phase2/docs_ia.md` section 2.9 describes this index as listing ADR-0001–0010 and being linked from other guides' “Decisions” sections, and `migration_plan.md` schedules updates to it alongside testing work so that test-related decisions remain discoverable, justifying its assignment to Testing & E2E as the primary owner.

Overall, the testing content was intentionally consolidated into a single large guide (`docs/testing-guide.md`), which naturally yields fewer target docs in this theme. Assigning `docs/development-setup.md` and `docs/adr/README.md` here balances the distribution to three targets while staying true to the testing-focused responsibilities described in the migration plan.

### Workflow, Releases, CI (5 targets)

This theme defines **how to work with the codebase day-to-day**, including development workflows, release processes, contributor onboarding, and automation/CI expectations.

- `docs/workflow-and-ci.md` consolidates `development-workflow.md`, `git-workflow.md`, `linting-guide.md`, and relevant parts of `command-reference.md` (as described in `working/phase2/migration_plan.md`) into a single guide on trunk-based development (ADR-0002), pre-commit hooks, linting with Ruff (ADR-0005), and CI behavior.
- `docs/releases-and-versioning.md` documents the release and versioning strategy, primarily sourced from `changesets-guide.md`. It explains how releases fit into trunk-based development and CI, including how changesets are used to manage version bumps and changelog generation.
- `docs/README.md` functions as the documentation hub and navigation page. `docs_ia.md` assigns it the role of helping contributors discover the right guide (architecture, testing, workflow, etc.), making it a key part of the day-to-day workflow experience.
- `README.md` at the repository root remains the primary onboarding document for new users and contributors. `migration_plan.md` includes a refresh of this file to align with the new documentation structure, and it is the natural entry point into the workflow and CI story.
- `AGENTS.md` defines expectations for AI agents and automation, including how they should interact with tooling, tests, and workflows (e.g., dual-venv handling, OpenAPI regeneration, linting, and testing). These conventions are tightly integrated with how CI and automation operate, so this doc is owned by the Workflow, Releases, CI theme.

## Alignment with Migration Plan

The assignments above align with the phased migration strategy described in `working/phase2/migration_plan.md` (especially section 5):

- **Phase 3 – Code Standards & Architecture** focuses on creating `docs/code-style-guide.md`, `docs/architecture.md`, and `docs/api.md`, and on updating `docs/LIFECYCLE.md` along with related tooling (e.g., `pyproject.toml`, pre-commit configuration). All four of these targets are owned by the Code Standards & Architecture theme.
- **Phase 4 – Testing & E2E** creates `docs/testing-guide.md`, updates `docs/development-setup.md` with E2E dependencies and dual-venv details, updates `docs/adr/README.md` with testing-related ADRs, and aligns `tests/conftest.py` and fixtures. These tasks map directly to the three Testing & E2E targets.
- **Phase 5 – Workflow, Releases, CI** creates `docs/workflow-and-ci.md`, `docs/releases-and-versioning.md`, and `docs/README.md`, and refreshes the root `README.md` and `AGENTS.md` to match the new structure and workflows. These are the five targets owned by the Workflow, Releases, CI theme.

Some targets (notably `docs/development-setup.md` and `docs/adr/README.md`) are touched by multiple phases for different concerns, but each has a single **primary theme owner** for coordination: Testing & E2E for development-setup and ADR index, Code Standards & Architecture for lifecycle, and Workflow, Releases, CI for onboarding and automation docs.

## Acceptance Criteria Verification

- **All 12 targets from `docs_ia.md` are assigned:**
  - `docs/code-style-guide.md`
  - `docs/architecture.md`
  - `docs/api.md`
  - `docs/LIFECYCLE.md`
  - `docs/testing-guide.md`
  - `docs/development-setup.md`
  - `docs/adr/README.md`
  - `docs/workflow-and-ci.md`
  - `docs/releases-and-versioning.md`
  - `docs/README.md`
  - `README.md`
  - `AGENTS.md`
- **Each target is assigned to exactly one theme:** ✓ (no overlaps).
- **Each theme owns between 3 and 6 targets:** ✓ (Code Standards & Architecture: 4; Testing & E2E: 3; Workflow, Releases, CI: 5).
- **Rationales reference inventory and migration context:** ✓ (cites `docs_ia.md`, `migration_plan.md`, `docs_inventory.md`, and key ADRs such as ADR-0001, ADR-0002, ADR-0003, ADR-0005, ADR-0006, ADR-0007, ADR-0010 where relevant).
- **Assignments align with `migration_plan.md` strategies and phases:** ✓ (explicitly mapped to Phases 3–5 and their tasks).
