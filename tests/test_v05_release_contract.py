import json
import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class V05ReleaseContractTests(unittest.TestCase):
    def test_version_is_v05_and_marketplace_matches(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        version = manifest["version"]
        self.assertRegex(version, r"^0\.5\.0\+codex\.\d{14}$")
        self.assertEqual(marketplace["plugins"][0]["version"], version)
        for relative in ("README.md", "CHANGELOG.md", "INSTALL.md", "docs/v0.5-verification-report.md"):
            self.assertIn(version, (ROOT / relative).read_text(encoding="utf-8"), relative)

    def test_readme_routes_to_current_report(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/v0.5-verification-report.md", text)
        self.assertIn("Idea Lab", text)
        self.assertIn("source ingestion", text.lower())

    def test_report_states_real_capabilities_and_boundaries(self):
        text = (ROOT / "docs/v0.5-verification-report.md").read_text(encoding="utf-8")
        for phrase in ("idea-lab/v1", "source-ledger/v1", "future-knowledge", "No bundled crawler", "not factual certification"):
            self.assertIn(phrase, text)

    def test_schemas_and_validators_are_present(self):
        for relative in (
            "shared/schemas/idea-lab-record.schema.json",
            "shared/schemas/source-ledger.schema.json",
            "shared/validators/idea_lab.py",
            "shared/validators/source_ledger.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_all_relative_documentation_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        failures = []
        paths = [ROOT / "README.md", ROOT / "INSTALL.md", *ROOT.glob("skills/*/SKILL.md")]
        for path in paths:
            for target in pattern.findall(path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                if relative and not (path.parent / relative).resolve().is_file():
                    failures.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
