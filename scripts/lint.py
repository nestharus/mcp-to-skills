import shutil
import subprocess
import sys


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
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        return getattr(exc, "returncode", 1)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
