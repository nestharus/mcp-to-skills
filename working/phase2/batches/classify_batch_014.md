# Issue Classification Batch 14

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


ISS-0131: **Pre-commit configuration mismatch**: The recommended multi-repo pre-commit setup conflicts with the actual `.pre-commit-config.yaml`, which relies on a single `local` hook running `uv run lint`; documentation and configuration must be reconciled to avoid confusion.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0132: **Script section mismatch**: The use of `[tool.uv.scripts]` in examples does not match the project's current `[project.scripts]` usage; STYLE_8 should be updated to reflect how `uv` is actually invoked here.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0133: **Duplicate tooling documentation**: STYLE_8 substantially overlaps with `docs/to_integrate/linting-guide.md` and the `README.md` Code Quality section; Phase 2 integration should merge these into a single, authoritative description of the tooling stack.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0134: **Version drift**: Hard-coded tool versions in STYLE_8 do not match `pyproject.toml` and will quickly become outdated; examples should either be updated or rewritten to be version-agnostic.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0135: **Import ordering overlap**: Import ordering guidance duplicates content from STYLE_1 and other style docs; consolidated style documentation should avoid conflicting rules and pick a single source of truth.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0136: **Workflow inconsistency**: STYLE_8's narrative of separate `format` and `lint` commands differs from the reality that `uv run lint` (via `scripts/lint.py`) already executes formatting; documentation should clarify that a single command is the canonical workflow.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0137: **Missing Ruff config details**: STYLE_8 mentions that Ruff is configured via `pyproject.toml` but does not reflect this repository's actual settings (e.g., 100-character line length); integrated docs should reference the concrete configuration.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0138: **`TYPE_CHECKING` imports context**: While TYPE_CHECKING usage is shown, the rationale (avoiding import cycles and runtime costs) is only lightly touched on; integration work should ensure this guidance is connected to broader import and typing patterns from other style docs.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0139: **CI integration specifics**: STYLE_8 vaguely recommends adding `uv run lint` to CI without showing concrete CI configuration; this must be coordinated with `docs/to_integrate/git-workflow.md` and the project's actual CI workflows.
Source: working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md

ISS-0140: Major duplication with `docs/to_integrate/e2e-testing-guide.md`: both documents cover E2E testing for FastAPI, health checks, live server fixtures, and httpx usage, but the existing guide is project-specific while TEST_7 is generic/tutorial-style.
Source: working/phase1/summaries/docs/to_integrate/TEST_7.summary.md


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
