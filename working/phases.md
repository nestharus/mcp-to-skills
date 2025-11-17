High-level strategy:

1. Do a foundation pass that produces summaries and an inventory of all docs, without trying to read everything in one go.
2. Design the final documentation information architecture and a migration plan, based on those summaries.
3. Execute themed integration phases (code standards & architecture; testing & E2E; workflow, releases & CI), each one using both the original docs and the growing set of summaries/plans from prior phases.
4. In each phase, have the planner only work on small, explicit subsets of files and accumulate outputs into `working/` files that the next phase consumes.

Below are the “big phases” with goals, directions, and deliverables. Each of these is what you hand to the planner as the task to break down.

---

## Phase 1 – Per-document summaries and content inventory (foundation)

**Goal**

Create a structured understanding of what each doc in `docs/to_integrate/` and key existing docs contains, without trying to integrate or rewrite anything yet. This is the raw material for all later phases.

**Scope / directions**

* Include:

  * All files under `docs/to_integrate/`
  * Existing: `docs/LIFECYCLE.md`, `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`, `docs/README.md` (if present), root `README.md`, `AGENTS.md`.
* No single task should be “read all N docs”; tasks should work on 1–3 docs at a time, grouped by theme (STYLE, TEST, API, workflow, changesets/CI, etc.).
* For each doc, produce:

  * A short structured summary (purpose, main topics, opinions/guidelines, assumptions, obvious staleness).
  * Tags: e.g. `style`, `testing`, `architecture`, `workflow`, `changesets`, `fastapi`, `pytest`, `ci`.
* Start a preliminary mapping of “this doc probably feeds into these target docs” (e.g. STYLE_* → `code-style-guide.md`).
* Collect “red flags”: duplicated sections, obviously outdated content, conflicting guidance, obvious missing topics.

**Inputs**

* `docs/to_integrate/*`
* `docs/LIFECYCLE.md`
* `docs/TEST.md`
* `docs/TESTING_ARCHITECTURE.md`
* `docs/README.md` (if exists)
* `README.md`
* `AGENTS.md`

**Deliverables**

* `working/phase1/summaries/<relative-path>.summary.md`
  One file per source doc, machine- and human-readable.
* `working/phase1/docs_inventory.md`
  Table with: source path, short title, tags, rough target doc(s), notes.
* `working/phase1/content_issues.md`
  List of conflicts, duplicates, staleness, gaps (high-level, not resolved yet).
* `working/phase1/open_questions.md`
  Questions that clearly need research or product/project decisions.

Subsequent phases must read these `working/phase1/*` files first, and only go back to original docs as needed.

---

## Phase 2 – Final docs information architecture and migration plan

**Goal**

Define the final desired documentation layout under `docs/`, and a concrete mapping from all existing + `to_integrate` docs into that layout. This is still planning, not heavy rewriting.

**Scope / directions**

* Operate primarily on:

  * `working/phase1/docs_inventory.md`
  * `working/phase1/summaries/*`
  * `working/phase1/content_issues.md`
* Use the summaries to:

  * Decide the final set of “top-level” docs (e.g. `code-style-guide.md`, `linting-guide.md`, `testing-guide.md`, `testing-architecture.md`, `api-patterns-guide.md`, `architecture-overview.md`, `development-workflow.md`, `development-setup.md`, `git-workflow.md`, `changesets-guide.md`, `e2e-testing-guide.md`, `e2e-dependencies.md`, `docs/README.md`, etc.).
  * Decide which existing docs are kept as-is, merged, renamed, or deleted.
  * Decide which non-doc files need to be touched by later phases (`tests/conftest.py`, `.github/workflows/*`, `.changeset/`, `pyproject.toml`, etc.).
* Explicitly avoid “read everything again”; rely on the Phase 1 summaries except when a detail absolutely matters.
* Clarify which themes map to which later phases:

  * Code standards & architecture
  * Testing & E2E
  * Workflow, release, changesets, CI

**Inputs**

* `working/phase1/summaries/*`
* `working/phase1/docs_inventory.md`
* `working/phase1/content_issues.md`
* `working/phase1/open_questions.md`

**Deliverables**

* `working/phase2/docs_ia.md`
  Final docs information architecture:

  * List of target docs under `docs/`
  * Short purpose for each
  * Relationships/cross-links (e.g. where `LIFECYCLE.md` is referenced).
* `working/phase2/migration_plan.md`
  For each source file (docs and key code files): target file(s), merge strategy (merge/split/retire), priority, notes.
* `working/phase2/phase_theme_assignments.md`
  For each target doc or area, which later “big phase” owns integrating it.
* Updated/trimmed `working/phase1/content_issues.md` folded into:

  * `working/phase2/conflict_backlog.md` (issues to be resolved in later phases).
* Optional: `working/phase2/research_backlog.md`
  Grouped research topics for Python 3.14, pytest, FastAPI, changesets, CI, etc., tagged by which later phase they support.

All later phases must treat `migration_plan.md` as the source of truth for what moves where.

Adopt Diátaxis tagging for every target doc (Tutorial / How‑to / Reference / Explanation). Include this “doc type” in working/phase2/docs_ia.md so authors know how to write each page.
Diátaxis

Mandate ADRs as the output format for decisions (store under docs/adr/ and link from each guide’s “Decisions” sidebar).
Architectural Decision Records

Deliverable additions: a migration matrix with “source → target, action (merge/split/retire), owner, priority” and a short style taxonomy (what belongs in style vs. architecture vs. workflow).

---

## Phase 3 – Code standards, linting, and architecture overview

**Goal**

Create a coherent, modern set of code standards and architecture docs aligned with Python 3.14, FastAPI, and the actual project structure, then update or produce the corresponding documentation and config.

**What this phase owns**

* Style and linting guidance:

  * `STYLE_1.md` … `STYLE_8.md`
  * `linting-guide.md`
* FastAPI code patterns:

  * `api-patterns-guide.md`
  * relevant parts of `fastapi-best-practices.md`
* Architecture:

  * `architecture-overview.md`
  * any relevant pieces from `docs/TESTING_ARCHITECTURE.md` that describe system structure
* Tooling/config that encodes style:

  * `pyproject.toml`
  * `.pre-commit-config.yaml`
  * any style-related scripts under `scripts/`

**Scope / directions**

* Use Phase 1 summaries and Phase 2 migration plan to decide which source docs feed:

  * `docs/code-style-guide.md`
  * `docs/linting-guide.md`
  * `docs/api-patterns-guide.md`
  * `docs/architecture-overview.md`
* Use `app/core/*`, `app/routes/metadata_router_v1.py`, `app/services/*`, `app/main.py` to ensure docs match reality (e.g. versioned handlers vs routers, dependency wiring, settings).
* This phase should:

  * Include research tasks on Python 3.14 / FastAPI best practices for style, architecture, and dependency management.
  * Include conflict-resolution tasks to unify STYLE_* docs and reconcile them with actual code and linting tools.
  * Produce updated docs and updated config/tooling plans; not necessarily implement every refactor, but at least document the intended architecture and conventions.

**Inputs**

* `working/phase1/summaries/*` (for STYLE, linting, API, architecture docs)
* `working/phase2/docs_ia.md`
* `working/phase2/migration_plan.md`
* Source docs under `docs/to_integrate` relevant to style/architecture:

  * `STYLE_*.md`
  * `linting-guide.md`
  * `api-patterns-guide.md`
  * `fastapi-best-practices.md`
  * `architecture-overview.md`
* Code:

  * `app/core/dependencies.py`
  * `app/core/factory.py`
  * `app/core/settings.py`
  * `app/routes/metadata_router_v1.py`
  * `app/services/*`
  * `app/main.py`
* Tooling:

  * `pyproject.toml`
  * `.pre-commit-config.yaml`
  * relevant `scripts/`

**Deliverables**

* Final (or near-final) docs under `docs/`:

  * `docs/code-style-guide.md`
  * `docs/linting-guide.md`
  * `docs/api-patterns-guide.md`
  * `docs/architecture-overview.md`
* `working/phase3/style_conflicts_resolved.md`
  Explicit decisions where STYLE_* docs disagreed or differed from current code/tools.
* `working/phase3/tooling_alignment_plan.md`
  Concrete plan or applied changes for aligning `pyproject.toml`, `.pre-commit-config.yaml`, and scripts with the agreed style/linting rules.
* Optional: `working/phase3/refactor_todo.md`
  Architectural refactors that are desirable but out-of-scope for this docs phase (e.g. fully moving to versioned handlers).

Later phases (testing, CI) must assume the conventions defined here .

Consolidate on Ruff (lint+format) and encode rules in pyproject.toml; document “Why Ruff” in the style guide.
Astral Docs

Add a “Health & lifecycle” section to architecture with explicit contracts and probe settings, plus code references.
Kubernetes

Ensure the uv developer workflow is shown once (project‑level), and all examples use uv run ….
Astral Docs

---

## Phase 4 – Testing, fixtures, and E2E story

**Goal**

Unify and modernize all testing documentation and fixtures into a single, coherent testing strategy that matches the actual tests and supports pytest + FastAPI best practices.

**What this phase owns**

* Testing docs:

  * `TEST_1.md` … `TEST_9.md`
  * `docs/TEST.md`
  * `docs/TESTING_ARCHITECTURE.md`
  * `e2e-testing-guide.md`
  * `e2e_dependencies.md`
* Fixtures and test layout:

  * `docs/to_integrate/test_fixtures_soft_and_e2e.py`
  * `tests/conftest.py`
  * `tests/unit/*`, `tests/integration/*`, `tests/component/*`
* Any test-related configuration:

  * pytest config in `pyproject.toml` or `pytest.ini`
  * test-related scripts in `scripts/`

**Scope / directions**

* Use Phase 2’s migration plan to decide final testing docs:

  * `docs/testing-guide.md`
  * `docs/testing-architecture.md`
  * `docs/e2e-testing-guide.md`
  * `docs/e2e-dependencies.md`
* Use Phase 3’s style and architecture decisions as constraints for test code style and structure.
* This phase should:

  * Include research tasks on pytest + FastAPI testing best practices (async, fixtures, TestClient/httpx, marking, layers).
  * Include summarization-and-alignment tasks for TEST_* docs and existing testing docs, using Phase 1 summaries as starting point.
  * Include conflict-resolution tasks between:

    * written guidance (all test docs),
    * actual `tests/*` structure and fixtures.
  * Produce a final fixture layout plan and then update `tests/conftest.py` and/or create fixture modules accordingly.

**Inputs**

* `working/phase1/summaries/*` (testing/E2E docs)
* `working/phase2/docs_ia.md`
* `working/phase2/migration_plan.md`
* `working/phase3/style_conflicts_resolved.md` (for consistency)
* Testing-related source files:

  * `docs/to_integrate/TEST_*.md`
  * `docs/to_integrate/e2e-testing-guide.md`
  * `docs/to_integrate/e2e_dependencies.md`
  * `docs/TEST.md`
  * `docs/TESTING_ARCHITECTURE.md`
  * `docs/to_integrate/test_fixtures_soft_and_e2e.py`
  * `tests/conftest.py`
  * `tests/unit/*`, `tests/integration/*`, `tests/component/*`
  * `pyproject.toml` (pytest config)
  * test-related `scripts/`

**Deliverables**

* Final (or near-final) docs under `docs/`:

  * `docs/testing-guide.md`
  * `docs/testing-architecture.md` (or renamed version of TESTING_ARCHITECTURE)
  * `docs/e2e-testing-guide.md`
  * `docs/e2e-dependencies.md`
* Updated fixtures and layout:

  * Updated `tests/conftest.py` integrating `test_fixtures_soft_and_e2e.py` content per the new fixture plan.
  * Any new fixture modules or folder restructuring under `tests/*` if required by the plan.
* `working/phase4/testing_conflicts_resolved.md`
  Decisions about layering (unit/integration/component/e2e), where fixtures live, naming, and how tests are run.
* `working/phase4/testing_commands.md`
  Canonical commands for running each test layer (inputs later used by dev workflow / command reference / CI).

Later phases (workflow & CI) will reference these commands and structure.

Use pytest‑asyncio + HTTPX ASGITransport for app‑in‑process tests; reserve Testcontainers for external services.
pytest-asyncio
+2
HTTPX
+2

Add optional Schemathesis track for schema conformance and fuzzing (nightly).
Schemathesis

Capture canonical commands for each layer; Phase 5 will import them for CI.

---

## Phase 5 – Developer workflow, Git workflow, releases, changesets, CI, and docs index

**Goal**

Define and document how developers actually work on this repo end-to-end: setup, day-to-day workflow, branching and Git strategy, testing in practice, release process with Changesets (or chosen tool), and CI pipeline. Also finalize the docs landing pages.

**What this phase owns**

* Workflow and setup docs:

  * `development-workflow.md`
  * `devpelopment-setup.md` → `development-setup.md`
  * `git-workflow.md`
  * `command-reference.md`
  * `docs/LIFECYCLE.md`
  * `docs/to_integrate/README.md` → `docs/README.md`
  * Root `README.md`
* Release and changesets:

  * `changesets-guide.md`
  * `.changeset/` folder organization and config
* CI:

  * `.github/workflows/ci.yml`
  * `.github/workflows/changesets.yml`
* Cleanup:

  * removal of `app/ui` and any outdated references
  * aligning docs with actual repo layout and tools

**Scope / directions**

* Use previous phases’ outputs as constraints:

  * Style & architecture (Phase 3)
  * Testing structure & commands (Phase 4)
* This phase should:

  * Include research tasks for:

    * Changesets usage and GitHub Actions integration,
    * sensible Git workflow for this repo,
    * modern Python/FastAPI CI patterns (lint, type-check, tests, build OpenAPI, etc.).
  * Design the release process:

    * how changesets are created,
    * how versioning works,
    * how CI ties into merges and releases.
  * Design the CI pipeline (jobs, stages, what commands to run) using the canonical commands from Phase 4 and the tooling from Phase 3.
  * Finalize the docs structure as a coherent whole:

    * `docs/README.md` as docs index,
    * root `README.md` as project landing with pointers into docs,
    * cross-links between workflow, lifecycle, style, testing, architecture, and changesets docs.

**Inputs**

* `working/phase1/summaries/*` (workflow/release docs)
* `working/phase2/docs_ia.md`
* `working/phase2/migration_plan.md`
* `working/phase3/tooling_alignment_plan.md`
* `working/phase4/testing_commands.md`
* `docs/to_integrate/*` relevant to workflow:

  * `changesets-guide.md`
  * `development-workflow.md`
  * `devpelopment-setup.md`
  * `git-workflow.md`
  * `command-reference.md`
  * `README.md` (to docs/README)
* Existing:

  * `docs/LIFECYCLE.md`
  * `docs/README.md` (if exists)
  * `README.md`
* Repo:

  * `.github/workflows/*`
  * `.factory/`
  * `.changeset/` (if present, or to be created)
  * `pyproject.toml`
  * `uv.lock`
  * `app/ui` and references to it
  * `scripts/`

**Deliverables**

* Final/updated docs under `docs/`:

  * `docs/development-workflow.md`
  * `docs/development-setup.md`
  * `docs/git-workflow.md`
  * `docs/command-reference.md`
  * `docs/changesets-guide.md`
  * `docs/README.md` as the docs index
  * Updated `docs/LIFECYCLE.md` if needed
* Repo and config:

  * `.changeset/` directory initialized or restructured according to plan.
  * `.github/workflows/ci.yml` designed/updated to run style, lint, type-check, tests, and any other checks.
  * `.github/workflows/changesets.yml` designed/updated to integrate with the Changesets process.
  * `app/ui` removed and references cleaned up, if that’s the decided direction.
* Top-level:

  * Updated root `README.md` aligned with final architecture, workflows, and docs layout.
* `working/phase5/system_overview.md`
  High-level explanation of how everything fits together: code structure, tests, workflows, CI, releases, docs.

Choose GitHub Flow or Trunk‑Based explicitly and add release‑branch rules.
GitHub Docs
+1

Prefer Towncrier for human‑written changes with low merge conflict; if fully automated versioning is required, layer Python Semantic Release.
Towncrier
+1

CI: matrix jobs (lint/format → tests → openapi‑diff → package). Add workflow_dispatch for manual runs.
GitHub Docs

---