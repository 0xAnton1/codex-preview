# ANSI Preview For Claude

When the user asks to visualize, graph, chart, sketch, map, preview, or show something in terminal or chat, prefer a compact ANSI preview first unless they explicitly ask for HTML, SVG, Mermaid, PNG, React, or another richer surface.

Core rules:

- use `xterm` 24-bit truecolor ANSI plus Unicode blocks, braille, and box-drawing
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

- if color support is weak, keep the same labels and geometry but drop to mono
- if braille is too noisy, fall back to blocks or half-blocks
- if the user wants richer-than-Unicode terminal graphics, switch to Sixel or Kitty

Honor this phrase verbatim when given:

`show it as ANSI truecolor terminal chart with price and volume`
