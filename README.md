# Codex Preview

![Repo](https://img.shields.io/badge/repo-public-16a34a.svg)
![License](https://img.shields.io/badge/license-MIT-0f766e.svg)
![Codex](https://img.shields.io/badge/Codex_Desktop-ready-10b981.svg)
![Terminal](https://img.shields.io/badge/purpose-terminal_UI-0ea5e9.svg)

![Codex Preview hero](./assets/codex-preview-hero.svg)

A no-dependency terminal renderer and Codex skill for easier visual reasoning.

Turn numeric series, JSON/CSV records, service states, pipelines, and UI ideas into compact braille charts, comparison bars, width-aware tables, state lanes, flows, and wireframes.

It is built for Codex Desktop's [integrated terminal](https://learn.chatgpt.com/docs/integrated-terminal), with a copy-safe Unicode fallback for chat, Markdown, issues, and pull requests. Structured data is rendered deterministically, so the same input keeps the same geometry.

## Why Use It?

Visualization should make a decision easier, not become another project.

- **See the shape quickly:** spot trends, gaps, outliers, and state changes without opening a notebook, browser, or plotting stack.
- **Compare consistently:** render alternatives with the same width, labels, bars, and axes so differences are easy to scan.
- **Think before building:** sketch a dashboard, pipeline, or service flow in the terminal before writing frontend code.
- **Keep the result portable:** use color in the terminal and clean Unicode in Codex chat, documentation, issues, and reviews.
- **Reduce alignment work:** JSON and CSV inputs go through the deterministic renderer instead of being hand-padded by the model.

## What It Does

- numeric series as deterministic braille charts with explicit gaps
- positive and negative comparisons as zero-aligned bars
- JSON and CSV records as width-aware tables
- categorical history as sampled state lanes
- sequential systems as wrapping box-drawing flows
- page and dashboard ideas as terminal wireframes

Structured inputs use the dependency-free `scripts/preview.py` renderer, so scaling, gaps, widths, truncation, and alignment are reproducible. Codex still composes conceptual wireframes when there is no structured input. The separate demo script verifies terminal color and Unicode support locally.

## Codex Desktop: Where It Works

| Surface | Result | Recommended output |
|---|---|---|
| Integrated terminal | Best experience | ANSI truecolor + Unicode |
| Codex chat | Good structural preview | fenced monochrome Unicode |
| Markdown, issues, PRs | Portable | monochrome Unicode or screenshots |
| Limited fonts / terminals | Reduced fidelity | ASCII or block fallback |

Raw ANSI escape sequences are not intended for the Codex chat renderer. In chat, the geometry still works; open the integrated terminal when you want live color. This distinction is deliberate and keeps copied output readable.

## Quick Start

### Windows / Codex Desktop

From PowerShell:

```powershell
irm https://raw.githubusercontent.com/0xAnton1/codex-preview/main/scripts/install.ps1 | iex
```

Or from a cloned checkout:

```powershell
.\scripts\install.ps1 -Target codex
```

The default destination is `$CODEX_HOME\skills\codex-preview`, or `$HOME\.codex\skills\codex-preview` when `CODEX_HOME` is unset.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/0xAnton1/codex-preview/main/scripts/install.sh | bash -s -- --target codex
```

### Repo-local install

Install the skill only for the current repository:

```bash
./scripts/install.sh --target codex --codex-dir "$PWD/.codex"
```

On Windows:

```powershell
.\scripts\install.ps1 -Target codex -CodexDir (Join-Path $PWD '.codex')
```

Start a new Codex task after installation so the skill is discovered.

## Try It In 30 Seconds

From a cloned checkout, run the chat-safe demo:

```powershell
python .\scripts\demo.py --surface chat
```

Then ask Codex:

```text
Use $codex-preview to visualize these test timings as a compact braille chart.
```

For a real terminal preview, use:

```text
Use $codex-preview in the integrated terminal to compare these API latencies with zero-aligned bars.
```

## Use It In Codex

Invoke the skill directly:

```text
Use $codex-preview to sketch a terminal dashboard for build health,
test coverage, deploy status, and recent latency.
```

Other useful prompts:

```text
Use $codex-preview to show these values as a compact braille trend.
Use $codex-preview to map this pipeline as a terminal flow.
Use $codex-preview to compare these options in a TUI table.
Use $codex-preview to sketch this page as a terminal wireframe.
```

For a colored result, ask Codex to render or run the preview in the integrated terminal. For a response you want to copy into Markdown, ask for monochrome Unicode.

## Use The Renderer Directly

The renderer requires only Python 3. Global display options come before the rendering mode.

```powershell
# Braille chart with a missing-value gap
python .\scripts\preview.py --surface chat --width 70 line `
  --title "Latency" --values "10,12,11,18,14,,20,24,21"

# Mixed-sign comparison around a shared zero axis
python .\scripts\preview.py --surface chat bars `
  --title "P&L" --items "Alpha=42,Beta=-17,Gamma=28"

# Width-aware CSV table
python .\scripts\preview.py --width 80 table `
  --input results.csv --columns "name,score,status" --limit 15

# Categorical state history
python .\scripts\preview.py lanes `
  --items "API=ok,ok,warn,ok;DB=ok,warn,fail,ok"

# Wrapping sequential flow
python .\scripts\preview.py --width 60 flow `
  --steps "Ingest,Validate,Transform,Score,Publish"
```

JSON and CSV schemas, state names, and additional examples are documented in [`references/renderer.md`](./references/renderer.md).

## Verify Your Terminal

Run the bundled demo:

```powershell
python .\scripts\demo.py --surface auto --color auto
```

Force either surface when testing:

```powershell
python .\scripts\demo.py --surface terminal --color always
python .\scripts\demo.py --surface chat
```

`--surface chat` always suppresses ANSI escapes, even if color is requested. It produces the same portable form used in Codex chat and Markdown.

Expected chat fallback:

```text
┌────────────────────────────────────────────────────────────────────┐
│                    CODEX PREVIEW · TERMINAL UI                     │
│ Surface  chat         Mode  portable     Layout  fixed-width       │
├──────────────────────┼──────────────────────┼──────────────────────┤
│        SYSTEM        │       RENDERER       │        CHECKS        │
│      ● HEALTHY       │       ● ACTIVE       │     ▲ 1 WARNING      │
├────────────────────────────────────────────────────────────────────┤
│ Load        █████████████░░░░░░░  64%                              │
│ Coverage    █████████████████░░░  86%                              │
│ Throughput  ▁▂▄▅▇█▇▆▄▃▅▆      128/min                              │
│ Trend       ⢀⣠⠤⠒⠉⠉⠢⣄    ⣀⡠⠤⠒⠉     rising                           │
├────────────────────────────────────────────────────────────────────┤
│  surface: chat  ·  renderer: Unicode / no ANSI  ·  width: 70 cols  │
└────────────────────────────────────────────────────────────────────┘
```

## Is It Token-Efficient?

Sometimes—and now the skill says so precisely.

Braille is spatially efficient: one terminal cell represents a `2 × 4` dot grid, so a curve can carry more shape than a block-only chart of the same width. A compact chart or table can also replace a long verbal description.

ANSI is not automatically token-efficient. Every color escape sequence adds bytes and usually adds tokens. The efficient default is therefore:

1. one small preview;
2. monochrome or a few long color spans;
3. sampled data and abbreviated labels;
4. no repeated frame or prose duplication.

Do not rely on universal token ranges: token counts vary by model tokenizer, text, geometry, and color density. Measure the actual prompt and output with the tokenizer used by your target model when cost matters. The skill entrypoint is intentionally short, while the larger pattern library is loaded only when needed.

The deterministic renderer primarily improves reliability and avoids repeated model attempts to hand-align output. It does not make the rendered characters free: output returned to chat still counts like other text.

## How The Skill Works

Codex discovers the skill from its `SKILL.md` metadata. When a request clearly asks for a terminal/TUI visualization—or when you invoke `$codex-preview`—Codex loads the instructions and chooses a visual form. Structured data is routed through `scripts/preview.py`; detailed command schemas live in `references/renderer.md`; freeform templates remain in `references/patterns.md` for conceptual layouts.

This follows OpenAI's recommended skill structure: a focused `SKILL.md`, optional references for progressive disclosure, scripts for deterministic work, and UI metadata in `agents/openai.yaml`. See [OpenAI's skill documentation](https://developers.openai.com/plugins/build/skills).

```text
codex-preview/
├── SKILL.md
├── agents/openai.yaml
├── references/patterns.md
├── references/renderer.md
├── scripts/demo.py
├── scripts/preview.py
├── scripts/install.ps1
├── scripts/install.sh
├── tests/test_preview.py
├── CLAUDE.md
├── .claude/commands/codex-preview.md
└── assets/
```

## Design Boundaries

- Terminal-first does not mean terminal-only. Chat receives a portable Unicode fallback.
- The preview should expose structure, not pretend missing data exists.
- Explicit HTML, SVG, Mermaid, image, or interactive requests keep their requested format.
- Sixel and Kitty graphics require actual terminal and renderer support; the skill does not assume either.
- Color must reinforce labels and geometry, never become the only carrier of meaning.

## Tests

Run the dependency-free suite:

```powershell
python -B -m unittest discover -s tests -v
```

The suite checks Unicode display width, missing-value gaps, mixed-sign axes, table truncation, state sampling, flow wrapping, JSON/CSV loading, and chat suppression of ANSI escapes.

## Claude Compatibility

Claude support remains available through `CLAUDE.md` and `.claude/commands/codex-preview.md`:

```bash
./scripts/install.sh --target claude --project-dir "$PWD"
```

Or on Windows:

```powershell
.\scripts\install.ps1 -Target claude -ProjectDir $PWD
```

The installer preserves an existing `CLAUDE.md` and writes the extra guidance to `.claude/codex-preview-reference.md`.

## License

MIT
