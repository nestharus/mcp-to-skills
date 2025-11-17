from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from . import extract_red_flags, generate_batch_prompts, generate_rollups, update_classifications

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CSV_PATH = REPO_ROOT / "working" / "phase2" / "issues_index.csv"


def cmd_scan(_: argparse.Namespace) -> int:
    """Scan summaries and incrementally update the issues index.

    This command is safe to run repeatedly; it reuses existing ISS IDs
    where possible, annotates red-flag bullets in place, and appends
    new issues without renumbering or dropping existing rows.
    """

    return extract_red_flags.main()


def cmd_batch(args: argparse.Namespace) -> int:
    return generate_batch_prompts.main(
        [
            f"--csv-path={args.csv_path}",
            f"--batch-size={args.batch_size}",
            f"--output-dir={args.output_dir}",
        ],
    )


def cmd_update(args: argparse.Namespace) -> int:
    cli_args = [f"--csv-path={args.csv_path}"]
    if args.results_file:
        cli_args.append(f"--results-file={args.results_file}")
    if args.results_dir:
        cli_args.append(f"--results-dir={args.results_dir}")
    return update_classifications.main(cli_args)


def cmd_rollup(args: argparse.Namespace) -> int:
    return generate_rollups.main([f"--csv-path={args.csv_path}"])


def cmd_sql(args: argparse.Namespace) -> int:
    import duckdb

    if args.query:
        conn = duckdb.connect(":memory:")
        conn.execute(
            "CREATE TABLE issues AS SELECT * FROM read_csv_auto(?, header=True)",
            [str(args.csv_path)],
        )
        for row in conn.execute(args.query).fetchall():
            print(row)
        return 0

    conn = duckdb.connect(":memory:")
    conn.execute(
        "CREATE TABLE issues AS SELECT * FROM read_csv_auto(?, header=True)",
        [str(args.csv_path)],
    )
    print("Loaded issues table. Enter SQL or type 'exit' to quit.")
    while True:
        try:
            query = input("duckdb> ").strip()
        except (EOFError, KeyboardInterrupt):  # pragma: no cover - interactive
            print()
            break
        if query.lower() in {"exit", "quit"}:
            break
        if not query:
            continue
        try:
            for row in conn.execute(query).fetchall():
                print(row)
        except Exception as exc:  # pragma: no cover - interactive
            print(f"Error: {exc}")

    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    import duckdb

    conn = duckdb.connect(":memory:")
    conn.execute(
        "CREATE TABLE issues AS SELECT * FROM read_csv_auto(?, header=True)",
        [str(args.csv_path)],
    )

    total = conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
    print(f"Total issues: {total}")

    print("By classification:")
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
    return 0


def cmd_classify(_: argparse.Namespace) -> int:
    print("Rule-based classifier is disabled; use Droid batches instead.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Triage manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan summaries and rebuild index")
    scan.set_defaults(func=cmd_scan)

    batch = subparsers.add_parser("batch", help="Generate batch prompt files")
    batch.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    batch.add_argument("--batch-size", type=int, default=10)
    batch.add_argument(
        "--output-dir", type=Path, default=REPO_ROOT / "working" / "phase2" / "batches"
    )
    batch.set_defaults(func=cmd_batch)

    update = subparsers.add_parser("update", help="Apply classification results to index")
    update.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    update.add_argument("--results-file", type=Path)
    update.add_argument("--results-dir", type=Path)
    update.set_defaults(func=cmd_update)

    rollup = subparsers.add_parser("rollup", help="Generate backlog and summary documents")
    rollup.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    rollup.set_defaults(func=cmd_rollup)

    sql = subparsers.add_parser("sql", help="Run SQL queries against the issues index")
    sql.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    sql.add_argument("--query")
    sql.set_defaults(func=cmd_sql)

    validate = subparsers.add_parser("validate", help="Run integrity checks against the index")
    validate.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    validate.set_defaults(func=cmd_validate)

    classify = subparsers.add_parser(
        "classify",
        help="(disabled) classification is sourced from Droid batch results",
    )
    classify.set_defaults(func=cmd_classify)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    func = getattr(args, "func")
    return func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
