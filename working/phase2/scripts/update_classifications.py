from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

import duckdb

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CSV_PATH = REPO_ROOT / "working" / "phase2" / "issues_index.csv"

VALID_CLASSIFICATIONS = {"RESOLVED", "CONFLICT", "RESEARCH", "UNCLASSIFIED"}


def load_results_from_file(path: Path) -> Dict[str, Dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    start = text.find("```json")
    if start != -1:
        start = text.find("{", start)
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start : end + 1]
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Results file must contain a JSON object: {path}")
    return {k: v for k, v in data.items() if isinstance(v, dict)}


def load_results(results_file: Path | None, results_dir: Path | None) -> Dict[str, Dict[str, str]]:
    merged: Dict[str, Dict[str, str]] = {}
    if results_file:
        merged.update(load_results_from_file(results_file))
    if results_dir and results_dir.is_dir():
        for path in sorted(results_dir.glob("*.json")):
            merged.update(load_results_from_file(path))
    return merged


def update_csv(csv_path: Path, results: Dict[str, Dict[str, str]]) -> None:
    rows: List[dict] = []
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            issue_id = row.get("id", "")
            if issue_id in results:
                data = results[issue_id]
                classification = data.get("classification", "").upper()
                if classification and classification not in VALID_CLASSIFICATIONS:
                    raise ValueError(
                        f"Invalid classification '{classification}' for {issue_id}",
                    )
                if classification:
                    row["classification"] = classification
                if "classification_ref" in data:
                    row["classification_ref"] = data["classification_ref"]
                if "notes" in data:
                    row["notes"] = data["notes"]
                # Optional: allow Droid to set issue_type directly if provided
                if "issue_type" in data and data["issue_type"]:
                    row["issue_type"] = data["issue_type"]
            rows.append(row)

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_duckdb_validations(csv_path: Path) -> None:
    conn = duckdb.connect(":memory:")
    conn.execute(
        "CREATE TABLE issues AS SELECT * FROM read_csv_auto(?, header=True)",
        [str(csv_path)],
    )

    print("Classification counts:")
    for classification, count in conn.execute(
        "SELECT classification, COUNT(*) FROM issues "
        "GROUP BY classification ORDER BY classification",
    ).fetchall():
        print(f"  {classification or '<EMPTY>'}: {count}")

    duplicates = conn.execute(
        "SELECT id, COUNT(*) FROM issues GROUP BY id HAVING COUNT(*) > 1",
    ).fetchall()
    if duplicates:
        print("Duplicate IDs detected:")
        for issue_id, count in duplicates:
            print(f"  {issue_id}: {count}")
    else:
        print("No duplicate IDs detected.")

    nulls = conn.execute(
        "SELECT COUNT(*) FROM issues WHERE classification IS NULL OR classification = ''",
    ).fetchone()[0]
    print(f"Rows with empty classification: {nulls}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Update issues_index.csv with classification results."
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--results-file", type=Path)
    parser.add_argument("--results-dir", type=Path)
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not args.csv_path.exists():
        raise SystemExit(f"CSV not found: {args.csv_path}")

    results = load_results(args.results_file, args.results_dir)
    if not results:
        print("No results found; nothing to update.")
        return 0

    print(f"Updating classifications for {len(results)} issues")
    update_csv(args.csv_path, results)
    run_duckdb_validations(args.csv_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
