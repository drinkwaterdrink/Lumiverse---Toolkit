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
    @staticmethod
    def artifact(role, name=None):
        name = name or f"{role}.json"
        return {"id": role, "role": role, "path": name, "sha256": "0" * 64}

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

    def test_single_character_does_not_require_lorebook_artifacts(self):
        roles = ["charx", "card_source", "import_guide", "artifact_passport"]
        manifest = {
            "schema": world_package.SCHEMA_ID,
            "project_id": "p",
            "profile": "single_character",
            "native_lumiverse_full_fidelity": False,
            "artifacts": [self.artifact(role) for role in roles],
        }
        self.assertEqual(world_package.validate_world_package(manifest), [])

    def test_narrator_world_requires_lorebook_artifacts(self):
        roles = ["charx", "card_source", "import_guide", "artifact_passport"]
        manifest = {
            "schema": world_package.SCHEMA_ID,
            "project_id": "p",
            "profile": "narrator_world",
            "native_lumiverse_full_fidelity": False,
            "artifacts": [self.artifact(role) for role in roles],
        }
        messages = [f["message"] for f in world_package.validate_world_package(manifest)]
        self.assertTrue(any("loreforge_source" in message for message in messages))
        self.assertTrue(any("character_book_backup" in message for message in messages))

    def test_no_profile_requires_a_preset(self):
        self.assertNotIn("loom_preset", world_package.required_roles("narrator_world"))
        self.assertNotIn("loom_preset", world_package.required_roles("multi_card_world"))


if __name__ == "__main__":
    unittest.main()
