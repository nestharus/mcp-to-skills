# STYLE_4.md Summary

## Purpose
Document naming conventions and domain model patterns for Python/FastAPI projects, emphasizing Pydantic models, enums, and consistent naming across variables, functions, classes, and constants.

## Main Topics
- Domain models using shared Pydantic models and enums for type-safe entity modeling.
- Naming conventions: snake_case for variables/functions, PascalCase for classes/models/enums, UPPER_SNAKE_CASE for constants.
- FastAPI integration examples using these domain models in request/response schemas.
- Type-safe status checks and enum usage patterns for clearer business logic.

## Opinions/Guidelines
- Use shared Pydantic models and enums for consistency across services.
- Prefer descriptive names over abbreviations.
- Avoid camelCase in Python; use snake_case for variables and functions.
- Reserve UPPER_SNAKE_CASE for values that are truly constant.
- Rely on type hints to enable better tooling, IDE support, and static checks.

## Assumptions
- The project has or will have a shared types module (for example, `ui_designer.shared_types`) for cross-service consistency.
- Developers are familiar with Pydantic v2 models and FastAPI request/response patterns.
- Naming conventions are enforced via linting tools such as Ruff or pylint.
- These conventions are intended to apply project-wide rather than per-module.

## Staleness Indicators
- References a `ui_designer.shared_types` module that does not exist in this project, suggesting content was copied from a different codebase.
- Uses domain examples like `ProjectId`, `ProjectStatus`, and `DesignToken` that do not appear in the current MCP metadata domain.
- Does not reference the actual domain models in this project (for example, `MetadataItem`, `FetchRequest`, and related contracts in `app/contracts/metadata_contract.py`).
- Provides generic guidance without project-specific examples tied to the current API surface.

## Tags
`style`, `naming`, `conventions`, `pydantic`, `domain-models`, `enums`, `type-safety`, `fastapi`, `snake-case`, `pascal-case`

## Preliminary Target Docs
Most of this content likely belongs in a consolidated `docs/code-style-guide.md` under a naming conventions and domain modeling section. The domain model patterns may also be integrated into the schemas section of `docs/to_integrate/api-patterns-guide.md` or a future `docs/domain-modeling-guide.md`.

## Red Flags
1. **External module reference**: Mentions `ui_designer.shared_types`, which does not exist in this repository and appears to come from another project. Either remove or replace with a project-appropriate shared types module if one is introduced.
2. **Domain model mismatch**: Example types (`Project`, `ProjectStatus`, `DesignToken`) do not match the actual MCP metadata domain (`MetadataItem`, `FetchRequest`, etc.) defined in `app/contracts/metadata_contract.py`.
3. **Shared types assumption**: Assumes a shared types package for cross-service reuse, while this project is currently a single service with contracts living under `app/contracts/`.
4. **Overlap with STYLE_1**: Repeats naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE) already covered in STYLE_1; these should be consolidated into a single style guide section.
5. **Overlap with api-patterns-guide**: Domain modeling patterns overlap with the schemas and generics guidance in `docs/to_integrate/api-patterns-guide.md` and should be merged or cross-referenced.
6. **Missing linting enforcement**: Recommends naming conventions but does not describe how they are enforced; this should be aligned with the actual configuration in `pyproject.toml` and the Ruff setup.
7. **Constants vs configuration**: Treats all UPPER_SNAKE_CASE values as constants without differentiating configuration that may come from environment or settings modules such as `app/core/settings.py`.

## References
- `docs/to_integrate/STYLE_4.md` (source document).
- `working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md` (overlapping naming guidance).
- `app/contracts/metadata_contract.py` (actual domain models used by the service).
- `docs/to_integrate/api-patterns-guide.md` (overlapping schemas and domain modeling patterns).
- `pyproject.toml` (implied, for linting and naming enforcement configuration).
