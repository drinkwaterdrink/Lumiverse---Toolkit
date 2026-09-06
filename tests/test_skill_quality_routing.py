from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted((ROOT / "skills").glob("*/SKILL.md"))


class SkillQualityRoutingTests(unittest.TestCase):
    def test_all_six_skills_route_to_shared_authority_agency_and_evidence(self):
        self.assertEqual(len(SKILLS), 6)
        for path in SKILLS:
            text = path.read_text(encoding="utf-8")
            for reference in ("agency-contract.md", "source-authority.md", "evidence-model.md"):
                with self.subTest(skill=path.parent.name, reference=reference):
                    self.assertIn(f"../../shared/references/{reference}", text)

    def test_creative_skills_route_to_quality_kernel(self):
        for name in (
            "lumiverse-character-forge", "lumiverse-scenario-forge",
            "forge-lumiverse-lorebooks", "lumiverse-world-forge",
        ):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("../../shared/references/creative-quality-kernel.md", text)

    def test_create_then_refine_is_default_with_optional_interview_and_idea_lab(self):
        for name in ("lumiverse-character-forge", "lumiverse-scenario-forge", "lumiverse-world-forge"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("create then refine", text)
            self.assertIn("interview", text)
            self.assertIn("idea lab", text)

    def test_preset_creation_is_separate_from_world_packages(self):
        text = (ROOT / "skills/lumiverse-world-forge/SKILL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "skills/lumiverse-world-forge/references/build-workflow.md").read_text(encoding="utf-8")
        self.assertIn("Preset creation is separate", text)
        self.assertIn("must not require a dedicated Loom preset", workflow)

    def test_intimacy_module_is_optional_and_separately_routed(self):
        text = (ROOT / "skills/lumiverse-project-steward/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("optional routed module", text)
        self.assertIn("consenting-adult", text)

    def test_scenario_modes_use_dynamic_sections(self):
        skill = (ROOT / "skills/lumiverse-scenario-forge/SKILL.md").read_text(encoding="utf-8")
        modes = (ROOT / "skills/lumiverse-scenario-forge/references/modes-and-output.md").read_text(encoding="utf-8")
        self.assertNotIn("Always use CORE, USER, NPC, CONFLICT, OPENING, and EXPANSION", skill)
        self.assertNotIn("all six sections", modes)
        self.assertIn("CORE → OPENING → EXPANSION NOTES", modes)
        self.assertIn("dynamic sections", modes.lower())

    def test_all_relative_markdown_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        failures = []
        for path in SKILLS:
            for target in pattern.findall(path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                if relative and not (path.parent / relative).resolve().is_file():
                    failures.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
