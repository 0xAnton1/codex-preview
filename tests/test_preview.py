from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

import sys

sys.path.insert(0, str(SCRIPTS))

import preview
import demo


class PreviewTests(unittest.TestCase):
    def test_demo_is_fixed_width(self) -> None:
        rendered = demo.render(False, "chat")
        widths = {preview.display_width(line) for line in rendered.splitlines()}
        self.assertEqual(widths, {70})
        self.assertIn("▁▂▄▅▇█▇▆▄▃▅▆", rendered)
        self.assertNotIn("⢀⣠", rendered)

    def test_fit_respects_wide_characters(self) -> None:
        rendered = preview.fit("A界B", 5)
        self.assertEqual(preview.display_width(rendered), 5)
        self.assertEqual(rendered, "A界B ")

    def test_fit_uses_available_space_when_truncating(self) -> None:
        self.assertEqual(preview.fit("abcdefghij", 5), "abcd…")

    def test_chat_never_enables_ansi(self) -> None:
        self.assertFalse(preview.color_enabled("always", "chat"))

    def test_braille_plot_has_fixed_dimensions_and_gaps(self) -> None:
        rendered = preview.braille_plot([0, None, 1], cells=12, rows=4)
        self.assertEqual(len(rendered), 4)
        self.assertTrue(all(preview.display_width(line) == 12 for line in rendered))
        self.assertNotIn("⣿", "".join(rendered))

    def test_line_preserves_declared_width(self) -> None:
        rendered = preview.render_line([1, 3, 2, None, 5], 60, 4, "", False)
        chart_lines = rendered.splitlines()[1:5]
        self.assertTrue(all(preview.display_width(line) == 60 for line in chart_lines))
        self.assertIn("gaps represent unavailable values", rendered)

    def test_mixed_bars_have_equal_width_and_axis(self) -> None:
        rendered = preview.render_bars([("gain", 12), ("loss", -5)], 60, "", False)
        lines = rendered.splitlines()
        self.assertTrue(all(preview.display_width(line) == 60 for line in lines))
        self.assertTrue(all("│" in line for line in lines))

    def test_extreme_mixed_bars_keep_both_sides_of_zero(self) -> None:
        rendered = preview.render_bars([("gain", 1), ("loss", -1_000_000)], 50, "", False)
        gain, loss = rendered.splitlines()
        self.assertIn("│█", gain)
        self.assertIn("█│", loss)

    def test_table_truncates_and_aligns(self) -> None:
        rows = [
            {"name": "a-very-long-service-name", "latency": 12.4, "status": "healthy"},
            {"name": "api", "latency": 8.2, "status": "warning"},
        ]
        rendered = preview.render_table(rows, ["name", "latency", "status"], 40, "", False)
        widths = {preview.display_width(line) for line in rendered.splitlines()}
        self.assertEqual(widths, {40})
        self.assertIn("…", rendered)

    def test_lanes_preserve_first_and_last_state_when_sampled(self) -> None:
        lanes = {"api": ["fail"] + ["ok"] * 30 + ["warn"]}
        lines = preview.render_lanes(lanes, 40, "", False).splitlines()
        track = lines[0].split("│", 1)[1]
        self.assertIn("×", track)
        self.assertIn("▓", track)
        self.assertTrue(all(preview.display_width(line) <= 40 for line in lines))

    def test_flow_wraps_with_continuation_marker(self) -> None:
        rendered = preview.render_flow(
            ["ingest", "validate", "transform", "score", "publish"], 35, "", False
        )
        self.assertIn("↳", rendered)
        self.assertTrue(all(preview.display_width(line) <= 35 for line in rendered.splitlines()))

    def test_flow_truncates_single_oversized_step(self) -> None:
        rendered = preview.render_flow(["x" * 100], 40, "", False)
        self.assertLessEqual(preview.display_width(rendered), 40)
        self.assertIn("…", rendered)

    def test_load_json_and_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            json_path = directory / "values.json"
            csv_path = directory / "values.csv"
            json_path.write_text(json.dumps({"series": [1, 2, None, 4]}), encoding="utf-8")
            csv_path.write_text("name,value\na,1\nb,2\n", encoding="utf-8")

            values, _ = preview.values_from_document(preview.load_document(str(json_path)), "series")
            records = preview.records_from_document(
                preview.load_document(str(csv_path)), "name", "value"
            )

        self.assertEqual(values, [1.0, 2.0, None, 4.0])
        self.assertEqual(records, [("a", 1.0), ("b", 2.0)])


if __name__ == "__main__":
    unittest.main()
