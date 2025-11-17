## Purpose

- Define FastAPI backend API patterns that align cleanly with a frontend using TanStack Query, emphasizing consistent response shapes, strong typing, and predictable behavior for queries and mutations.

## Main Topics

- Tech stack integration: FastAPI, Pydantic v2, SQLAlchemy (or similar), and shared types with a TypeScript/TanStack Query frontend.
- Core principles: plain resources instead of envelope responses, a single `AppError` error shape, strict separation of domain logic from HTTP concerns, and Pydantic models everywhere.
- Project structure: modular `APIRouter` instances per bounded context, versioned API packages (e.g., `/api/v1`), and thin route handlers delegating to services.
- Schemas and generics: `Paginated[T]`, `ErrorCode`, `AppError`, and typed create/update payload models to standardize responses and payloads.
- Error handling: domain-level exceptions with global exception handlers that map them to `AppError` HTTP responses in a consistent format.
- Pagination and infinite scroll: query parameters like `page`/`pageSize` and a `Paginated[T]` wrapper for list endpoints.
- Mutations: POST/PATCH/DELETE operations with typed payloads, clear status codes, and predictable JSON responses.
- Dependency injection: layering routers → services → repositories via FastAPI `Depends`, keeping endpoints thin and testable.
- API versioning and stability: `/api/v1` prefixes, additive changes, and avoiding breaking changes.
- Testing patterns: `TestClient`, dependency overrides, and alignment of backend behavior with documented contracts.

## Opinions/Guidelines

- Return plain JSON resources (objects/arrays) instead of wrapping everything in response envelopes.
- Use a single, consistent `AppError` structure for all non-2xx responses so the frontend can handle errors uniformly.
- Keep domain logic in services/repositories and treat routers as thin HTTP adapters that translate inputs/outputs and errors.
- Use Pydantic models for all request and response bodies; avoid untyped `dict` payloads and responses.
- Organize routes by bounded context with dedicated `APIRouter` modules and apply versioned prefixes (`/api/v1/...`).
- Design endpoints and response shapes to match TanStack Query usage: stable URLs, clear cache keys, and standard HTTP codes.
- Use generic types such as `Paginated[T]` and shared error models to keep API behavior consistent across endpoints.
- Implement global exception handlers that translate domain exceptions into `AppError` responses with well-known error codes.
- Use query params `page` and `pageSize` for pagination and always return pagination metadata along with data lists.
- Prefer POST for create (201), PATCH for partial updates (200), and DELETE for deletes (204) with minimal/no response body.
- Build a layered DI chain (`get_db` → repositories → services) so each layer is independently testable.
- Version APIs via path prefixes and avoid breaking changes; introduce new endpoints or versions instead.
- Test endpoints using `TestClient`, dependency overrides, and fixtures that align with the documented API patterns.

## Assumptions

- Backend is implemented with FastAPI, Pydantic v2, and an ORM such as SQLAlchemy.
- Frontend uses TanStack Query and relies on stable URLs, predictable HTTP status codes, and consistent JSON shapes.
- Shared TypeScript types exist or will exist (`Project`, `Paginated<T>`, `AppError`, `ErrorCode`, etc.) for strong typing across the stack.
- The team has adopted a layered architecture (routers → services → repositories) and wants strict separation of concerns.
- Python 3.10+ syntax (e.g., `str | None`) and Pydantic v2 features are available.

## Staleness Indicators

- Assumes database/ORM layers and repository patterns that are not present in the current project (no DB dependencies in `pyproject.toml`).
- Describes a mature layered architecture while the codebase still uses hardcoded responses and minimal DI (e.g., `metadata_router_v1` and `mcp_manager`).
- Assumes tight frontend integration (TanStack Query, shared TS types) that does not currently exist in this backend-only repo.
- References authentication patterns (e.g., OAuth2) and richer domain models than the current MCP metadata domain.
- Example domains (`Project`, `User`) diverge from actual contracts (`MetadataItem`, `FetchRequest`), so names and types will need adaptation.

## Tags

- architecture
- fastapi
- api-patterns
- routers
- schemas
- error-handling
- pagination
- mutations
- dependency-injection
- versioning
- testing
- pydantic
- tanstack-query
- frontend-alignment

## Preliminary Target Docs

- Likely to become `docs/api-patterns-guide.md` or a section within a broader FastAPI/architecture guide.
- Overlaps heavily with STYLE_6’s layered architecture guidance and should be consolidated to avoid duplication.
- Error-handling and DI patterns may be extracted into a general backend code style or architecture reference.
- Testing sections should be reconciled with `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md` to keep patterns consistent.
 - Introduction of advanced layering and patterns should be staged according to `docs/LIFECYCLE.md` so early phases are not overloaded.

## Red Flags

- Major overlap with STYLE_6 on layered architecture, DI, and error handling; maintaining both separately risks drift.
- Significant conceptual overlap with `fastapi-best-practices.md`, especially around clean architecture and SOLID ideas.
- Assumes SQLAlchemy, DB sessions, and repository abstractions that the current project does not yet use.
- Describes routers/services/repositories and complex DI chains while current endpoints still use hardcoded data and minimal services.
- Frontend/TanStack Query alignment is assumed but not yet part of this repo’s actual scope.
- Domain examples (`Project`, `User`) do not match the MCP metadata domain, making direct copy-paste misleading.
- No concrete custom exception hierarchy (`DomainError`, `NotFoundError`, etc.) exists in the codebase yet.
- Pagination patterns (`Paginated[T]`, `page`/`pageSize`) are not implemented in current routes (e.g., `/fetch` just returns a list).
- Testing recommendations (TestClient, dependency overrides) need to be aligned with existing pytest fixtures and docs.
- Versioning guidance partially duplicates what is already done (`/api/v1` metadata router), so future edits must avoid contradictions.

## References

- docs/to_integrate/api-patterns-guide.md
- docs/to_integrate/fastapi-best-practices.md
- working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md
- app/routes/metadata_router_v1.py
- app/services/mcp_manager.py
- app/core/dependencies.py
- app/contracts/metadata_contract.py
- pyproject.toml
- docs/TEST.md
- docs/TESTING_ARCHITECTURE.md
- tests/conftest.py
