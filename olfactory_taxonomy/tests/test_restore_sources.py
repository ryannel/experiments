"""Source restoration must preserve later edits and reject bad archives."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/restore_sources.py'


class RestoreSourcesTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        (self.root / 'data').mkdir()
        (self.root / 'source/images').mkdir(parents=True)
        self.master = self.root / 'source/master.svg'
        self.master.write_text('<svg>my later edits</svg>')
        self.pixels = b'original source image bytes'
        self.archive = self.root / 'working.zip'
        with zipfile.ZipFile(self.archive, 'w') as z:
            z.writestr('source/images/one.png', self.pixels)
            z.writestr('source/master.svg', '<svg>older released master</svg>')
        manifest = {'assets': [{'path': 'images/one.png', 'sha256': hashlib.sha256(self.pixels).hexdigest()}]}
        (self.root / 'source/artwork.json').write_text(json.dumps(manifest))
        package = {'working_source': {'filename': 'working.zip', 'url': 'https://invalid.example/unused', 'bytes': self.archive.stat().st_size, 'sha256': hashlib.sha256(self.archive.read_bytes()).hexdigest()}}
        (self.root / 'data/source-packages.json').write_text(json.dumps(package))
        spec = importlib.util.spec_from_file_location('restore_under_test', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.module.ROOT = self.root

    def restore(self):
        with patch('sys.argv', ['restore_sources.py', '--archive', str(self.archive)]), contextlib.redirect_stdout(io.StringIO()):
            self.module.main()

    def test_restores_only_images_and_is_repeatable(self):
        self.restore()
        self.restore()
        self.assertEqual((self.root / 'source/images/one.png').read_bytes(), self.pixels)
        self.assertEqual(self.master.read_text(), '<svg>my later edits</svg>')

    def test_changed_original_is_never_overwritten(self):
        image = self.root / 'source/images/one.png'
        image.write_bytes(b'my revised photograph')
        with self.assertRaisesRegex(ValueError, 'Existing image differs'):
            self.restore()
        self.assertEqual(image.read_bytes(), b'my revised photograph')
        self.assertEqual(self.master.read_text(), '<svg>my later edits</svg>')

    def test_bad_archive_installs_nothing(self):
        self.archive.write_bytes(b'corrupted archive')
        with self.assertRaisesRegex(ValueError, 'checksum/size mismatch'):
            self.restore()
        self.assertFalse((self.root / 'source/images/one.png').exists())
        self.assertEqual(self.master.read_text(), '<svg>my later edits</svg>')


if __name__ == '__main__':
    unittest.main()
