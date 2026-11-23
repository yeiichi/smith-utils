"""Normalize Japanese glyph variants using the MJ single-choice reduction table."""

import re
from functools import cache
from importlib.resources import files


_VARIATION_SELECTORS = (
    "\u180b-\u180d\u180f\ufe00-\ufe0f\U000e0100-\U000e01ef"
)
_TEXT_UNITS = re.compile(
    rf"[^{_VARIATION_SELECTORS}][{_VARIATION_SELECTORS}]*|[{_VARIATION_SELECTORS}]+"
)


@cache
def _load_replacements() -> dict[str, str]:
    resource = files(__package__) / "_data" / "mjsu-1.2.0.tsv"
    replacements = {}
    with resource.open(encoding="ascii") as table:
        for row in table:
            source, target = row.split("\t")
            key = "".join(chr(int(code, 16)) for code in source.split())
            replacements[key] = chr(int(target, 16))
    return replacements


def normalize_kanji_variants(text: str) -> str:
    """Replace Japanese glyph variants with their selected MJSU 1.2.0 targets.

    Bare characters use their default MJ glyph. A character with an attached
    variation selector is replaced only when the exact sequence has a usable
    target. Other text is preserved verbatim.

    The conversion is idempotent and can merge distinct glyphs into the same
    character.

    :raises TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not text:
        return text

    replacements = _load_replacements()
    normalized = []
    for match in _TEXT_UNITS.finditer(text):
        unit = match[0]
        normalized.append(replacements.get(unit, unit))
    return "".join(normalized)
