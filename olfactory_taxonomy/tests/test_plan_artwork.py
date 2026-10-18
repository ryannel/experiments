"""Fresh planning must not depend on saved photographs or an existing master."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('plan_artwork_under_test', ROOT / 'scripts/plan_artwork.py')
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)


class FreshPlanningTests(unittest.TestCase):
    def test_plan_works_without_originals_or_existing_svg(self):
        with tempfile.TemporaryDirectory() as folder:
            fresh = Path(folder)
            (fresh / 'data').mkdir()
            (fresh / 'source').mkdir()
            shutil.copy2(ROOT / 'data/cells.json', fresh / 'data/cells.json')
            for name in ['artwork.json', 'generation-briefs.json']:
                shutil.copy2(ROOT / 'source' / name, fresh / 'source' / name)
            shutil.copytree(ROOT / 'source/prompts', fresh / 'source/prompts')
            plan = planner.build_plan(fresh)
            self.assertFalse((fresh / 'source/master.svg').exists())
            self.assertFalse((fresh / 'source/images').exists())
            targets = [cell for job in plan['jobs'] for cell in job['cell_ids']]
            expected = {cell['id'] for cell in json.loads((fresh / 'data/cells.json').read_text())}
            self.assertEqual(set(targets), expected)
            self.assertEqual(len(targets), len(expected))
            self.assertEqual(len(plan['jobs']), 130)
            self.assertTrue(all(not job['requires_reference_images'] for job in plan['jobs']))
            overrides = json.loads((fresh / 'source/generation-briefs.json').read_text())['briefs']
            for job in plan['jobs']:
                if job['id'] in overrides:
                    self.assertTrue(job['prompt'].startswith(overrides[job['id']]))


if __name__ == '__main__':
    unittest.main()
