# ANSI Preview

![Repo](https://img.shields.io/badge/repo-public-16a34a.svg)
![License](https://img.shields.io/badge/license-MIT-0f766e.svg)
![Codex](https://img.shields.io/badge/Codex-compatible-10b981.svg)
![Claude](https://img.shields.io/badge/Claude-compatible-2563eb.svg)

Braille charts. Flow maps. Wireframes. Terminal-first visuals.

> A lightweight Codex skill pack for clean ANSI truecolor previews: braille charts, flow maps, wireframes, tables, and terminal-first visual thinking.

![ANSI Preview hero](./assets/ansi-preview-hero.svg)

## Why I Built It

I originally built this for myself.
It made me noticeably more productive and took real mental load off long coding sessions.
When you stare at a black terminal for `10h+`, plain text starts to blur together.
Adding compact color, structure, and shape made it much easier to stay focused and reason clearly.

This is especially useful for:

- visualizing complex processes step by step
- showing things an LLM understands but does not explain clearly in plain prose
- previewing a UI, chart, data slice, or system flow before writing real code
- getting a fast high-level read when you do not want to open a full frontend or plotting stack
- turning a dull black-and-white conversation into something easier to review in chat, markdown, and docs

On terminals and chat surfaces that support ANSI truecolor and Unicode well, tools like Codex and Claude can make these previews feel surprisingly alive while staying lightweight and immediate.

## What This Is

`ansi-preview` is a small public skill pack for turning requests like:

- `visualize it`
- `graph it`
- `show the flow`
- `preview the layout`
- `show it as ANSI truecolor terminal chart with price and volume`

into compact, readable terminal visuals.

It is designed to work well for:

- Codex users via `SKILL.md`
- Claude users via `CLAUDE.md` and `.claude/commands/ansi-preview.md`
- GitHub readers via screenshots, SVGs, and copy-paste-friendly examples

## Quick Start

### Fast Download

- Public GitHub repo: `https://github.com/0xAnton1/ansi-preview`
- Latest release: `https://github.com/0xAnton1/ansi-preview/releases/latest`
- Download ZIP: `https://github.com/0xAnton1/ansi-preview/archive/refs/heads/main.zip`
- Clone:

```bash
git clone git@github.com:0xAnton1/ansi-preview.git
```

### One-Command Install

Codex global install:

```bash
curl -fsSL https://raw.githubusercontent.com/0xAnton1/ansi-preview/main/scripts/install.sh | bash -s -- --target codex
```

Codex repo-local install:

```bash
curl -fsSL https://raw.githubusercontent.com/0xAnton1/ansi-preview/main/scripts/install.sh | bash -s -- --target codex --codex-dir "$PWD/.codex"
```

Claude install into the current project:

```bash
curl -fsSL https://raw.githubusercontent.com/0xAnton1/ansi-preview/main/scripts/install.sh | bash -s -- --target claude --project-dir "$PWD"
```

Install both in one shot:

```bash
curl -fsSL https://raw.githubusercontent.com/0xAnton1/ansi-preview/main/scripts/install.sh | bash -s -- --target both --project-dir "$PWD"
```

## Why This Format Works

- fast first-look inspection
- often cheaper than HTML, SVG, or long prose for early thinking
- braille charts carry more curve detail per cell
- easy to paste into chats, issues, docs, and PRs
- strong bridge between plain text and richer UI work

## Use With Codex

Copy this repo's portable core into a skill directory:

```text
.codex/skills/ansi-preview/
├── SKILL.md
├── agents/openai.yaml
└── references/patterns.md
```

Good install targets:

- repo-local: `.codex/skills/ansi-preview`
- user-global: `~/.codex/skills/ansi-preview`
- scripted install: `scripts/install.sh --target codex`

## Use With Claude

This repo also includes:

- `CLAUDE.md` for project-level guidance
- `.claude/commands/ansi-preview.md` for a reusable slash command prompt

Useful install targets:

- repo-local `CLAUDE.md`
- repo-local `.claude/commands/ansi-preview.md`
- or copy the command text into your own Claude command library
- scripted install: `scripts/install.sh --target claude --project-dir /path/to/project`

Behavior note:

- the installer will not overwrite an existing project `CLAUDE.md`
- if one already exists, it writes `.claude/ansi-preview-reference.md` instead

## Gallery

### Smooth Braille Chart

```ansi
Metric 0.91 ┤                ⢀⣠⠴⠒⠉⠉⠓⢦⣀
       0.64 ┤          ⢀⡴⠋              ⠙⢦⡀
       0.37 ┤      ⢀⡴⠋                    ⠘⣆
       0.18 ┤  ⢀⡴⠃                        ⠘⣆
       0.05 ┼⠤⠋                            ⠈⠒
              step-1     step-2     step-3     step-4
```

### Series + Activity

```ansi
SERIES    ⢀⣠⠴⠒⠋⠉⠉⠓⢦⣀      level 0.64
ACTIVITY  ▂▃▅█▇▅▃▂▆█▆▄▂      load 1.8x
```

### Parallel System Flow

```ansi
Legend  ■ primary flow  ■ exploration flow  ■ aggregate outputs  ■ caution

                        CURRENT SYSTEM OVERVIEW

         PRIMARY PATH                                  EXPLORATION PATH
┌───────────────────────────────┐              ┌──────────────────────────────────────────┐
│ input bundle / live event     │              │ input bundle                             │
│ states, scores, tags, timing  │              │ states, scores, history, windows         │
└──────────────┬────────────────┘              └───────────────────┬──────────────────────┘
               │                                                   │
               ▼                                                   ▼
┌───────────────────────────────┐              ┌──────────────────────────────────────────┐
│ decision engine               │              │ summarize_state_trajectory()             │
│ pick leader                   │              │                                          │
│ score confidence / entry      │              │ per step computes:                       │
└──────────────┬────────────────┘              │ • center / spread                        │
               │                               │ • confidence gap                         │
               ▼                               │ • nearby support                         │
┌───────────────────────────────┐              │ • protected zone around center           │
│ routing layer                 │              └───────────────────┬──────────────────────┘
│ hold / refresh rules          │                                  │
│ exit if leader changes        │                                  ▼
└──────────────┬────────────────┘              ┌──────────────────────────────────────────┐
               │                               │ expand each step into candidate rows      │
               ▼                               │ row = moment × target                     │
┌───────────────────────────────┐              │                                          │
│ execution loop                │              │ per row stores:                          │
│ sort by entry score           │              │ • rank / priority                        │
│ final score = confidence      │              │ • role = center / nearby /               │
└──────────────┬────────────────┘              │   protected / outside                    │
               │                               │ • locked gain / locked risk              │
               ▼                               │ • change_1 / drift_1                     │
┌───────────────────────────────┐              └───────────────────┬──────────────────────┘
│ aggregate outputs             │                                  │
│ reports / alerts / logs       │                                  ▼
└───────────────────────────────┘              ┌──────────────────────────────────────────┐
                                               │ review tables / summary views            │
                                               │ compare patterns and refine rules        │
                                               └──────────────────────────────────────────┘
```

### Funny ANSI Cat

```ansi
 /\_/\\
( o.o )
 > ^ <
```

## Prompt Examples

- `Use $ansi-preview to show this as a smooth braille chart.`
- `Use $ansi-preview to show it as ANSI truecolor terminal chart with price and volume.`
- `Use $ansi-preview to sketch this UI in terminal first.`
- `Use $ansi-preview to map this flow with several boxes and a legend.`
- `Use $ansi-preview to compare these variants in one compact table.`

## Visual Language

### Chart Modes

- `braille raster`: dense or smooth series
- `block sparkline`: tiny summaries
- `half-block / quadrant`: simplified shape with more weight
- `box-drawing scaffold`: wireframes, flows, structural diagrams

### Legend Convention

- `primary flow`: green or main accent
- `exploration flow`: cyan
- `aggregate outputs`: blue
- `caution`: amber
- `neutral context`: gray

If color drops out, labels and geometry should still make the preview readable.

## Token Profile

Rough rule:

- ANSI is usually cheaper than HTML, SVG, or long prose for first-look visuals
- braille is especially efficient for smooth curves
- repeated truecolor escape sequences are the main token cost multiplier

Approximate output-token ranges:

| Preview type | Mono / low-color | Full truecolor |
|---|---:|---:|
| tiny sparkline or strip | 15-40 | 25-70 |
| smooth braille chart | 70-140 | 110-220 |
| series + activity stack | 30-80 | 50-120 |
| compact table or wireframe | 90-220 | 130-320 |
| parallel system flow | 260-500 | 380-700 |

These are general planning numbers, not exact tokenizer measurements.
Actual usage depends on terminal width, label length, and how aggressively color is applied.

## Compatibility

- best experience: truecolor terminal with braille and box-drawing support
- good fallback: 256-color terminal
- safe fallback: monochrome Unicode
- richer-than-Unicode terminal ask: Sixel or Kitty

## Publishing Notes

There is no special packaging step required for this repo to be useful.
The practical public distribution path is:

1. publish the repo on GitHub
2. keep the core skill files stable
3. show screenshots or SVG previews in `assets/`
4. document Codex and Claude install paths clearly

## What's Included

```text
ansi-preview/
├── SKILL.md
├── agents/openai.yaml
├── references/patterns.md
├── CLAUDE.md
├── .claude/commands/ansi-preview.md
├── scripts/install.sh
├── assets/ansi-preview-hero.svg
├── LICENSE
└── README.md
```

## What Is Still Missing

- PNG screenshots for richer GitHub previews
- a short GIF for the README hero section
- optional Windows-native installer

## License

MIT
