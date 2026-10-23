"""Guards for the D1a trace mechanism (P22): schema, storage, legacy reads, gate hook."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory import trace
from harness_factory.runtime import gate_report, record_gate_miss_trace


def _build_ok_harness(root: Path) -> None:
    from harness_factory.assemble import build_files
    from harness_factory.classify import classify
    from harness_factory.derive import derive
    from harness_factory.spec import TaskSpec

    task = TaskSpec(text="add unit tests to the parser")
    for name, text in build_files(derive(task, classify(task))).items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


class TraceSchemaTest(unittest.TestCase):
    def test_make_trace_rejects_unknown_event(self):
        with self.assertRaises(ValueError):
            trace.make_trace("opinion", project="p", task="t", harness="h")

    def test_validate_flags_missing_required_fields(self):
        problems = trace.validate({"v": 1, "event": "gate_miss"})
        joined = "; ".join(problems)
        for field in ("project", "task", "harness", "ts"):
            self.assertIn(field, joined)

    def test_validate_flags_unknown_event(self):
        line = trace.make_trace("gate_miss", project="p", task="t", harness="h")
        line["event"] = "nope"
        self.assertIn("unknown event", "; ".join(trace.validate(line)))

    def test_validate_flags_bad_detail(self):
        line = trace.make_trace("gate_miss", project="p", task="t", harness="h", detail="text")
        self.assertIn("detail", "; ".join(trace.validate(line)))

    def test_valid_trace_passes(self):
        line = trace.make_trace("gate_miss", project="p", task="t", harness="h", detail={"g": 1})
        self.assertEqual(trace.validate(line), [])


class TraceStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_record_and_read_roundtrip_append_only(self):
        path = self.tmp / "traces.jsonl"
        for i in range(2):
            trace.record_trace(
                path, trace.make_trace("gate_miss", project=f"p{i}", task="t", harness="h")
            )
        lines = trace.read_traces(path)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[1]["project"], "p1")

    def test_record_rejects_invalid_line(self):
        with self.assertRaises(ValueError):
            trace.record_trace(self.tmp / "traces.jsonl", {"v": 1})

    def test_legacy_free_text_reads_as_signal(self):
        path = self.tmp / "traces.jsonl"
        path.write_text("human said the gate was too strict\n", encoding="utf-8")
        lines = trace.read_traces(path)
        self.assertEqual(lines[0]["event"], trace.LEGACY_EVENT)

    def test_legacy_harvest_line_reads_as_signal(self):
        path = self.tmp / "traces.jsonl"
        path.write_text(
            json.dumps({"source": "harvest", "domain": "research"}) + "\n", encoding="utf-8"
        )
        lines = trace.read_traces(path)
        self.assertEqual(lines[0]["event"], trace.LEGACY_EVENT)
        self.assertEqual(lines[0]["domain"], "research")

    def test_collect_copies_valid_and_rejects_invalid(self):
        proj = self.tmp / "proj"
        (proj / ".harness").mkdir(parents=True)
        good = trace.make_trace("human_correction", project="p", task="t", harness="h")
        (proj / ".harness" / "traces.jsonl").write_text(
            json.dumps(good) + "\nnot-json\n" + json.dumps({"v": 9}) + "\n", encoding="utf-8"
        )
        copied, rejected = trace.collect_traces(proj, self.tmp)
        self.assertEqual((copied, rejected), (1, 2))
        self.assertEqual(trace.read_traces(self.tmp / "updates" / "traces.jsonl")[-1]["event"],
                         "human_correction")

    def test_collect_no_project_traces_is_a_noop(self):
        copied, rejected = trace.collect_traces(self.tmp / "nope", self.tmp)
        self.assertEqual((copied, rejected), (0, 0))


class GateMissTraceTest(unittest.TestCase):
    def test_failed_gate_records_trace_and_passed_gate_does_not(self):
        tmp = Path(tempfile.mkdtemp())
        # a directory without a manifest always fails the gate
        report = gate_report(tmp)
        self.assertFalse(report["passed"])
        path = record_gate_miss_trace(tmp, report, tmp)
        self.assertIsNotNone(path)
        lines = trace.read_traces(path)
        self.assertEqual(lines[-1]["event"], "gate_miss")
        self.assertEqual(lines[-1]["harness"], "none")

        ok = tmp / "ok"
        _build_ok_harness(ok)
        report2 = gate_report(ok)
        self.assertTrue(report2["passed"])
        self.assertIsNone(record_gate_miss_trace(ok, report2, tmp))

    def test_gate_miss_trace_binds_to_the_manifest_hash(self):
        tmp = Path(tempfile.mkdtemp())
        ok = tmp / "ok"
        _build_ok_harness(ok)
        # corrupt the manifest (reference a missing file) so the gate fails while a manifest is present
        manifest_path = ok / ".harness" / "manifest.json"
        plan = json.loads(manifest_path.read_text(encoding="utf-8"))
        plan["files"].append("tasks/DOES-NOT-EXIST.md")
        manifest_path.write_text(json.dumps(plan), encoding="utf-8")
        report = gate_report(ok)
        self.assertFalse(report["passed"])
        path = record_gate_miss_trace(ok, report, tmp)
        self.assertIsNotNone(path)
        line = trace.read_traces(path)[-1]
        self.assertNotEqual(line["harness"], "none")
        self.assertIn("failed_gates", line["detail"])


if __name__ == "__main__":
    unittest.main()
