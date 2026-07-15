from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_ready.cli import main
from ai_ready.scoring import decision, load_assessment, render_markdown, score_assessment, validate_assessment


class ReadinessScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_path = ROOT / "examples" / "sample_assessment.json"
        cls.sample = json.loads(cls.sample_path.read_text(encoding="utf-8"))

    def test_sample_assessment_scores_as_controlled_pilot(self):
        result = score_assessment(self.sample)
        self.assertEqual(result.decision, "Controlled pilot only")
        self.assertEqual((result.total, result.max_total), (42, 70))
        self.assertFalse(result.has_veto)

    def test_veto_overrides_score(self):
        self.assertEqual(decision(70, 70, True), "Do not proceed: veto item present")

    def test_markdown_report_contains_category_table_and_disclaimer(self):
        report = render_markdown(score_assessment(self.sample))
        self.assertIn("## Category scores", report)
        self.assertIn("| business workflow and value |", report)
        self.assertIn("decision-support heuristic", report)

    def test_rejects_missing_required_field(self):
        data = deepcopy(self.sample); data.pop("scores")
        with self.assertRaisesRegex(ValueError, "Missing required fields: scores"):
            validate_assessment(data)

    def test_rejects_empty_system_name(self):
        data = deepcopy(self.sample); data["system_name"] = "  "
        with self.assertRaisesRegex(ValueError, "system_name"):
            validate_assessment(data)

    def test_rejects_boolean_as_numeric_score(self):
        data = deepcopy(self.sample); data["scores"]["business_workflow_and_value"] = True
        with self.assertRaisesRegex(ValueError, "numeric, not boolean"):
            validate_assessment(data)

    def test_rejects_score_above_maximum(self):
        data = deepcopy(self.sample); data["scores"]["business_workflow_and_value"] = 11
        with self.assertRaisesRegex(ValueError, "score out of range"):
            validate_assessment(data)

    def test_rejects_non_boolean_veto(self):
        data = deepcopy(self.sample); data["veto_items"]["unauthorized_data_use"] = "false"
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            validate_assessment(data)

    def test_rejects_non_string_gap(self):
        data = deepcopy(self.sample); data["top_gaps"] = [7]
        with self.assertRaisesRegex(ValueError, "list of strings"):
            validate_assessment(data)

    def test_cli_validate_and_report(self):
        self.assertEqual(main(["validate", str(self.sample_path)]), 0)
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            self.assertEqual(main(["report", str(self.sample_path), "--output", str(report)]), 0)
            self.assertIn("# AI readiness report", report.read_text(encoding="utf-8"))

    def test_cli_returns_error_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            invalid = Path(tmp) / "invalid.json"; invalid.write_text("{", encoding="utf-8")
            with patch("sys.stderr"):
                self.assertEqual(main(["validate", str(invalid)]), 2)


if __name__ == "__main__":
    unittest.main()
