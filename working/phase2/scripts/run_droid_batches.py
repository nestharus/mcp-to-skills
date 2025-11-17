from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
BATCH_DIR = REPO_ROOT / "working" / "phase2" / "batches"
RESULT_DIR = REPO_ROOT / "working" / "phase2" / "batch_results"


def main() -> int:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    for batch_path in sorted(BATCH_DIR.glob("classify_batch_*.md")):
        result_path = RESULT_DIR / f"{batch_path.stem}.json"
        print(
            "Running droid for "
            f"{batch_path.relative_to(REPO_ROOT)} -> "
            f"{result_path.relative_to(REPO_ROOT)}",
        )
        with result_path.open("w", encoding="utf-8") as out:
            proc = subprocess.run(
                [
                    "droid",
                    "exec",
                    "--auto",
                    "high",
                    "-f",
                    str(batch_path),
                ],
                cwd=str(REPO_ROOT),
                stdout=out,
            )
        if proc.returncode != 0:
            print(f"droid exec failed for {batch_path} with code {proc.returncode}")
            return proc.returncode

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
