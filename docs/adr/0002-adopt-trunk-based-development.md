# ADR 0002: Adopt Trunk-Based Development

## Context

The project aims for frequent integration, fast feedback, and minimal merge friction. Traditional long-lived branches and complex release branches can slow delivery, complicate reviews, and increase the risk of integration conflicts, especially for a relatively small team and service.

## Decision

Adopt trunk-based development (TBD) as the branching model:

- Developers work on short-lived feature branches based off `main`, typically lasting no more than a couple of days.
- Changes are merged back into `main` frequently after review and passing checks.
- Long-lived release branches are avoided unless a future release process explicitly requires them.

## Consequences

- Reduces merge conflicts and keeps `main` close to the current state of development.
- Relies on strong automated testing and pre-commit checks to maintain trunk stability.
- Encourages smaller, more focused pull requests and quicker reviews.
- Future release branching strategies (e.g., hotfix branches) can be layered on top of this model if needed.

## References

- `docs/workflow-and-ci.md` (branching and CI workflow)
- `docs/releases-and-versioning.md` (release process)
