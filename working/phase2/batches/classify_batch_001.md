# Issue Classification Batch 1

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


ISS-0001: Dual-venv requirement can confuse newcomers who only read README; consider referencing this doc elsewhere.
Source: working/phase1/summaries/AGENTS.summary.md

ISS-0002: Some instructions (“run tests after every change”) are general best practices rather than agent-exclusive guidance, raising question of duplicate ownership.
Source: working/phase1/summaries/AGENTS.summary.md

ISS-0003: No troubleshooting guidance for diverging venv states or dependency drift between `.venv` and `.venv2`.
Source: working/phase1/summaries/AGENTS.summary.md

ISS-0004: Manual OpenAPI regeneration remains error-prone; automation would reduce misses.
Source: working/phase1/summaries/AGENTS.summary.md

ISS-0005: Setup, linting, and API-reference sections overlap with multiple `docs/to_integrate/*.md` guides—dedupe in later phases.
Source: working/phase1/summaries/README.summary.md

ISS-0006: OpenAPI and health check details repeat information already kept in schema + lifecycle doc; risk of inconsistencies.
Source: working/phase1/summaries/README.summary.md

ISS-0007: No explicit mention of dual-venv nuance described in `AGENTS.md`, so new contributors may miss important context.
Source: working/phase1/summaries/README.summary.md

ISS-0008: “Future steps” blur current vs planned capabilities, potentially misleading readers about what exists today.
Source: working/phase1/summaries/README.summary.md

ISS-0009: Heavy dependence on future Phase 2 work increases staleness risk if not promptly updated.
Source: working/phase1/summaries/docs/LIFECYCLE.summary.md

ISS-0010: Health check guidance overlaps with README and schema docs; divergence likely without consolidation.
Source: working/phase1/summaries/docs/LIFECYCLE.summary.md


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
