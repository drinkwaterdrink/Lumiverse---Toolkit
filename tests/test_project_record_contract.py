import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "shared" / "validators" / "project_record.py"
SCHEMA_PATH = ROOT / "shared" / "schemas" / "project-record.schema.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("project_record", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_record():
    return {
        "schema": "lumiverse-toolkit.project/v1",
        "project": {
            "id": "project-nightshift-house",
            "name": "Nightshift House",
            "version": "0.1",
            "status": "planning",
            "target": {
                "application": "Lumiverse",
                "documentation_snapshot": None,
            },
        },
        "authority": {
            "source_order": [
                "user",
                "approved_project",
                "lumiverse_docs_technical",
                "external_reference",
                "generated",
            ],
            "fact_statuses": ["canon", "provisional", "disputed", "deprecated"],
        },
        "preferences": {
            "detail": "rich",
            "always_injected": "lean",
            "primary_surface": "android-mobile",
        },
        "agency": {
            "protected_subject": "{{user}}",
            "reserved": [
                "actions",
                "dialogue",
                "thoughts",
                "feelings",
                "attraction",
                "consent",
                "decisions",
                "relationships",
                "abilities",
                "backstory",
                "next_voluntary_action",
            ],
        },
        "policies": [],
        "entities": [],
        "canon": [],
        "artifacts": [
            {
                "id": "artifact-world-book",
                "type": "world_book",
                "status": "planned",
                "display_name": None,
                "origin": "user",
            },
            {
                "id": "artifact-generic-preset",
                "type": "loom_preset",
                "status": "planned",
                "display_name": "Generic Roleplay",
                "origin": "user",
            },
        ],
        "dependencies": [
            {
                "id": "dependency-preset-uses-world-book",
                "from": "artifact-generic-preset",
                "to": "artifact-world-book",
                "type": "references",
                "status": "provisional",
                "origin": "generated",
            }
        ],
        "validation": {"status": "not_run", "findings": [], "last_run": None},
        "release": {"status": "unreleased", "manifest": None},
        "decisions": [],
        "unresolved": [],
        "extensions": {"unknown_future_field": True},
    }


class ProjectRecordContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_schema_declares_authoritative_identifier(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            schema["properties"]["schema"]["const"],
            "lumiverse-toolkit.project/v1",
        )

    def test_valid_record_passes_and_unknown_fields_survive(self):
        record = valid_record()
        self.assertEqual(self.validator.validate_project_record(record), [])
        self.assertTrue(record["extensions"]["unknown_future_field"])

    def test_missing_required_ledger_fails_at_exact_path(self):
        record = valid_record()
        del record["canon"]
        findings = self.validator.validate_project_record(record)
        self.assertIn("missing-required-field", {item["code"] for item in findings})
        self.assertIn("$.canon", {item["path"] for item in findings})

    def test_duplicate_ids_fail(self):
        record = valid_record()
        record["artifacts"][1]["id"] = record["artifacts"][0]["id"]
        findings = self.validator.validate_project_record(record)
        self.assertIn("duplicate-id", {item["code"] for item in findings})

    def test_dependency_to_missing_artifact_fails(self):
        record = valid_record()
        record["dependencies"][0]["to"] = "artifact-does-not-exist"
        findings = self.validator.validate_project_record(record)
        self.assertIn("missing-dependency-target", {item["code"] for item in findings})

    def test_incomplete_agency_reservations_are_blocking(self):
        record = valid_record()
        record["agency"]["reserved"].remove("consent")
        findings = self.validator.validate_project_record(record)
        result = next(item for item in findings if item["code"] == "incomplete-agency-contract")
        self.assertEqual(result["severity"], "blocker")

    def test_all_normalized_agency_reservations_are_required(self):
        record = valid_record()
        record["agency"]["reserved"].remove("next_voluntary_action")
        findings = self.validator.validate_project_record(record)
        result = next(item for item in findings if item["code"] == "incomplete-agency-contract")
        self.assertEqual(result["severity"], "blocker")

    def test_real_frank_policy_must_be_scoped(self):
        record = valid_record()
        record["policies"] = [
            {
                "id": "policy-real-frank",
                "origin": "user",
                "applies_to": {"artifact_type": "all"},
                "rules": {"version_increment": 0.1},
            }
        ]
        findings = self.validator.validate_project_record(record)
        self.assertIn("unscoped-project-policy", {item["code"] for item in findings})


if __name__ == "__main__":
    unittest.main()
