Command Line Tools
==================

The ``smith`` command provides small wrappers around selected ``smith-utils`` APIs.

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
