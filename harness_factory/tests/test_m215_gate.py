"""Guards for P73.R1 (the M2.15 emitted gate) and P78.R1/R2 (mlops/dataops).

The gate's contract: a `surprise` must be closed by an `epistemic_observation`
before the next surprise, before `task_outcome`, or before the stream ends -
blind pragmatic retry is what it refuses. The domain contract: mlops/dataops
tasks route to their domains and fire their capabilities.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory.check import check_harness
from harness_factory.classify import classify
from harness_factory.derive import derive
from harness_factory.spec import TaskSpec


def _emit(tmp: Path, text: str) -> Path:
    from harness_factory.assemble import build_files

    task = TaskSpec(text=text)
    for name, body in build_files(derive(task, classify(task))).items():
        target = tmp / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return tmp


def _write_traces(root: Path, events: list[str]) -> None:
    path = root / ".harness" / "traces.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for i, event in enumerate(events):
            fh.write(json.dumps({"v": 1, "ts": f"t{i}", "project": "p", "task": "t",
                                 "harness": "h", "event": event}) + "\n")


class EpistemicSwitchGateTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        _emit(self.root, "Add unit tests to the parser")

    def test_no_traces_passes(self):
        self.assertEqual(check_harness(self.root), [])

    def test_open_surprise_fails(self):
        _write_traces(self.root, ["surprise"])
        problems = check_harness(self.root)
        self.assertTrue(any("M2.15" in p and "left open" in p for p in problems))

    def test_closed_surprise_passes(self):
        _write_traces(self.root, ["surprise", "epistemic_observation", "task_outcome"])
        self.assertEqual(check_harness(self.root), [])

    def test_stacked_surprise_fails(self):
        _write_traces(self.root, ["surprise", "surprise", "epistemic_observation"])
        problems = check_harness(self.root)
        self.assertTrue(any("stacked" in p for p in problems))

    def test_task_outcome_with_open_surprise_fails(self):
        _write_traces(self.root, ["surprise", "task_outcome"])
        problems = check_harness(self.root)
        self.assertTrue(any("task_outcome" in p and "M2.15" in p for p in problems))

    def test_v3_events_validate_in_trace_vocabulary(self):
        from harness_factory import trace

        for event in ("surprise", "epistemic_observation"):
            line = trace.make_trace(event, project="p", task="t", harness="h")
            self.assertEqual(trace.validate(line), [])


class MlopsDataopsRoutingTest(unittest.TestCase):
    def test_mlops_task_routes_and_fires_the_capability(self):
        task = TaskSpec(text="Set up a model registry with drift monitoring and a retraining gate")
        plan = derive(task, classify(task))
        self.assertEqual(plan.features.domain, "mlops")
        self.assertIn("model-lifecycle-discipline", plan.capabilities)

    def test_dataops_task_routes_and_fires_the_capability(self):
        task = TaskSpec(text="Declare a data contract with lineage and a backfill plan")
        plan = derive(task, classify(task))
        self.assertEqual(plan.features.domain, "dataops")
        self.assertIn("data-contract-discipline", plan.capabilities)

    def test_the_two_domains_do_not_shadow_each_other(self):
        model_task = TaskSpec(text="Monitor model drift and gate retraining on measurements")
        data_task = TaskSpec(text="Audit data quality contracts and dataset lineage")
        self.assertEqual(derive(model_task, classify(model_task)).features.domain, "mlops")
        self.assertEqual(derive(data_task, classify(data_task)).features.domain, "dataops")


if __name__ == "__main__":
    unittest.main()
