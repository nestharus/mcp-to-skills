Here’s how the guidance you provided (for TypeScript) can be adapted for **Python 3.14**, taking into account new features of this version (especially around type annotations).

---

## ✅ Good: Explicit return types for public APIs

In Python 3.14, you should annotate public-facing functions (parameters **and** return type). Example:

```python
from typing import List

class Item:
    price: float

def calculate_total(items: List[Item]) -> float:
    return sum(item.price for item in items)
```

---

## ✅ Good: Let inference help for simple internal cases

For local variables in simple contexts where the type is obvious, you can omit explicit annotations:

```python
numbers = [1, 2, 3]
doubled = [n * 2 for n in numbers]
count = len(numbers)
```

Here, adding `: int` to `count` is unnecessary.

---

## ❌ Bad: Unnecessary / overly verbose annotation

Avoid annotating trivial locals just because you can:

```python
# ❌ Bad
count: int = len(items)

# ✅ Better
count = len(items)
```

---

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

## ✅ Recommended Python 3.14 style-guide summary

Putting it all together for Python 3.14:

* Annotate all **public** module functions/methods with parameter and return types.
* Use classes (or `@dataclass`) for data-shapes.
* Use type aliases (`TypeAlias`), `Union`, `Literal`, etc., for unions/intersections.
* For simple local variables inside functions where the type is obvious, skip explicit annotations.
* Write forward-referencing hints naturally (no quotes) when possible.
* Avoid redundant annotations on simple locals.
* If your code inspects annotations at runtime, prefer `annotationlib.get_annotations()` rather than hacking `__annotations__`.

---

If you like, I can **generate a full Python 3.14 style-guide document** (with examples and dos/ don’ts) tailored from your original TypeScript-based guidance.

[1]: https://docs.python.org/3/whatsnew/3.14.html?utm_source=chatgpt.com "What's new in Python 3.14"
[2]: https://realpython.com/python-annotations/?utm_source=chatgpt.com "Python 3.14 Preview: Lazy Annotations"
[3]: https://www.nb-data.com/p/python-314-12-features-you-can-use?utm_source=chatgpt.com "Python 3.14: 12 Features You Can Use Today"
[4]: https://docs.python.org/3/howto/annotations.html?utm_source=chatgpt.com "Annotations Best Practices"
