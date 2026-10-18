"""Guard: an emitted harness must *locate* its factory without being re-told.

``init`` writes the resolved factory path into ``.harness/pointer.json`` and into
the emitted ``AGENTS.md`` standing-reference block, and ``harness doctor`` /
``harness gate`` can verify that the pointer still resolves.  This is what turns
"mention the directory once" from a promise into a checkable structural link.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from harness_factory import config, pointer
from harness_factory.assemble import build_files, write_harness
from harness_factory.classify import classify
from harness_factory.cli import main
from harness_factory.derive import derive
from harness_factory.runtime import gate_report
from harness_factory.spec import TaskSpec

POINTER = ".harness/pointer.json"
HARNESS = Path(__file__).resolve().parent.parent  # .../harness_factory


def _plan(**overrides):
    task = TaskSpec(text="build an evaluated research pipeline over several sessions")
    return derive(task, classify(task, overrides=overrides))


class PointerEmissionTest(unittest.TestCase):
    def test_pointer_is_emitted_and_valid_json(self):
        files = build_files(_plan())
        self.assertIn(POINTER, files)
        data = json.loads(files[POINTER])
        self.assertEqual(data["revoke"], "stop using harness_factory")
        self.assertIn("how_to_use", data)

    def test_pointer_records_the_resolved_factory_root(self):
        expected = config.factory_root()
        self.assertIsNotNone(expected, "test must run from a factory checkout")
        data = json.loads(build_files(_plan())[POINTER])
        self.assertEqual(data["harness_factory"], str(expected))
        self.assertTrue(Path(data["skill_md"]).is_file())
        self.assertTrue(Path(data["entry_docs"]["reference/capability-router.md"]).is_file())

    def test_entry_docs_cover_the_whole_load_index(self):
        """The pointer must locate every loadable entry doc, not a frozen subset.

        Derived-from-index means an agent that follows the pointer can use the
        *whole* capability reference (routers + the field/instrument/outlet maps).
        """
        from harness_factory import pointer as _pointer, skill

        loadable = {e.path for e in skill.index() if e.group in {"overview", "reference"}}
        self.assertEqual(loadable - set(_pointer.ENTRY_DOCS), set())
        missing = [p for p in _pointer.ENTRY_DOCS if not (HARNESS / p).is_file()]
        self.assertEqual(missing, [])

    def test_pointer_lists_the_field_reference_docs(self):
        data = json.loads(build_files(_plan())[POINTER])
        for rel in (
            "reference/evidence-instruments.md",
            "reference/methodology-map.md",
            "reference/cross-language.md",
            "reference/outlet-map.md",
        ):
            self.assertIn(rel, data["entry_docs"])
            self.assertTrue(Path(data["entry_docs"][rel]).is_file())

    def test_pointer_is_null_when_no_checkout_is_reachable(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = build_files(_plan(), factory_root=tmp)  # a dir, but no SKILL.md
        data = json.loads(files[POINTER])
        self.assertIsNone(data["harness_factory"])
        self.assertEqual(data["entry_docs"], {})
        self.assertIn("<harness_factory path>", files["AGENTS.md"])

    def test_agents_md_names_the_real_path_and_the_pointer(self):
        files = build_files(_plan())
        agents = files["AGENTS.md"]
        expected = config.factory_root()
        self.assertNotIn("<harness_factory path>", agents)
        self.assertIn(expected.as_posix(), agents)
        self.assertIn(POINTER, agents)
        self.assertIn("stop using harness_factory", agents)


class PointerVerifyTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self):
        write_harness(_plan(), self.root)

    def test_fresh_harness_verifies(self):
        self._write()
        result = pointer.verify(self.root)
        self.assertTrue(result["ok"], result["problems"])
        self.assertTrue(result["standing_reference"], "emitted AGENTS.md must carry the convention")

    def test_missing_pointer_is_reported(self):
        result = pointer.verify(self.root)
        self.assertFalse(result["found"])
        self.assertFalse(result["ok"])
        self.assertTrue(result["problems"])

    def test_unreachable_factory_is_flagged(self):
        self._write()
        path = self.root / POINTER
        data = json.loads(path.read_text(encoding="utf-8"))
        data["harness_factory"] = str(self.root / "nowhere")
        path.write_text(json.dumps(data), encoding="utf-8")
        result = pointer.verify(self.root)
        self.assertFalse(result["ok"])
        self.assertTrue(any("not reachable" in p for p in result["problems"]))

    def test_null_factory_is_flagged(self):
        self._write()
        path = self.root / POINTER
        data = json.loads(path.read_text(encoding="utf-8"))
        data["harness_factory"] = None
        path.write_text(json.dumps(data), encoding="utf-8")
        result = pointer.verify(self.root)
        self.assertFalse(result["ok"])

    def test_verify_reports_missing_standing_reference(self):
        self._write()
        (self.root / "AGENTS.md").write_text("# no convention here\n", encoding="utf-8")
        result = pointer.verify(self.root)
        self.assertFalse(result["standing_reference"])
        self.assertTrue(result["ok"], "reachability is independent of the rules-file block")


class PointerWiringTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._saved_home = os.environ.get("HARNESS_HOME")
        os.environ["HARNESS_HOME"] = str(self.root / "_home")

    def tearDown(self):
        if self._saved_home is None:
            os.environ.pop("HARNESS_HOME", None)
        else:
            os.environ["HARNESS_HOME"] = self._saved_home
        self._tmp.cleanup()

    def test_gate_reports_an_advisory_pointer_gate(self):
        write_harness(_plan(), self.root)
        report = gate_report(self.root)
        ids = {g["id"]: g for g in report["gates"]}
        self.assertIn(POINTER, ids)
        self.assertEqual(ids[POINTER]["kind"], "advisory")
        self.assertEqual(ids[POINTER]["status"], "ok")

    def test_doctor_project_reports_reachability(self):
        write_harness(_plan(), self.root)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = main(["doctor", "--project", str(self.root)])
        out = buf.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("pointer @", out)
        self.assertIn("reachable: yes", out)


if __name__ == "__main__":
    unittest.main()
