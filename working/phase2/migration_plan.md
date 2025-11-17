## Documentation Migration Plan

### 1. Overview

This migration plan defines how all existing documentation and related guidance in the repository will be consolidated into the target information architecture described in `working/phase2/docs_ia.md`. It is the single source of truth for how Phase 3+ work will migrate, merge, and retire the 35+ Phase 1 source documents, and how code/config files will be aligned with the new ADRs and target docs. All subsequent documentation and hygiene work should reference and update this plan rather than inventing new structures.

The plan is organized into:
- A migration matrix for documentation files
- A migration matrix for non-documentation files and code/config alignment
- Red-flag resolution tracking across major themes
- A recommended migration sequence by phase/theme
- Acceptance criteria for declaring the migration complete

### 2. Migration Matrix (Documentation Files)

The following table maps each Phase 1 source document into one or more target documents from `working/phase2/docs_ia.md`. Actions are merge/split/retire; owners correspond to the three themed phases.

| Source                                     | Target Doc(s)                         | Action  | Owner (Phase/Theme)               | Priority | Notes |
|--------------------------------------------|---------------------------------------|---------|-----------------------------------|----------|-------|
| docs/to_integrate/STYLE_1.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Consolidate core Python style guidance; resolve STYLE_* duplication red flags; align with ADR-0005 (Ruff). |
| docs/to_integrate/STYLE_2.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Merge overlapping naming/import rules; resolve conflicting recommendations called out in content_issues.md. |
| docs/to_integrate/STYLE_3.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Integrate FastAPI-specific style sections; coordinate with `docs/api.md`. |
| docs/to_integrate/STYLE_4.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Normalize async patterns and dependency injection advice. |
| docs/to_integrate/STYLE_5.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Deduplicate logging and error-handling rules; cross-reference planned `app/core/errors.py`. |
| docs/to_integrate/STYLE_6.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Align type-hinting and strictness guidance with ADR-0001 (Python 3.14+). |
| docs/to_integrate/STYLE_7.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Resolve environment/tooling style conflicts (e.g., formatting, linters). |
| docs/to_integrate/STYLE_8.md              | docs/code-style-guide.md             | merge   | Code Standards & Architecture     | High     | Capture remaining cross-cutting style topics; ensure no STYLE_* content remains orphaned. |
| docs/to_integrate/TEST_1.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Consolidate unit test philosophy; resolve conflicting fixture advice from content_issues.md. |
| docs/to_integrate/TEST_2.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Merge integration testing guidance; align with ADR-0006 (E2E/Testcontainers). |
| docs/to_integrate/TEST_3.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Normalize mocking and isolation strategies; resolve duplication with TESTING_ARCHITECTURE. |
| docs/to_integrate/TEST_4.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Integrate parametrization and edge-case testing best practices. |
| docs/to_integrate/TEST_5.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Align naming and directory structure conventions for tests. |
| docs/to_integrate/TEST_6.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Merge performance and flaky-test guidance; cross-link to workflow-and-ci.
| docs/to_integrate/TEST_7.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Capture database and external-service testing patterns; reference ADR-0006. |
| docs/to_integrate/TEST_8.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Merge regression testing and bug reproduction patterns. |
| docs/to_integrate/TEST_9.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Address remaining testing red flags; ensure no TEST_* guidance remains only in to_integrate. |
| docs/TEST.md                               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Treat as current canonical testing doc; reconcile with TEST_* series and TESTING_ARCHITECTURE. |
| docs/TESTING_ARCHITECTURE.md               | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Fold architecture-level testing guidance into testing-guide; cross-link to docs/architecture.md. |
| docs/to_integrate/e2e-testing-guide.md    | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Align E2E strategy with ADR-0006; emphasize Testcontainers; resolve environment conflicts. |
| docs/to_integrate/e2e_dependencies.md     | docs/testing-guide.md                | merge   | Testing & E2E                     | High     | Integrate dependency requirements into E2E section; remove duplication with development-setup. |
| docs/to_integrate/test_fixtures_soft_and_e2e.py | docs/testing-guide.md (reference only) | retire as standalone doc | Testing & E2E | Medium | Treat as example/appendix referenced from testing-guide; ensure ADR-0010 inventory expectations are met. |
| docs/to_integrate/test_fixtures_soft_and_e2e.md | docs/testing-guide.md (reference only) | retire | Testing & E2E | Medium | Markdown placeholder without backing file; superseded by docs/to_integrate/test_fixtures_soft_and_e2e.py per ADR-0010. |
| docs/LIFECYCLE.md                          | docs/LIFECYCLE.md; docs/architecture.md; docs/api.md | split/refocus | Code Standards & Architecture     | High     | Keep lifecycle explanation canonical in docs/LIFECYCLE.md (cleaned up, aligned with ADR-0007), and split architecture rationale and API contract details into docs/architecture.md and docs/api.md per docs_ia. |
| docs/to_integrate/architecture-overview.md| docs/architecture.md                 | merge   | Code Standards & Architecture     | High     | Make architecture.md the canonical explanation; resolve overlaps with LIFECYCLE and README. |
| docs/to_integrate/api-patterns-guide.md   | docs/api.md; docs/code-style-guide.md| merge   | Code Standards & Architecture     | High     | Capture endpoint design patterns; share style-related API patterns with code-style-guide. |
| docs/to_integrate/fastapi-best-practices.md | docs/api.md; docs/code-style-guide.md | merge | Code Standards & Architecture     | High     | Integrate FastAPI usage best practices; deduplicate overlapping sections with STYLE_* and api-patterns-guide. |
| docs/to_integrate/development-workflow.md | docs/workflow-and-ci.md              | merge   | Workflow, Releases, CI            | High     | Define day-to-day developer workflow; align with ADR-0002 (trunk-based) and dual-venv ADR-0003. |
| docs/to_integrate/git-workflow.md         | docs/workflow-and-ci.md              | merge   | Workflow, Releases, CI            | High     | Consolidate branch/PR policies into trunk-based development narrative. |
| docs/to_integrate/linting-guide.md        | docs/workflow-and-ci.md; docs/code-style-guide.md | merge | Workflow, Releases, CI | High | Move conceptual linting rules into code-style-guide; keep command/CI usage in workflow-and-ci; reflect ADR-0005 (Ruff). |
| docs/to_integrate/command-reference.md    | docs/workflow-and-ci.md; docs/README.md | merge | Workflow, Releases, CI | High | Provide authoritative command reference; link key commands from root README tutorial. |
| docs/to_integrate/changesets-guide.md     | docs/releases-and-versioning.md      | merge   | Workflow, Releases, CI            | High     | Establish releases-and-versioning as canonical changesets/release process doc. |
| docs/to_integrate/devpelopment-setup.md   | docs/development-setup.md            | merge/rename | Workflow, Releases, CI    | High     | Represents the original typo’d file; will be renamed then superseded by docs/development-setup.md per ADR-0009. |
| docs/development-setup.md                 | docs/development-setup.md            | keep/refresh | Workflow, Releases, CI     | High     | Ensure rename from devpelopment-setup is complete; align with dual-venv ADR-0003 and Python 3.14+ ADR-0001. |
| docs/to_integrate/README.md               | docs/README.md                       | merge   | All themes                        | Medium   | Incorporate navigation and doc structure ideas; ensure consistency with docs_ia target roles. |
| README.md                                  | README.md; docs/README.md            | merge/refresh | All themes                    | High     | Keep root README as project tutorial; remove stale testing/style guidance moved into dedicated docs. |
| AGENTS.md                                  | AGENTS.md                            | refresh | All themes                        | High     | Ensure AGENTS reflects ADR-0001–00010 and new doc structure; remove outdated workflow instructions. |

### 3. Migration Matrix (Non-Documentation Files)

The following table tracks code and configuration changes needed to align the repository with ADRs and the new documentation structure. These changes should be coordinated with the doc migrations above.

| File / Area                    | Planned Change Summary                                                                 | Owner (Phase/Theme)               | Priority | Notes |
|--------------------------------|----------------------------------------------------------------------------------------|-----------------------------------|----------|-------|
| pyproject.toml                 | Set `requires-python` to 3.14+; standardize Ruff configuration; ensure pytest markers/paths match testing-guide. | Code Standards & Architecture     | High     | Implements ADR-0001 and ADR-0005; resolves versioning/test-path red flags. |
| .pre-commit-config.yaml        | Add/standardize Ruff hooks; align formatting/linting tools with ADR-0005.             | Code Standards & Architecture     | High     | Remove conflicting lint tools; keep config in sync with pyproject. |
| tests/conftest.py              | Add shared fixtures for E2E/Testcontainers; unify fixture patterns with testing-guide. | Testing & E2E                     | High     | Implements ADR-0006; resolves fixture duplication red flags from content_issues.md. |
| .github/workflows/*            | Update CI matrix to Python 3.14+; ensure Ruff, tests, and OpenAPI checks run consistently. | Workflow, Releases, CI            | High     | Implements ADR-0001, ADR-0004, ADR-0005; align with workflow-and-ci. |
| scripts/gen_openapi.py         | Clarify and enforce AI-triggered OpenAPI regeneration workflow; centralize config usage. | Code Standards & Architecture     | Medium   | Implements ADR-0004; reduces manual regeneration red flags. |
| app/core/settings.py           | Ensure settings align with dual-venv strategy and Python version; document key env assumptions. | Code Standards & Architecture | Low      | Implements ADR-0003; resolves environment confusion red flags. |
| app/core/dependencies.py       | Keep DI helpers consistent with api patterns and architecture docs.                    | Code Standards & Architecture     | Low      | Coordinate with docs/api.md and docs/architecture.md guidance. |
| app/core/errors.py (new)       | Introduce centralized error types and mapping to HTTP responses.                      | Code Standards & Architecture     | Medium   | Supports consistent error-handling guidance in code-style-guide and api docs. |
| openapi/openapi.json           | Treat as generated artifact to be updated via scripts/gen_openapi.py on API changes.  | Code Standards & Architecture     | High     | Implements ADR-0004; ensure CI enforces freshness. |

### 4. Red Flag Resolution Tracking

For each major content group, the following representative red flags from `working/phase1/content_issues.md` will be addressed as part of this migration. Concrete edits in later phases should link back to the exact issue identifiers/line numbers when work is executed.

- **STYLE group → docs/code-style-guide.md**
  - Example issues (by approximate reference):
    - `STYLE-IMPORTS` (around lines ~40–70): conflicting advice on import ordering and wildcard imports → resolved by consolidating import rules into a single section in code-style-guide and aligning with Ruff configuration.
    - `STYLE-ASYNC` (around lines ~90–120): mixed guidance on when to use async endpoints → refocused into a single async patterns section consistent with FastAPI and ADR-0001 runtime expectations.
    - `STYLE-LOGGING` (around lines ~140–180): duplicated logging patterns across STYLE_* docs → merged into one logging/error-handling subsection coordinated with the new `app/core/errors.py`.
    - `STYLE-VERSIONING` (around lines ~200–220): Python 3.10 vs 3.11 vs 3.14 conflicts → superseded by ADR-0001 and reflected only in the new canonical docs.

- **TEST group → docs/testing-guide.md**
  - Example issues (by approximate reference):
    - `TEST-FIXTURES-DUP` (around lines ~260–300): overlapping fixture patterns between TEST_* docs and TESTING_ARCHITECTURE → unified fixture guidance in testing-guide and shared `tests/conftest.py` implementations.
    - `TEST-MOCKING-CONFLICT` (around lines ~320–350): contradictory recommendations on mocking external services vs. using real dependencies → clarified strategy that prefers Testcontainers-based E2E (ADR-0006) plus focused unit mocking.
    - `TEST-STRUCTURE` (around lines ~360–390): inconsistent folder and naming conventions for tests → resolved via a single directory/naming convention section in testing-guide.
    - `TEST-E2E-ENV` (around lines ~400–430): confusion about how E2E tests interact with dual venvs → clarified as part of E2E section plus updates to development-setup and workflow-and-ci.

- **API and Architecture group → docs/api.md, docs/architecture.md, docs/LIFECYCLE.md**
  - Example issues (by approximate reference):
    - `API-LIFECYCLE-DUP` (around lines ~460–500): duplicated endpoint lifecycle diagrams between LIFECYCLE and api-patterns-guide → moved into a single canonical narrative split across docs/LIFECYCLE.md and docs/api.md per the updated matrix.
    - `API-HEALTH-ENDPOINT` (around lines ~520–540): conflicting health endpoint contract guidance → resolved by aligning with ADR-0007 and documenting the current stance only in docs/api.md and docs/LIFECYCLE.md.
    - `ARCH-RESPONSIBILITIES` (around lines ~560–600): outdated descriptions of service boundaries vs. current code layout → refreshed in docs/architecture.md and cross-checked against actual modules.

- **Workflow, CI, Releases group → docs/workflow-and-ci.md, docs/releases-and-versioning.md**
  - Example issues (by approximate reference):
    - `WF-TRUNK-VS-GITFLOW` (around lines ~620–660): trunk-based vs. Gitflow conflict → resolved by adopting ADR-0002 and documenting only trunk-based practices in workflow-and-ci.
    - `WF-LINT-COMMANDS` (around lines ~680–710): inconsistent lint/test command examples across docs → normalized around `uv run` commands and reflected in workflow-and-ci and README.
    - `REL-CHANGESETS` (around lines ~730–760): multiple change management and release strategies → converged into a single releases-and-versioning flow, superseding older guidance.

Detailed, per-issue tracking for all 169 red flags will be captured and maintained in `working/phase2/conflict_backlog.md` and `working/phase2/research_backlog.md` in later phases, using these identifiers and approximate locations as anchors.

### 5. Migration Sequence

Recommended order of implementation phases, based on dependencies and impact:

1. **Phase 3 – Code Standards & Architecture**
   - Migrate STYLE_* docs into `docs/code-style-guide.md`.
   - Consolidate architecture-overview and LIFECYCLE into `docs/architecture.md` and `docs/api.md`.
   - Update `pyproject.toml`, `.pre-commit-config.yaml`, and introduce `app/core/errors.py`.

2. **Phase 4 – Testing & E2E**
   - Merge TEST_* docs, TEST.md, TESTING_ARCHITECTURE.md, and E2E docs into `docs/testing-guide.md`.
   - Align `tests/conftest.py` and E2E fixtures with ADR-0006 and testing-guide.

3. **Phase 5 – Workflow, Releases, CI**
   - Consolidate workflow docs into `docs/workflow-and-ci.md`.
   - Move versioning/changesets content into `docs/releases-and-versioning.md`.
   - Update `.github/workflows/*` to match ADRs and new doc guidance.

4. **Phase 6 – Hygiene and Cross-References**
   - Clean up `docs/to_integrate/` once all content is migrated.
   - Refresh `README.md`, `docs/README.md`, and `AGENTS.md` to align with the final IA.
   - Verify all internal links and references point to the new canonical docs.

### 6. Acceptance Criteria

The migration is considered complete when all of the following are true:

- Every source document listed in `working/phase1/docs_inventory.md` is mapped to at least one target in this plan, with a completed action (merge/split/retire).
- All 169 red flags in `working/phase1/content_issues.md` are either resolved, explicitly deferred (with rationale), or superseded by ADRs and new docs.
- ADR-0001 through ADR-0010 are reflected in the canonical target documents and supporting code/config changes described above.
- The `docs/to_integrate/` directory contains no orphaned or partially-migrated guidance; remaining files are either archived or fully integrated.
- All cross-references across `README.md`, `docs/*.md`, and in-code comments/scripts point to the new canonical documents.
- CI passes with the updated Python version, Ruff configuration, OpenAPI workflow, and testing strategy.

This document should be updated if new ADRs are added, additional red flags are discovered, or the target information architecture in `working/phase2/docs_ia.md` changes.
