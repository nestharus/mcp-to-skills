# ADR 0005: Standardize on Ruff for Linting and Formatting

## Context

Historically, Python projects often used a combination of tools such as Black, isort, and flake8 for formatting and linting. Maintaining multiple tools and configurations increases complexity and can lead to inconsistent results. Ruff provides fast, unified linting and formatting with good support for modern Python versions.

## Decision

- Use Ruff as the primary tool for linting and formatting Python code.
- Prefer `ruff check` (optionally with `--fix`) for linting and `ruff format` for code formatting.
- Configure Ruff in `pyproject.toml` under `[tool.ruff]` and related sections.
- Update pre-commit hooks to run Ruff instead of overlapping tools like flake8, isort, or Black.

## Consequences

- Simplifies the toolchain and reduces configuration drift.
- Speeds up lint and format runs locally and in CI.
- May require minor style adjustments to conform to Ruff’s formatting rules and enabled lint rules.

## References

- `pyproject.toml` (Ruff configuration)
- `.pre-commit-config.yaml` (Ruff hooks)
- `docs/code-style-guide.md` and `docs/workflow-and-ci.md`
