from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/lumiverse-world-forge"


class WorldProfileTests(unittest.TestCase):
    def test_skill_and_references_exist(self):
        self.assertTrue((SKILL / "SKILL.md").is_file())
        for name in ["profiles-and-routing.md", "narrator-and-ensemble-contract.md", "build-workflow.md", "worldbuilder-concepts-review.md", "validation-and-release.md"]:
            self.assertTrue((SKILL / "references" / name).is_file())

    def test_skill_names_all_profiles_and_specialists(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for value in ["single_character", "character_with_world", "narrator_world", "ensemble_scenario", "multi_card_world", "lumiverse-character-forge", "lumiverse-scenario-forge", "forge-lumiverse-lorebooks", "lumiverse-project-steward"]:
            self.assertIn(value, text)

    def test_narrator_agency_contract_is_present(self):
        text = (SKILL / "references/narrator-and-ensemble-contract.md").read_text(encoding="utf-8")
        self.assertIn("never completes the user's next voluntary action", text)
        self.assertIn("alternate greetings", text)


if __name__ == "__main__":
    unittest.main()
