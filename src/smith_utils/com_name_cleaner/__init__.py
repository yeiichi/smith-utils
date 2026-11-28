"""Normalize Japanese organization names using rules for common legal forms."""

from collections import defaultdict
from dataclasses import dataclass
import re
from typing import Literal
import unicodedata

__all__ = ["ParsedName", "normalize_name", "parse_name", "split_name"]

LEGAL_FORMS: dict[str, tuple[str, ...]] = {
    # Companies and mutual companies
    "株式会社": ("(株)",),
    "有限会社": ("(有)",),
    "合同会社": ("(同)",),
    "合名会社": ("(名)",),
    "合資会社": ("(資)",),
    "相互会社": ("(相)",),

    # General, public-interest, and legacy associations and foundations
    "財団法人": ("(財)",),
    "社団法人": ("(社)",),
    "一般社団法人": ("(一社)",),
    "公益社団法人": ("(公社)",),
    "一般財団法人": ("(一財)",),
    "公益財団法人": ("(公財)",),

    # Nonprofit, welfare, education, medical, and religious organizations
    "特定非営利活動法人": ("(特非)", "(NPO)"),
    "認定特定非営利活動法人": ("(認特非)",),
    "社会福祉法人": ("(社福)", "(福)"),
    "学校法人": ("(学)",),
    "準学校法人": ("(準学)",),
    "医療法人": ("(医)",),
    "医療法人社団": ("(医社)",),
    "医療法人財団": ("(医財)",),
    "社会医療法人": ("(社医)",),
    "宗教法人": ("(宗)",),
    "更生保護法人": ("(更)",),

    # Professional corporations
    "弁護士法人": ("(弁)",),
    "外国法事務弁護士法人": ("(外弁)",),
    "税理士法人": ("(税)",),
    "司法書士法人": ("(司)",),
    "行政書士法人": ("(行)",),
    "社会保険労務士法人": ("(社労)",),
    "弁理士法人": ("(特)",),
    "土地家屋調査士法人": ("(調)",),
    "監査法人": ("(監)",),
    "特許業務法人": ("(特)",),

    # Cooperatives, associations, and unions
    "事業協同組合": ("(協)",),
    "事業協同小組合": ("(小協)",),
    "協同組合連合会": ("(協連)",),
    "企業組合": ("(企)",),
    "協業組合": ("(業)",),
    "信用協同組合": ("(信組)",),
    "信用金庫": ("(信金)",),
    "信用金庫連合会": ("(信金連)",),
    "労働金庫": ("(労金)",),
    "労働金庫連合会": ("(労金連)",),
    "農業協同組合": ("(農協)",),
    "農業協同組合連合会": ("(農協連)",),
    "漁業協同組合": ("(漁協)",),
    "漁業協同組合連合会": ("(漁協連)",),
    "水産加工業協同組合": ("(水協)",),
    "森林組合": ("(森組)",),
    "森林組合連合会": ("(森連)",),
    "消費生活協同組合": ("(生協)",),
    "消費生活協同組合連合会": ("(生協連)",),
    "商工組合": ("(商工)",),
    "商工組合連合会": ("(商工連)",),
    "商店街振興組合": ("(振)",),
    "商店街振興組合連合会": ("(振連)",),
    "生活衛生同業組合": ("(生衛)",),
    "生活衛生同業組合連合会": ("(生衛連)",),
    "酒造組合": ("(酒造)",),
    "酒販組合": ("(酒販)",),
    "内航海運組合": ("(海運)",),
    "管理組合法人": ("(管)",),
    "労働組合": ("(労組)",),
    "健康保険組合": ("(健保)",),
    "国民健康保険組合": ("(国保)",),
    "共済組合": ("(共済)",),
    "農事組合法人": ("(農)",),

    # Financial, investment, public, and special corporations
    "投資法人": ("(投)",),
    "特定目的会社": ("(特目)",),
    "独立行政法人": ("(独)",),
    "地方独立行政法人": ("(地独)",),
    "国立大学法人": ("(国大)",),
    "公立大学法人": ("(公大)",),
    "特殊法人": (),
    "認可法人": (),
    "商工会議所": ("(商議)",),
    "商工会": ("(商工会)",),
    "職業訓練法人": ("(職訓)",),
}


def _compile_patterns() -> tuple[tuple[re.Pattern[str], re.Pattern[str], tuple[str, ...]], ...]:
    forms_by_token: dict[str, list[str]] = defaultdict(list)
    for form, aliases in LEGAL_FORMS.items():
        for token in (form, *aliases):
            forms_by_token[token].append(form)

    patterns = []
    for token, forms in forms_by_token.items():
        # Accept spaces inside a designation, including '( 株 )' and '株 式 会 社'.
        pattern = r"\s*".join(re.escape(char) for char in token)
        patterns.append((re.compile(pattern), re.compile(pattern + r"\Z"), tuple(forms)))
    return tuple(patterns)


_PATTERNS = _compile_patterns()
_FULL_WIDTH_OFFSET = ord("！") - ord("!")
_ASCII_TO_FULL_WIDTH = {
    codepoint: chr(codepoint + _FULL_WIDTH_OFFSET)
    for codepoint in range(ord("!"), ord("~") + 1)
}
_ASCII_TO_FULL_WIDTH[ord(" ")] = "\u3000"


@dataclass(frozen=True)
class ParsedName:
    """An immutable result from :func:`parse_name`.

    ``original`` holds the input as supplied. ``normalized`` holds the display
    text after Unicode and whitespace normalization and any legal-form
    expansion. ``name`` holds the extracted stem or the whole normalized
    text when no form was extracted. ``legal_form`` holds the canonical
    designation and ``position`` is ``"prefix"`` or ``"suffix"``. Both are
    ``None`` when no form was extracted.

    Possible ``status`` values are

    - ``"parsed"`` when a single form and a stem were extracted.
    - ``"unrecognized"`` when no supported form matched either edge.
    - ``"ambiguous"`` when the split was unclear.
    - ``"empty"`` when normalization left no text.
    """

    original: str
    normalized: str
    name: str
    legal_form: str | None
    position: Literal["prefix", "suffix"] | None
    status: Literal["parsed", "unrecognized", "ambiguous", "empty"]

    @property
    def parts(self) -> tuple[str | None, str, str | None]:
        """Return ``(prefix, stem, suffix)`` with ``None`` for absent forms."""
        prefix = self.legal_form if self.position == "prefix" else None
        suffix = self.legal_form if self.position == "suffix" else None
        return prefix, self.name, suffix


def _edge_matches(text: str) -> list[tuple[str, str, str]]:
    # Keep the longest match at each edge. For example, 医療法人社団
    # contains the shorter prefix 医療法人. Keep all forms for a shared alias.
    best: dict[str, tuple[int, tuple[str, ...], str]] = {}
    for prefix, suffix, forms in _PATTERNS:
        match = prefix.match(text)
        if match and ("prefix" not in best or match.end() > best["prefix"][0]):
            best["prefix"] = (match.end(), forms, text[match.end():].strip())
        match = suffix.search(text)
        if match:
            length = len(text) - match.start()
            if "suffix" not in best or length > best["suffix"][0]:
                best["suffix"] = (length, forms, text[:match.start()].strip())
    return [(form, position, name) for position, (_, forms, name) in best.items() for form in forms]


def parse_name(value: str, *, remove_all_spaces: bool = False) -> ParsedName:
    """Normalize a Japanese organization name and identify its legal form.

    Apply Unicode NFKC and trim and collapse whitespace. A supported legal
    form or abbreviation at either end is replaced with its canonical form
    in the same position, with no separator between the form and the stem.

    Ambiguous cases include competing forms, shared abbreviations, a form
    without a stem, and expansions that would change the extracted parts
    on a second pass.
    These cases keep the Unicode- and whitespace-normalized input as both
    the display text and the stem.

    Args:
        value: Organization name to normalize.
        remove_all_spaces: Remove all Unicode whitespace before parsing.
            By default, whitespace within the stem is collapsed to single spaces.

    Returns:
        The display text, extracted parts, and parsing status.

    Raises:
        TypeError: If ``value`` is not a string.
    """
    if not isinstance(value, str):
        raise TypeError("organization name must be a str")
    text = unicodedata.normalize("NFKC", value)
    text = "".join(text.split()) if remove_all_spaces else " ".join(text.split())
    if not text:
        return ParsedName(value, "", "", None, None, "empty")
    matches = _edge_matches(text)
    if not matches:
        return ParsedName(value, text, text, None, None, "unrecognized")
    if len(matches) != 1:
        return ParsedName(value, text, text, None, None, "ambiguous")
    form, position, name = matches[0]
    if not name or _edge_matches(name):
        return ParsedName(value, text, text, None, None, "ambiguous")
    normalized = form + name if position == "prefix" else name + form
    if normalized != text and _edge_matches(normalized) != matches:
        return ParsedName(value, text, text, None, None, "ambiguous")
    return ParsedName(value, normalized, name, form, position, "parsed")


def normalize_name(
    value: str, *, remove_all_spaces: bool = False, full_width: bool = True
) -> str:
    """Return display text with full-width ASCII equivalents by default.

    The default widens ASCII letters, digits, punctuation, and spaces after
    parsing. Pass ``full_width=False`` for the display text from
    :func:`parse_name`. Both modes preserve ASCII letter case.
    The ``remove_all_spaces`` option follows the same whitespace rules as
    :func:`parse_name`.
    """
    text = parse_name(value, remove_all_spaces=remove_all_spaces).normalized
    return text.translate(_ASCII_TO_FULL_WIDTH) if full_width else text


def split_name(value: str, *, remove_all_spaces: bool = False) -> tuple[str | None, str, str | None]:
    """Return ``(prefix, stem, suffix)`` from :func:`parse_name`.

    Absent forms are ``None``. When no form is extracted, the stem is the
    normalized text. Pass ``remove_all_spaces=True`` to remove all whitespace
    before splitting.
    """
    return parse_name(value, remove_all_spaces=remove_all_spaces).parts
