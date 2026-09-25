---
name: codex-preview
description: Create compact terminal-first previews with Unicode charts, tables, flows, and UI wireframes. Use when the user asks for a terminal, TUI, ANSI, CLI, braille, or text-mode visualization; do not replace requested HTML, SVG, Mermaid, images, or interactive visualizations.
---

# Codex Preview

Turn a visual idea or data summary into a compact terminal preview.

## Choose The Output Surface

Decide where the preview will be viewed before adding color:

- **Real terminal, including the Codex Desktop integrated terminal:** use ANSI color when the terminal supports it. Keep the geometry readable without color.
- **Codex Desktop chat or Markdown:** return a fenced plain-text Unicode preview. Do not print raw escape sequences; chat renderers may show them literally or strip them.
- **Unknown or redirected output:** default to monochrome Unicode.

Explicit user format choices win. Do not use this skill when the user asks for HTML, SVG, Mermaid, PNG, React, or another richer surface.

## Workflow

1. Identify the question the preview must answer and the available data. Never invent missing values.
2. For numeric, tabular, state-lane, or sequential data, read [references/renderer.md](references/renderer.md) and use `scripts/preview.py` for deterministic layout when local Python is available.
3. For conceptual output, or when the renderer does not fit, choose the smallest useful form:
   - trend or dense series: braille line or sparkline;
   - ranking or comparison: aligned table with microbars;
   - process or decision logic: box-drawing flow;
   - page or dashboard: labeled wireframe;
   - state over time: lanes, bands, or a compact matrix.
4. Bucket or sample long series before drawing. Preserve endpoints, extrema, gaps, and important transitions.
5. Render one primary preview, normally 60-100 columns, followed by at most a short interpretation.
6. Check alignment, labels, legend meaning, and monochrome readability.

## Rendering Rules

- Use Unicode braille for dense curves, blocks for small summaries, and box drawing for structure.
- Use color semantically and sparingly: green/up, red/down, amber/warning, blue/info, gray/context.
- Keep each colored run long enough to matter; avoid per-character truecolor changes.
- Build and pad the uncolored text first, then apply ANSI to complete spans so escape codes cannot break alignment.
- Use fixed logical widths for bars and columns. Prefer ordinary spaces for padding; avoid invisible braille blanks.
- Label axes or units when their absence could mislead.
- Mark sampled, normalized, estimated, or unavailable data explicitly.
- Avoid giant frames, decorative gradients, duplicated views, and long prose that repeats the graphic.
- Do not claim Sixel or Kitty support unless the active terminal and an available renderer actually support it.

## Token Discipline

- Prefer a short mono or low-color preview for first-pass inspection.
- Braille increases spatial density, but ANSI escape sequences add tokens; “ANSI” is not automatically cheaper.
- Reuse a small palette, color spans rather than characters, abbreviate labels, and omit redundant borders.
- Treat token efficiency as workload-dependent. Compare actual outputs with the target model tokenizer when cost matters.

## Optional Patterns

Read [references/patterns.md](references/patterns.md) only when the best visual form is unclear or the request needs a richer layout pattern.
