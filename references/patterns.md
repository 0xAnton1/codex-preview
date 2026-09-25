# Codex Preview Patterns

Load this file only when the best terminal form is unclear or the request needs a richer layout.

## Surface First

- Real terminal: ANSI is allowed when color is supported.
- Codex chat, Markdown, redirected output, or uncertain capability: use monochrome Unicode.
- Keep labels and geometry meaningful after color is removed.

## Intent Map

- trend, price, metric, smooth curve: braille raster; add one activity strip when a second magnitude matters.
- tiny summary: sparkline or microbar.
- funnel or stage comparison: aligned stage bars with deltas.
- dashboard or page: box-drawing wireframe with proportions and labels.
- system flow or decision logic: directional box flow.
- status, coverage, or regime history: lanes, bands, or a compact matrix.
- variants or rankings: aligned table with bars and deltas.

## Color Presets

- `semantic`: green/up, red/down, amber/warning, blue/info.
- `accent`: one highlight plus neutral structure.
- `categorical`: a small, distinct palette for a few series.
- `heatmap`: ordered intensity; use only when the value scale matters.
- `mono`: default outside a confirmed color terminal.

Color spans should cover meaningful runs. Avoid changing color character by character.

For aligned templates, compose and pad plain Unicode rows first, then wrap complete spans in ANSI color. Keep progress bars at one declared logical width and use ordinary spaces for padding; ANSI bytes and invisible braille blanks must not participate in layout calculations.

## Compact Templates

### Braille Line

```text
Metric 0.91 ┤        ⢀⣠⠤⠒⠉⠉⠢⣄
       0.64 ┤    ⢀⡴⠋          ⠘⢦⡀
       0.37 ┤ ⢀⡴⠃              ⠘⣆
       0.10 ┼⠤⠋                  ⠈⠒
              t0                   tN
```

### Series And Activity

```text
SERIES    ⣀⣠⣤⣶⣾⣷⣶⣤⣀
ACTIVITY  ▂▃▅█▇▃▂▆█▅▃▂
```

### UI Wireframe

```text
┌──────────────────────── App Shell ────────────────────────┐
│ Header                                                    │
├───────────────┬───────────────────────────┬───────────────┤
│ Left Nav      │ Main Chart / Table        │ Side Panel    │
│ filters       │ primary content           │ detail / logs │
├───────────────┴───────────────────────────┴───────────────┤
│ Status strip                                              │
└───────────────────────────────────────────────────────────┘
```

### Flow

```text
[Input] -> [Parse] -> [Score] -> [Decide] -> [Render]
                 \-> [Warn / fallback]
```

### Comparison Table

```text
Variant      Score   Delta   Preview
baseline     0.42    --      ████
candidate-a  0.57   +0.15    ██████
candidate-b  0.49   +0.07    █████
```

## Data And Layout Checks

- Bucket dense input; preserve endpoints, extrema, gaps, and important transitions.
- State units and transformations that affect interpretation.
- Mark unavailable or estimated values rather than silently substituting them.
- Abbreviate labels before shrinking the data region.
- Omit full borders when whitespace provides enough structure.
- Prefer one preview that answers the question over several near-duplicates.

## When ANSI Is The Wrong Tool

- Keep an explicitly requested HTML, SVG, Mermaid, image, React, or interactive format.
- If the user explicitly needs true color inside chat, render the terminal design to an image rather than pasting ANSI escape sequences.
- Use a richer renderer for dense multidimensional inspection or precise publication graphics.
- Use Sixel or Kitty only when the active terminal and an available renderer are confirmed to support it.
