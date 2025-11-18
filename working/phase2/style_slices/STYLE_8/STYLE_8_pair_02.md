# STYLE_8 section pair 2

This file contains one or two `##` sections from docs/to_integrate/STYLE_8.md.

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

