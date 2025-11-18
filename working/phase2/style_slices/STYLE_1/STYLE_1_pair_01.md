# STYLE_1 section pair 1

This file contains one or two `##` sections from docs/to_integrate/STYLE_1.md.

> Deprecated: This legacy style guide has been superseded by `docs/code-style-guide.md`.
>
> Do not update this file. See `docs/code-style-guide.md` for the canonical Python 3.14+ style, typing, and tooling standards.

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

