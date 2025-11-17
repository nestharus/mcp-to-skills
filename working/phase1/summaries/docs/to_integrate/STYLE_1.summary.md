# STYLE_1.md Summary

## Purpose
Document the comprehensive Python 3.14+ style and typing guide covering mandatory typing, PEP 8 compliance with project-specific deviations, modern type annotation syntax, tooling recommendations, and testing conventions.

## Main Topics
- Mandatory type annotations for all new code using modern Python 3.14 syntax (built-in generics, union types with `|`).
- PEP 8 baseline with 120-character line length (explicit deviation).
- Import organization (stdlib, third-party, local with blank line separators).
- Docstring requirements (Google or NumPy style, project must choose one).
- Python 3.14 lazy annotation evaluation (PEP 649/749) and implications.
- Public vs internal API conventions (`__all__`, leading underscore).
- Tooling stack: formatter (black or ruff), import sorter (isort or ruff), linter (ruff/flake8/pylint), type checker (mypy/pyright/pyre).
- Testing conventions with pytest (AAA pattern, fixture composition, test file naming).
- Avoiding `Any` with justification comments when necessary.
- Version-specific guidance (no compatibility shims, use modern syntax only).

## Opinions/Guidelines
- Type annotations are mandatory for all public APIs and important attributes.
- Use `Any` sparingly with explanatory comments.
- Prefer `Protocol` or ABCs over `Any` for duck-typed contracts.
- Line length is 120 characters (not PEP 8's 79).
- Remove commented-out code rather than leaving it.
- All CI pipelines must run formatter check, linting, type checking, and tests.
- Test files mirror package structure.
- No `from module import *` except in documented, justified cases.

## Assumptions
- Project targets Python 3.14+ exclusively (no backward compatibility needed).
- Developers have chosen one docstring style (Google or NumPy) consistently.
- CI pipeline is configured to enforce all quality gates.
- Type checker is configured with strict settings for new code.
- Lazy annotation evaluation (PEP 649) is the default behavior.

## Staleness Indicators
- References "project should choose" for docstring style and primary linter, suggesting decisions may not be finalized.
- Mentions multiple tool options (black vs ruff, mypy vs pyright vs pyre) without specifying project's actual choices.
- Generic guidance that may need project-specific examples once codebase matures.
- No mention of actual `pyproject.toml` configuration or `ruff.toml` settings.

## Tags
`style`, `typing`, `python314`, `pep8`, `type-hints`, `annotations`, `tooling`, `linting`, `formatting`, `testing`, `pytest`, `docstrings`, `imports`, `code-quality`

## Preliminary Target Docs
Likely integrates into `docs/code-style-guide.md` or similar consolidated style guide. Sections on tooling may feed into `docs/linting-guide.md`. Testing conventions overlap with `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md`.

## Red Flags
1. **Python version conflict**: STYLE_1 targets Python 3.14+, but `README.md` tech stack section may reference 3.12+ in some places—needs reconciliation.
2. **Tooling ambiguity**: STYLE_1 lists multiple options (black OR ruff, mypy OR pyright OR pyre) but `README.md` and `AGENTS.md` only mention Ruff for formatting/linting—clarify project's actual tooling choices.
3. **Type checker gap**: STYLE_1 mandates type checking in CI but `README.md` and `AGENTS.md` don't mention running mypy/pyright—determine if type checking is actually enforced.
4. **Docstring style undecided**: STYLE_1 says "choose Google or NumPy" but doesn't specify which this project uses—audit existing code and document the decision.
5. **Line length consistency**: Verify that `pyproject.toml` and Ruff configuration actually enforce 120-char limit mentioned in STYLE_1.
6. **Import sorting**: STYLE_1 mentions isort or Ruff but `README.md` only mentions Ruff—confirm Ruff handles import sorting.
7. **Testing overlap**: STYLE_1's testing section duplicates content in `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md`—consolidate in Phase 2.
8. **Lazy annotations**: STYLE_1 discusses PEP 649 implications but doesn't provide concrete examples of runtime introspection patterns—may need expansion.

## References
- `docs/to_integrate/STYLE_1.md`
- `README.md` (tooling, Python version)
- `AGENTS.md` (CLI workflows, quality gates)
- `pyproject.toml` (implied, for tool configuration)
- `docs/TEST.md` (testing conventions overlap)
- `docs/TESTING_ARCHITECTURE.md` (testing structure overlap)
