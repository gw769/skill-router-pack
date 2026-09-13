import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('search', Path(__file__).resolve().parents[1] / 'use-installed-skills/scripts/search.py')
search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search)

class SearchTests(unittest.TestCase):
    def test_local_nested_and_multiline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / '.codex/skills/library/writer/SKILL.md'
            path.parent.mkdir(parents=True)
            path.write_text('---\nname: writer\ndescription: |\n  paper writing\n---\n')
            with patch.object(Path, 'home', return_value=root), patch.object(search.shutil, 'which', return_value=None):
                rows = search.local_rows()
            self.assertEqual(len(rows), 1)
            self.assertTrue(Path(rows[0]['path']).is_file())
            self.assertGreater(search.score({'paper'}, rows[0]), 0)

    def test_catalog_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'index.json'
            path.write_text(json.dumps([{'name':'x','path':'skills/x'}, {'name':'y','path':'skills/y/SKILL.md'}, {'path':'../bad'}]))
            rows = search.catalog_rows(path)
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(r['path'].count('SKILL.md') == 1 for r in rows))
            self.assertTrue(all(r['status'] == 'catalog-only' for r in rows))

    def test_absent_index(self):
        self.assertEqual(search.catalog_rows(Path('/nonexistent/index.json')), [])

    def test_no_match(self):
        self.assertEqual(search.score({'unmatched'}, {'name':'writer','description':'paper'}), 0)

if __name__ == '__main__':
    unittest.main()
