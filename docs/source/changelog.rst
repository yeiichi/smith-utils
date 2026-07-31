Changelog
=========

Unreleased
----------

- No unreleased changes.

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
