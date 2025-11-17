# Open Questions (Phase 1)

All phase 1 questions have now been resolved and captured as Architectural Decision Records (ADRs) under `docs/adr/`. See the ADR index in `docs/adr/README.md` for full context.

## Summary Table

| Question # | ADR        | Status   |
|-----------:|-----------|----------|
| 1          | ADR-0001  | Resolved |
| 2          | ADR-0002  | Resolved |
| 3          | ADR-0003  | Resolved |
| 4          | ADR-0004  | Resolved |
| 5          | ADR-0005  | Resolved |
| 6          | ADR-0006  | Resolved |
| 7          | ADR-0007  | Resolved |
| 8          | ADR-0008  | Resolved |
| 9          | ADR-0009  | Resolved |
| 10         | ADR-0010  | Resolved |

Below, each original question is retained with its concise answer and an explicit resolution pointing at the corresponding ADR.

---

## Q1. Supported Python versions and `project.requires-python`

**Question**  
Which Python versions are officially supported, and what should `project.requires-python` be in `pyproject.toml`?

**Answer**  
3.14

**Resolution (ADR-0001 – Use Python 3.14+)**  
ADR-0001 specifies that the project requires Python 3.14+, with `project.requires-python` set to `">=3.14.0,<3.15.0"` and older versions are not supported.

---

## Q2. Branching strategy and release policy

**Question**  
Which branching strategy do we adopt (GitHub Flow or Trunk-Based Development) and what is our release branching policy?

**Answer**  
Trunk

**Resolution (ADR-0002 – Adopt Trunk-Based Development)**  
ADR-0002 standardizes on trunk-based development using short-lived feature branches merged rapidly into `main`, with releases cut from the trunk instead of long-lived release branches.

---

## Q3. Dual virtual environments vs single workflow

**Question**  
Do we keep dual virtual environments (`.venv`, `.venv2`) or converge on a single documented workflow using `uv`?

**Answer**  
`.venv` is standard but in multi-OS environments you will have one `.venv` per OS. In this environment `.venv` is for WSL and `.venv2` is for Windows. `.venv2` integrates with the IDE while `.venv` integrates with the terminal.

**Resolution (ADR-0003 – Keep Dual Virtual Environments)**  
ADR-0003 accepts dual environments as the official pattern, documenting `.venv` for WSL tooling and `.venv2` for Windows IDEs while preferring `uv run ...` workflows that do not hardcode interpreter paths.

---

## Q4. OpenAPI schema regeneration and canonical location

**Question**  
Should OpenAPI schema regeneration be enforced via pre-commit, CI, or both, and where is the canonical `openapi.json` stored?

**Answer**  
`openapi.json` is managed by AI. AI will regenerate it when needed per instruction files. It does not always need to be regenerated. `openapi.json` is located at `openapi/openapi.json`.

**Resolution (ADR-0004 – OpenAPI Schema Regeneration is AI-Managed)**  
ADR-0004 designates `openapi/openapi.json` as the canonical schema artifact and delegates regeneration to AI-assisted workflows (`uv run gen_openapi`), without enforcing it via pre-commit hooks.

---

## Q5. Standardizing on Ruff vs Black/isort

**Question**  
Do we standardize on Ruff for linting and formatting and deprecate Black/isort in favor of `ruff format` and `ruff check --fix`?

**Answer**  
We use Ruff.

**Resolution (ADR-0005 – Standardize on Ruff)**  
ADR-0005 makes Ruff the single source of truth for linting and formatting via `ruff format` and `ruff check --fix`, deprecating separate Black and isort tooling.

---

## Q6. E2E dependencies via Testcontainers and data seeding

**Question**  
What external dependencies should E2E tests exercise via Testcontainers (e.g., Postgres, Redis), and what data seeding policy do we use?

**Answer**  
We should document strategies for PostgreSQL, Redis, LocalStack, Docker containers, etc. Every test is responsible for its own data so that we know what data is present. We provide scripts to generate data.

**Resolution (ADR-0006 – E2E Testing Strategies with Testcontainers)**  
ADR-0006 records the strategy to use Testcontainers (for Postgres, Redis, and similar services) and to keep tests self-contained by owning their data setup, optionally supported by shared data-generation scripts.

---

## Q7. `/livez`, `/readyz`, `/startupz` contracts

**Question**  
What are the exact contracts for `/livez`, `/readyz`, and `/startupz` endpoints and which checks run in each?

**Answer**  
Contracts undefined at the moment.

```python
@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

I do not see `/livez`, `/readyz`, or `/startupz` in the codebase right now.

**Resolution (ADR-0007 – Defer Health Endpoint Contracts)**  
ADR-0007 formalizes that `/health` remains the interim probe endpoint and that detailed `/livez`, `/readyz`, and `/startupz` contracts are deferred until later phases.

---

## Q8. Canonical target docs and locations

**Question**  
What are the canonical target docs (file names & locations) for style, testing, API, architecture, and workflow?

**Answer**  
Unknown.

**Resolution (ADR-0008 – Canonical Target Docs via Phase 2 IA)**  
ADR-0008 assigns Phase 2 information architecture work to define the canonical target docs and locations, using those outputs as the source of truth for style, testing, API, architecture, and workflow documentation.

---

## Q9. Renaming `devpelopment-setup.md`

**Question**  
Rename `docs/to_integrate/devpelopment-setup.md` to `development-setup.md` now or after Phase 2, and add redirects?

**Answer**  
During phase 2 we will produce `development-setup.md` in the appropriate location.

**Resolution (ADR-0009 – Rename devpelopment-setup.md to development-setup.md)**  
ADR-0009 accepts the rename to `development-setup.md` and treats the Phase 2 information architecture as the moment to finalize the document’s location and any redirects.

---

## Q10. Handling `test_fixtures_soft_and_e2e`

**Question**  
Either add the missing source files for `docs/to_integrate/test_fixtures_soft_and_e2e.md` or remove their summaries. What is the decision?

**Answer**  
The source is a `.py` file, not a `.md` file.

**Resolution (ADR-0010 – Adjust Inventory for test_fixtures_soft_and_e2e.py)**  
ADR-0010 clarifies that `test_fixtures_soft_and_e2e.py` is a code example rather than a documentation page and updates the inventory to treat it accordingly.
