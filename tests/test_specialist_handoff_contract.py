import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "shared" / "validators" / "specialist_handoff.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "handoffs"


def load_validator():
    spec = importlib.util.spec_from_file_location("specialist_handoff", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture(name):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class SpecialistHandoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_lorebook_handoff_passes(self):
        self.assertEqual(
            self.validator.validate_specialist_handoff(load_fixture("lorebook-valid.json")),
            [],
        )

    def test_preset_handoff_passes(self):
        self.assertEqual(
            self.validator.validate_specialist_handoff(load_fixture("preset-valid.json")),
            [],
        )

    def test_missing_authority_fails(self):
        handoff = load_fixture("lorebook-valid.json")
        handoff["evidence"]["source_authority"] = []
        findings = self.validator.validate_specialist_handoff(handoff)
        self.assertIn("missing-source-authority", {item["code"] for item in findings})

    def test_lorebook_requires_activation_tests(self):
        handoff = load_fixture("lorebook-valid.json")
        handoff["specialist_requirements"].pop("activation_tests")
        findings = self.validator.validate_specialist_handoff(handoff)
        self.assertIn("missing-lorebook-tests", {item["code"] for item in findings})

    def test_generic_preset_cannot_select_tracker(self):
        handoff = load_fixture("preset-valid.json")
        handoff["specialist_requirements"]["tracker"] = "Trackwright"
        findings = self.validator.validate_specialist_handoff(handoff)
        self.assertIn("generic-preset-tracker-coupling", {item["code"] for item in findings})

    def test_real_frank_policy_cannot_be_global(self):
        handoff = load_fixture("preset-valid.json")
        handoff["policies"][0]["applies_to"] = {"artifact_type": "all"}
        findings = self.validator.validate_specialist_handoff(handoff)
        self.assertIn("unscoped-real-frank-policy", {item["code"] for item in findings})

    def test_return_contract_is_required(self):
        handoff = load_fixture("preset-valid.json")
        handoff["return_contract"].remove("artifact_passport")
        findings = self.validator.validate_specialist_handoff(handoff)
        self.assertIn("incomplete-return-contract", {item["code"] for item in findings})


if __name__ == "__main__":
    unittest.main()
