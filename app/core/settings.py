from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mcp_config_path: str | None = None
    allow_missing_config: bool = False

    @model_validator(mode="after")
    def validate_mcp_config(self) -> Self:
        value = self.mcp_config_path
        allow_missing = self.allow_missing_config

        if value is None:
            if not allow_missing:
                raise ValueError("MCP_CONFIG_PATH must be set")
        else:
            path = Path(value)
            if not path.exists():
                raise ValueError(f"Config file not found: {path}")
            if not path.is_file():
                raise ValueError(f"Config path is not a file: {path}")
        return self
