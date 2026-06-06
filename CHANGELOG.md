# CHANGELOG

<!-- version list -->

## Unreleased

### Features

- Add file classification utilities via `smith_utils.file.classify_file`.
- Expose `FileClassification` and `classify_file` from the top-level `smith_utils` namespace.

### Documentation

- Document file classification in the README, quickstart, and API reference.


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
