from .metrics import StringDistance, analyze_pair, Result, Relation
from .newlines import NewlineType, normalize_file_to_lf, normalize_newlines_stream
from .normalization import normalize_text
from .unicode_char_names import UnicodeCharNameRecord, make_unicode_char_name_records

__all__ = [
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
]
