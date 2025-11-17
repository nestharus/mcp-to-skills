# Issue Classification Batch 5

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


ISS-0041: The dependency version drift section refers to context7-based lookup without explaining the actual usage pattern or any local tooling for it.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0042: The guide notes the repo is not a monorepo but still hints at multi-package coordination, which could confuse contributors.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0043: Mentions `uv sync` and other setup commands that may already be described in `README.md`, leading to duplicated setup guidance.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0044: Tagging instructions (e.g., `git tag -a v1.3.0`) may conflict with or duplicate tagging guidance in `docs/to_integrate/git-workflow.md`.
Source: working/phase1/summaries/docs/to_integrate/changesets-guide.summary.md

ISS-0045: Significant overlap with `README.md` "Code Quality" section, which already describes `uv run lint`, formatting, and pre-commit hooks.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0046: Overlap with `docs/to_integrate/git-workflow.md` around the "run checks before commit" step; they disagree on whether to exclude E2E tests in the default loop.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0047: References `uv run mcp-setup` without explaining what it does or where it is defined, even though initial setup is described in `README.md`.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0048: Describes pre-commit as lint-only while some sections imply broader automation; this must stay aligned with `.pre-commit-config.yaml`.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0049: Mandates regenerating OpenAPI on API changes but does not explain how to validate the generated schema or handle generation failures.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md

ISS-0050: Encourages TDD and mirroring `app/` in `tests/` but `docs/TESTING_ARCHITECTURE.md` may already define a more precise structure, risking conflicting advice.
Source: working/phase1/summaries/docs/to_integrate/development-workflow.summary.md


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
