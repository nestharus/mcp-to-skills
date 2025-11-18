You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_1.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_1 section pair 3

This file contains one or two `##` sections from docs/to_integrate/STYLE_1.md.

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


--- SOURCE SECTION END ---
