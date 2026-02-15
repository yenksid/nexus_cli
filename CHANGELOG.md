# Changelog

All notable changes to this project will be documented in this file.

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