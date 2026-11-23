"""Generate the bundled Unicode replacements from the pinned MJ source files."""

import argparse
import json
import re
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


MJSU_SHA256 = "beff70c8d07cd5701af5a64c88acc862982ba4521c6384e8a1694326704022c7"
MJ_LIST_SHA256 = "f79075bf006b66c5e57a6df60503c5a01679cabbcea2f124eb3758593cf6fd3f"
OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "src/smith_utils/text/_data/mjsu-1.2.0.tsv"
)
SPREADSHEET_NS = "{http://purl.oclc.org/ooxml/spreadsheetml/main}"
HEADERS = {
    "C": "MJ文字図形名",
    "E": "実装したUCS",
    "F": "実装したMoji_JohoコレクションIVS",
    "G": "実装したSVS",
}


def read_pinned(path: Path, checksum: str) -> bytes:
    data = path.read_bytes()
    if sha256(data).hexdigest() != checksum:
        raise ValueError(f"Unexpected SHA-256 for {path}")
    return data


def unicode_scalar(code: str) -> str:
    if not re.fullmatch(r"[0-9A-F]{4,6}", code):
        raise ValueError(f"Invalid hexadecimal code point {code!r}")
    value = int(code, 16)
    if 0xD800 <= value <= 0xDFFF:
        raise ValueError(f"Surrogate code point {code}")
    return chr(value)


def read_targets(data: bytes) -> dict[str, str | None]:
    targets = {}
    for row in json.loads(data)["content"]:
        glyph = row["MJ文字図形名"]
        target = row["変換先"]
        if glyph in targets:
            raise ValueError(f"Duplicate MJSU glyph {glyph}")
        if target["JIS X 0213"] == "1-01-18":
            if target["UCS"] != "U+FF3F":
                raise ValueError(f"Inconsistent no-target sentinel for {glyph}")
            targets[glyph] = None
        else:
            targets[glyph] = unicode_scalar(target["UCS"].removeprefix("U+"))
    return targets


def spreadsheet_elements(archive: ZipFile, member: str, tag: str):
    with archive.open(member) as stream:
        for _, element in ElementTree.iterparse(stream, events=("end",)):
            if element.tag == SPREADSHEET_NS + tag:
                yield element
                element.clear()


def read_glyph_inputs(data: bytes) -> dict[str, list[str]]:
    inputs = {}
    with ZipFile(BytesIO(data)) as archive:
        strings = [
            "".join(element.itertext())
            for element in spreadsheet_elements(archive, "xl/sharedStrings.xml", "si")
        ]
        rows = spreadsheet_elements(archive, "xl/worksheets/sheet1.xml", "row")
        for row in rows:
            values = {}
            for cell in row:
                column = cell.attrib["r"].rstrip("0123456789")
                value = cell.findtext(SPREADSHEET_NS + "v")
                if column in HEADERS and value is not None:
                    values[column] = strings[int(value)] if cell.get("t") == "s" else value
            if row.attrib["r"] == "1":
                if values != HEADERS:
                    raise ValueError("Unexpected MJ character list columns")
                continue
            glyph = values["C"]
            if glyph in inputs:
                raise ValueError(f"Duplicate character list glyph {glyph}")
            keys = []
            if "E" in values:
                keys.append(unicode_scalar(values["E"].removeprefix("U+")))
            for column, first, last in (
                ("F", 0xE0100, 0xE01EF),
                ("G", 0xFE00, 0xFE0F),
            ):
                if column in values:
                    for sequence in values[column].split(";"):
                        base, selector = sequence.strip().split("_")
                        selector = unicode_scalar(selector)
                        if not first <= ord(selector) <= last:
                            raise ValueError(f"Invalid variation selector for {glyph}")
                        keys.append(unicode_scalar(base) + selector)
            inputs[glyph] = keys
    return inputs


def make_replacements(
    glyph_inputs: dict[str, list[str]], targets: dict[str, str | None]
) -> dict[str, str]:
    if glyph_inputs.keys() != targets.keys():
        raise ValueError("The MJSU and character list glyph IDs must match")

    exact_targets = {}
    for glyph, keys in glyph_inputs.items():
        target = targets[glyph]
        for key in keys:
            if exact_targets.setdefault(key, target) != target:
                raise ValueError(f"Conflicting targets for {key!a}")

    replacements = {
        key: target
        for key, target in exact_targets.items()
        if target is not None and key != target
    }
    if replacements.keys() & replacements.values():
        raise ValueError("Every target must be a fixed point")
    return replacements


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mjsu_json", type=Path)
    parser.add_argument("mj_list_xlsx", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    targets = read_targets(read_pinned(args.mjsu_json, MJSU_SHA256))
    glyph_inputs = read_glyph_inputs(read_pinned(args.mj_list_xlsx, MJ_LIST_SHA256))
    replacements = make_replacements(glyph_inputs, targets)
    with args.output.open("w", encoding="ascii", newline="\n") as output:
        for source, target in sorted(replacements.items()):
            codepoints = " ".join(f"{ord(char):04X}" for char in source)
            output.write(f"{codepoints}\t{ord(target):04X}\n")


if __name__ == "__main__":
    main()
