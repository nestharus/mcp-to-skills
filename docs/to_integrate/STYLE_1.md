````markdown
# Python 3.14+ Style & Typing Guide

This project targets **Python 3.14+** only. Assume a modern type system, lazy annotation semantics (PEP 649), and no need for pre-3.10 compatibility. :contentReference[oaicite:0]{index=0}

Baseline: follow **PEP 8 – Style Guide for Python Code** and **PEP 484 – Type Hints**, with the project-specific rules below. :contentReference[oaicite:1]{index=1}

---

## 1. Typing Is Mandatory

### 1.1 Always Use Type Annotations

- All new code must be fully typed: function parameters, return types, and important module/class attributes.
- Use the standard `typing` module and built-in generic types (e.g. `list[int]`, `dict[str, Any]`) instead of `typing.List`, `typing.Dict`, etc. :contentReference[oaicite:2]{index=2}
- Prefer precise types over broad ones.

```python
from collections.abc import Mapping, Sequence
from typing import Any

def normalize_scores(scores: Mapping[str, float]) -> dict[str, float]:
    [ELIDED]
````

### 1.2 Use `Any` Sparingly

* `Any` is allowed but should be **rare**.
* When you use `Any`, add a short comment explaining why it is necessary.

```python
from typing import Any

def load_plugin(config: dict[str, Any]) -> Plugin:
    # `config` is deserialized user input; schema varies per plugin.
    [ELIDED]
```

Better alternatives to `Any`:

* `object` when you truly only treat values opaquely (no attribute access, no assumptions).
* `Protocol` or ABCs when you need “duck-typed” structural contracts.
* Generics (`TypeVar`, `TypeVarTuple`, etc.) when the relationship between types matters. ([Python documentation][1])

---

## 2. Naming & Layout

Follow PEP 8 naming rules. ([Python documentation][2])

* Functions, methods, variables: `snake_case`
* Classes, exceptions: `PascalCase`
* Constants: `UPPER_SNAKE_CASE`
* Avoid ambiguous one-letter names (`l`, `O`, `I`).

Formatting:

* Indentation: **4 spaces** (no tabs).
* Line length: project limit is **120 characters** (PEP 8 recommends 79; we intentionally deviate here).
* Blank lines:

    * 2 blank lines between top-level functions and classes.
    * 1 blank line between methods in a class.

---

## 3. Imports

* Imports go at the top of the file, after the module docstring and before globals/constants. ([Python documentation][2])
* Group imports with a blank line between groups:

    1. Standard library
    2. Third-party
    3. Local application / project

Example:

```python
"""High-level orchestration for data pipeline."""

from __future__ import annotations  # Only if you explicitly need legacy behaviour

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

import httpx

from .config import PipelineConfig
from .logging import get_logger
```

* Do not use `from module import *` except in controlled, documented cases (e.g., test helpers where explicitly justified).

---

## 4. Comments & Docstrings

* Every public module, class, function, and method must have a docstring.
* Use a consistent docstring style (Google or NumPy); the project should choose one and stick to it.
* Docstrings should describe:

    * What the object does.
    * Important parameters and return values.
    * Exceptions that callers should care about.

Example (Google style):

```python
def fetch_user(user_id: str) -> User:
    """Fetch a user by ID.

    Args:
        user_id: External user identifier.

    Returns:
        The user instance.

    Raises:
        UserNotFoundError: If no user exists with the given ID.
    """
    [ELIDED]
```

Inline comments:

* Use when the intention isn’t obvious from the code.
* Keep them short and focused on “why”, not “what”.
* Remove commented-out code rather than leaving it in the file.

---

## 5. Type Hinting Details (Python 3.14+)

### 5.1 Modern Syntax Only

Since we target 3.14+, always use modern syntax: ([Python documentation][2])

* Built-in generics:

  ```python
  list[int]
  dict[str, float]
  tuple[int, str]
  ```

* Union types:

  ```python
  int | None          # instead of Optional[int]
  int | str | bytes   # instead of Union[int, str, bytes]
  ```

* Use `collections.abc` for generic container interfaces:

  ```python
  from collections.abc import Iterable, Mapping

  def dump(data: Mapping[str, object]) -> str:
      [ELIDED]
  ```

### 5.2 Optional, Literal, Self, etc.

Use the standard typing constructs: ([Python documentation][1])

* Optional: `T | None`
* Literal, LiteralString, TypedDict, Protocol, runtime_checkable, Self, etc., where appropriate.

```python
from typing import Literal, Self

Status = Literal["pending", "running", "done"]

class Job:
    def start(self) -> Self:
        [ELIDED]
```

### 5.3 Annotations Semantics (PEP 649 / 749)

Python 3.14 uses **lazy (deferred) evaluation of annotations** by default (PEP 649 / PEP 749). ([Python Enhancement Proposals (PEPs)][3])

Guidance:

* Code that only uses annotations for static checking can ignore this.
* If you introspect annotations at runtime (e.g., with `typing.get_type_hints`), read the PEP 649 behaviour and handle lazy evaluation correctly (avoid assuming annotations are plain dicts of concrete types).
* New code should **not rely** on stringified annotations semantics (PEP 563).

Use `from __future__ import annotations` only if you have a specific, documented reason (e.g., aligning behaviour for a shared library that still supports older interpreters). In a 3.14-only project, it should generally be unnecessary and may be removed over time as the ecosystem stabilises around PEP 649.

---

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

## 8. Avoiding Untyped or Loosely Typed Code

Do **not** silence the type system just to get a file “passing”.

If you cannot express a type precisely:

* Consider:

    * Introducing a `Protocol` or ABC representing the subset of behaviour you use.
    * Using generics where relationships between parameters and returns matter.
* If you must use `Any`:

    * Restrict it to the smallest scope possible.
    * Add a brief comment:

        * Why `Any` is needed.
        * What would need to change to replace it later.
    * Optionally, add a `# TODO` with a ticket reference.

```python
from typing import Any

def call_untyped_plugin(plugin: Any, payload: dict[str, object]) -> dict[str, object]:
    # TODO(PROJ-123): replace `Any` with PluginProtocol once legacy plugins are migrated.
    return plugin.handle(payload)
```

---

## 9. Testing Conventions

* Use `pytest`.
* Test files should be named `test_*.py` or `*_test.py`.
* Mirror the package structure:

    * `src/my_pkg/foo.py` → `tests/my_pkg/test_foo.py`
* Use pytest fixtures for shared setup; keep them small and composable.
* Typing in tests:

    * Type annotate tests that encode non-trivial logic.
    * Allow lighter typing for simple “glue” tests, but avoid untyped helper utilities.

---

## 10. Version-Specific Guidance (Python 3.14+ Only)

Given the minimum version is 3.14:

* Always use:

    * Built-in generics: `list[int]`, `dict[str, object]`, etc.
    * `|` union syntax.
    * Modern `typing` features (e.g., `Self`, `LiteralString`, `TypeAlias`).
* Do not:

    * Add compatibility shims for older Python versions.
    * Use deprecated aliases (`typing.List`, `typing.Dict`, etc.) in new code.
* When using new typing features or semantics (e.g., relying on lazy annotations for metaprogramming), include a short comment in the relevant module or class summarising any non-obvious implications.

---

This document should be kept in the repository (e.g., `docs/python-style-guide.md`) and updated as the project’s tooling, Python versions, or conventions evolve.

```
::contentReference[oaicite:10]{index=10}
```

[1]: https://docs.python.org/3/library/typing.html?utm_source=chatgpt.com "typing — Support for type hints"
[2]: https://docs.python.org/3/whatsnew/3.11.html?utm_source=chatgpt.com "What's New In Python 3.11"
[3]: https://peps.python.org/pep-0749/?utm_source=chatgpt.com "PEP 749 – Implementing PEP 649"
[4]: https://realpython.com/python-news-may-2024/?utm_source=chatgpt.com "Python News: What's New From May 2024"
