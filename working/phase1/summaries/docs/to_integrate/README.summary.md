**Purpose**: Serve as a documentation hub/index organizing all project guides into categories (Getting Started, Core Guides subdivided into Architecture/Development/Quality, Quick Reference, Contributing) with links, common commands, and a troubleshooting table.

**Main Topics**:
- Getting Started: links to Development Setup and Development Workflow
- Core Guides organized by theme:
  - Architecture & Design: Architecture Overview, Application Lifecycle, API Patterns Guide
  - Development & Workflow: Git Workflow, Code Style Guide
  - Quality & Testing: Linting & Code Quality Guide, Testing Architecture, E2E Testing Guide
- Quick Reference: key tools (Command Reference), Common Issues table (command not found, dual venv, E2E tests), Common Commands section (uv sync, server, pytest, lint, OpenAPI, Docker)
- Contributing: links to setup, workflow, quality guides, and authoring guidance (stable docs in `docs/`, proposals in `plans/`)
- Help section: check guides, search issues, ask in chat, create new issue

**Opinions/Guidelines**:
- Documentation should be organized by user journey (getting started → core guides → reference)
- Guides should be thematic and focused (separate files for git, testing, linting, etc.)
- Common commands and troubleshooting should be easily accessible in the index
- Stable guidance belongs in `docs/`, proposals in `plans/`
- Index should link to all guides and be kept up-to-date as new docs are added

**Assumptions**:
- All linked guides exist or will exist by the time this index is integrated
- Developers will use this as the primary entry point to project documentation
- `uv` is the canonical tool for all workflows
- E2E tests will use a documented `@pytest.mark.e2e` marker as described in the planned E2E configuration docs (`docs/to_integrate/e2e_dependencies.md`, `docs/to_integrate/e2e-testing-guide.md`), even though that marker is not yet wired into `pyproject.toml` or `tests/conftest.py` in this phase
- Docker is available for containerized workflows
- Project uses `tests/fixtures/sample_mcp.toml` for OpenAPI generation

**Staleness Indicators**:
- Many linked guides don't exist yet in `docs/` (Architecture Overview is empty, Code Style Guide, API Patterns Guide, Git Workflow, Development Workflow, Changesets Guide, Command Reference, Linting Guide, E2E Testing Guide are all in `to_integrate/` awaiting integration)
- Common Issues table references guides that may not be finalized
- Common Commands section duplicates content from root `README.md` and `devpelopment-setup.md`
- No mention of Phase 2 features or roadmap
- "Authoring Docs & Plans" section references `plans/` directory that doesn't exist yet

**Tags**: `index`, `documentation`, `hub`, `navigation`, `getting-started`, `setup`, `prerequisites`, `reference`, `contributing`, `onboarding`, `guides`

**Preliminary Target Docs**:
- Primary target: Integrate as `docs/README.md` (first documentation index for the project)
- Update root `README.md` to link to `docs/README.md` as the primary docs entry point
- Ensure all linked guides are integrated or created before this index goes live
- Consider adding a "Documentation" section to root README that points to this index

**Red Flags** (8-10 specific issues):
1. **Missing guides**: Links to 10+ guides that don't exist yet in `docs/` (Architecture Overview, Code Style Guide, API Patterns Guide, Git Workflow, Development Workflow, Changesets Guide, Command Reference, Linting Guide, E2E Testing Guide)—integrate these first or mark as "Coming Soon".
2. **Common Commands duplication**: Commands section duplicates root `README.md` setup/run/lint sections and `devpelopment-setup.md` verification steps—consolidate in Phase 2 to avoid maintenance burden.
3. **E2E marker integration pending**: References `pytest -m e2e` while the documented `@pytest.mark.e2e` plan in `docs/to_integrate/e2e_dependencies.md` and `docs/to_integrate/e2e-testing-guide.md` is not yet wired into `pyproject.toml` or `tests/conftest.py`—align these configs with the docs before treating the CLI examples here as canonical.
4. **Plans directory missing**: "Authoring Docs & Plans" section references `plans/` directory that doesn't exist—create directory or remove reference.
5. **Common Issues table**: Links to guides for troubleshooting but doesn't provide inline solutions—consider adding brief inline fixes or expanding the table.
6. **No search functionality**: Index is manual links; consider adding a search tool or tags for easier navigation as docs grow.
7. **Overlap with root README**: Root README has a "Documentation" section linking to LIFECYCLE.md, TEST.md, TESTING_ARCHITECTURE.md—reconcile with this index to avoid dual entry points.
8. **Contributing section**: Links to multiple guides but doesn't provide a quick-start for first-time contributors—add a "First Contribution" checklist or link to a CONTRIBUTING.md.
9. **Help section generic**: "Ask in team chat" and "Create a new issue" lack specifics (which chat? issue template?)—add links or clarify channels.
10. **No versioning**: Index doesn't indicate which version of the project it applies to—consider adding a version or "Last Updated" timestamp.

**References**:
- `docs/to_integrate/README.md` (source)
- `README.md` (overlaps: commands, setup, docs links)
- `docs/LIFECYCLE.md` (linked)
- `docs/TEST.md` (linked)
- `docs/TESTING_ARCHITECTURE.md` (linked)
- `docs/to_integrate/devpelopment-setup.md` (linked as Development Setup)
- `docs/to_integrate/development-workflow.md` (linked)
- `docs/to_integrate/git-workflow.md` (linked)
- `docs/to_integrate/command-reference.md` (linked)
- `docs/to_integrate/linting-guide.md` (linked)
- `docs/to_integrate/e2e-testing-guide.md` (linked)
- `docs/to_integrate/architecture-overview.md` (linked, but empty)
- `docs/to_integrate/api-patterns-guide.md` (linked)
- `docs/to_integrate/changesets-guide.md` (linked)
- `pyproject.toml` (pytest markers, scripts)
- `tests/fixtures/sample_mcp.toml` (OpenAPI generation)
