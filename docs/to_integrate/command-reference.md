Command Reference

This project uses uv for all dependency management and task execution.

All commands should be run from within the activated virtual environment. The primary pattern is uv run <command>, which executes scripts defined in pyproject.toml or tools from the virtual environment (like pytest or uvicorn).

1. Project Setup

This is the complete workflow to set up the project from scratch.

Install uv (if not already present):

# Recommended (from Dockerfile)
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Or, if you have pip
pip install uv


Create the virtual environment:
(This creates a .venv directory in the project root).

uv venv


Activate the environment:

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate


Sync Main Dependencies:
(This installs the main application dependencies from uv.lock—FastAPI, Pydantic, etc.)

uv sync


Install Dev Tools & Hooks:
(This is the critical step that runs the mcp-setup script. This script installs dev tools like pytest and ruff and sets up pre-commit hooks.)

uv run mcp-setup


After these 5 steps, your environment is fully configured for development.

2. Daily Development Commands

These are the commands you will use most often.

Running the Application

Development Server (with Hot-Reload):
This is the recommended way to run the server for development.

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Production-Style Server:
This runs the start-server.py script, just like the Dockerfile.

python scripts/start-server.py --host "0.0.0.0" --port "8000"


Testing

Run the entire test suite using pytest. uv automatically finds pytest within the virtual environment.

uv run pytest


Linting & Formatting

This project uses Ruff for both. The lint script runs formatting first, then checks for linting errors.

uv run lint


If you only want to format the code without linting, you can run ruff directly:

uv run ruff format .


3. Other Common Commands

Generating OpenAPI Schema

This regenerates the openapi/openapi.json file based on the current FastAPI code. Commit this file after any API changes.

# With a valid config file
uv run gen_openapi --config tests/fixtures/sample_mcp.toml

# If you don't have a config file yet
uv run gen_openapi --allow-missing-config


Pre-Commit Hooks

The uv run mcp-setup command should install these for you. If you need to manage them manually:

# Manually install hooks (if setup script failed)
uv run pre-commit install

# Run hooks on all files (useful for CI)
uv run pre-commit run --all-files


Building the Project

This project uses hatch as its build backend.

# Build the project (creates a .whl file in /dist)
uv run hatch build


4. Docker Commands

You can build and run the project as a container, which mirrors the production environment.

Building the Image

docker build -t mcp-metadata-broker:dev .


Running the Container

This command runs the container, forwards port 8000, and securely mounts a local config file.

docker run --rm -p 8000:8000 \
-e MCP_CONFIG_PATH=/configs/mcp.toml \
-v /path/to/your/local-mcp.toml:/configs/mcp.toml:ro \
mcp-metadata-broker:dev


--rm: Automatically remove the container when it exits.

-p 8000:8000: Maps port 8000 on your machine to port 8000 in the container.

-e MCP_CONFIG_PATH=[ELIDED]: Sets the environment variable inside the container.

-v /path/to/your/local-mcp.toml:[ELIDED]:ro: Mounts your local config file as read-only.

5. Troubleshooting & "Why?"

"command not found: pytest" or "command not found: lint"

If you see this, you have activated your virtual environment but your development dependencies are not installed. This happens if you only run uv sync and forget the second setup step.

✅ Solution: Run the setup script. This will install pytest, ruff, pre-commit, etc.

uv run mcp-setup


Why uv run [ELIDED]?

Using uv run ensures that you are always using the exact version of a tool (like pytest or ruff) that is pinned for this project. It's the Python equivalent of npm run [ELIDED] or bun run [ELIDED] and avoids conflicts with tools installed globally on your machine.

WSL vs. Windows (.venv vs. .venv2)

As noted in AGENTS.md, you may see both .venv (for Linux/WSL) and .venv2 (for Windows). Both are intentional.

Always run uv commands from the environment you are currently in (WSL or Windows).

The uv run [ELIDED] workflow ensures your commands will work in both environments without changes.

Do not delete either .venv directory.