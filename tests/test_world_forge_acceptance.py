import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compiler = load("compiler", "skills/forge-lumiverse-lorebooks/scripts/compile_character_book.py")
charx = load("charx", "skills/lumiverse-character-forge/scripts/package_charx.py")


class WorldForgeAcceptanceTests(unittest.TestCase):
    def test_narrator_book_compiles_and_packages(self):
        source = json.loads((ROOT / "tests/fixtures/world_forge/narrator-loreforge-valid.json").read_text(encoding="utf-8"))
        card = json.loads((ROOT / "tests/fixtures/world_forge/narrator-card-valid.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "station-world.charx"
            book, manifest = compiler.compile_character_book(source, "world")
            card["data"]["character_book"] = book
            charx.package(card, output)
            with zipfile.ZipFile(output) as archive:
                result = json.loads(archive.read("card.json"))
            self.assertEqual(result, card)
            self.assertEqual(len(result["data"]["character_book"]["entries"]), 3)
            self.assertFalse(manifest["native_lumiverse_full_fidelity"])

    def test_revision_preserves_unknown_archive_members(self):
        card = json.loads((ROOT / "tests/fixtures/world_forge/narrator-card-valid.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.charx"
            output = root / "revised.charx"
            card["unknown_future_field"] = {"keep": True}
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("card.json", "{}")
                archive.writestr("extra.bin", b"opaque")
            card["data"]["scenario"] = "The board changes while the user watches."
            charx.package(card, output, source=source)
            members = charx.read_archive(output)
            self.assertEqual(members["extra.bin"], b"opaque")
            self.assertEqual(json.loads(members["card.json"]), card)


if __name__ == "__main__":
    unittest.main()
