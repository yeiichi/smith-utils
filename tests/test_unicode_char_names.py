from src.smith_utils.text.unicode_char_names import make_unicode_char_name_records


def test_make_unicode_char_name_records():
    records = make_unicode_char_name_records("Aあ")
    assert len(records) == 2
    assert records[0].index == 0
    assert records[0].codepoint == "U+0041"
    assert records[0].char == "A"
    assert records[0].name == "LATIN CAPITAL LETTER A"
    assert records[1].codepoint == "U+3042"
    assert records[1].name == "HIRAGANA LETTER A"


def test_make_unicode_char_name_records_no_name_character():
    records = make_unicode_char_name_records("\n")
    assert len(records) == 1
    assert records[0].codepoint == "U+000A"
    assert records[0].name == "<no name>"
