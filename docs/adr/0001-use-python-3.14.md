# ADR 0001: Use Python 3.14+

## Context

The project increasingly relies on modern Python features, including improved type hinting, async capabilities, and performance optimizations that are best supported on recent Python versions. Maintaining compatibility with older Python versions (e.g., 3.8–3.13) increases testing and support burden without clear benefit for the intended deployment environments.

## Decision

Set the project’s minimum supported Python version to 3.14 or higher by configuring `project.requires-python = ">=3.14"` in `pyproject.toml` and aligning tooling and CI to use Python 3.14+. Older Python versions are considered unsupported.

## Consequences

- Enables use of the latest typing improvements and language features without guards or backports.
- Simplifies dependency management by targeting a single modern runtime.
- Requires contributors and CI to run Python 3.14+, which may necessitate environment upgrades.
- Reduces the need for conditional code paths and compatibility shims.

## References

- `pyproject.toml` (Python version and tool configuration)
- `docs/code-style-guide.md` (typing and style expectations)
- CI workflows under `.github/workflows/`
