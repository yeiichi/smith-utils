Japanese Organization Names
===========================

Use :func:`~smith_utils.com_name_cleaner.normalize_name` for display text,
:func:`~smith_utils.com_name_cleaner.split_name` for a three-part tuple, or
:func:`~smith_utils.com_name_cleaner.parse_name` when you also need the
parsing status.

By default, ``normalize_name`` and ``split_name`` convert printable ASCII
characters, including letters, digits, punctuation, and spaces, to full width
in the display text and stem, respectively. Pass ``full_width=False`` for
half-width ASCII. Both modes preserve letter case.

.. code-block:: python

   from smith_utils.com_name_cleaner import normalize_name, parse_name

   normalize_name("Demo 123")  # "Ｄｅｍｏ　１２３"
   normalize_name("Ｄｅｍｏ　１２３", full_width=False)  # "Demo 123"

   result = parse_name("例示用商事（株）")
   result.normalized  # "例示用商事株式会社"
   result.parts       # (None, "例示用商事", "株式会社")
   result.status      # "parsed"

For shell and CSV examples, see :ref:`com-name-cleaner-cli`.

The parser recognizes supported legal forms at the beginning or end of a
name. Common abbreviations include ``(株)`` for ``株式会社``, ``(有)`` for
``有限会社``, ``(同)`` for ``合同会社``, and ``(一社)`` for ``一般社団法人``.
The parser also covers professional corporations, cooperatives, financial
institutions, and public bodies. The legacy abbreviations ``(社)`` and
``(財)`` expand to ``社団法人`` and ``財団法人`` respectively.

Unicode normalization also lets the parser recognize forms written with
full-width parentheses and characters such as ``㈱``. A form found only
inside a name stays in the stem. Shared abbreviations such as ``(特)``
produce an ``ambiguous`` status because ``(特)`` can refer to either
``弁理士法人`` or ``特許業務法人``. When the split is ambiguous, the
parser keeps the Unicode- and whitespace-normalized input as the stem.

.. automodule:: smith_utils.com_name_cleaner
   :members: ParsedName, normalize_name, parse_name, split_name

CSV files
---------

.. automodule:: smith_utils.com_name_cleaner.csv_io
   :members: clean_csv
