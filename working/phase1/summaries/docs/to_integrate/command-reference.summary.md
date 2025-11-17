**Purpose**
- Document the comprehensive `uv`-based command reference for the MCP Metadata Broker project, covering setup, daily development workflows, testing, linting, OpenAPI generation, Docker operations, and troubleshooting.

**Main Topics**
- Project setup: installing `uv`, creating/activating virtual environments, syncing dependencies, and running `uv run mcp-setup` to install dev tools and pre-commit hooks.
- Daily development commands: running the dev server with `uv run uvicorn --reload`, production-style server via `uv run start-server`, executing `uv run pytest` for tests, and using `uv run lint` for linting/formatting.
- Other common commands: generating OpenAPI via `uv run gen_openapi --config <config> [--allow-missing-config]`, managing sample configs, and running project scripts defined in `pyproject.toml`.
- Docker workflows: building the image, running the container with config file mounting (read-only), and mapping ports for local development.
- Troubleshooting: handling missing dev dependencies, resolving venv/`uv` issues, and explaining the rationale for always using `uv run`.
- Environment/venv context: WSL vs Windows dual-venv setup (`.venv` and `.venv2`), with guidance to keep both directories.

**Opinions / Guidelines**
- Prefer `uv run <command>` for all project tasks to ensure consistent, project-pinned tool versions and avoid global-tool drift.
- After `uv sync`, always run `uv run mcp-setup` to install dev tooling, pre-commit hooks, and ensure a fully functional local environment.
- Use `uvicorn --reload` for local development and rely on project-provided scripts (e.g., `start-server`) for production-like runs.
- Regenerate and commit `openapi/openapi.json` via `uv run gen_openapi --config tests/fixtures/sample_mcp.toml` whenever API contracts change.
- When using Docker, mount configuration TOML files read-only and avoid baking secrets into the image.
- Never delete `.venv` or `.venv2`; treat both as intentional and required for dual WSL/Windows development.

**Assumptions**
- `uv` is installed globally and available on the developer's PATH.
- Developers have an active virtual environment (or rely on `uv`'s environment management) before running commands.
- `MCP_CONFIG_PATH` points to a valid TOML configuration file, or `--allow-missing-config` is used for workflows that tolerate absent config.
- Docker is installed and available for container-based workflows.
- `pyproject.toml` defines `project.scripts` entries (e.g., `lint`, `gen_openapi`, `mcp-setup`, `start-server`) that match the documented commands.

**Staleness Indicators**
- "From scratch" setup instructions may diverge from reality as the project and tooling evolve (e.g., new scripts, additional dependencies).
- Docker examples assume specific ports and paths which may change as deployment conventions solidify.
- Troubleshooting tips focus on early-phase issues such as missing dev dependencies; over time, runtime/configuration errors may become more relevant.
- The doc does not yet reference future CI/CD or deployment workflows, which may introduce new canonical commands.

**Tags**
- tooling, commands, uv, cli, setup, development, testing, linting, openapi, docker, troubleshooting, workflow

**Preliminary Target Docs**
- Recommend keeping this content as a standalone `docs/command-reference.md` because it serves as a dense, reference-style catalog of commands that developers will consult frequently.
- Setup and workflow sections can inform a shorter overview in `README.md` and a future `docs/development-setup.md`, but detailed flags/options should remain here.

**Red Flags**
- Overlap with `README.md`: setup, quality, OpenAPI, and run commands largely duplicate README sections; README should likely link here instead of repeating details.
- Overlap with `docs/to_integrate/linting-guide.md`: the Linting & Formatting section restates Ruff usage that is better owned by the linting guide.
- Overlap with `STYLE_8` tooling guidance: pre-commit and `uv run lint` workflows are described in multiple places, risking divergence.
- Dual-venv (`.venv` / `.venv2`) context is mentioned but not deeply explained; coordination with `AGENTS.md` is required to avoid confusion.
- `gen_openapi` examples rely on `tests/fixtures/sample_mcp.toml` without clearly distinguishing between sample and real config usage.
- Docker volume-mount examples use placeholder paths and do not explain config discovery or secret-handling patterns.
- CI commands are absent; there is no clear mapping between this reference and the actual CI workflows used in the repo.
- `uv run hatch build` is mentioned without explaining when/why to build, which may confuse developers unfamiliar with packaging flows.
- No explicit Python version requirement is stated here, which may drift from `README.md` and `pyproject.toml` versions.
- Troubleshooting scenarios focus on local environment issues but do not cover config validation failures or runtime errors that may become common.

**References**
- `docs/to_integrate/command-reference.md` (source of detailed commands and explanations).
- `README.md` (overlapping setup, run, and quality sections).
- `AGENTS.md` (dual-venv WSL/Windows context and `uv run` conventions).
- `docs/to_integrate/linting-guide.md` (overlapping lint/linting philosophy content).
- `pyproject.toml` (script definitions and tool configuration).
- `.pre-commit-config.yaml` (pre-commit hook configuration matching `uv run lint`).
- `scripts/start-server.py` (production server entrypoint used by documented commands).
- `tools/gen_openapi.py` (implementation backing `uv run gen_openapi`).
- `Dockerfile` (container build configuration relevant for Checkov and Docker workflows).
