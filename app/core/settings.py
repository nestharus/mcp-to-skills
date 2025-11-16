from __future__ import annotations

import math
import tomllib
from pathlib import Path
from typing import Final, Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

_CONFIG_CACHE: dict[Path, tuple[int, dict]] = {}
_ALLOWED_SERVER_KEYS: Final = ("command", "args", "startup_timeout_sec")


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables and an MCP TOML file.

    The MCP config path comes from the ``MCP_CONFIG_PATH`` environment variable and must
    point to a TOML file containing ``[mcp_servers.<name>]`` tables. Each server entry
    requires ``command`` (str), ``args`` (list[str]), and ``startup_timeout_sec``
    (float > 0). Setting ``allow_missing_config=True`` skips TOML parsing, which is used
    for tests and tooling; otherwise the application fails fast if the config file is
    missing, unreadable, or invalid. Parsed server definitions are exposed via
    ``mcp_servers``. The ``include_error_body`` flag (default: ``False``) controls
    whether validation error responses echo the original request body so operators can
    enable verbose diagnostics when needed.
    """

    mcp_config_path: str | None = None
    allow_missing_config: bool = False
    mcp_servers: dict[str, dict] = Field(default_factory=dict)
    include_error_body: bool = False

    @model_validator(mode="after")
    def validate_mcp_config(self) -> Self:
        """Validate MCP config path and parse TOML to populate ``mcp_servers``.

        When ``allow_missing_config`` is true and ``mcp_config_path`` is ``None`` the
        validator returns immediately. Otherwise it ensures the path exists and is a
        file, parses the TOML via ``tomllib``, verifies an ``[mcp_servers]`` table is
        present, checks every server entry defines the required keys with the correct
        types, and normalizes ``startup_timeout_sec`` to ``float``. Any issue raises a
        ``ValueError`` so misconfigurations surface during application start-up.
        """
        path = self._resolve_config_path()
        if path is None:
            self.mcp_servers = {}
            return self

        parsed = self._load_toml_config(path)
        servers = self._extract_servers(parsed)
        self.mcp_servers = self._validate_servers(servers)
        return self

    def _resolve_config_path(self) -> Path | None:
        value = self.mcp_config_path
        if value is None:
            if not self.allow_missing_config:
                raise ValueError("MCP_CONFIG_PATH must be set")
            return None

        path = Path(value).expanduser()
        if not path.exists():
            raise ValueError(f"Config file not found: {path}")
        if not path.is_file():
            raise ValueError(f"Config path is not a file: {path}")
        return path

    def _load_toml_config(self, path: Path) -> dict:
        resolved = path.resolve()
        try:
            mtime_ns = path.stat().st_mtime_ns
        except OSError as exc:
            raise ValueError(f"Cannot read {path}: {exc}") from exc

        cached = _CONFIG_CACHE.get(resolved)
        if cached is not None and cached[0] == mtime_ns:
            return cached[1]

        try:
            with path.open("rb") as file_obj:
                parsed = tomllib.load(file_obj)
        except OSError as exc:
            raise ValueError(f"Cannot read {path}: {exc}") from exc
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"Invalid TOML format in {path}: {exc}") from exc

        _CONFIG_CACHE[resolved] = (mtime_ns, parsed)
        return parsed

    @staticmethod
    def _extract_servers(parsed: dict) -> dict:
        servers = parsed.get("mcp_servers")
        if servers is None:
            raise ValueError("TOML file must contain an [mcp_servers] section")
        if not isinstance(servers, dict):
            raise ValueError("The [mcp_servers] section must be a table")
        return servers

    def _validate_servers(self, servers: dict[str, dict]) -> dict[str, dict]:
        validated: dict[str, dict] = {}
        for name, config in servers.items():
            validated[name] = self._validate_single_server(name, config)
        return validated

    def _validate_single_server(self, name: str, config: dict | object) -> dict:
        if not isinstance(config, dict):
            raise ValueError(f"Server '{name}' configuration must be a table")

        command = config.get("command")
        if not isinstance(command, str) or not command:
            raise ValueError(f"Server '{name}' must define a non-empty 'command' string")

        args = config.get("args")
        if not isinstance(args, list):
            raise ValueError(f"Server '{name}' must define an 'args' list")
        for arg in args:
            if not isinstance(arg, str):
                raise ValueError(f"Server '{name}' has a non-string argument in 'args': {arg}")

        timeout = self._normalize_timeout(name, config)

        normalized_args = list(args)

        normalized_values = (command, normalized_args, timeout)
        return dict(zip(_ALLOWED_SERVER_KEYS, normalized_values, strict=True))

    def _normalize_timeout(self, name: str, config: dict) -> float:
        if "startup_timeout_sec" not in config:
            raise ValueError(f"Server '{name}' must define 'startup_timeout_sec' (float > 0)")
        value = config["startup_timeout_sec"]
        # startup_timeout_sec values are specified in seconds.
        if isinstance(value, bool):
            raise ValueError(f"Server '{name}' has boolean 'startup_timeout_sec'")
        try:
            timeout = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Server '{name}' has non-numeric 'startup_timeout_sec'") from exc
        if timeout <= 0 or not math.isfinite(timeout):
            raise ValueError(
                f"Server '{name}' has invalid 'startup_timeout_sec' (must be finite and > 0)"
            )
        return timeout
