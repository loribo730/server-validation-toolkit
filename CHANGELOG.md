# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows semantic versioning.

## [1.0.0] - 2026-06-04

### Added

- Added public release baseline.
- Added `storage-summary` with text and JSON lsblk parsing.
- Added `ipmi-summary` for `ipmitool sensor list` output.
- Added `report` command for combined Markdown diagnostic reports.
- Added additional unit tests for parser behavior and report generation.
- Expanded README documentation, known limitations, and verification workflow.

### Changed

- Kept existing `collect`, `sanitize`, `package`, and `pcie-summary` behavior compatible.
- Added `lsblk_json` to the default collector command set for more stable storage parsing.

## [0.2.0] - 2026-06-04

### Added

- Added storage hardware device summary parser for `lsblk` text outputs.
- Introduced `storage-summary` subcommand to the core CLI system.
- Added automated unit tests covering valid and malformed block storage outputs.

## [0.1.2] - 2026-06-04

### Changed

- Added explicit exception documentation to archive helpers.
- Documented why diagnostic command execution uses `check=False`.
- Expanded README documentation with known limitations and verification steps.
- Kept existing CLI behavior unchanged.

## [0.1.1] - 2026-06-04

### Fixed

- Improved sanitizer directory traversal from repeated full scans to one precomputed text-file set.
- Replaced `Path.rename()` with `shutil.move()` in sanitized collection flow for safer filesystem boundary handling.
- Added regression tests for sanitizer traversal behavior and sanitized collection movement.

## [0.1.0] - 2026-06-04

### Added

- Initial public release.
- Added Ubuntu Server diagnostic collector.
- Added best-effort sanitizer for sensitive identifiers.
- Added archive packaging command.
- Added PCIe summary parser for `lspci` output.
- Added GitHub Actions CI workflow.
- Added issue and pull request templates.
