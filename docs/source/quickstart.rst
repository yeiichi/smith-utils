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

.. autoclass:: StringDistance
   :no-index:
   :members:

.. autofunction:: analyze_pair
   :no-index:

.. code-block:: python

   from smith_utils import normalize_text

   # Normalize text.
   clean_text = normalize_text("  Ｓｍｉｔｈ  Ｕｔｉｌｓ  ")  # "smith utils"

.. code-block:: python

   from smith_utils import make_unicode_char_name_records

   # Extract codepoint and Unicode name metadata.
   records = make_unicode_char_name_records("Aあ")
