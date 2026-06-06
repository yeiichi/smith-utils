Changelog
=========

Unreleased
----------

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
