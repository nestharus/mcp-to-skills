## Purpose
- Document the project's branching, committing, and merging strategy using a rebase-first workflow with manual squashing to maintain a clean, linear `main` branch history.

## Main Topics
- Branch naming conventions: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/` prefixes tied to change type.
- Conventional Commits specification: commit message structure with `type(scope): subject`, optional body, and footer.
- Local development workflow: create branch, implement changes, run checks, commit, push, and keep branch rebased on `main`.
- Pull request and merging strategy: draft PRs, review feedback, interactive rebase and manual squash, final merge to `main`.
- Automated checks: pre-commit hooks, CI checks (lint, tests, automated review tools, code quality analysis) that must pass before merge.

## Opinions / Guidelines
- Use Conventional Commits for all final squashed commits to keep history readable and machine-parseable.
- Prefer a rebase-first workflow (avoid merge commits into `main`) and perform manual squashing via interactive rebase.
- Use `git push --force-with-lease` when updating PR branches after rebasing to avoid overwriting collaborators' work.
- Rely on pre-commit hooks for linting only; developers are responsible for running tests locally before pushing.
- Treat CI checks (linting, full test suite including E2E, automated reviews) as mandatory gates for merging to `main`.

## Assumptions
- Contributors are comfortable with interactive rebase, resolving conflicts, and force-pushing safely.
- CI is configured with automated review and code quality tools (e.g., Coderabbit, Macroscope, Sonar) as part of PR checks.
- E2E tests are present and can be run with a dedicated pytest marker (e.g., `pytest -m e2e`).
- The `main` branch is protected and requires at least one approved review before merging.
- The hosting platform (e.g., GitHub) is used with a standard PR-based workflow.

## Staleness Indicators
- References to Coderabbit and Macroscope as CI review tools may not match the actual configured tools in this repository.
- Mentions of running `pytest -m e2e` assume an `e2e` marker definition in `pyproject.toml` that may not exist yet.
- Sonar is described as part of PR checks, but Sonar configuration files may be missing from the repo.
- The description of pre-commit behavior assumes `.pre-commit-config.yaml` only runs `uv run lint`; any expansion of hooks would require doc updates.
- The workflow assumes all CI checks (lint, unit, integration, E2E) are wired into `.github` workflows, which may still be evolving.

## Tags
- `workflow`, `git`, `branching`, `commits`, `conventional-commits`, `rebase`, `squash`, `pull-requests`, `ci`, `changesets`, `versioning`, `code-review`, `pre-commit`, `sonar`, `coderabbit`

## Preliminary Target Docs
- Likely target: standalone `docs/git-workflow.md` focused on git mechanics and history hygiene.
- Cross-reference `docs/development-workflow.md` for daily commands and local testing expectations.
- Cross-reference `docs/changesets-guide.md` for how commit conventions align with versioning and release notes.

## Red Flags
- Overlap with `docs/to_integrate/development-workflow.md` where both describe running `uv run lint` and pytest before committing; they differ on whether to exclude E2E tests by default.
- Overlap with `README.md` "Code Quality" section, which also explains pre-commit hooks and `uv run lint`, risking duplicated guidance.
- References to an `e2e` pytest marker (`pytest -m e2e`) that may not be configured in `pyproject.toml`.
- Mentions of Coderabbit and Macroscope as mandatory CI checks without visible configuration in `.github/` workflows.
- Sonar is treated as a required PR check but there is no obvious `sonar-project.properties` or documented Sonar setup.
- Conventional Commits are required for final squashed commits, yet no automated enforcement (e.g., commitlint) is documented.
- Guidance recommends `--force-with-lease` but does not elaborate on risks of force-pushing or collaboration considerations.
- Assumes branch protection rules on `main` (required reviews, status checks) that are not documented in-repo.
- Commit message structure is described here and again in `docs/to_integrate/changesets-guide.md`, creating potential consistency drift.
- Pre-commit is described as lint-only here while other docs hint at broader automation; any change to hook scope must be synchronized across docs.

## References
- `docs/to_integrate/git-workflow.md`
- `docs/to_integrate/development-workflow.md`
- `docs/to_integrate/changesets-guide.md`
- `README.md` (Code Quality section)
- `.pre-commit-config.yaml`
- `pyproject.toml` (pytest markers and tool configuration)
- `.github/` CI workflows (if present)
