import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/forge-lumiverse-lorebooks/scripts/compile_character_book.py"
spec = importlib.util.spec_from_file_location("compiler", SCRIPT)
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


class EmbeddedCharacterBookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((ROOT / "tests/fixtures/world_forge/narrator-loreforge-valid.json").read_text(encoding="utf-8"))

    def test_base_subset_and_manifest(self):
        book, manifest = compiler.compile_character_book(self.source, "world")
        self.assertEqual(set(book), {"entries"})
        self.assertTrue(book["entries"][0]["constant"])
        self.assertEqual(book["entries"][1]["keys"], ["Mara Vale", "Mara"])
        self.assertEqual(manifest["stable_id_map"]["world.mara"], 1)
        self.assertIn("sticky", manifest["omitted_settings"]["world.location"])
        self.assertFalse(manifest["native_lumiverse_full_fidelity"])

    def test_invalid_book_id_refused(self):
        with self.assertRaises(ValueError):
            compiler.compile_character_book(self.source, "missing")

    def test_disabled_entry_is_not_enabled(self):
        source = json.loads(json.dumps(self.source))
        source["books"][0]["entries"][1]["state"] = "disabled"
        book, _ = compiler.compile_character_book(source, "world")
        self.assertFalse(book["entries"][1]["enabled"])


if __name__ == "__main__":
    unittest.main()
