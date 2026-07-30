"""Utilities for generating random strings."""

import secrets
import string
from typing import Literal

CharCategory = Literal["ascii", "kanji", "mix"]

ASCII_CHARS = string.ascii_letters + string.digits
KANJI_CHARS = "".join(chr(i) for i in range(0x4E00, 0xA000))

CHARSETS = {
    "ascii": ASCII_CHARS,
    "kanji": KANJI_CHARS,
}


def _validate_length(length: int) -> None:
    if length < 0:
        raise ValueError("length must be greater than or equal to 0")


def _validate_ascii_ratio(ascii_ratio: float) -> None:
    if not 0 <= ascii_ratio <= 1:
        raise ValueError("ascii_ratio must be between 0 and 1")


def random_mixed_char(*, ascii_ratio: float = 0.5) -> str:
    """Return one random ASCII or kanji character based on ``ascii_ratio``."""

    _validate_ascii_ratio(ascii_ratio)
    charset = ASCII_CHARS if secrets.randbelow(10_000) < ascii_ratio * 10_000 else KANJI_CHARS
    return secrets.choice(charset)


def random_string(
    length: int,
    *,
    char_category: CharCategory = "ascii",
    ascii_ratio: float = 0.5,
) -> str:
    """Generate a random string of the given length and category."""

    _validate_length(length)
    if char_category == "mix":
        return "".join(random_mixed_char(ascii_ratio=ascii_ratio) for _ in range(length))

    try:
        population = CHARSETS[char_category]
    except KeyError:
        allowed = ", ".join(repr(key) for key in (*CHARSETS, "mix"))
        raise ValueError(f"char_category must be one of: {allowed}") from None

    return "".join(secrets.choice(population) for _ in range(length))
