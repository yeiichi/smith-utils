"""Unicode character name utilities."""

import unicodedata
from typing import NamedTuple


class UnicodeCharNameRecord(NamedTuple):
    index: int
    codepoint: str
    char: str
    name: str


def make_unicode_char_name_records(text: str) -> list[UnicodeCharNameRecord]:
    return [
        UnicodeCharNameRecord(
            index=i,
            codepoint=f"U+{ord(char):04X}",
            char=char,
            name=unicodedata.name(char, "<no name>"),
        )
        for i, char in enumerate(text)
    ]
