Japanese Organization Names
===========================

Use :func:`~smith_utils.com_name_cleaner.normalize_name` for display text,
:func:`~smith_utils.com_name_cleaner.split_name` for a three-part tuple, or
:func:`~smith_utils.com_name_cleaner.parse_name` when you also need the
parsing status.

.. code-block:: python

   from smith_utils.com_name_cleaner import parse_name

   result = parse_name("例示用商事（株）")
   result.normalized  # "例示用商事株式会社"
   result.parts       # (None, "例示用商事", "株式会社")
   result.status      # "parsed"

For shell and CSV examples, see :ref:`com-name-cleaner-cli`.

.. automodule:: smith_utils.com_name_cleaner
   :members: ParsedName, normalize_name, parse_name, split_name

CSV files
---------

.. automodule:: smith_utils.com_name_cleaner.csv_io
   :members: clean_csv
