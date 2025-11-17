# FastAPI API Patterns Guide

Complement to the existing **API Patterns Guide for the frontend** – this one defines how the FastAPI backend should expose APIs so that the frontend can use TanStack Query with minimal friction and strong typing.

---

## Tech Stack Integration

Assumed backend stack:

* **FastAPI** – HTTP routing, OpenAPI generation ([FastAPI][1])
* **Pydantic (v2)** – request/response models and validation ([Deepnote][2])
* **SQLAlchemy or equivalent** – data access (not prescribed here)
* **UI Designer shared types** – keep response shapes aligned with `Project`, `Paginated<T>`, `AppError`, `ErrorCode`, and `CreatePayload/UpdatePayload` from `@ui-designer/shared-types`.

---

## Core Principles

1. **Return plain resources, not wrapped envelopes**

    * `GET /projects/{id}` returns a `Project` JSON object, not `{ status, data }`.
    * `GET /projects` returns `Paginated<Project>` (`items`, `total`, `page`, `pageSize`), matching the frontend.

2. **Use a single, consistent error shape (`AppError`) everywhere**

    * JSON: `{ code: ErrorCode; message: string; statusCode: number; details?: object }`
    * Map *all* non-2xx responses to this shape using centralized exception handlers.

3. **Keep domain logic and HTTP concerns separate**

    * Services raise domain exceptions (`DomainError`); routers map them to HTTP responses. ([DEV Community][3])

4. **Use Pydantic models everywhere**

    * No untyped `dict` responses or request bodies.
    * Prefer Pydantic generics for reusable patterns like `Paginated[T]`. ([lewoudar.medium.com][4])

5. **Structure the app with routers, not one giant `main.py`**

    * Group endpoints by feature, use `APIRouter`, and version via prefixes (`/api/v1`). ([FastAPI][1])

6. **Design endpoints to match TanStack Query usage**

    * Stable URLs + standard status codes + predictable JSON shapes → easy query options and error handling on the frontend.

---

## Recommended Patterns

### 1. Project Structure & Routers

**Pattern**

Use a modular structure with `APIRouter` per bounded context (projects, agents, auth, etc.) and an explicit versioned API package.

```text
app/
  main.py
  api/
    v1/
      routers/
        projects.py
        agents.py
      schemas.py
      dependencies.py
  core/
    config.py
    errors.py
  db/
    session.py
    models/
```

FastAPI’s “bigger applications” and `APIRouter` docs encourage exactly this style. ([FastAPI][1])

**Example**

```python
# app/api/v1/routers/projects.py
from fastapi import APIRouter, Depends, Query, status
from .schemas import Project, ProjectCreate, ProjectUpdate, PaginatedProject
from ..dependencies import get_project_service, ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    svc: ProjectService = Depends(get_project_service),
) -> Project:
    return await svc.get(project_id)


@router.get("", response_model=PaginatedProject)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    svc: ProjectService = Depends(get_project_service),
) -> PaginatedProject:
    return await svc.list(page=page, page_size=page_size, search=search)


@router.post(
    "",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreate,
    svc: ProjectService = Depends(get_project_service),
) -> Project:
    return await svc.create(payload)


@router.patch("/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    svc: ProjectService = Depends(get_project_service),
) -> Project:
    return await svc.update(project_id, payload)
```

In `main.py`:

```python
from fastapi import FastAPI
from app.api.v1.routers import projects
from app.core.errors import register_exception_handlers

app = FastAPI(title="UI Designer API", version="1.0.0")

app.include_router(projects.router, prefix="/api/v1")

register_exception_handlers(app)
```

---

### 2. Schemas & Generics

Align Pydantic models with the shared TypeScript types used by the frontend (`Project`, `Paginated<T>`, `CreatePayload<T>`, `UpdatePayload<T>`, etc.).

**Paginated**

The frontend expects a shape like:

````ts
interface Paginated<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}
``` :contentReference[oaicite:13]{index=13}  

Mirror this in Python with a generic model:

```python
# app/api/v1/schemas.py
from typing import Generic, List, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel  # v2-compatible alias
from enum import Enum

T = TypeVar("T")


class ErrorCode(str, Enum):
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    # add more to match shared-types


class AppError(BaseModel):
    code: ErrorCode
    message: str
    statusCode: int
    details: dict | None = None


class Paginated(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    pageSize: int
````

Use a concrete alias per entity for nice OpenAPI docs:

```python
class Project(BaseModel):
    id: str
    name: str
    # [ELIDED]


class PaginatedProject(Paginated[Project]):
    pass
```

This pattern (generic pagination model with `items` and metadata) is widely used with FastAPI and Pydantic. ([lewoudar.medium.com][4])

**Create / Update payloads**

Map `CreatePayload<Project>` and `UpdatePayload<Project>` to backend models:

```python
class ProjectCreate(BaseModel):
    name: str
    # required fields only


class ProjectUpdate(BaseModel):
    name: str | None = None
    # all fields optional for PATCH
```

Routers then use these as `response_model` and body types, giving you typed docs and validation automatically. ([Deepnote][2])

---

### 3. Error Handling

Goal: **every non-2xx response is an `AppError` JSON**, so that TanStack Query handlers can reliably do:

```ts
const error: AppError = await response.json()
throw error
```

#### 3.1 Domain exceptions

Keep HTTP details out of the service layer; raise domain errors and map them at the edge. ([DEV Community][3])

```python
# app/core/errors.py
class DomainError(Exception):
    def __init__(
        self,
        *,
        code: ErrorCode,
        message: str,
        status_code: int,
        details: dict | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundError(DomainError):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            code=ErrorCode.RESOURCE_NOT_FOUND,
            message=f"{resource} {resource_id} not found",
            status_code=404,
        )


class InternalAppError(DomainError):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            code=ErrorCode.INTERNAL_ERROR,
            message=message,
            status_code=500,
        )
```

#### 3.2 Global exception handlers

Use FastAPI’s exception handling hooks to map domain errors, validation errors, and unexpected exceptions to the `AppError` schema. ([FastAPI][5])

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.schemas import AppError, ErrorCode
from .errors import DomainError, InternalAppError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(
        request: Request, exc: DomainError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=AppError(
                code=exc.code,
                message=exc.message,
                statusCode=exc.status_code,
                details=exc.details,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=AppError(
                code=ErrorCode.INTERNAL_ERROR,  # or a dedicated VALIDATION_ERROR
                message="Request validation failed",
                statusCode=422,
                details={"errors": exc.errors()},
            ).model_dump(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        # Normalize any plain HTTPException to AppError
        status_code = exc.status_code
        code = (
            ErrorCode.RESOURCE_NOT_FOUND
            if status_code == 404
            else ErrorCode.INTERNAL_ERROR
        )
        return JSONResponse(
            status_code=status_code,
            content=AppError(
                code=code,
                message=exc.detail if isinstance(exc.detail, str) else "HTTP error",
                statusCode=status_code,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        # Log and hide internals in production
        return JSONResponse(
            status_code=500,
            content=AppError(
                code=ErrorCode.INTERNAL_ERROR,
                message="Unexpected error",
                statusCode=500,
            ).model_dump(),
        )
```

Frontend code that does either `throw await response.json()` or constructs `AppError` based on status now always sees the same shape.

---

### 4. Pagination & Infinite Scroll

The frontend patterns expect:

* Query params: `page`, `pageSize`, optional `search`/`filters`.
* Response body: `Paginated<Project>` with `items`, `total`, `page`, `pageSize`.

**Recommended endpoint**

```python
from fastapi import Query

@router.get("", response_model=PaginatedProject)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    svc: ProjectService = Depends(get_project_service),
) -> PaginatedProject:
    result = await svc.list(page=page, page_size=page_size, search=search)

    # result should contain .items and .total
    return PaginatedProject(
        items=result.items,
        total=result.total,
        page=page,
        pageSize=page_size,
    )
```

**For infinite scroll**

The frontend uses `useInfiniteQuery` with `pageParam` and `getNextPageParam` based on `page`, `pageSize`, and `total`.

Just ensure:

* `GET /projects?page={page}&pageSize={pageSize}` always returns the same `Paginated<Project>` shape.
* `total` is the total count across all pages, not just the page length.

If you ever move to cursor-based pagination, add fields like `nextCursor` but keep `page` and `pageSize` intact for backward compatibility. ([lewoudar.medium.com][4])

---

### 5. Mutations (Create/Update/Delete)

Match the frontend’s `CreatePayload` and `UpdatePayload` usage by:

* `POST /projects`

    * Body: `ProjectCreate`
    * Response: `201 Created` + `Project` JSON

* `PATCH /projects/{id}`

    * Body: `ProjectUpdate` (partial)
    * Response: `200 OK` + updated `Project` JSON

* `DELETE /projects/{id}`

    * Response: `204 No Content` (no payload)

This directly supports React Query mutation options illustrated in the frontend guide.

**Example**

```python
from fastapi import status

@router.post(
    "",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreate,
    svc: ProjectService = Depends(get_project_service),
) -> Project:
    return await svc.create(payload)


@router.patch("/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    svc: ProjectService = Depends(get_project_service),
) -> Project:
    return await svc.update(project_id, payload)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    svc: ProjectService = Depends(get_project_service),
) -> None:
    await svc.delete(project_id)
```

**Avoid**

* Custom envelopes like:

  ```json
  { "status": "success", "data": { [ELIDED] } }
  ```

* Or nested result types (`ApiResult<ApiSuccess<T>, ApiFailure>`) on the wire. These complicate TanStack Query typing and are explicitly discouraged on the frontend side.

---

### 6. Dependency Injection & Layering

Use FastAPI’s DI system to keep endpoints thin and testable. ([FastAPI][6])

**Pattern**

* `dependencies.py` exports providers like `get_db_session`, `get_current_user`, `get_project_service`.
* Routers depend on services; services depend on repositories and external APIs.

```python
# app/api/v1/dependencies.py
from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.projects import ProjectService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_session() as session:
        yield session


def get_project_service(
    session: AsyncSession = Depends(get_db_session),
) -> ProjectService:
    return ProjectService(session=session)
```

```python
# app/services/projects.py
from app.core.errors import NotFoundError

class ProjectService:
    def __init__(self, session):
        self.session = session

    async def get(self, project_id: str) -> Project:
        project = await self._load(project_id)
        if not project:
            raise NotFoundError("Project", project_id)
        return project

    # list/create/update/delete [ELIDED]
```

Benefits:

* No global state; easy per-test overrides of `get_project_service`. ([Reddit][7])
* Domain logic is framework-agnostic and reusable in background tasks or scripts. ([DEV Community][3])

---

### 7. Versioning & Stability

* Prefix all API routes with `/api/v1` via router inclusion.
* Only introduce breaking changes with a new version (`/api/v2`), not by changing existing response shapes.
* Add fields instead of renaming or removing them when possible.

This keeps the frontend’s query definitions (`queryKey` factories and TanStack Query options) stable over time.

---

### 8. Testing Patterns

* Use `TestClient` or `httpx.AsyncClient` against the real FastAPI app.
* Override dependencies (`get_project_service`, `get_db_session`) in tests for mocking. ([FastAPI][6])

Example override:

```python
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.dependencies import get_project_service

class FakeProjectService:
    async def get(self, project_id: str) -> Project:
        # return a fixed project for tests
        [ELIDED]

def override_project_service():
    return FakeProjectService()

app.dependency_overrides[get_project_service] = override_project_service

client = TestClient(app)
```

---

## Summary

* **Endpoints**: Resource-oriented, versioned, typed with Pydantic, no response envelopes.
* **Errors**: Centralized handlers mapping all failures to `AppError`, with `ErrorCode` aligned to shared types.
* **Pagination**: Uniform `Paginated<T>` with `items`, `total`, `page`, `pageSize` and `page`/`pageSize` query params.
* **Mutations**: Plain `Project` responses for create/update, `204` for delete.
* **Architecture**: Routers + DI + domain services; no HTTP concerns in business logic.

This keeps the FastAPI backend in lockstep with the frontend API patterns, so TanStack Query can use simple `fetch` calls and strong typing without extra wrappers or boilerplate.

[1]: https://fastapi.tiangolo.com/tutorial/bigger-applications/?utm_source=chatgpt.com "Bigger Applications - Multiple Files"
[2]: https://deepnote.com/blog/ultimate-guide-to-fastapi-library-in-python?utm_source=chatgpt.com "Ultimate guide to FastAPI library in Python"
[3]: https://dev.to/buffolander/building-robust-error-handling-in-fastapi-and-avoiding-rookie-mistakes-ifg?utm_source=chatgpt.com "Building Robust Error Handling in FastAPI – and avoiding [ELIDED]"
[4]: https://lewoudar.medium.com/fastapi-and-pagination-d27ad52983a?utm_source=chatgpt.com "FastAPI and pagination - Kevin Tewouda - Medium"
[5]: https://fastapi.tiangolo.com/tutorial/handling-errors/?utm_source=chatgpt.com "Handling Errors"
[6]: https://fastapi.tiangolo.com/tutorial/dependencies/?utm_source=chatgpt.com "Dependencies"
[7]: https://www.reddit.com/r/FastAPI/comments/1iq7it3/state_management_and_separation_of_routes/?utm_source=chatgpt.com "State management and separation of routes : r/FastAPI"
