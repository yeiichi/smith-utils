# tests/test_refinement.py

import pytest
from src.smith_utils.numeric.refinement import parse_numeric_value


def test_clean_numeric_valid_input():
    assert parse_numeric_value("1,234.56") == 1234.56
    assert parse_numeric_value("1234.56") == 1234.56
    assert parse_numeric_value("1 234.56", sep=" ") == 1234.56


def test_clean_numeric_invalid_input_raises_error():
    with pytest.raises(ValueError):
        parse_numeric_value("invalid")
    with pytest.raises(ValueError):
        parse_numeric_value("1234,56.78")


def test_clean_numeric_relaxed_mode_invalid_input():
    assert parse_numeric_value("invalid", relaxed=True) == "invalid"
    assert parse_numeric_value("1234,56.78", relaxed=True) == "1234,56.78"


def test_clean_numeric_none_value():
    assert parse_numeric_value(None) == 0.0


def test_clean_numeric_with_custom_separators():
    assert parse_numeric_value("1.234,56", sep=".", decimal=",") == 1234.56
    assert parse_numeric_value("1 234,56", sep=" ", decimal=",") == 1234.56


def test_clean_numeric_negative_number():
    assert parse_numeric_value("-1234.56") == -1234.56
    assert parse_numeric_value("(1234.56)") == -1234.56
    assert parse_numeric_value("(1,234.56)") == -1234.56
