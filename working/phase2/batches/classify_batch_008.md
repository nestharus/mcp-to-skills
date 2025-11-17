# Issue Classification Batch 8

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


ISS-0071: Guidance recommends `--force-with-lease` but does not elaborate on risks of force-pushing or collaboration considerations.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0072: Assumes branch protection rules on `main` (required reviews, status checks) that are not documented in-repo.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0073: Commit message structure is described here and again in `docs/to_integrate/changesets-guide.md`, creating potential consistency drift.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0074: Pre-commit is described as lint-only here while other docs hint at broader automation; any change to hook scope must be synchronized across docs.
Source: working/phase1/summaries/docs/to_integrate/git-workflow.summary.md

ISS-0075: **Python version conflict**: STYLE_1 targets Python 3.14+, but `README.md` tech stack section may reference 3.12+ in some places—needs reconciliation.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md

ISS-0076: **Tooling ambiguity**: STYLE_1 lists multiple options (black OR ruff, mypy OR pyright OR pyre) but `README.md` and `AGENTS.md` only mention Ruff for formatting/linting—clarify project's actual tooling choices.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md

ISS-0077: **Type checker gap**: STYLE_1 mandates type checking in CI but `README.md` and `AGENTS.md` don't mention running mypy/pyright—determine if type checking is actually enforced.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md

ISS-0078: **Docstring style undecided**: STYLE_1 says "choose Google or NumPy" but doesn't specify which this project uses—audit existing code and document the decision.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md

ISS-0079: **Line length consistency**: Verify that `pyproject.toml` and Ruff configuration actually enforce 120-char limit mentioned in STYLE_1.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md

ISS-0080: **Import sorting**: STYLE_1 mentions isort or Ruff but `README.md` only mentions Ruff—confirm Ruff handles import sorting.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md


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
