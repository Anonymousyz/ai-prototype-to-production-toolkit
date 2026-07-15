from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentationContractTests(unittest.TestCase):
    def test_package_versions_match_v050(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
        init = (ROOT / "src" / "ai_ready" / "__init__.py").read_text(encoding="utf-8-sig")
        p_ver = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE).group(1)
        i_ver = re.search(r'__version__ = "([^"]+)"', init).group(1)
        self.assertEqual((p_ver, i_ver), ("0.5.0", "0.5.0"))

    def test_prompts_have_information_and_human_review_boundaries(self):
        for path in (ROOT / "prompts").glob("*.md"):
            text = path.read_text(encoding="utf-8-sig").lower()
            self.assertIn("authorized", text, path.name)
            self.assertIn("confidential", text, path.name)
            self.assertIn("human", text, path.name)
            self.assertIn("not", text, path.name)

    def test_cli_docs_describe_canonical_contract(self):
        text = (ROOT / "docs" / "cli.md").read_text(encoding="utf-8-sig").lower()
        for phrase in ("seven canonical", "eight canonical", "reviewer", "assessment_date", "anything: 1/1"):
            self.assertIn(phrase, text)

    def test_workflow_is_only_an_inactive_template(self):
        self.assertFalse((ROOT / ".github" / "workflows").exists())
        self.assertTrue((ROOT / "docs" / "github_actions_validate.template.yml").exists())


if __name__ == "__main__":
    unittest.main()
