# AGENTS.md Summary

## Purpose
Provide AI agents (and other automation) with repository-specific workflow rules covering dual virtual environments, CLI expectations, testing + linting requirements, documentation sync, and OpenAPI regeneration.

## Main Topics
- Dual virtual environments: `.venv` (WSL/Linux) vs `.venv2` (Windows/IDE) are both intentional and must stay intact.
- CLI-first tooling: prefer `uv run ...` commands that remain agnostic to interpreter paths so both environments work seamlessly.
- Testing mandate: after any code change, immediately run `uv run pytest` and `uv run lint` before hand-off.
- Documentation discipline: keep README and `docs/*.md` synchronized with actual behavior in the same change set.
- OpenAPI synchronization: regenerate `openapi/openapi.json` with `uv run gen_openapi --config tests/fixtures/sample_mcp.toml` whenever API signatures shift.

## Opinions/Guidelines
- Treat both venvs as valid; never delete/rename either or assume one is authoritative.
- Use CLI workflows to avoid hard-coding interpreter paths, ensuring parity between Windows and WSL workflows.
- Run lint + tests proactively (not just before commits) to keep branches healthy.
- Consider documentation part of the change, not an afterthought; update markdown references simultaneously.
- Always commit regenerated OpenAPI artifacts when API contracts evolve.

## Assumptions
- Project is often edited from both Windows (IDE) and WSL (CLI) contexts, necessitating dual venvs.
- `uv` is the canonical orchestration tool for installs, scripts, linting, and testing.
- Agents have access to `tests/fixtures/sample_mcp.toml` for schema generation.
- Markdown docs remain the primary reference format.

## Staleness Indicators
- None apparent; guidance reflects current dual-environment workflow and is unlikely to change unless tooling consolidates.

## Tags
`agents`, `workflow`, `dual-venv`, `windows`, `wsl`, `cli`, `testing`, `linting`, `documentation`, `openapi`

## Preliminary Target Docs
- Remains agent-specific (`AGENTS.md`), though overlapping advice (tests, docs, schema regen) might deserve duplication in contributor docs for humans.

## Red Flags
1. Dual-venv requirement can confuse newcomers who only read README; consider referencing this doc elsewhere.
2. Some instructions (“run tests after every change”) are general best practices rather than agent-exclusive guidance, raising question of duplicate ownership.
3. No troubleshooting guidance for diverging venv states or dependency drift between `.venv` and `.venv2`.
4. Manual OpenAPI regeneration remains error-prone; automation would reduce misses.

## References
- `AGENTS.md`
- `README.md`
- `docs/TEST.md`
- `openapi/openapi.json`
- `tests/fixtures/sample_mcp.toml`
