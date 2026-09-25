#!/usr/bin/env python3
"""Render deterministic terminal-first previews from structured data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Sequence


RESET = "\x1b[0m"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
PALETTE = {
    "cyan": "\x1b[38;2;34;211;238m",
    "green": "\x1b[38;2;52;211;153m",
    "red": "\x1b[38;2;248;113;113m",
    "amber": "\x1b[38;2;251;191;36m",
    "gray": "\x1b[38;2;148;163;184m",
    "bold": "\x1b[1m",
}
BRAILLE_BITS = ((1, 8), (2, 16), (4, 32), (64, 128))
MISSING = {"", "-", "na", "n/a", "none", "null", "nan"}


def display_width(text: str) -> int:
    """Return terminal-cell width after removing ANSI styling."""
    width = 0
    for character in ANSI_RE.sub("", str(text)):
        if unicodedata.combining(character):
            continue
        width += 2 if unicodedata.east_asian_width(character) in {"W", "F"} else 1
    return width


def fit(text: Any, width: int, align: str = "left") -> str:
    """Truncate and pad unstyled text to an exact terminal-cell width."""
    value = str(text)
    kept: list[str] = []
    used = 0
    truncated = False
    for character in value:
        character_width = display_width(character)
        if used + character_width > width:
            truncated = True
            break
        kept.append(character)
        used += character_width

    if truncated and width > 0:
        while kept and used + 1 > width:
            removed = kept.pop()
            used -= display_width(removed)
        kept.append("…")
        used += 1

    rendered = "".join(kept)
    padding = " " * max(0, width - used)
    if align == "right":
        return f"{padding}{rendered}"
    if align == "center":
        left = len(padding) // 2
        return f"{padding[:left]}{rendered}{padding[left:]}"
    return f"{rendered}{padding}"


def paint(text: str, tone: str, enabled: bool) -> str:
    return f"{PALETTE[tone]}{text}{RESET}" if enabled else text


def resolve_surface(surface: str) -> str:
    if surface != "auto":
        return surface
    return "terminal" if sys.stdout.isatty() else "chat"


def color_enabled(mode: str, surface: str) -> bool:
    if surface == "chat" or mode == "never" or os.environ.get("NO_COLOR") is not None:
        return False
    return mode == "always" or sys.stdout.isatty()


def parse_number(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        number = float(value)
        return number if math.isfinite(number) else None
    text = str(value).strip()
    if text.lower() in MISSING:
        return None
    try:
        number = float(text.replace(",", ""))
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def format_number(value: float) -> str:
    magnitude = abs(value)
    if magnitude >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if magnitude >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if magnitude >= 1_000:
        return f"{value / 1_000:.2f}K"
    if magnitude >= 100:
        return f"{value:.0f}"
    if magnitude >= 10:
        return f"{value:.1f}"
    return f"{value:.2f}"


def parse_csv_values(text: str) -> list[float | None]:
    return [parse_number(part) for part in text.split(",")]


def load_document(path: str) -> Any:
    source = Path(path)
    if source.suffix.lower() == ".json":
        return json.loads(source.read_text(encoding="utf-8"))
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def choose_numeric_column(rows: Sequence[dict[str, Any]], requested: str | None) -> str:
    if not rows:
        raise ValueError("input contains no rows")
    if requested:
        if requested not in rows[0]:
            raise ValueError(f"column not found: {requested}")
        return requested
    for column in rows[0]:
        values = [parse_number(row.get(column)) for row in rows]
        if any(value is not None for value in values):
            return column
    raise ValueError("input contains no numeric column")


def values_from_document(document: Any, column: str | None) -> tuple[list[float | None], list[str]]:
    if isinstance(document, list) and all(not isinstance(item, dict) for item in document):
        return [parse_number(item) for item in document], []
    if isinstance(document, list) and all(isinstance(item, dict) for item in document):
        rows = document
        selected = choose_numeric_column(rows, column)
        labels = [str(row.get(next(iter(row)), "")) for row in rows]
        return [parse_number(row.get(selected)) for row in rows], labels
    if isinstance(document, dict):
        selected = column or next((key for key, value in document.items() if isinstance(value, list)), None)
        if selected is None or selected not in document or not isinstance(document[selected], list):
            raise ValueError("JSON object needs a list-valued column")
        return [parse_number(item) for item in document[selected]], []
    raise ValueError("unsupported input shape")


def bresenham(x0: int, y0: int, x1: int, y1: int) -> Iterable[tuple[int, int]]:
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy
    while True:
        yield x0, y0
        if x0 == x1 and y0 == y1:
            return
        twice = 2 * error
        if twice >= dy:
            error += dy
            x0 += sx
        if twice <= dx:
            error += dx
            y0 += sy


def braille_plot(values: Sequence[float | None], cells: int, rows: int) -> list[str]:
    if cells < 2 or rows < 1:
        raise ValueError("plot dimensions are too small")
    finite = [value for value in values if value is not None]
    if not finite:
        raise ValueError("series contains no finite values")

    low, high = min(finite), max(finite)
    pixel_width, pixel_height = cells * 2, rows * 4
    dots: set[tuple[int, int]] = set()
    previous: tuple[int, int] | None = None

    for index, value in enumerate(values):
        if value is None:
            previous = None
            continue
        x = 0 if len(values) == 1 else round(index * (pixel_width - 1) / (len(values) - 1))
        ratio = 0.5 if high == low else (value - low) / (high - low)
        y = round((1 - ratio) * (pixel_height - 1))
        point = (x, y)
        if previous is None:
            dots.add(point)
        else:
            dots.update(bresenham(*previous, *point))
        previous = point

    rendered: list[str] = []
    for cell_y in range(rows):
        line: list[str] = []
        for cell_x in range(cells):
            bits = 0
            for dot_y in range(4):
                for dot_x in range(2):
                    if (cell_x * 2 + dot_x, cell_y * 4 + dot_y) in dots:
                        bits |= BRAILLE_BITS[dot_y][dot_x]
            line.append(chr(0x2800 + bits) if bits else " ")
        rendered.append("".join(line))
    return rendered


def render_line(
    values: Sequence[float | None], width: int, height: int, title: str, enabled: bool
) -> str:
    finite = [value for value in values if value is not None]
    if not finite:
        raise ValueError("series contains no finite values")
    label_width = max(len(format_number(min(finite))), len(format_number(max(finite))), 5)
    plot_width = width - label_width - 2
    if plot_width < 12:
        raise ValueError("width is too small for a line chart")
    plot = braille_plot(values, plot_width, height)

    lines = [paint(fit(title, width), "bold", enabled)] if title else []
    lines.append(f"range {format_number(min(finite))} → {format_number(max(finite))}  n={len(values)}")
    for index, graph_line in enumerate(plot):
        label = format_number(max(finite)) if index == 0 else format_number(min(finite)) if index == height - 1 else ""
        axis = "┤" if index < height - 1 else "┼"
        lines.append(f"{fit(label, label_width, 'right')} {axis}{paint(graph_line, 'cyan', enabled)}")
    if any(value is None for value in values):
        lines.append(paint("gaps represent unavailable values", "gray", enabled))
    return "\n".join(lines)


def records_from_document(document: Any, label_column: str | None, value_column: str | None) -> list[tuple[str, float]]:
    if isinstance(document, dict):
        records = []
        for label, value in document.items():
            number = parse_number(value)
            if number is not None:
                records.append((str(label), number))
        return records
    if isinstance(document, list) and all(isinstance(item, dict) for item in document):
        rows: list[dict[str, Any]] = document
        selected_value = choose_numeric_column(rows, value_column)
        selected_label = label_column or next((key for key in rows[0] if key != selected_value), selected_value)
        records = []
        for row in rows:
            value = parse_number(row.get(selected_value))
            if value is not None:
                records.append((str(row.get(selected_label, "")), value))
        return records
    raise ValueError("bars need a JSON object or tabular records")


def parse_items(text: str) -> list[tuple[str, float]]:
    records = []
    for item in text.split(","):
        if "=" not in item:
            raise ValueError("bar items must use label=value")
        label, raw_value = item.split("=", 1)
        value = parse_number(raw_value)
        if value is None:
            continue
        records.append((label.strip(), value))
    return records


def render_bars(records: Sequence[tuple[str, float]], width: int, title: str, enabled: bool) -> str:
    if not records:
        raise ValueError("no bar records to render")
    label_width = min(max(display_width(label) for label, _ in records), max(8, width // 3))
    value_width = max(len(format_number(value)) for _, value in records)
    bar_width = width - label_width - value_width - 5
    if bar_width < 10:
        raise ValueError("width is too small for bars")

    minimum = min(value for _, value in records)
    maximum = max(value for _, value in records)
    negative_width = 0
    if minimum < 0 < maximum:
        negative_width = min(
            bar_width - 1,
            max(1, round(bar_width * abs(minimum) / (abs(minimum) + maximum))),
        )
    elif maximum <= 0:
        negative_width = bar_width
    positive_width = bar_width - negative_width
    negative_scale = abs(minimum) if minimum < 0 else 1
    positive_scale = maximum if maximum > 0 else 1

    lines = [paint(fit(title, width), "bold", enabled)] if title else []
    for label, value in records:
        if value < 0:
            filled = round(abs(value) / negative_scale * negative_width)
            body = f"{'░' * (negative_width - filled)}{'█' * filled}│{' ' * positive_width}"
            tone = "red"
        else:
            filled = round(value / positive_scale * positive_width)
            body = f"{' ' * negative_width}│{'█' * filled}{'░' * (positive_width - filled)}"
            tone = "green"
        lines.append(
            f"{fit(label, label_width)}  {paint(body, tone, enabled)}  {fit(format_number(value), value_width, 'right')}"
        )
    return "\n".join(lines)


def table_rows(document: Any) -> list[dict[str, Any]]:
    if isinstance(document, list) and all(isinstance(item, dict) for item in document):
        return list(document)
    if isinstance(document, dict):
        keys = list(document)
        if keys and all(isinstance(document[key], list) for key in keys):
            length = max(len(document[key]) for key in keys)
            return [{key: document[key][index] if index < len(document[key]) else "" for key in keys} for index in range(length)]
    raise ValueError("table input needs records or a JSON object of columns")


def allocate_columns(rows: Sequence[dict[str, Any]], columns: Sequence[str], width: int) -> list[int]:
    natural = [max(display_width(column), *(display_width(row.get(column, "")) for row in rows)) for column in columns]
    available = width - 3 * (len(columns) - 1)
    if available < len(columns) * 3:
        raise ValueError("width is too small for the selected columns")
    sizes = [min(value, max(8, available // len(columns))) for value in natural]
    while sum(sizes) > available:
        index = max(range(len(sizes)), key=sizes.__getitem__)
        sizes[index] -= 1
    while sum(sizes) < available:
        candidates = [index for index, size in enumerate(sizes) if size < natural[index]]
        index = candidates[0] if candidates else max(range(len(sizes)), key=lambda item: natural[item])
        sizes[index] += 1
    return sizes


def render_table(rows: Sequence[dict[str, Any]], columns: Sequence[str], width: int, title: str, enabled: bool) -> str:
    if not rows:
        raise ValueError("table contains no rows")
    if not columns:
        columns = list(rows[0])
    missing = [column for column in columns if column not in rows[0]]
    if missing:
        raise ValueError(f"columns not found: {', '.join(missing)}")
    sizes = allocate_columns(rows, columns, width)

    def formatted(values: Sequence[Any], header: bool = False) -> str:
        cells = []
        for value, size in zip(values, sizes):
            align = "left" if header or parse_number(value) is None else "right"
            cells.append(fit(value, size, align))
        return " │ ".join(cells)

    lines = [paint(fit(title, width), "bold", enabled)] if title else []
    lines.append(paint(formatted(columns, True), "bold", enabled))
    lines.append("─┼─".join("─" * size for size in sizes))
    lines.extend(formatted([row.get(column, "") for column in columns]) for row in rows)
    return "\n".join(lines)


STATE_SYMBOLS = {
    "ok": "█",
    "healthy": "█",
    "up": "█",
    "warn": "▓",
    "warning": "▓",
    "degraded": "▓",
    "fail": "×",
    "failed": "×",
    "down": "×",
    "idle": "·",
    "off": "·",
    "missing": "?",
    "unknown": "?",
}


def parse_lanes(text: str) -> dict[str, list[str]]:
    lanes: dict[str, list[str]] = {}
    for lane in text.split(";"):
        if "=" not in lane:
            raise ValueError("lanes must use name=state,state;name=state,state")
        label, states = lane.split("=", 1)
        lanes[label.strip()] = [state.strip() for state in states.split(",")]
    return lanes


def lanes_from_document(document: Any) -> dict[str, list[str]]:
    if not isinstance(document, dict) or not all(isinstance(value, list) for value in document.values()):
        raise ValueError("lane input needs a JSON object of state lists")
    return {str(key): [str(item) for item in value] for key, value in document.items()}


def render_lanes(lanes: dict[str, list[str]], width: int, title: str, enabled: bool) -> str:
    if not lanes:
        raise ValueError("no lanes to render")
    label_width = min(max(display_width(label) for label in lanes), max(8, width // 3))
    track_width = width - label_width - 3
    if track_width < 8:
        raise ValueError("width is too small for lanes")
    lines = [paint(fit(title, width), "bold", enabled)] if title else []
    for label, states in lanes.items():
        symbols = [STATE_SYMBOLS.get(state.lower(), "?") for state in states]
        if len(symbols) > track_width:
            symbols = [
                symbols[round(index * (len(symbols) - 1) / (track_width - 1))]
                for index in range(track_width)
            ]
        track = "".join(symbols)
        lines.append(f"{fit(label, label_width)} │ {fit(track, track_width)}")
    legend_entries = ["█ ok", "▓ warning", "× failed", "· idle", "? unknown"]
    legend_line = ""
    for entry in legend_entries:
        addition = entry if not legend_line else f"  {entry}"
        if legend_line and display_width(legend_line + addition) > width:
            lines.append(paint(legend_line, "gray", enabled))
            legend_line = entry
        else:
            legend_line += addition
    lines.append(paint(legend_line, "gray", enabled))
    return "\n".join(lines)


def flow_steps(document: Any) -> list[str]:
    if isinstance(document, list):
        return [str(item) for item in document]
    if isinstance(document, dict) and isinstance(document.get("steps"), list):
        return [str(item) for item in document["steps"]]
    raise ValueError("flow input needs a JSON list or a steps list")


def render_flow(steps: Sequence[str], width: int, title: str, enabled: bool) -> str:
    if not steps:
        raise ValueError("flow contains no steps")
    tokens = [f"[{fit(step, max(1, width - 6)).rstrip()}]" for step in steps]
    lines: list[str] = [paint(fit(title, width), "bold", enabled)] if title else []
    current = ""
    for token in tokens:
        addition = token if not current else f" → {token}"
        if current and display_width(current + addition) > width:
            lines.append(current)
            current = f"  ↳ {token}"
        else:
            current += addition
    lines.append(current)
    return "\n".join(lines)


def add_shared_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--input", help="JSON or CSV input file")
    parser.add_argument("--title", default="", help="optional preview title")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", choices=("auto", "chat", "terminal"), default="auto")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto")
    parser.add_argument("--width", type=int, default=70, help="output width, 40-160 cells")
    subparsers = parser.add_subparsers(dest="command", required=True)

    line = subparsers.add_parser("line", help="render a braille line chart")
    add_shared_arguments(line)
    line.add_argument("--values", help="comma-separated values; blank/null values create gaps")
    line.add_argument("--column", help="numeric column for JSON/CSV records")
    line.add_argument("--height", type=int, default=6, help="chart height, 2-16 rows")

    bars = subparsers.add_parser("bars", help="render comparison bars")
    add_shared_arguments(bars)
    bars.add_argument("--items", help="comma-separated label=value items")
    bars.add_argument("--label-column")
    bars.add_argument("--value-column")

    table = subparsers.add_parser("table", help="render JSON/CSV records as a table")
    add_shared_arguments(table)
    table.add_argument("--columns", help="comma-separated columns; defaults to all")
    table.add_argument("--limit", type=int, default=20)

    lanes = subparsers.add_parser("lanes", help="render categorical states over time")
    add_shared_arguments(lanes)
    lanes.add_argument("--items", help="name=state,state;name=state,state")

    flow = subparsers.add_parser("flow", help="render a compact sequential flow")
    add_shared_arguments(flow)
    flow.add_argument("--steps", help="comma-separated step labels")
    return parser


def render_from_args(args: argparse.Namespace) -> str:
    if not 40 <= args.width <= 160:
        raise ValueError("width must be between 40 and 160 cells")
    surface = resolve_surface(args.surface)
    enabled = color_enabled(args.color, surface)

    if args.command == "line":
        if not 2 <= args.height <= 16:
            raise ValueError("height must be between 2 and 16 rows")
        if args.values is not None:
            values = parse_csv_values(args.values)
        elif args.input:
            values, _ = values_from_document(load_document(args.input), args.column)
        else:
            raise ValueError("line requires --values or --input")
        return render_line(values, args.width, args.height, args.title, enabled)

    if args.command == "bars":
        if args.items:
            records = parse_items(args.items)
        elif args.input:
            records = records_from_document(load_document(args.input), args.label_column, args.value_column)
        else:
            raise ValueError("bars requires --items or --input")
        return render_bars(records, args.width, args.title, enabled)

    if args.command == "table":
        if not args.input:
            raise ValueError("table requires --input")
        if not 1 <= args.limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")
        rows = table_rows(load_document(args.input))[: args.limit]
        columns = [column.strip() for column in args.columns.split(",")] if args.columns else []
        return render_table(rows, columns, args.width, args.title, enabled)

    if args.command == "lanes":
        if args.items:
            lanes = parse_lanes(args.items)
        elif args.input:
            lanes = lanes_from_document(load_document(args.input))
        else:
            raise ValueError("lanes requires --items or --input")
        return render_lanes(lanes, args.width, args.title, enabled)

    if args.command == "flow":
        if args.steps:
            steps = [step.strip() for step in args.steps.split(",")]
        elif args.input:
            steps = flow_steps(load_document(args.input))
        else:
            raise ValueError("flow requires --steps or --input")
        return render_flow(steps, args.width, args.title, enabled)

    raise ValueError(f"unknown command: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        print(render_from_args(args))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
