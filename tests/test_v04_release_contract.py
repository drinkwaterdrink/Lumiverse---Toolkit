import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V04ReleaseContractTests(unittest.TestCase):
    def test_plugin_version_is_v04_and_documented(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        version = manifest["version"]
        self.assertRegex(version, r"^0\.4\.0\+codex\.\d{14}$")
        for relative in ("README.md", "CHANGELOG.md", "INSTALL.md", "docs/v0.4-verification-report.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(version, text, relative)

    def test_all_six_skills_are_registered(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["skills"], "./skills/")
        names = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(names, {
            "forge-lumiverse-lorebooks",
            "lumiverse-character-forge",
            "lumiverse-preset-converter",
            "lumiverse-project-steward",
            "lumiverse-scenario-forge",
            "lumiverse-world-forge",
        })

    def test_release_docs_state_new_contracts_and_boundaries(self):
        report = (ROOT / "docs/v0.4-verification-report.md").read_text(encoding="utf-8")
        for phrase in (
            "Creative Quality Kernel", "capability receipt", "build ledger",
            "PASS, FAIL, and UNPROVEN", "not runtime certification",
        ):
            self.assertIn(phrase, report)

    def test_readme_points_to_current_report(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/v0.4-verification-report.md", readme)
        self.assertNotIn("## v0.3 bundled skills", readme)

    def test_no_broken_relative_markdown_links(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        failures = []
        for path in [ROOT / "README.md", ROOT / "INSTALL.md", *ROOT.glob("skills/*/SKILL.md")]:
            for target in pattern.findall(path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                if relative and not (path.parent / relative).resolve().is_file():
                    failures.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
