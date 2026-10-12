from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory.assemble import build_files, write_harness
from harness_factory.check import check_harness
from harness_factory.classify import classify
from harness_factory.derive import derive
from harness_factory.spec import TaskSpec


def _plan(**overrides):
    task = TaskSpec(text="build an evaluated research pipeline over several sessions")
    feats = classify(task, overrides=overrides)
    return derive(task, feats)


class AssembleTest(unittest.TestCase):
    def test_build_files_has_no_placeholders(self):
        files = build_files(_plan())
        self.assertIn("AGENTS.md", files)
        self.assertIn(".harness/manifest.json", files)
        for name, content in files.items():
            self.assertNotIn("{{", content, f"unrendered placeholder in {name}")

    def test_manifest_lists_all_files(self):
        plan = _plan()
        files = build_files(plan)
        manifest = json.loads(files[".harness/manifest.json"])
        for name in manifest["files"]:
            self.assertIn(name, files)

    def test_write_and_check_pass(self):
        plan = _plan(horizon="multi_session", collaboration="human_review")
        with tempfile.TemporaryDirectory() as tmp:
            written = write_harness(plan, tmp)
            self.assertTrue(written)
            self.assertEqual(check_harness(tmp), [])
            self.assertTrue((Path(tmp) / ".harness/ledger.md").exists())

    def test_refuses_overwrite_without_force(self):
        plan = _plan()
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(plan, tmp)
            with self.assertRaises(FileExistsError):
                write_harness(plan, tmp)

    def test_force_overwrites(self):
        plan = _plan()
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(plan, tmp)
            write_harness(plan, tmp, force=True)
            self.assertEqual(check_harness(tmp), [])

    def test_check_reports_missing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(check_harness(tmp))


if __name__ == "__main__":
    unittest.main()
