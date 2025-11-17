# Open Questions (Phase 1)

- Which Python versions are officially supported, and what should `project.requires-python` be in `pyproject.toml`?
3.14
- Which branching strategy do we adopt (GitHub Flow or Trunk-Based Development) and what is our release branching policy?
Trunk
- Do we keep dual virtual environments (`.venv`, `.venv2`) or converge on a single documented workflow using `uv`?
.venv is standard BUT in multi OS environments you will have one .venv per OS. In this environment .venv is for WSL and .venv2 is for Windows.
.venv2 integrates with the IDE while .venv integrates with the terminal.
- Should OpenAPI schema regeneration be enforced via pre-commit, CI, or both, and where is the canonical `openapi.json` stored?
openapi.json is managed by AI. AI will regenerated it when needed per instructions files. It doesn't always need to be regenerated.
openapi.json is located at openapi/openapi.json
- Do we standardize on Ruff for linting and formatting and deprecate Black/isort in favor of `ruff format` and `ruff check --fix`?
We use ruff.
- What external dependencies should E2E tests exercise via Testcontainers (e.g., Postgres, Redis), and what data seeding policy do we use?
We should document strategies for postgresql, redis, localstack, docker containers etc.
Every test is responsible for its own data so that we know what data is present. We provide scripts to generate data.
- What are the exact contracts for `/livez`, `/readyz`, and `/startupz` endpoints and which checks run in each?
Contracts undefined at the moment.
- @router.get("/health")
  async def health_check() -> dict[str, str]:
  return {"status": "ok"}
I do not see /livez, /readyz, or /startupz in the codebase right now.
- What are the canonical target docs (file names & locations) for style, testing, API, architecture, and workflow?
Unknown
- Rename `docs/to_integrate/devpelopment-setup.md` to `development-setup.md` now or after Phase 2, and add redirects?
During phase 2 we will produce development-setup.md in the appropriate location.
- Either add the missing source files for: docs/to_integrate/test_fixtures_soft_and_e2e.md or remove their summaries. What is the decision?
The source is a .py file, not a .md file.