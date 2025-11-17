Overview
This project uses FastAPI for the web framework, Uvicorn as the ASGI server, and pytest as the testing framework. Tests are run via uv as the Python runtime/manager.

Important: This project uses pytest as the test runner. Always use `uv run pytest` (or `uv run python -m pytest`) to run tests. Do NOT invoke alternative runners or ad-hoc `python` commands that bypass pytest’s configuration.

Note: For async tests and FastAPI integration (e.g., using `httpx.AsyncClient` or `fastapi.testclient.TestClient`), follow the FastAPI testing patterns and fixtures defined in this repo (e.g., shared `test_app` or `client` fixtures, event loop fixtures, etc.).

Writing Tests

AAA + Traversal Rules
Adopt Arrange–Act–Assert with soft-style assertions and extracted traversals/conditions:

* Arrange, Act, Assert in order; keep test bodies linear and readable.
* Extract traversal and conditions into helpers (generators or pure functions).
* Use “soft-style” assertions for multiple checks by collecting failures and asserting once at the end of the test; keep all assertion logic in the test body.
* Avoid `if` statements in the test body; encode branching inside traversal helpers.
* Use loops in the test only to iterate over traversal outputs (no ad-hoc iteration over raw nested structures).
* Prefer parameterized tests (`@pytest.mark.parametrize`) to cover scenarios.
* Group initialization/related tests with nested classes or modules; use fixtures (`@pytest.fixture`) and `autouse` fixtures instead of per-test setup where possible.

Example — traversal + soft-style assertions (Python/pytest-idiomatic):

```python
import pytest

class NumberGeneratorService:
    def __init__(self, *, count: int, size: int, min: int, max: int) -> None:
        self.count = count
        self.size = size
        self.min = min
        self.max = max

    def generate_arrays(self) -> list[list[int]]:
        # Dummy implementation for illustration only
        import random

        result: list[list[int]] = []
        for _ in range(self.count):
            arr: list[int] = []
            while len(arr) < self.size:
                value = random.randint(self.min, self.max)
                if value not in arr:
                    arr.append(value)
            result.append(arr)
        return result


def number_generator_test_cases() -> list[tuple[int, int, int, int]]:
    return [
        (1, 5, 0, 10),
        (5, 5, 0, 10),
        (3, 1, 0, 10),
        (3, 5, 0, 10),
        (3, 1, 0, 0),
        (3, 5, 5, 10),
    ]


from typing import Generator, Iterable


def array_stream(result_arrays: Iterable[list[int]]) -> Generator[dict, None, None]:
    for array_index, array in enumerate(result_arrays):
        yield {"array_index": array_index, "array": array}


def value_stream(result_arrays: Iterable[list[int]]) -> Generator[dict, None, None]:
    for array_index, arr in enumerate(result_arrays):
        for value_index, value in enumerate(arr):
            yield {
                "array_index": array_index,
                "value_index": value_index,
                "value": value,
            }


@pytest.mark.parametrize(
    "count, size, range_min, range_max",
    number_generator_test_cases(),
    ids=lambda p: str(p),
)
def test_number_generator_service(count: int, size: int, range_min: int, range_max: int) -> None:
    # Arrange
    service = NumberGeneratorService(
        count=count,
        size=size,
        min=range_min,
        max=range_max,
    )

    # Act
    result = service.generate_arrays()

    # Assert (soft-style: collect all failures, assert once)
    errors: list[str] = []

    if len(result) != count:
        errors.append(f"expected {count} arrays, got {len(result)}")

    for item in array_stream(result):
        array_index = item["array_index"]
        array = item["array"]

        if len(array) != size:
            errors.append(f"array[{array_index}] length expected {size}, got {len(array)}")

    for item in value_stream(result):
        array_index = item["array_index"]
        value_index = item["value_index"]
        value = item["value"]

        if value < range_min:
            errors.append(
                f"min violation at [{array_index}][{value_index}]: "
                f"value {value} < {range_min}"
            )
        if value > range_max:
            errors.append(
                f"max violation at [{array_index}][{value_index}]: "
                f"value {value} > {range_max}"
            )

    for item in array_stream(result):
        array_index = item["array_index"]
        array = item["array"]
        distinct = len(set(array))
        if distinct != len(array):
            errors.append(
                f"duplicate values in array[{array_index}]: "
                f"{array} (distinct={distinct}, len={len(array)})"
            )

    assert not errors, ";\n".join(errors)
```

Notes:

* Assertions remain in the test; traversal helpers only expose structure (`array_stream`, `value_stream`).
* “Soft-style” behavior is implemented by collecting all failures into `errors` and asserting once; this surfaces all violations in one test run instead of failing fast on the first mismatch.
* Use `@pytest.mark.parametrize` when each tuple should produce a separate test; use shared fixtures when multiple tests need the same setup or FastAPI app/client.
* Prefer generator functions (`def [ELIDED] -> Generator[ELIDED]`) for traversals over building large intermediate lists to keep memory usage low and intent clear.
* For FastAPI routes, follow the same AAA and traversal principles when asserting on JSON responses, headers, and status codes (e.g., traverse response payloads via helpers instead of inline nested loops/ifs in the test body).
