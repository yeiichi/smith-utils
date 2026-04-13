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

### 📅 Datetime Utilities (`smith_utils.datetime`)
Robust date parsing and formatting.
- `ensure_date`: Flexible conversion of strings, `datetime.date` objects, or `None` (returns today) into a `date` object.
- `parse_strict_date`: Strict parsing for `YYYYMMDD` or `YYYY-MM-DD` formats, rejecting ambiguous inputs.
- `format_ordinal`: Converts integers to ordinal strings (e.g., `1` → `"1st"`, `22` → `"22nd"`).

### 🔢 Numeric Refinement (`smith_utils.numeric`)
Clean and parse messy numeric data.
- `parse_numeric_value`: Handles custom separators, decimals, and negative formats like `(1,234.56)`.
- `parse_currency_value`: Alias for numeric parsing, specifically for currency strings.

### 📝 Text Normalization & Metrics (`smith_utils.text`)
Standardize text and compare string similarity.
- `normalize_text`: Unicode NFKC normalization, case folding, and whitespace handling.
- `StringDistance`: Implementation of Damerau-Levenshtein and Jaro-Winkler algorithms for fuzzy matching.

## Installation

Install via pip:

```bash
pip install smith-utils
```

## Quick Start

```python
from smith_utils.datetime.date_utils import ensure_date
from smith_utils.numeric.refinement import parse_numeric_value
from smith_utils.text.normalization import normalize_text

# Datetime
date = ensure_date("20231225") # datetime.date(2023, 12, 25)

# Numeric
value = parse_numeric_value("(1,250.50)") # -1250.5

# Text
clean_text = normalize_text("  Ｓｍｉｔｈ  Ｕｔｉｌｓ  ") # "smith utils"
```

## Directory Structure
- `src/smith_utils/`: Main package source.
- `legacy/`: Legacy scripts and templates (not included in distribution).
- `tests/`: Comprehensive test suite.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
