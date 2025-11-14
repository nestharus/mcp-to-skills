"""
Utility to launch the MCP metadata broker via Uvicorn.

Required environment variables:
    MCP_CONFIG_PATH: Path to the MCP configuration TOML file.
"""

import os
import sys

import uvicorn

from app.core.dependencies import get_settings
from app.core.factory import create_app


def main() -> None:
    try:
        settings = get_settings()
    except Exception as exc:
        print(
            "Failed to load settings: ensure MCP_CONFIG_PATH points to a valid file.",
            file=sys.stderr,
        )
        print(f"Details: {exc}", file=sys.stderr)
        sys.exit(1)

    app = create_app(settings)
    host = os.environ.get("HOST", "0.0.0.0")
    try:
        port = int(os.environ.get("PORT", "8000"))
    except ValueError:
        print("PORT environment variable must be an integer.", file=sys.stderr)
        sys.exit(1)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
