# ANSI Preview Patterns

Load this file only when the user wants a richer preview or the best visual form is not obvious.

## Smooth Chart Default

The smooth terminal chart style people usually mean is `braille raster`.
Use it for dense lines, curves, overlays, or price paths that should feel less jagged than block charts.
Reason: each cell behaves like a compact `2x4` dot canvas, so shape density is high for low token cost.

## Intent Map

- `graph the series`, `show the trend`, `plot the metric`, `make it smooth`, `use the curvy ansi style`: braille raster first; add an activity strip if a second magnitude matters.
- `show it as ANSI truecolor terminal chart with price and volume`: render that exact stacked price plus volume terminal preview.
- `show the funnel`, `compare stages`: stage bars with conversion deltas.
- `preview the dashboard`, `sketch the page`: box-drawing wireframe with panels and labels.
- `show the flow`, `map the logic`: flow chart with directional connectors.
- `show status over time`, `compare regimes`: lane chart or status bands.
- `compare variants`, `rank the runs`: aligned table with microbars, deltas, and highlights.

## Color Presets

- `semantic`: green/up, red/down, amber/warn, blue/info.
- `accent`: one calm highlight hue plus grayscale structure.
- `categorical`: small distinct palette for a few series.
- `heatmap`: ordered gradient for intensity or score.
- `mono`: no color dependency.

Publication default:
- charts: `semantic`
- UI wireframes: `accent`
- docs / unknown terminals: `mono` or very restrained `accent`

## Legend Convention

Keep legend order stable so screenshots and docs stay familiar:

- `primary`: green or the main accent; use for the main / live / default path
- `exploration`: cyan; use for alternate, research, or branch analysis paths
- `aggregate outputs`: blue; use for reports, summaries, dashboards, or exported views
- `caution`: amber; use for warnings, fallbacks, blockers, or review points
- `neutral`: gray; use for context, scaffolding, or inactive states

If color is unavailable:
- keep the legend labels in the same order
- keep box shapes and spacing unchanged
- let labels carry the meaning instead of color alone

## Compact Templates

### Braille Line Chart

```ansi
Metric 0.91 ┤        ⢀⣠⠤⠒⠉⠉⠢⣄
       0.64 ┤    ⢀⡴⠋          ⠘⢦⡀
       0.37 ┤ ⢀⡴⠃              ⠘⣆
       0.10 ┼⠤⠋                  ⠈⠒
              t0                   tN
```

### UI Wireframe

```ansi
┌──────────────────────── App Shell ────────────────────────┐
│ Header                                                    │
├───────────────┬───────────────────────────┬───────────────┤
│ Left Nav      │ Main Chart / Table        │ Side Panel    │
│ filters       │ primary content           │ detail / logs │
├───────────────┴───────────────────────────┴───────────────┤
│ Footer / status strip                                      │
└────────────────────────────────────────────────────────────┘
```

### Flow Chart

```ansi
[Input] -> [Parse] -> [Score] -> [Decide] -> [Render]
                 \-> [Warn / fallback]
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

### Comparison Table

```ansi
Variant      Score   Delta   Preview
baseline     0.42    --      ████
candidate-a  0.57   +0.15    ██████
candidate-b  0.49   +0.07    █████
```

### Series + Activity Stack

```ansi
SERIES    ⣀⣠⣤⣶⣾⣷⣶⣤⣀
ACTIVITY  ▂▃▅█▇▃▂▆█▅▃▂
```

### Funny Cat

```ansi
 /\_/\\
( o.o )
 > ^ <
```

## Efficiency Rules

- Use one preview that answers the question directly.
- Prefer braille raster over wide charts when the goal is smoothness with low token spend.
- Bucket dense data before plotting.
- Abbreviate labels before shrinking the chart body.
- Avoid full borders if spacing alone keeps the structure readable.
- Reserve truecolor gradients for cases where value density matters.
- If sharing externally, make sure the preview still reads in plain text with color stripped.

## Escalate Beyond ANSI When Needed

- Use HTML, SVG, or React if the user wants a build-ready UI artifact.
- Use Mermaid when the user explicitly wants Mermaid syntax.
- Use Sixel/Kitty when the user wants richer graphics but still inside the terminal.
