# ADR 0008: Canonical Target Docs via Phase 2 IA

## Context

The repository currently contains many overlapping and partially conflicting documentation files under `docs/` and `docs/to_integrate/`. Phase 1 analysis produced an inventory and highlighted duplication, conflicts, and gaps. Phase 2 introduced a consolidated information architecture (IA) to define a small set of canonical target docs.

## Decision

- Adopt the Phase 2 documentation IA described in `working/phase2/docs_ia.md` as the source of truth for documentation structure.
- Consolidate existing docs into the defined target documents (e.g., `docs/code-style-guide.md`, `docs/testing-guide.md`, `docs/architecture.md`, `docs/api.md`, `docs/workflow-and-ci.md`, `docs/releases-and-versioning.md`, `docs/development-setup.md`).
- Treat `docs/to_integrate/` as staging material to be migrated and eventually removed.

## Consequences

- Reduces duplication and contradictions across documentation.
- Provides clear navigation for contributors and operators.
- Requires a focused migration effort to move content from legacy files into the new structure.

## References

- `working/phase2/docs_ia.md` (information architecture)
- Target docs under `docs/`
