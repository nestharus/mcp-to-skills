# Issue Classification Batch 13

Please classify and assign an issue_type for the following 10 issues from the Phase 1 content analysis.

## Classification Guidelines

- **RESOLVED**: Issue is addressed by migration plan
  (in `working/phase2/migration_plan.md`) or ADR decisions
  (in `docs/adr/`). Provide ADR number or migration section reference.
- **CONFLICT**: Issue requires manual resolution in Phases 3-5.
  Assign to theme (Code Standards & Architecture, Testing & E2E,
  or Workflow/Releases/CI) based on
  `working/phase2/phase_theme_assignments.md`.
- **RESEARCH**: Issue requires external research (tool versions,
  best practices). Assign to research topic (Ruff Configuration,
  Python 3.14+ Features, Testing Patterns, E2E Infrastructure,
  FastAPI Best Practices, Versioning & Releases,
  CI/CD Automation).

## Context Files

- Migration plan: `working/phase2/migration_plan.md`
- Phase assignments: `working/phase2/phase_theme_assignments.md`
- ADRs: `docs/adr/*.md`

## Issues to Classify


ISS-0121: **Overlap with STYLE_1**: Type-hinting and docstring requirements repeat STYLE_1 guidance and should be centralized in a unified style guide.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0122: **OpenAPI tooling disconnect**: Discusses automatic OpenAPI generation but does not reference the actual tooling in this repo (`scripts/gen_openapi.py` and `openapi/openapi.json`), which should be aligned.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0123: **Testing patterns vs current tests**: Mentions DI-based testing strategies and dependency overrides, but does not reference the existing testing setup (`tests/conftest.py`, `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`), which already define how tests are structured.
Source: working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md

ISS-0124: **No FastAPI integration**: Guidance is written in framework-agnostic terms and does not reference FastAPI constructs like `HTTPException` or application-level exception handlers; this needs alignment with how errors are actually surfaced in `app/routes/metadata_router_v1.py` and related routers.
Source: working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md

ISS-0125: **Logging vs `print()`**: Examples rely on `print()` for error reporting, which is not appropriate for production services; these should be updated to use the project's logging approach.
Source: working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md

ISS-0126: **Custom exception placement**: The document does not specify where custom exceptions should be defined (for example, a shared `app/core/exceptions.py` module vs. per-feature exceptions); the project should standardize on a location and update references.
Source: working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md

ISS-0127: **Overlap with testing docs**: Error handling and custom exception patterns have implications for tests and fixtures, which may overlap with `docs/TEST.md` and `docs/to_integrate/TEST_*.md`; coordination is needed when integrating.
Source: working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md

ISS-0128: **Comment density guidance**: There is no explicit guidance on when not to comment (i.e., preferring self-documenting code) or how to avoid over-commenting; this may need to be clarified based on team preferences.
Source: working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md

ISS-0129: **Docstrings vs comments**: The relationship between inline comments and docstrings (outlined in STYLE_1) is not clarified; consolidated style docs should ensure these are consistent and non-contradictory.
Source: working/phase1/summaries/docs/to_integrate/STYLE_7.summary.md

ISS-0130: **`mypy` not installed**: STYLE_8's strong emphasis on `mypy` (strict mode, hooks, CI) is out of sync with the current project, which does not include `mypy` as a dependency or mention it in any primary docs; a decision is needed on whether to adopt `mypy` or remove/soften this guidance.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md


## Output Format

For each issue, provide both a workflow classification and an issue_type bucket:
```json
{
  "ISS-XXXX": {
    "classification": "RESOLVED|CONFLICT|RESEARCH",
    "classification_ref": "ADR-0001 | Migration §3.2 | Ruff Configuration",
    "issue_type": "Duplicates|Conflicts|Staleness|Gaps|Naming|Env|OpenAPI|Testing|Versioning|Health|Other",
    "notes": "Brief explanation"
  }
}
```
