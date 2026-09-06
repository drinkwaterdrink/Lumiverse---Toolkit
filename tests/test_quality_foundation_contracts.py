import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "shared/validators/capability_receipt.py"
REFERENCES = ROOT / "shared/references"


def load_validator():
    if not VALIDATOR.is_file():
        raise AssertionError("capability receipt validator is missing")
    spec = importlib.util.spec_from_file_location("capability_receipt", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def valid_receipt():
    return {
        "schema": "lumiverse-toolkit.capability-receipt/v1",
        "artifact_id": "card.mara",
        "target": {"application": "Lumiverse", "lumiverse_build": None},
        "capabilities": [
            {
                "id": "character-card-v3",
                "maturity": "static_validated",
                "evidence": [
                    {"kind": "native_template", "source": "Mara reference CHARX"}
                ],
                "dependencies": [],
                "limitations": ["Runtime import not observed in this build."],
            }
        ],
    }


class CapabilityReceiptTests(unittest.TestCase):
    def test_valid_receipt_passes(self):
        validator = load_validator()
        self.assertEqual(validator.validate_capability_receipt(valid_receipt()), [])

    def test_nonconcept_capability_requires_evidence(self):
        validator = load_validator()
        receipt = valid_receipt()
        receipt["capabilities"][0]["evidence"] = []
        codes = {f["code"] for f in validator.validate_capability_receipt(receipt)}
        self.assertIn("missing-capability-evidence", codes)

    def test_runtime_observation_identifies_observation_kind(self):
        validator = load_validator()
        receipt = valid_receipt()
        receipt["capabilities"][0]["maturity"] = "runtime_observed"
        codes = {f["code"] for f in validator.validate_capability_receipt(receipt)}
        self.assertIn("missing-observation-kind", codes)

    def test_certification_requires_named_build_and_repeatable_evidence(self):
        validator = load_validator()
        receipt = valid_receipt()
        receipt["capabilities"][0]["maturity"] = "certified_for_build"
        codes = {f["code"] for f in validator.validate_capability_receipt(receipt)}
        self.assertIn("missing-target-build", codes)
        self.assertIn("insufficient-certification-evidence", codes)

    def test_unknown_maturity_fails(self):
        validator = load_validator()
        receipt = valid_receipt()
        receipt["capabilities"][0]["maturity"] = "probably_works"
        codes = {f["code"] for f in validator.validate_capability_receipt(receipt)}
        self.assertIn("unsupported-maturity", codes)

    def test_duplicate_capability_ids_fail(self):
        validator = load_validator()
        receipt = valid_receipt()
        receipt["capabilities"].append(json.loads(json.dumps(receipt["capabilities"][0])))
        codes = {f["code"] for f in validator.validate_capability_receipt(receipt)}
        self.assertIn("duplicate-capability-id", codes)


class SharedReferenceTests(unittest.TestCase):
    def test_shared_reference_set_exists(self):
        expected = {
            "lumiverse-capability-map.md",
            "creative-quality-kernel.md",
            "agency-contract.md",
            "source-authority.md",
            "artifact-ownership.md",
            "evidence-model.md",
            "idea-lab.md",
            "source-ingestion.md",
        }
        self.assertEqual(expected, {p.name for p in REFERENCES.glob("*.md")})

    def test_agency_contract_uses_complete_normalized_reservations(self):
        text = (REFERENCES / "agency-contract.md").read_text(encoding="utf-8")
        for reserved in (
            "actions", "dialogue", "thoughts", "feelings", "attraction",
            "consent", "decisions", "relationships", "abilities", "backstory",
            "next voluntary action",
        ):
            self.assertIn(reserved, text.lower())

    def test_capability_map_rejects_foreign_setting_names_as_native_facts(self):
        text = (REFERENCES / "lumiverse-capability-map.md").read_text(encoding="utf-8")
        self.assertIn("No direct documented Lumiverse equivalent", text)
        self.assertIn("contemporary native export", text)


if __name__ == "__main__":
    unittest.main()
