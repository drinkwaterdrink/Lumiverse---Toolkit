import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "shared/validators/idea_lab.py"
FIXTURE = ROOT / "tests/fixtures/idea_lab/variants-valid.json"


def load_module():
    spec = importlib.util.spec_from_file_location("idea_lab", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IdeaLabContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_module()

    def record(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def codes(self, record):
        return {f["code"] for f in self.validator.validate_idea_lab(record)}

    def test_valid_variants_pass(self):
        self.assertEqual(self.validator.validate_idea_lab(self.record()), [])

    def test_valid_direct_route_can_use_one_candidate(self):
        record = self.record()
        record["route"] = "direct"
        record["candidates"] = record["candidates"][:1]
        record["comparison"] = record["comparison"][:1]
        self.assertEqual(self.validator.validate_idea_lab(record), [])

    def test_variants_require_three_candidates(self):
        record = self.record()
        record["candidates"] = record["candidates"][:2]
        self.assertIn("insufficient-variants", self.codes(record))

    def test_duplicate_direction_signatures_fail(self):
        record = self.record()
        record["candidates"][1]["direction_signature"] = record["candidates"][0]["direction_signature"]
        self.assertIn("duplicate-direction", self.codes(record))

    def test_variants_require_meaningful_divergence(self):
        record = self.record()
        for candidate in record["candidates"]:
            candidate["divergence_dimensions"] = ["tone"]
        self.assertIn("insufficient-divergence", self.codes(record))

    def test_selected_candidate_must_exist(self):
        record = self.record()
        record["selected_candidate_id"] = "idea-missing"
        self.assertIn("unknown-selected-candidate", self.codes(record))

    def test_unselected_candidate_cannot_be_approved_canon(self):
        record = self.record()
        record["selected_candidate_id"] = "idea-station"
        record["candidates"][1]["status"] = "approved"
        self.assertIn("canonized-unselected-candidate", self.codes(record))

    def test_agency_risk_requires_blocking_finding(self):
        record = self.record()
        record["candidates"][0]["agency_risks"] = ["Assigns the user's profession."]
        self.assertIn("unblocked-agency-risk", self.codes(record))
        record["validation"]["findings"] = [{
            "code": "agency-risk", "severity": "blocker",
            "candidate_id": "idea-station", "message": "User role must remain open."
        }]
        self.assertNotIn("unblocked-agency-risk", self.codes(record))

    def test_variant_comparison_covers_every_candidate(self):
        record = self.record()
        record["comparison"] = record["comparison"][:2]
        self.assertIn("incomplete-comparison", self.codes(record))


if __name__ == "__main__":
    unittest.main()
