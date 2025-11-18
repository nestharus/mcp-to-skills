You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_1.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_1 section pair 6

This file contains one or two `##` sections from docs/to_integrate/STYLE_1.md.

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

--- SOURCE SECTION END ---
