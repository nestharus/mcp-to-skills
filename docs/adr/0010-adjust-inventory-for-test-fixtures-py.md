# ADR 0010: Adjust Inventory for test_fixtures_soft_and_e2e.py

## Context

The Phase 1 documentation inventory listed `docs/to_integrate/test_fixtures_soft_and_e2e.py` as if it were a markdown document, but the file is Python code containing fixture examples. Its content is valuable for testing guidance but should not be treated as a standalone documentation page.

## Decision

- Treat `docs/to_integrate/test_fixtures_soft_and_e2e.py` as example code, not as a documentation source.
- Reference its patterns and snippets in `docs/testing-guide.md` when documenting fixtures and soft assertions.
- Exclude it from future documentation inventories that are intended to track markdown docs.

## Consequences

- Keeps the documentation inventory accurate and focused on actual docs.
- Encourages reuse of the example code without duplicating it as prose.
- Allows the testing guide to evolve while keeping the underlying examples in code.

## References

- `docs/testing-guide.md` (fixtures and E2E sections)
- `docs/to_integrate/test_fixtures_soft_and_e2e.py` (example code)
