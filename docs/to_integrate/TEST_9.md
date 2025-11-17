Debugging tests (Python / pytest)

Using print/logs

```python
def test_should_process_data():
    input_data = ...
    expected = ...

    data = process_data(input_data)
    print("Processed data:", data)  # or use logging
    assert data == expected
```

Using debugger

```python
def test_should_process_data():
    input_data = ...
    expected = ...

    breakpoint()  # or: import pdb; pdb.set_trace()
    data = process_data(input_data)
    assert data == expected
```

Running a single test

Assuming tests live under `tests/` with `tests/unit`, `tests/component`, `tests/integration`:

```bash
# Run tests matching a pattern in name or -k expression
pytest -k "should_process_data"

# Run a specific test file
pytest tests/unit/test_user_service.py

# Run a specific test function in a file
pytest tests/unit/test_user_service.py::test_should_process_data

# Run a specific class method (if you use test classes)
pytest tests/unit/test_user_service.py::TestUserService::test_should_process_data
```

Common patterns

Testing error handling

```python
import pytest

def test_should_throw_error_for_invalid_input():
    with pytest.raises(ValueError, match="Invalid email"):
        validate_email("invalid")
```

Testing “type guards” / predicates

```python
def test_is_user_returns_true_for_valid_user_object():
    obj = {"id": 1, "name": "John"}
    assert is_user(obj) is True

def test_is_user_returns_false_for_invalid_object():
    obj = {"foo": "bar"}
    assert is_user(obj) is False
```

Testing transformations

```python
def test_should_transform_user_data_correctly():
    input_data = {"first_name": "John", "last_name": "Doe"}
    output = transform_user(input_data)
    assert output == {"full_name": "John Doe"}
```

Resources

* pytest documentation
* Coverage and pytest-cov documentation
* General Python testing best practices (fixture usage, parametrization, test naming, etc.)

Test placement strategy (Python)

* All tests are under `tests/` at the project root.
* Unit tests:

    * `tests/unit/`
    * Mirror the application package/module structure where it helps:

        * `src/myapp/user.py` → `tests/unit/test_user.py`
        * `src/myapp/features/foo.py` → `tests/unit/features/test_foo.py`
* Component tests:

    * `tests/component/`
    * Grouped by component or feature boundary:

        * `tests/component/api/`
        * `tests/component/services/`
* Integration tests:

    * `tests/integration/`
    * Optionally organized by category (similar idea to `client/`, `server/`, `middleware/`):

        * `tests/integration/client/`
        * `tests/integration/server/`
        * `tests/integration/middleware/`
    * Shared fixtures:

        * `tests/fixtures/` (DB setup, external service mocks, common data builders, etc.)
* E2E tests (if you have them):

    * `tests/e2e/`
* Coverage expectations:

    * Include all runtime packages in coverage, e.g. `shared_types` (or equivalent), and enforce 80%+ coverage via `pytest-cov`/`coverage` configuration.
