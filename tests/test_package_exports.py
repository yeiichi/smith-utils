from src import smith_utils


def test_exports_are_available_globally():
    expected = {
        "get_file_digest",
        "get_text_digest",
        "NewlineType",
        "normalize_file_to_lf",
        "normalize_newlines_stream",
        "StringDistance",
        "analyze_pair",
        "Result",
        "Relation",
        "normalize_text",
        "UnicodeCharNameRecord",
        "make_unicode_char_name_records",
    }

    for name in expected:
        assert hasattr(smith_utils, name), f"missing export: {name}"
        assert name in smith_utils.__all__
