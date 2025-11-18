# STYLE issues plan for docs/to_integrate/STYLE_7.md

This plan is generated from `issues_index.csv` and is scoped to `docs/to_integrate/STYLE_7.md`.

## Relevant issues

| id | doc | line_no | description_text | issue_type | classification | classification_ref | notes |
|---|---|---|---|---|---|---|---|
| ISS-0124 | working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md | 40 | **No FastAPI integration**: Guidance is written in framework-agnostic terms and does not reference FastAPI constructs like `HTTPException` or application-level exception handlers; this needs alignment with how errors are actually surfaced in `app/routes/metadata_router_v1.py` and related routers. | Gaps | CONFLICT | Code Standards & Architecture | STYLE_7’s framework-agnostic error guidance still needs to be reconciled with concrete FastAPI patterns (HTTPException, router-level handlers) and aligned with docs/api.md and app/routes/metadata_router_v1.py behaviour during the Code Standards & Architecture phase. |
| ISS-0125 | working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md | 41 | **Logging vs `print()`**: Examples rely on `print()` for error reporting, which is not appropriate for production services; these should be updated to use the project's logging approach. | Health | RESOLVED | Migration §2 (STYLE_* → docs/code-style-guide.md, logging/error-handling) & §4 (STYLE-LOGGING red flag) | Logging vs print() is explicitly called out as a STYLE red flag and will be unified into a single logging/error-handling subsection in docs/code-style-guide.md, coordinated with centralized error handling in app/core/errors.py instead of print-based examples. |
| ISS-0126 | working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md | 42 | **Custom exception placement**: The document does not specify where custom exceptions should be defined (for example, a shared `app/core/exceptions.py` module vs. per-feature exceptions); the project should standardize on a location and update references. | Code Standards & Architecture | RESOLVED | Migration §3 (app/core/errors.py new file) | The non-doc migration matrix introduces app/core/errors.py as the centralized location for error types and HTTP mappings, which standardizes where custom exceptions live and how they are referenced from style and API docs. |
| ISS-0127 | working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md | 43 | **Overlap with testing docs**: Error handling and custom exception patterns have implications for tests and fixtures, which may overlap with `docs/TEST.md` and `docs/to_integrate/TEST_*.md`; coordination is needed when integrating. | Conflicts | CONFLICT | Testing & E2E | Error-handling and custom exception patterns from STYLE_7 will affect tests and fixtures and must be coordinated with docs/testing-guide.md and existing TEST_* content during the Testing & E2E phase to avoid conflicting guidance across testing docs. |
| ISS-0128 | working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md | 44 | **Comment density guidance**: There is no explicit guidance on when not to comment (i.e., preferring self-documenting code) or how to avoid over-commenting; this may need to be clarified based on team preferences. | Gaps | CONFLICT | Code Standards & Architecture | Comment-density expectations (when not to comment and preferring self-documenting code) are not yet spelled out; they need to be defined and integrated into docs/code-style-guide.md when consolidating STYLE_7-era commentary guidance. |
| ISS-0129 | working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md | 45 | **Docstrings vs comments**: The relationship between inline comments and docstrings (outlined in STYLE_1) is not clarified; consolidated style docs should ensure these are consistent and non-contradictory. | Duplicates | CONFLICT | Code Standards & Architecture | The relationship between inline comments and docstrings, split today between STYLE_1 and STYLE_7, must be explicitly harmonized in the unified docs/code-style-guide.md to prevent overlapping or contradictory rules. |

## Instructions

For each issue listed above:

- Open `docs/to_integrate/STYLE_7.md`.
- Confirm whether the described problem is still present.
- If it is still present, edit `docs/to_integrate/STYLE_7.md` to resolve it, aligning with current ADRs, `pyproject.toml`, and the consolidated `docs/code-style-guide.md`.
- If it has already been resolved, ensure the intent of the fix remains clear and that no contradictory guidance remains.

Focus only on the concerns described in these issues; do not introduce unrelated changes.
