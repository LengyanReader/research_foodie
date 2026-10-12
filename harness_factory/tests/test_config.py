from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from harness_factory import config

_ENV_KEYS = ("HARNESS_HOME", "HARNESS_DATA_DIR", "HARNESS_CORPUS_DIR")


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in _ENV_KEYS}
        self.tmp = Path(tempfile.mkdtemp())
        os.environ["HARNESS_HOME"] = str(self.tmp)
        for key in ("HARNESS_DATA_DIR", "HARNESS_CORPUS_DIR"):
            os.environ.pop(key, None)

    def tearDown(self):
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_home_from_env(self):
        self.assertEqual(config.home(), self.tmp)

    def test_defaults_live_under_home(self):
        self.assertEqual(config.catalog_dir().parent, self.tmp)
        self.assertEqual(config.corpus_dir().parent, self.tmp)
        self.assertEqual(config.updates_dir(), self.tmp / "updates")

    def test_ensure_home_creates_and_seeds(self):
        home = config.ensure_home()
        self.assertEqual(home, self.tmp)
        self.assertTrue((self.tmp / "catalog" / "modules.json").exists())
        self.assertTrue((self.tmp / "catalog" / "watchlist.json").exists())
        self.assertTrue((self.tmp / "corpus").is_dir())
        self.assertTrue((self.tmp / "updates").is_dir())

    def test_seed_keeps_existing_by_default(self):
        config.ensure_home()
        target = config.catalog_dir() / "modules.json"
        target.write_text('{"X": {}}', encoding="utf-8")
        result = config.seed_catalog()
        self.assertIn("modules.json", result["kept"])
        self.assertEqual(target.read_text(encoding="utf-8"), '{"X": {}}')

    def test_seed_force_overwrites(self):
        config.ensure_home()
        target = config.catalog_dir() / "modules.json"
        target.write_text('{"X": {}}', encoding="utf-8")
        config.seed_catalog(force=True)
        self.assertNotEqual(target.read_text(encoding="utf-8"), '{"X": {}}')

    def test_corpus_root_prefers_checkout(self):
        project = self.tmp / "proj"
        (project / "review").mkdir(parents=True)
        self.assertEqual(config.resolve_corpus_root(project), project / "review")

    def test_corpus_root_falls_back_to_home(self):
        self.assertEqual(config.resolve_corpus_root(None), config.corpus_dir())


if __name__ == "__main__":
    unittest.main()
