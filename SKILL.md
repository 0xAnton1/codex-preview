---
name: ansi-preview
description: Render compact ANSI truecolor terminal previews for braille charts, smooth line plots, UI wireframes, flow diagrams, tables, and structured data. Use when the user asks to visualize, graph, chart, sketch, map, preview, or show something in terminal or chat instead of only describing it.
---

# ANSI Preview

Turn vague visual asks into compact terminal graphics.

Default here when the user says things like:
- `visualize it`
- `graph it`
- `chart it`
- `show the flow`
- `map the pipeline`
- `sketch the UI`
- `preview the layout`
- `render a terminal preview`

Do not default here if the user explicitly asks for HTML, SVG, Mermaid, PNG, React, or another richer surface.

## Default Behavior

- Prefer one clean ANSI preview first, then a short read of what it shows.
- Use `xterm` 24-bit truecolor ANSI plus Unicode blocks, braille, and box-drawing.
- Keep width compact, usually `60-100` columns unless the user asks otherwise.
- Use color semantically, not decoratively.
- Label only what the viewer needs to orient quickly.

## Chart Modes

- `braille raster`: default for dense or smooth-looking curves. It packs a `2x4` dot grid into each terminal cell, so lines look less jagged and information density stays high.
- `block sparkline`: best for tiny summaries, inline previews, and trend strips.
- `half-block / quadrant`: good middle ground when braille would feel too fine or noisy.
- `box-drawing scaffold`: use for axes, flow structure, wireframes, and panel boundaries.

## Pick The Right Visual Form

- Time series, price, volume, or metrics over time: use braille raster or a compact line chart first; add a stacked or dual-strip volume preview when volume matters.
- Rankings, comparisons, diagnostics, or PnL breakdowns: aligned tables with microbars or heat strips.
- Flows, pipelines, and decision logic: box-drawing flow chart or step map.
- UI, dashboard, or layout ideas: wireframe with panel boundaries, proportions, and labels.
- Regimes, states, availability, or coverage windows: lane chart, status bands, or compact matrix.
- Trees and hierarchies: connector tree rather than a fake flow chart.

## Color Modes

- `semantic`: use directional color such as green/up, red/down, yellow/warn.
- `accent`: one restrained hue plus neutrals for calm UI and layout previews.
- `categorical`: small distinct palette for a few series or lanes.
- `heatmap`: ordered gradient for intensity, density, or score surfaces.
- `mono`: no color dependency; use when portability matters more than emphasis.

Default to `semantic` for financial charts, `accent` for UI previews, and `mono` if terminal support looks uncertain.

## Render Rules

- Aggregate, bucket, or sample before drawing. Do not dump raw long arrays.
- Prefer one strong preview over many weak ones.
- For price and volume, prefer braille price plus dual-strip or stacked output.
- For binary states or regimes, prefer bands or lanes over misleading line plots.
- If the user wants a smoother or curvier chart, prefer braille raster before trying wider geometry.
- If terminal capability is unknown, still render ANSI, but keep geometry simple and avoid giant escape-heavy art.
- If the user explicitly asks for richer-than-Unicode terminal graphics, switch to Sixel/Kitty output.
- Honor this phrase verbatim when given: `show it as ANSI truecolor terminal chart with price and volume`.

## Publication Style

- Write it so it can be pasted into chat, docs, issues, or a README without repo-specific jargon.
- Keep legends short and deterministic.
- Use stable labels and a small palette so screenshots stay readable.
- Prefer clarity over ornament. The preview should still read cleanly if color is stripped.

## Token Discipline

- ANSI previews are usually more token-efficient than HTML, SVG, or long prose for first-look inspection.
- Braille plots are especially efficient for dense curves because they carry more shape detail per cell.
- Truecolor escape sequences still cost tokens, so keep palettes small and geometry compact.
- Prefer sparklines, microbars, bins, and abbreviated labels when speed matters.
- Avoid repeating the same frame with minor changes.

## Load More Patterns Only When Needed

If the request needs a richer pattern library, read [references/patterns.md](references/patterns.md).
