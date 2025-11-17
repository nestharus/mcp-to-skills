# Agent Notes

This file summarizes agent-specific guidance and points at key Architectural Decision Records (ADRs) under `docs/adr/` for full context.

- This repository may include multiple virtual environment directories. `.venv` corresponds to the Linux (WSL) toolchain, while `.venv2` points to the Windows interpreter that the host IDE uses. Windows paths typically reference `.venv2`, and WSL tooling (including `uv run [ELIDED]`) points at `.venv`. This dual-venv strategy is captured in `docs/adr/0003-keep-dual-virtual-environments.md`.
- Treat both directories as intentional. Do not delete or rename them, and assume either may contain valid interpreter state depending on which side (Windows vs. WSL) last executed `uv`.
- When updating documentation or scripts, prefer CLI workflows (`uv run [ELIDED]`) that do not assume a specific interpreter path so both environments continue to work without extra steps, aligning with the dual-venv guidance in ADR-0003.
- After making any code changes, immediately run `uv run pytest` and `uv run lint` so regressions, lint issues, and formatting problems are caught before handing work off. Ruff is the standardized lint/format tool as described in `docs/adr/0005-standardize-on-ruff.md`.
- Keep the markdown reference docs (README, docs/*.md, etc.) synchronized with the project's actual patterns, structure, and conventions—whenever behavior, workflows, or best practices change, update both the code and the documentation in the same pass and let later reviewers correct any mistakes discovered.
- Whenever changing API signatures or adding endpoints, regenerate the OpenAPI schema (`uv run gen_openapi --config tests/fixtures/sample_mcp.toml`) and commit the resulting `openapi/openapi.json` updates so docs stay in sync. OpenAPI regeneration is treated as an AI-managed artifact per `docs/adr/0004-openapi-regeneration-ai-managed.md`.
- When working with branches, follow the trunk-based development approach documented in `docs/adr/0002-adopt-trunk-based-development.md` (short-lived branches, frequent integration into `main`).

For a complete list of architectural and workflow decisions, see the ADR index in `docs/adr/README.md`.
