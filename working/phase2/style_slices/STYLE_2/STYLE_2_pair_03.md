# STYLE_2 section pair 3

This file contains one or two `##` sections from docs/to_integrate/STYLE_2.md.

## Interfaces vs Types — Python equivalent

In TypeScript you distinguish `interface` (object shapes) from `type` (unions/intersections). In Python:

* Use a `@dataclass` or class for structured data shapes.
* Use `TypeAlias`, `Union`, `Literal`, etc., for aliasing/unions/intersections.

```python
from dataclasses import dataclass
from typing import TypeAlias, Literal, Union

@dataclass
class User:
    id: int
    name: str

Status: TypeAlias = Literal['active', 'inactive', 'pending']
Result: TypeAlias = Union[Success, Error]  # assuming Success, Error are classes
```

---

## 📌 Python 3.14-specific updates for type annotations

Because you specified Python 3.14, here are key changes that affect how you write/type-hint code:

* In Python 3.14, **deferred evaluation (lazy evaluation) of annotations** is the default. ([Python documentation][1])

    * That means you no longer *need* `from __future__ import annotations` just to enable forward references; the runtime will not evaluate the annotation expression immediately. ([Real Python][2])
    * Forward references, circular references become easier to handle (no need to wrap types in quotes just for that reason). ([Nb Data][3])
* There is a new module `annotationlib` (introduced in 3.14) which gives APIs like `annotationlib.get_annotations()` to inspect deferred annotations. ([Python documentation][4])

**Implication for your style guide:**

* Continue to annotate public APIs (parameters + return type) as usual.
* You can write type hints referencing classes defined later in the module *without* quoting them (in many cases).
* You don’t need to use redundant `from __future__ import annotations` for forward references (though it’s still supported).
* If your codebase does runtime introspection of annotations, be aware of the new `annotationlib` API.

---

