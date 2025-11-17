**Purpose**
- Provide a deep dive into soft-style versus hard assertions in pytest, along with async testing patterns for FastAPI/httpx, common async pitfalls, and debugging strategies for failing async tests.

**Main Topics**
- Soft-style assertions (aggregate failures, report together) versus hard assertions (fail fast).
- Recommended soft-style pattern: collect error messages in a list and assert once at the end.
- Appropriate use of hard assertions for precondition checks before expensive or destructive operations.
- Interaction between soft-style patterns and static analysis tools (ruff, flake8, Sonar).
- Async testing patterns: separating awaited I/O from synchronous assertions.
- Correct patterns: `response = await async_client.get(...)` followed by normal `assert` on `response`.
- Incorrect patterns: missing `await`, passing coroutines into helpers, or asserting directly on coroutines.
- Common async pitfalls: unawaited coroutines, hanging tests, background tasks that outlive the test, and unclosed resources.
- Debugging tips: reduce timeouts, add explicit timeouts, inspect for unawaited coroutines, and use verbose pytest output.

**Opinions / Guidelines**
- Prefer soft-style assertions in pytest tests so multiple failures can be triaged at once.
- Reserve hard assertions for critical preconditions or guardrails before expensive or destructive steps.
- Always await async operations before making assertions; assertions themselves should remain synchronous.
- Use `@pytest.mark.asyncio` (or equivalent) for async tests.
- Avoid creating background tasks that outlive the scope of the test.
- Use well-scoped fixtures to manage async clients, database connections, and server processes.
- Add targeted linter suppression comments (for example `# noqa`) only when the soft-style pattern is intentional and correct.

**Assumptions**
- The project uses pytest together with pytest-asyncio for async tests.
- FastAPI is the primary web framework.
- `httpx.AsyncClient` is used for async endpoint testing.
- Developers are familiar with coroutines, `await`, and the event loop model.
- Linters such as ruff, flake8, or Sonar are configured via `pyproject.toml` or other config files.
- Shared fixtures manage client lifecycle (for example, an `async_client` fixture defined in `tests/conftest.py`).

**Staleness Indicators**
- Uses placeholder names such as `myapp.main` and `MyService` that do not exist in the current project.
- Does not reference concrete modules like `app/routes/metadata_router_v1.py` or `app/services/mcp_manager.py`.
- Does not explicitly cross-link to the async testing guidance already present in `docs/TEST.md`.
- Mentions linters and static analysis tools without tying them to the actual configuration in `pyproject.toml` or `.checkov.yaml`.

**Tags**
- `testing`, `pytest`, `soft-assertions`, `async`, `fastapi`, `httpx`, `pytest-asyncio`, `debugging`, `coroutines`, `test-patterns`, `linting`.

**Preliminary Target Docs**
- Primary: a consolidated `docs/testing-guide.md` or an extended `docs/TEST.md` that includes dedicated sections on soft-style assertions and async pitfalls.
- Secondary: a troubleshooting or debugging guide that surfaces the async failure investigation tips.

**Red Flags**
1. Strong advocacy for soft-style assertions conflicts with the predominately single-assert examples in `docs/TEST.md`, which may confuse contributors.
2. Soft-style assertion concepts overlap heavily with TEST_1, indicating these should be merged into a single canonical section.
3. Async testing patterns and pitfalls partially duplicate `docs/TEST.md` but add more detail, suggesting the need for careful integration to avoid contradictory advice.
4. References to linter behavior (ruff/flake8/Sonar) lack concrete configuration examples tied to this project’s `pyproject.toml`.
5. The document relies on generic service examples instead of real project code such as `app/services/mcp_manager.py`.
6. Mentions properly scoped fixtures without naming actual fixtures like `async_client` present in `tests/conftest.py`.
7. Background task handling guidance is high level and does not show concrete FastAPI background task testing patterns.
8. Debugging tips (timeouts, unawaited coroutine search) are not captured in current `docs/TEST.md`, so they risk being lost if TEST_2 is not integrated carefully.
9. The distinction between when to use hard versus soft assertions is described qualitatively but would benefit from concrete, project-specific examples.

**References**
- `docs/to_integrate/TEST_2.md`.
- `docs/TEST.md` (overlaps on async testing and FastAPI testing patterns).
- `docs/to_integrate/TEST_1.md` (overlaps on soft-style assertions).
- `tests/conftest.py` (source of async client fixtures implied by the document).
- `pyproject.toml` and `.checkov.yaml` (locations for linter and static analysis configuration).
- `app/routes/metadata_router_v1.py` and `app/services/mcp_manager.py` (candidates for concrete async test examples).
