# Issue Classification Batch 2

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


ISS-0011: Error handling for TOML parsing or MCP initialization is only implied—no explicit remediation guidance.
Source: working/phase1/summaries/docs/LIFECYCLE.summary.md

ISS-0012: Cache implementation details live elsewhere (`app/core/settings.py`), so readers may miss nuance without cross-reference.
Source: working/phase1/summaries/docs/LIFECYCLE.summary.md

ISS-0013: Scope overlap with `docs/TESTING_ARCHITECTURE.md`—distinguish “how” vs “why” or merge carefully.
Source: working/phase1/summaries/docs/TEST.summary.md

ISS-0014: Fixture instructions duplicate details already encoded in code (`tests/conftest.py`), risking drift.
Source: working/phase1/summaries/docs/TEST.summary.md

ISS-0015: Component test guidance stops short of true E2E once real MCP subprocess support ships.
Source: working/phase1/summaries/docs/TEST.summary.md

ISS-0016: Potential conflicts with `docs/to_integrate/TEST_*.md` series that may contain divergent advice.
Source: working/phase1/summaries/docs/TEST.summary.md

ISS-0017: Reiterates information already present in `docs/TEST.md`; ensure boundaries between rationale vs execution remain clear.
Source: working/phase1/summaries/docs/TESTING_ARCHITECTURE.summary.md

ISS-0018: Historical note about `app/tests/` could confuse newcomers who never saw that layout; consider moving to a “history” appendix.
Source: working/phase1/summaries/docs/TESTING_ARCHITECTURE.summary.md

ISS-0019: Lacks guidance on exceptional cases (e.g., when an `__init__.py` might still be necessary for namespace packages).
Source: working/phase1/summaries/docs/TESTING_ARCHITECTURE.summary.md

ISS-0020: Major overlap with STYLE_6 on layered architecture, DI, and error handling; maintaining both separately risks drift.
Source: working/phase1/summaries/docs/to_integrate/api-patterns-guide.summary.md


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
