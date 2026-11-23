import pytest

from src.smith_utils import text
from src.smith_utils.text.kanji_variants import (
    _load_replacements,
    normalize_kanji_variants,
)


def test_export_from_text_package():
    assert text.normalize_kanji_variants is normalize_kanji_variants
    assert "normalize_kanji_variants" in text.__all__


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("髙橋", "高橋"),
        ("\U0002CF1C", "色"),
        ("\u3530", "恒"),
        ("\u3530\U000E0100", "恒"),
        ("\u3530\U000E0101", "恆"),
        ("辺\U000E0101", "辺"),
        ("神\uFE00", "神"),
        ("\u3A3E\U000E0101", "樣"),
        ("  Ａ髙🙂\uFE0F\t\n國﨑舊", "  Ａ高🙂\uFE0F\t\n國﨑舊"),
    ],
)
def test_normalize_approved_mappings(source, expected):
    assert normalize_kanji_variants(source) == expected
    assert normalize_kanji_variants(expected) == expected


@pytest.mark.parametrize(
    "source",
    [
        "",
        "㐁＿",
        "\u3404\U000E0101",
        "\u3A3E",
        "\u3A3E\U000E0100",
        "髙\U000E01EF",
        "\u3530\U000E0100\U000E0101",
        "\u3530\uFE0F",
        "髙\u180B",
        "\U000E0101",
        "Hello\r\nこんにちは 🙂",
    ],
)
def test_preserve_text_without_an_approved_mapping(source):
    assert normalize_kanji_variants(source) == source


@pytest.mark.parametrize("value", [None, 1, b"text"])
def test_non_string_input_raises_type_error(value):
    with pytest.raises(TypeError, match="text must be a str"):
        normalize_kanji_variants(value)


def test_all_bundled_mappings_are_applied_and_idempotent():
    replacements = _load_replacements()
    assert len(replacements) == 21_623
    for source, target in replacements.items():
        assert normalize_kanji_variants(source) == target
        assert normalize_kanji_variants(target) == target
