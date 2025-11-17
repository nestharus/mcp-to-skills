## Purpose
Document Python 3.14+ conventions for inline comments (focusing on explaining "why" rather than "what"), structured TODO/FIXME/NOTE markers, and error handling best practices including custom exception types, specific exception handling, and safe propagation/logging of errors.

## Main Topics
- Inline comment conventions that explain rationale, trade-offs, and non-obvious behavior instead of restating code.
- Standardized TODO/FIXME/NOTE comment markers for IDE tooling and code review visibility.
- Custom error classes that inherit from specific built-in exceptions (for example, `ValueError`, `IOError`).
- Specific exception handling with multiple `except` blocks instead of broad catch-alls.
- Avoiding broad "catch all" patterns (e.g., `except Exception:`) that hide real failures.
- Re-raising exceptions with bare `raise` to preserve original traceback when propagating.
- Logging exceptions before re-raising to aid debugging and observability.

## Opinions/Guidelines
- Write comments to capture "why" design decisions were made, when code is intentionally non-obvious, or when there are important invariants or caveats; avoid comments that simply restate the code.
- Use `TODO`, `FIXME`, and `NOTE` prefixes consistently so IDEs and tooling can surface outstanding work and important caveats.
- Define custom exception classes that derive from specific built-ins (e.g., a `ValidationError` that inherits from `ValueError`) rather than using bare `Exception` subclasses.
- Prefer multiple specific `except` clauses over a single broad handler; only use broad handlers at clear process boundaries and always log/re-raise.
- Never silently swallow exceptions (for example, `except Exception: return None`); always either handle them meaningfully, log them, or propagate them.
- When re-raising after logging or cleanup, use `raise` without arguments to keep the original traceback.

## Assumptions
- Developers are using IDEs or tools that recognize `TODO`, `FIXME`, and `NOTE` markers in comments.
- The project has a logging strategy in place (for example, using the standard library `logging` module) for recording exceptions.
- Code targets Python 3.14+ and may use async/await patterns in error handling paths.
- Custom exception classes will be defined in modules that make sense for the domain (for example, shared/core exceptions vs. per-feature exceptions).

## Staleness Indicators
- Examples use generic custom exception names (e.g., `ValidationError`, `NetworkError`) without tying them to this project's actual domain-specific exceptions.
- Error handling guidance is expressed in generic Python terms and does not mention FastAPI-specific mechanisms such as `HTTPException` or global exception handlers.
- The document does not specify where, in this repository's structure, custom exceptions should live (for example, a dedicated `exceptions` module vs. per-feature modules).
- Example snippets use `print()` for error output instead of the project's preferred logging approach.

## Tags
`style`, `comments`, `error-handling`, `exceptions`, `python314`, `best-practices`, `documentation`

## Preliminary Target Docs
Primary integration target is `docs/code-style-guide.md` (overall code style and commenting guidance). Comment conventions and TODO/FIXME/NOTE usage may also be incorporated into developer onboarding or contribution guidelines. Error handling patterns can complement FastAPI-specific guidance in `docs/fastapi-best-practices.md`, especially around API error responses.

## Red Flags
1. **No FastAPI integration**: Guidance is written in framework-agnostic terms and does not reference FastAPI constructs like `HTTPException` or application-level exception handlers; this needs alignment with how errors are actually surfaced in `app/routes/metadata_router_v1.py` and related routers.
2. **Logging vs `print()`**: Examples rely on `print()` for error reporting, which is not appropriate for production services; these should be updated to use the project's logging approach.
3. **Custom exception placement**: The document does not specify where custom exceptions should be defined (for example, a shared `app/core/exceptions.py` module vs. per-feature exceptions); the project should standardize on a location and update references.
4. **Overlap with testing docs**: Error handling and custom exception patterns have implications for tests and fixtures, which may overlap with `docs/TEST.md` and `docs/to_integrate/TEST_*.md`; coordination is needed when integrating.
5. **Comment density guidance**: There is no explicit guidance on when not to comment (i.e., preferring self-documenting code) or how to avoid over-commenting; this may need to be clarified based on team preferences.
6. **Docstrings vs comments**: The relationship between inline comments and docstrings (outlined in STYLE_1) is not clarified; consolidated style docs should ensure these are consistent and non-contradictory.

## References
- `docs/to_integrate/STYLE_7.md` (source of comment and error handling guidance)
- `docs/to_integrate/STYLE_1.md` (related docstring and general style conventions)
- `docs/to_integrate/fastapi-best-practices.md` (potential integration point for API error handling)
- `app/routes/metadata_router_v1.py` (actual error handling patterns in FastAPI routers)
- `app/contracts/metadata_contract.py` (potential location for domain-specific validation errors)
