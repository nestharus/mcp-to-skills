"""Helper to display the configured MCP metadata entry point."""

from pathlib import Path
from typing import Any

import tomllib


def load_metadata_descriptor(config_path: str) -> dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"MCP config not found at {path}")
    with path.open("rb") as file:
        try:
            return tomllib.load(file)
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"Invalid TOML format in {path}: {exc}") from exc


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Show MCP metadata configuration")
    parser.add_argument("config", help="Path to the MCP TOML file")
    args = parser.parse_args()
    descriptor = load_metadata_descriptor(args.config)
    print("Loaded metadata descriptor:")
    print(descriptor)


if __name__ == "__main__":
    main()
