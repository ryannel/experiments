#!/usr/bin/env python3
"""Verify the portable explorer's local links, tile coverage and dimensions."""
import json
import math
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from PIL import Image
from build_explorer import level_size, tile_box


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        self.urls.extend(value for key, value in attrs if key in ('src', 'href') and value)


def audit_explorer(folder):
    issues = []
    config = json.loads((folder/'map.json').read_text())
    width, height = config['width'], config['height']
    maximum, tile = config['maxLevel'], config['tileSize']
    if maximum != math.ceil(math.log2(max(width, height))) or tile != 512 or config['overlap'] != 1:
        issues.append('Explorer pyramid parameters differ from the renderer/encoder contract.')
    expected = set()
    for mode, metadata in config['modes'].items():
        count = 0
        for level in range(maximum + 1):
            w, h = level_size(width, height, maximum, level)
            for y in range(math.ceil(h/tile)):
                for x in range(math.ceil(w/tile)):
                    path = folder/'tiles'/mode/str(level)/f'{x}_{y}.webp'
                    expected.add(path)
                    if not path.is_file():
                        issues.append(f'Missing tile: {path.relative_to(folder)}')
                        continue
                    left, top, right, bottom = tile_box(w, h, x, y)
                    with Image.open(path) as image:
                        if image.format != 'WEBP' or image.size != (right-left, bottom-top):
                            issues.append(f'Invalid tile dimensions: {path.relative_to(folder)}')
                        image.verify()
                    count += 1
        if count != metadata['tile_count']:
            issues.append(f'Tile count mismatch for {mode}.')
    actual = set((folder/'tiles').rglob('*.webp'))
    if actual != expected:
        issues.append('Tile directory contains missing or unlisted images.')
    parser = Links()
    parser.feed((folder/'index.html').read_text())
    for url in parser.urls:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        if not (folder/unquote(parts.path)).is_file():
            issues.append(f'Explorer link missing: {url}')
    if any((folder/name).exists() for name in ('world-artwork-unlabelled-v1.png','world-labelled-v1.png')):
        issues.append('Do not bundle native PNG masters in the web explorer.')
    return issues


if __name__ == '__main__':
    folder = Path(__file__).resolve().parents[1]/'showcase/explorer'
    issues = audit_explorer(folder)
    if issues:
        raise SystemExit('\n'.join(issues))
    print('Explorer: local links, both tile pyramids and exact edge dimensions pass.')
