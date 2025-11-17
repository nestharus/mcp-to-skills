Linting and Code Quality Guide

1. Overview

This project uses a layered approach to code quality, relying on a set of specialized tools for different tasks. Unlike JavaScript projects that use many ESLint plugins, our Python setup is centered around a few powerful, distinct tools.

Our philosophy is:

Fast local feedback: Use Ruff for instant linting and formatting.

Security scanning: Use Checkov to find misconfigurations in files like Dockerfile.

Deep CI analysis: Use Sonar (in the pull request) for in-depth bug detection, code smell analysis, and security vulnerability scanning.

2. Our Quality Toolset

Tool 1: Ruff (The Linter & Formatter)

Ruff is our primary, all-in-one tool for local development. It is configured in pyproject.toml and replaces older tools like Flake8, isort, and Black.

What it does: Lints for correctness, enforces style, formats code, and sorts imports.

When it runs:

Locally: Every time you run uv run lint.

On Commit: The pre-commit hook runs uv run lint automatically.

In CI: Runs as a check in every pull request.

Tool 2: Checkov (The IaC Security Scanner)

Checkov is a static analysis tool that scans infrastructure-as-code (IaC) files for security misconfigurations. It is included in our dev dependencies.

What it does: Scans files like Dockerfile for common security issues (e.g., running as root, exposed ports, missing hardening).

When it runs:

Locally (Manual): You can run it manually to check your files.

In CI: Runs as a security check in every pull request.

Tool 3: Sonar (The CI Quality Gate)

Sonar (e.g., SonarCloud/SonarQube) is our most comprehensive quality gate. It runs only in the pull request.

What it does: Performs deep static analysis to find bugs, code smells, complexity issues, and security vulnerabilities (e.g., injection risks) that Ruff may not be designed to catch.

When it runs:

In CI: Runs automatically when you open or update a pull request.

3. Running Checks Locally

Before pushing, you can run the same checks that CI will.

Linting & Formatting with Ruff

The lint script in pyproject.toml runs both formatting and linting.

# Run the all-in-one lint command (format then check)
uv run lint

# To ONLY format your code (without checking)
uv run ruff format .


Security Scanning with Checkov

You can run checkov from your virtual environment to scan files.

# Scan the Dockerfile specifically
uv run checkov -f Dockerfile

# Scan the entire project directory for any config files
uv run checkov -d .


4. Automated Checks (CI & Hooks)

Pre-Commit Hook

As defined in .pre-commit-config.yaml, our local pre-commit hook only runs uv run lint (Ruff). This is intentional to keep it fast. It ensures you never commit unformatted code.

Pull Request (CI)

When you open a PR, the full, comprehensive suite of checks is triggered, as defined in git-workflow.md:

Ruff: Confirms linting and formatting.

Checkov: Runs the security scan.

Sonar: Runs the deep code quality analysis.

Pytest: Runs all test tiers (Unit, Component, Integration, and E2E).

A PR can only be merged when all these checks pass.