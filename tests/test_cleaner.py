import pytest

from smith_utils.com_name_cleaner import normalize_name, parse_name, split_name


@pytest.mark.parametrize("form", (
    "有限会社", "合名会社", "合資会社", "相互会社", "財団法人", "社団法人",
    "医療法人", "医療法人社団", "医療法人財団", "社会医療法人", "宗教法人",
    "学校法人", "社会福祉法人", "一般社団法人", "公益社団法人", "一般財団法人", "公益財団法人",
))
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


@pytest.mark.parametrize(("raw", "expected"), [
    ("株式会社三菱総合研究所", "株式会社三菱総合研究所"),
    ("（株）三菱総合研究所", "株式会社三菱総合研究所"),
    ("㈱三菱総合研究所", "株式会社三菱総合研究所"),
    ("一般社団法人日本養鶏協会", "一般社団法人日本養鶏協会"),
    ("（一社）日本養鶏協会", "一般社団法人日本養鶏協会"),
    ("丸紅株式会社", "丸紅株式会社"),
    ("丸紅㈱", "丸紅株式会社"),
    ("丸紅(株)", "丸紅株式会社"),
    ("　（ 株 ） \t三菱総合研究所　", "株式会社三菱総合研究所"),
    ("丸紅　 株 式 会 社", "丸紅株式会社"),
    ("(株) ACME　 Japan", "株式会社ACME Japan"),
    ("㈲ ＡＢＣ ｶﾀｶﾅ", "有限会社ABC カタカナ"),
])
def test_normalize_name(raw, expected):
    assert normalize_name(raw) == expected


def test_remove_all_spaces():
    assert normalize_name("(株) ACME　 Japan", remove_all_spaces=True) == "株式会社ACMEJapan"


def test_abbreviated_suffix():
    result = parse_name("丸紅(株)")
    assert result.original == "丸紅(株)"
    assert (result.name, result.legal_form, result.position, result.status) == (
        "丸紅", "株式会社", "suffix", "parsed",
    )


@pytest.mark.parametrize("text", ["(社)日本協会", "株の会社", "研究所(株)東京支店", "ABC・Japan", "NPO法人テスト"])
def test_unrecognized(text):
    assert normalize_name(text) == text
    assert parse_name(text).status == "unrecognized"


@pytest.mark.parametrize("text", [
    "株式会社ABC(株)", "(株)(有)ABC", "株式会社", "(株)", "医療法人社団テスト社団法人",
    "社団法人財団法人テスト", "社会医療法人", "医療法人社団", "社団法人",
])
def test_ambiguous(text):
    result = parse_name(text)
    assert result.status == "ambiguous"
    assert result.legal_form is None
    assert result.normalized == text


def test_empty():
    assert parse_name("　\t").status == "empty"


@pytest.mark.parametrize("value", [None, 123, float("nan")])
def test_invalid_type(value):
    with pytest.raises(TypeError):
        normalize_name(value)


@pytest.mark.parametrize("text", ["（株） A　B", "丸紅㈱", "(社)日本協会", "(株)(有)ABC", ""])
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
    ("川崎車両　(株)", (None, "川崎車両", "株式会社")),
    ("（一社）日本養鶏協会", ("一般社団法人", "日本養鶏協会", None)),
    ("テスト", (None, "テスト", None)),
    ("(株)テスト(有)", (None, "(株)テスト(有)", None)),
    ("　", (None, "", None)),
])
def test_split_name(raw, expected):
    assert split_name(raw) == expected
