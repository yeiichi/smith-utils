import datetime

import pytest

from src.smith_utils.datetime.date_utils import format_ordinal, parse_strict_date


def test_format_ordinal_single_digits():
    assert format_ordinal(1) == "1st"
    assert format_ordinal(2) == "2nd"
    assert format_ordinal(3) == "3rd"
    assert format_ordinal(4) == "4th"
    assert format_ordinal(9) == "9th"


def test_format_ordinal_double_digits():
    assert format_ordinal(11) == "11th"
    assert format_ordinal(12) == "12th"
    assert format_ordinal(13) == "13th"
    assert format_ordinal(21) == "21st"
    assert format_ordinal(22) == "22nd"


def test_format_ordinal_large_numbers():
    assert format_ordinal(100) == "100th"
    assert format_ordinal(111) == "111th"
    assert format_ordinal(112) == "112th"
    assert format_ordinal(113) == "113th"
    assert format_ordinal(121) == "121st"


def test_format_ordinal_negative_numbers():
    assert format_ordinal(-1) == "-1st"
    assert format_ordinal(-2) == "-2nd"
    assert format_ordinal(-3) == "-3rd"
    assert format_ordinal(-11) == "-11th"
    assert format_ordinal(-22) == "-22nd"


def test_format_ordinal_edge_cases():
    assert format_ordinal(0) == "0th"
    assert format_ordinal(1000) == "1000th"


def test_parse_strict_date_basic_format():
    assert parse_strict_date("20260413") == datetime.date(2026, 4, 13)
    assert parse_strict_date("19991231") == datetime.date(1999, 12, 31)


def test_parse_strict_date_extended_format():
    assert parse_strict_date("2026-04-13") == datetime.date(2026, 4, 13)
    assert parse_strict_date("1999-12-31") == datetime.date(1999, 12, 31)


def test_parse_strict_date_invalid_formats():
    with pytest.raises(ValueError, match="Could not parse '13-04-2026'. Expected YYYY-MM-DD or YYYYMMDD."):
        parse_strict_date("13-04-2026")

    with pytest.raises(ValueError, match="Could not parse '2026/04/13'. Expected YYYY-MM-DD or YYYYMMDD."):
        parse_strict_date("2026/04/13")


def test_parse_strict_date_ambiguous_inputs():
    with pytest.raises(ValueError, match=r"Ambiguous date '2026413' rejected\. .*"):
        parse_strict_date("2026413")

    with pytest.raises(ValueError, match="Ambiguous date '06-13' rejected. .*"):
        parse_strict_date("06-13")