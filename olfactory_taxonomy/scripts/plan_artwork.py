#!/usr/bin/env python3
"""Plan fresh artwork from final cell data and briefs; no old images or master SVG required."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def point(radius, angle):
    a = math.radians(angle)
    return 3072 + radius * math.sin(a), 3072 - radius * math.cos(a)


def sector(inner, outer, start, end):
    p0, p1 = point(outer, start), point(outer, end)
    p2, p3 = point(inner, end), point(inner, start)
    large = int(end - start > 180)
    return (f'M {p0[0]:.5f},{p0[1]:.5f} A {outer},{outer} 0 {large} 1 {p1[0]:.5f},{p1[1]:.5f} '
            f'L {p2[0]:.5f},{p2[1]:.5f} A {inner},{inner} 0 {large} 0 {p3[0]:.5f},{p3[1]:.5f} Z')


def build_plan(root=ROOT):
    cells = json.loads((root / 'data/cells.json').read_text())
    by_id = {c['id']: c for c in cells}
    manifest = json.loads((root / 'source/artwork.json').read_text())
    overrides = json.loads((root / 'source/generation-briefs.json').read_text())['briefs']
    jobs, covered = [], []
    for asset in manifest['assets']:
        targets = sorted([by_id[i] for i in asset['cell_ids']], key=lambda c: c['inner'])
        covered.extend(asset['cell_ids'])
        if len({(c['start'], c['end']) for c in targets}) != 1:
            raise ValueError(f'Image crosses distinct angular spans: {asset["id"]}')
        for a, b in zip(targets, targets[1:]):
            if a['outer'] != b['inner']:
                raise ValueError(f'Non-contiguous image placement: {asset["id"]}')
        start, end = targets[0]['start'], targets[0]['end']
        inner, outer = targets[0]['inner'], targets[-1]['outer']
        fields = {c['field'] for c in targets}
        priority = 0 if 'descriptors' in fields else {'note': 1, 'family': 2, 'realm': 3}[targets[0]['field']]
        role = ['Scent route', 'Character summary', 'Family summary', 'Broad-area summary'][priority]
        cues = [c['text'] for c in cells if c['field'] == 'descriptors' and c['start'] >= start - 1e-6 and c['end'] <= end + 1e-6]
        if asset.get('reference_inputs_historical') and asset['id'] not in overrides:
            raise ValueError(f'Fresh-generation brief missing for edited image: {asset["id"]}')
        brief = overrides.get(asset['id'])
        if brief is None:
            brief = (root / 'source' / asset['prompt']).read_text().strip()
        context = ' → '.join(dict.fromkeys(asset.get('full_scent_path') or [targets[0]['realm'], targets[0]['text']]))
        prompt = f'{brief}\n\nScent context: {context}.\n'
        prompt += 'Create a new text-free photograph. Keep the distinctive scent cues recognisable in the actual tapered crop, including generous partial shapes. No lettering or diagram boundaries.\n'
        if priority:
            prompt += 'Mix representative descendant cues organically across one composition, without subdividing the image into child bands. Descendant comparisons: ' + '; '.join(cues) + '.\n'
        else:
            prompt += 'This one continuous photograph spans the listed comparison, feel and reference cells. Material names illustrate scent facets; do not add chemical diagrams or ingredient-identification claims.\n'
        jobs.append({'id': asset['id'], 'priority': priority, 'role': role, 'cell_ids': asset['cell_ids'], 'labels': [c['text'] for c in targets], 'scent_context': context, 'descendant_comparisons': cues, 'prompt': prompt, 'requires_reference_images': False, 'suggested_dimensions_px': asset['dimensions_px'], 'sector': {'inner': inner, 'outer': outer, 'start': start, 'end': end, 'clip_path': sector(inner, outer, start, end)}, 'staged_image': f'build/regeneration/images/{asset["id"]}.png'})
    if Counter(covered) != Counter(by_id.keys()):
        raise ValueError('Artwork plan must cover every final cell exactly once')
    if len({j['id'] for j in jobs}) != len(jobs):
        raise ValueError('Duplicate artwork job IDs')
    jobs.sort(key=lambda j: (j['priority'], j['sector']['start'], j['id']))
    return {'canvas_px': manifest['canvas'], 'viewbox': manifest['coordinate_viewbox'], 'generation_order': 'Scent routes, character summaries, families, broad areas', 'asset_count': len(jobs), 'cell_count': len(cells), 'notes': 'A fresh generation plan, not a byte-identical recreation. Use built-in image generation. Keep accepted originals untouched; inspect the actual sector crops before promoting replacements.', 'jobs': jobs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/artwork-plan.json')
    args = parser.parse_args()
    plan = build_plan()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + '\n')
    print(f'Planned {plan["asset_count"]} new compositions covering {plan["cell_count"]} cells; no existing images required. Wrote {args.output}')


if __name__ == '__main__':
    main()
