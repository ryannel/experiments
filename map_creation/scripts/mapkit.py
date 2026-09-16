#!/usr/bin/env python3
"""Offline, small-map production helper. Painting and visual judgment are external."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = Path(__file__).resolve().parents[1]
MAX_PIXELS = 16_000_000
CHECKS = ('style', 'geography', 'routes', 'structures', 'joins', 'required_sites', 'mask_perimeter')
SLUG = re.compile(r'^[a-z0-9][a-z0-9_-]{0,63}$')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.writing')
    temporary.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def slug(value):
    require(bool(SLUG.fullmatch(value)), 'Use a lowercase ID with letters, numbers, hyphens or underscores (max 64).')
    return value


def inside(root, relative):
    require(isinstance(relative, str) and relative, 'Expected a project-relative file path.')
    p = Path(relative)
    require(not p.is_absolute(), 'Absolute paths are not allowed in project records.')
    target = (root / p).resolve()
    require(target.is_relative_to(root.resolve()), 'Path escapes project root.')
    return target


def text_field(item, key):
    require(isinstance(item.get(key), str) and bool(item[key].strip()), f'Missing text field: {key}')


def validate_world(w):
    require(isinstance(w, dict), 'World must be a JSON object.')
    require(w.get('version') == 1, 'Expected world format version 1.')
    text_field(w, 'name')
    canvas = w.get('canvas', {})
    width, height = canvas.get('width'), canvas.get('height')
    require(type(width) is int and type(height) is int and width > 0 and height > 0, 'Positive integer canvas dimensions required.')
    require(width * height <= MAX_PIXELS, 'Canvas exceeds 16 million pixels; see docs/scaling.md.')
    collections = ('land', 'regions', 'rivers', 'roads', 'settlements', 'factions')
    all_ids = set()
    for key in collections:
        require(isinstance(w.get(key), list), f'{key} must be an array.')
        for item in w[key]:
            require(isinstance(item, dict), f'{key} entries must be objects.')
            text_field(item, 'id')
            require(item['id'] not in all_ids, f'Duplicate ID: {item["id"]}')
            all_ids.add(item['id'])
    require(bool(w['land']), 'At least one land polygon is required.')

    def point(p):
        require(isinstance(p, list) and len(p) == 2, 'Point must be [x, y].')
        require(all(type(n) in (int, float) and math.isfinite(n) for n in p), 'Coordinates must be finite numbers.')
        require(0 <= p[0] < width and 0 <= p[1] < height, f'Point outside canvas: {p}')

    def points(item, key, minimum):
        value = item.get(key)
        require(isinstance(value, list) and len(value) >= minimum, f'{item["id"]}: {key} needs {minimum} points.')
        for p in value:
            point(p)

    for item in w['land'] + w['regions']:
        points(item, 'polygon', 3)
    for item in w['regions']:
        require(item.get('kind') in ('forest', 'upland', 'farmland', 'wetland'), 'Unknown region kind.')
    factions = {f['id'] for f in w['factions']}
    for f in w['factions']:
        text_field(f, 'name')
        require(f.get('kind') in ('state', 'community', 'network'), 'Unknown faction kind.')
    sites = {s['id']: s for s in w['settlements']}
    for s in sites.values():
        text_field(s, 'name')
        text_field(s, 'role')
        point(s.get('point'))
        require(s.get('faction') is None or s['faction'] in factions, f'{s["id"]}: unknown faction.')
        pop = s.get('population')
        require(pop is None or type(pop) is int and pop >= 0, 'Population must be null or a nonnegative integer.')
        require(s.get('status') in ('planned', 'painted', 'moved', 'deferred', 'unresolved'), 'Invalid site status.')
    rivers = {r['id']: r for r in w['rivers']}
    for r in rivers.values():
        points(r, 'points', 2)
        require(type(r.get('width')) in (int, float) and 0 < r['width'] <= 128, 'River width must be > 0 and <= 128 pixels.')
        downstream = r.get('downstream')
        require(downstream in ('sea', 'closed-basin') or downstream in rivers, f'{r["id"]}: unknown downstream ID.')
        if downstream in rivers:
            require(r['points'][-1] in rivers[downstream]['points'], f'{r["id"]}: endpoint must equal a vertex in the receiving river.')
        seen = {r['id']}
        while downstream in rivers:
            require(downstream not in seen, 'River network has a downstream cycle.')
            seen.add(downstream)
            downstream = rivers[downstream].get('downstream')
    for r in w['roads']:
        points(r, 'points', 2)
        require(r.get('from') in sites and r.get('to') in sites, 'Road endpoints must reference settlement IDs.')
        require(r['points'][0] == sites[r['from']]['point'] and r['points'][-1] == sites[r['to']]['point'], 'Road endpoints must match referenced settlement anchors.')
    return w


def world(project):
    return validate_world(read(project / 'world.json'))


def state(project):
    return read(project / 'metadata/state.json')


def fingerprint(project):
    data = state(project)
    files = ['world.json', 'style.json']
    references = read(project / 'style.json').get('reference_files', [])
    require(isinstance(references, list), 'style.reference_files must be project-relative path strings.')
    for ref in references:
        require(inside(project, ref).is_file(), f'Missing style reference: {ref}')
        files.append(ref)
    if data.get('base'):
        files.append(data['base']['file'])
        require(sha(inside(project, data['base']['file'])) == data['base']['sha256'], 'Base image changed.')
    for item in data['accepted']:
        file = inside(project, item['file'])
        require(sha(file) == item['sha256'], 'Accepted source changed; restore it before continuing.')
        files.append(item['file'])
        require(sha(inside(project, item['review_file'])) == item['review_sha256'], 'Accepted review changed.')
    return {'revision': data['revision'], 'files': {p: sha(inside(project, p)) for p in files}}


def font(size):
    # Pillow's bundled font avoids machine-specific font paths.
    return ImageFont.load_default(size=size)


def guide_image(w, style, labels=False):
    width, height = w['canvas']['width'], w['canvas']['height']
    colors = style['palette']
    img = Image.new('RGB', (width, height), colors['water'])
    d = ImageDraw.Draw(img)
    for land in w['land']:
        poly = [tuple(p) for p in land['polygon']]
        d.polygon(poly, fill=colors['land'])
        d.line(poly + poly[:1], fill='#9caeaa', width=3)
    for r in w['regions']:
        fill = {'forest': colors['forest'], 'upland': colors['upland'], 'farmland': '#c6ba78', 'wetland': '#839b82'}[r['kind']]
        d.polygon([tuple(p) for p in r['polygon']], fill=fill)
    for r in w['rivers']:
        pts = [tuple(p) for p in r['points']]
        d.line(pts, fill='#a7c5bc', width=round(r['width']) + 4, joint='curve')
        d.line(pts, fill=colors['water'], width=round(r['width']), joint='curve')
    for r in w['roads']:
        d.line([tuple(p) for p in r['points']], fill=colors['road'], width=4, joint='curve')
    for s in w['settlements']:
        x, y = s['point']
        radius = 10 if s['role'] == 'capital' else 6
        d.ellipse((x-radius, y-radius, x+radius, y+radius), fill='#f4e9c9', outline=colors['ink'], width=2)
        if labels:
            d.text((x+14,y-8),s['name'],font=font(19),fill=colors['ink'],stroke_width=2,stroke_fill=colors['land'])
    return img


def preview(img, path):
    result = img.convert('RGB').copy()
    result.thumbnail((1600, 1600))
    path.parent.mkdir(parents=True, exist_ok=True)
    result.save(path, quality=88)


def compose(project):
    w = world(project)
    data = state(project)
    fingerprint(project)
    if data.get('base'):
        with Image.open(inside(project, data['base']['file'])) as im:
            img = im.convert('RGB')
    else:
        img = guide_image(w, read(project / 'style.json'))
    for item in data['accepted']:
        x, y, width, height = item['rect']
        with Image.open(inside(project, item['file'])) as tile:
            require(tile.size == (width, height), 'Accepted tile dimensions changed.')
            img.paste(tile.convert('RGB'), (x, y))
    return img


def new(args):
    project = Path(args.output).resolve()
    require(not project.exists(), 'Output already exists; choose a new project directory.')
    w = validate_world(read(args.world or ROOT / 'examples/bracken-reach/world.json'))
    if args.base:
        with Image.open(args.base) as im:
            require(im.size == (w['canvas']['width'], w['canvas']['height']), 'Base dimensions must match --world. Supply a world model aligned to the base image.')
    project.mkdir(parents=True)
    for folder in ('planning','metadata','iterations','previews','assets/masters','private','releases'):
        (project / folder).mkdir(parents=True)
    write(project / 'world.json', w)
    shutil.copy2(ROOT / 'templates/style.json', project / 'style.json')
    for f in ('brief.md','societies.md','decisions.md'):
        shutil.copy2(ROOT / 'templates' / f, project / 'planning' / f)
    (project / '.gitignore').write_text('private/\n.env\n.env.*\n__pycache__/\n', encoding='utf-8')
    baseline = None
    if args.base:
        dest = project / 'assets/masters/base-v1.png'
        with Image.open(args.base) as im:
            im.convert('RGB').save(dest)
        original = project / 'assets/masters' / ('base-original' + Path(args.base).suffix.lower())
        shutil.copy2(args.base, original)
        baseline = {'file': dest.relative_to(project).as_posix(), 'sha256': sha(dest), 'review_status': 'imported; not visually reviewed by this helper'}
    write(project / 'metadata/state.json', {'version':1,'revision':0,'base':baseline,'accepted':[]})
    print(f'Created {project.name}. Edit world.json, style.json and planning/ before painting.')


def guide(args):
    project = Path(args.project).resolve()
    w = world(project)
    output = project / 'previews'
    preview(guide_image(w,read(project/'style.json'),labels=True), output/'guide.jpg')
    print('Wrote previews/guide.jpg (schematic planning guide).')


def candidate(project, candidate_id):
    return project / 'iterations' / slug(candidate_id)


def verify_prepared(project, folder):
    info = read(folder / 'prepared.json')
    require(info['inputs'] == fingerprint(project), 'Candidate is stale: prepare a new ID using current inputs.')
    for filename, digest in info['prepared_files'].items():
        require(sha(folder / filename) == digest, f'Prepared input changed: {filename}')
    return info


def prepare(args):
    project = Path(args.project).resolve()
    w = world(project)
    folder = candidate(project,args.candidate)
    require(not folder.exists(), 'Candidate ID already exists; use a new version.')
    x,y,width,height = args.rect
    require(x >= 0 and y >= 0 and width > 0 and height > 0 and x+width <= w['canvas']['width'] and y+height <= w['canvas']['height'], 'Rectangle outside canvas.')
    mask = None
    if args.mask:
        require(bool(state(project)['accepted']) or bool(state(project).get('base')), 'Refinement needs accepted artwork or an imported base.')
        with Image.open(args.mask) as im:
            require(im.size == (width,height), 'Mask must match the local rectangle size.')
            require(im.mode == 'L', 'Mask must be an 8-bit grayscale (L) image.')
            mask = im.copy()
            require(mask.getbbox() is not None, 'Mask cannot be entirely black.')
    inputs = fingerprint(project)
    base = compose(project)
    folder.mkdir(parents=True)
    rect = (x,y,x+width,y+height)
    shutil.copy2(project/'world.json', folder/'world.json')
    shutil.copy2(project/'style.json', folder/'style.json')
    reference_copies = []
    for number, ref in enumerate(read(project/'style.json').get('reference_files', []), 1):
        original = inside(project, ref)
        filename = f'reference-{number}{original.suffix}'
        shutil.copy2(original, folder/filename)
        reference_copies.append(filename)
    base.crop(rect).save(folder/'prior.png')
    guide_image(w,read(project/'style.json')).crop(rect).save(folder/'guide.png')
    if mask:
        mask.save(folder/'mask.png')
    context = base.copy()
    ImageDraw.Draw(context).rectangle((x,y,x+width-1,y+height-1),outline='#f46247',width=4)
    preview(context,folder/'context.jpg')
    sites = [s for s in w['settlements'] if x <= s['point'][0] < x+width and y <= s['point'][1] < y+height]
    mode = 'refine' if mask else 'paint'
    prompt = f'''# Candidate {args.candidate}\n\nMode: {mode}\nNative output: {width} x {height}\nWorld rectangle: {args.rect}\nWorld: {w['name']}\n\n'''
    prompt += 'Use prior.png as the edit target; change only the masked feature.\n' if mask else 'Use guide.png as structural intent and prior.png/context.jpg as current map context.\n'
    prompt += 'Match the selected style reference and style.json. Keep geography, connected routes and required sites. No lettering. Inspect all affected neighbours; reference context does not guarantee preservation.\n\nRequired site anchors (local pixels):\n'
    for s in sites:
        prompt += f"- {s['id']}: {s['name']} ({s['role']}) at [{s['point'][0]-x}, {s['point'][1]-y}]\n"
    if not sites:
        prompt += '- No planned settlement anchors in this rectangle.\n'
    prompt += '\nBefore submitting, add regional intent, all crossing obligations and reference image roles to your exact submitted prompt. Record that final text in provenance.json. The prepared prompt is a starting brief, not a complete geography contract.\n'
    (folder/'prompt.md').write_text(prompt,encoding='utf-8')
    files = ['world.json','style.json','prior.png','guide.png','context.jpg','prompt.md'] + reference_copies + (['mask.png'] if mask else [])
    write(folder/'prepared.json',{'candidate':args.candidate,'mode':mode,'rect':args.rect,'inputs':inputs,'required_sites':[s['id'] for s in sites],'style_reference_copies':reference_copies,'prepared_files':{f:sha(folder/f) for f in files}})
    print(f'Prepared iterations/{args.candidate}. Paint externally, then ingest the lossless output.')


def ingest(args):
    project = Path(args.project).resolve()
    folder = candidate(project,args.candidate)
    info = verify_prepared(project,folder)
    require(not (folder/'ingested.json').exists(), 'Candidate already ingested; use a new ID for a new attempt.')
    provenance = read(args.provenance)
    for key in ('tool','prompt'):
        text_field(provenance,key)
        require(not provenance[key].startswith('REPLACE'), f'Complete provenance field: {key}')
    require(type(provenance.get('calls')) is int and provenance['calls'] >= 0, 'Provenance requires actual call count; use 0 for manual/offline fixtures.')
    image_path = Path(args.image)
    with Image.open(image_path) as im:
        require(im.format == 'PNG', 'Supply a lossless PNG master; retain other formats separately.')
        require(im.size == tuple(info['rect'][2:]), 'Returned dimensions differ from target. Retain original and prepare a compatible new candidate; no automatic scaling.')
        require(im.mode in ('RGB','RGBA'), 'Painting must be RGB or RGBA.')
        if im.mode == 'RGBA':
            require(im.getextrema()[3] == (255,255), 'Terrain painting must be opaque.')
        generated = im.convert('RGB')
    require(provenance.get('native_dimensions') == list(generated.size), 'Provenance native_dimensions must match the actual image.')
    output = generated
    if info['mode'] == 'refine':
        with Image.open(folder/'prior.png') as prior, Image.open(folder/'mask.png') as mask:
            output = Image.composite(generated,prior.convert('RGB'),mask)
    shutil.copy2(image_path,folder/'returned-master.png')
    output.save(folder/'integrated.png')
    write(folder/'provenance.json',provenance)
    write(folder/'ingested.json',{'files':{f:sha(folder/f) for f in ('returned-master.png','integrated.png','provenance.json')},'native_dimensions':list(generated.size)})
    print('Retained returned-master.png and integrated.png. Run inspect and review the actual pixels.')


def verify_ingested(folder):
    info=read(folder/'ingested.json')
    for filename,digest in info['files'].items():
        require(sha(folder/filename)==digest, f'Ingested file changed: {filename}')
    return info


def inspect(args):
    project=Path(args.project).resolve()
    folder=candidate(project,args.candidate)
    info=verify_prepared(project,folder)
    verify_ingested(folder)
    assembled=compose(project)
    x,y,width,height=info['rect']
    with Image.open(folder/'integrated.png') as tile:
        assembled.paste(tile,(x,y))
    evidence=folder/'evidence'
    evidence.mkdir(exist_ok=True)
    preview(assembled,evidence/'overview.jpg')
    # Cover the whole target plus a 96-pixel collar with overlapping native crops.
    left,top=max(0,x-96),max(0,y-96)
    right,bottom=min(assembled.width,x+width+96),min(assembled.height,y+height+96)
    records=[]
    for yy in range(top,bottom,640):
        for xx in range(left,right,640):
            bounds=[xx,yy,min(xx+768,right),min(yy+768,bottom)]
            name=f'native-{xx}-{yy}.png'
            assembled.crop(bounds).save(evidence/name)
            records.append({'file':(evidence/name).relative_to(project).as_posix(),'world_bounds':bounds})
    write(evidence/'index.json',records)
    review_path=folder/'review.json'
    if not review_path.exists():
        write(review_path,{'candidate':args.candidate,'image_sha256':sha(folder/'integrated.png'),'reviewer':'','user_approval':'not requested or not supplied','checks':{k:{'status':'unclear','observation':'','evidence':[]} for k in CHECKS},'sites':{s:{'status':'unresolved','observation':''} for s in info['required_sites']},'open_issues':[]})
    print(f'Wrote {len(records)} native crops and overview; complete iterations/{args.candidate}/review.json.')


def accept(args):
    project=Path(args.project).resolve()
    folder=candidate(project,args.candidate)
    data=state(project)
    if any(i['candidate']==args.candidate for i in data['accepted']):
        fingerprint(project)
        print('Candidate is already accepted; state unchanged.')
        return
    info=verify_prepared(project,folder)
    verify_ingested(folder)
    review_path=Path(args.review) if args.review else folder/'review.json'
    review=read(review_path)
    require(review.get('candidate')==args.candidate,'Review belongs to a different candidate.')
    require(review.get('image_sha256')==sha(folder/'integrated.png'),'Review image hash does not match.')
    text_field(review,'reviewer')
    require(isinstance(review.get('open_issues'),list) and not review['open_issues'],'Resolve open issues before acceptance; keep limitations in planning notes.')
    for key in CHECKS:
        check=review.get('checks',{}).get(key,{})
        require(check.get('status')=='pass',f'Required check is not passed: {key}')
        text_field(check,'observation')
        paths=check.get('evidence')
        require(isinstance(paths,list) and bool(paths),f'{key}: evidence required.')
        for rel in paths:
            file=inside(project,rel)
            require(file.is_file(),f'Missing evidence: {rel}')
    for site in info['required_sites']:
        record=review.get('sites',{}).get(site,{})
        require(record.get('status') in ('painted','moved','deferred'),f'Site is unresolved: {site}')
        text_field(record,'observation')
        if record['status']=='moved':
            require(isinstance(record.get('destination'),list) and len(record['destination'])==2,'Moved site needs destination coordinates.')
    review['evidence_sha256'] = {rel: sha(inside(project, rel)) for check in review['checks'].values() for rel in check.get('evidence', [])}
    frozen=folder/'accepted-review.json'
    write(frozen,review)
    data['revision']+=1
    data['accepted'].append({'candidate':args.candidate,'rect':info['rect'],'file':(folder/'integrated.png').relative_to(project).as_posix(),'sha256':sha(folder/'integrated.png'),'review_file':frozen.relative_to(project).as_posix(),'review_sha256':sha(frozen)})
    write(project/'metadata/state.json',data)
    print(f'Accepted revision {data["revision"]}. Reviewer selection is separate from user approval.')


def labels_svg(w):
    width,height=w['canvas']['width'],w['canvas']['height']
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<g font-family="serif" font-size="19" fill="#20382f" stroke="#f1e4bf" stroke-width="3" paint-order="stroke">']
    for s in w['settlements']:
        x,y=s['point']
        lines.append(f'<text x="{x+14}" y="{y+6}">{escape(s["name"])}</text>')
    return '\n'.join(lines+['</g>','</svg>'])+'\n'


def export(args):
    project=Path(args.project).resolve()
    w=world(project)
    data=state(project)
    require(bool(data['accepted']),'No accepted painting; guide-only exports are not releases.')
    size=(w['canvas']['width'],w['canvas']['height'])
    coverage=Image.new('L',size,255 if data.get('base') else 0)
    d=ImageDraw.Draw(coverage)
    for item in data['accepted']:
        x,y,width,height=item['rect']
        d.rectangle((x,y,x+width-1,y+height-1),fill=255)
    complete=coverage.getextrema()[0]==255
    require(complete or args.allow_partial,'Unpainted guide remains. Finish coverage or use --allow-partial for an explicitly partial work-in-progress.')
    folder=project/'releases'/slug(args.release)
    require(not folder.exists(),'Release exists; choose a new release ID.')
    img=compose(project)
    folder.mkdir(parents=True)
    img.save(folder/'artwork.png')
    preview(img,folder/'preview.jpg')
    (folder/'labels.svg').write_text(labels_svg(w),encoding='utf-8')
    source=fingerprint(project)
    write(folder/'manifest.json',{'release':args.release,'revision':data['revision'],'native_dimensions':list(img.size),'coverage':'full canvas' if complete else 'partial: unpainted schematic guide remains','label_status':'planned anchors; inspect against actual artwork before publishing','user_approval':'not inferred; consult accepted reviews','source_fingerprint':source,'files':{f:sha(folder/f) for f in ('artwork.png','preview.jpg','labels.svg')}})
    shutil.copy2(ROOT/'templates/release-notes.md',folder/'release-notes.md')
    print(f'Prepared local release {args.release}. Inspect labels and complete release notes; nothing was published.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('new'); p.add_argument('--output',required=True); p.add_argument('--world'); p.add_argument('--base'); p.set_defaults(run=new)
    p=sub.add_parser('validate'); p.add_argument('world'); p.set_defaults(run=lambda a: (validate_world(read(a.world)),print('World structure valid. Geography, population and pixels still require review.')))
    p=sub.add_parser('guide'); p.add_argument('project'); p.set_defaults(run=guide)
    p=sub.add_parser('prepare'); p.add_argument('project'); p.add_argument('candidate'); p.add_argument('--rect',type=int,nargs=4,required=True,metavar=('X','Y','W','H')); p.add_argument('--mask'); p.set_defaults(run=prepare)
    p=sub.add_parser('ingest'); p.add_argument('project'); p.add_argument('candidate'); p.add_argument('--image',required=True); p.add_argument('--provenance',required=True); p.set_defaults(run=ingest)
    p=sub.add_parser('inspect'); p.add_argument('project'); p.add_argument('candidate'); p.set_defaults(run=inspect)
    p=sub.add_parser('accept'); p.add_argument('project'); p.add_argument('candidate'); p.add_argument('--review'); p.set_defaults(run=accept)
    p=sub.add_parser('export'); p.add_argument('project'); p.add_argument('release'); p.add_argument('--allow-partial',action='store_true'); p.set_defaults(run=export)
    args=parser.parse_args()
    try:
        args.run(args)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2,f'Error: {error}\n')


if __name__=='__main__':
    main()
