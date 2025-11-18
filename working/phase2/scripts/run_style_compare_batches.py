from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SLICES_DIR = ROOT / "working" / "phase2" / "style_slices"
PROMPTS_DIR = ROOT / "working" / "phase2" / "style_compare_prompts"


def _build_prompt(slice_path: Path) -> str:
    slice_text = slice_path.read_text(encoding="utf-8")
    return f"""You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/{slice_path.parent.name}.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in
`docs/code-style-guide.md` so that no important guidance from this slice is lost,
resolving any conflicts in favor of the current ADRs, `pyproject.toml`, and the
existing codebase behavior.

--- SOURCE SECTION START ---
{slice_text}
--- SOURCE SECTION END ---
"""


def _ensure_prompts() -> list[Path]:
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    prompt_paths: list[Path] = []

    for style_dir in sorted(SLICES_DIR.glob("STYLE_*")):
        for slice_path in sorted(style_dir.glob("*.md")):
            prompt_name = slice_path.stem + ".prompt.md"
            prompt_path = PROMPTS_DIR / prompt_name
            prompt_text = _build_prompt(slice_path)
            prompt_path.write_text(prompt_text, encoding="utf-8")
            prompt_paths.append(prompt_path)

    return prompt_paths


def _droid_exec(prompt_path: Path) -> int:
    cmd = ["droid", "exec", "--file", str(prompt_path)]
    completed = subprocess.run(cmd, cwd=ROOT)
    return completed.returncode


def main() -> None:
    if not SLICES_DIR.exists():
        raise SystemExit(f"Style slices directory not found: {SLICES_DIR}")

    prompt_paths = _ensure_prompts()
    failures: list[Path] = []

    for prompt_path in prompt_paths:
        code = _droid_exec(prompt_path)
        if code != 0:
            failures.append(prompt_path)

    if failures:
        failed = "\n".join(str(p) for p in failures)
        raise SystemExit(f"droid exec failed for prompts:\n{failed}")


if __name__ == "__main__":  # pragma: no cover - manual utility
    main()
