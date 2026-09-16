"""Behavior checks for source preservation, acceptance and standalone packaging.

Artificial solid-color paintings test mechanics only; they are not art reviews.
"""
import copy
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace as Args
import sys
import tempfile
import unittest
import zipfile
from PIL import Image, ImageChops, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import mapkit as m
from package_experiment import build


class MapkitTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.project=self.base/'world'
        m.new(Args(output=str(self.project),world=None,base=None))

    def prepare(self,id='pilot-v1',rect=(300,220,768,512),mask=None):
        m.prepare(Args(project=str(self.project),candidate=id,rect=list(rect),mask=mask))
        return self.project/'iterations'/id

    def ingest(self,folder,size=(768,512),color='#aa8866'):
        source=self.base/(folder.name+'.png')
        Image.new('RGB',size,color).save(source)
        provenance=self.base/(folder.name+'.json')
        m.write(provenance,{'tool':'offline test fixture','prompt':'Synthetic solid color for code checks; no artistic quality claim.','calls':0,'native_dimensions':list(size)})
        m.ingest(Args(project=str(self.project),candidate=folder.name,image=str(source),provenance=str(provenance)))
        return source

    def review(self,folder):
        m.inspect(Args(project=str(self.project),candidate=folder.name))
        review=m.read(folder/'review.json')
        review['reviewer']='automated test fixture; not a visual reviewer'
        for check in review['checks'].values():
            check.update(status='pass',observation='Synthetic test record for acceptance logic only.',evidence=[f'iterations/{folder.name}/evidence/overview.jpg'])
        for site in review['sites'].values():
            site.update(status='deferred',observation='Synthetic fixture; site painting is outside test scope.')
        m.write(folder/'review.json',review)
        return review

    def accept(self,folder):
        m.accept(Args(project=str(self.project),candidate=folder.name,review=None))

    def test_workflow_preserves_master_and_requires_review(self):
        folder=self.prepare()
        source=self.ingest(folder)
        self.assertEqual(source.read_bytes(),(folder/'returned-master.png').read_bytes())
        m.inspect(Args(project=str(self.project),candidate=folder.name))
        with self.assertRaises(ValueError):
            self.accept(folder)
        self.assertEqual(m.state(self.project)['revision'],0)
        self.review(folder)
        self.accept(folder)
        self.accept(folder)
        self.assertEqual(m.state(self.project)['revision'],1)
        with self.assertRaises(ValueError):
            m.export(Args(project=str(self.project),release='full',allow_partial=False))
        m.export(Args(project=str(self.project),release='partial',allow_partial=True))
        self.assertIn('partial',m.read(self.project/'releases/partial/manifest.json')['coverage'])

    def test_style_reference_is_retained_and_changes_invalidate_candidate(self):
        reference=self.project/'assets/masters/style-v1.png'
        Image.new('RGB',(32,32),'blue').save(reference)
        style=m.read(self.project/'style.json')
        style['reference_files']=['assets/masters/style-v1.png']
        m.write(self.project/'style.json',style)
        folder=self.prepare()
        self.assertEqual(reference.read_bytes(),(folder/'reference-1.png').read_bytes())
        self.assertEqual((self.project/'world.json').read_bytes(),(folder/'world.json').read_bytes())
        Image.new('RGB',(32,32),'red').save(reference)
        with self.assertRaisesRegex(ValueError,'stale'):
            self.ingest(folder)

    def test_wrong_dimensions_not_resized(self):
        folder=self.prepare()
        with self.assertRaisesRegex(ValueError,'dimensions'):
            self.ingest(folder,size=(384,256))
        self.assertFalse((folder/'ingested.json').exists())

    def test_stale_candidate_rejected_after_other_acceptance(self):
        first=self.prepare()
        stale=self.prepare('parallel-v1')
        self.ingest(first)
        self.review(first)
        self.accept(first)
        with self.assertRaisesRegex(ValueError,'stale'):
            self.ingest(stale)

    def test_changed_world_invalidates_preparation(self):
        folder=self.prepare()
        w=m.world(self.project)
        w['name']='Changed intent'
        m.write(self.project/'world.json',w)
        with self.assertRaisesRegex(ValueError,'stale'):
            self.ingest(folder)

    def test_exact_preservation_outside_mask(self):
        first=self.prepare()
        self.ingest(first)
        self.review(first)
        self.accept(first)
        mask=Image.new('L',(128,128),0)
        ImageDraw.Draw(mask).rectangle((35,35,90,90),fill=255)
        maskpath=self.base/'mask.png'
        mask.save(maskpath)
        repair=self.prepare('repair-v1',(400,300,128,128),str(maskpath))
        self.ingest(repair,(128,128),'#223344')
        with Image.open(repair/'prior.png') as before, Image.open(repair/'integrated.png') as after:
            changed=ImageChops.difference(before,after)
            self.assertIsNotNone(changed.getbbox())
            protected=ImageChops.multiply(changed,ImageChops.invert(mask).convert('RGB'))
            self.assertIsNone(protected.getbbox())
        self.review(repair)
        self.accept(repair)

    def test_mutated_ingested_pixels_rejected(self):
        folder=self.prepare()
        self.ingest(folder)
        self.review(folder)
        Image.new('RGB',(768,512),'red').save(folder/'integrated.png')
        with self.assertRaisesRegex(ValueError,'changed'):
            self.accept(folder)

    def test_missing_evidence_and_path_escape_rejected(self):
        folder=self.prepare()
        self.ingest(folder)
        review=self.review(folder)
        review['checks']['routes']['evidence']=['../outside.txt']
        m.write(folder/'review.json',review)
        with self.assertRaisesRegex(ValueError,'escapes'):
            self.accept(folder)
        review['checks']['routes']['evidence']=['missing.png']
        m.write(folder/'review.json',review)
        with self.assertRaisesRegex(ValueError,'Missing evidence'):
            self.accept(folder)

    def test_world_graph_bounds_ids_and_capacity(self):
        original=m.world(self.project)
        for mutate in (
            lambda w:w['rivers'][1].update(downstream='missing'),
            lambda w:w['rivers'][1]['points'].__setitem__(-1,[1,1]),
            lambda w:w['settlements'][0].update(point=[-1,0]),
            lambda w:w['factions'][0].update(id=w['land'][0]['id']),
            lambda w:w['canvas'].update(width=10000,height=10000),
        ):
            bad=copy.deepcopy(original)
            mutate(bad)
            with self.assertRaises(ValueError):
                m.validate_world(bad)

    def test_no_candidate_overwrite_or_path_traversal(self):
        self.prepare()
        with self.assertRaises(ValueError): self.prepare()
        with self.assertRaises(ValueError): self.prepare('../escape')
        with self.assertRaises(ValueError): self.prepare('outside',(1500,900,300,300))

    def test_full_coverage_export_and_escaped_labels(self):
        w=m.world(self.project)
        w['settlements'][0]['name']='North & <South>'
        m.write(self.project/'world.json',w)
        folder=self.prepare('all-v1',(0,0,1536,1024))
        self.ingest(folder,(1536,1024))
        self.review(folder)
        self.accept(folder)
        m.export(Args(project=str(self.project),release='release-v1',allow_partial=False))
        text=(self.project/'releases/release-v1/labels.svg').read_text()
        self.assertIn('North &amp; &lt;South&gt;',text)
        with Image.open(self.project/'releases/release-v1/preview.jpg') as im:
            self.assertLessEqual(im.width,1600)

    def test_package_is_self_contained_and_excludes_work(self):
        archive=self.base/'kit.zip'
        build(ROOT,archive)
        with zipfile.ZipFile(archive) as z:
            names=z.namelist()
            self.assertTrue(any('/.agents/skills/map-director/SKILL.md' in n for n in names))
            self.assertIn('map_creation/.codex/config.toml', names)
            self.assertFalse(any('/work/' in n or '/__pycache__/' in n for n in names))
            z.extractall(self.base/'extracted')
        extracted=self.base/'extracted/map_creation'
        import subprocess
        result=subprocess.run([sys.executable,str(extracted/'scripts/mapkit.py'),'new','--output',str(self.base/'fresh-world')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        result=subprocess.run([sys.executable,str(extracted/'scripts/mapkit.py'),'guide',str(self.base/'fresh-world')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':
    unittest.main()
