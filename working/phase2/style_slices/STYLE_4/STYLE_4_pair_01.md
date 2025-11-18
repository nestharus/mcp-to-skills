# STYLE_4 section pair 1

This file contains one or two `##` sections from docs/to_integrate/STYLE_4.md.

> Deprecated: This legacy style guide has been superseded by `docs/code-style-guide.md`.
>
> Do not update this file. See `docs/code-style-guide.md` for the canonical Python 3.14+ style, typing, and tooling standards.
#### Domain Models

Use shared Pydantic models and enums for consistent entity modeling across your FastAPI services.

```python
from ui_designer.shared_types import Project, ProjectStatus, DesignToken

# ✅ Good – type-safe status checks
def can_edit_project(project: Project) -> bool:
    editable_statuses: set[ProjectStatus] = {
        ProjectStatus.DRAFT,
        ProjectStatus.IN_PROGRESS,
    }
    return project.status in editable_statuses


# ✅ Good – working with design tokens
def apply_design_token(token: DesignToken) -> str:
    return f"var(--{token.type}-{token.name})"
```

Example usage in FastAPI:

```python
from fastapi import APIRouter, Depends
from ui_designer.shared_types import Project, ProjectId

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: ProjectId) -> Project:
    [ELIDED]


@router.patch("/{project_id}", response_model=Project)
async def update_project(project_id: ProjectId, project: Project) -> Project:
    if not can_edit_project(project):
        [ELIDED]
    [ELIDED]
```

Refer to the `ui_designer.shared_types` module and the API patterns guide for full model and enum definitions and usage guidelines.

## Naming Conventions

### Variables and functions

* Use `snake_case` for variables and functions
* Use descriptive names that explain purpose
* Avoid abbreviations unless widely understood

```python
# ✅ Good
user_count = len(users)
is_authenticated = check_auth()


def calculate_total_price(items: list[Item]) -> float:
    [ELIDED]


# ❌ Bad
userCount = len(users)
auth = check_auth()


def calc(items):
    [ELIDED]
```

### Classes, Pydantic models, and enums

* Use `PascalCase` for classes, Pydantic models, and enums

```python
# ✅ Good
class Project(BaseModel):
    id: str
    name: str


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in-progress"
    ARCHIVED = "archived"


# ❌ Bad
class project(BaseModel):
    [ELIDED]


class project_status(Enum):
    [ELIDED]
```

### Constants

Use `UPPER_SNAKE_CASE` for true constants:

```python
# ✅ Good
MAX_RETRY_ATTEMPTS = 3
API_BASE_URL = "https://api.example.com"


# ❌ Bad
max_retry_attempts = 3
api_base_url = "https://api.example.com"
```
