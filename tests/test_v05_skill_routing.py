from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class V05SkillRoutingTests(unittest.TestCase):
    def text(self, name):
        return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")

    def test_all_skills_route_to_source_ingestion(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name):
                self.assertIn("../../shared/references/source-ingestion.md", path.read_text(encoding="utf-8"))

    def test_creative_skills_route_to_idea_lab(self):
        for name in ("lumiverse-character-forge", "lumiverse-scenario-forge", "forge-lumiverse-lorebooks", "lumiverse-world-forge"):
            with self.subTest(skill=name):
                self.assertIn("../../shared/references/idea-lab.md", self.text(name))

    def test_steward_owns_shared_record_validation(self):
        text = self.text("lumiverse-project-steward")
        self.assertIn("shared/validators/idea_lab.py", text)
        self.assertIn("shared/validators/source_ledger.py", text)
        self.assertIn("source conflict", text.lower())

    def test_character_routes_source_facts_by_field_ownership(self):
        text = self.text("lumiverse-character-forge")
        for phrase in ("temporal snapshot", "knowledge partition", "World Book candidates"):
            self.assertIn(phrase, text)

    def test_scenario_rejects_future_knowledge(self):
        text = self.text("lumiverse-scenario-forge").lower()
        self.assertIn("future-knowledge", text)
        self.assertIn("temporal snapshot", text)

    def test_lorebook_uses_grounded_entry_suggestions(self):
        text = self.text("forge-lumiverse-lorebooks").lower()
        self.assertIn("entry suggestions", text)
        self.assertIn("spoiler", text)

    def test_world_forge_keeps_source_corpus_out_of_world_book_by_default(self):
        text = self.text("lumiverse-world-forge")
        self.assertIn("Databank", text)
        self.assertIn("source ledger", text.lower())

    def test_preset_converter_does_not_claim_native_preset_creation(self):
        text = self.text("lumiverse-preset-converter")
        self.assertIn("migration evidence", text)
        self.assertIn("does not make Preset Converter a native preset creator", text)

    def test_no_scraper_bypass_is_promised(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "skills").glob("*/SKILL.md"))
        self.assertIn("access controls", combined)
        self.assertIn("unavailable", combined)

    def test_all_relative_skill_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        failures = []
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            for target in pattern.findall(path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                if relative and not (path.parent / relative).resolve().is_file():
                    failures.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
