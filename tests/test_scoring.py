from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_ready.scoring import decision, load_assessment, render_markdown, score_assessment


class ReadinessScoringTests(unittest.TestCase):
    def test_sample_assessment_scores_as_controlled_pilot(self):
        data = load_assessment(ROOT / "examples" / "sample_assessment.json")
        result = score_assessment(data)
        self.assertEqual(result.decision, "Controlled pilot only")
        self.assertEqual(result.total, 42)
        self.assertEqual(result.max_total, 70)
        self.assertFalse(result.has_veto)
        self.assertIn("Audit log design is incomplete", result.top_gaps)

    def test_veto_overrides_score(self):
        self.assertEqual(decision(70, 70, True), "Do not proceed: veto item present")

    def test_markdown_report_contains_category_table(self):
        data = load_assessment(ROOT / "examples" / "sample_assessment.json")
        report = render_markdown(score_assessment(data))
        self.assertIn("## Category scores", report)
        self.assertIn("| business workflow and value |", report)


if __name__ == "__main__":
    unittest.main()
