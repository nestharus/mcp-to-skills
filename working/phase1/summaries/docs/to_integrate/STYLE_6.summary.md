# STYLE_6.md Summary

## Purpose
Document comprehensive FastAPI best practices for Python 3.14+ projects, focusing on a scalable layered architecture (routers, services, repositories), dependency injection, error handling, and documentation patterns for maintainable, testable APIs.

## Main Topics
- Overall project structure with a layered architecture: routers (HTTP layer), services (business logic), repositories (data access), and shared contracts.
- Routers (handlers): thin HTTP layer, Pydantic-based validation, `response_model` usage, and translation of domain errors into HTTP responses.
- Services (business logic): plain Python classes with no HTTP concerns, orchestrating domain operations and raising business exceptions.
- Repositories (data access): plain Python classes handling CRUD and ORM interactions.
- Dependency injection: provider functions using `typing.Annotated` and `fastapi.Depends` to wire settings, services, and repositories.
- Error handling: custom exception types, mapping domain errors to HTTP status codes, and consistent error responses.
- Documentation patterns: type hints, Google-style docstrings, and Pydantic `Field` metadata for rich OpenAPI schemas.

## Opinions/Guidelines
- Keep route handlers thin and free of business logic; they should orchestrate dependencies and map domain outcomes to HTTP responses.
- Services must not depend on HTTP types such as `Request`, `Response`, or `HTTPException`.
- Services should raise custom business exceptions (for example, `UserNotFoundError`) that routers translate into appropriate HTTP errors.
- Repositories should contain only data access logic; business rules stay in services.
- Use `typing.Annotated` with `Depends` for clearer dependency injection signatures.
- Type-hint all functions and methods, using modern union syntax (for example, `str | None`).
- Use Google-style docstrings for public APIs and Pydantic `Field` to enrich OpenAPI docs with descriptions and examples.

## Assumptions
- The project targets Python 3.14+ and uses modern typing features.
- An ORM such as SQLAlchemy is available for repository implementations and database sessions.
- The team has adopted a layered architecture pattern and understands inversion of control and dependency injection.
- FastAPI's automatic OpenAPI generation is a primary way of documenting the API.
- Pydantic v2 is used for request/response models and domain contracts.

## Staleness Indicators
- Describes a full routers → services → repositories architecture, but this codebase is still early-stage: there is no repository layer, and data in `app/routes/metadata_router_v1.py` is hardcoded.
- Assumes SQLAlchemy-style database sessions and repository classes, while this project currently has no database package (no `app/db/` or equivalent).
- Mentions service classes and DI chains that are only partially represented here (`app/services/mcp_manager.py` exists but is not yet wired into the routes).
- Shows dependency injection chains (for example, `get_db → get_user_repo → get_user_service`) that are more complex than the current `app/core/dependencies.py`, which only caches settings.
- Assumes a hierarchy of custom business exceptions, which this project does not yet implement.

## Tags
`style`, `architecture`, `fastapi`, `routers`, `services`, `repositories`, `dependency-injection`, `layered-architecture`, `separation-of-concerns`, `error-handling`, `pydantic`, `type-hints`, `docstrings`, `openapi`, `testing`

## Preliminary Target Docs
STYLE_6 is effectively a full FastAPI architecture guide and overlaps heavily with `docs/to_integrate/api-patterns-guide.md`. Architecture-related FastAPI patterns from STYLE_6 should either be merged into `docs/to_integrate/api-patterns-guide.md` or consolidated alongside `docs/fastapi-patterns.md` to keep routing, services, and DI guidance aligned. Selected sections may also feed into `docs/code-style-guide.md` (documentation and typing patterns) and the testing documentation set.

## Red Flags
1. **Major duplication with api-patterns-guide**: Large portions of STYLE_6 (project structure, routers, services, repositories, and DI) closely mirror `docs/to_integrate/api-patterns-guide.md`; these two documents should be merged rather than maintained separately.
2. **Overlap with fastapi-best-practices**: Architectural and SOLID/clean-architecture advice overlaps with `docs/to_integrate/fastapi-best-practices.md`; content should be deduplicated or clearly scoped.
3. **Aspirational vs descriptive architecture**: The guide describes a mature layered architecture that is not yet implemented here (no repositories, minimal DI, hardcoded responses in `metadata_router_v1.py`), so it currently functions as a target state rather than a description of the existing system.
4. **Database assumption**: Assumes a relational database and SQLAlchemy sessions, but this project has no concrete database setup; guidance should be made database-agnostic or clearly marked as future work.
5. **Missing custom exception layer**: Recommends custom business exceptions (for example, `UserNotFoundError`, `UserAlreadyExistsError`) and a centralized error-handling strategy, but the project lacks an `app/core/errors.py` or equivalent exception hierarchy.
6. **Dependency injection not implemented end-to-end**: Shows complete DI chains (database → repository → service), while `app/core/dependencies.py` only wires settings; integrating services and repositories via DI remains future work.
7. **Domain mismatch**: Examples reference generic User/Project domains instead of the MCP metadata domain (for example, `MetadataItem`, `FetchRequest`, and related contracts in `app/contracts/metadata_contract.py`).
8. **Overlap with STYLE_5**: Thin route handlers and service delegation rules are repeated in STYLE_5; these should be consolidated into a single set of routing/service guidelines.
9. **Overlap with STYLE_1**: Type-hinting and docstring requirements repeat STYLE_1 guidance and should be centralized in a unified style guide.
10. **OpenAPI tooling disconnect**: Discusses automatic OpenAPI generation but does not reference the actual tooling in this repo (`scripts/gen_openapi.py` and `openapi/openapi.json`), which should be aligned.
11. **Testing patterns vs current tests**: Mentions DI-based testing strategies and dependency overrides, but does not reference the existing testing setup (`tests/conftest.py`, `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`), which already define how tests are structured.

## References
- `docs/to_integrate/STYLE_6.md` (source document).
- `docs/to_integrate/api-patterns-guide.md` (major overlapping architecture content).
- `docs/to_integrate/fastapi-best-practices.md` (overlapping best practices and architecture principles).
- `working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md` (type hints and docstring guidance).
- `working/phase1/summaries/docs/to_integrate/STYLE_5.summary.md` (thin route handler and service patterns).
- `app/routes/metadata_router_v1.py` (current router implementation with hardcoded data).
- `app/services/mcp_manager.py` (placeholder service referenced in the architecture guide).
- `app/core/dependencies.py` (current DI implementation limited to settings).
- `app/contracts/metadata_contract.py` (current Pydantic contracts and domain models).
- `scripts/gen_openapi.py` (OpenAPI generation tooling).
- `tests/conftest.py`, `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md` (existing testing infrastructure and guidance).
