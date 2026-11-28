import pytest

from smith_utils.com_name_cleaner import LEGAL_FORMS, normalize_name, parse_name, split_name


@pytest.mark.parametrize("form", LEGAL_FORMS)
@pytest.mark.parametrize("position", ["prefix", "suffix"])
@pytest.mark.parametrize("separator", ["", "　"], ids=["compact", "spaced"])
def test_parse_full_form(form, position, separator):
    designation = separator.join(form)
    if position == "prefix":
        raw = designation + "　テスト"
        expected = form + "テスト"
    else:
        raw = "テスト　" + designation
        expected = "テスト" + form
    result = parse_name(raw)
    assert result.original == raw
    assert result.legal_form == form
    assert result.position == position
    assert result.name == "テスト"
    assert result.status == "parsed"
    assert result.normalized == expected
    assert normalize_name(expected) == expected


@pytest.mark.parametrize(("form", "alias"), [
    (form, alias)
    for form, aliases in LEGAL_FORMS.items()
    for alias in aliases
    if alias != "(特)"
])
def test_parse_alias_at_either_edge(form, alias):
    assert split_name(f"{alias}例示用組織") == (form, "例示用組織", None)
    assert split_name(f"例示用組織{alias}") == (None, "例示用組織", form)


@pytest.mark.parametrize(("raw", "expected"), [
    ("株式会社例示用総合研究所", "株式会社例示用総合研究所"),
    ("（株）例示用総合研究所", "株式会社例示用総合研究所"),
    ("㈱例示用総合研究所", "株式会社例示用総合研究所"),
    ("一般社団法人例示用協会", "一般社団法人例示用協会"),
    ("（一社）例示用協会", "一般社団法人例示用協会"),
    ("（社）例示用協会", "社団法人例示用協会"),
    ("例示用基金（財）", "例示用基金財団法人"),
    ("（ＮＰＯ）例示用団体", "特定非営利活動法人例示用団体"),
    ("例示用商事株式会社", "例示用商事株式会社"),
    ("例示用商事㈱", "例示用商事株式会社"),
    ("例示用商事(株)", "例示用商事株式会社"),
    ("　（ 株 ） \t例示用総合研究所　", "株式会社例示用総合研究所"),
    ("例示用商事　 株 式 会 社", "例示用商事株式会社"),
    ("(株) DEMO　 Works", "株式会社ＤＥＭＯ　Ｗｏｒｋｓ"),
    ("㈲ ＡＢＣ ｶﾀｶﾅ", "有限会社ＡＢＣ　カタカナ"),
    ("Demo 123", "Ｄｅｍｏ　１２３"),
    ("（株）Demo 　123! ｶﾀｶﾅ", "株式会社Ｄｅｍｏ　１２３！　カタカナ"),
])
def test_normalize_name(raw, expected):
    assert normalize_name(raw) == expected


@pytest.mark.parametrize(("full_width", "expected", "without_spaces"), [
    (True, "株式会社Ｄｅｍｏ　１２３！　カタカナ", "株式会社Ｄｅｍｏ１２３！カタカナ"),
    (False, "株式会社Demo 123! カタカナ", "株式会社Demo123!カタカナ"),
])
def test_normalize_name_width(full_width, expected, without_spaces):
    raw = "（株）Ｄeｍo　１２３！ ｶﾀｶﾅ"
    assert normalize_name(raw, full_width=full_width) == expected
    assert normalize_name(expected, full_width=full_width) == expected
    assert normalize_name(raw, full_width=full_width, remove_all_spaces=True) == without_spaces


def test_abbreviated_suffix():
    result = parse_name("例示用商事(株)")
    assert result.original == "例示用商事(株)"
    assert (result.name, result.legal_form, result.position, result.status) == (
        "例示用商事", "株式会社", "suffix", "parsed",
    )


@pytest.mark.parametrize("text", ["株の会社", "研究所(株)東京支店", "Demo・Works", "NPO法人テスト"])
def test_unrecognized(text):
    assert normalize_name(text, full_width=False) == text
    assert parse_name(text).status == "unrecognized"


@pytest.mark.parametrize("text", [
    "株式会社ABC(株)", "(株)(有)ABC", "株式会社", "(株)", "医療法人社団テスト社団法人",
    "社団法人財団法人テスト", "社会医療法人", "医療法人社団", "社団法人",
    "(特)例示用事務所", "例示用事務所(特)",
])
def test_ambiguous(text):
    result = parse_name(text)
    assert result.status == "ambiguous"
    assert result.legal_form is None
    assert result.normalized == text


def test_full_width_shared_alias():
    result = parse_name("（ 特 ）　例示用事務所")
    assert result.status == "ambiguous"
    assert result.parts == (None, "( 特 ) 例示用事務所", None)


def test_empty():
    assert parse_name("　\t").status == "empty"


@pytest.mark.parametrize("value", [None, 123, float("nan")])
def test_invalid_type(value):
    with pytest.raises(TypeError):
        normalize_name(value)


@pytest.mark.parametrize("text", ["（株） A　B", "例示用商事㈱", "(社)例示用協会", "(株)(有)ABC", ""])
def test_idempotence(text):
    result = parse_name(text)
    reparsed = parse_name(result.normalized)
    assert reparsed.normalized == result.normalized
    assert reparsed.parts == result.parts
    assert reparsed.status == result.status


@pytest.mark.parametrize(("raw", "normalized"), [
    ("（医）　社団テスト", "(医) 社団テスト"),
    ("(医)財団", "(医)財団"),
    ("テスト社会(医)", "テスト社会(医)"),
])
def test_expansion_that_changes_parts_is_ambiguous(raw, normalized):
    result = parse_name(raw)
    assert result.normalized == normalized
    assert result.parts == (None, normalized, None)
    assert result.status == "ambiguous"
    assert parse_name(normalized).parts == result.parts
    assert parse_name(normalized).status == result.status


@pytest.mark.parametrize(("raw", "expected"), [
    ("例示用車両　(株)", (None, "例示用車両", "株式会社")),
    ("（一社）例示用協会", ("一般社団法人", "例示用協会", None)),
    ("テスト", (None, "テスト", None)),
    ("(株)テスト(有)", (None, "（株）テスト（有）", None)),
    ("　", (None, "", None)),
])
def test_split_name(raw, expected):
    assert split_name(raw) == expected


@pytest.mark.parametrize(("full_width", "expected", "without_spaces"), [
    (True, "Ｄｅｍｏ　１２３！　カタカナ", "Ｄｅｍｏ１２３！カタカナ"),
    (False, "Demo 123! カタカナ", "Demo123!カタカナ"),
])
def test_split_name_width(full_width, expected, without_spaces):
    raw = "（株）Ｄeｍo　１２３！ ｶﾀｶﾅ"
    assert split_name(raw, full_width=full_width) == ("株式会社", expected, None)
    assert split_name(raw, full_width=full_width, remove_all_spaces=True) == (
        "株式会社", without_spaces, None,
    )
