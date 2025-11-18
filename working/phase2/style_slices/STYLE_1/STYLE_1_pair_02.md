# STYLE_1 section pair 2

This file contains one or two `##` sections from docs/to_integrate/STYLE_1.md.

## 2. Naming & Layout

Follow PEP 8 naming rules. ([Python documentation][2])

* Functions, methods, variables: `snake_case`
* Classes, exceptions: `PascalCase`
* Constants: `UPPER_SNAKE_CASE`
* Avoid ambiguous one-letter names (`l`, `O`, `I`).

Formatting:

* Indentation: **4 spaces** (no tabs).
* Line length: project limit is **120 characters** (PEP 8 recommends 79; we intentionally deviate here).
* Blank lines:

    * 2 blank lines between top-level functions and classes.
    * 1 blank line between methods in a class.

---

## 3. Imports

* Imports go at the top of the file, after the module docstring and before globals/constants. ([Python documentation][2])
* Group imports with a blank line between groups:

    1. Standard library
    2. Third-party
    3. Local application / project

Example:

```python
"""High-level orchestration for data pipeline."""

from __future__ import annotations  # Only if you explicitly need legacy behaviour

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

import httpx

from .config import PipelineConfig
from .logging import get_logger
```

* Do not use `from module import *` except in controlled, documented cases (e.g., test helpers where explicitly justified).

---

