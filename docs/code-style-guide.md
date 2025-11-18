## Python Code Style Guide

This document is the canonical reference for Python 3.14+ code style, typing, and tooling for the MCP metadata broker. It complements PEP 8 and the ADR set, and is enforced by the Ruff configuration in `pyproject.toml`.

Key decisions are recorded in:

- `docs/adr/0001-use-python-3.14.md` – Fixes the supported runtime range to Python 3.14.x.
- `docs/adr/0005-standardize-on-ruff.md` – Standardizes on Ruff as the single linting/formatting tool.
- `docs/adr/0006-adopt-uv-mypy-checkov.md` – Aligns the Python tooling stack around `uv` for environment management, Ruff for lint/format, `mypy` for type-checking, and `checkov` for infrastructure-as-code scanning.

### Typing and Type Hints

- Typing is mandatory for all new code: add annotations for function parameters, return types, attributes, and important module-level values.
- In particular, annotate **both parameter types and return types** for all public-facing functions, methods, and APIs (public module functions and methods).
- Always use modern Python 3.14+ syntax for types: built-in generics (`list[int]`, `dict[str, MetadataItem]`) and unions with `|` (for example, `int | None` instead of `Optional[int]`).
- Use `collections.abc` for container interfaces (`Iterable`, `Mapping`, `Sequence`, etc.) when you only need read-only/structural behavior, and concrete built-ins (for example, `dict[str, float]`) for owned or mutated collections.
- Use classes (including `@dataclass`) for structured data shapes that correspond to TypeScript-style "interfaces".
- Prefer `@dataclass` for simple data containers where appropriate.
- Use `TypeAlias` (or `type` aliases in Python 3.14 syntax), `Literal`, and unions of types to model TypeScript-style "type" aliases and unions.
- Use `type` aliases to name common shapes (for example, `type MetadataMap = dict[str, MetadataItem]`). Prefer explicit aliases such as `ProjectId = str` or `ProjectsList = list[Project]` over opaque container types.
- Use standard typing helpers such as `Literal`, `LiteralString`, `TypedDict`, `Protocol`, `runtime_checkable`, and `Self` where they clarify contracts.
- When you cannot express a type precisely, first consider introducing a `Protocol` or ABC capturing just the behaviour you need, or using generics where relationships between parameters and returns matter.
- Define generics using descriptive `TypeVar` names that match the domain (for example, `TInput`, `TOutput`, `TResponse`) rather than single-letter aliases like `T` and `U`.
- Use `Any` sparingly and only at clear boundaries (parsing untyped JSON, opaque plugin configuration, third-party library hooks). Do not silence the type system simply to get a file "passing".
- If you must use `Any`, restrict it to the smallest possible scope and add a brief comment explaining why it is needed and what would have to change to replace it (optionally including a `TODO` with a ticket reference).
- Prefer more precise alternatives to `Any` where possible: `object` for truly opaque values, `Protocol`/ABCs for structural contracts, and generics (`TypeVar`, `TypeVarTuple`, etc.) when relationships between types matter.

#### Local Variable Annotations

- Let type inference handle simple, obviously typed local variables; do **not** add redundant annotations just because you can.
- For example, prefer `count = len(items)` over `count: int = len(items)` when the type is clear from the right-hand side.
- Reserve explicit annotations for locals when they meaningfully clarify intent (for example, complex generics, union-heavy flows, or values whose type is not obvious from the expression).
- Avoid annotating simple locals when the type is immediately evident from the right-hand side expression.

#### Annotation Semantics and Forward References (PEP 649 / 749)

- Python 3.14 uses lazy evaluation of annotations (PEP 649 / 749). Code that only uses annotations for static checking can generally ignore this detail.
- You can reference classes and other types defined later in the module as normal names in most cases; you do not need to quote them solely for forward-reference purposes.
- Forward references in aliases and annotations should use natural names (for example, `ProjectsList = list[Project]`) and avoid quoting purely for ordering reasons; string annotations remain acceptable when they materially simplify circular imports or runtime introspection.
- When writing forward-referencing hints, use natural names (no quoting) in new code unless there is a specific reason to use string annotations.
- There is a dedicated `annotationlib` module for inspecting deferred annotations at runtime; prefer its APIs when you need to read annotations dynamically instead of reaching directly into `__annotations__`.
- If you introspect annotations at runtime (for example, using `typing.get_type_hints` or `annotationlib.get_annotations`), be aware that annotations may not be plain dictionaries of concrete types and should be resolved according to the modern semantics.
- Do not rely on older stringified-annotation behavior (PEP 563). `from __future__ import annotations` should only be used when there is a specific, documented need (for example, shared libraries that must align behavior across multiple runtimes); it is not required for normal application code in this project.

### Naming & Layout

- Follow standard PEP 8 naming rules unless a more specific convention is documented in this guide or an ADR.
- Modules and packages: `snake_case` (for example, `metadata_router_v1`).
- Functions, methods, and local variables: `snake_case`.
- Classes, Pydantic models, Pydantic enums, and exceptions: `PascalCase` (for example, `FetchRequest`, `MetadataItem`, `MetadataError`, `ProjectStatus`). This includes domain services and Pydantic models.
- Constants and other true invariants: `UPPER_SNAKE_CASE` (for example, `MAX_RETRY_ATTEMPTS`).
- Avoid ambiguous one-letter names such as `l`, `O`, and `I`; prefer short but descriptive names even for loop variables.

Layout and vertical spacing:

- Indentation is **4 spaces**; never use tabs.
- The canonical line length is **100 characters**, as configured in Ruff. Older guidance that mentioned 120 characters is superseded by this setting.
- Use 2 blank lines between top-level functions and classes.
- Use 1 blank line between methods in a class.
- Use single blank lines within functions and methods to separate logical sections when it improves readability.

File and directory structure:

- Use `snake_case` for module (file) names and package (directory) names.
- Match a module's name to its primary responsibility (for example, `user_service.py`, `user_profile.py`, `api_client.py`, `user_router.py`).
- In FastAPI-style layouts, keep routers, services, and models organized by responsibility, mirroring patterns such as `app/routes/users.py`, `app/services/user_service.py`, and `app/models/user_profile.py` when introducing new areas.

When modeling shared domain entities and enums across services, prefer shared Pydantic models and enums so that FastAPI routers, scripts, and higher-level tools can rely on a single, type-safe representation (for example, shared `Project`, `ProjectStatus`, or `DesignToken` types). Keep domain-specific type aliases (such as `ProjectId = str`) and enums in central modules where they can be reused consistently across routers and services.

### Imports

- Place imports at the top of the file, after any module docstring and before module-level constants or other top-level definitions.
- Let Ruff manage import ordering, grouping, and deduplication; do not use isort or similar tools.
- The logical grouping Ruff enforces (and that new code should follow) is:
  1. Standard library
  2. External / third-party dependencies
  3. Internal absolute imports from this project
  4. Internal relative imports (for example, `from .submodule import name`)
  5. Type-only imports guarded by `if TYPE_CHECKING:` when needed to avoid circular dependencies.
- When circular dependencies require type-only imports, place them in a guarded block at the end of the import section:

  ```python
  from typing import TYPE_CHECKING

  if TYPE_CHECKING:
      from app.services.mcp_manager import MCPManager  # noqa: F401
      from .types import SomeLocalType  # noqa: F401
  ```

- Do not use wildcard imports (`from module import *`) except in rare, tightly controlled, and well-documented helper modules (for example, test helper re-exports where justified), because they pollute the module namespace and make it harder to trace where names come from.

### Functions and Organization

- Keep functions focused on a single responsibility. Functions should be small and do one thing well.
- Always add type hints for function parameters and return values in new code.
- FastAPI route handlers should be thin: validate input, delegate to services, and translate results to HTTP responses.
- Prefer async functions for I/O-bound work that integrates with FastAPI, and organize asynchronous workflows using `async`/`await` instead of nested callbacks or deeply nested inline logic.
- Prefer simple list/dict comprehensions or small, named helper functions over large inline lambdas or deeply nested inline functions.

### Comments and Docstrings

- Every public module, class, function, and method must have a docstring.
- Use Google-style docstrings consistently for all public APIs; any older guidance about choosing between Google and NumPy styles is superseded by this rule.
- Docstrings should describe what the object does, any important parameters and return values, and exceptions that callers should care about.
- Focus inline comments on explaining *why* the code behaves a certain way rather than restating *what* the code already shows.
- Use inline comments when the intent is not obvious from the code, and keep them short and close to the code they explain.
- Avoid leaving commented-out code in the repository; remove unused code instead of commenting it out.

Inline comments should clarify intent without narrating obvious behaviour. Prefer comments that explain the reasoning, constraints, or trade-offs behind a block of code instead of restating the implementation.

```python
# ✅ Good: explains rationale
# Retry failed requests to handle transient network errors
max_retries = 3

# ❌ Bad: restates what the code already says
# Set max retries to 3
max_retries = 3
```

Use `TODO`, `FIXME`, and `NOTE` prefixes sparingly and keep them actionable. These markers are recognized by most IDEs and should always describe a concrete follow-up.

```python
# TODO: Implement caching layer for metadata fetches
# FIXME: Handle edge case when user is None
# NOTE: Temporary workaround for upstream API limitation
```

### Error Handling

- Prefer domain-specific exception types over generic `Exception`; define custom exceptions by subclassing a relevant built-in base such as `ValueError` or `IOError` when it improves clarity and caller handling.
- Use multiple, specific `except` blocks to handle different error cases rather than a single broad catch-all; avoid bare `except` clauses and avoid `except Exception:` unless you immediately re-raise after logging or attaching context.
- Never silently swallow unexpected exceptions ("Pokémon exception" handling); if you must catch `Exception`, log the error with sufficient context and re-raise so failures are visible to callers and tests.
- Keep exception handling close to the boundary where you can take a meaningful action (for example, translating a validation error to a `400` response or a network failure to a `503` response in FastAPI routers).
- Translate internal errors to appropriate HTTP responses in FastAPI routers, using specific exception types to drive consistent status codes and error payloads.

### FastAPI Architecture and Patterns

- Keep a clear layering between routers (HTTP), services (business logic), and repositories (data access) for all non-trivial features.
- Use Pydantic models for request and response bodies and to validate input at the API boundary.
- Keep FastAPI route handlers thin: validate inputs, delegate to a service, and translate service-level exceptions into `HTTPException` responses.
- Inject dependencies using FastAPI's `Depends` together with `typing.Annotated` type aliases for clarity.
- Avoid leaking HTTP details (such as `Request`, `Response`, or `HTTPException`) into services or repositories.
- Ensure repositories are responsible only for persistence concerns and work with ORM or storage-specific models, not FastAPI request types.
- Use dependency provider functions (for example, `get_db()`, `get_user_repo()`, `get_user_service()`) in dedicated modules (such as `app/core/dependencies.py`) to wire the layers together.
- Keep router modules cohesive and focused on a related set of endpoints while services and repositories model reusable domain behaviour.

### Formatting, Linting, Type Checking, and Security Scanning

- Ruff is the single source of truth for linting and formatting; do not configure Black, isort, flake8, or other overlapping tools. Use `ruff format` for automatic formatting instead of `black`.
- Line length is **100 characters**, as configured in Ruff. This is the canonical project choice and replaces older 120-character guidance from the legacy STYLE_* documents.
- Use **4 spaces** for indentation; never use tabs. `ruff format` will enforce this automatically.
- `ruff format` also manages trailing commas for multi-line collections (lists, dicts, sets) and function definitions. Rely on this behavior so that adding new items or parameters typically changes only a single line in diffs.
- `uv run lint` is the primary entry point for project-wide checks. It runs Ruff linting/formatting and mypy type checking (via the `lint` script in `pyproject.toml`), and may also chain additional tooling (such as security scanning) as the project evolves.
- When you need to run individual tools, prefer the `uv` script aliases defined in `pyproject.toml` (for example, `uv run lint` for the full check suite) instead of calling tools directly so that local and CI behavior stay aligned.
- Use `checkov` (typically via CI or dedicated scripts) to statically scan infrastructure-as-code artefacts (for example, Dockerfiles, Terraform, and configuration files) for security and compliance issues; treat failing checks as build breakers unless explicitly documented otherwise.
- Follow PEP 8-style vertical spacing: use 2 blank lines between top-level functions and classes, 1 blank line between methods in a class, and single blank lines to separate logical sections within a function.

#### Automated Tooling and Hooks

- All quality and security tools are wired through `uv` scripts (see the `[project.scripts]` section in `pyproject.toml`), which act as the single interface for running checks locally and in CI.
- Use `uv run lint` before committing changes to ensure Ruff, mypy, and any configured security checks all pass.
- Pre-commit hooks are configured in `.pre-commit-config.yaml` and installed via `uv run mcp-setup`; they are responsible for running fast, file-scoped checks on staged changes so that most issues are caught before they reach CI.
- The pre-commit configuration is allowed to evolve over time, but it should remain aligned with the `uv` scripts so that running hooks locally provides the same guarantees as running the full `uv run lint` pipeline.

### Testing Conventions

- Use `pytest` for all tests; do not introduce other test runners.
- Name test files `test_*.py` or `*_test.py` and keep them under `tests/`, mirroring the structure of `app/` where practical (for example, `app/core/settings.py` → `tests/core/test_settings.py`).
- Use pytest fixtures for shared setup; keep fixtures small, composable, and focused on a clear responsibility.
- Type annotate tests that encode non-trivial logic or complex data flows so that mypy can catch regressions; lighter typing is acceptable for simple glue tests, but avoid untyped helper utilities.
- Prefer parametrization and fixtures to large, monolithic tests; keep tests readable and focused on a single behaviour.

### Version-Specific Guidance (Python 3.14+)

- Target Python 3.14+ only; do not add compatibility shims, backports, or conditional code paths for older Python versions.
- Always use modern typing syntax:
  - Built-in generics such as `list[int]`, `dict[str, object]`, and `tuple[MetadataItem, ...]`.
  - Union types using `|` (for example, `str | None` instead of `Optional[str]`).
  - Modern `typing` features where they clarify contracts (for example, `Self`, `LiteralString`, `TypeAlias`).
- Do not introduce deprecated typing aliases (for example, `typing.List`, `typing.Dict`, `typing.Optional`) in new code; prefer the built-in and modern spellings instead.
- When you rely on newer typing semantics or behavior that may be non-obvious (for example, lazy annotation evaluation or runtime use of `get_type_hints` in metaprogramming), add a short comment in the relevant module or class summarizing the important implications for maintainers.

### Public vs Internal APIs

- Use a leading underscore for internal functions, classes, and modules that are not part of the public surface (for example, `_internal`, `_helpers`).
- Treat underscore-prefixed modules and packages as internal implementation details that can change without notice.
- For modules that act as a stable public entry point, define `__all__` to expose a curated API surface.
- When a symbol is part of the public API, ensure it is covered by user-facing documentation and tests.
- Avoid breaking public APIs without a documented deprecation path and migration guidance; prefer additive changes and compatibility shims when feasible.

### See also

- `docs/testing-guide.md` – Comprehensive testing patterns and tiers.
- `docs/api.md` – FastAPI-specific API patterns and endpoint guidance.
- `docs/architecture.md` – Overall service and layering architecture.
- `docs/workflow-and-ci.md` – Local workflow, CI, and pre-commit integration.
