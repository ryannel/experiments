#!/usr/bin/env python3
"""Restore checksum-verified image assets without replacing editable project files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(chunk)
    return checksum.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, help='Use an already downloaded ZIP')
    args = parser.parse_args()
    package = json.loads((ROOT / 'data/source-packages.json').read_text())['working_source']
    manifest = json.loads((ROOT / 'source/artwork.json').read_text())
    base = ROOT / 'source'
    prefix = 'images'
    pending = []
    for asset in manifest['assets']:
        rel = PurePosixPath(asset['path'])
        if rel.is_absolute() or '..' in rel.parts or rel.parts[0] != prefix:
            raise ValueError(f'Invalid image path: {rel}')
        path = base / str(rel)
        if path.is_symlink():
            raise ValueError(f'Refusing symlink destination: {rel}')
        if path.exists():
            if not path.is_file() or digest(path) != asset['sha256']:
                raise ValueError(f'Existing image differs: {rel}. It has been preserved. For an intentional edit, update its manifest entry; otherwise move it aside before restoring.')
        else:
            pending.append((asset, path))
    if not pending:
        print(f'All {len(manifest["assets"])} images are already installed and checksum-verified.')
        return
    cache = ROOT / 'build/downloads'
    cache.mkdir(parents=True, exist_ok=True)
    archive = args.archive
    if archive is None:
        archive = cache / package['filename']
        if not archive.exists():
            partial = archive.with_suffix('.download')
            print(f'Downloading {package["filename"]} ({package["bytes"]:,} bytes)…', flush=True)
            try:
                with urlopen(Request(package['url'], headers={'User-Agent': 'Olfactory-Atlas-source-restore'}), timeout=120) as response, partial.open('wb') as out:
                    shutil.copyfileobj(response, out)
                if partial.stat().st_size != package['bytes'] or digest(partial) != package['sha256']:
                    raise ValueError('Downloaded archive checksum/size mismatch; no images have been installed.')
                partial.replace(archive)
            finally:
                partial.unlink(missing_ok=True)
    if archive.stat().st_size != package['bytes'] or digest(archive) != package['sha256']:
        raise ValueError('Archive checksum/size mismatch; no images have been installed.')
    # Stage and verify every missing asset before writing any project image.
    with zipfile.ZipFile(archive) as source, tempfile.TemporaryDirectory(prefix='restore-', dir=cache) as folder:
        staged = []
        for i, (asset, destination) in enumerate(pending):
            member = 'source/' + asset['path']
            temp = Path(folder) / str(i)
            with source.open(member) as stream, temp.open('wb') as out:
                shutil.copyfileobj(stream, out)
            if digest(temp) != asset['sha256']:
                raise ValueError(f'Image checksum mismatch: {member}. No images have been installed.')
            staged.append((temp, destination))
        for temp, destination in staged:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open('xb') as out, temp.open('rb') as stream:
                shutil.copyfileobj(stream, out)
    print(f'Restored {len(pending)} original images. Existing SVGs, prompts, metadata and images were preserved.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        raise SystemExit(str(error))
