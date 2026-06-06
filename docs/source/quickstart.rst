Quickstart
==========

This page gives a short introduction to the most common use cases.

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

.. code-block:: python

   from smith_utils import parse_numeric_value

   # Parse messy numeric data.
   value = parse_numeric_value("(1,250.50)")  # -1250.5

Text Normalization & Metrics
============================

.. currentmodule:: smith_utils

.. autofunction:: normalize_text
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
