**Purpose**: Document the comprehensive first-time onboarding guide covering prerequisites, step-by-step setup (clone, install uv, create venv, install dependencies), verification steps (linting, testing, server health check), editor configuration (VS Code interpreter selection), project structure overview, troubleshooting (dual venv, missing commands), and next-steps links.

**Main Topics**:
- Prerequisites: Python 3.14, uv, Git, Docker (optional)
- Initial setup: clone repo, install uv, create/activate venv with `uv venv`, install deps with `uv sync` + `uv run mcp-setup`
- Verification: `uv run lint`, `uv run pytest`, `uv run uvicorn app.main:app --reload`, health endpoint check at `/api/metadata/v1/health`
- VS Code configuration: selecting `.venv` interpreter for linting/testing integration
- Project structure: `app/`, `scripts/`, `docs/`, `tests/`, `openapi/`, `pyproject.toml`
- Troubleshooting: missing commands (forgot `mcp-setup`), uv not in PATH, dual venv explanation (`.venv` for WSL, `.venv2` for Windows)
- Next steps: links to Command Reference, LIFECYCLE.md, TEST.md

**Opinions/Guidelines**:
- Use `uv` as the canonical package/environment manager
- Two-step dependency install: `uv sync` (main deps) then `uv run mcp-setup` (dev tools + pre-commit hooks)
- Always activate the correct venv for your shell (WSL vs Windows)
- Select the `.venv` interpreter in VS Code for tool integration
- Verify setup with lint, tests, and server health check before starting development
- Dual venvs (`.venv` and `.venv2`) are intentional, not errors

**Assumptions**:
- Developers are using VS Code with the Python extension
- Project targets Python 3.14 exclusively
- `uv` is installed and in PATH
- Developers may switch between Windows and WSL environments
- Pre-commit hooks are opt-in via `mcp-setup` script
- Health endpoint at `/api/metadata/v1/health` is available for verification

**Staleness Indicators**:
- References "mcp-metadata-broker" as the project name, but repo is "mcp-to-skills"—verify project name consistency
- Links to guides (Command Reference, LIFECYCLE.md, TEST.md) that exist but may not be in final form
- No mention of Phase 2 or future features, suggesting doc is current for Phase 1
- Troubleshooting section is minimal; may need expansion as common issues emerge

**Tags**: `setup`, `onboarding`, `prerequisites`, `uv`, `venv`, `python314`, `vscode`, `troubleshooting`, `dual-venv`, `development`, `getting-started` (intentionally omits `index` because this doc is a workflow guide, not a documentation hub)

**Preliminary Target Docs**:
- Primary target: Merge into root `README.md` setup section OR create standalone `docs/development-setup.md` (recommended to reduce README bloat)
- If standalone, link from root README's "Documentation" section and from `docs/README.md` index (once integrated)
- Dual-venv troubleshooting overlaps with `AGENTS.md`—consider cross-referencing or consolidating in a troubleshooting guide

**Red Flags** (8-10 specific issues):
1. **Major overlap with root README.md**: Prerequisites, `uv sync` + `mcp-setup` steps, project structure, `uv run lint`, `uv run pytest`, `uv run uvicorn` command, health endpoint, Docker—nearly 60% duplication. Consolidate in Phase 2.
2. **Project name mismatch**: Doc references "mcp-metadata-broker" but repo is "mcp-to-skills"—update all references for consistency.
3. **Dual-venv explanation**: Troubleshooting section explains `.venv` vs `.venv2`, which overlaps with `AGENTS.md` guidance—decide if this belongs in developer docs or remains agent-specific.
4. **VS Code-centric**: Assumes VS Code as the primary editor; consider adding brief notes for other IDEs (PyCharm, Vim, etc.) or making editor section optional.
5. **Missing verification details**: Health endpoint check shows "you will see a JSON response" but doesn't specify expected structure—add example response for clarity.
6. **Incomplete next-steps links**: References "Command Reference" and "Testing Guide" without full paths—verify these docs exist and provide accurate links.
7. **No mention of Phase 2**: Doc is current for Phase 1 but doesn't hint at future features (DB, caching, orchestration)—consider adding a "Roadmap" or "Future Features" section.
8. **Troubleshooting gaps**: Only covers 3 issues (missing commands, uv not found, dual venv)—expand with common errors like port conflicts, config path issues, or dependency resolution failures.
9. **Pre-commit hook explanation**: Mentions `mcp-setup` installs hooks but doesn't explain what they do or how to skip them—add brief description or link to `.pre-commit-config.yaml`.
10. **Docker section missing**: Root README covers Docker build/run but this doc only mentions Docker as optional prerequisite—add Docker workflow section or link to root README.

**References**:
- `docs/to_integrate/devpelopment-setup.md` (source)
- `README.md` (overlaps: prerequisites, setup, structure, commands)
- `AGENTS.md` (dual-venv guidance)
- `docs/LIFECYCLE.md` (linked in next steps)
- `docs/TEST.md` (linked in next steps)
- `pyproject.toml` (implied for dependency management)
- `.pre-commit-config.yaml` (pre-commit hooks)
- `app/main.py` (FastAPI app entry point)
- `tests/fixtures/sample_mcp.toml` (config for OpenAPI generation)
