from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_ready.cli import main
from ai_ready.scoring import (
    decision,
    load_assessment,
    migrate_assessment,
    render_html,
    render_json,
    render_markdown,
    score_assessment,
    validate_assessment,
)


class ReadinessScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_path = ROOT / "examples" / "sample_assessment.json"
        cls.sample = json.loads(cls.sample_path.read_text(encoding="utf-8"))

    def test_sample_assessment_scores_as_controlled_pilot(self):
        self.assertEqual(self.sample.get("schema_version"), "0.6")
        result = score_assessment(self.sample)
        self.assertEqual(result.decision, "Controlled pilot only")
        self.assertEqual((result.total, result.max_total), (42, 70))
        self.assertFalse(result.has_veto)

    def test_all_fictional_assessment_examples_validate(self):
        paths = sorted((ROOT / "examples").glob("*.json"))
        self.assertGreaterEqual(len(paths), 4)
        for path in paths:
            with self.subTest(path=path.name):
                validate_assessment(json.loads(path.read_text(encoding="utf-8")))

    def test_veto_overrides_score(self):
        self.assertEqual(decision(70, 70, True), "Do not proceed: veto item present")

    def test_public_decision_api_rejects_non_finite_inputs(self):
        for total, maximum in ((float("nan"), 70), (float("inf"), 70), (70, float("inf"))):
            with self.subTest(total=total, maximum=maximum):
                with self.assertRaisesRegex(ValueError, "finite"):
                    decision(total, maximum, False)

    def test_public_decision_api_requires_boolean_veto_flag(self):
        for value in ("false", 0, 1, None):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "boolean"):
                    decision(42, 70, value)

    def test_markdown_report_contains_category_table_and_disclaimer(self):
        report = render_markdown(score_assessment(self.sample))
        self.assertIn("## Category scores", report)
        self.assertIn("| business workflow and value |", report)
        self.assertIn("decision-support heuristic", report)

    def test_html_report_is_accessible_static_and_escapes_untrusted_text(self):
        data = deepcopy(self.sample)
        data["system_name"] = "<script>alert('x')</script>"
        report = render_html(score_assessment(data))
        self.assertIn('<html lang="en">', report)
        self.assertIn("<table", report)
        self.assertIn('aria-label="business workflow and value: 70.0%"', report)
        self.assertIn("&lt;script&gt;", report)
        self.assertNotIn("<script>", report)

    def test_rejects_missing_required_field(self):
        data = deepcopy(self.sample); data.pop("scores")
        with self.assertRaisesRegex(ValueError, "Missing required fields: scores"):
            validate_assessment(data)

    def test_v06_requires_explicit_schema_version(self):
        data = deepcopy(self.sample)
        data.pop("schema_version", None)
        with self.assertRaisesRegex(ValueError, "Missing required fields: schema_version"):
            validate_assessment(data)

    def test_migrates_legacy_v05_without_mutating_source(self):
        legacy = deepcopy(self.sample)
        legacy.pop("schema_version")
        migrated = migrate_assessment(legacy)
        self.assertNotIn("schema_version", legacy)
        self.assertEqual(migrated["schema_version"], "0.6")
        validate_assessment(migrated)

    def test_migration_rejects_unknown_version(self):
        for version in ("9.9", None):
            with self.subTest(version=version):
                data = deepcopy(self.sample)
                data["schema_version"] = version
                with self.assertRaisesRegex(ValueError, "unsupported schema_version"):
                    migrate_assessment(data)

    def test_rejects_empty_system_name(self):
        data = deepcopy(self.sample); data["system_name"] = "  "
        with self.assertRaisesRegex(ValueError, "system_name"):
            validate_assessment(data)

    def test_rejects_null_stage_like_the_public_schema(self):
        data = deepcopy(self.sample); data["stage"] = None
        with self.assertRaisesRegex(ValueError, "stage"):
            validate_assessment(data)

    def test_loads_assessment_with_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bom_assessment.json"
            payload = json.dumps(self.sample, ensure_ascii=False, indent=2)
            path.write_bytes(b"\xef\xbb\xbf" + payload.encode("utf-8"))
            result = score_assessment(load_assessment(path))
            self.assertEqual((result.total, result.max_total), (42, 70))

    def test_decision_tier_boundaries_are_stable(self):
        for total, expected in (
            (25, "Demo only"),
            (26, "Controlled pilot only"),
            (45, "Controlled pilot only"),
            (46, "Small production trial with monitoring"),
            (60, "Small production trial with monitoring"),
            (61, "Stronger production readiness, still check controls"),
        ):
            with self.subTest(total=total):
                self.assertEqual(decision(total, 70, False), expected)

    def test_rejects_boolean_as_numeric_score(self):
        data = deepcopy(self.sample); data["scores"]["business_workflow_and_value"] = True
        with self.assertRaisesRegex(ValueError, "numeric, not boolean"):
            validate_assessment(data)

    def test_rejects_string_and_non_finite_scores(self):
        for value in ("7", "NaN", float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                data = deepcopy(self.sample)
                data["scores"]["business_workflow_and_value"] = value
                with self.assertRaisesRegex(ValueError, "JSON number|finite"):
                    validate_assessment(data)

    def test_rejects_unknown_root_field(self):
        data = deepcopy(self.sample)
        data["unexpected"] = "not allowed by the public schema"
        with self.assertRaisesRegex(ValueError, "Unknown root fields: unexpected"):
            validate_assessment(data)

    def test_rejects_score_above_maximum(self):
        data = deepcopy(self.sample); data["scores"]["business_workflow_and_value"] = 11
        with self.assertRaisesRegex(ValueError, "score out of range"):
            validate_assessment(data)

    def test_rejects_noncanonical_score_dimensions(self):
        data = deepcopy(self.sample)
        data["scores"] = {"anything": 1}
        data["max_scores"] = {"anything": 1}
        with self.assertRaisesRegex(ValueError, "canonical score dimensions"):
            validate_assessment(data)

    def test_rejects_changed_canonical_maximum(self):
        data = deepcopy(self.sample)
        data["max_scores"]["business_workflow_and_value"] = 1
        with self.assertRaisesRegex(ValueError, "canonical maximum"):
            validate_assessment(data)

    def test_requires_complete_canonical_veto_set(self):
        data = deepcopy(self.sample)
        data["veto_items"].pop("unauthorized_data_use")
        with self.assertRaisesRegex(ValueError, "canonical veto items"):
            validate_assessment(data)

    def test_requires_dimension_evidence(self):
        data = deepcopy(self.sample)
        data.pop("evidence", None)
        with self.assertRaisesRegex(ValueError, "evidence"):
            validate_assessment(data)

    def test_requires_declared_human_review_metadata(self):
        data = deepcopy(self.sample)
        data.pop("review", None)
        with self.assertRaisesRegex(ValueError, "review"):
            validate_assessment(data)

    def test_review_date_requires_exact_calendar_date_syntax(self):
        for value in ("20260715", "2026-W29-2", "2026-02-30"):
            with self.subTest(value=value):
                data = deepcopy(self.sample)
                data["review"]["reviewed_at"] = value
                with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                    validate_assessment(data)

    def test_review_object_rejects_unknown_fields(self):
        data = deepcopy(self.sample)
        data["review"]["unexpected_attestation"] = "not defined by the public schema"
        with self.assertRaisesRegex(ValueError, "review fields"):
            validate_assessment(data)
        legacy = deepcopy(data)
        legacy.pop("schema_version")
        with self.assertRaisesRegex(ValueError, "review fields"):
            migrate_assessment(legacy)

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

    def test_cli_generates_static_html_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.html"
            self.assertEqual(
                main(["report", str(self.sample_path), "--format", "html", "--output", str(report)]),
                0,
            )
            text = report.read_text(encoding="utf-8")
            self.assertIn('<html lang="en">', text)
            self.assertNotIn("<script>", text)

    def test_cli_migrates_legacy_v05_to_new_file(self):
        legacy = deepcopy(self.sample)
        legacy.pop("schema_version")
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "legacy.json"
            output = Path(tmp) / "v06.json"
            source.write_text(json.dumps(legacy), encoding="utf-8")
            self.assertEqual(main(["migrate", str(source), "--output", str(output)]), 0)
            migrated = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(migrated["schema_version"], "0.6")
            validate_assessment(migrated)

    def test_cli_migrate_refuses_existing_output(self):
        legacy = deepcopy(self.sample)
        legacy.pop("schema_version")
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "legacy.json"
            output = Path(tmp) / "existing.json"
            source.write_text(json.dumps(legacy), encoding="utf-8")
            output.write_text("keep", encoding="utf-8")
            with patch("sys.stderr"):
                self.assertEqual(main(["migrate", str(source), "--output", str(output)]), 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep")

    def test_cli_refuses_to_overwrite_source_assessment(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "assessment.json"
            source.write_text(self.sample_path.read_text(encoding="utf-8"), encoding="utf-8")
            original = source.read_bytes()
            with patch("sys.stderr"):
                self.assertEqual(main(["report", str(source), "--output", str(source)]), 2)
            self.assertEqual(source.read_bytes(), original)

    def test_cli_refuses_hardlink_alias_of_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "assessment.json"
            alias = Path(tmp) / "hardlink-report.md"
            source.write_text(self.sample_path.read_text(encoding="utf-8"), encoding="utf-8")
            os.link(source, alias)
            original = source.read_bytes()
            with patch("sys.stderr"):
                self.assertEqual(main(["report", str(source), "--output", str(alias)]), 2)
            self.assertEqual(source.read_bytes(), original)

    def test_cli_refuses_symlink_alias_of_source_when_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "assessment.json"
            alias = Path(tmp) / "symlink-report.md"
            source.write_text(self.sample_path.read_text(encoding="utf-8"), encoding="utf-8")
            try:
                os.symlink(source, alias)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symbolic links are not available in this environment: {exc}")
            original = source.read_bytes()
            with patch("sys.stderr"):
                self.assertEqual(main(["report", str(source), "--output", str(alias)]), 2)
            self.assertEqual(source.read_bytes(), original)

    def test_cli_example_uses_packaged_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "sample.json"
            self.assertEqual(main(["example", "--output", str(output)]), 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), self.sample)

    def test_cli_example_refuses_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "sample.json"
            output.write_text("keep", encoding="utf-8")
            with patch("sys.stderr"):
                self.assertEqual(main(["example", "--output", str(output)]), 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep")

    def test_json_renderer_disallows_non_finite_output(self):
        result = score_assessment(self.sample)
        object.__setattr__(result, "total", float("nan"))
        with self.assertRaises(ValueError):
            render_json(result)

    def test_cli_returns_error_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            invalid = Path(tmp) / "invalid.json"; invalid.write_text("{", encoding="utf-8")
            with patch("sys.stderr"):
                self.assertEqual(main(["validate", str(invalid)]), 2)


if __name__ == "__main__":
    unittest.main()
