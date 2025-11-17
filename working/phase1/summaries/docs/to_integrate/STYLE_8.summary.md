## Purpose
Document the Python 3.14+ tooling and workflow recommendations centered on `uv`, `ruff` (formatting and linting), `mypy` (type checking), and `checkov` (infrastructure/security scanning), including import ordering and formatting conventions, as well as pre-commit and CI integration patterns.

## Main Topics
- Import ordering conventions enforced by tooling: standard library imports, third-party packages, internal absolute imports, internal relative imports, and `TYPE_CHECKING`-guarded imports.
- Avoiding wildcard imports (`from module import *`) in favor of explicit imports.
- Formatting standards such as 4-space indentation and the use of trailing commas in multi-line literals to reduce diff noise.
- Recommended tooling stack: `ruff` for formatting and linting, `mypy` for static type checking, `checkov` for security/IaC analysis, and `uv` as the task runner.
- Task/script definitions in configuration (shown as `[tool.uv.scripts]` examples) to provide `uv run format`, `uv run lint`, and related commands.
- Pre-commit hook configuration using separate repositories (`ruff-pre-commit`, `mirrors-mypy`, `checkov`) to run checks on staged files.
- Suggested workflow: run `uv run format` before `uv run lint` locally, with all checks enforced in CI.

## Opinions/Guidelines
- Use `ruff` as the unified tool for both formatting and linting (replacing separate tools like `black`, `isort`, and `flake8`).
- Do not use wildcard imports; prefer explicit imports to keep module namespaces clear and predictable.
- Apply trailing commas in multi-line collections and argument lists to improve Git diffs when items are added or reordered.
- Run `uv run format` to normalize code style before running `uv run lint` to catch remaining issues.
- Configure pre-commit hooks so that they operate only on staged files for better performance during development.
- Use `mypy` with strict settings (e.g., `--strict`) for new or critical code paths when static type checking is enabled.
- Ensure that all quality checks (formatting, linting, type checking, and security scans) are mandatory in CI before merging changes.

## Assumptions
- The project uses `uv` as the primary command runner and dependency manager for tasks like formatting and linting.
- `mypy` is available and configured in the environment for static type checking, including strict mode for new code.
- Pre-commit hooks are installed from dedicated third-party hook repositories for `ruff`, `mypy`, and `checkov`.
- Configuration files (such as `pyproject.toml`) provide script/task entries that map directly to `uv run` commands.
- CI pipelines are configured to run the full quality gate suite on every pull request.

## Staleness Indicators
- **MAJOR**: STYLE_8 assumes `[tool.uv.scripts]` is used for defining tasks, but this project currently defines commands under `[project.scripts]` in `pyproject.toml`.
- **MAJOR**: STYLE_8 describes a pre-commit setup with separate `ruff-pre-commit`, `mirrors-mypy`, and `checkov` repositories, while the actual `.pre-commit-config.yaml` uses a simpler `local` hook that runs `uv run lint`.
- **MAJOR**: Extensive guidance on `mypy` (including strict mode, configuration, and hooks) conflicts with the current project, which does not list `mypy` in `pyproject.toml` and does not mention it in `README.md`, `AGENTS.md`, or `docs/to_integrate/linting-guide.md`.
- Example versions (e.g., `ruff` v0.5.5, `mypy` v1.11.0, `checkov` 3.2.144) do not align with this project's actual `pyproject.toml`, which uses `ruff` 0.14.5 and `checkov` >= 3.2.493 and omits `mypy`.
- STYLE_8 describes `uv run format` followed by `uv run lint` as separate steps, but the current `scripts/lint.py` implementation already includes formatting as part of the lint workflow.
- Import ordering and formatting guidance overlaps with existing configuration in `pyproject.toml` (for example, Ruff's configured line length of 100, not 120) and with other style docs.

## Tags
`style`, `tooling`, `ruff`, `mypy`, `checkov`, `uv`, `imports`, `formatting`, `pre-commit`, `ci`, `type-checking`, `security`

## Preliminary Target Docs
Primary integration targets are `docs/code-style-guide.md` (for import ordering and formatting conventions) and `docs/linting-guide.md` (for linting, formatting, and security tooling workflows). Pre-commit and CI workflow details may also inform sections in `README.md` (developer setup) or a dedicated development workflow document such as `docs/development-setup.md`.

## Red Flags
1. **`mypy` not installed**: STYLE_8's strong emphasis on `mypy` (strict mode, hooks, CI) is out of sync with the current project, which does not include `mypy` as a dependency or mention it in any primary docs; a decision is needed on whether to adopt `mypy` or remove/soften this guidance.
2. **Pre-commit configuration mismatch**: The recommended multi-repo pre-commit setup conflicts with the actual `.pre-commit-config.yaml`, which relies on a single `local` hook running `uv run lint`; documentation and configuration must be reconciled to avoid confusion.
3. **Script section mismatch**: The use of `[tool.uv.scripts]` in examples does not match the project's current `[project.scripts]` usage; STYLE_8 should be updated to reflect how `uv` is actually invoked here.
4. **Duplicate tooling documentation**: STYLE_8 substantially overlaps with `docs/to_integrate/linting-guide.md` and the `README.md` Code Quality section; Phase 2 integration should merge these into a single, authoritative description of the tooling stack.
5. **Version drift**: Hard-coded tool versions in STYLE_8 do not match `pyproject.toml` and will quickly become outdated; examples should either be updated or rewritten to be version-agnostic.
6. **Import ordering overlap**: Import ordering guidance duplicates content from STYLE_1 and other style docs; consolidated style documentation should avoid conflicting rules and pick a single source of truth.
7. **Workflow inconsistency**: STYLE_8's narrative of separate `format` and `lint` commands differs from the reality that `uv run lint` (via `scripts/lint.py`) already executes formatting; documentation should clarify that a single command is the canonical workflow.
8. **Missing Ruff config details**: STYLE_8 mentions that Ruff is configured via `pyproject.toml` but does not reflect this repository's actual settings (e.g., 100-character line length); integrated docs should reference the concrete configuration.
9. **`TYPE_CHECKING` imports context**: While TYPE_CHECKING usage is shown, the rationale (avoiding import cycles and runtime costs) is only lightly touched on; integration work should ensure this guidance is connected to broader import and typing patterns from other style docs.
10. **CI integration specifics**: STYLE_8 vaguely recommends adding `uv run lint` to CI without showing concrete CI configuration; this must be coordinated with `docs/to_integrate/git-workflow.md` and the project's actual CI workflows.

## References
- `docs/to_integrate/STYLE_8.md` (source of tooling and workflow guidance)
- `pyproject.toml` (actual configuration: `ruff` 0.14.5, `checkov` constraints, `[project.scripts]` usage, Ruff config such as 100-char line length)
- `.pre-commit-config.yaml` (current pre-commit setup using a `local` hook for `uv run lint`)
- `README.md` (Code Quality section and developer workflow notes)
- `AGENTS.md` (repository-specific guidance on running `uv run pytest` and `uv run lint` after changes)
- `docs/to_integrate/linting-guide.md` (overlapping linting and tooling documentation)
- `docs/to_integrate/STYLE_1.md` (related style and import guidance)
- `scripts/lint.py` (implementation of the `uv run lint` command, including format+lint orchestration)
