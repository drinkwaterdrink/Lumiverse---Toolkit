import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def load_module(name, relative_path):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConnectedProjectAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_validator = load_module(
            "project_record", "shared/validators/project_record.py"
        )
        cls.handoff_validator = load_module(
            "specialist_handoff", "shared/validators/specialist_handoff.py"
        )
        cls.project = json.loads(
            (FIXTURES / "end_to_end" / "nightshift-project.json").read_text(encoding="utf-8")
        )
        cls.lorebook = json.loads(
            (FIXTURES / "handoffs" / "lorebook-valid.json").read_text(encoding="utf-8")
        )
        cls.preset = json.loads(
            (FIXTURES / "handoffs" / "preset-valid.json").read_text(encoding="utf-8")
        )

    def test_connected_package_passes_all_structural_contracts(self):
        self.assertEqual(self.project_validator.validate_project_record(self.project), [])
        self.assertEqual(self.handoff_validator.validate_specialist_handoff(self.lorebook), [])
        self.assertEqual(self.handoff_validator.validate_specialist_handoff(self.preset), [])

    def test_handoffs_reference_the_project_and_declared_artifacts(self):
        project_id = self.project["project"]["id"]
        artifact_ids = {item["id"] for item in self.project["artifacts"]}
        for handoff in (self.lorebook, self.preset):
            self.assertEqual(handoff["project_id"], project_id)
            self.assertIn(handoff["artifact"]["id"], artifact_ids)

    def test_lorebook_has_all_activation_test_classes(self):
        cases = self.lorebook["specialist_requirements"]["activation_tests"]
        self.assertTrue(cases["positive"])
        self.assertTrue(cases["negative"])
        self.assertTrue(cases["collision"])

    def test_generic_preset_remains_tracker_agnostic(self):
        requirements = self.preset["specialist_requirements"]
        self.assertEqual(requirements["preset_kind"], "generic_roleplay")
        self.assertEqual(requirements["tracker"], "unselected")

    def test_real_frank_policy_is_scoped_and_has_no_invented_version(self):
        policy = next(item for item in self.preset["policies"] if item["id"] == "policy-real-frank")
        self.assertEqual(policy["applies_to"]["artifact_type"], "loom_preset")
        self.assertEqual(policy["applies_to"]["name_family"], "Real Frank")
        self.assertIsNone(policy["rules"]["starting_version"])

    def test_missing_runtime_evidence_remains_explicitly_unresolved(self):
        unresolved = {item["id"] for item in self.project["unresolved"]}
        self.assertIn("unresolved-world-book-native-template", unresolved)
        self.assertIn("unresolved-source-preset", unresolved)
        self.assertEqual(self.project["release"]["status"], "unreleased")

    def test_world_forge_routing_and_boundaries_are_documented(self):
        routing = (ROOT / "skills/lumiverse-project-steward/references/routing-and-handoffs.md").read_text(encoding="utf-8")
        world_skill = (ROOT / "skills/lumiverse-world-forge/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("World Forge", routing)
        self.assertIn("narrator_world", world_skill)
        self.assertIn("ensemble_scenario", world_skill)
        self.assertIn("compile_character_book.py", world_skill)


if __name__ == "__main__":
    unittest.main()
