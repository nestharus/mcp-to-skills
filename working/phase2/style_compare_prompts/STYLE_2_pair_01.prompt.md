You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_2.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_2 section pair 1

This file contains one or two `##` sections from docs/to_integrate/STYLE_2.md.

> Deprecated: This legacy style guide has been superseded by `docs/code-style-guide.md`.
>
> Do not update this file. See `docs/code-style-guide.md` for the canonical Python 3.14+ style, typing, and tooling standards.
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


--- SOURCE SECTION END ---
