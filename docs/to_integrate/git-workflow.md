Git Workflow

This document outlines the branching, committing, and merging strategy for this project. We use a "rebase-first" workflow with manual squashing to maintain a clean, linear, and meaningful main branch history.

1. Branch Naming Convention

All new work must be done on a feature branch. Branch names should be prefixed to indicate the type of work:

feat/: For new features (e.g., feat/metadata-caching)

fix/: For bug fixes (e.g., fix/health-check-500)

docs/: For documentation changes (e.g., docs/update-git-workflow)

refactor/: For code refactoring (e.g., refactor/settings-module)

test/: For adding or improving tests (e.g., test/add-e2e-tests)

chore/: For maintenance, CI, or build script changes (e.g., chore/update-ruff)

2. Commit Message Convention

We follow the Conventional Commits specification. This is not just a style guide; it's what allows for automated versioning and changelog generation.

Format

<type>(<scope>): <subject>

<body>

<footer>


Type: feat, fix, docs, refactor, test, chore, perf, ci, style, build.

Scope (Optional): The module or part of the app affected (e.g., app, api, scripts, e2e).

Subject: A concise (50-70 char) description in the imperative tense (e.g., "add caching layer," not "added caching layer").

Body (Optional): Explains the "what" and "why" of the change.

Footer (Optional): Used for BREAKING CHANGE: notes or for referencing issue numbers.

This format is most important for your final squashed commit message that gets merged into main.

3. Local Development Workflow

This is your day-to-day "code and commit" loop.

Create Branch:

git checkout main
git pull origin main
git checkout -b feat/my-new-feature


Code and Commit Locally:

Write your code and tests.

Commit often. Make small, "work-in-progress" (WIP) commits. These are for you and will be cleaned up later.

git add .
git commit -m "WIP: add service"


Run Local Checks (Manual):
Before you push or open a PR, run the core checks locally. This is much faster than waiting for CI.

# 1. Run linting and formatting
uv run lint

# 2. Run all tests EXCEPT the slow E2E tests
uv run pytest -m "not e2e"


Keep Your Branch Updated:
Periodically rebase your branch on main to pull in the latest changes. This makes the final rebase much easier.

git fetch origin
git rebase origin/main


(Resolve any conflicts, then continue with git rebase --continue)

4. Pull Request & Merging Strategy

This is the core of our workflow. We do not use the "Squash and Merge" button on GitHub. We prepare a clean, single-commit branch before merging.

Step 1: Open a "Draft" Pull Request

As soon as you push your first commit, open a Draft Pull Request.

This allows the CI/PR checks (Coderabbit, Sonar, tests) to run on your WIP commits and gives teammates visibility.

Step 2: Get Feedback

Your PR will be checked by:

Automated Review: Coderabbit, Macroscope

Code Quality: Sonar

Automated Tests: Unit Tests, Component Tests, Integration Tests, E2E Tests

Address feedback from both bots and humans with new "fixup" commits.

Step 3: Prepare Your Branch for Merge (Squash & Rebase)

Once your PR is fully reviewed and all checks are green, you must clean up your branch.

Fetch Latest main:

git fetch origin main


Start an Interactive Rebase:
This is the "squash separately" step. We rebase against main and clean our commits at the same time.

git rebase -i origin/main


Squash Your Commits:
Your text editor will open with a list of all the commits on your branch.

pick the first (oldest) commit.

Change all other commits from pick to s (squash) or f (fixup). fixup is often cleaner as it discards the commit message.

Before:

pick 1a2b3c4 feat: add service
pick 4d5e6f7 WIP: fix tests
pick 7g8h9i0 fix: address pr feedback


After:

pick 1a2b3c4 feat: add service
f 4d5e6f7 WIP: fix tests
f 7g8h9i0 fix: address pr feedback


Write the Final Commit Message:
After saving and closing the rebase file, your editor will open again, prompting you to write the single commit message for the new, squashed commit.

This is the most important commit message.

Write a perfect Conventional Commit message (see Section 2).

Force Push:
Your branch history is now different from the remote, so you must force push. Use --force-with-lease as a safety measure.

git push --force-with-lease


Step 4: Final Merge

Your PR will now show one clean, descriptive commit.

All PR checks (Sonar, Coderabbit, all tests) will run one last time.

Once all checks pass, your PR can be merged into main (this will be a fast-forward merge).

5. Automated Checks

Local Pre-Commit Hook

As defined in .pre-commit-config.yaml, our pre-commit hook only runs uv run lint (Ruff format + check).

It does not run pytest. You are responsible for running tests manually before committing or pushing.

Pull Request Checks (CI)

A PR will not be merged unless all of the following checks pass:

Automated Review: Coderabbit, Macroscope

Code Quality: Sonar

Test Suite:

Unit Tests

Component Tests

Integration Tests

E2E Tests (uv run pytest -m e2e)