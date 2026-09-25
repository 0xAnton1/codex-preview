# Changelog

All notable changes to Codex Preview are documented here.

This project follows [Semantic Versioning](https://semver.org/) and the
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

## [Unreleased]

### Added

- Reserved for changes after `0.2.0`.

## [0.2.0] - 2026-09-25

### Added

- A deterministic, dependency-free renderer for line charts, braille plots,
  comparison bars, tables, state lanes, flows, and wireframes.
- Explicit terminal and chat surface modes, including ANSI suppression for
  copy-safe chat output.
- Cross-platform installers for Codex and Claude on PowerShell and POSIX
  shells.
- A runnable demo and a 14-case standard-library test suite covering geometry,
  widths, truncation, loading, wrapping, and chat safety.

### Changed

- Documentation now explains the Codex Desktop integrated-terminal workflow,
  portable chat fallback, and the boundary between structured rendering and
  conceptual wireframes.
- Boxed dashboard examples use fixed-width Unicode geometry that remains
  aligned when copied into chat or Markdown.

### Fixed

- Mixed-sign bars, missing-value gaps, table truncation, state sampling, and
  flow wrapping now have deterministic, tested behavior.

## [0.1.0] - 2026-04-06

- Initial public terminal-preview skill pack.

[Unreleased]: https://github.com/0xAnton1/codex-preview/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/0xAnton1/codex-preview/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/0xAnton1/codex-preview/releases/tag/v0.1.0
