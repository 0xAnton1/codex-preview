Render the user's request as a compact terminal-first preview.

Rules:

- use ANSI color only in a real terminal that supports it
- use fenced monochrome Unicode in chat or Markdown
- use Unicode braille, blocks, and box-drawing
- prefer `braille raster` for dense or smooth curves
- use stacked or dual-strip output for price plus volume
- use box-drawing for system maps, wireframes, and flow diagrams
- keep width compact, usually `60-100` columns
- keep legends short and deterministic
- color should clarify structure, not decorate it
- use Sixel or Kitty only when the active terminal and an available renderer support it
- honor this phrase verbatim when given: `show it as ANSI truecolor terminal chart with price and volume`

Legend convention:

- `primary flow`
- `exploration flow`
- `aggregate outputs`
- `caution`
- `neutral context`

Request:

$ARGUMENTS
