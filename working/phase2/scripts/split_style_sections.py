from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STYLE_DIR = ROOT / "docs" / "to_integrate"
SLICES_DIR = ROOT / "working" / "phase2" / "style_slices"


def _split_sections(text: str) -> list[list[str]]:
    lines = text.splitlines(keepends=True)
    sections: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line.startswith("## ") and current:
            sections.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append(current)
    return sections


def _pair_sections(sections: list[list[str]]) -> list[list[str]]:
    pairs: list[list[str]] = []
    for i in range(0, len(sections), 2):
        chunk = sections[i : i + 2]
        merged: list[str] = []
        for sec in chunk:
            merged.extend(sec)
        pairs.append(merged)
    return pairs


def main() -> None:
    SLICES_DIR.mkdir(parents=True, exist_ok=True)
    for i in range(1, 9):
        style_name = f"STYLE_{i}.md"
        style_path = STYLE_DIR / style_name
        if not style_path.exists():
            continue

        text = style_path.read_text(encoding="utf-8")
        sections = _split_sections(text)
        pairs = _pair_sections(sections)

        target_dir = SLICES_DIR / f"STYLE_{i}"
        target_dir.mkdir(parents=True, exist_ok=True)

        for idx, pair in enumerate(pairs, start=1):
            slice_path = target_dir / f"STYLE_{i}_pair_{idx:02d}.md"
            header = (
                f"# STYLE_{i} section pair {idx}\n\n"
                f"This file contains one or two `##` sections from "
                f"docs/to_integrate/STYLE_{i}.md.\n\n"
            )
            slice_path.write_text(header + "".join(pair), encoding="utf-8")


if __name__ == "__main__":  # pragma: no cover - manual utility
    main()
