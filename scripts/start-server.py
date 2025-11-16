"""Launch the MCP metadata broker with CLI controls and health validation."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Sequence
from typing import Any

# Bind to loopback by default for safer local development; pass --host 0.0.0.0
# (or another interface) explicitly when exposing the service outside localhost.
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
HEALTH_CHECK_DELAY = 5
HEALTH_CHECK_RETRIES = 3
HEALTH_CHECK_INTERVAL = 2


def _format_health_probe_host(host: str) -> str:
    """Return a host suitable for health-check URLs, normalizing wildcards."""

    hostname = host.strip() or "localhost"
    if hostname == "0.0.0.0":
        hostname = "127.0.0.1"
    elif hostname in {"::", "[::]"}:
        hostname = "::1"

    if "%" in hostname and _is_ipv6_host(hostname):
        hostname = re.sub(r"%(?!25)", "%25", hostname)

    if ":" in hostname:
        if hostname.startswith("[") and hostname.endswith("]"):
            return hostname
        return f"[{hostname}]"

    return hostname


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Launch the MCP metadata broker via Uvicorn with health checks."
    )
    parser.add_argument(
        "--config-path",
        help="Path to MCP config TOML; overrides MCP_CONFIG_PATH env var.",
    )
    parser.add_argument(
        "--host",
        help=(
            "Server bind address (default: env HOST or 127.0.0.1 for local runs; "
            "pass 0.0.0.0 to listen on all interfaces)."
        ),
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Server port (default: env PORT or 8000).",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable autoreload; useful for development.",
    )
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Explicitly disable autoreload.",
    )
    parser.add_argument(
        "--skip-health-check",
        action="store_true",
        help="Skip the post-start health probe (not recommended).",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.reload and args.no_reload:
        parser.error("--reload and --no-reload are mutually exclusive.")
    return args


def _terminate_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    try:
        process.terminate()
    except OSError:
        return
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except OSError:
            return
        try:
            process.wait(timeout=5)
        except (subprocess.TimeoutExpired, OSError):
            pass


def _ensure_process_running(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        return
    print("Uvicorn process exited before health check completed.", file=sys.stderr)
    sys.exit(process.returncode)


def _request_health_payload(url: str) -> dict[str, Any]:
    # url is always a fixed http://.../health endpoint, so urllib here is safe.
    with urllib.request.urlopen(url, timeout=3) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected status {response.status}")
        payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("Unexpected non-object payload")
        return payload


def _handle_probe_error(attempt: int, exc: Exception, process: subprocess.Popen[bytes]) -> None:
    if attempt == HEALTH_CHECK_RETRIES:
        print(
            f"Health check failed after {HEALTH_CHECK_RETRIES} attempts: {exc}",
            file=sys.stderr,
        )
        _terminate_process(process)
        sys.exit(1)
    time.sleep(HEALTH_CHECK_INTERVAL)


def _handle_unexpected_payload(attempt: int, process: subprocess.Popen[bytes]) -> None:
    print("Health endpoint returned unexpected payload.", file=sys.stderr)
    if attempt == HEALTH_CHECK_RETRIES:
        _terminate_process(process)
        sys.exit(1)
    time.sleep(HEALTH_CHECK_INTERVAL)


def _prepare_environment(args: argparse.Namespace) -> dict[str, str]:
    env = os.environ.copy()
    if args.config_path:
        env["MCP_CONFIG_PATH"] = args.config_path
    return env


def _normalize_host_value(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _is_ipv6_host(host: str) -> bool:
    candidate = host
    if candidate.startswith("[") and candidate.endswith("]"):
        candidate = candidate[1:-1]
    # Strip RFC 4007 zone identifier (e.g., "%eth0" or "%25eth0") before validation
    zone_index = candidate.rfind("%")
    if zone_index != -1:
        candidate = candidate[:zone_index]
    try:
        ipaddress.IPv6Address(candidate)
    except ValueError:
        return False
    return True


def _resolve_host(args: argparse.Namespace, env: dict[str, str]) -> str:
    cli_host = _normalize_host_value(getattr(args, "host", None))
    env_host = _normalize_host_value(env.get("HOST"))
    host = cli_host or env_host or DEFAULT_HOST

    if ":" in host and not _is_ipv6_host(host):
        print(
            "Host value must not include a port; use --port or the PORT environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)

    return host


def _resolve_port(args: argparse.Namespace, env: dict[str, str]) -> int:
    if args.port is not None:
        port = args.port
    else:
        env_port = env.get("PORT")
        if env_port is None:
            port = DEFAULT_PORT
        else:
            try:
                port = int(env_port)
            except ValueError:
                print("PORT environment variable must be an integer.", file=sys.stderr)
                sys.exit(1)

    if not (1 <= port <= 65535):
        print("Port must be between 1 and 65535 (health check cannot use 0).", file=sys.stderr)
        sys.exit(1)

    return port


def _build_uvicorn_command(host: str, port: int, *, reload_enabled: bool) -> list[str]:
    bind_host = host[1:-1] if host.startswith("[") and host.endswith("]") else host
    command = [
        "uvicorn",
        "app.main:app",
        "--host",
        bind_host,
        "--port",
        str(port),
    ]
    if reload_enabled:
        command.append("--reload")
    return command


def _launch_uvicorn(command: list[str], env: dict[str, str]) -> subprocess.Popen[bytes]:
    try:
        return subprocess.Popen(command, env=env)
    except FileNotFoundError as exc:
        print(
            f"uvicorn executable not found: {exc}. Install uvicorn in the active environment.",
            file=sys.stderr,
        )
        sys.exit(1)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"Failed to launch uvicorn: {exc}", file=sys.stderr)
        sys.exit(1)


def _install_signal_handlers(process: subprocess.Popen[bytes]) -> None:
    def forward_signal(signum: int, _frame: object) -> None:
        if process.poll() is None:
            try:
                process.send_signal(signum)
            except OSError:
                pass

    signal.signal(signal.SIGINT, forward_signal)
    signal.signal(signal.SIGTERM, forward_signal)


def _wait_for_process(process: subprocess.Popen[bytes]) -> int:
    try:
        return process.wait()
    finally:
        if process.poll() is None:
            _terminate_process(process)


def perform_health_check(
    host: str,
    port: int,
    process: subprocess.Popen[bytes],
) -> None:
    time.sleep(HEALTH_CHECK_DELAY)
    probe_host = _format_health_probe_host(host)
    url = f"http://{probe_host}:{port}/health"
    for attempt in range(1, HEALTH_CHECK_RETRIES + 1):
        _ensure_process_running(process)
        try:
            payload = _request_health_payload(url)
        except (
            RuntimeError,
            TypeError,
            json.JSONDecodeError,
            UnicodeDecodeError,
            OSError,
        ) as exc:
            _handle_probe_error(attempt, exc, process)
            continue
        if payload.get("status") == "ok":
            print("Service healthy; continuing to run.")
            return
        _handle_unexpected_payload(attempt, process)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    env = _prepare_environment(args)
    host = _resolve_host(args, env)
    port = _resolve_port(args, env)
    reload_enabled = args.reload and not args.no_reload
    command = _build_uvicorn_command(host, port, reload_enabled=reload_enabled)
    process = _launch_uvicorn(command, env)

    _install_signal_handlers(process)

    if not args.skip_health_check:
        perform_health_check(host, port, process)

    exit_code = _wait_for_process(process)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
