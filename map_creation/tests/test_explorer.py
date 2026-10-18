"""Tile pyramid and source-preservation checks; no photographic quality claim."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from PIL import Image, ImageChops, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from build_explorer import build, level_size, tile_box


class ExplorerTests(unittest.TestCase):
    def test_odd_edge_tiles_reconstruct_native_pixels_without_rewriting_source(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source = folder/'painting.png'
            image = Image.new('RGB', (1031, 517))
            image.putdata([((x//20)*4 % 256, (y//20)*8 % 256, 100) for y in range(517) for x in range(1031)])
            image.save(source)
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            config = build({'artwork': source}, folder/'viewer', quality=95)
            self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())
            maximum = config['maxLevel']
            self.assertEqual(level_size(1031, 517, maximum, maximum-1), (516, 259))
            joined = Image.new('RGB', image.size)
            for y in range(2):
                for x in range(3):
                    box = tile_box(*image.size, x, y)
                    with Image.open(folder/'viewer/tiles/artwork'/str(maximum)/f'{x}_{y}.webp') as tile:
                        joined.paste(tile, box[:2])
            self.assertLess(max(ImageStat.Stat(ImageChops.difference(image, joined)).mean), 4)
            self.assertEqual(config['modes']['artwork']['source_file'], 'painting.png')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                build({'artwork': source}, folder/'viewer')

    def test_mismatched_modes_are_not_installed(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            Image.new('RGB', (32, 24)).save(folder/'a.png')
            Image.new('RGB', (32, 25)).save(folder/'b.png')
            with self.assertRaisesRegex(ValueError, 'identical dimensions'):
                build({'artwork': folder/'a.png', 'labels': folder/'b.png'}, folder/'viewer')
            self.assertFalse((folder/'viewer/tiles').exists())
            self.assertFalse((folder/'viewer/map.json').exists())


if __name__ == '__main__':
    unittest.main()
