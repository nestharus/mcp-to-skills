# STYLE_5.md Summary

## Purpose
Document function design principles, file and directory naming conventions, and async/await patterns for Python/FastAPI projects, with emphasis on single-responsibility functions, thin route handlers, and idiomatic async code.

## Main Topics
- Class and data model naming (PascalCase for classes, Pydantic models, and domain services).
- File and directory naming (snake_case for modules and packages, names reflecting primary responsibility).
- Function design: small, single-responsibility functions with clear type hints.
- FastAPI route handlers that remain thin and delegate to service functions.
- Callbacks and inline functions (preference for comprehensions and named helpers over complex lambdas).
- Async/await usage for clear control flow instead of callback-style patterns.
- Example FastAPI project layout separating routes, services, and models.

## Opinions/Guidelines
- Functions should do one thing well and have clear inputs/outputs.
- Route handlers must be thin: avoid embedding business logic, validation, or persistence concerns directly in handlers.
- Prefer named helper functions or comprehensions over deeply nested or opaque lambdas.
- Use async/await consistently rather than callback-heavy patterns.
- File names should align with the primary concept they implement (for example, `user_service.py` for `UserService`).
- Avoid deeply nested control flow; refactor into smaller helpers when complexity grows.

## Assumptions
- The project uses FastAPI with async route handlers across the HTTP layer.
- A service layer exists (or will exist) to encapsulate business logic away from routers.
- Developers are comfortable with the single-responsibility principle and basic refactoring.
- Linting tools enforce function complexity limits (for example, max complexity or max lines per function).
- The team has or will adopt a consistent project layout for routes, services, and models.

## Staleness Indicators
- Example layout references modules like `api/routes/users.py`, while this project uses `app/routes/metadata_router_v1.py` and related MCP-specific routes.
- The document assumes a mature service layer (`app.services.*`) but `app/services/mcp_manager.py` is still a placeholder and is not wired into the router.
- Does not discuss current async usage in this codebase, where route handlers are `async def` but do not yet delegate to async services.
- Provides generic examples rather than concrete ones using the MCP metadata domain.

## Tags
`style`, `functions`, `async`, `await`, `fastapi`, `route-handlers`, `services`, `single-responsibility`, `naming`, `files`, `directories`, `callbacks`, `lambdas`

## Preliminary Target Docs
Most of this guidance likely feeds into a consolidated `docs/code-style-guide.md` (functions and file naming sections) or a FastAPI-specific style guide such as `docs/fastapi-patterns.md`. The async/await and thin-handler patterns also overlap with sections in `docs/to_integrate/fastapi-best-practices.md` and `docs/to_integrate/api-patterns-guide.md`.

## Red Flags
1. **Project structure mismatch**: The sample project layout (`api/routes/users.py`) does not match this repository, which uses `app/routes/metadata_router_v1.py` and MCP-focused services; examples should be updated to use the actual module structure.
2. **Service layer not integrated**: STYLE_5 assumes thin route handlers delegating to services, but `app/routes/metadata_router_v1.py` currently contains hardcoded logic and does not call `app/services/mcp_manager.py`, so the pattern is aspirational.
3. **Overlap with STYLE_6**: Function design and route handler patterns are repeated in STYLE_6's router sections; these should be consolidated into a single architecture/style document.
4. **Overlap with api-patterns-guide**: The recommendations for thin handlers and service delegation overlap heavily with `docs/to_integrate/api-patterns-guide.md` (especially sections on routers and services).
5. **Overlap with fastapi-best-practices**: Async/await and concurrency guidance overlaps with `docs/to_integrate/fastapi-best-practices.md`; duplication should be reduced.
6. **Missing complexity enforcement details**: Suggests small functions but does not specify how tools (for example, Ruff, pylint) enforce max complexity or lines; should be aligned with `pyproject.toml`.
7. **Callback section relevance**: Emphasizes callback-style patterns that are less common in idiomatic Python FastAPI code; this section may be de-emphasized or simplified.
8. **File naming vs router content**: Recommends one responsibility per file, but `metadata_router_v1.py` contains multiple route functions; expectations for router modules should be clarified.

## References
- `docs/to_integrate/STYLE_5.md` (source document).
- `working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md` (overlapping naming and style guidance).
- `docs/to_integrate/api-patterns-guide.md` (route/service separation patterns).
- `docs/to_integrate/fastapi-best-practices.md` (async/await and concurrency advice).
- `app/routes/metadata_router_v1.py` (current router implementation with hardcoded logic).
- `app/services/mcp_manager.py` (placeholder service referenced by the style guide).
- `pyproject.toml` (implied, for complexity and lint configuration).
