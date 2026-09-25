# Codex Preview For Claude

When the user asks for a terminal, TUI, ANSI, CLI, braille, or text-mode visualization, prefer a compact terminal preview unless they explicitly ask for HTML, SVG, Mermaid, PNG, React, or another richer surface.

Core rules:

- use ANSI color only in a real terminal that supports it
- use fenced monochrome Unicode in chat or Markdown; do not print raw escape sequences there
- prefer `braille raster` for dense or smooth curves
- prefer stacked or dual-strip output for price plus volume
- use box-drawing for flows, wireframes, and structural maps
- keep previews compact, usually around `60-100` columns
- keep legends short and stable
- use color semantically, not decoratively

Legend convention:

- `primary flow`: green or main accent
- `exploration flow`: cyan
- `aggregate outputs`: blue
- `caution`: amber
- `neutral context`: gray

Fallbacks:

- if color support is weak or unknown, keep the same labels and geometry but drop to mono
- if braille is too noisy, fall back to blocks or half-blocks
- use Sixel or Kitty only when the active terminal and an available renderer support it

Honor this phrase verbatim when given:

`show it as ANSI truecolor terminal chart with price and volume`
