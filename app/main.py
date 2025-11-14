"""WSGI/ASGI entry point for the MCP metadata broker.

Required environment variables:
    MCP_CONFIG_PATH: Path to the MCP configuration TOML file.
"""

import sys

from fastapi import FastAPI

from app.core.dependencies import get_settings
from app.core.factory import create_app


def get_application(*, allow_missing_config: bool = False) -> FastAPI:
    """Create and return a configured FastAPI instance."""

    try:
        settings = get_settings(allow_missing_config=allow_missing_config)
    except Exception as exc:
        print(
            "Failed to load settings: ensure MCP_CONFIG_PATH points to a valid file.",
            file=sys.stderr,
        )
        print(f"Details: {exc}", file=sys.stderr)
        sys.exit(1)

    return create_app(settings)


app = get_application()
