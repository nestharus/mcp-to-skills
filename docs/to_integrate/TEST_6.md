Here’s a direct Python/pytest equivalent.

```python
# test_fetch_user.py
import pytest

# --- Code under test (examples) ---

import asyncio

async def fetch_user_async(user_id: int):
    await asyncio.sleep(0)  # simulate async work
    if user_id < 0:
        raise ValueError("User not found")
    return {"id": 1, "name": "John"}


def fetch_user_callback(user_id: int, callback):
    # simulate async work with asyncio
    async def _work():
        await asyncio.sleep(0)
        if user_id < 0:
            callback(ValueError("User not found"), None)
        else:
            callback(None, {"id": 1, "name": "John"})

    asyncio.create_task(_work())


# --- Async testing (Promises → async/await) ---

@pytest.mark.asyncio
async def test_should_resolve_with_user_data():
    user = await fetch_user_async(1)
    assert user == {"id": 1, "name": "John"}


@pytest.mark.asyncio
async def test_should_reject_with_error():
    with pytest.raises(ValueError, match="User not found"):
        await fetch_user_async(-1)


# --- Testing callbacks (Jest-style done) ---

@pytest.mark.asyncio
async def test_should_call_callback_with_result():
    future: asyncio.Future = asyncio.get_event_loop().create_future()

    def callback(error, user):
        if error:
            future.set_exception(error)
        else:
            future.set_result(user)

    fetch_user_callback(1, callback)

    user = await future
    assert user == {"id": 1, "name": "John"}
```

Notes:

* Uses `pytest` plus `pytest-asyncio` for `@pytest.mark.asyncio`.
* `fetch_user_async` mirrors the Promise-based version.
* The callback test uses an `asyncio.Future` to emulate Jest’s `done` callback.
