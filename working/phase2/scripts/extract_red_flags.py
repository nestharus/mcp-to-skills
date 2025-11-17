from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
SUMMARIES_ROOT = REPO_ROOT / "working" / "phase1" / "summaries"
INDEX_CSV_PATH = REPO_ROOT / "working" / "phase2" / "issues_index.csv"


RED_FLAGS_HEADER_RE = re.compile(r"^##\s+Red Flags\s*$", re.IGNORECASE)
BULLET_RE = re.compile(r"^(?P<prefix>(?:\d+\.|[-*+])\s+)(?P<text>.+?)\s*$")
ISSUE_ID_RE = re.compile(r"\[ISS-(?P<num>\d{4})]$")


@dataclass
class RedFlag:
    issue_id: str
    doc: str
    line_no: int
    description_text: str


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        if path.is_file():
            yield path


def load_existing_index(
    csv_path: Path,
) -> Tuple[List[dict], Dict[Tuple[str, int], dict], int]:
    if not csv_path.exists():
        return [], {}, 0

    rows: List[dict] = []
    by_key: Dict[Tuple[str, int], dict] = {}
    highest_id = 0

    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            key = (row.get("doc", ""), int(row.get("line_no", 0) or 0))
            by_key[key] = row
            m = re.search(r"ISS-(\d{4})", row.get("id", ""))
            if m:
                highest_id = max(highest_id, int(m.group(1)))

    return rows, by_key, highest_id


def parse_red_flags(
    path: Path,
    existing_by_key: Dict[Tuple[str, int], dict],
    start_index: int,
) -> Tuple[List[RedFlag], int]:
    rel_doc = path.relative_to(REPO_ROOT).as_posix()
    flags: List[RedFlag] = []
    in_red_flags = False
    current_index = start_index

    content = path.read_text(encoding="utf-8").splitlines()

    for lineno, line in enumerate(content, start=1):
        if RED_FLAGS_HEADER_RE.match(line):
            in_red_flags = True
            continue
        if in_red_flags and line.startswith("## ") and not RED_FLAGS_HEADER_RE.match(line):
            break
        if not in_red_flags:
            continue

        match = BULLET_RE.match(line)
        if not match:
            continue

        text = match.group("text").rstrip()

        existing = existing_by_key.get((rel_doc, lineno))
        if existing:
            issue_id = existing.get("id", "")
        else:
            tag_match = ISSUE_ID_RE.search(text)
            if tag_match:
                issue_id = f"ISS-{int(tag_match.group('num')):04d}"
            else:
                current_index += 1
                issue_id = f"ISS-{current_index:04d}"

        flags.append(
            RedFlag(
                issue_id=issue_id,
                doc=rel_doc,
                line_no=lineno,
                description_text=text,
            ),
        )

    return flags, current_index


def annotate_file(path: Path, flags: List[RedFlag]) -> None:
    if not flags:
        return

    by_line = {flag.line_no: flag for flag in flags}
    lines = path.read_text(encoding="utf-8").splitlines()

    for lineno, line in enumerate(lines, start=1):
        flag = by_line.get(lineno)
        if not flag:
            continue

        match = BULLET_RE.match(line)
        if not match:
            continue

        prefix = match.group("prefix")
        text = match.group("text").rstrip()

        if ISSUE_ID_RE.search(text):
            continue

        lines[lineno - 1] = f"{prefix}{text} [{flag.issue_id}]"

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def merge_and_write_csv(
    existing_rows: List[dict],
    new_flags: List[RedFlag],
    csv_path: Path,
) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    by_key: Dict[Tuple[str, int], dict] = {}
    for row in existing_rows:
        key = (row.get("doc", ""), int(row.get("line_no", 0) or 0))
        by_key[key] = row

    for flag in new_flags:
        key = (flag.doc, flag.line_no)
        if key in by_key:
            by_key[key]["description_text"] = flag.description_text
            by_key[key]["id"] = flag.issue_id
        else:
            by_key[key] = {
                "id": flag.issue_id,
                "doc": flag.doc,
                "line_no": flag.line_no,
                "description_text": flag.description_text,
                "issue_type": "",
                "classification": "UNCLASSIFIED",
                "classification_ref": "",
                "notes": "",
            }

    fieldnames = [
        "id",
        "doc",
        "line_no",
        "description_text",
        "issue_type",
        "classification",
        "classification_ref",
        "notes",
    ]

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(by_key.values(), key=lambda r: (r["doc"], int(r["line_no"]))):
            writer.writerow(row)


def main() -> int:
    if not SUMMARIES_ROOT.exists():
        print(f"Summaries directory not found: {SUMMARIES_ROOT}", file=sys.stderr)
        return 1

    existing_rows, existing_by_key, highest_id = load_existing_index(INDEX_CSV_PATH)

    all_flags: List[RedFlag] = []
    file_count = 0
    current_index = highest_id

    for md_file in iter_markdown_files(SUMMARIES_ROOT):
        flags, current_index = parse_red_flags(md_file, existing_by_key, current_index)
        if flags:
            file_count += 1
            print(f"Scanning {md_file.relative_to(REPO_ROOT)}... found {len(flags)} red flags")
            annotate_file(md_file, flags)
            all_flags.extend(flags)

    merge_and_write_csv(existing_rows, all_flags, INDEX_CSV_PATH)
    print(f"Total red flags indexed: {len(all_flags)} across {file_count} files")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
