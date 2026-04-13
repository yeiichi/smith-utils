Quickstart
==========

This page gives a short introduction to the most common use cases.

Datetime Utilities
------------------

.. code-block:: python

   from smith_utils.datetime.date_utils import ensure_date

   # Convert strings or datetime.date objects into a date object.
   date = ensure_date("20231225")  # datetime.date(2023, 12, 25)

Numeric Refinement
------------------

.. code-block:: python

   from smith_utils.numeric.refinement import parse_numeric_value

   # Parse messy numeric data.
   value = parse_numeric_value("(1,250.50)")  # -1250.5

Text Normalization
------------------

.. code-block:: python

   from smith_utils.text.normalization import normalize_text

   # Normalize text.
   clean_text = normalize_text("  Ｓｍｉｔｈ  Ｕｔｉｌｓ  ")  # "smith utils"
