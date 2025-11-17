Here is an adapted Python 3.14+ style guide based on your current setup and requirements, incorporating `ruff`, `checkov`, `uv`, and adding `mypy` for type checking.

-----

## 🐍 Python Style Guide (3.14+)

This guide outlines our team's coding standards, built around our modern tooling stack: `uv`, `ruff`, `mypy`, and `checkov`.

## Imports

We use `ruff` to automatically format and enforce import order, which replaces the need for `isort`. The logical order it follows is:

1.  Standard Library
2.  External Dependencies (Third-party)
3.  Internal Absolute Imports
4.  Internal Relative Imports
5.  Type Imports (when using `if TYPE_CHECKING:`)

<!-- end list -->

```python
# 1. Standard Library
import json
from pathlib import Path
from dataclasses import dataclass

# 2. External Dependencies
import requests
from pydantic import BaseModel

# 3. Internal Absolute Imports
from my_app.services.api import api_client
from my_app.utils.dates import format_date

# 4. Internal Relative Imports
from .user_card import UserCard
from .. import schemas

# 5. Type Imports (for circular dependencies)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_app.models import User # noqa: F401
    from .types import Props       # noqa: F401
```

### Avoid Wildcard Imports

Wildcard imports (`from module import *`) pollute the global namespace and make code difficult to read and debug.

```python
# ✅ Good
from my_app.components.ui import Button, Input

# ❌ Bad (Avoid this)
from my_app.components.ui import *
```

-----

## Formatting

We use `ruff format` as our code formatter, which is a drop-in replacement for `black`. It handles all formatting rules automatically.

### Indentation

* Use **4 spaces** for indentation (this is the standard set by **PEP 8**).
* `ruff format` handles this automatically.

### Trailing Commas

* `ruff format` automatically adds trailing commas to multi-line collections (lists, dicts, sets) and function definitions.
* This produces cleaner Git diffs when adding new items or parameters.

<!-- end list -->

```python
# ✅ Good (object)
user = {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
}

# ✅ Good (function parameters)
def create_user(
    id: int,
    name: str,
    email: str,
):
    """[ELIDED]"""
    pass

# Adding a new parameter only changes one line
def create_user(
    id: int,
    name: str,
    email: str,
    is_admin: bool,
):
    """[ELIDED]"""
    pass
```

-----

## 🤖 Automated Tooling & Enforcement

Our development workflow is enforced by a combination of tools managed by `uv` and `pre-commit`.

### 1\. Linting & Formatting with Ruff

`ruff` handles both linting (`ruff check`) and formatting (`ruff format`). It's configured in our `pyproject.toml` file.

### 2\. Type Checking with mypy

To catch type-related bugs before runtime, we use **`mypy`**, the standard for static type checking in Python. This was the missing piece in our previous setup.

* Run it via: `uv run typecheck`

### 3\. Security Scanning with Checkov

We continue to use `checkov` to scan our codebase and Infrastructure-as-Code (IaC) files for security vulnerabilities.

* Run it via: `uv run security`

### 4\. Running Tasks with uv

We define all our scripts in `pyproject.toml` under the `[tool.uv.scripts]` section. This provides a single interface for running all our quality checks.

**Example `pyproject.toml` configuration:**

```toml
[tool.uv.scripts]
# Run all formatters
format = "ruff format ."

# Run all non-fixing checks
lint = [
    "ruff check .",
    "uv run typecheck",
    "uv run security",
]

# Individual tasks
typecheck = "mypy ."
security = "checkov --directory ."
```

> **Workflow:**
>
>   * Run `uv run format` to fix formatting.
>   * Run `uv run lint` to check for all linting, type, and security errors.

### 5\. Git Hooks with pre-commit

To ensure no bad code is ever committed, our `pre-commit` hook runs our checks on staged files. The hook is configured to run the individual tasks for maximum speed and efficiency.

Here is the recommended `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.5 # Use the latest ruff version
    hooks:
    -   id: ruff-format
        args: [ "--check" ] # Use --check to fail on unformatted files
    -   id: ruff
        args: [ "--fix", "--exit-non-zero-on-fix" ]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0 # Use the latest mypy version
    hooks:
    -   id: mypy
        args: [ "--strict" ] # Enforce strict type checking
        additional_dependencies: [
            # Add your project's type-stub dependencies here
            # e.g., "pandas-stubs"
        ]

-   repo: https://github.com/bridgecrewio/checkov
    rev: 3.2.144 # Use the latest checkov version
    hooks:
    -   id: checkov
        args: [ "--quiet" ] # Add any other flags you use
```

> **Note:** The user's original request mentioned the pre-commit hook runs `uv run lint`. While possible (using a `local` hook), the setup above is the community-standard way to use `pre-commit`. It's generally faster as it only runs tools on the files that have changed.