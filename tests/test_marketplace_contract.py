import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"


class MarketplaceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
        cls.entry = cls.marketplace["plugins"][0]

    def test_marketplace_identity(self):
        self.assertEqual(self.marketplace["name"], "lumiverse-toolkit-marketplace")
        self.assertEqual(self.marketplace["interface"]["displayName"], "Lumiverse Toolkit")

    def test_marketplace_exposes_one_expected_plugin(self):
        self.assertEqual(len(self.marketplace["plugins"]), 1)
        self.assertEqual(self.entry["name"], "lumiverse-toolkit")

    def test_plugin_source_is_public_repository_root(self):
        self.assertEqual(
            self.entry["source"],
            {
                "source": "url",
                "url": "https://github.com/drinkwaterdrink/Lumiverse---Toolkit.git",
                "ref": "main",
            },
        )

    def test_marketplace_version_matches_plugin_manifest(self):
        manifest = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(self.entry["version"], manifest["version"])

    def test_install_policy_is_explicit_and_opt_in(self):
        self.assertEqual(self.entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(self.entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(self.entry["category"], "Productivity")


if __name__ == "__main__":
    unittest.main()
