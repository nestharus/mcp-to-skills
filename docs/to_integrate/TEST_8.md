1. Keep tests fast

* Avoid unnecessary async/event-loop usage
* Mock external dependencies (DB, HTTP, filesystem, etc.)
* Don’t test implementation details (private methods, internal calls); test observable behavior

```python
# example: mocking an HTTP client
from unittest.mock import Mock

def test_fetch_user_uses_client():
    client = Mock()
    client.get.return_value = {"email": "john@example.com"}

    user = fetch_user(client, user_id=1)

    client.get.assert_called_once_with("/users/1")
    assert user.email == "john@example.com"
```

---

2. Make tests independent

* Each test should be runnable alone
* Do not rely on test ordering
* Clean up state in fixtures or teardown

```python
import pytest
import tempfile
import shutil
from myapp import create_user_db

@pytest.fixture
def temp_db():
    tmp_dir = tempfile.mkdtemp()
    db = create_user_db(tmp_dir)
    yield db
    shutil.rmtree(tmp_dir)  # cleanup

def test_create_user(temp_db):
    user = temp_db.create_user(email="a@example.com")
    assert user.id is not None

def test_delete_user(temp_db):
    user = temp_db.create_user(email="b@example.com")
    temp_db.delete_user(user.id)
    assert temp_db.get_user(user.id) is None
```

---

3. Use descriptive assertions

Good:

```python
def test_user_email_is_set():
    user = User(email="john@example.com")
    assert user.email == "john@example.com"
```

Bad:

```python
def test_user_email_is_truthy():
    user = User(email="john@example.com")
    assert user.email  # too vague
```

Add custom messages if it helps:

```python
assert user.email == "john@example.com", "User email should match input value"
```

---

4. Test one thing at a time

Good:

```python
def test_valid_email_format():
    assert is_valid_email("john@example.com") is True
    assert is_valid_email("invalid-email") is False

def test_email_length_limit():
    long_email = "a" * 250 + "@example.com"
    assert is_valid_email(long_email) is False
```

Bad:

```python
def test_email_validation():
    # format, length, domain, blacklist, etc. all in one
    assert is_valid_email("john@example.com") is True
    # several unrelated concerns mixed together
```

Each test should have a clear, narrow responsibility.

---

5. Avoid test duplication (use fixtures / setup)

Using pytest fixtures instead of repeating setup:

```python
import pytest
from myapp import UserService

@pytest.fixture
def user_service():
    return UserService()

def test_create_user(user_service):
    user = user_service.create_user(email="a@example.com")
    assert user.id is not None

def test_delete_user(user_service):
    user = user_service.create_user(email="b@example.com")
    user_service.delete_user(user.id)
    assert user_service.get_user(user.id) is None
```

If using `unittest` style:

```python
import unittest
from myapp import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.service = UserService()

    def test_create_user(self):
        user = self.service.create_user(email="a@example.com")
        self.assertIsNotNone(user.id)

    def test_delete_user(self):
        user = self.service.create_user(email="b@example.com")
        self.service.delete_user(user.id)
        self.assertIsNone(self.service.get_user(user.id))
```
