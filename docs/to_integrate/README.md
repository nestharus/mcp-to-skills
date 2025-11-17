MCP Metadata Broker Documentation

Welcome to the project documentation for the MCP Metadata Broker. This index will help you find the right guide for your needs.

1. Getting Started

Development Setup - First-time setup, installing uv, creating the virtual environment, and verifying your setup.

Development Workflow - Day-to-day "code, test, lint, commit" workflow.

2. Core Guides

Architecture & Design

Architecture Overview - High-level system architecture and patterns.

Application Lifecycle - How the app starts, loads config, and shuts down.

API Patterns Guide - API design patterns and conventions.

Development & Workflow

Git Workflow - Branching strategy, commit conventions, and our rebase-first merging process.

Code Style Guide - Coding standards and best practices.

Quality & Testing

Linting & Code Quality Guide - How we use Ruff, Checkov, and Sonar.

Testing Architecture - Overview of our multi-tiered testing strategy.

E2E Testing Guide - How to write and run high-fidelity E2E tests with a live server.

3. Quick Reference

Key Tools

Command Reference - Complete list of all uv run commands and Docker usage.

Common Issues

Issue

Guide

"command not found: pytest"

Development Setup

"command not found: lint"

Development Setup

Seeing .venv and .venv2

Command Reference

E2E tests won't run

E2E Testing Guide

Common Commands

# Install all dependencies (main + dev)
uv sync
uv run mcp-setup

# Run the dev server with hot-reload
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run all tests (except E2E)
uv run pytest -m "not e2e"

# Run only E2E tests (slow)
uv run pytest -m e2e

# Run linting & formatting
uv run lint

# Regenerate the OpenAPI schema
uv run gen_openapi --config tests/fixtures/sample_mcp.toml

# Build the Docker image
docker build -t mcp-metadata-broker:dev .



4. Contributing

Before contributing, please read:

Development Setup

Git Workflow

Development Workflow

Linting & Code Quality Guide

Authoring Docs & Plans

Stable guidance belongs in docs/ (this directory). Add new guides here and link them from this index.

Proposals and explorations belong in the root plans/ directory.

5. Need Help?

Check the relevant guide above.

Search existing issues in the repository.

Ask in the team chat.

Create a new issue with details about your problem.