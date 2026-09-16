#!/usr/bin/env python3
"""Audit maintained kit files; work directories are intentionally outside scope."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = ('README.md','AGENTS.md','CREDITS.md','LICENSE.md','requirements.txt','.gitignore')
SOURCE_DIRS = ('.agents','docs','templates','examples','showcase','scripts','tests')
IGNORED_PARTS = {'__pycache__','.pytest_cache','.DS_Store'}
EXTENSIONS = {'.md','.json','.py','.txt','.yaml','.yml','.jpg','.png','.svg'}


def selected_files(root):
    paths=[]
    for name in ROOT_FILES:
        p=root/name
        if not p.is_file():
            raise ValueError(f'Missing required root file: {name}')
        paths.append(p)
    for name in SOURCE_DIRS:
        folder=root/name
        if not folder.is_dir():
            raise ValueError(f'Missing required source directory: {name}')
        for p in folder.rglob('*'):
            if any(part in IGNORED_PARTS for part in p.relative_to(root).parts) or p.suffix=='.pyc':
                continue
            if p.is_symlink():
                raise ValueError(f'Symlink not allowed in package: {p.relative_to(root)}')
            if p.is_file():
                if p.suffix not in EXTENSIONS:
                    raise ValueError(f'Unexpected file type: {p.relative_to(root)}')
                paths.append(p)
    for p in paths:
        if p.is_symlink():
            raise ValueError(f'Symlink not allowed: {p}')
    return sorted(paths)


def audit(root):
    files=selected_files(root)
    selected={p.resolve() for p in files}
    issues=[]
    for p in files:
        rel=p.relative_to(root).as_posix()
        if p.suffix in {'.jpg','.png'}:
            with Image.open(p) as im:
                if im.width>1600:
                    issues.append(f'{rel}: showcase/example image wider than 1600 px')
                im.verify()
            continue
        content=p.read_text(encoding='utf-8')
        if p.suffix=='.json':
            json.loads(content)
        if re.search(r'/(?:Users|home)/[A-Za-z0-9_-]+/',content):
            issues.append(f'{rel}: machine-specific home path')
        if re.search(r'\bsk-[A-Za-z0-9_-]{20,}',content):
            issues.append(f'{rel}: possible credential')
        if p.suffix=='.md':
            # Ignore fenced code before checking normal inline Markdown links.
            body=re.sub(r'```.*?```','',content,flags=re.S)
            for target in re.findall(r'\]\(([^)]+)\)',body):
                target=target.split('#',1)[0].split(' "',1)[0]
                if not target or re.match(r'^[a-zA-Z]+:',target):
                    continue
                destination=(p.parent/unquote(target)).resolve()
                if destination not in selected:
                    issues.append(f'{rel}: missing or unbundled link: {target}')
        if p.name=='SKILL.md':
            match=re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n',content)
            if not match or match[1]!=p.parent.name:
                issues.append(f'{rel}: invalid skill name/frontmatter')
    provenance=json.loads((root/'showcase/provenance.json').read_text())
    art=root/'showcase'/provenance['file']
    if hashlib.sha256(art.read_bytes()).hexdigest()!=provenance['sha256']:
        issues.append('Showcase hash differs from provenance.')
    with Image.open(art) as im:
        if list(im.size)!=provenance['dimensions']:
            issues.append('Showcase dimensions differ from provenance.')
    return files,issues


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args()
    try:
        files,issues=audit(args.root.resolve())
    except (ValueError,OSError) as e:
        parser.exit(1,f'Package audit failed: {e}\n')
    if issues:
        parser.exit(1,'\n'.join(issues)+'\n')
    print(f'Checked {len(files)} maintained files: links, skills, JSON, images, provenance and basic privacy patterns pass.')
    print('This is not a visual approval or an exhaustive secret/license audit.')


if __name__=='__main__':
    main()
