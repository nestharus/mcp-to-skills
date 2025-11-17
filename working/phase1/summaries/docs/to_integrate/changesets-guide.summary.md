## Purpose
- Document the project's version management workflow using a Python-native, changesets-style approach with uv, where release intent is recorded as markdown files in `.changeset/`, versions are managed via `pyproject.toml` and `uv version`, and no manual `CHANGELOG.md` is maintained.

## Main Topics
- Changesets concept: intent-based versioning inspired by the JS Changesets project, capturing user-visible changes in small markdown files.
- Core commands: `uv run changeset`, `uv run version-packages`, and `uv run release` for creating changesets, bumping versions, and performing releases.
- Creating changesets: interactive flow, selecting bump type (major/minor/patch), and writing frontmatter and summaries.
- Versioning the package: scanning `.changeset/`, determining the aggregate bump, and updating `[project].version` via `uv version --bump`.
- Releasing: optional build and publish steps using `uv build` and `uv publish`, plus tagging and pushing release tags.
- Changeset file format: markdown with YAML frontmatter keyed by package name, plus human-readable description and migration notes.
- Best practices: one changeset per logical change, clear user-facing summaries, explicit breaking changes, and coordinated dependency bumps.
- CI integration: validating presence and correctness of changesets on PRs and automating release steps on main or tagged commits.
- Skipping changesets: when docs-only, test-only, or purely internal refactors do not require a new release.

## Opinions / Guidelines
- Require a changeset for any PR that modifies shipped behavior (new features, bug fixes, or breaking changes).
- Do not maintain a manual `CHANGELOG.md`; rely on changesets, tags, and PR descriptions for release notes.
- Treat `[project].version` in `pyproject.toml` as the single source of truth for the package version.
- Use strict semantic versioning (major for breaking changes, minor for new features, patch for backwards-compatible fixes).
- Ensure the changeset frontmatter package key matches `[project].name` in `pyproject.toml`.
- Write concise, user-focused summaries and call out breaking changes with clear migration guidance.
- Skip changesets only for docs-only, test-only, or non-functional refactors.
- Use `uv add` and `uv lock --upgrade-package` to manage dependencies, and document noteworthy dependency upgrades in changesets.
- Prefer CI enforcement so that PRs touching `app/` or `tools/` fail if they lack a corresponding changeset.

## Assumptions
- The project uses uv exclusively for environment management and scripts (no pip/poetry-based release tooling).
- This is effectively a single-package repo, with the package name defined in `pyproject.toml` (e.g., `mcp-to-skills`).
- A `.changeset/` directory exists (or will be created) and is tracked in git.
- `uv version` can be used to bump the version in `pyproject.toml` based on a computed semver increment.
- Supporting changesets tooling lives under `tools/` and is exposed via `[tool.uv.scripts]`.
- CI (e.g., GitHub Actions) is available and can be configured to validate changesets and run release workflows.
- Optional publishing targets (PyPI or private index) can be reached using `uv publish`.

## Staleness Indicators
- References to `uv run changeset`, `uv run version-packages`, and `uv run release` assume scripts defined in `[tool.uv.scripts]` that may not yet exist.
- Assumes a `.changeset/` directory is present, but it might not be created in this repo.
- CI enforcement of changesets on PRs is described but corresponding workflows may not be present under `.github/`.
- Usage of `uv version --bump` is mentioned without covering pre-release, build metadata, or version conflict handling.
- The doc assumes integration with context7 for dependency version guidance but may not explain how to access or use it.
- Publishing guidance assumes configured credentials and indexes for `uv publish` without pointing to concrete configuration examples.

## Tags
- `workflow`, `versioning`, `changesets`, `semver`, `releases`, `ci`, `uv`, `pyproject`, `changelog`, `git`, `tagging`, `publishing`, `dependencies`

## Preliminary Target Docs
- Likely target: standalone `docs/changesets-guide.md` focused on versioning and release management.
- Cross-reference `docs/git-workflow.md` for commit conventions and tagging practices.
- Cross-reference `docs/development-workflow.md` for the day-to-day development loop that feeds into changesets.
- Cross-reference `README.md` for setup and tooling expectations (uv, scripts, and environment).

## Red Flags
- Changesets tooling (`uv run changeset`, `uv run version-packages`, `uv run release`) may not yet be implemented in `pyproject.toml` `[tool.uv.scripts]` or `tools/`.
- The `.changeset/` directory may be missing, despite the guide assuming it exists and is used in all feature and bugfix PRs.
- Overlap with `docs/to_integrate/git-workflow.md` where commit conventions and release tagging are discussed separately, risking divergence.
- CI enforcement that fails PRs touching `app/` or `tools/` without changesets is recommended but not obviously configured in `.github/` workflows.
- Publishing workflow with `uv build` and `uv publish` is described without detailing how to configure credentials, indexes, or secrets.
- No guidance on handling pre-release versions (e.g., `1.0.0-alpha.1`), build metadata (e.g., `1.0.0+build.123`), or version conflicts.
- The dependency version drift section refers to context7-based lookup without explaining the actual usage pattern or any local tooling for it.
- The guide notes the repo is not a monorepo but still hints at multi-package coordination, which could confuse contributors.
- Mentions `uv sync` and other setup commands that may already be described in `README.md`, leading to duplicated setup guidance.
- Tagging instructions (e.g., `git tag -a v1.3.0`) may conflict with or duplicate tagging guidance in `docs/to_integrate/git-workflow.md`.

## References
- `docs/to_integrate/changesets-guide.md`
- `docs/to_integrate/git-workflow.md`
- `docs/to_integrate/development-workflow.md`
- `README.md` (setup and tooling sections)
- `pyproject.toml` (`[project].version`, `[tool.uv.scripts]`)
- `.changeset/` directory (if present)
- `uv.lock`
- `.github/` CI workflows (if present)
