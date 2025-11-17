Development Setup

This guide walks you through setting up the mcp-metadata-broker project for local development, from a fresh clone to a running server.

Prerequisites

Before you begin, ensure you have the following tools installed on your system:

Python 3.14 (python --version should show 3.14.x)

uv (The project's Python package and environment manager)

Git

Docker (Optional, for building and running the container)

1. Initial Setup

Follow these steps in your terminal to set up the project.

Step 1: Clone the Repository

git clone <repository-url>
cd mcp-metadata-broker


Step 2: Install uv (if you don't have it)

We recommend uv for managing all dependencies and virtual environments.

# Recommended (Linux/macOS)
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Or, if you have pip
pip install uv


Step 3: Create and Activate the Virtual Environment

This creates a local .venv directory and activates it.

# 1. Create the virtual environment
uv venv

# 2. Activate it
# Linux/macOS
source .venv/bin/activate

# Windows (Powershell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat


You should see (.venv) at the start of your shell prompt.

Step 4: Install All Dependencies

This is a two-part process:

uv sync installs the main application dependencies (FastAPI, etc.) from uv.lock.

uv run mcp-setup is a custom script that installs all development tools (pytest, ruff, pre-commit) and sets up the pre-commit hooks.

# 1. Install main dependencies
uv sync

# 2. Install dev dependencies and git hooks
uv run mcp-setup


Your environment is now fully configured.

2. Verify the Setup

Run these commands to ensure everything is working correctly.

Step 1: Run the Linter

This command formats your code and checks for any style errors.

uv run lint


This should complete without errors.

Step 2: Run the Tests

This command discovers and runs the entire test suite.

uv run pytest


All tests should pass.

Step 3: Run the Development Server

This command starts the FastAPI server with automatic hot-reloading.

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Step 4: Check the Health Endpoint

With the server running, open this URL in your browser or with curl:

http://localhost:8000/api/metadata/v1/health

If the setup is successful, you will see a JSON response.

3. Editor Configuration (VS Code)

We recommend using VS Code with the official Python extension by Microsoft.

The most important step is to select the correct Python interpreter:

Open the command palette (Ctrl+Shift+P or Cmd+Shift+P).

Type Python: Select Interpreter.

Choose the interpreter from your project's virtual environment. It will be labeled as .venv and point to ./.venv/bin/python.

This ensures that VS Code uses all the tools (ruff, pytest) you installed in your virtual environment for linting, formatting, and testing.

4. Project Structure

app/: Primary FastAPI application code and domain models.

scripts/: Helper scripts (e.g., bootstrap or operational tooling).

docs/: Reference documentation (like this file).

tests/: Automated tests (unit, integration, etc.).

openapi/: Generated OpenAPI schema file.

pyproject.toml: The central file defining the project, dependencies, and scripts.

5. Troubleshooting

"command not found: pytest" or "command not found: lint"

Cause: You ran uv sync but forgot the second step. The development tools are not installed.

Solution: Run uv run mcp-setup to install all dev dependencies.

"uv: command not found"

Cause: uv is not installed or not in your system's PATH.

Solution: Follow Step 2 to install it.

I see .venv and .venv2 directories.

Cause: This is normal if you switch between Windows and WSL. As noted in AGENTS.md, .venv is typically for Linux (WSL) and .venv2 for the Windows host.

Solution: This is not an error. Treat both as intentional. Always make sure you have activated the correct environment for the shell you are in.

Next Steps

Now that you're set up, here are some other useful documents:

Command Reference: A complete list of all uv run commands.

Application Lifecycle (docs/LIFECYCLE.md): How the app starts, loads config, and shuts down.

Testing Guide (docs/TEST.md): How to write and run tests.