# Issue Classification Batch 9

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


ISS-0081: **Testing overlap**: STYLE_1's testing section duplicates content in `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md`—consolidate in Phase 2.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md

ISS-0082: **Lazy annotations**: STYLE_1 discusses PEP 649 implications but doesn't provide concrete examples of runtime introspection patterns—may need expansion.
Source: working/phase1/summaries/docs/to_integrate/STYLE_1.summary.md

ISS-0083: **Overlap with STYLE_1**: Significant content duplication with `docs/to_integrate/STYLE_1.md` on typing, annotations, and Python 3.14 features—consolidate in Phase 2.
Source: working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md

ISS-0084: **Draft status**: Document appears to be a conversion/adaptation rather than finalized guidance ("if you like, I can generate[ELIDED]").
Source: working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md

ISS-0085: **Missing examples**: No concrete examples of `annotationlib.get_annotations()` usage or runtime introspection patterns.
Source: working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md

ISS-0086: **TypeScript heritage**: Some phrasing suggests direct translation from TypeScript docs rather than Python-native guidance.
Source: working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md

ISS-0087: **Incomplete coverage**: Focuses narrowly on annotation decisions without broader style context covered in STYLE_1.
Source: working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md

ISS-0088: **No conflict with existing docs**: Unlike STYLE_1, doesn't introduce tooling or conventions that contradict `README.md`/`AGENTS.md`.
Source: working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md

ISS-0089: **Overlap with to_integrate docs**: Content overlaps with `docs/to_integrate/api-patterns-guide.md` and `docs/to_integrate/fastapi-best-practices.md`—consolidate in Phase 2.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md

ISS-0090: **Draft status**: Document appears to be a conversion from TypeScript guidance rather than finalized Python/FastAPI documentation.
Source: working/phase1/summaries/docs/to_integrate/STYLE_3.summary.md


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
