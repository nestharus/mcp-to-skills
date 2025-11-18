You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_5.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_5 section pair 1

This file contains one or two `##` sections from docs/to_integrate/STYLE_5.md.

> Deprecated: This legacy style guide has been superseded by `docs/code-style-guide.md`.
>
> Do not update this file. See `docs/code-style-guide.md` for the canonical Python 3.14+ style, typing, and tooling standards.
### Classes and Data Models

Use `PascalCase` for classes and data models (including Pydantic models and domain services):

```python
# ✅ Good
from pydantic import BaseModel

class UserService:
    [ELIDED]

class UserProfile(BaseModel):
    id: int
    email: str

# ❌ Bad
class userService:
    [ELIDED]

class user_profile(BaseModel):
    id: int
    email: str
```

### Files and Directories

In Python/FastAPI projects:

* Use `snake_case` for module (file) names
* Use `snake_case` for package (directory) names
* Match file name to its primary responsibility

```text
✅ Good
user_service.py
user_profile.py
api_client.py
user_router.py

❌ Bad
UserService.py
userProfile.py
API_Client.py
UserRouter.py
```

Example FastAPI layout:

```text
app/
  main.py
  api/
    routes/
      users.py        # contains /users endpoints
    dependencies.py
  services/
    user_service.py
  models/
    user_profile.py
```

---

## Functions

### Keep Functions Small

Functions should do one thing and do it well, with type hints:

```python
# ✅ Good
import re

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

def validate_password(password: str) -> bool:
    return len(password) >= 8
```

```python
# ❌ Bad
def validate_user(email: str, password: str) -> bool:
    # validates email, password, logs stuff, touches the DB, etc.
    [ELIDED]
```

Keep FastAPI route handlers thin; push logic into service functions:

```python
# ✅ Good: route is thin
from fastapi import APIRouter, HTTPException
from .schemas import UserCreate
from .services import create_user

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(payload: UserCreate):
    user = await create_user(payload)
    return user
```

```python
# ❌ Bad: route does everything
@router.post("/users")
async def create_user_endpoint(payload: dict):
    # validate, hash password, talk to DB, send email, etc.
    [ELIDED]
```

### Callbacks and Small Inline Functions

Python rarely uses callbacks the same way JavaScript does, but similar rules apply: keep inline functions small and readable.

```python
users = [{"name": "alice"}, {"name": "bob"}]

# ✅ Good: comprehensions for simple transformations
names = [user["name"] for user in users]

# ✅ Also OK: small lambda for simple callback-style usage
active_users = list(filter(lambda u: u["active"], users))

# ❌ Bad: large, complex inline lambdas
active_users = list(filter(
    lambda u: u["active"] and u["last_login"] is not None and len(u["roles"]) > 1,
    users,
))
```

Prefer named functions when logic is non-trivial:

```python
def is_power_user(user: dict) -> bool:
    return user["active"] and user["last_login"] is not None and len(user["roles"]) > 1

power_users = [u for u in users if is_power_user(u)]
```

### Avoid Nested Callbacks; Prefer async/await

In FastAPI, use `async`/`await` instead of nested callbacks or deeply nested logic.

```python
# ✅ Good
async def fetch_user(user_id: int):
    [ELIDED]

async def fetch_profile(profile_id: int):
    [ELIDED]

async def update_profile(profile):
    [ELIDED]

async def process_user(user_id: int) -> None:
    user = await fetch_user(user_id)
    profile = await fetch_profile(user.profile_id)
    await update_profile(profile)
```

```python
# ❌ Bad: callback-style / deeply nested logic
def process_user(user_id: int, on_done):
    def on_user(user):
        def on_profile(profile):
            def on_update(_: object):
                on_done()
            update_profile_async(profile, on_update)
        fetch_profile_async(user.profile_id, on_profile)
    fetch_user_async(user_id, on_user)
```

Integrating with FastAPI:

```python
# services/user_service.py
async def process_user(user_id: int) -> None:
    user = await fetch_user(user_id)
    profile = await fetch_profile(user.profile_id)
    await update_profile(profile)
```

```python
# api/routes/users.py
from fastapi import APIRouter, HTTPException
from app.services.user_service import process_user

router = APIRouter()

@router.post("/users/{user_id}/process")
async def process_user_endpoint(user_id: int):
    try:
        await process_user(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "ok"}
```

This keeps route handlers simple, uses `async`/`await` idiomatically, and avoids nested control flow.

--- SOURCE SECTION END ---
