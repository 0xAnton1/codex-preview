#!/usr/bin/env python3
"""Render a dependency-free Codex Preview terminal or chat demo."""

from __future__ import annotations

import argparse
import sys

from preview import color_enabled, fit, paint, resolve_surface


INNER_WIDTH = 68
COLUMN_WIDTH = 22


def bar(percent: int, width: int = 20) -> str:
    filled = round(max(0, min(100, percent)) * width / 100)
    return f"{'█' * filled}{'░' * (width - filled)}"


def row(text: str = "", align: str = "left") -> str:
    return f"│{fit(text, INNER_WIDTH, align)}│"


def columns(values: tuple[tuple[str, str], ...], enabled: bool) -> str:
    cells = [paint(fit(text, COLUMN_WIDTH, "center"), tone, enabled) for text, tone in values]
    return f"│{'│'.join(cells)}│"


def render(enabled: bool, surface: str) -> str:
    top = f"┌{'─' * INNER_WIDTH}┐"
    rule = f"├{'─' * INNER_WIDTH}┤"
    column_rule = f"├{'─' * COLUMN_WIDTH}┼{'─' * COLUMN_WIDTH}┼{'─' * COLUMN_WIDTH}┤"
    bottom = f"└{'─' * INNER_WIDTH}┘"

    title = paint(fit("CODEX PREVIEW · TERMINAL UI", INNER_WIDTH, "center"), "bold", enabled)
    surface_label = "ANSI truecolor" if enabled else "Unicode / no ANSI"
    footer = f"surface: {surface}  ·  renderer: {surface_label}  ·  width: {INNER_WIDTH + 2} cols"

    return "\n".join(
        [
            top,
            f"│{title}│",
            row(f" Surface  {surface:<12} Mode  {'color' if enabled else 'portable':<12} Layout  fixed-width"),
            column_rule,
            columns((("SYSTEM", "gray"), ("RENDERER", "gray"), ("CHECKS", "gray")), enabled),
            columns((("● HEALTHY", "green"), ("● ACTIVE", "cyan"), ("▲ 1 WARNING", "amber")), enabled),
            rule,
            row(f" Load        {bar(64)}  64%"),
            row(f" Coverage    {bar(86)}  86%"),
            row(" Throughput  ▁▂▄▅▇█▇▆▄▃▅▆      128/min"),
            row(" Trend       ⢀⣠⠤⠒⠉⠉⠢⣄    ⣀⡠⠤⠒⠉     rising"),
            rule,
            row(footer, "center"),
            bottom,
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--surface",
        choices=("auto", "chat", "terminal"),
        default="auto",
        help="target output surface (default: auto)",
    )
    parser.add_argument(
        "--color",
        choices=("auto", "always", "never"),
        default="auto",
        help="ANSI color policy for terminal output (default: auto)",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    surface = resolve_surface(args.surface)
    print(render(color_enabled(args.color, surface), surface))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
