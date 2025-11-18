You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_2.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_2 section pair 2

This file contains one or two `##` sections from docs/to_integrate/STYLE_2.md.

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


--- SOURCE SECTION END ---
