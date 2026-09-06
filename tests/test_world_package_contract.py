import importlib.util
from pathlib import Path
import tempfile
import unittest
import hashlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("world_package", ROOT / "shared/validators/world_package.py")
world_package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(world_package)


class WorldPackageTests(unittest.TestCase):
    def test_valid_manifest_and_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            names = ["world.charx", "card.json", "lore.json", "guide.md", "passport.json", "book.json", "compile.json"]
            artifacts = []
            for i, name in enumerate(names):
                path = root / name
                path.write_text(name, encoding="utf-8")
                role = ["charx", "card_source", "loreforge_source", "import_guide", "artifact_passport", "character_book_backup", "compilation_manifest"][i]
                artifacts.append({"id": role, "role": role, "path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
            manifest = {"schema": world_package.SCHEMA_ID, "project_id": "p", "profile": "narrator_world", "native_lumiverse_full_fidelity": False, "artifacts": artifacts}
            self.assertEqual(world_package.validate_world_package(manifest, root), [])

    def test_missing_role_and_hash_fail(self):
        manifest = {"schema": world_package.SCHEMA_ID, "project_id": "p", "profile": "narrator_world", "native_lumiverse_full_fidelity": False, "artifacts": []}
        codes = {f["code"] for f in world_package.validate_world_package(manifest)}
        self.assertIn("missing-required-artifact", codes)

    def test_native_fidelity_requires_template(self):
        manifest = {"schema": world_package.SCHEMA_ID, "project_id": "p", "profile": "narrator_world", "native_lumiverse_full_fidelity": True, "native_template_evidence": [], "artifacts": []}
        self.assertIn("unsupported-fidelity-claim", {f["code"] for f in world_package.validate_world_package(manifest)})


if __name__ == "__main__":
    unittest.main()
