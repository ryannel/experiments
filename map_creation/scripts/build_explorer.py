#!/usr/bin/env python3
"""Encode explicitly selected public atlas paintings into a static WebP pyramid.

The offline encoder decodes one source at a time. The browser never loads a master.
No setting documents, SVGs, prompts or private source paths are copied.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import tempfile
import shutil
from PIL import Image

TILE = 512
OVERLAP = 1


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def level_size(width, height, maximum, level):
    factor = 2 ** (maximum - level)
    return math.ceil(width / factor), math.ceil(height / factor)


def tile_box(width, height, x, y):
    return (max(0, x * TILE - OVERLAP), max(0, y * TILE - OVERLAP),
            min(width, (x + 1) * TILE + OVERLAP), min(height, (y + 1) * TILE + OVERLAP))


def build(sources, output, quality=90):
    output = Path(output)
    if (output / 'tiles').exists() or (output / 'map.json').exists():
        raise ValueError('Tile output already exists. Build in a fresh folder before replacing a reviewed delivery.')
    # This selected 100MP atlas exceeds Pillow's default warning threshold.
    # Keep a ceiling rather than disable decompression protection globally.
    previous_limit = Image.MAX_IMAGE_PIXELS
    Image.MAX_IMAGE_PIXELS = 200_000_000
    output.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='atlas-tiles-') as temporary:
            staging = Path(temporary)
            dimensions = None
            records = {}
            for mode, source in sources.items():
                source = Path(source)
                with Image.open(source) as opened:
                    if opened.width * opened.height > 200_000_000:
                        raise ValueError('Source exceeds this encoder’s 200-megapixel limit.')
                    if dimensions is not None and dimensions != opened.size:
                        raise ValueError('Artwork and labelled paintings must have identical dimensions.')
                    dimensions = opened.size
                    width, height = dimensions
                    maximum = math.ceil(math.log2(max(dimensions)))
                    count = 0
                    image = opened.convert('RGB')
                    try:
                        for level in range(maximum + 1):
                            w, h = level_size(width, height, maximum, level)
                            scaled = image if level == maximum else image.resize((w, h), Image.Resampling.LANCZOS)
                            folder = staging / 'tiles' / mode / str(level)
                            folder.mkdir(parents=True)
                            try:
                                for y in range(math.ceil(h / TILE)):
                                    for x in range(math.ceil(w / TILE)):
                                        with scaled.crop(tile_box(w, h, x, y)) as tile:
                                            tile.save(folder / f'{x}_{y}.webp', 'WEBP', quality=quality, method=6, exif=b'')
                                        count += 1
                            finally:
                                if scaled is not image:
                                    scaled.close()
                    finally:
                        image.close()
                records[mode] = {'source_file': source.name, 'source_sha256': digest(source), 'tile_count': count}
            if not records:
                raise ValueError('At least one explicitly selected painting is required.')
            config = {'title': 'The Lantern Sea', 'width': width, 'height': height,
                      'tileSize': TILE, 'overlap': OVERLAP, 'maxLevel': maximum,
                      'quality': quality, 'modes': records,
                      'revision': hashlib.sha256(json.dumps({'sources': records, 'quality': quality, 'tileSize': TILE, 'overlap': OVERLAP}, sort_keys=True).encode()).hexdigest()[:12],
                      'source_release': 'world-atlas-complete-v1',
                      'review_status': 'Source record: agent review complete; user review of the eastern expansion pending.',
                      'delivery': 'Lossy WebP tiles at native dimensions; original PNG masters remain in the source project.'}
            shutil.move(str(staging / 'tiles'), output / 'tiles')
            (output / 'map.json').write_text(json.dumps(config, indent=2) + '\n')
    finally:
        Image.MAX_IMAGE_PIXELS = previous_limit
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artwork', required=True, type=Path)
    parser.add_argument('--labelled', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--quality', type=int, default=90, choices=range(1, 101), metavar='1–100')
    args = parser.parse_args()
    sources = {'artwork': args.artwork}
    if args.labelled:
        sources['labels'] = args.labelled
    try:
        config = build(sources, args.output, args.quality)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Encoding failed: {error}\n')
    print(f"Encoded {config['width']} × {config['height']}: {sum(m['tile_count'] for m in config['modes'].values())} tiles. Source files unchanged.")


if __name__ == '__main__':
    main()
