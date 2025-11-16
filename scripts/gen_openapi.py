"""Entry point for generating the OpenAPI schema via `uv run gen_openapi`."""

from __future__ import annotations

from tools.gen_openapi import main as generate_openapi


def main() -> int:
    generate_openapi()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
