# STYLE issues plan for docs/to_integrate/STYLE_4.md

This plan is generated from `issues_index.csv` and is scoped to `docs/to_integrate/STYLE_4.md`.

## Relevant issues

| id | doc | line_no | description_text | issue_type | classification | classification_ref | notes |
|---|---|---|---|---|---|---|---|
| ISS-0098 | working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md | 38 | **External module reference**: Mentions `ui_designer.shared_types`, which does not exist in this repository and appears to come from another project. Either remove or replace with a project-appropriate shared types module if one is introduced. | Conflicts | CONFLICT | Code Standards & Architecture | Reference to ui_designer.shared_types points at a non-existent module in this repo and must be removed or replaced with an appropriate shared-types location when integrating STYLE_4 into docs/code-style-guide.md. |
| ISS-0099 | working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md | 39 | **Domain model mismatch**: Example types (`Project`, `ProjectStatus`, `DesignToken`) do not match the actual MCP metadata domain (`MetadataItem`, `FetchRequest`, etc.) defined in `app/contracts/metadata_contract.py`. | Staleness | CONFLICT | Code Standards & Architecture | Example domain types like Project and DesignToken in STYLE_4 are stale relative to the current MCP metadata models (e.g., MetadataItem, FetchRequest) and need updating during STYLE_4 → docs/code-style-guide.md migration to reflect the real contract in app/contracts/metadata_contract.py. |
| ISS-0100 | working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md | 40 | **Shared types assumption**: Assumes a shared types package for cross-service reuse, while this project is currently a single service with contracts living under `app/contracts/`. | Architecture | CONFLICT | Code Standards & Architecture | Assumption of a cross-service shared types package conflicts with the current single-service layout where contracts live under app/contracts/; architecture and style docs need to clarify if/when a shared types package will exist or drop that assumption. |
| ISS-0101 | working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md | 41 | **Overlap with STYLE_1**: Repeats naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE) already covered in STYLE_1; these should be consolidated into a single style guide section. | Duplicates | CONFLICT | Code Standards & Architecture | STYLE_4 naming rules will be merged into the single canonical `docs/code-style-guide.md` per Migration §2 (STYLE_1–8 merge), but the overlap with STYLE_1 still needs manual consolidation of sections and examples during the Code Standards & Architecture phase. |
| ISS-0102 | working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md | 42 | **Overlap with api-patterns-guide**: Domain modeling patterns overlap with the schemas and generics guidance in `docs/to_integrate/api-patterns-guide.md` and should be merged or cross-referenced. | Duplicates | CONFLICT | Code Standards & Architecture | Domain modeling and generics guidance from STYLE_4 and `api-patterns-guide` are both mapped into `docs/api.md` and `docs/code-style-guide.md` in Migration §2, yet it remains a red-flag duplication that must be resolved by hand when composing the target API/style docs. |
| ISS-0103 | working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md | 43 | **Missing linting enforcement**: Recommends naming conventions but does not describe how they are enforced; this should be aligned with the actual configuration in `pyproject.toml` and the Ruff setup. | Gaps | CONFLICT | Code Standards & Architecture | ADR-0005 (Ruff) and Migration §3 plan to standardize Ruff config in `pyproject.toml` and `.pre-commit-config.yaml`, but STYLE_4’s missing ‘how this is enforced’ section still requires manual alignment between the narrative style guide and the concrete Ruff rules. |
| ISS-0104 | working/phase1/summaries/docs/to_integrate/STYLE_4.summary.md | 44 | **Constants vs configuration**: Treats all UPPER_SNAKE_CASE values as constants without differentiating configuration that may come from environment or settings modules such as `app/core/settings.py`. | Conflicts | CONFLICT | Code Standards & Architecture | The simplistic treatment of all UPPER_SNAKE_CASE values as constants conflicts with configuration patterns tied to `app/core/settings.py` and environment-driven settings called out in Migration §3; this needs an explicit rule in the consolidated `docs/code-style-guide.md` during Code Standards & Architecture work. |

## Instructions

For each issue listed above:

- Open `docs/to_integrate/STYLE_4.md`.
- Confirm whether the described problem is still present.
- If it is still present, edit `docs/to_integrate/STYLE_4.md` to resolve it, aligning with current ADRs, `pyproject.toml`, and the consolidated `docs/code-style-guide.md`.
- If it has already been resolved, ensure the intent of the fix remains clear and that no contradictory guidance remains.

Focus only on the concerns described in these issues; do not introduce unrelated changes.
