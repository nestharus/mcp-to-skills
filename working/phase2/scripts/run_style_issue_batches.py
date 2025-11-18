from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLANS_DIR = ROOT / "working" / "phase2" / "style_plans"


def _droid_exec(plan_path: Path) -> int:
    """Run `droid exec` for a single plan file.

    This assumes `droid` is available on PATH and that the working directory
    is the repository root so file paths in the plan are valid.
    """

    cmd = ["droid", "exec", "--file", str(plan_path)]
    completed = subprocess.run(cmd, cwd=ROOT)
    return completed.returncode


def main() -> None:
    if not PLANS_DIR.exists():
        raise SystemExit(f"Plan directory not found: {PLANS_DIR}")

    failures: list[Path] = []
    for plan_path in sorted(PLANS_DIR.glob("STYLE_*.plan.md")):
        code = _droid_exec(plan_path)
        if code != 0:
            failures.append(plan_path)

    if failures:
        failed = "\n".join(str(p) for p in failures)
        raise SystemExit(f"droid exec failed for:\n{failed}")


if __name__ == "__main__":  # pragma: no cover - manual utility
    main()
