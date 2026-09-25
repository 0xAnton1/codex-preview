# Deterministic Renderer

Use `scripts/preview.py` when the request includes numeric, tabular, categorical-state, or sequential data. It uses only the Python standard library and produces chat-safe Unicode or terminal ANSI from the same inputs.

Keep global options before the subcommand:

```text
python scripts/preview.py [--surface auto|chat|terminal] [--color auto|always|never] [--width 40..160] MODE MODE_OPTIONS
```

## Modes

### Braille line

Inline values:

```powershell
python scripts/preview.py --surface chat --width 70 line --title "Latency" --values "10,12,11,18,14,,20,24,21"
```

From JSON or CSV records:

```powershell
python scripts/preview.py line --input metrics.csv --column latency_ms --height 6
```

Blank, `null`, `none`, `na`, `n/a`, `nan`, and `-` values create visible gaps. The renderer preserves endpoints and draws every finite source point, including multiple points mapped into the same terminal column.

### Comparison bars

```powershell
python scripts/preview.py --surface chat bars --title "P&L" --items "Alpha=42,Beta=-17,Gamma=28"
python scripts/preview.py bars --input results.csv --label-column name --value-column score
```

Mixed-sign bars share a zero axis. Positive and negative magnitudes are scaled independently so both remain visible.

### Table

```powershell
python scripts/preview.py --width 80 table --input results.csv --columns "name,score,status" --limit 15
```

Table input is either CSV, a JSON array of objects, or a JSON object of equally shaped column lists. Long cells are truncated with an ellipsis and numeric values are right-aligned.

### State lanes

```powershell
python scripts/preview.py lanes --items "API=ok,ok,warn,ok;DB=ok,warn,fail,ok"
python scripts/preview.py lanes --input states.json
```

JSON lane input is an object whose values are state lists. Recognized states include `ok`, `healthy`, `up`, `warn`, `degraded`, `fail`, `down`, `idle`, `missing`, and `unknown`. Longer histories are sampled while preserving the first and final states.

### Sequential flow

```powershell
python scripts/preview.py --width 60 flow --steps "Ingest,Validate,Transform,Score,Publish"
python scripts/preview.py flow --input flow.json
```

Flow JSON is a list of step names or an object with a `steps` list. Long flows wrap with a continuation marker.

## Surface Rules

- `--surface chat` never emits ANSI, even with `--color always`.
- `--surface terminal` may emit ANSI according to `--color` and `NO_COLOR`.
- `--surface auto` chooses terminal only when standard output is a TTY.
- Use `--width` to match the target surface. The renderer validates widths from 40 to 160 terminal cells.

If structured input does not fit these shapes, transform it explicitly and state the transformation. Do not silently replace missing values, units, or labels.
