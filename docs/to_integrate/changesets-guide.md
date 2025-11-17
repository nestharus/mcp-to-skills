# Version Management with Changesets (Python + uv)

## Overview

The `mcp-to-skills` FastAPI project uses a lightweight, Python-native “changesets-style” workflow:

* Release intent is stored as markdown files in `.changeset/`.
* Versions are managed via `pyproject.toml` and `uv version`.
* No manual `CHANGELOG.md`; communicate changes via PR descriptions, tags, and commit messages.

Important:

* Do not write human-authored changelogs in `.changeset/`. That folder is for release intent entries only (what to release and how to bump).
* The authoritative version lives in `[project].version` in `pyproject.toml`. ([Astral Docs][1])

Project layout (simplified):

* `app/` – main FastAPI application (`main.py`).
* `scripts/` – e.g. `start-server.py` (entry point used by Dockerfile).
* `tools/` – utilities (e.g. `gen_openapi.py`, changesets tooling).
* `openapi/` – `openapi.json`.
* `tests/`, `dist/`, `out/`, `.github/`, `Dockerfile`, etc.

The repo is a single Python project (not a monorepo). All versioning applies to the single package, typically named `mcp-to-skills` in `pyproject.toml`.

---

## Why a Changesets-style Workflow?

The concept is borrowed from the JS Changesets project: a “changeset” is an intent to release with a semver bump and a short description of the change. ([GitHub][2])

Using the same idea for Python gives:

* **Intent-based versioning**: Each PR that should change the released artifact adds one small file in `.changeset/`.
* **Clear semantics**: Every changeset specifies `major` / `minor` / `patch`.
* **uv integration**: A Python CLI (run via `uv run`) reads these files and:

    * Calculates the next version using `uv version --bump …`. ([Astral Docs][3])
    * Bumps `[project].version` in `pyproject.toml`.
* **CI-friendly**: Easy to enforce “no release without a changeset” and to wire into GitHub Actions.

---

## Commands

All commands are run via `uv` in the project root: ([Astral Docs][1])

Existing:

* `uv run mcp-setup`
* `uv run lint` (ruff + checkov)
* `uv run gen_openapi` (drives `tools/gen_openapi.py` → `openapi/openapi.json`)

Changesets-related (Python tooling you wire up under `tools/` and `[tool.uv.scripts]`):

* `uv run changeset` – create a new changeset file in `.changeset/`.
* `uv run version-packages` – consume changesets and bump `pyproject.toml` version.
* `uv run release` (optional) – build and publish distributions using `uv build` / `uv publish`. ([Astral Docs][1])

---

## Creating a Changeset (Release Intent)

When you make changes that should be released, create a changeset:

```bash
uv run changeset
```

Typical interactive flow (single package):

1. **Select bump type**: `major`, `minor`, or `patch`.
2. **Write summary**: Short description of what changed.

### Bump Types (Semantic Versioning)

* **Major** (`1.0.0 → 2.0.0`): Breaking changes; existing clients may need code changes.
* **Minor** (`1.0.0 → 1.1.0`): New features; backward compatible.
* **Patch** (`1.0.0 → 1.0.1`): Bug fixes or small internal improvements; backward compatible. ([Astral Docs][3])

### Example

```bash
$ uv run changeset
? Bump type (major / minor / patch): minor
? Summary: Add user profile endpoints and models
```

This creates a file like `.changeset/bright-otters-add-profile.md`:

```markdown
---
'mcp-to-skills': minor
---

Add user profile endpoints and models

Adds /profile endpoints, new Pydantic models, and tests.
```

Notes:

* The key in the frontmatter (`'mcp-to-skills'`) must match `[project].name` in `pyproject.toml`. ([Astral Docs][1])
* You can add extra detail in the body as needed; keep the top summary line concise.

---

## Versioning the Package

When you’re ready to cut a release from `main`, run:

```bash
uv run version-packages
```

The Python tooling behind `version-packages` does:

1. Scan `.changeset/*.md`.
2. Determine the highest bump type requested:

    * Any `major` → overall bump is `major`.
    * Else if any `minor` → overall bump is `minor`.
    * Else if any `patch` → overall bump is `patch`.
3. Compute the new version:

    * Uses `uv version --bump <major|minor|patch>` to update `[project].version` in `pyproject.toml`. ([Astral Docs][3])
4. Remove (or archive) the consumed `.changeset/*.md` files.
5. Print a summary of the release (old version, new version, and included summaries).

Then commit:

```bash
git add pyproject.toml uv.lock .changeset
git commit -m "chore: version mcp-to-skills"
```

`uv.lock` should be treated as managed by uv; don’t edit it manually. ([Astral Docs][1])

---

## Publishing (Optional)

If you publish `mcp-to-skills` as a package (e.g. internal index):

1. Make sure `version-packages` has been run and committed.

2. Build distributions:

   ```bash
   uv build
   ```

   This creates wheels and source dists under `dist/`. ([Astral Docs][1])

3. Publish:

   ```bash
   uv publish
   ```

   This uploads artifacts from `dist/` to the configured index (PyPI or private). ([Astral Docs][3])

Configure credentials via `uv auth` or environment variables as described in the `uv publish` docs. ([Astral Docs][3])

If you only ship via Docker, you may skip `uv publish` and just use the version for image tags and labels.

---

## Workflow

### Development Flow

1. Make code changes under `app/`, `tools/`, etc.
2. If the change should result in a release:

    * Run `uv run changeset`.
    * Commit both code and the new `.changeset/*.md` file.
3. Open a PR:

    * Include a “Release intent” section summarizing the change and bump type.

No version bump happens in feature branches.

### Release Flow

1. Merge PRs to `main`. Each release-worthy PR should already include a changeset file.

2. On `main`, run:

   ```bash
   uv run version-packages
   ```

3. Commit the resulting `pyproject.toml`, `uv.lock`, and `.changeset/` changes.

4. Tag the release, e.g.:

   ```bash
   git tag -a v1.3.0 -m "Release v1.3.0"
   git push --follow-tags
   ```

5. Optionally:

    * Run `uv build` and `uv publish` locally, or
    * Have a GitHub Actions workflow trigger on tags and run `uv build` / `uv publish` in CI. ([Astral Docs][1])

---

## Changeset File Format

Changeset files are markdown with YAML frontmatter:

```markdown
---
'mcp-to-skills': patch
---

Fix error handling when MCP backend is unreachable

Handles connection errors with retries and clearer error responses.
```

Rules:

* Only one package key (`'mcp-to-skills'`) for this repo.
* Value is one of `major`, `minor`, `patch`.
* The body is free-form markdown. Use the first line as a short title-style summary.

---

## Best Practices

### 1. One Changeset per Feature

Create a changeset for each logical change that should affect the released artifact, even if that change spans multiple files:

```bash
git commit -m "feat: add MCP → skills mapping"
uv run changeset
```

If you later fix a bug in that feature, add a separate patch changeset.

### 2. Write Clear Summaries

Good summaries:

* State what changed at a user-facing level.
* Avoid vague “update code” phrasing.

Examples:

```markdown
# ✅ Good

Add authentication middleware for MCP API

Implements API key-based auth for all /mcp routes.

# ❌ Bad

Update auth
```

### 3. Include Breaking Changes Explicitly

If you need a **major** bump, say why and how to migrate:

```markdown
---
'mcp-to-skills': major
---

Drop support for legacy MCP v1 schema

BREAKING CHANGE: Requests must now use MCP v2 schema.

Migration:
- Update outbound messages to include `skills_version` field.
- Remove `legacy_mode` flag from client configuration.
```

### 4. Keep the Repository Single-package Aware

Because this is not a monorepo:

* Frontmatter always uses `'mcp-to-skills'`.
* If you ever split code into separate installable packages, extend the format to include multiple keys (one per package), following the same pattern.

### 5. Selecting Dependency Versions (Version Drift)

When adding or upgrading dependencies:

* Use `uv add <name>` to add dependencies so `pyproject.toml` and `uv.lock` stay in sync. ([Astral Docs][1])
* Use `uv lock --upgrade-package <name>` to deliberately upgrade a dependency within its allowed constraint range. ([Astral Docs][1])
* Read upstream release notes and migration guides for breaking changes.
* If a dependency upgrade is risky, mention:

    * Why you’re upgrading.
    * What could break.
    * Any follow-up migration steps.
      in the same PR description as the changeset.

---

## CI Integration

Typical GitHub Actions setup for `mcp-to-skills`:

* **PR validation**:

    * `uv run lint` (ruff + checkov).
    * `uv run gen_openapi` to keep `openapi/openapi.json` in sync.
    * Tests under `tests/`.
    * Optional: fail the build if a PR modifies `app/` or `tools/` but does not include a new `.changeset/*.md` file.

* **Release workflow**:

    * Triggered manually or on tags.
    * Runs `uv build` and optionally `uv publish` to publish packages or to attach artifacts to a GitHub Release. ([Astral Docs][1])

No Node-based Changesets GitHub Action is used; all tooling is Python + uv.

---

## Skipping Changesets

You do not need a changeset for changes that don’t affect the released behavior:

* Documentation-only updates.
* Test-only changes.
* Refactors with no observable behavior changes.
* CI configuration / workflow changes.

For these, commit normally without `uv run changeset`.

---

## Troubleshooting

### “No changesets present”

Symptom: `uv run version-packages` reports that there are no changesets to process.

Fix:

* At least one `.changeset/*.md` file must exist and not be marked as consumed.
* Add a changeset via `uv run changeset`, or defer the release until there is something to ship.

### “Changeset validation failed”

Symptom: The changesets Python tooling reports invalid frontmatter.

Fix:

* Ensure the file starts and ends its frontmatter with `---` lines.
* Ensure the mapping is valid YAML, e.g.:

  ```yaml
  'mcp-to-skills': minor
  ```

### “Unknown package in changeset”

Symptom: Tooling complains that the package name does not match.

Fix:

* The key in frontmatter must match `[project].name` in `pyproject.toml` (currently `mcp-to-skills`). ([Astral Docs][1])

---

## Resources

* `uv` project and CLI docs ([Astral Docs][4])
* `uv` build backend and hatchling/backends discussion ([Astral Docs][5])
* Changesets concept (intent-based release files) ([GitHub][2])
* Semantic Versioning – [https://semver.org/](https://semver.org/)
* Conventional Commits – [https://www.conventionalcommits.org/](https://www.conventionalcommits.org/)

This fully replaces the earlier `ui-designer` / Bun / monorepo wording and is aligned with the `mcp-to-skills` Python FastAPI repo, `uv`, hatchling, and the `.changeset/` folder.

[1]: https://docs.astral.sh/uv/guides/projects/ "Working on projects | uv"
[2]: https://github.com/changesets/changesets?utm_source=chatgpt.com "changesets/changesets: 🦋 A way to manage your ..."
[3]: https://docs.astral.sh/uv/reference/cli/ "Commands | uv"
[4]: https://docs.astral.sh/uv/?utm_source=chatgpt.com "uv"
[5]: https://docs.astral.sh/uv/concepts/build-backend/ "Build backend | uv"


### Selecting Dependency Versions (Version Drift)

When adding or upgrading dependencies, and the required version differs from versions documented in this repo or your model knowledge:

- Use context7 to retrieve the authoritative current version, release notes, and migration guides.
- Check for breaking changes and plan migrations accordingly.
- Include a short summary of the upgrade rationale and risks in the changeset summary.
- Coordinate multi-package upgrades in one changeset when they must land together.