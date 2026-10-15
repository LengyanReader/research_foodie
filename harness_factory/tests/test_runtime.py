from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory.assemble import write_harness
from harness_factory.classify import classify
from harness_factory.derive import derive
from harness_factory.runtime import gate_report, harvest, record_signals
from harness_factory.spec import TaskSpec


def _plan(**overrides):
    task = TaskSpec(text="build an evaluated research pipeline over several sessions")
    feats = classify(task, overrides=overrides)
    return derive(task, feats)


def _gate_ids(report):
    return {g["id"]: g for g in report["gates"]}


class GateReportTest(unittest.TestCase):
    def test_fresh_harness_passes_hard_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(_plan(), tmp)
            report = gate_report(tmp)
            self.assertTrue(report["passed"], report)
            gates = _gate_ids(report)
            self.assertEqual(gates["manifest-valid"]["status"], "pass")
            self.assertEqual(gates["check-py-runs"]["status"], "pass")

    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = gate_report(tmp)
            self.assertFalse(report["passed"])
            self.assertEqual(_gate_ids(report)["manifest-valid"]["status"], "fail")

    def test_deleted_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(_plan(), tmp)
            (Path(tmp) / "tasks/PROGRESS.md").unlink()
            report = gate_report(tmp)
            self.assertFalse(report["passed"])
            self.assertEqual(_gate_ids(report)["files-present"]["status"], "fail")

    def test_placeholder_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(_plan(), tmp)
            target = Path(tmp) / "AGENTS.md"
            target.write_text(target.read_text(encoding="utf-8") + "\n{{ oops }}\n", encoding="utf-8")
            report = gate_report(tmp)
            self.assertFalse(report["passed"])
            self.assertEqual(_gate_ids(report)["no-placeholders"]["status"], "fail")

    def test_module_gates_are_advisory(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(_plan(horizon="multi_session", grounding="required"), tmp)
            report = gate_report(tmp)
            advisory = [g for g in report["gates"] if g["kind"] == "advisory"]
            self.assertTrue(any(g["id"] == ".harness/PROVENANCE.md" for g in advisory))
            # advisory gates never flip the verdict
            self.assertTrue(report["passed"])


class HarvestTest(unittest.TestCase):
    def test_bundle_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(_plan(), tmp)
            bundle = harvest(tmp)
            self.assertEqual(bundle["source"], "harvest")
            self.assertEqual(bundle["gates"]["passed"], True)
            self.assertGreaterEqual(bundle["gates"]["hard_total"], 4)
            self.assertIn("progress_lines", bundle["signals"])

    def test_record_signals_appends_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(_plan(), tmp)
            bundle = harvest(tmp)
            with tempfile.TemporaryDirectory() as kb:
                path = record_signals(kb, bundle)
                self.assertTrue(path.exists())
                line = json.loads(path.read_text(encoding="utf-8").strip())
                self.assertEqual(line["source"], "harvest")
                record_signals(kb, bundle)
                self.assertEqual(len(path.read_text(encoding="utf-8").strip().splitlines()), 2)

    def test_custom_signals_are_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_harness(_plan(), tmp)
            (Path(tmp) / ".harness/signals.jsonl").write_text(
                '{"kind": "note", "value": 1}\nnot-json\n', encoding="utf-8"
            )
            bundle = harvest(tmp)
            self.assertEqual(len(bundle["custom_signals"]), 2)
            self.assertEqual(bundle["custom_signals"][0]["kind"], "note")
            self.assertEqual(bundle["custom_signals"][1]["raw"], "not-json")


if __name__ == "__main__":
    unittest.main()
