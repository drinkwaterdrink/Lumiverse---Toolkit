import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "shared/validators/source_ledger.py"
FIXTURE = ROOT / "tests/fixtures/source_ingestion/timeline-valid.json"


def load_module():
    spec = importlib.util.spec_from_file_location("source_ledger", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceLedgerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_module()

    def record(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def findings(self, record):
        return self.validator.validate_source_ledger(record)

    def codes(self, record):
        return {item["code"] for item in self.findings(record)}

    def test_valid_mixed_source_snapshot_passes(self):
        self.assertEqual(self.findings(self.record()), [])

    def test_canon_fact_requires_provenance(self):
        record = self.record()
        record["facts"][0]["source_ids"] = []
        self.assertIn("missing-fact-provenance", self.codes(record))

    def test_duplicate_content_hash_requires_alias(self):
        record = self.record()
        duplicate = dict(record["sources"][0])
        duplicate["id"] = "source-copy"
        record["sources"].append(duplicate)
        self.assertIn("duplicate-source-content", self.codes(record))
        record["sources"][-1]["alias_of"] = record["sources"][0]["id"]
        self.assertNotIn("duplicate-source-content", self.codes(record))

    def test_excluded_source_requires_reason(self):
        record = self.record()
        record["sources"][2]["relevance_reason"] = ""
        self.assertIn("missing-relevance-reason", self.codes(record))

    def test_final_ledger_blocks_unresolved_conflict(self):
        record = self.record()
        record["conflicts"][0]["status"] = "unresolved"
        record["conflicts"][0]["resolution"] = None
        self.assertIn("unresolved-source-conflict", self.codes(record))

    def test_future_fact_cannot_be_active_at_snapshot(self):
        record = self.record()
        record["facts"][1]["active_at_snapshot"] = True
        self.assertIn("future-knowledge-leak", self.codes(record))

    def test_hidden_truth_cannot_enter_unknowing_character_owner(self):
        record = self.record()
        record["facts"][2]["owner"] = "character:entity-clerk"
        record["facts"][2]["knowers"] = []
        self.assertIn("hidden-truth-owner-leak", self.codes(record))
        record["facts"][2]["knowers"] = ["entity-clerk"]
        self.assertNotIn("hidden-truth-owner-leak", self.codes(record))

    def test_adaptation_references_source_fact_and_stays_distinct(self):
        record = self.record()
        record["adaptations"][0]["source_fact_ids"] = ["fact-missing"]
        self.assertIn("unknown-adaptation-source-fact", self.codes(record))
        record = self.record()
        record["adaptations"][0]["statement"] = record["facts"][0]["statement"]
        self.assertIn("undifferentiated-adaptation", self.codes(record))

    def test_entity_source_reference_must_exist(self):
        record = self.record()
        record["entities"][0]["source_ids"].append("source-missing")
        self.assertIn("unknown-entity-source", self.codes(record))

    def test_entry_suggestion_must_be_grounded(self):
        record = self.record()
        record["entry_suggestions"][0]["fact_ids"] = []
        record["entry_suggestions"][0]["entity_ids"] = []
        self.assertIn("ungrounded-entry-suggestion", self.codes(record))

    def test_conflicted_fact_requires_conflict_record(self):
        record = self.record()
        record["facts"][0]["status"] = "CONFLICTED"
        record["conflicts"] = []
        self.assertIn("orphan-conflicted-fact", self.codes(record))


if __name__ == "__main__":
    unittest.main()
