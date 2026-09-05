import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/lumiverse-character-forge/scripts/package_charx.py'
spec = importlib.util.spec_from_file_location('charx', SCRIPT)
charx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(charx)


class CharxTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.card = {'spec': 'chara_card_v3', 'spec_version': '3.0', 'data': {'name': 'Test', 'description': '{{user}}', 'extensions': {'future': [1, 2]}}}
        self.output = self.root / 'test.charx'

    def test_new_card_preserves_json(self):
        charx.package(self.card, self.output)
        self.assertEqual(json.loads(charx.read_archive(self.output)['card.json']), self.card)

    def test_source_book_unknown_fields_and_assets_preserved(self):
        self.card['unknown'] = {'opaque': True}
        self.card['data']['character_book'] = {'entries': [{'content': 'Lore', 'custom': 42}]}
        self.card['data']['assets'] = [{'uri': 'embeded://assets/icon.webp'}]
        source = self.root / 'source.charx'
        with zipfile.ZipFile(source, 'w') as z:
            z.writestr('assets/icon.webp', b'opaque-test-bytes')
            z.writestr('extra.bin', b'unknown-resource')
            z.writestr('card.json', '{}')
        charx.package(self.card, self.output, source)
        result = charx.read_archive(self.output)
        self.assertEqual(result['extra.bin'], b'unknown-resource')
        self.assertEqual(result['assets/icon.webp'], b'opaque-test-bytes')
        self.assertEqual(json.loads(result['card.json']), self.card)

    def test_missing_asset_rejected(self):
        self.card['data']['assets'] = [{'uri': 'embeded://missing.png'}]
        with self.assertRaises(ValueError): charx.package(self.card, self.output)
        self.assertFalse(self.output.exists())

    def test_traversal_rejected(self):
        source = self.root / 'bad.zip'
        with zipfile.ZipFile(source, 'w') as z: z.writestr('../escape', 'bad')
        with self.assertRaises(ValueError): charx.package(self.card, self.output, source)

    def test_existing_output_never_overwritten(self):
        self.output.write_bytes(b'keep')
        with self.assertRaises(FileExistsError): charx.package(self.card, self.output)
        self.assertEqual(self.output.read_bytes(), b'keep')

    def test_wrong_envelope_rejected(self):
        self.card['spec_version'] = '2.0'
        with self.assertRaises(ValueError): charx.package(self.card, self.output)

    def test_assets_directory(self):
        assets = self.root / 'resources'
        (assets / 'assets').mkdir(parents=True)
        (assets / 'assets/test.bin').write_bytes(b'asset')
        self.card['data']['assets'] = [{'uri': 'embeded://assets/test.bin'}]
        charx.package(self.card, self.output, assets_dir=assets)
        self.assertEqual(charx.read_archive(self.output)['assets/test.bin'], b'asset')
