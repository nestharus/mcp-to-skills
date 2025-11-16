#!/usr/bin/env bash
set -euo pipefail

# Consume stdin (JSON payload from Droid) so hooks do not leave input pending.
cat >/dev/null || true

# Run from project root provided by Factory for consistent paths.
cd "$FACTORY_PROJECT_DIR"

echo "Running ruff lint..."
uv run ruff check

echo "Running python tests..."
uv run pytest
