#!/usr/bin/env python3
"""Validate the distributable exhibit using only the Python standard library."""
import argparse,hashlib,json,math,re,struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NS='{http://www.w3.org/2000/svg}'

def require(condition,message):
    if not condition:raise ValueError(message)

class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        self.urls += [v for k,v in attrs if k in ('href','src') and v]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--originals',action='store_true');args=parser.parse_args()
    cfg=json.loads((ROOT/'data/explorer.json').read_text());cells=json.loads((ROOT/'data/cells.json').read_text())
    wheel=ET.parse(ROOT/'source/master.svg').getroot()
    labels={t.get('data-cell'):' '.join(''.join(t.itertext()).split()) for t in wheel.iter(NS+'text') if t.get('data-cell')}
    require(len(labels)==318 and labels=={c['id']:c['text'] for c in cells},'Cell labels do not match the master')
    for field,count in [('realm',4),('family',20),('note',48),('descriptors',82),('texture_tactile',82),('reference_material',82)]:
        ring=sorted([c for c in cells if c['field']==field],key=lambda c:c['start'])
        require(len(ring)==count,f'Incorrect count for {field}')
        end=0
        for cell in ring:
            require(abs(cell['start']-end)<1e-6,f'Gap/overlap in {field}')
            require(cell['outer']>cell['inner']>=0,f'Invalid radii in {field}')
            end=cell['end']
        require(abs(end-360)<1e-6,f'Incomplete {field} coverage')
    ids={e.get('id') for e in wheel.iter() if e.get('id')}
    for ref in re.findall(r'url\(#([^)]*)\)|href="#([^"]*)"',(ROOT/'source/master.svg').read_text()):
        require((ref[0] or ref[1]) in ids,'Dangling SVG reference')
    manifest=json.loads((ROOT/'source/artwork.json').read_text())
    assets=manifest['assets'];require(len(assets)==130,'Expected 130 source photographs')
    require({im.get('href') for im in wheel.iter(NS+'image')}=={a['path'] for a in assets},'Artwork manifest differs from SVG')
    for a in assets:
        require((ROOT/'source'/a['prompt']).is_file(),f'Missing prompt: {a["id"]}')
        if args.originals:
            p=ROOT/'source'/a['path'];require(p.is_file(),f'Install source archive; missing {p.name}')
            data=p.read_bytes();require(hashlib.sha256(data).hexdigest()==a['sha256'],f'Original hash changed: {p.name}')
            require(data[:8]==b'\x89PNG\r\n\x1a\n','Original must be PNG')
            require(list(struct.unpack('>II',data[16:24]))==a['dimensions_px'],f'Dimensions changed: {p.name}')
    tile_count=0
    for mode in cfg['modes']:
        dzi=ET.parse(ROOT/f'exhibit/{mode}.dzi').getroot();dzin='{http://schemas.microsoft.com/deepzoom/2008}'
        require(dzi.get('TileSize')==str(cfg['tileSize']) and dzi.get('Overlap')==str(cfg['overlap']),'Tile metadata mismatch')
        size=dzi.find(dzin+'Size');require(size.get('Width')==str(cfg['size']) and size.get('Height')==str(cfg['size']),'Pyramid size mismatch')
        for level in range(cfg['maxLevel']+1):
            side=math.ceil(cfg['size']/2**(cfg['maxLevel']-level));tiles=math.ceil(side/cfg['tileSize'])
            for y in range(tiles):
                for x in range(tiles):
                    p=ROOT/f'exhibit/{mode}_files/{level}/{x}_{y}.webp';require(p.is_file(),f'Missing tile: {p.relative_to(ROOT)}')
                    with p.open('rb') as f:header=f.read(12)
                    require(header[:4]==b'RIFF' and header[8:]==b'WEBP',f'Invalid WebP: {p.name}')
                    tile_count+=1
    for page in [ROOT/'index.html',ROOT/'exhibit/index.html']:
        links=Links();links.feed(page.read_text())
        for url in links.urls:
            parts=urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:continue
            require((page.parent/unquote(parts.path)).is_file(),f'Broken local link in {page.name}: {url}')
    avif=(ROOT/'exports/olfactory-atlas.avif').read_bytes()
    require(b'avif' in avif[:64],'Invalid AVIF export')
    print(f'Validated {len(labels)} labels, six complete rings, {len(assets)} assets, {tile_count} tiles and local exhibit links.'+(' All original PNG checksums verified.' if args.originals else ' Originals are optional for viewing.'))

if __name__=='__main__':main()
