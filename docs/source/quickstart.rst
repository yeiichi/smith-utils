Quickstart
==========

This page gives a short introduction to the most common use cases.
For command line usage, see :doc:`cli`.

.. _organization-name-quickstart:

Japanese Organization Names
===========================

Use ``com_name_cleaner`` to standardize a name or extract its legal form.
For example, ``（株）`` becomes ``株式会社`` and stays on the same side of
the name. The examples below use fictional names.

Use :func:`~smith_utils.com_name_cleaner.normalize_name` when you need a
display string. It collapses whitespace and converts ASCII letters, digits,
punctuation, and spaces to full width by default. Letter case is preserved.

.. code-block:: pycon

   >>> from smith_utils.com_name_cleaner import normalize_name, parse_name, split_name
   >>> normalize_name("（株）Demo 　123! ｶﾀｶﾅ")
   '株式会社Ｄｅｍｏ　１２３！　カタカナ'
   >>> normalize_name("（株）Demo 　123! ｶﾀｶﾅ", full_width=False)
   '株式会社Demo 123! カタカナ'

Use :func:`~smith_utils.com_name_cleaner.split_name` for a ``(prefix, stem,
suffix)`` tuple, or :func:`~smith_utils.com_name_cleaner.parse_name` to also
get the parsing status. Missing forms appear as ``None``. For example, a
name with legal forms at both ends is marked ``ambiguous`` for review.

.. code-block:: pycon

   >>> split_name("例示用商事（株）")
   (None, '例示用商事', '株式会社')
   >>> parse_name("（株）例示用商事（有）").status
   'ambiguous'

From the shell, pass a name directly or select the name column in a CSV file.
The CSV example below writes ``organizations_cleaned.csv`` alongside the
input and appends the normalized name, parts, and parsing status.

.. code-block:: bash

   com-name-cleaner '例示用商事（株）'
   printf '会社名\n例示用商事（株）\n' > organizations.csv
   com-name-cleaner --csv organizations.csv --column 会社名

The CLI and CSV output use the same normalization as ``parse_name``, which
uses Unicode NFKC and keeps ASCII characters half-width. For more options,
see :ref:`com-name-cleaner-cli` and :doc:`api/com_name_cleaner`.

Datetime Utilities
==================

.. currentmodule:: smith_utils

.. autofunction:: format_ordinal
   :no-index:
.. autofunction:: parse_strict_date
   :no-index:
.. autofunction:: ensure_date
   :no-index:

.. code-block:: python

   from smith_utils import ensure_date

   # Convert strings or datetime.date objects into a date object.
   date = ensure_date("20231225")  # datetime.date(2023, 12, 25)

Numeric Refinement
==================

.. currentmodule:: smith_utils

.. autofunction:: parse_numeric_value
   :no-index:
.. autofunction:: parse_currency_value
   :no-index:
.. autofunction:: sample_positive_gaussian
   :no-index:

.. code-block:: python

   from smith_utils import parse_numeric_value

   # Parse messy numeric data.
   value = parse_numeric_value("(1,250.50)")  # -1250.5

.. code-block:: python

   from smith_utils import sample_positive_gaussian

   # Generate Gaussian samples truncated to 0 < sample <= approx_upper_bound.
   # approx_upper_bound is treated as mean + 3 * sigma.
   samples = sample_positive_gaussian(mean=5.0, approx_upper_bound=10.0, trial_number=3)

Text Normalization & Metrics
============================

.. currentmodule:: smith_utils

.. autofunction:: normalize_text
   :no-index:
.. autofunction:: random_string
   :no-index:
.. autofunction:: make_unicode_char_name_records
   :no-index:
.. autofunction:: normalize_file_to_lf
   :no-index:
.. autofunction:: normalize_newlines_stream
   :no-index:

.. autoclass:: StringDistance
   :no-index:
   :members:

.. autofunction:: analyze_pair
   :no-index:
.. autoclass:: Result
   :no-index:
   :members:
.. autoclass:: Relation
   :no-index:

.. code-block:: python

   from smith_utils import normalize_text

   # Normalize text.
   clean_text = normalize_text("  Ｓｍｉｔｈ  Ｕｔｉｌｓ  ")  # "smith utils"

.. code-block:: python

   from smith_utils import random_string

   # Generate a secure random ASCII string.
   token = random_string(16)

.. code-block:: python

   from smith_utils import make_unicode_char_name_records

   # Extract codepoint and Unicode name metadata.
   records = make_unicode_char_name_records("Aあ")

.. code-block:: python

   from smith_utils import normalize_file_to_lf

   # Normalize newlines to LF and report original newline style.
   summary = normalize_file_to_lf("input.txt", "output.txt")

Crypto Hash Utilities
=====================

.. currentmodule:: smith_utils

.. autofunction:: get_text_digest
   :no-index:
.. autofunction:: get_file_digest
   :no-index:

.. code-block:: python

   from smith_utils import get_file_digest, get_text_digest

   # Calculate SHA-256 digests for strings and files.
   text_digest = get_text_digest("smith-utils")
   file_digest = get_file_digest("input.txt")

File Classification Utilities
=============================

.. currentmodule:: smith_utils

.. autoclass:: FileClassification
   :no-index:
   :members:

.. autofunction:: classify_file
   :no-index:

.. code-block:: python

   from smith_utils import classify_file

   # Classify a file from extension, MIME, magic bytes, and file(1) evidence.
   classification = classify_file("input.pdf")
   file_class = classification.file_class  # "document"
   categories = classification.categories  # ("document", "pdf")
