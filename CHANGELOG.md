# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0](https://github.com/yenksid/nexus_cli/compare/v0.2.0...v0.3.0) (2026-02-15)


### Features

* setup automated multi-file versioning and project roadmap. Closes [#4](https://github.com/yenksid/nexus_cli/issues/4) ([2d50873](https://github.com/yenksid/nexus_cli/commit/2d5087331e361c5757d63faf442a2e0a0b146eb2))


### Bug Fixes

* rename manifest file to .release-please-manifest.json. Closes [#4](https://github.com/yenksid/nexus_cli/issues/4) ([53746fe](https://github.com/yenksid/nexus_cli/commit/53746fe5d78524343d751e4b37d1dddcb8034ea5))
* rename manifest file to .release-please-manifest.json. Closes [#4](https://github.com/yenksid/nexus_cli/issues/4) ([ad03a8c](https://github.com/yenksid/nexus_cli/commit/ad03a8cdb9217391758cc41e39db5dc7b1f00dbd))

## [0.2.0] - 2026-02-14
### Added
- Modular Registry Pattern for file handlers in `handlers.py`.
- Automatic token estimation using `tiktoken`.
- Context minification flag (`-m`) for token efficiency.
- Auto-clipboard functionality (`-c`) via `pyperclip`.
- Comprehensive E2E test suite in `tests/run_tests.py`.
- Progress indicators and styled console output using `rich`.
- Dynamic timestamped filenames for scan outputs.
- GitHub Actions CI pipeline for Windows, Linux, and macOS.
