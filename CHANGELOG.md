# CHANGELOG

<!-- version list -->

## v1.0.0 (2026-11-28)

### Breaking Changes

- `normalize_name()` now returns full-width ASCII equivalents by default while preserving letter case. Pass `full_width=False` for the previous output.

### Features

- Add `normalize_kanji_variants()` for Japanese glyph normalization using the MJSU 1.2.0 table.
- Expand `com_name_cleaner` to recognize 78 legal forms and report shared abbreviations such as `(特)` as ambiguous.

### Documentation

- Add a Japanese organization-name Quick Start for Python, CLI, and CSV workflows using fictional organization names.

## v0.6.0 (2026-11-22)

### Features

- Normalize Japanese organization names and extract legal forms from text and CSV.
- Add the `smith com-name-cleaner` subcommand and the standalone `com-name-cleaner` command.

### Documentation

- Document the cleaner's Python API, parsing statuses, and CLI usage.

## v0.5.0 (2026-07-31)

### Features

- Add positive Gaussian sampling via `sample_positive_gaussian`.
- Add `smith positive-gaussian-samples` CLI command.

### Documentation

- Document positive Gaussian sampling in the README, quickstart, CLI docs, and numeric API reference.


## v0.4.0 (2026-06-06)

### Build System

- Switch to Hatchling
  ([`e1521e2`](https://github.com/yeiichi/smith-utils/commit/e1521e2dae3f0e37d74bb05deb04fb3631cf1f23))

### Features

- Add file classification utilities
  ([`9fa0248`](https://github.com/yeiichi/smith-utils/commit/9fa0248a4aa28848cea8563069e7a28504ee9a20))

## v0.3.1 (2026-06-04)

### Features

- Add SHA-256 hash utilities for text strings and files.
- Expose hash helpers from `smith_utils.crypto` and the top-level `smith_utils` namespace.

### Build System

- Switch the package build backend from Setuptools to Hatchling.


## v0.3.0 (2026-05-29)

### Features

- Expose text utilities at package root
  ([`93ee497`](https://github.com/yeiichi/smith-utils/commit/93ee4970a0e5f30b17fc5c235e07c11a9affd7c9))


## v0.2.1 (2026-05-28)

### Bug Fixes

- Trigger patch release for URL correction
  ([`07ae073`](https://github.com/yeiichi/smith-utils/commit/07ae073eb2edf1d029faf7b491f95098fe390309))

### Documentation

- Correct URLs for Documentation and Changelog in TOML
  ([`860d3a0`](https://github.com/yeiichi/smith-utils/commit/860d3a07e3539180279cc0e7f78012a0d18ec3e0))


## v0.2.0 (2026-05-28)

### Chores

- Update .gitignore
  ([`156ea65`](https://github.com/yeiichi/smith-utils/commit/156ea657e54a4115c39133226e10c72c5ec2ae07))

### Features

- **text**: Add unicode/newlines APIs and configure semantic-release
  ([`aed682e`](https://github.com/yeiichi/smith-utils/commit/aed682e0c7ecf1751ab0719d4560b3afbb6b1a1e))


## v0.1.0 (2026-04-13)

- Initial Release
