You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_7.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_7 section pair 1

This file contains one or two `##` sections from docs/to_integrate/STYLE_7.md.

> Deprecated: This legacy style guide has been superseded by `docs/code-style-guide.md`.
>
> Do not update this file. See `docs/code-style-guide.md` for the canonical Python 3.14+ style, typing, and tooling standards.
Here is that style guide adapted for Python 3.14, following Pythonic conventions and PEP 8.

## 🐍 Python 3.14 Style Guide (Adapted)

### Inline Comments

Use comments to explain **why**, not **what**. Python comments use the `#` symbol.

```python
# ✅ Good
# Retry failed requests to handle transient network errors
max_retries = 3

# ❌ Bad
# Set max retries to 3
max_retries = 3
```

-----

### TODO Comments

This convention is identical in Python and is recognized by most IDEs.

```python
# TODO: Implement caching for better performance
# FIXME: Handle edge case when user is None
# NOTE: This is a temporary workaround for API limitation
```

-----


--- SOURCE SECTION END ---
