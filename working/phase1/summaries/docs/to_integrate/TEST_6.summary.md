## Purpose
- Capture async and callback-based testing patterns from `docs/to_integrate/TEST_6.md`, focusing on pytest-based strategies for testing `async` functions and bridging callback-style async code into an async/await testing model.

## Main Topics
- Using `@pytest.mark.asyncio` (or equivalent configuration) to run async test functions under pytest.
- Testing successful async flows by `await`-ing the function under test and asserting on results.
- Testing async error paths with `pytest.raises` wrapped around awaited calls.
- Adapting callback-based async APIs into tests using `asyncio.Future` or similar primitives to await completion.
- Handling errors in async contexts, including propagating exceptions from callbacks into the test's async flow.

## Opinions / Guidelines
- Treat async tests as first-class citizens, using pytest-asyncio (or native async support when configured) to avoid blocking patterns.
- Use `pytest.raises(ExpectedException, match="...")` with `await` inside the context manager when validating async failures.
- Prefer bridging callback-style code to async/await in tests via `asyncio.Future` (or similar) rather than relying on arbitrary sleeps or polling.
- Keep async examples small and focused, using simulated work like `asyncio.sleep(0)` when needed for illustration rather than real I/O.
- Strive for consistent error-handling patterns in async code (for example, domain errors expressed as specific exception types).

## Assumptions
- pytest-asyncio (or equivalent async plugin) is installed and configured for this project.
- The primary async runtime is `asyncio`, not alternative frameworks like trio or anyio.
- The project already uses async constructs in FastAPI routes, HTTP clients, or MCP-related subprocess calls, making async testing patterns broadly applicable.
- Developers are familiar with basic async/await syntax and comfortable with event-loop concepts.

## Staleness Indicators
- Examples use placeholder functions such as `fetch_user_async` and `fetch_user_callback` rather than current project-specific async entry points (for example, MCP manager calls or async FastAPI routes).
- The document does not reference existing async fixtures (such as an `async_client` or app factory) that are defined in `tests/conftest.py`.
- There is no explicit mention of FastAPI-specific testing patterns (for example, using `httpx.AsyncClient` or `TestClient`) that are already part of this repository's testing approach.
- Callback-based patterns may be less relevant if the codebase has fully standardized on async/await rather than callbacks; this should be validated before heavy integration.
- Error-handling examples rely on generic exception types and messages that may not align with the project's existing error taxonomy.

## Tags
- testing, pytest, async, pytest-asyncio, asyncio, callbacks, promises, error-handling, async-await, future

## Preliminary Target Docs
- Primary: extend the async testing section of `docs/TEST.md` with richer examples, including callback-bridging patterns where they match real project use cases.
- Secondary: a broader testing reference (for example, `docs/testing-guide.md`) that groups all async-specific guidance (routes, services, MCP calls) in one place.
- Callback-based material should be incorporated only where the project actually uses callbacks; otherwise it can be reduced to a brief pattern reference.

## Red Flags / Integration Risks
- Async testing guidance overlaps with existing `docs/TEST.md` content; TEST_6 adds detail (especially around callbacks) that needs consolidation to avoid duplication.
- Generic examples must be replaced with project-specific scenarios (for example, testing async route handlers or MCP manager behaviors) to be truly useful.
- If the project does not employ callback-style async code, overemphasizing callback patterns may confuse contributors and distract from the dominant async/await style.
- Lack of integration with current async fixtures and app factories might lead to parallel, inconsistent testing patterns if incorporated naively.
- Error-handling and exception examples must be harmonized with the project's actual exception types and error responses (especially for FastAPI endpoints).
- Any mention of event-loop management must respect pytest-asyncio's configuration and avoid conflicting with how the project currently starts and manages the loop.

## References
- `docs/to_integrate/TEST_6.md`
- `docs/TEST.md` (existing async testing guidance)
- `tests/conftest.py` (async fixtures and app/client factories)
- `app/services/mcp_manager.py` (async or subprocess patterns that may benefit from these tests)
- `app/routes/metadata_router_v1.py` (async route handlers)
