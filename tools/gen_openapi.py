"""Generate the OpenAPI schema JSON for the MCP Metadata Broker."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

import orjson
from fastapi import FastAPI


def ensure_config_path(config: str | None, *, allow_missing: bool = False) -> str | None:
    """Ensure MCP_CONFIG_PATH is set and references an optional file."""

    config_path: Path | None = None

    if config:
        config_path = Path(config)
    else:
        env_value = os.environ.get("MCP_CONFIG_PATH")
        if env_value:
            config_path = Path(env_value)

    if config_path is None:
        if allow_missing:
            os.environ.pop("MCP_CONFIG_PATH", None)
            return None
        raise RuntimeError(
            "MCP configuration path is required. "
            "Use --config or set MCP_CONFIG_PATH in the environment."
        )

    if not allow_missing and not config_path.exists():
        raise FileNotFoundError(f"MCP config not found at {config_path}")

    os.environ["MCP_CONFIG_PATH"] = str(config_path)
    return str(config_path)


def build_application(*, allow_missing_config: bool = False) -> FastAPI:
    """Import and instantiate the FastAPI application."""

    from app.main import get_application

    return get_application(allow_missing_config=allow_missing_config)


def generate_schema(app: FastAPI) -> dict[str, Any]:
    """Return the OpenAPI schema dictionary."""

    schema = app.openapi()
    if not isinstance(schema, dict):
        raise TypeError(f"Expected dict schema from FastAPI, got {type(schema).__name__}.")
    return schema


def write_schema(schema: dict[str, Any], output_path: Path) -> None:
    """Serialize the schema to JSON and write it to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        payload = orjson.dumps(schema, option=orjson.OPT_INDENT_2).decode("utf-8")
    except orjson.JSONEncodeError as exc:
        raise RuntimeError("Failed to serialize OpenAPI schema.") from exc
    output_path.write_text(payload, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the OpenAPI schema JSON for the MCP Metadata Broker."
    )
    parser.add_argument(
        "--config",
        help="Path to the MCP TOML file (defaults to MCP_CONFIG_PATH environment variable).",
    )
    parser.add_argument(
        "--output",
        default="openapi/openapi.json",
        help="Path to write the generated OpenAPI JSON (default: openapi/openapi.json).",
    )
    parser.add_argument(
        "--allow-missing-config",
        action="store_true",
        help=(
            "Skip MCP config existence checks; useful when generating a schema before "
            "an MCP configuration file exists."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        ensure_config_path(args.config, allow_missing=args.allow_missing_config)
        app = build_application(allow_missing_config=args.allow_missing_config)
        schema = generate_schema(app)
        output_path = Path(args.output)
        write_schema(schema, output_path)
    except Exception as exc:
        print(f"Failed to generate OpenAPI schema: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"Wrote OpenAPI schema to {output_path}")


if __name__ == "__main__":
    main()
