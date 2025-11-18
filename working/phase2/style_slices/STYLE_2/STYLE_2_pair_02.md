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

