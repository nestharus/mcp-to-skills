You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_1.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_1 section pair 4

This file contains one or two `##` sections from docs/to_integrate/STYLE_1.md.

## 6. Public vs Internal APIs

* Treat modules/packages with a leading underscore (`_internal`, `_helpers`) as internal implementation details.
* Public API surface:

    * Expose via `__all__` in packages where appropriate.
    * Document in the project’s user-facing docs.
    * Avoid breaking changes without deprecation and a migration path.

---

## 7. Linting, Formatting, and Tooling

Use tools to enforce consistency so developers focus on behaviour, not formatting. ([Real Python][4])

Recommended setup:

* **Formatter**: `black` (or equivalent) with the project’s chosen line length (e.g. 120).
* **Import sorter**: `isort` or `ruff`’s import rules.
* **Linter**: `ruff`, `flake8`, or `pylint` (project chooses one primary linter).
* **Type checker**: `mypy`, `pyright`, or `pyre` (configure strictness incrementally, but bias toward stricter settings for new code).

All CI pipelines should run:

1. Formatter check (or auto-format on commit).
2. Linting.
3. Type checking.
4. Tests.

---


--- SOURCE SECTION END ---
