# Content Issues (Conflicts, Duplicates, Staleness, Gaps)


Total red flags collected: **169** from **35** summaries.


### Duplicates (34)

**Examples**
- `AGENTS`: Some instructions (“run tests after every change”) are general best practices rather than agent-exclusive guidance, raising question of duplicate ownership.
- `README`: Setup, linting, and API-reference sections overlap with multiple `docs/to_integrate/*.md` guides—dedupe in later phases.
- `README`: OpenAPI and health check details repeat information already kept in schema + lifecycle doc; risk of inconsistencies.
- `docs/TEST`: Scope overlap with `docs/TESTING_ARCHITECTURE.md`—distinguish “how” vs “why” or merge carefully.
- `docs/TEST`: Fixture instructions duplicate details already encoded in code (`tests/conftest.py`), risking drift.
- `docs/to_integrate/STYLE_1`: **Testing overlap**: STYLE_1's testing section duplicates content in `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md`—consolidate in Phase 2.
- `docs/to_integrate/STYLE_2`: **Overlap with STYLE_1**: Significant content duplication with `docs/to_integrate/STYLE_1.md` on typing, annotations, and Python 3.14 features—consolidate in Phase 2.
- `docs/to_integrate/STYLE_3`: **Overlap with to_integrate docs**: Content overlaps with `docs/to_integrate/api-patterns-guide.md` and `docs/to_integrate/fastapi-best-practices.md`—consolidate in Phase 2.

**Recommended action**

- Consolidate repeated guidance into canonical target docs (e.g., `code-style-guide.md`, `testing-guide.md`, `api.md`). Keep cross-links but remove repeated prose.


### Conflicts (20)

**Examples**
- `AGENTS`: No troubleshooting guidance for diverging venv states or dependency drift between `.venv` and `.venv2`.
- `docs/TEST`: Fixture instructions duplicate details already encoded in code (`tests/conftest.py`), risking drift.
- `docs/TEST`: Potential conflicts with `docs/to_integrate/TEST_*.md` series that may contain divergent advice.
- `docs/to_integrate/STYLE_1`: **Python version conflict**: STYLE_1 targets Python 3.14+, but `README.md` tech stack section may reference 3.12+ in some places—needs reconciliation.
- `docs/to_integrate/STYLE_2`: **No conflict with existing docs**: Unlike STYLE_1, doesn't introduce tooling or conventions that contradict `README.md`/`AGENTS.md`.
- `docs/to_integrate/STYLE_3`: **ErrorCode mismatch**: Example `ErrorCode` enum may not match actual error handling in `app/contracts/metadata_contract.py` or `app/routes/metadata_router_v1.py`—audit existing code.
- `docs/to_integrate/STYLE_4`: **Domain model mismatch**: Example types (`Project`, `ProjectStatus`, `DesignToken`) do not match the actual MCP metadata domain (`MetadataItem`, `FetchRequest`, etc.) defined in `app/contracts/metadata_contract.py`.
- `docs/to_integrate/STYLE_5`: **Project structure mismatch**: The sample project layout (`api/routes/users.py`) does not match this repository, which uses `app/routes/metadata_router_v1.py` and MCP-focused services; examples should be updated to use the actual module structure.

**Recommended action**

- During integration, resolve inconsistencies by deferring to code and CI defaults. Record the decision in the canonical doc and add a short rationale.


### Staleness (3)

**Examples**
- `README`: “Future steps” blur current vs planned capabilities, potentially misleading readers about what exists today.
- `docs/TESTING_ARCHITECTURE`: Historical note about `app/tests/` could confuse newcomers who never saw that layout; consider moving to a “history” appendix.
- `docs/to_integrate/STYLE_8`: **Version drift**: Hard-coded tool versions in STYLE_8 do not match `pyproject.toml` and will quickly become outdated; examples should either be updated or rewritten to be version-agnostic.

**Recommended action**

- Mark future or planned content with a **Future** callout and date. Where possible, add a checklist to ensure updates land alongside code changes.


### Gaps (9)

**Examples**
- `docs/TESTING_ARCHITECTURE`: Lacks guidance on exceptional cases (e.g., when an `__init__.py` might still be necessary for namespace packages).
- `docs/to_integrate/STYLE_2`: **Missing examples**: No concrete examples of `annotationlib.get_annotations()` usage or runtime introspection patterns.
- `docs/to_integrate/STYLE_4`: **Missing linting enforcement**: Recommends naming conventions but does not describe how they are enforced; this should be aligned with the actual configuration in `pyproject.toml` and the Ruff setup.
- `docs/to_integrate/STYLE_5`: **Missing complexity enforcement details**: Suggests small functions but does not specify how tools (for example, Ruff, pylint) enforce max complexity or lines; should be aligned with `pyproject.toml`.
- `docs/to_integrate/STYLE_6`: **Missing custom exception layer**: Recommends custom business exceptions (for example, `UserNotFoundError`, `UserAlreadyExistsError`) and a centralized error-handling strategy, but the project lacks an `app/core/errors.py` or equivalent exception hierarchy.
- `docs/to_integrate/STYLE_8`: **Missing Ruff config details**: STYLE_8 mentions that Ruff is configured via `pyproject.toml` but does not reflect this repository's actual settings (e.g., 100-character line length); integrated docs should reference the concrete configuration.
- `docs/to_integrate/TEST_7`: Missing pytest-check integration: TEST_7 uses plain `assert` statements, while `docs/to_integrate/e2e-testing-guide.md` recommends pytest-check for soft assertions in E2E tests.
- `docs/to_integrate/changesets-guide`: The `.changeset/` directory may be missing, despite the guide assuming it exists and is used in all feature and bugfix PRs.

**Recommended action**

- Convert gaps into issues and add to `open_questions.md`. Assign a target owner and due date.


### Naming (5)

**Examples**
- `docs/to_integrate/STYLE_3`: **Generic naming overlap**: `TypeVar` naming guidance duplicates STYLE_1 and STYLE_2—consolidate in single style guide.
- `docs/to_integrate/STYLE_4`: **Overlap with STYLE_1**: Repeats naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE) already covered in STYLE_1; these should be consolidated into a single style guide section.
- `docs/to_integrate/STYLE_4`: **Missing linting enforcement**: Recommends naming conventions but does not describe how they are enforced; this should be aligned with the actual configuration in `pyproject.toml` and the Ruff setup.
- `docs/to_integrate/STYLE_5`: **File naming vs router content**: Recommends one responsibility per file, but `metadata_router_v1.py` contains multiple route functions; expectations for router modules should be clarified.
- `docs/to_integrate/TEST_7`: Fixture naming conflict: TEST_7 suggests fixtures like `api_base_url` and `wait_for_api`, but the project already uses fixtures such as `live_server` and `api_client` in `tests/conftest.py`.

**Recommended action**

- Fix misspellings (e.g., `devpelopment-setup.md` → `development-setup.md`) and add redirects/aliases if external links exist.


### Env (14)

**Examples**
- `AGENTS`: Dual-venv requirement can confuse newcomers who only read README; consider referencing this doc elsewhere.
- `AGENTS`: No troubleshooting guidance for diverging venv states or dependency drift between `.venv` and `.venv2`.
- `README`: No explicit mention of dual-venv nuance described in `AGENTS.md`, so new contributors may miss important context.
- `docs/to_integrate/STYLE_8`: **Pre-commit configuration mismatch**: The recommended multi-repo pre-commit setup conflicts with the actual `.pre-commit-config.yaml`, which relies on a single `local` hook running `uv run lint`; documentation and configuration must be reconciled to avoid confusion.
- `docs/to_integrate/STYLE_8`: **Script section mismatch**: The use of `[tool.uv.scripts]` in examples does not match the project's current `[project.scripts]` usage; STYLE_8 should be updated to reflect how `uv` is actually invoked here.
- `docs/to_integrate/STYLE_8`: **Workflow inconsistency**: STYLE_8's narrative of separate `format` and `lint` commands differs from the reality that `uv run lint` (via `scripts/lint.py`) already executes formatting; documentation should clarify that a single command is the canonical workflow.
- `docs/to_integrate/STYLE_8`: **CI integration specifics**: STYLE_8 vaguely recommends adding `uv run lint` to CI without showing concrete CI configuration; this must be coordinated with `docs/to_integrate/git-workflow.md` and the project's actual CI workflows.
- `docs/to_integrate/changesets-guide`: Changesets tooling (`uv run changeset`, `uv run version-packages`, `uv run release`) may not yet be implemented in `pyproject.toml` `[tool.uv.scripts]` or `tools/`.

**Recommended action**

- Standardize commands on `uv run ...` and document dual-venv usage clearly; prefer CLI-agnostic invocations.


### Openapi (5)

**Examples**
- `AGENTS`: Manual OpenAPI regeneration remains error-prone; automation would reduce misses.
- `README`: OpenAPI and health check details repeat information already kept in schema + lifecycle doc; risk of inconsistencies.
- `docs/LIFECYCLE`: Health check guidance overlaps with README and schema docs; divergence likely without consolidation.
- `docs/to_integrate/STYLE_6`: **OpenAPI tooling disconnect**: Discusses automatic OpenAPI generation but does not reference the actual tooling in this repo (`scripts/gen_openapi.py` and `openapi/openapi.json`), which should be aligned.
- `docs/to_integrate/development-workflow`: Mandates regenerating OpenAPI on API changes but does not explain how to validate the generated schema or handle generation failures.

**Recommended action**

- Automate OpenAPI export in pre-commit and CI; fail builds on drift; link `/openapi.json` in docs.


### Testing (39)

**Examples**
- `docs/TEST`: Fixture instructions duplicate details already encoded in code (`tests/conftest.py`), risking drift.
- `docs/TEST`: Component test guidance stops short of true E2E once real MCP subprocess support ships.
- `docs/TESTING_ARCHITECTURE`: Reiterates information already present in `docs/TEST.md`; ensure boundaries between rationale vs execution remain clear.
- `docs/to_integrate/STYLE_1`: **Testing overlap**: STYLE_1's testing section duplicates content in `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md`—consolidate in Phase 2.
- `docs/to_integrate/STYLE_6`: **Testing patterns vs current tests**: Mentions DI-based testing strategies and dependency overrides, but does not reference the existing testing setup (`tests/conftest.py`, `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`), which already define how tests are structured.
- `docs/to_integrate/STYLE_7`: **No FastAPI integration**: Guidance is written in framework-agnostic terms and does not reference FastAPI constructs like `HTTPException` or application-level exception handlers; this needs alignment with how errors are actually surfaced in `app/routes/metadata_router_v1.py` and related routers.
- `docs/to_integrate/STYLE_7`: **Overlap with testing docs**: Error handling and custom exception patterns have implications for tests and fixtures, which may overlap with `docs/TEST.md` and `docs/to_integrate/TEST_*.md`; coordination is needed when integrating.
- `docs/to_integrate/STYLE_8`: **Duplicate tooling documentation**: STYLE_8 substantially overlaps with `docs/to_integrate/linting-guide.md` and the `README.md` Code Quality section; Phase 2 integration should merge these into a single, authoritative description of the tooling stack.

**Recommended action**

- Unify on `pytest` (+ `pytest-asyncio` for async). For E2E, use `testcontainers` for external deps and keep fixtures in `tests/conftest.py`.


### Versioning (5)

**Examples**
- `docs/to_integrate/STYLE_1`: **Python version conflict**: STYLE_1 targets Python 3.14+, but `README.md` tech stack section may reference 3.12+ in some places—needs reconciliation.
- `docs/to_integrate/STYLE_8`: **Version drift**: Hard-coded tool versions in STYLE_8 do not match `pyproject.toml` and will quickly become outdated; examples should either be updated or rewritten to be version-agnostic.
- `docs/to_integrate/changesets-guide`: Changesets tooling (`uv run changeset`, `uv run version-packages`, `uv run release`) may not yet be implemented in `pyproject.toml` `[tool.uv.scripts]` or `tools/`.
- `docs/to_integrate/changesets-guide`: No guidance on handling pre-release versions (e.g., `1.0.0-alpha.1`), build metadata (e.g., `1.0.0+build.123`), or version conflicts.
- `docs/to_integrate/changesets-guide`: The dependency version drift section refers to context7-based lookup without explaining the actual usage pattern or any local tooling for it.

**Recommended action**

- Declare a single supported Python range via `requires-python` in `pyproject.toml`, and align all docs to it.


### Health (2)

**Examples**
- `README`: OpenAPI and health check details repeat information already kept in schema + lifecycle doc; risk of inconsistencies.
- `docs/LIFECYCLE`: Health check guidance overlaps with README and schema docs; divergence likely without consolidation.

**Recommended action**

- Provide distinct `/livez`, `/readyz`, and `/startupz` endpoints and surface them in K8s probes.


### Other (69)

**Examples**
- `docs/LIFECYCLE`: Heavy dependence on future Phase 2 work increases staleness risk if not promptly updated.
- `docs/LIFECYCLE`: Error handling for TOML parsing or MCP initialization is only implied—no explicit remediation guidance.
- `docs/LIFECYCLE`: Cache implementation details live elsewhere (`app/core/settings.py`), so readers may miss nuance without cross-reference.
- `docs/to_integrate/STYLE_1`: **Tooling ambiguity**: STYLE_1 lists multiple options (black OR ruff, mypy OR pyright OR pyre) but `README.md` and `AGENTS.md` only mention Ruff for formatting/linting—clarify project's actual tooling choices.
- `docs/to_integrate/STYLE_1`: **Type checker gap**: STYLE_1 mandates type checking in CI but `README.md` and `AGENTS.md` don't mention running mypy/pyright—determine if type checking is actually enforced.
- `docs/to_integrate/STYLE_1`: **Docstring style undecided**: STYLE_1 says "choose Google or NumPy" but doesn't specify which this project uses—audit existing code and document the decision.
- `docs/to_integrate/STYLE_1`: **Line length consistency**: Verify that `pyproject.toml` and Ruff configuration actually enforce 120-char limit mentioned in STYLE_1.
- `docs/to_integrate/STYLE_1`: **Import sorting**: STYLE_1 mentions isort or Ruff but `README.md` only mentions Ruff—confirm Ruff handles import sorting.

**Recommended action**

- Review individually in Phase 2.
