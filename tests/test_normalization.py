from src.smith_utils.text.normalization import normalize_text


def test_normalize_none_input():
    assert normalize_text(None) == ""


def test_normalize_empty_string():
    assert normalize_text("") == ""


def test_normalize_whitespaces_only():
    assert normalize_text("   ") == ""


def test_normalize_lowercase_conversion():
    result = normalize_text("Hello World")
    assert result == "hello world"


def test_normalize_unicodedata_nfkc():
    result = normalize_text(u"① Ⅱ Ⅲ")
    assert result == "1 ii iii"


def test_normalize_remove_all_whitespace():
    result = normalize_text(" Hello   World ", ignore_case=False, remove_all_whitespace=True)
    assert result == "HelloWorld"


def test_normalize_trim_whitespace():
    result = normalize_text("   Hello World   ")
    assert result == "hello world"


def test_normalize_nfkc_and_case_fold():
    result = normalize_text(u"①ＡＢＣ def")
    assert result == "1abc def"


def test_normalize_case_sensitive_option():
    result = normalize_text("Hello World", ignore_case=False)
    assert result == "Hello World"
