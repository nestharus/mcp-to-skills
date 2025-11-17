**Purpose**
- Document the AAA (Arrange-Act-Assert) testing pattern with traversal rules, soft-style assertions, and parameterized testing for pytest-based test suites in FastAPI projects.

**Main Topics**
- AAA pattern enforcement (Arrange, Act, Assert in strict order).
- Traversal helpers (generators/pure functions) to extract structure from nested data.
- Soft-style assertions (collect all failures, assert once at end).
- Avoiding `if` statements in test bodies (encode branching in helpers instead).
- Parameterized tests with `@pytest.mark.parametrize`.
- Fixture composition and `autouse` fixtures.
- Example pattern: `NumberGeneratorService` with `array_stream` and `value_stream` traversal helpers.
- FastAPI-specific guidance for JSON response traversal.

**Opinions / Guidelines**
- Tests should follow AAA structure linearly with clear separation of concerns.
- Extract traversal logic into generator functions and keep assertions in the test body.
- Prefer soft-style error aggregation (e.g., accumulate messages in `errors: list[str]` and `assert not errors, ";".join(errors)`).
- Avoid `if` statements in test bodies; express branching through traversal helpers.
- Prefer generators over building large intermediate lists for traversal.
- Use `@pytest.mark.parametrize` to cover multiple scenarios compactly.
- Group related tests using nested classes or modules.
- Use `uv run pytest` as the standard entry point for tests.

**Assumptions**
- pytest is the primary test runner for the project.
- FastAPI is used as the web framework with `httpx.AsyncClient` or `TestClient` for HTTP tests.
- `uv` is the Python runtime/package manager used for running tests.
- Shared fixtures such as an application instance and HTTP clients are provided in `tests/conftest.py`.
- Developers are comfortable with generator functions and `yield` syntax.

**Staleness Indicators**
- Refers to generic fixtures in "this repo" without precise paths (assumes `tests/conftest.py` but does not name fixtures explicitly).
- Core example uses `NumberGeneratorService`, which is illustrative and not part of the actual project code.
- Does not reference concrete project modules like `app/contracts/metadata_contract.py` or `app/routes/metadata_router_v1.py`.
- Does not acknowledge existing testing docs such as `docs/TEST.md` or `docs/TESTING_ARCHITECTURE.md`.

**Tags**
- `testing`, `pytest`, `aaa`, `soft-assertions`, `traversal`, `parameterized-tests`, `fixtures`, `fastapi`, `generators`, `test-patterns`.

**Preliminary Target Docs**
- Primary: a consolidated `docs/testing-guide.md` or an extended `docs/TEST.md` that adds sections on AAA structure and soft-style assertions.
- Secondary: `docs/TESTING_ARCHITECTURE.md` for incorporating traversal helper patterns into overall testing structure.

**Red Flags**
1. Soft-style assertions are presented as required, while current `docs/TEST.md` mostly uses traditional single `assert` statements, creating inconsistency.
2. Generator-based traversal helpers (`array_stream`, `value_stream`) are not mentioned in existing testing docs, so the pattern could be overlooked.
3. Examples rely on `NumberGeneratorService` instead of real project types such as `MetadataItem` or request/response models used in metadata routes.
4. Soft-style assertion concepts are split between TEST_1 (introduction) and TEST_2 (deeper treatment), suggesting a need for consolidation.
5. References to shared fixtures are generic and do not align explicitly with actual fixtures such as `test_app`, `client`, or `async_client` in `tests/conftest.py`.
6. The document does not tie AAA guidance to the unit/integration/component test split described in `docs/TESTING_ARCHITECTURE.md`, leaving scope ambiguous.
7. Parameterization guidance overlaps with existing `docs/TEST.md` content but emphasizes different use cases.
8. FastAPI response traversal advice overlaps with `docs/TEST.md`'s FastAPI testing section and must be reconciled.

**References**
- `docs/to_integrate/TEST_1.md`.
- `docs/TEST.md` (overlaps on async testing, FastAPI patterns, and parametrization).
- `docs/TESTING_ARCHITECTURE.md` (overlaps on test structure and fixture usage).
- `tests/conftest.py` (source of shared fixtures referenced conceptually).
- `app/contracts/metadata_contract.py` and `app/routes/metadata_router_v1.py` (candidates for concrete testing examples).
