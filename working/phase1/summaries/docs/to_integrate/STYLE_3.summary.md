# STYLE_3.md Summary

## Purpose
Document FastAPI-specific patterns and best practices for Python 3.14, covering descriptive generic naming, type aliases, centralized error handling, and service layer architecture.

## Main Topics
- Descriptive `TypeVar` naming conventions (e.g., `TInput`, `TOutput`, `TModel` rather than `T`, `U`).
- Type alias syntax using the `type` statement or `TypeAlias` annotation.
- Python 3.14 lazy annotation evaluation enabling natural forward references.
- Project-specific error model: `ErrorCode` enum (`StrEnum`) and `AppError` (`BaseModel`).
- Centralized exception handling in FastAPI with custom `AppException` and global handler.
- Service layer pattern ("query function" analogue) for business logic separation.
- Endpoint wiring with Pydantic validation and response models.
- Async endpoint and service patterns for I/O-bound operations.
- FastAPI project structure recommendations (routers, services, schemas).
- Mapping TypeScript patterns to Python/FastAPI equivalents.

## Opinions/Guidelines
- Use descriptive `TypeVar` names like `TInput`/`TOutput` instead of single letters to clarify intent.
- Prefer `type Alias = ...` or `Alias: TypeAlias = ...` for readability.
- Maintain shared error model (`ErrorCode` + `AppError`) across all endpoints.
- Use centralized exception handling via FastAPI exception handlers raising a project-specific `AppException`.
- Separate business logic into service layer functions that return typed models or raise exceptions.
- Keep endpoints as thin delegators over service functions.
- Use `async` for I/O-bound operations and avoid blocking the event loop.
- Leverage Pydantic + FastAPI for parameter validation and response modeling.
- Organize project into routers, services, and schemas modules for scalability.

## Assumptions
- Project uses FastAPI as the web framework.
- Pydantic v2 handles data validation and serialization.
- Developers understand async/await patterns and event loop implications.
- Service layer pattern is preferred over fat controllers.
- Centralized error handling is established project-wide.
- Python 3.14 lazy annotations are understood and leveraged.

## Staleness Indicators
- Adapted from TypeScript guidance with explicit mapping table, suggesting conversion rather than native Python documentation.
- Mentions "if you'd like, I can produce a complete markdown version" indicating draft status.
- Generic examples without project-specific context from the actual codebase.
- No mention of existing `app/` structure, routers, or services in this project.
- `ErrorCode` and `AppError` examples may not match actual implementation in `app/contracts/metadata_contract.py`.

## Tags
`style`, `fastapi`, `architecture`, `api-patterns`, `error-handling`, `generics`, `type-alias`, `python314`, `pep8`, `pydantic`, `async`, `service-layer`, `exception-handling`, `typing`

## Preliminary Target Docs
Likely integrates into `docs/fastapi-patterns.md` or `docs/api-patterns-guide.md`. Error handling sections may feed into `docs/error-handling-guide.md`. Generic naming conventions belong in `docs/code-style-guide.md` alongside STYLE_1 and STYLE_2 content.

## Red Flags
1. **Overlap with to_integrate docs**: Content overlaps with `docs/to_integrate/api-patterns-guide.md` and `docs/to_integrate/fastapi-best-practices.md`—consolidate in Phase 2.
2. **Draft status**: Document appears to be a conversion from TypeScript guidance rather than finalized Python/FastAPI documentation.
3. **ErrorCode mismatch**: Example `ErrorCode` enum may not match actual error handling in `app/contracts/metadata_contract.py` or `app/routes/metadata_router_v1.py`—audit existing code.
4. **Service layer gap**: No mention of existing `app/services/mcp_manager.py` or how it fits the service layer pattern described.
5. **Router structure**: Doesn't reference existing `app/routes/metadata_router_v1.py` or explain how it aligns with recommended patterns.
6. **Async patterns**: No mention of existing async patterns in `app/main.py` or `app/services/mcp_manager.py`—verify consistency.
7. **TypeScript mapping table**: Mapping table is useful but may confuse Python-only developers—consider removing or moving to an appendix.
8. **Generic naming overlap**: `TypeVar` naming guidance duplicates STYLE_1 and STYLE_2—consolidate in single style guide.
9. **README/AGENTS alignment**: No direct conflicts with the tooling/workflow guidance in `README.md` or `AGENTS.md`, but FastAPI/testing guidance here must stay synchronized with those docs.

## References
- `docs/to_integrate/STYLE_3.md`
- `docs/to_integrate/STYLE_1.md` (TypeVar naming overlap)
- `docs/to_integrate/api-patterns-guide.md` (likely overlap)
- `docs/to_integrate/fastapi-best-practices.md` (likely overlap)
- `app/contracts/metadata_contract.py` (error model comparison)
- `app/routes/metadata_router_v1.py` (router pattern comparison)
- `app/services/mcp_manager.py` (service layer comparison)
- `app/main.py` (exception handler comparison)
