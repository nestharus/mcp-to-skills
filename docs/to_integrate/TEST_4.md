### Test naming (pytest)

Use descriptive names that explain:

* What is being tested
* Under what conditions
* What the expected outcome is

```python
# ✅ Good
def test_raises_error_when_input_is_none():
    ...

def test_returns_empty_list_when_no_items_match_filter():
    ...
```

```python
# ❌ Bad
def test_works():
    ...

def test_test_1():
    ...
```

General patterns that work well in Python:

* `test_<method>_when_<condition>_then_<expected>()`
* `test_<thing_under_test>_<expected_behavior>()`

### Test organization

Rough equivalent of nested `describe` blocks is:

* Test modules per unit (e.g. `test_user_service.py`)
* Classes per method or feature group
* Test functions per behavior

```python
# tests/unit/test_user_service.py

class TestCreateUser:
    def test_creates_user_with_valid_data(self):
        ...

    def test_raises_error_when_email_invalid(self):
        ...

    def test_hashes_password_before_saving(self):
        ...


class TestDeleteUser:
    def test_deletes_user_by_id(self):
        ...

    def test_raises_error_when_user_not_found(self):
        ...
```

You can also keep it flat if you prefer:

```python
def test_create_user_with_valid_data():
    ...

def test_create_user_raises_error_when_email_invalid():
    ...

def test_create_user_hashes_password_before_saving():
    ...

def test_delete_user_by_id():
    ...

def test_delete_user_raises_error_when_user_not_found():
    ...
```

### Running tests

Assuming a standard layout like:

* `src/your_app/` or `your_app/`
* `tests/unit/`
* `tests/integration/`
* `tests/e2e/`

and using `pytest` (+ `pytest-cov` for coverage).

#### Unit, integration, and all tests

```bash
# Unit tests (co-located or under tests/unit/)
pytest tests/unit

# Integration tests
pytest tests/integration

# All tests
pytest
```

Watch mode is not built into pytest, but you can use `ptw` (pytest-watch) or `pytest-testmon` if you want that behavior.

#### With coverage (pytest-cov)

```bash
# Unit test coverage
pytest tests/unit --cov=your_app --cov-report=term-missing

# Integration test coverage
pytest tests/integration --cov=your_app --cov-report=term-missing

# All tests with coverage
pytest --cov=your_app --cov-report=term-missing
```

#### Run a specific test file

```bash
pytest tests/unit/test_user_service.py
```

#### Run a specific test or class

```bash
# Single test function
pytest tests/unit/test_user_service.py::test_creates_user_with_valid_data

# Single test class
pytest tests/unit/test_user_service.py::TestCreateUser
```

#### Run tests matching a pattern (similar to `--grep`)

```bash
# Match by test name substring / expression
pytest -k "UserService"
pytest -k "create_user and error"
```

#### Run tests for a specific package / submodule

```bash
# If tests are organized by package
pytest tests/unit/your_app/shared_types
# Or by file pattern
pytest tests -k "shared_types"
```

### E2E tests

If you keep E2E tests under `tests/e2e/` (e.g. using Playwright for Python or another E2E tool):

```bash
pytest tests/e2e
```

Or use the specific runner for your E2E framework if it is not pytest-based; just mirror the structure:

* E2E tests live at `tests/e2e/`
* E2E config in the root (e.g. `playwright.config.py` or equivalent)

### Test filtering (focus / skip)

Pytest’s equivalents to `it.only`, `it.skip`, etc.:

#### Run only this test (focus)

Simplest approach: use node ids or `-k`:

```bash
pytest tests/unit/test_user_service.py::TestCreateUser::test_creates_user_with_valid_data
```

or

```bash
pytest -k "creates_user_with_valid_data"
```

You can also use markers like `@pytest.mark.focus` and run `pytest -m focus`, if you define such a convention.

#### Skip a test

```python
import pytest


@pytest.mark.skip(reason="not implemented yet")
def test_should_skip_this_test():
    ...
```

Conditional skip:

```python
@pytest.mark.skipif(condition, reason="explanation")
def test_skipped_on_condition():
    ...
```

#### Mark a test as expected to fail

Roughly analogous to “this is currently broken”:

```python
@pytest.mark.xfail(reason="known bug, tracking in ISSUE-123")
def test_currently_failing_behavior():
    ...
```

#### Skip or focus groups of tests (describe-level equivalent)

Use class-level decorators:

```python
import pytest


@pytest.mark.skip(reason="UserService tests temporarily disabled")
class TestUserService:
    def test_creates_user_with_valid_data(self):
        ...

    def test_raises_error_when_email_invalid(self):
        ...
```

Or run a specific class via node id as shown earlier instead of `describe.only`:

```bash
pytest tests/unit/test_user_service.py::TestUserService
```
