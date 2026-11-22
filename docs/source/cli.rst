Command Line Tools
==================

The ``smith`` command provides small wrappers around selected ``smith-utils`` APIs.
Use ``smith com-name-cleaner`` or the standalone ``com-name-cleaner`` for
Japanese organization names.

Random strings
--------------

Generate secure random ASCII strings by default:

.. code-block:: bash

   smith random-string 16

Choose another character category:

.. code-block:: bash

   smith random-string 12 --category kanji
   smith random-string 12 --category mix --ascii-ratio 0.7

Digests
-------

Calculate SHA-256 digests for text or files:

.. code-block:: bash

   smith digest --text "smith-utils"
   smith digest input.txt

Text normalization
------------------

Normalize text passed as an argument:

.. code-block:: bash

   smith normalize-text "  Ｓｍｉｔｈ  Ｕｔｉｌｓ  "

Or read from standard input:

.. code-block:: bash

   cat input.txt | smith normalize-text

Useful options:

.. code-block:: bash

   smith normalize-text --keep-case "  Hello   World  "
   smith normalize-text --remove-all-whitespace "  Hello   World  "
   smith normalize-text --no-nfkc "① ＡＢＣ"

Unicode names
-------------

Print one tab-separated row per character:

.. code-block:: bash

   smith unicode-names "Aあ"

File classification
-------------------

Classify a file from extension, MIME, magic bytes, and ``file(1)`` evidence:

.. code-block:: bash

   smith classify-file input.pdf

Positive Gaussian samples
-------------------------

Generate Gaussian samples truncated to positive values up to the approximate upper bound.
The bound is treated as ``mean + 3 * sigma`` and as a truncation bound:

.. code-block:: bash

   smith positive-gaussian-samples 3 --mean 5 --approx-upper-bound 10

.. _com-name-cleaner-cli:

Japanese organization names
---------------------------

Both ``smith com-name-cleaner`` and ``com-name-cleaner`` accept the same arguments.
Pass one or more quoted names as arguments or send one UTF-8 name per line
on standard input. By default, the command prints one normalized name per line.

.. code-block:: bash

   smith com-name-cleaner '㈱ 例示用工房' '例示用商事（株）'
   printf '%s\n' '㈱ 例示用工房' '例示用商事（株）' | com-name-cleaner

Use ``--parts`` for JSON Lines arrays in prefix, stem, suffix order.
Missing legal forms appear as ``null``. Use ``--json`` for JSON Lines
objects with the original and normalized text, the extracted fields, and
the parsing status.

.. code-block:: bash

   com-name-cleaner --parts '例示用商事（株）'
   com-name-cleaner --json '(医) 社団例示用診療所'

The second example returns an ``ambiguous`` status because expanding
``(医)`` would make ``社団`` appear to be part of the legal form.
Use ``--remove-all-spaces`` in either text or CSV mode to remove all Unicode
whitespace before parsing.

Clean a CSV
~~~~~~~~~~~

Supply the input file and the exact header of the organization-name column.

.. code-block:: bash

   com-name-cleaner --csv organizations.csv --column 会社名
   com-name-cleaner --csv legacy.csv --column 会社名 --encoding cp932 --output cleaned.csv

The first command writes ``organizations_cleaned.csv`` beside the input.
By default, the reader accepts UTF-8 with or without a byte order mark (BOM).
The output uses UTF-8 with a BOM. It preserves the original columns and
appends ``normalized_name``, ``prefix``, ``stem``, ``suffix``, and
``parse_status``. Missing legal forms appear as empty cells.

See :doc:`api/com_name_cleaner` for the Python API and parsing statuses.
