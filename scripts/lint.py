import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OPENAPI_SCHEMA = REPO_ROOT / "openapi" / "openapi.json"
CHECKOV_CONFIG = REPO_ROOT / ".checkov.yaml"


def _uv() -> str:
    uv_exe = shutil.which("uv")
    if uv_exe is None:
        raise RuntimeError("The `uv` CLI must be installed to run lint.")
    return uv_exe


def main() -> int:
    try:
        uv_exe = _uv()
        subprocess.check_call([uv_exe, "run", "ruff", "format", "."])
        subprocess.check_call([uv_exe, "run", "ruff", "check", "--fix", "."])
        if not OPENAPI_SCHEMA.exists():
            print(
                f"OpenAPI schema missing at {OPENAPI_SCHEMA}. "
                "Run `uv run gen_openapi --config tests/fixtures/sample_mcp.toml` first.",
                file=sys.stderr,
            )
            return 1

        subprocess.check_call(
            [
                uv_exe,
                "run",
                "checkov",
                "--config-file",
                str(CHECKOV_CONFIG),
                "--framework",
                "openapi",
                "-f",
                str(OPENAPI_SCHEMA),
            ]
        )
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        return getattr(exc, "returncode", 1)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
