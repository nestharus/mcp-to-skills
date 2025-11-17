## Phase 2 Conflict Backlog

Counts derived from content_issues triage: 120 resolved via ADRs/merges; 33 research in research_backlog.md; 16 active conflicts here.
This backlog tracks the subset of the 169 red flags from `working/phase1/content_issues.md` that still require manual resolution in Phases 3–5.
Items already addressed by the migration plan in `working/phase2/migration_plan.md` or by ADR decisions are excluded here but remain annotated in `content_issues.md` for traceability.
Theme ownership and phase names follow `working/phase2/phase_theme_assignments.md`.

### Summary

- Total original issues: 169
- Resolved via migration plan / ADRs: 0
- Remaining conflicts in this backlog: 16
- Items requiring external research: tracked separately in `working/phase2/research_backlog.md`

Breakdown by theme:

- Code Standards & Architecture: 5
- Testing & E2E: 4
- Workflow, Releases, CI: 7

Breakdown by category:

- Duplicates: 0
- Conflicts: 7
- Staleness: 0
- Gaps: 4
- Naming: 1
- Env: 4
- OpenAPI: 1
- Testing: 3
- Versioning: 2
- Health: 0
- Other: 0

### Code Standards & Architecture

| Issue ID | Issue Description | Source Doc(s) | Target Phase | Priority | Notes |
| -------- | ----------------- | ------------- | ------------ | -------- | ----- |
| CONFLICT-STYLE-ERRORCODE | Example `ErrorCode` enum in STYLE_3 may not match actual error handling contracts. | `docs/to_integrate/STYLE_3.md`, `app/contracts/metadata_contract.py`, `app/routes/metadata_router_v1.py` | Phase 3 – Code Standards & Architecture | High | Audit actual error types and codes before finalizing `docs/code-style-guide.md` and `docs/api.md` examples. See `working/phase1/content_issues.md` Conflicts section. |
| CONFLICT-STYLE-DOMAIN-MODEL | Example domain models in STYLE_4 (`Project`, `ProjectStatus`, `DesignToken`) do not reflect the MCP metadata domain used in this repo. | `docs/to_integrate/STYLE_4.md`, `app/contracts/metadata_contract.py` | Phase 3 – Code Standards & Architecture | Medium | Replace example models with realistic `MetadataItem` / request/response types when consolidating into `docs/code-style-guide.md`. |
| CONFLICT-STYLE-PROJECT-STRUCTURE | Sample project layout in STYLE_5 (`api/routes/users.py`) diverges from actual modules like `app/routes/metadata_router_v1.py` and MCP services. | `docs/to_integrate/STYLE_5.md`, `app/routes/metadata_router_v1.py` | Phase 3 – Code Standards & Architecture | Medium | Align structure examples with real router/service layout and planned `docs/architecture.md` guidance. |
| CONFLICT-PYTHON-VERSION | STYLE_1 targets Python 3.14+ while some docs still reference 3.12+. | `docs/to_integrate/STYLE_1.md`, `README.md`, `AGENTS.md` | Phase 3 – Code Standards & Architecture | High | Ensure all docs and tooling examples align with ADR-0001 and the `pyproject.toml` `requires-python` setting. |
| GAP-STYLE-ERRORS-MODULE | Style docs recommend a centralized error layer but repo lacks `app/core/errors.py`. | `docs/to_integrate/STYLE_6.md` | Phase 3 – Code Standards & Architecture | Medium | Implement `app/core/errors.py` per `working/phase2/migration_plan.md` and align docs/examples. |

### Testing & E2E

| Issue ID | Issue Description | Source Doc(s) | Target Phase | Priority | Notes |
| -------- | ----------------- | ------------- | ------------ | -------- | ----- |
| NAMING-FIXTURE-CONFLICT | Fixture names suggested in TEST_7 (`api_base_url`, `wait_for_api`) conflict with existing fixtures (`live_server`, `api_client`). | `docs/to_integrate/TEST_7.md`, `tests/conftest.py` | Phase 4 – Testing & E2E | Medium | Standardize fixture naming in `docs/testing-guide.md` and update examples to match actual fixtures. |
| GAP-PYTEST-CHECK | TEST_7 uses plain `assert` while E2E docs recommend `pytest-check` for soft assertions. | `docs/to_integrate/TEST_7.md`, `docs/to_integrate/e2e-testing-guide.md` | Phase 4 – Testing & E2E | Low | Decide whether to adopt `pytest-check` broadly and reflect the decision in tests and `docs/testing-guide.md`. |
| CONFLICT-TEST-DOCS-VS-CODE | Fixture instructions in `docs/TEST.md` duplicate or diverge from `tests/conftest.py`. | `docs/TEST.md`, `tests/conftest.py` | Phase 4 – Testing & E2E | High | Make `tests/conftest.py` the source of truth; ensure `docs/testing-guide.md` only documents patterns that match actual fixtures. |
| GAP-E2E-COMPONENT-TESTS | Component test guidance stops short of true E2E once real MCP subprocess support ships. | `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md` | Phase 4 – Testing & E2E | Medium | Clarify the boundary between component and E2E tests in `docs/testing-guide.md` and adjust examples as MCP subprocess support evolves. |

### Workflow, Releases, CI

| Issue ID | Issue Description | Source Doc(s) | Target Phase | Priority | Notes |
| -------- | ----------------- | ------------- | ------------ | -------- | ----- |
| ENV-DUAL-VENV-TROUBLESHOOTING | Missing troubleshooting guidance for diverging `.venv` / `.venv2` environments. | `AGENTS.md`, `README.md` | Phase 5 – Workflow, Releases, CI | Medium | Expand dual-venv guidance in `docs/workflow-and-ci.md` and `docs/development-setup.md` to cover common failure modes. |
| ENV-PRECOMMIT-MISMATCH | STYLE_8 pre-commit recommendations conflict with actual `.pre-commit-config.yaml` (single `uv run lint` hook). | `docs/to_integrate/STYLE_8.md`, `.pre-commit-config.yaml` | Phase 5 – Workflow, Releases, CI | High | Align pre-commit guidance in `docs/workflow-and-ci.md` with the real hooks and `scripts/lint.py`. |
| ENV-SCRIPTS-SECTION-MISMATCH | STYLE_8 uses `[tool.uv.scripts]` examples while the repo uses `[project.scripts]`. | `docs/to_integrate/STYLE_8.md`, `pyproject.toml` | Phase 5 – Workflow, Releases, CI | Medium | Update examples to reflect actual `uv` invocation patterns and `pyproject.toml` layout. |
| ENV-WORKFLOW-INCONSISTENT-LINT | STYLE_8 describes separate `format` and `lint` commands but the repo uses a single `uv run lint`. | `docs/to_integrate/STYLE_8.md`, `scripts/lint.py` | Phase 5 – Workflow, Releases, CI | Medium | Clarify canonical commands in `docs/workflow-and-ci.md`; avoid duplicating obsolete workflows. |
| VERSION-CHANGESETS-TOOLING | Changesets commands are documented but not implemented in scripts. | `docs/to_integrate/changesets-guide.md`, `pyproject.toml`, `tools/` | Phase 5 – Workflow, Releases, CI | High | Either implement changesets-like tooling (e.g., via Python ecosystem tools) or update `docs/releases-and-versioning.md` with the chosen approach. |
| VERSION-PRE-RELEASE-GAPS | No clear guidance for handling pre-release versions and build metadata. | `docs/to_integrate/changesets-guide.md` | Phase 5 – Workflow, Releases, CI | Medium | Document strategy in `docs/releases-and-versioning.md` consistent with trunk-based development. |
| OPENAPI-TOOLING-DISCONNECT | STYLE_6 discusses OpenAPI generation but does not align with `scripts/gen_openapi.py` usage. | `docs/to_integrate/STYLE_6.md`, `scripts/gen_openapi.py`, `openapi/openapi.json` | Phase 5 – Workflow, Releases, CI | High | Ensure OpenAPI workflow is documented in `docs/workflow-and-ci.md` and enforced in CI. |

### Cross-Cutting Issues

Some issues affect multiple themes and should be coordinated across phases:

- DUAL-VENV-AND-E2E: Dual-venv setup affects both environment onboarding (Workflow, Releases, CI) and E2E testing reliability (Testing & E2E). Coordinate updates between `docs/development-setup.md`, `docs/workflow-and-ci.md`, and `docs/testing-guide.md`.
- TOOLING-STACK-CLARITY: Overlapping or ambiguous guidance on Ruff, formatters, and type checkers spans style, testing, and workflow docs. Final decisions should be reflected consistently in `docs/code-style-guide.md`, `docs/testing-guide.md`, and `docs/workflow-and-ci.md`.

### Resolution Tracking Guidance

- When resolving an issue, update this backlog row with a link to the commit/PR and mark the status in an adjacent column (for example, by adding a `Status` column with values such as `Open`, `In Progress`, `Done`).
- Always cross-reference the originating description in `working/phase1/content_issues.md` (by category and bullet text) so that the original 169-item analysis remains traceable.
- For issues that become purely research questions, move them into `working/phase2/research_backlog.md` and mark the corresponding backlog row here as "Moved to research_backlog".
