import shutil
import subprocess


def run_pre_commit_install() -> None:
    """Invoke `pre-commit install` through uv so dev dependencies are always available."""
    uv_exe = shutil.which("uv")
    if uv_exe is None:
        raise RuntimeError("The `uv` CLI must be installed and on PATH to run project setup.")

    subprocess.check_call([uv_exe, "run", "--group", "dev", "pre-commit", "install"])


def main() -> int:
    try:
        run_pre_commit_install()
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(
            "Failed to install pre-commit hooks; try `uv run pre-commit install` manually or "
            "`uv sync --group dev` if dependencies are missing."
        )
        return getattr(exc, "returncode", 1)

    print("Pre-commit hooks installed! Run `uv run pre-commit run --all-files` to validate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
