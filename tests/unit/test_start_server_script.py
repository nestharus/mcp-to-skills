"""Behavioral tests for the start-server CLI helpers."""

from importlib import util
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
START_SERVER_PATH = ROOT / "scripts" / "start-server.py"
SPEC = util.spec_from_file_location("start_server_script", START_SERVER_PATH)
assert SPEC is not None  # pragma: no cover - import sanity guard
start_server = util.module_from_spec(SPEC)  # type: ignore[arg-type]
assert SPEC.loader is not None  # pragma: no cover - import sanity guard
SPEC.loader.exec_module(start_server)  # type: ignore[union-attr]


def _args(**kwargs: object) -> SimpleNamespace:
    return SimpleNamespace(**kwargs)


def test_resolve_host_defaults_to_loopback():
    env = {}
    args = _args(host=None)

    assert start_server._resolve_host(args, env) == "127.0.0.1"


def test_resolve_host_prefers_cli_argument():
    env = {"HOST": "10.0.0.5"}
    args = _args(host="0.0.0.0")

    assert start_server._resolve_host(args, env) == "0.0.0.0"


def test_resolve_host_prefers_env_over_default():
    env = {"HOST": "10.1.2.3"}
    args = _args(host=None)

    assert start_server._resolve_host(args, env) == "10.1.2.3"


def test_resolve_host_ignores_blank_cli_value():
    env = {"HOST": "10.2.3.4"}
    args = _args(host="   ")

    assert start_server._resolve_host(args, env) == "10.2.3.4"


def test_resolve_host_treats_empty_env_as_unset():
    env = {"HOST": "   "}
    args = _args(host=None)

    assert start_server._resolve_host(args, env) == "127.0.0.1"


def test_resolve_host_rejects_host_with_port_from_cli():
    env = {}
    args = _args(host="localhost:9000")

    with pytest.raises(SystemExit):
        start_server._resolve_host(args, env)


def test_resolve_host_rejects_host_with_port_from_env():
    env = {"HOST": "[::1]:9000"}
    args = _args(host=None)

    with pytest.raises(SystemExit):
        start_server._resolve_host(args, env)


def test_resolve_host_accepts_ipv6_zone_identifier():
    env = {}
    args = _args(host="[fe80::1%25eth0]")

    assert start_server._resolve_host(args, env) == "[fe80::1%25eth0]"


@pytest.mark.parametrize(
    ("host", "expected"),
    [
        ("0.0.0.0", "127.0.0.1"),  # noqa: S104
        ("::", "[::1]"),
        ("[::]", "[::1]"),
        ("", "localhost"),
        ("   ", "localhost"),
        ("example.com", "example.com"),
        ("2001:db8::1", "[2001:db8::1]"),
        ("[2001:db8::1]", "[2001:db8::1]"),
    ],
)
def test_format_health_probe_host_normalizes_wildcards(host, expected):
    assert start_server._format_health_probe_host(host) == expected


@pytest.mark.parametrize(
    ("host", "expected"),
    [
        ("fe80::1%eth0", "[fe80::1%25eth0]"),
        ("[fe80::1%eth0]", "[fe80::1%25eth0]"),
        ("[fe80::1%25eth0]", "[fe80::1%25eth0]"),
    ],
)
def test_format_health_probe_host_encodes_zone_identifier(host, expected):
    assert start_server._format_health_probe_host(host) == expected
