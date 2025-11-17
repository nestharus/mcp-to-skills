# STYLE_2.md Summary

## Purpose
Provide focused guidance on type annotation best practices for Python 3.14, emphasizing when to use explicit annotations versus type inference, and how to leverage Python 3.14's deferred annotation evaluation features.

## Main Topics
- Explicit return type annotations for all public APIs (functions, methods).
- Type inference for simple internal cases (local variables with obvious types).
- Avoiding unnecessary verbose annotations on trivial locals.
- Python 3.14 deferred (lazy) evaluation of annotations as default behavior.
- Forward references and circular references without string quotes.
- `annotationlib` module for runtime annotation introspection.
- Interfaces vs types in Python: dataclasses for shapes, `TypeAlias`/`Union`/`Literal` for unions.
- When to omit `from __future__ import annotations` in Python 3.14+ projects.

## Opinions/Guidelines
- Always annotate public API parameters and return types.
- Skip annotations on trivial local variables where the type is obvious (e.g., `count = len(items)`).
- Use dataclasses or classes for structured data shapes.
- Use `TypeAlias`, `Union`, and `Literal` for type aliases and unions.
- Write forward-referencing hints naturally without quotes in Python 3.14.
- Prefer `annotationlib.get_annotations()` over manually poking `__annotations__` for runtime introspection.
- `from __future__ import annotations` is generally unnecessary in 3.14-only projects.

## Assumptions
- Project targets Python 3.14+ exclusively.
- Developers understand the difference between static type checking and runtime introspection.
- Code does not rely on stringified annotations semantics (PEP 563).
- Lazy annotation evaluation (PEP 649) is the default and understood by the team.

## Staleness Indicators
- Adapted from TypeScript guidance, so some examples may feel like direct translations rather than idiomatic Python.
- Mentions "if you like, I can generate a full Python 3.14 style-guide document" suggesting this is a draft or partial conversion.
- No concrete examples of `annotationlib` usage for runtime introspection.
- Lacks project-specific examples from the actual codebase.

## Tags
`style`, `typing`, `python314`, `pep8`, `type-hints`, `annotations`, `type-inference`, `lazy-annotations`, `pep649`, `annotationlib`, `forward-references`, `type-alias`

## Preliminary Target Docs
Integrates into `docs/code-style-guide.md` alongside `STYLE_1.md` content. The annotation best practices section complements STYLE_1's comprehensive typing rules.

## Red Flags
1. **Overlap with STYLE_1**: Significant content duplication with `docs/to_integrate/STYLE_1.md` on typing, annotations, and Python 3.14 features—consolidate in Phase 2.
2. **Draft status**: Document appears to be a conversion/adaptation rather than finalized guidance ("if you like, I can generate...").
3. **Missing examples**: No concrete examples of `annotationlib.get_annotations()` usage or runtime introspection patterns.
4. **TypeScript heritage**: Some phrasing suggests direct translation from TypeScript docs rather than Python-native guidance.
5. **Incomplete coverage**: Focuses narrowly on annotation decisions without broader style context covered in STYLE_1.
6. **No conflict with existing docs**: Unlike STYLE_1, doesn't introduce tooling or conventions that contradict `README.md`/`AGENTS.md`.

## References
- `docs/to_integrate/STYLE_2.md`
- `docs/to_integrate/STYLE_1.md` (overlapping content)
- Python 3.14 documentation (PEP 649, `annotationlib`)
- `README.md` (Python version)
