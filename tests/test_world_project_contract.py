import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "shared/validators/world_project.py"
FIXTURES = ROOT / "tests/fixtures/world_forge"

spec = importlib.util.spec_from_file_location("world_project", VALIDATOR)
world_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(world_project)


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class WorldProjectContractTests(unittest.TestCase):
    def test_valid_profiles_pass(self):
        self.assertEqual(world_project.validate_world_project(load("narrator-world-valid.json")), [])
        self.assertEqual(world_project.validate_world_project(load("multi-card-valid.json")), [])

    def test_profile_output_mismatch(self):
        record = load("narrator-world-valid.json")
        record["artifacts"] = [record["artifacts"][0]]
        self.assertIn("profile-output-mismatch", {f["code"] for f in world_project.validate_world_project(record)})

    def test_agency_is_blocking(self):
        record = load("narrator-world-valid.json")
        record["agency"]["reserved"].remove("consent")
        finding = next(f for f in world_project.validate_world_project(record) if f["code"] == "incomplete-agency-contract")
        self.assertEqual(finding["severity"], "blocker")

    def test_temporal_conflict(self):
        record = load("narrator-world-valid.json")
        record["temporal"] = [{"id": "one", "entity_id": "entity-mara", "era": "opening", "status": "alive", "location": "entity-station"}, {"id": "two", "entity_id": "entity-mara", "era": "opening", "status": "dead", "location": "entity-station"}]
        self.assertIn("temporal-conflict", {f["code"] for f in world_project.validate_world_project(record)})

    def test_relationship_asymmetry_is_minor(self):
        record = load("narrator-world-valid.json")
        record["relationships"] = [{"id": "r", "from": "entity-mara", "to": "entity-dispatcher", "summary": "trust", "reciprocal_id": None, "intentional_asymmetry": False}]
        finding = next(f for f in world_project.validate_world_project(record) if f["code"] == "unreviewed-relationship-asymmetry")
        self.assertEqual(finding["severity"], "minor")

    def test_unknown_extensions_are_allowed(self):
        record = load("narrator-world-valid.json")
        self.assertTrue(record["extensions"]["future"])
        self.assertEqual(world_project.validate_world_project(record), [])


if __name__ == "__main__":
    unittest.main()
