Changelog
=========

Unreleased
----------

- No unreleased changes.

v1.0.0
------

- **Breaking change**. ``normalize_name()`` now returns full-width ASCII
  equivalents by default while preserving letter case. Pass
  ``full_width=False`` for the previous output.
- Add ``normalize_kanji_variants()`` for Japanese glyph normalization using
  the MJSU 1.2.0 table.
- Expand ``com_name_cleaner`` to recognize 78 legal forms and report shared
  abbreviations such as ``(特)`` as ambiguous.
- Add a :ref:`Japanese organization-name Quick Start <organization-name-quickstart>`
  for Python, CLI, and CSV workflows using fictional organization names.

v0.6.0
------

- Normalize Japanese organization names and extract legal forms from text and CSV.
- Add the ``smith com-name-cleaner`` subcommand and the standalone ``com-name-cleaner`` command.
- Document the cleaner's Python API, parsing statuses, and CLI usage.

v0.5.0
------

- Added Positive Gaussian Sampling (``sample_positive_gaussian``).
- Added the ``smith positive-gaussian-samples`` CLI command.
- Documented positive Gaussian sampling in the README, quickstart, CLI docs, and numeric API reference.

v0.4.0
------

- Added File Classification Utilities (``FileClassification``, ``classify_file``).
- Exposed file classification helpers from ``smith_utils.file`` and top-level ``smith_utils``.
- Documented file classification in the quickstart and API reference.

v0.3.1
------

- Added Crypto Hash Utilities (``get_text_digest``, ``get_file_digest``).
- Exposed hash helpers from ``smith_utils.crypto`` and top-level ``smith_utils``.
- Switched the package build backend from Setuptools to Hatchling.

v0.3.0
------

- Exposed text utilities at the package root.

v0.2.1
------

- Corrected project documentation and changelog URLs.

v0.2.0
------

- Added Unicode name metadata and newline normalization utilities.
- Configured semantic-release.

v0.1.0
------

- Initial release of ``smith-utils``.
- Added Datetime Utilities (``ensure_date``, ``parse_strict_date``, ``format_ordinal``).
- Added Numeric Refinement (``parse_numeric_value``).
- Added Text Normalization (``normalize_text``) and Metrics (``StringDistance``).
