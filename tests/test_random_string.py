import string

import pytest

from src.smith_utils import random_mixed_char, random_string
from src.smith_utils.text import CharCategory
from src.smith_utils.text.random_string import ASCII_CHARS, KANJI_CHARS


def test_random_string_generates_ascii_string_of_requested_length():
    result = random_string(32)

    assert len(result) == 32
    assert set(result) <= set(string.ascii_letters + string.digits)


def test_random_string_generates_kanji_string_of_requested_length():
    result = random_string(16, char_category="kanji")

    assert len(result) == 16
    assert set(result) <= set(KANJI_CHARS)


def test_random_string_generates_mixed_string_of_requested_length():
    result = random_string(20, char_category="mix")

    assert len(result) == 20
    assert set(result) <= set(ASCII_CHARS + KANJI_CHARS)


def test_random_string_accepts_zero_length():
    assert random_string(0) == ""


def test_random_string_rejects_negative_length():
    with pytest.raises(ValueError, match="length"):
        random_string(-1)


def test_random_string_rejects_unknown_char_category():
    with pytest.raises(ValueError, match="char_category"):
        random_string(8, char_category="emoji")


@pytest.mark.parametrize("ascii_ratio", [-0.1, 1.1])
def test_random_mixed_char_rejects_ascii_ratio_outside_unit_interval(ascii_ratio):
    with pytest.raises(ValueError, match="ascii_ratio"):
        random_mixed_char(ascii_ratio=ascii_ratio)


def test_random_mixed_char_can_force_ascii():
    result = random_mixed_char(ascii_ratio=1)

    assert result in ASCII_CHARS


def test_random_mixed_char_can_force_kanji():
    result = random_mixed_char(ascii_ratio=0)

    assert result in KANJI_CHARS


def test_char_category_type_alias_is_exported():
    assert CharCategory is not None
