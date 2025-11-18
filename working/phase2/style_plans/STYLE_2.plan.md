# STYLE issues plan for docs/to_integrate/STYLE_2.md

This plan is generated from `issues_index.csv` and is scoped to `docs/to_integrate/STYLE_2.md`.

## Relevant issues

| id | doc | line_no | description_text | issue_type | classification | classification_ref | notes |
|---|---|---|---|---|---|---|---|
| ISS-0083 | working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md | 44 | **Overlap with STYLE_1**: Significant content duplication with `docs/to_integrate/STYLE_1.md` on typing, annotations, and Python 3.14 features—consolidate in Phase 2. | Duplicates | CONFLICT | Code Standards & Architecture | STYLE_2 significantly overlaps STYLE_1 on typing and Python 3.14 annotation guidance; migration_plan.md explicitly merges STYLE_1 and STYLE_2 into docs/code-style-guide.md in the Code Standards & Architecture theme, so the duplication must be resolved during that consolidation. |
| ISS-0084 | working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md | 45 | **Draft status**: Document appears to be a conversion/adaptation rather than finalized guidance ("if you like, I can generate[ELIDED]"). | Staleness | CONFLICT | Code Standards & Architecture | STYLE_2 is a draft/partially converted style doc; migration_plan.md treats STYLE_* as sources to merge and clean into docs/code-style-guide.md, so this draft status needs manual resolution and editing as part of the Code Standards & Architecture phase. |
| ISS-0085 | working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md | 46 | **Missing examples**: No concrete examples of `annotationlib.get_annotations()` usage or runtime introspection patterns. | Gaps | RESEARCH | Python 3.14+ Features | The missing concrete examples of annotationlib.get_annotations() and runtime introspection patterns in STYLE_2 represent a knowledge gap; filling it requires researching Python 3.14’s annotationlib and best-practice patterns for runtime annotation inspection. |
| ISS-0086 | working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md | 47 | **TypeScript heritage**: Some phrasing suggests direct translation from TypeScript docs rather than Python-native guidance. | Staleness | CONFLICT | Code Standards & Architecture | STYLE_2’s TypeScript-derived phrasing indicates non-idiomatic and partially stale guidance; as STYLE_* docs are merged into docs/code-style-guide.md under Code Standards & Architecture, this heritage needs manual rewriting to match Python-native style. |
| ISS-0087 | working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md | 48 | **Incomplete coverage**: Focuses narrowly on annotation decisions without broader style context covered in STYLE_1. | Gaps | CONFLICT | Code Standards & Architecture | STYLE_2 focuses narrowly on annotations and omits broader style context already covered by STYLE_1; during the STYLE_* → docs/code-style-guide.md consolidation, this imbalance must be resolved so that STYLE_2’s content is integrated without leaving fragmented or partial guidance. |
| ISS-0088 | working/phase1/summaries/docs/to_integrate/STYLE_2.summary.md | 49 | **No conflict with existing docs**: Unlike STYLE_1, doesn't introduce tooling or conventions that contradict `README.md`/`AGENTS.md`. | Other | RESOLVED | Migration §2 – STYLE_* → docs/code-style-guide.md | The fact that STYLE_2 does not conflict with README/AGENTS tooling guidance is already accounted for in migration_plan.md, which merges STYLE_2 into docs/code-style-guide.md while deferring to ADR-0005 and existing Ruff-based tooling decisions; no additional work beyond the planned consolidation is required. |

## Instructions

For each issue listed above:

- Open `docs/to_integrate/STYLE_2.md`.
- Confirm whether the described problem is still present.
- If it is still present, edit `docs/to_integrate/STYLE_2.md` to resolve it, aligning with current ADRs, `pyproject.toml`, and the consolidated `docs/code-style-guide.md`.
- If it has already been resolved, ensure the intent of the fix remains clear and that no contradictory guidance remains.

Focus only on the concerns described in these issues; do not introduce unrelated changes.
