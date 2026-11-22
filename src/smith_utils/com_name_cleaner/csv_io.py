"""Append normalized organization-name fields to a CSV file."""

import csv
from pathlib import Path
from tempfile import NamedTemporaryFile

from . import parse_name


def clean_csv(source: Path, column: str, destination: Path, *,
              encoding: str = "utf-8-sig", remove_all_spaces: bool = False) -> None:
    """Copy a CSV and append the organization-name parsing results.

    The added columns are ``normalized_name``, ``prefix``, ``stem``,
    ``suffix``, and ``parse_status``. Absent forms become empty cells.
    The output is UTF-8 with a byte order mark (BOM). An existing destination
    is replaced only after the input has been read and the output written.

    Args:
        source: Path to a comma-separated file with a header row.
        column: Exact header of the organization-name column.
        destination: Path to a separate output file.
        encoding: Input encoding. The default accepts UTF-8 with or without a BOM.
        remove_all_spaces: Remove all whitespace from names before parsing.

    Raises:
        ValueError: If the paths refer to the same file, the selected column
            is missing or occurs more than once, a result column already
            exists, or a record has the wrong number of fields.
        csv.Error: If the input contains malformed CSV.
        OSError: If a file cannot be read or written.
    """
    if source.resolve() == destination.resolve() or (
        destination.exists() and source.samefile(destination)
    ):
        raise ValueError("Choose an output file different from the input file.")
    fields = ["normalized_name", "prefix", "stem", "suffix", "parse_status"]
    temporary = None
    try:
        with source.open(encoding=encoding, newline="") as src:
            reader = csv.reader(src, strict=True)
            header = next(reader, [])
            if header.count(column) != 1:
                raise ValueError(f"Expected one column named {column!r}. Headers: {header!r}")
            collisions = [field for field in fields if field in header]
            if collisions:
                raise ValueError(f"Result columns already present: {', '.join(collisions)}")
            index = header.index(column)
            with NamedTemporaryFile(mode="w", dir=destination.parent, encoding="utf-8-sig",
                                    newline="", delete=False) as out:
                temporary = Path(out.name)
                writer = csv.writer(out)
                writer.writerow(header + fields)
                for row in reader:
                    if not row:  # Ignore blank physical records, like csv.DictReader.
                        continue
                    if len(row) != len(header):
                        raise ValueError(f"Wrong number of fields in record ending at line {reader.line_num}.")
                    result = parse_name(row[index], remove_all_spaces=remove_all_spaces)
                    writer.writerow([*row, result.normalized, *result.parts, result.status])
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
