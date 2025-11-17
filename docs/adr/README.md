# Architectural Decision Records (ADRs)

This directory contains Architectural Decision Records (ADRs) for the project, using a lightweight Nygard-style format:

- **Context**: Background and forces influencing the decision.
- **Decision**: The concrete choice made.
- **Consequences**: Outcomes, trade-offs, and follow-ups.

All significant technical, architectural, and workflow decisions MUST be captured as ADRs under `docs/adr/`. When making a new decision that changes tooling, APIs, testing strategy, branching, or other cross-cutting concerns, add a new ADR file and update the index table below.

## ADR Index

| Number | Title                                           | Status  | Date       | Summary                                                | File                                       |
|--------|-------------------------------------------------|---------|------------|--------------------------------------------------------|--------------------------------------------|
| 0001   | Use Python 3.14+                                | Accepted| 2025-11-17 | Require Python 3.14+ and deprecate older versions      | `docs/adr/0001-use-python-3.14.md`         |
| 0002   | Adopt Trunk-Based Development                   | Accepted| 2025-11-17 | Standardize on trunk-based development for Git         | `docs/adr/0002-adopt-trunk-based-development.md` |
| 0003   | Keep Dual Virtual Environments                  | Accepted| 2025-11-17 | Retain `.venv` (WSL) and `.venv2` (Windows IDE)       | `docs/adr/0003-keep-dual-virtual-environments.md` |
| 0004   | OpenAPI Schema Regeneration is AI-Managed       | Accepted| 2025-11-17 | Delegate OpenAPI regeneration to AI-assisted workflows | `docs/adr/0004-openapi-regeneration-ai-managed.md` |
| 0005   | Standardize on Ruff for Linting and Formatting  | Accepted| 2025-11-17 | Use Ruff as the primary lint/format tool               | `docs/adr/0005-standardize-on-ruff.md`     |
| 0006   | E2E Testing Strategies with Testcontainers      | Accepted| 2025-11-17 | Use Testcontainers for E2E dependencies                | `docs/adr/0006-e2e-testing-strategies.md`  |
| 0007   | Defer /livez, /readyz, /startupz Contracts      | Accepted| 2025-11-17 | Keep `/health` interim; defer detailed probe contracts | `docs/adr/0007-defer-health-endpoint-contracts.md` |
| 0008   | Canonical Target Docs via Phase 2 IA            | Accepted| 2025-11-17 | Use Phase 2 IA as source of truth for docs             | `docs/adr/0008-canonical-target-docs-via-ia.md` |
| 0009   | Rename devpelopment-setup.md to development-setup.md | Accepted| 2025-11-17 | Fix typo and elevate development setup doc        | `docs/adr/0009-rename-devpelopment-setup.md` |
| 0010   | Adjust Inventory for test_fixtures_soft_and_e2e.py | Accepted| 2025-11-17 | Treat fixtures file as code example, not doc      | `docs/adr/0010-adjust-inventory-for-test-fixtures-py.md` |

For new ADRs, follow the naming pattern `NNNN-short-title.md`, incrementing `NNNN` and updating this table.
