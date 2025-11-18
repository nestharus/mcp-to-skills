# STYLE_6 section pair 1

This file contains one or two `##` sections from docs/to_integrate/STYLE_6.md.

> Deprecated: This legacy style guide has been superseded by `docs/code-style-guide.md`.
>
> Do not update this file. See `docs/code-style-guide.md` for the canonical Python 3.14+ style, typing, and tooling standards.
Here's a documentation-style guide for FastAPI best practices, following the structure of your React example.

## 🐍 FastAPI Best Practices (Python 3.14+)

This guide covers a scalable, maintainable structure for FastAPI applications, emphasizing a clean separation of concerns using routers, services, repositories, and dependency injection.

-----

### 1\. Overall Project Structure

A clean, layered structure is key to a scalable API. Each layer has a distinct responsibility.

```text
/app
├── main.py             # FastAPI app instantiation, mounts routers
├── dependencies.py     # Dependency "provider" functions (e.g., get_db)
├── core/
│   └── settings.py     # Pydantic settings management (env vars)
├── db/
│   ├── base.py         # SQLAlchemy Base and engine setup
│   └── models.py       # SQLAlchemy ORM models (e.g., User, Item)
├── models/
│   └── schema.py       # Pydantic models (schemas) for API I/O
├── repositories/
│   └── user_repo.py    # Data Access Layer (only talks to DB)
├── services/
│   └── user_service.py # Business Logic Layer (orchestrates)
└── routers/
    └── users.py        # API Layer (handles HTTP requests)
```

-----

### 2\. Routers (Handlers)

Routers are the **HTTP layer**. Their only job is to handle incoming requests, validate data (using Pydantic), call the *service layer*, and return a response.

**Best Practices:**

* **Keep handlers thin.** They should contain *no* business logic.
* Use `APIRouter` to organize endpoints into separate files.
* Use Pydantic models for `response_model` to guarantee output structure and for request bodies to get automatic validation.
* Inject the **Service** using `Depends`.
* Catch service-level exceptions and translate them into `HTTPException`.

<!-- end list -->

```python
# app/routers/users.py

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import schema
from app.services.user_service import UserService, UserAlreadyExistsError
from app.dependencies import get_user_service # DI provider

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Use Annotated for cleaner dependency injection
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@router.post(
    "/",
    response_model=schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_in: schema.UserCreate,
    user_service: UserServiceDep,
) -> schema.UserPublic:
    """
    Create a new user.
    """
    try:
        # ✅ Good: Delegate all logic to the service layer
        new_user = user_service.create_user(user_in)
        return new_user
    except UserAlreadyExistsError as e:
        # ✅ Good: Translate business exceptions to HTTP exceptions
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
```

-----

### 3\. Services (Business Logic)

Services are the **business logic layer**. They orchestrate tasks, enforce rules, and are completely decoupled from HTTP.

**Best Practices:**

* Should be a plain Python class.
* **Must not** know about `Request`, `Response`, or `HTTPException`.
* If something goes wrong, it should **raise a custom business exception** (e.g., `UserNotFoundError`, `InsufficientStockError`).
* Inject the **Repository** in its `__init__`.
* Methods should accept and return Pydantic models or simple data, not ORM models (to maintain separation).

<!-- end list -->

```python
# app/services/user_service.py

from app.models import schema
from app.repositories.user_repo import UserRepo
from app.db import models as db_models
# (Assume password hashing utils exist elsewhere)

# --- Custom Business Exceptions ---
class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists.")

class UserNotFoundError(Exception):
    pass

# --- Service Class ---
class UserService:
    # ✅ Good: Inject repository via __init__
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_user(self, user_in: schema.UserCreate) -> db_models.User:
        """
        Business logic to create a new user.
        """
        # ✅ Good: Business rule check
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            # ✅ Good: Raise specific business exception
            raise UserAlreadyExistsError(email=user_in.email)

        # (Logic to hash password[ELIDED])
        hashed_password = [ELIDED] # hash_password(user_in.password)

        # Create a new ORM model from schema data
        user_to_create = db_models.User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
        )
        
        # ✅ Good: Delegate data creation to the repository
        return self.user_repo.create_user(user_to_create)
```

-----

### 4\. Repositories (Data Access)

Repositories are the **data access layer**. Their *only* job is to query the database. They abstract *how* data is stored.

**Best Practices:**

* Should be a plain Python class.
* **Must not** contain any business logic.
* Inject the database session (e.g., `SQLAlchemy Session` or `Motor Client`) in its `__init__`.
* Methods are simple CRUD operations (Create, Read, Update, Delete).
* Methods accept and return **ORM models** (e.g., SQLAlchemy `User` models).

<!-- end list -->

```python
# app/repositories/user_repo.py

from sqlalchemy.orm import Session
from app.db import models as db_models

class UserRepo:
    # ✅ Good: Inject the DB session
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> db_models.User | None:
        """
        Fetch a single user by their email.
        """
        # ✅ Good: Simple, direct DB query
        return self.db.query(db_models.User).filter_by(email=email).first()

    def create_user(self, user: db_models.User) -> db_models.User:
        """
        Create a new user in the DB.
        """
        # ✅ Good: Simple data persistence logic
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

-----

### 5\. Dependency Injection (Wiring)

Dependency Injection (DI) is the "glue" that connects these decoupled layers. FastAPI's `Depends` system, combined with `typing.Annotated`, makes this clean.

**Best Practices:**

* Create "provider" functions in `app/dependencies.py` for concrete dependencies.
* Use `typing.Annotated` for clean and explicit dependency declarations.
* Use a generator for the `Session` to ensure `try[ELIDED]finally` (or `yield`) for proper open/close.

<!-- end list -->

```python
# app/dependencies.py

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.repositories.user_repo import UserRepo
from app.services.user_service import UserService

# --- 1. Database Session Provider ---
def get_db():
    """
    Dependency provider for the database session.
    Yields a session and ensures it's closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type alias for cleaner use in other functions
SessionDep = Annotated[Session, Depends(get_db)]

# --- 2. Repository Provider ---
def get_user_repo(db: SessionDep) -> UserRepo:
    """
    Dependency provider for the UserRepo.
    It, in turn, depends on get_db.
    """
    return UserRepo(db=db)

# Type alias
UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]

# --- 3. Service Provider ---
def get_user_service(repo: UserRepoDep) -> UserService:
    """
    Dependency provider for the UserService.
    It, in turn, depends on get_user_repo.
    """
    return UserService(user_repo=repo)
```

**How it comes together (in `app/routers/users.py`):**

```python
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@router.post("/")
def create_user(
    user_in: schema.UserCreate,
    user_service: UserServiceDep,  # <-- FastAPI handles everything!
):
    # [ELIDED]
    return user_service.create_user(user_in)
    # [ELIDED]
```

When this endpoint is called, FastAPI will:

1.  See `user_service: UserServiceDep`
2.  Call `get_user_service()`
3.  See `get_user_service()` needs `UserRepoDep`
4.  Call `get_user_repo()`
5.  See `get_user_repo()` needs `SessionDep`
6.  Call `get_db()`, get a `Session`, and `yield` it
7.  Pass the `Session` to `UserRepo`
8.  Pass the `UserRepo` to `UserService`
9.  Pass the `UserService` to your `create_user` handler.

-----

### 6\. Comments and Documentation

Python's primary documentation is **type hints** and **docstrings**. FastAPI leverages these for its automatic OpenAPI (Swagger/ReDoc) generation.

**Best Practices:**

* **Type Hint Everything.** Use modern `str | None` (Python 3.10+) or `Optional[str]`.
* Use **Google-style docstrings** for all public functions/methods.
* Use Pydantic's `Field` to add descriptions and examples to your API schemas.

<!-- end list -->

```python
# app/models/schema.py

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    # ✅ Good: Use Field to add docs, examples, and constraints
    email: EmailStr = Field(
        [ELIDED], 
        description="The user's unique email address.",
        example="jane.doe@example.com"
    )
    full_name: str | None = Field(
        default=None,
        description="The user's full name.",
        example="Jane Doe"
    )

class UserCreate(UserBase):
    password: str = Field(
        [ELIDED],
        min_length=8,
        description="User's password (min 8 characters).",
    )

class UserPublic(UserBase):
    id: int = Field([ELIDED], description="Unique user ID.")

    # ✅ Good: Pydantic v2 "model_config" (replaces Config class)
    # This ensures ORM models (like SQLAlchemy) can be
    # read directly into this Pydantic schema.
    model_config = {
        "from_attributes": True 
    }
```

```python
# app/services/user_service.py

class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def get_user_by_id(self, user_id: int) -> db_models.User:
        """Fetches a user from the database by their ID.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            The SQLAlchemy User model.

        Raises:
            UserNotFoundError: If no user is found with the provided ID.
        """
        user = self.user_repo.get_by_id(user_id) # Assume repo has this
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found.")
        return user
```