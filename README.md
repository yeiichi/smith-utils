# smith-utils
[![PyPI version](https://img.shields.io/pypi/v/smith-utils.svg)](https://pypi.org/project/smith-utils/)
![Python versions](https://img.shields.io/pypi/pyversions/smith-utils.svg)
![Status](https://img.shields.io/badge/status-Alpha-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
[![Documentation Status](https://readthedocs.org/projects/smith-utils/badge/?version=latest)](https://smith-utils.readthedocs.io/en/latest/?badge=latest)


**Smith Utils** is a central hub for data cleaning and parsing scripts. 
This package consolidates distributed utility functions to improve code reuse and maintenance efficiency across all yeiichi projects.

## Key Features

### Datetime Utilities (`smith_utils.datetime`)
Robust date parsing and formatting.
- `ensure_date`: Flexible conversion of strings, `datetime.date` objects, or `None` (returns today) into a `date` object.
- `parse_strict_date`: Strict parsing for `YYYYMMDD` or `YYYY-MM-DD` formats, rejecting ambiguous inputs.
- `format_ordinal`: Converts integers to ordinal strings (e.g., `1` → `"1st"`, `22` → `"22nd"`).

### Numeric Refinement (`smith_utils.numeric`)
Clean and parse messy numeric data.
- `parse_numeric_value`: Handles custom separators, decimals, and negative formats like `(1,234.56)`.
- `parse_currency_value`: Alias for numeric parsing, specifically for currency strings.

### Text Normalization & Metrics (`smith_utils.text`)
Standardize text and compare string similarity.
- `normalize_text`: Unicode NFKC normalization, case folding, and whitespace handling.
- `StringDistance`: Implementation of Damerau-Levenshtein and Jaro-Winkler algorithms for fuzzy matching.
- `analyze_pair`: Convenience function for string comparison returning a `Result`.
- `Relation` / `Result`: Relation enum and typed result for text comparisons.
- `make_unicode_char_name_records`: Extract Unicode codepoint/name metadata from text.
- `normalize_newlines_stream`: Stream-based newline normalization to LF with newline type detection.
- `normalize_file_to_lf`: File-based newline normalization helper.

### Crypto Hash Utilities (`smith_utils.crypto`)
Calculate SHA-256 digests for text and files.
- `get_text_digest`: Returns the SHA-256 hexadecimal digest for a text string.
- `get_file_digest`: Returns the SHA-256 hexadecimal digest for a file using streaming reads.

### File Classification Utilities (`smith_utils.file`)
Classify files from multiple evidence sources.
- `classify_file`: Returns extension, MIME, magic-number, and `file(1)` classification evidence.
- `FileClassification`: Dataclass result containing raw signals, `file_class`, and derived categories.

## Installation

Install via pip:

```bash
pip install smith-utils
```

## Quick Start

```python
from smith_utils import ensure_date, get_text_digest, parse_numeric_value, normalize_text
from smith_utils import make_unicode_char_name_records
from smith_utils import classify_file, get_file_digest, normalize_file_to_lf

# Datetime
date = ensure_date("20231225") # datetime.date(2023, 12, 25)

# Numeric
value = parse_numeric_value("(1,250.50)") # -1250.5

# Text
clean_text = normalize_text("  Ｓｍｉｔｈ  Ｕｔｉｌｓ  ") # "smith utils"

# Unicode metadata
records = make_unicode_char_name_records("Aあ")
# [UnicodeCharNameRecord(index=0, codepoint='U+0041', ...), ...]

# Normalize a file's newlines to LF
summary = normalize_file_to_lf("input.txt", "output.txt")
# {'newline_type': 'CRLF', 'bytes_in': ..., 'bytes_out': ...}

# SHA-256 digests
text_digest = get_text_digest("smith-utils")
file_digest = get_file_digest("input.txt")

# File classification
classification = classify_file("input.pdf")
# FileClassification(extension='.pdf', file_class='document', categories=('document', 'pdf'), ...)
```

## Directory Structure
- `src/smith_utils/`: Main package source.
- `legacy/`: Legacy scripts and templates (not included in distribution).
- `tests/`: Comprehensive test suite.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
