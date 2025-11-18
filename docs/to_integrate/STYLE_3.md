> Deprecated: This legacy style guide has been superseded by `docs/code-style-guide.md`.
>
> Do not update this file. See `docs/code-style-guide.md` for the canonical Python 3.14+ style, typing, and tooling standards.
Here is the updated documentation adapted for **FastAPI** with **Python 3.14** best practices, structured under the same headings as your original document:

---

### Generics

Use descriptive `TypeVar` names in Python 3.14 and adhere to modern type-alias syntax.

```python
from collections.abc import Callable, Iterable
from typing import TypeVar

TInput  = TypeVar("TInput")
TOutput = TypeVar("TOutput")

def map_iterable(
    items: Iterable[TInput],
    mapper: Callable[[TInput], TOutput],
) -> list[TOutput]:
    return [mapper(item) for item in items]
```

Avoid:

```python
T = TypeVar("T")
U = TypeVar("U")

def map_iterable(
    items: Iterable[T],
    mapper: Callable[[T], U],
) -> list[U]:
    return [mapper(item) for item in items]
```

#### Type Aliases (Python 3.14)

Use the `type` statement (or simple assignment) for aliases, which is the recommended approach in Python 3.12+ and fully idiomatic in Python 3.14. ([Python documentation][1])

```python
ProjectId    = str
ProjectsList = list["Project"]   # forward-reference simple thanks to lazy annotations in 3.14
```

Or for explicit clarity:

```python
from typing import TypeAlias

ProjectId:    TypeAlias = str
ProjectsList: TypeAlias = list["Project"]
```

Python 3.14 introduces **lazy annotation evaluation** so forward references work naturally (no need for `from __future__ import annotations`). ([Real Python][2])

---

### Project-Specific Types

Maintain a shared error model and consistent type definitions across your backend services.

```python
from enum import StrEnum
from pydantic import BaseModel

class ErrorCode(StrEnum):
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    VALIDATION_FAILED   = "VALIDATION_FAILED"
    UNAUTHORIZED        = "UNAUTHORIZED"
    FORBIDDEN           = "FORBIDDEN"
    INTERNAL_ERROR      = "INTERNAL_ERROR"

class AppError(BaseModel):
    code:        ErrorCode
    message:     str
    status_code: int
```

This mirrors your TypeScript contract with `AppError` and `ErrorCode`.

---

### Error Handling & Query Analogue in FastAPI

#### Centralised Exception Handling

Define a custom exception and global handler so all endpoints follow the same error contract.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, error: AppError):
        self.error = error
        super().__init__(error.message)

app = FastAPI()

@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.error.status_code,
        content=exc.error.model_dump(),
    )
```

#### Service / “Query Function” Layer

Your backend analogue of a TanStack Query’s `queryFn`:

```python
from typing import list
import httpx

async def fetch_projects(page: int, page_size: int) -> list[Project]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "http://backend.internal/api/projects",
            params={"page": page, "page_size": page_size},
            timeout=10.0,
        )
    if not resp.is_success:
        raise AppException(
            AppError(
                code=        ErrorCode.RESOURCE_NOT_FOUND,
                message=     "Unable to load projects",
                status_code= resp.status_code,
            )
        )
    data = resp.json()
    return [Project.model_validate(item) for item in data]
```

#### Endpoint Wiring

```python
from fastapi import Query

@app.get("/api/projects", response_model=list[Project])
async def list_projects(
    page:      int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return await fetch_projects(page=page, page_size=page_size)
```

* Successful response: `200 OK` + `Project[]`.
* On error: returns the `AppError` shape with the `status_code`, `code`, `message`.

---

### Mapping TS Guidelines → Python 3.14 + FastAPI

| TS Pattern                          | Python 3.14 / FastAPI Equivalent                                            |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `mapArray<TInput, TOutput>`         | `TypeVar("TInput")`, `TypeVar("TOutput")`, descriptive names                |
| Shared `AppError` + `ErrorCode`     | Use `StrEnum` + `BaseModel` for `AppError`                                  |
| `queryFn` + `useQuery` approach     | Service function (`async def`) that returns typed model or raises exception |
| No success/error wrapper containers | Endpoint returns model or `AppError` via exception handler                  |
| Type aliases in TS                  | Use `type Alias = [ELIDED]` or `Alias: TypeAlias = [ELIDED]` in Python 3.14               |

---

### Python 3.14 Specific Best Practices

* Leverage **lazy annotation evaluation** so you don’t need to wrap forward references in strings or rely on `from __future__ import annotations`. ([Real Python][2])
* Prefer `type Name = [ELIDED]` (or `Name: TypeAlias = [ELIDED]`) for type aliases, making intent clear. ([Python documentation][1])
* Maintain descriptive `TypeVar` names (`TInput`, `TModel`, `TOutput`) rather than generic `T`, `U`.
* Organise your FastAPI project structure to favour modularity (routers, services, schemas) so it scales. ([GitHub][3])
* Use async endpoints and services appropriately — use `async` when I/O bound. Avoid blocking operations on event-loop threads.
* For type dependencies, parameter validation, and response modelling rely on Pydantic+type hints built into FastAPI. ([FastAPI][4])

---

If you’d like, I can produce a **complete markdown version** of this documentation (fully formatted, ready for your project wiki) with code blocks and examples for each section.

[1]: https://docs.python.org/3/library/typing.html?utm_source=chatgpt.com "typing — Support for type hints"
[2]: https://realpython.com/python-annotations/?utm_source=chatgpt.com "Python 3.14 Preview: Lazy Annotations"
[3]: https://github.com/zhanymkanov/fastapi-best-practices?utm_source=chatgpt.com "zhanymkanov/fastapi-best-practices"
[4]: https://fastapi.tiangolo.com/python-types/?utm_source=chatgpt.com "Python Types Intro"
