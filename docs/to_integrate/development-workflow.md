Development Workflow

This document outlines the standard process for making, testing, and committing changes.

Your core workflow is: Code → Test → Lint → Commit.

The project is configured to help you follow this pattern. As noted in AGENTS.md, you should always run tests and linting after making changes to catch regressions before they are committed.

1. Daily Development Commands

These are the three commands you will use most.

1. Run the Development Server

This starts the FastAPI server with hot-reloading.

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Keep this running in a terminal while you code.

2. Run Tests

Run the entire pytest test suite.

uv run pytest


Run this after you make a change to ensure you haven't broken anything.

3. Run Linting & Formatting

This command (defined in pyproject.toml) runs ruff format first, then ruff check.

uv run lint


Run this before you commit to clean up your code and check for errors.

2. Automated Code Quality (Pre-Commit)

This project uses pre-commit to automate code quality checks. The uv run mcp-setup command you ran during setup already installed this for you.

Your .pre-commit-config.yaml is simple and powerful:

repos:
- repo: local
  hooks:
    - id: project-lint
      name: Run project lint pipeline
      entry: uv run lint
      language: system
      pass_filenames: false
      always_run: true


What This Means

When you run git commit:

The pre-commit hook will trigger.

It will execute the uv run lint command.

ruff format will format your files, and ruff check will look for errors.

If the linter finds any issues (or if the formatter changes a file), your commit will be stopped.

If your commit is stopped:

Check the output from uv run lint.

Your files may have been auto-formatted. Just run git add . to stage the formatting changes.

If there were lint errors, fix them.

git add your fixes and try to commit again.

This hook ensures that no unformatted code or code with simple lint errors ever makes it into the repository.

3. The Standard Git Workflow

Step 1. Create a Branch

Start from the main branch and create a descriptive feature branch.

# Get the latest changes
git checkout main
git pull

# Create your new branch
git checkout -b feat/my-new-feature


Branch Naming:

feat/: For new features (e.g., feat/metadata-caching)

fix/: For bug fixes (e.g., fix/health-check-500)

docs/: For documentation changes (e.g., docs/update-workflow)

refactor/: For code refactoring (e.g., refactor/settings-module)

test/: For adding or improving tests (e.g., test/add-unit-tests-core)

Step 2. Make Your Changes

Write your code, create tests, and update documentation as needed.

Where to Put Code:

app/: All primary FastAPI application code, Pydantic models, and domain logic.

scripts/: Helper scripts for setup, and operations (like start-server.py).

docs/: Project documentation (like this file).

tests/: All pytest tests. The structure here should mirror the app/ structure.

Step 3. Run Checks Manually

Before you commit, manually run the checks. This is the "agent" workflow from AGENTS.md.

# 1. Run all tests
uv run pytest

# 2. Run the linter
uv run lint


This is the fastest way to find and fix errors, rather than waiting for the pre-commit hook or CI.

Step 4. Commit Your Changes

git add .
git commit -m "feat: add caching layer to metadata endpoint"


The pre-commit hook (running uv run lint) will automatically run. If it passes, your commit is created.

Step 5. Push and Create a Pull Request

git push origin feat/my-new-feature


Then, open a Pull Request in your Git provider.

4. Important Workflow Rules

These rules (from AGENTS.md) are critical:

Changing the API?
If you add, remove, or change any API endpoints or Pydantic models, you must regenerate the OpenAPI schema:

uv run gen_openapi --config tests/fixtures/sample_mcp.toml


Commit the updated openapi/openapi.json file with your changes.

Changing the Workflow?
If you change how a command works or add a new tool, you must update the documentation (like this file, README.md, etc.) in the same pull request.

5. Debugging

Pydantic / Validation Errors:
If you get a 422 Unprocessable Entity error, check the FastAPI error logs. Pydantic gives detailed messages about what field failed validation and why.

Hot Reload Not Working?
If uvicorn isn't reloading, check for syntax errors in your terminal. A single syntax error will stop the server from reloading until it's fixed.

Test Failures:

Run uv run pytest -v for more verbose output.

To run a single test file: uv run pytest tests/unit/test_my_file.py

To run a single test function: uv run pytest tests/unit/test_my_file.py -k "test_my_function_name"

6. Common Workflows

Adding a New Feature

Create feat/ branch.

Write failing tests in the tests/ directory first (TDD).

Implement the feature in app/.

Run uv run pytest until all tests pass.

Update documentation (docs/) if needed.

Regenerate OpenAPI schema (uv run gen_openapi ...) if the API changed.

Run uv run lint.

Commit and create PR.

Fixing a Bug

Create fix/ branch.

Write a new test that reproduces the bug (and fails).

Implement the fix in app/ until the test passes.

Run the full suite uv run pytest to check for regressions.

Run uv run lint.

Commit and create PR.