"""Normalize Japanese organization names using rules for common legal forms."""

from dataclasses import dataclass
import re
from typing import Literal
import unicodedata

__all__ = ["ParsedName", "normalize_name", "parse_name", "split_name"]

# Deliberately explicit: (社), (財), and bare 株 are ambiguous and not expanded.
LEGAL_FORMS: dict[str, tuple[str, ...]] = {
    "株式会社": ("(株)",),
    "有限会社": ("(有)",),
    "合同会社": ("(同)",),
    "合名会社": ("(名)",),
    "合資会社": ("(資)",),
    "相互会社": (),
    "財団法人": (),
    "社団法人": (),
    "一般社団法人": ("(一社)",),
    "公益社団法人": ("(公社)",),
    "一般財団法人": ("(一財)",),
    "公益財団法人": ("(公財)",),
    "社会福祉法人": ("(社福)",),
    "学校法人": ("(学)",),
    "医療法人": ("(医)",),
    "医療法人社団": (),
    "医療法人財団": (),
    "社会医療法人": (),
    "宗教法人": (),
    "特定非営利活動法人": ("(特非)",),
}


def _pattern(token: str) -> re.Pattern[str]:
    # Accept spaces inside a designation, including '( 株 )' and '株 式 会 社'.
    return re.compile(r"\s*".join(re.escape(char) for char in token))


_TOKENS = sorted(
    [(token, form) for form, aliases in LEGAL_FORMS.items() for token in (form, *aliases)],
    key=lambda item: len(item[0]),
    reverse=True,
)
_PATTERNS = tuple((_pattern(token), form) for token, form in _TOKENS)


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
    # contains the shorter prefix 医療法人; 一般社団法人 contains the
    # shorter suffix 社団法人. These are overlaps, not conflicting forms.
    best: dict[str, tuple[int, str, str]] = {}
    for pattern, form in _PATTERNS:
        match = pattern.match(text)
        if match and ("prefix" not in best or match.end() > best["prefix"][0]):
            best["prefix"] = (match.end(), form, text[match.end():].strip())
        # Search using an end anchor: don't mistake a form in the middle for a suffix.
        match = re.search(pattern.pattern + r"\Z", text)
        if match:
            length = len(text) - match.start()
            if "suffix" not in best or length > best["suffix"][0]:
                best["suffix"] = (length, form, text[:match.start()].strip())
    return [(form, position, name) for position, (_, form, name) in best.items()]


def parse_name(value: str, *, remove_all_spaces: bool = False) -> ParsedName:
    """Normalize a Japanese organization name and identify its legal form.

    Apply Unicode NFKC and trim and collapse whitespace. A supported legal
    form or abbreviation at either end is replaced with its canonical form
    in the same position, with no separator between the form and the stem.

    Ambiguous cases include competing forms, a form without a stem, and
    expansions that would change the extracted parts on a second pass.
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


def normalize_name(value: str, *, remove_all_spaces: bool = False) -> str:
    """Return only the display text produced by :func:`parse_name`.

    The ``remove_all_spaces`` option follows the same whitespace rules as
    :func:`parse_name`.
    """
    return parse_name(value, remove_all_spaces=remove_all_spaces).normalized


def split_name(value: str, *, remove_all_spaces: bool = False) -> tuple[str | None, str, str | None]:
    """Return ``(prefix, stem, suffix)`` from :func:`parse_name`.

    Absent forms are ``None``. When no form is extracted, the stem is the
    normalized text. Pass ``remove_all_spaces=True`` to remove all whitespace
    before splitting.
    """
    return parse_name(value, remove_all_spaces=remove_all_spaces).parts
