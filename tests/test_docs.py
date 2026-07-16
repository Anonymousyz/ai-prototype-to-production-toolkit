from pathlib import Path
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ai_ready.scoring import score_assessment


class DocumentationContractTests(unittest.TestCase):
    def test_package_and_citation_versions_match_release(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
        init = (ROOT / "src" / "ai_ready" / "__init__.py").read_text(encoding="utf-8-sig")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8-sig")
        p_ver = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE).group(1)
        i_ver = re.search(r'__version__ = "([^"]+)"', init).group(1)
        c_ver = re.search(r'^version: ([^\s]+)', citation, re.MULTILINE).group(1)
        self.assertEqual((p_ver, i_ver, c_ver), ("0.6.0", "0.6.0", "0.6.0"))

    def test_prompts_have_information_and_human_review_boundaries(self):
        for path in (ROOT / "prompts").glob("*.md"):
            text = path.read_text(encoding="utf-8-sig").lower()
            self.assertIn("authorized", text, path.name)
            self.assertIn("confidential", text, path.name)
            self.assertIn("human", text, path.name)
            self.assertIn("not", text, path.name)

    def test_cli_docs_describe_canonical_contract(self):
        text = (ROOT / "docs" / "cli.md").read_text(encoding="utf-8-sig").lower()
        for phrase in (
            "10 / 12 / 12 / 10 / 10 / 10 / 6",
            "eight canonical",
            "review.owner",
            "review.reviewer_type",
            "review.reviewed_at",
            "`stage` is optional",
            "`top_gaps` is required but may be empty",
            "anything: 1/1",
            "schema_version",
            "ai-ready migrate",
            "--format html",
        ):
            self.assertIn(phrase, text)

    def test_json_schema_declares_v06_contract(self):
        schema = json.loads((ROOT / "schemas" / "readiness_assessment.schema.json").read_text(encoding="utf-8"))
        self.assertIn("v0.6", schema["title"])
        self.assertIn("schema_version", schema["required"])
        self.assertEqual(schema["properties"]["schema_version"], {"const": "0.6"})

    def test_all_human_review_artifacts_list_all_eight_vetoes(self):
        expected = {
            "unauthorized data use",
            "sensitive data to unapproved model",
            "high-risk decision without human review",
            "no logs",
            "no error/rollback owner",
            "cannot evaluate output quality",
            "uncontrolled cost",
            "marketed as production-ready but remains a demo",
        }
        for relative in (
            "templates/pilot_review_memo.md",
            "scorecards/ai_prototype_readiness_scorecard.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8-sig").lower()
            for phrase in expected:
                self.assertIn(phrase, text, f"{relative}: {phrase}")

    def test_workflow_is_only_an_inactive_template(self):
        self.assertFalse((ROOT / ".github" / "workflows").exists())
        self.assertTrue((ROOT / "docs" / "github_actions_validate.template.yml").exists())

    def test_portfolio_evidence_map_is_present_and_linked(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
        evidence_map = (ROOT / "docs" / "portfolio_evidence_map.md").read_text(encoding="utf-8-sig")
        self.assertIn("docs/portfolio_evidence_map.md", readme)
        self.assertIn("research-to-decision-toolkit", evidence_map)
        self.assertIn("awesome-ai-production-readiness", evidence_map)
        self.assertIn("does not claim real client outcomes", evidence_map)

    def test_v06_integration_and_handoff_are_bounded_and_linked(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
        integration = (ROOT / "integrations" / "promptfoo" / "README.md").read_text(encoding="utf-8-sig").lower()
        handoff = (ROOT / "docs" / "readiness_to_decision_handoff.md").read_text(encoding="utf-8-sig").lower()
        for relative in (
            "integrations/promptfoo/README.md",
            "docs/readiness_to_decision_handoff.md",
            "examples/synthetic_industrial_safety_procedure_assistant.json",
        ):
            self.assertIn(relative, readme)
        for phrase in ("authorized", "confidential", "human", "does not convert"):
            self.assertIn(phrase, integration)
        for phrase in ("research-to-decision-toolkit", "does not copy", "human decision"):
            self.assertIn(phrase, handoff)

    def test_release_and_distribution_contract_is_complete(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8-sig")
        manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8-sig")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
        self.assertNotIn("## v0.5.3", changelog)
        for required in (
            "recursive-include docs",
            "recursive-include schemas",
            "recursive-include examples",
            "recursive-include integrations",
            "recursive-include scorecards",
            "recursive-include templates",
            "recursive-include prompts",
            "recursive-include articles",
            "include CITATION.cff",
        ):
            self.assertIn(required, manifest)
        self.assertIn('license = "MIT"', pyproject)
        self.assertNotIn("License :: OSI Approved :: MIT License", pyproject)

    def test_promptfoo_results_are_ignored_and_version_is_pinned(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8-sig")
        integration = (ROOT / "integrations" / "promptfoo" / "README.md").read_text(encoding="utf-8-sig")
        self.assertIn("integrations/promptfoo/results/", gitignore)
        self.assertIn("promptfoo@0.121.19", integration)
        self.assertNotIn("promptfoo@latest", integration)

    def test_readme_expected_output_includes_human_review_metadata(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
        sample = json.loads((ROOT / "examples" / "sample_assessment.json").read_text(encoding="utf-8"))
        result = score_assessment(sample)
        self.assertIn(f"Review owner: {result.review_owner}", readme)
        self.assertIn(f"Reviewed at: {result.reviewed_at}", readme)


if __name__ == "__main__":
    unittest.main()
