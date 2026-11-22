"""Command-line interface for text and CSV organization-name cleaning."""

import argparse
import csv
from dataclasses import asdict
from functools import partial
import json
from pathlib import Path
import sys

from . import parse_name
from .csv_io import clean_csv


def main() -> None:
    """Run the command-line interface using arguments from ``sys.argv``."""
    parser = argparse.ArgumentParser(description="Normalize Japanese organization names.")
    configure_parser(parser)
    args = parser.parse_args()
    args.func(args)


def configure_parser(parser: argparse.ArgumentParser) -> None:
    """Register the shared organization-name arguments and command handler."""
    parser.add_argument("names", nargs="*", help="Names; otherwise read one per stdin line")
    parser.add_argument("--remove-all-spaces", action="store_true", help="Also remove internal word spaces")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--parts", action="store_true", help="Emit [prefix, stem, suffix] as JSON Lines")
    output.add_argument("--json", action="store_true", help="Emit JSON Lines with parsing status")
    parser.add_argument("--csv", metavar="INPUT", type=Path, help="Read names from a CSV file")
    parser.add_argument("--column", help="Exact CSV header containing organization names")
    parser.add_argument("--output", metavar="FILE", type=Path, help="Destination CSV (default: INPUT_cleaned.csv)")
    parser.add_argument("--encoding", help="Input CSV encoding (default: utf-8-sig)")
    parser.set_defaults(func=partial(_clean_names, parser))


def _clean_names(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.csv is not None:
        if args.column is None or args.names or args.parts or args.json:
            parser.error("--csv requires --column and accepts no positional names, --parts, or --json")
        destination = args.output or args.csv.with_name(args.csv.stem + "_cleaned.csv")
        try:
            clean_csv(args.csv, args.column, destination, encoding=args.encoding or "utf-8-sig",
                      remove_all_spaces=args.remove_all_spaces)
        except (OSError, ValueError, LookupError, csv.Error) as exc:
            parser.exit(1, f"{parser.prog}: {exc}\n")
        print(f"Wrote {destination}", file=sys.stderr)
        return
    if any(value is not None for value in (args.column, args.output, args.encoding)):
        parser.error("--column, --output, and --encoding require --csv")
    # Be explicit on Windows, where redirected streams can otherwise use a legacy code page.
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    names = args.names if args.names else (line.rstrip("\r\n") for line in sys.stdin)
    for name in names:
        result = parse_name(name, remove_all_spaces=args.remove_all_spaces)
        if args.parts:
            print(json.dumps(result.parts, ensure_ascii=False))
        elif args.json:
            print(json.dumps(asdict(result), ensure_ascii=False))
        else:
            print(result.normalized)
