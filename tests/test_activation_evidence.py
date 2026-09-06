import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/forge-lumiverse-lorebooks/scripts/simulate_activation.py"
spec = importlib.util.spec_from_file_location("simulate_activation", SCRIPT)
simulator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = simulator
spec.loader.exec_module(simulator)


def entry(stable_id, keyword, **changes):
    value = {
        "stable_id": stable_id,
        "state": "conditional",
        "keywords": [keyword],
        "secondary_keywords": [],
        "selective_logic": "or",
        "content": stable_id,
        "position": 0,
        "order": 0,
        "priority": 0,
    }
    value.update(changes)
    return value


def lore_spec(entries):
    return {
        "schema": "loreforge.lumiverse.v1",
        "books": [{"id": "world", "entries": entries}],
        "recommended_runtime": {
            "max_recursion_passes": 0,
            "max_activated_entries": 20,
            "max_token_budget": 4000,
            "min_priority": 0,
        },
    }


class ActivationEvidenceTests(unittest.TestCase):
    def assess(self, spec_value, case):
        evaluation = simulator.evaluate_case(spec_value, case)
        return simulator.assess_case(evaluation, case)

    def test_exact_keyword_case_passes(self):
        result = self.assess(
            lore_spec([entry("station", "Blackwater Station")]),
            {"messages": ["We enter Blackwater Station."], "expected_active": ["station"], "expected_inactive": []},
        )
        self.assertEqual(result["status"], "PASS")

    def test_vector_expected_match_is_unproven(self):
        result = self.assess(
            lore_spec([entry("custom", "moon rite", vectorized=True)]),
            {"messages": ["They discuss a lunar ceremony."], "expected_active": ["custom"], "expected_inactive": []},
        )
        self.assertEqual(result["status"], "UNPROVEN")

    def test_probability_gate_is_unproven(self):
        result = self.assess(
            lore_spec([entry("rumor", "rumor", use_probability=True, probability=40)]),
            {"messages": ["A rumor spreads."], "expected_active": ["rumor"], "expected_inactive": []},
        )
        self.assertEqual(result["status"], "UNPROVEN")

    def test_weighted_group_winner_is_unproven(self):
        entries = [
            entry("rain", "weather", group="weather", group_weight=70),
            entry("sun", "weather", group="weather", group_weight=30),
        ]
        result = self.assess(
            lore_spec(entries),
            {"messages": ["The weather changes."], "expected_active": ["rain"], "expected_inactive": []},
        )
        self.assertEqual(result["status"], "UNPROVEN")

    def test_persistent_timing_behavior_is_unproven(self):
        result = self.assess(
            lore_spec([entry("echo", "echo", sticky=3)]),
            {"messages": ["An echo sounds."], "expected_active": ["echo"], "expected_inactive": []},
        )
        self.assertEqual(result["status"], "UNPROVEN")

    def test_cli_returns_two_when_only_unproven(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec_path = root / "spec.json"
            tests_path = root / "tests.json"
            spec_path.write_text(json.dumps(lore_spec([entry("custom", "moon rite", vectorized=True)])), encoding="utf-8")
            tests_path.write_text(json.dumps({
                "schema": "loreforge.activation-tests.v1",
                "cases": [{"name": "semantic", "messages": ["lunar ceremony"], "expected_active": ["custom"], "expected_inactive": []}],
            }), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(spec_path), str(tests_path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNPROVEN", result.stdout)


if __name__ == "__main__":
    unittest.main()
