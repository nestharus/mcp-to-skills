"""Validation tests for Settings TOML loading."""

from pathlib import Path

import pytest

from app.core.settings import Settings


def _write_config(tmp_path, body: str) -> Path:
    path = tmp_path / "config.toml"
    path.write_text(body, encoding="utf-8")
    return path


def test_settings_loads_valid_toml(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y", "chrome" ]
startup_timeout_sec = 45
""",
    )

    settings = Settings(mcp_config_path=str(config))

    assert "chrome" in settings.mcp_servers
    assert settings.mcp_servers["chrome"]["command"] == "npx"
    assert settings.mcp_servers["chrome"]["startup_timeout_sec"] == 45.0


def test_settings_strips_unexpected_server_keys(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y", "chrome" ]
startup_timeout_sec = 45
extra = "ignored"
""",
    )

    settings = Settings(mcp_config_path=str(config))

    server_config = settings.mcp_servers["chrome"]
    assert server_config == {
        "command": "npx",
        "args": ["-y", "chrome"],
        "startup_timeout_sec": 45.0,
    }


def test_settings_rejects_missing_command(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
args = []
startup_timeout_sec = 30
""",
    )

    with pytest.raises(ValueError, match="non-empty 'command' string"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_non_list_args(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = "not-a-list"
startup_timeout_sec = 30
""",
    )

    with pytest.raises(ValueError, match="must define an 'args' list"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_args_with_non_string_item(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y", 123]
startup_timeout_sec = 30
""",
    )

    with pytest.raises(ValueError, match="non-string argument in 'args'"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_invalid_timeout(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y"]
startup_timeout_sec = 0
""",
    )

    with pytest.raises(ValueError, match="must be finite and > 0"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_negative_timeout(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y"]
startup_timeout_sec = -5
""",
    )

    with pytest.raises(ValueError, match="must be finite and > 0"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_infinite_timeout(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y"]
startup_timeout_sec = inf
""",
    )

    with pytest.raises(ValueError, match="must be finite and > 0"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_nan_timeout(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y"]
startup_timeout_sec = nan
""",
    )

    with pytest.raises(ValueError, match="must be finite and > 0"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_missing_timeout(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y"]
""",
    )

    with pytest.raises(ValueError, match="must define 'startup_timeout_sec'"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_boolean_timeout(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y"]
startup_timeout_sec = true
""",
    )

    with pytest.raises(ValueError, match="has boolean 'startup_timeout_sec'"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_non_numeric_timeout(tmp_path):
    config = _write_config(
        tmp_path,
        """
[mcp_servers.chrome]
command = "npx"
args = ["-y"]
startup_timeout_sec = "not-a-number"
""",
    )

    with pytest.raises(ValueError, match="non-numeric 'startup_timeout_sec'"):
        Settings(mcp_config_path=str(config))


def test_settings_requires_mcp_servers_section(tmp_path):
    config = _write_config(tmp_path, 'command = "npx"')

    with pytest.raises(ValueError, match=r"must contain an \[mcp_servers] section"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_non_table_mcp_servers(tmp_path):
    config = _write_config(
        tmp_path,
        'mcp_servers = "oops"',
    )

    with pytest.raises(ValueError, match="must be a table"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_non_table_server_entry(tmp_path):
    config = _write_config(
        tmp_path,
        ('[mcp_servers]\nchrome = "oops"'),
    )

    with pytest.raises(ValueError, match="configuration must be a table"):
        Settings(mcp_config_path=str(config))


def test_settings_rejects_invalid_toml(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("[mcp_servers", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid TOML format"):
        Settings(mcp_config_path=str(path))


def test_settings_allows_missing_config_when_flag_set():
    settings = Settings(mcp_config_path=None, allow_missing_config=True)

    assert settings.mcp_servers == {}


def test_sample_fixture_is_valid():
    fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "sample_mcp.toml"

    settings = Settings(mcp_config_path=str(fixture_path))

    assert "test-server" in settings.mcp_servers
