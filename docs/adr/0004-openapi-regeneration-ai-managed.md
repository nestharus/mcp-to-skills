# ADR 0004: OpenAPI Schema Regeneration is AI-Managed

## Context

The project exposes an API whose schema is captured in `openapi/openapi.json`. Keeping this schema in sync with the FastAPI routes and models is essential, but fully automating regeneration in pre-commit or CI can be brittle and slow. The repository is routinely edited with AI assistance, which can reliably run the regeneration command when API changes occur.

## Decision

- Treat `openapi/openapi.json` as the canonical OpenAPI specification.
- Regenerate the schema via `uv run gen_openapi --config tests/fixtures/sample_mcp.toml` when API contracts change.
- Do not enforce regeneration via pre-commit hooks; instead, rely on AI-assisted workflows and CI checks that can detect obvious drift when needed.

## Consequences

- Provides flexibility for iterative API development while keeping the schema up to date.
- Avoids pre-commit friction where regeneration might be slow or environment-dependent.
- Places responsibility on maintainers and AI agents to remember regeneration as part of API changes.

## References

- `openapi/openapi.json`
- `tools/gen_openapi.py` and `scripts/gen_openapi.py`
- `docs/api.md` (API contracts) and `docs/workflow-and-ci.md` (workflow notes)
