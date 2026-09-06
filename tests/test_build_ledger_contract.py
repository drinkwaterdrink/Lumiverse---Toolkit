import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "shared/validators/build_ledger.py"


def load_validator():
    if not VALIDATOR.is_file():
        raise AssertionError("build ledger validator is missing")
    spec = importlib.util.spec_from_file_location("build_ledger", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def ledger():
    return {
        "schema": "lumiverse-toolkit.build-ledger/v1",
        "project_id": "station-world",
        "status": "in_progress",
        "current_phase": "draft",
        "phases": [
            {
                "id": "discover",
                "status": "complete",
                "artifact": "artifacts/seed.md",
                "signoff_anchor": "DISCOVERY COMPLETE",
                "dependencies": [],
                "evidence": [{"kind": "artifact_gate"}],
            },
            {
                "id": "draft",
                "status": "in_progress",
                "artifact": "artifacts/draft.md",
                "signoff_anchor": "DRAFT COMPLETE",
                "dependencies": ["discover"],
                "evidence": [],
            },
            {
                "id": "optional-preset",
                "status": "skipped",
                "skip_reason": "Preset creation is a separate request.",
                "dependencies": [],
                "evidence": [],
            },
        ],
    }


class BuildLedgerTests(unittest.TestCase):
    def test_valid_artifact_gate_passes(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "artifacts").mkdir()
            (root / "artifacts/seed.md").write_text("Seed\nDISCOVERY COMPLETE\n", encoding="utf-8")
            self.assertEqual(validator.validate_build_ledger(ledger(), root), [])

    def test_complete_phase_requires_existing_nonempty_anchored_artifact(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            findings = validator.validate_build_ledger(ledger(), Path(tmp))
        codes = {f["code"] for f in findings}
        self.assertIn("missing-phase-artifact", codes)

    def test_complete_phase_rejects_missing_anchor(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "artifacts").mkdir()
            (root / "artifacts/seed.md").write_text("Seed only\n", encoding="utf-8")
            codes = {f["code"] for f in validator.validate_build_ledger(ledger(), root)}
        self.assertIn("missing-signoff-anchor", codes)

    def test_skipped_phase_requires_reason(self):
        validator = load_validator()
        record = ledger()
        del record["phases"][2]["skip_reason"]
        codes = {f["code"] for f in validator.validate_build_ledger(record)}
        self.assertIn("missing-skip-reason", codes)

    def test_completed_phase_cannot_depend_on_unfinished_phase(self):
        validator = load_validator()
        record = ledger()
        record["phases"][0]["dependencies"] = ["draft"]
        codes = {f["code"] for f in validator.validate_build_ledger(record)}
        self.assertIn("unresolved-phase-dependency", codes)

    def test_complete_ledger_requires_all_phases_resolved(self):
        validator = load_validator()
        record = ledger()
        record["status"] = "complete"
        record["current_phase"] = None
        codes = {f["code"] for f in validator.validate_build_ledger(record)}
        self.assertIn("incomplete-ledger", codes)


if __name__ == "__main__":
    unittest.main()
