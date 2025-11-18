You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_1.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_1 section pair 5

This file contains one or two `##` sections from docs/to_integrate/STYLE_1.md.

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


--- SOURCE SECTION END ---
