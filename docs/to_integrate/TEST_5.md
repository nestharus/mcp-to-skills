### Test coverage (Python)

#### Viewing coverage

```bash
# Generate coverage report (all tests)
coverage run -m pytest

# HTML coverage report
coverage html

# Open HTML coverage report (macOS)
open htmlcov/index.html
# Linux (example)
xdg-open htmlcov/index.html
# Windows (PowerShell)
start htmlcov\index.html
```

#### LLM coverage input: JSON per package/module

`coverage.py` can emit JSON directly:

```bash
# For a web app package
coverage run -m pytest apps/web
coverage json -o apps/web/coverage/coverage-final.json

# For shared types package
coverage run -m pytest packages/shared_types
coverage json -o packages/shared_types/coverage/coverage-final.json

# For query package
coverage run -m pytest packages/query
coverage json -o packages/query/coverage/coverage-final.json
```

Quick sanity check (similar to the `jq` no-op):

```bash
cat apps/web/coverage/coverage-final.json | jq . > /dev/null
cat packages/shared_types/coverage/coverage-final.json | jq . > /dev/null
cat packages/query/coverage/coverage-final.json | jq . > /dev/null
```

#### Optionally merge coverage for a single LLM input

Preferred: use `coverage combine` and then export JSON:

```bash
# Run coverage separately and keep .coverage files, e.g.
# apps/web/.coverage
# packages/shared_types/.coverage
# packages/query/.coverage

coverage combine \
  apps/web \
  packages/shared_types \
  packages/query

coverage json -o coverage/coverage-final-merged.json
```

Or merge JSONs yourself (example with `jq`, similar to your original):

```bash
jq -s 'reduce .[] as $item ({}; . * $item)' \
  apps/web/coverage/coverage-final.json \
  packages/shared_types/coverage/coverage-final.json \
  packages/query/coverage/coverage-final.json \
  > coverage/coverage-final-merged.json
```

---

### Coverage goals

* Unit tests: aim for ≥ 80% (branches, functions, lines, statements)
* Integration tests: aim for ≥ 70%
* Overall target: 80%
* Prioritize critical business logic; don’t chase 100% if it adds little value.
* Even “types-first” or “schema-first” packages should use the same thresholds if they have runtime constructs (enums, helpers, validators) that execute at runtime and thus show up in coverage.

---

### What to test

✅ Do test:

* Business logic and algorithms
* Edge cases and error conditions
* Public APIs and interfaces
* Data transformations
* Validation logic

❌ Don’t test:

* Third-party libraries
* Trivial getters/setters or dataclass boilerplate
* Framework internals (Django/Flask/FastAPI internals, etc.)
* Pure configuration files

---

### Mocking (functions, modules, timers) in Python

Using `unittest.mock` (works with `pytest` and `unittest`).

#### Mocking functions

```python
from unittest.mock import Mock

def test_mock_function():
    # Basic mock
    mock_fn = Mock()
    mock_fn.return_value = "mocked value"

    result = mock_fn("arg")

    mock_fn.assert_called_with("arg")
    mock_fn.assert_called_once()
    assert result == "mocked value"


def test_mock_with_implementation():
    mock_fn = Mock(side_effect=lambda x: x * 2)

    assert mock_fn(3) == 6
    mock_fn.assert_called_with(3)
```

If you use `pytest-mock`, you can also do:

```python
def test_with_mocker(mocker):
    mock_fn = mocker.Mock(return_value="mocked")
    mock_fn("arg")
    mock_fn.assert_called_once_with("arg")
```

#### Mocking modules / functions in modules

```python
from unittest.mock import patch

# api.py
# def fetch_user(user_id): ...

@patch("myapp.api.fetch_user")
def test_fetch_user(mock_fetch_user):
    mock_fetch_user.return_value = {"id": 1, "name": "John"}

    from myapp.service import get_user  # imports inside test to avoid import-time patch issues

    user = get_user(1)

    mock_fetch_user.assert_called_once_with(1)
    assert user["name"] == "John"
```

Partial mock (keep most behavior, override one function):

```python
from unittest.mock import patch

# utils.py
# def some_function(): ...
# def other_function(): ...

def test_partial_mock_utils():
    import myapp.utils as utils

    with patch.object(utils, "some_function") as mock_some_function:
        mock_some_function.return_value = "mocked"

        result = utils.some_function()
        assert result == "mocked"

        mock_some_function.assert_called_once()
```

Or with `pytest-mock`:

```python
def test_partial_mock_utils(mocker):
    import myapp.utils as utils

    mock_some_function = mocker.patch.object(utils, "some_function", return_value="mocked")
    assert utils.some_function() == "mocked"
    mock_some_function.assert_called_once()
```

#### Mocking timers / time-dependent behavior

Python doesn’t have fake timers built in, but you can patch time APIs or use helper libraries.

Basic patch using `pytest`’s `monkeypatch`:

```python
import time

def do_after_delay(callback, delay):
    time.sleep(delay)
    callback()

def test_do_after_delay(monkeypatch):
    calls = []

    def fake_sleep(seconds):
        # Skip real waiting, just record the call
        calls.append(seconds)

    monkeypatch.setattr(time, "sleep", fake_sleep)

    callback_called = []

    def callback():
        callback_called.append(True)

    do_after_delay(callback, 1.0)

    assert calls == [1.0]
    assert callback_called == [True]
```

Using `freezegun` (or similar) for time-based logic:

```python
from freezegun import freeze_time
import datetime

def is_expired(now, expires_at):
    return now >= expires_at

def test_is_expired():
    with freeze_time("2025-01-01 10:00:00"):
        now = datetime.datetime.now()
        expires_at = datetime.datetime(2025, 1, 1, 9, 0, 0)
        assert is_expired(now, expires_at) is True
```

This gives you Python-native equivalents of your Vitest/bun workflow: coverage reports, JSON for tooling/LLMs, clear coverage goals, and structured mocking patterns for functions, modules, and time.
