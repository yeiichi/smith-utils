Text Normalization & Metrics
============================

.. automodule:: smith_utils.text
   :members: normalize_text, normalize_kanji_variants, random_string, random_mixed_char, StringDistance, analyze_pair, Relation, Result, UnicodeCharNameRecord, make_unicode_char_name_records, NewlineType, normalize_newlines_stream, normalize_file_to_lf

Kanji variant normalization
---------------------------

``normalize_kanji_variants()`` applies the selected JIS X 0213-compatible
Unicode targets from MJSU 1.2.0. Bare characters use their default MJ glyph.
An attached selector must match a bundled Moji_Joho or standardized
variation sequence with a usable target. The conversion is many-to-one
and can discard glyph distinctions.

.. code-block:: python

   from smith_utils import normalize_kanji_variants

   assert normalize_kanji_variants("髙橋 國") == "高橋 國"
   assert normalize_kanji_variants("\u3530\U000E0101") == "恆"

The data is derived from the IPA's
`MJ Single-Choice Reduction Table 1.2.0 <https://moji.or.jp/mojikiban/map/>`_
and `MJ Character Information List 006.02 <https://moji.or.jp/mojikiban/mjlist/>`_.
The installed package includes the replacement table and its
CC BY-SA 2.1 Japan attribution and provenance notice.

For shell use, see :ref:`normalize-kanji-variants-cli`.
