"""pass^k reliability (P70): the estimator and its honest boundaries, proven on
SYNTHETIC task_outcome receipts — mirroring the P63 simulation-test precedent.

The point of the instrument is to score the factory's capability on the same bar
the external benchmarks use (τ-bench R282 / ThinkingBox R279): reliability over
*k* consistent runs, not the best one-shot. These tests prove the arithmetic and
the two honesty rules — *insufficient data reads as "not measurable", never a
fabricated number* (M5.11/M5.12), and *a pass is read off the receipt, never
guessed* (M0.4) — without running a single live model.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory import passk
from harness_factory import trace as tr


class PassKArithTest(unittest.TestCase):
    def test_all_success_is_one(self):
        self.assertEqual(passk.pass_k([True] * 4, 2), 1.0)

    def test_partial_estimate(self):
        # n=4, c=2, k=2 -> C(2,2)/C(4,2) = 1/6
        self.assertAlmostEqual(passk.pass_k([True, True, False, False], 2), 1 / 6, places=6)

    def test_below_k_runs_is_not_measurable(self):
        # n < k -> None: the estimate is withheld, never extrapolated (M5.12)
        self.assertIsNone(passk.pass_k([True], 2))

    def test_one_success_of_two_is_zero(self):
        # n=2, c=1, k=2 -> C(1,2)=0 over C(2,2)=1 -> 0.0 (a real zero, not None)
        self.assertEqual(passk.pass_k([True, False], 2), 0.0)

    def test_nonpositive_k(self):
        self.assertIsNone(passk.pass_k([True, True], 0))


class IsSuccessTest(unittest.TestCase):
    """A pass is READ from the receipt; an unreadable receipt is not a pass."""

    def test_explicit_passed_bool(self):
        self.assertTrue(passk.is_success({"passed": True}))
        self.assertFalse(passk.is_success({"passed": False}))

    def test_score_at_top_of_declared_scale(self):
        self.assertTrue(passk.is_success({"score": 1.0, "scale": [0, 1]}))
        self.assertFalse(passk.is_success({"score": 0.5, "scale": [0, 1]}))

    def test_string_verdict_token(self):
        self.assertTrue(passk.is_success({"score": "passed"}))
        self.assertFalse(passk.is_success({"score": "failed"}))

    def test_unreadable_is_not_pass(self):
        self.assertFalse(passk.is_success({}))
        self.assertFalse(passk.is_success(None))


class ReliabilitySimulationTest(unittest.TestCase):
    def _receipt(self, task: str, passed: bool) -> dict:
        return {
            "event": "task_outcome",
            "project": "updates/dogfood/sim",
            "task": task,
            "harness": "B-harness",
            "detail": {"passed": passed, "scale": [0, 1]},
        }

    def test_pass_at1_vs_pass_k_divergence(self):
        # Task A is reliable (4/4); task B is a one-shot fluke (1 pass, 3 fail).
        outcomes = (
            [self._receipt("A", True) for _ in range(4)]
            + [self._receipt("B", True)]
            + [self._receipt("B", False) for _ in range(3)]
        )
        rep = passk.reliability(outcomes, k=2)
        self.assertEqual(rep["tasks_total"], 2)
        self.assertEqual(rep["tasks_measured"], 2)  # both have n >= k
        self.assertAlmostEqual(rep["pass_at_1"], 0.625, places=4)  # mean (1.0, 0.25)
        self.assertAlmostEqual(rep["pass_k"], 0.5, places=4)       # mean (1.0, C(1,2)/C(4,2)=0)
        self.assertGreater(rep["pass_at_1"], rep["pass_k"])        # the gap τ-bench warns about
        self.assertAlmostEqual(rep["gap"], 0.125, places=4)

    def test_thin_data_reports_not_measurable(self):
        # A single run per task never reaches k -> pass^k withheld, honestly rendered.
        rep = passk.reliability([self._receipt("solo", True)], k=2)
        self.assertEqual(rep["tasks_measured"], 0)
        self.assertIsNone(rep["pass_k"])
        self.assertIn("not measurable", passk.render(rep))


class PassKEndToEndTest(unittest.TestCase):
    def test_run_over_temp_home(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            upd = root / "updates"
            upd.mkdir()
            lines = []
            for _ in range(3):  # task X: reliable
                lines.append(tr.make_trace(
                    "task_outcome", project="updates/dogfood/sim", task="X",
                    harness="B-harness", detail={"passed": True, "scale": [0, 1]}))
            lines.append(tr.make_trace(  # task Y: one pass
                "task_outcome", project="updates/dogfood/sim", task="Y",
                harness="B-harness", detail={"passed": True, "scale": [0, 1]}))
            for _ in range(2):  # task Y: two fails
                lines.append(tr.make_trace(
                    "task_outcome", project="updates/dogfood/sim", task="Y",
                    harness="B-harness", detail={"passed": False, "scale": [0, 1]}))
            (upd / "traces.jsonl").write_text(
                "\n".join(json.dumps(ln) for ln in lines) + "\n", encoding="utf-8")
            rep = passk.run(root, k=2)
            self.assertEqual(rep["outcomes_read"], 6)
            self.assertEqual(rep["tasks_measured"], 2)
            self.assertAlmostEqual(rep["pass_k"], 0.5, places=4)  # mean (1.0, 0.0)
            self.assertGreater(rep["pass_at_1"], rep["pass_k"])


class EmbodiedGradingTest(unittest.TestCase):
    """P71: uni-robot-agent [R291] grades the ENVIRONMENT's reported outcome
    (its SDK's ``task_success``), never the agent's ``agent_finished`` self-report,
    and an *unavailable* verdict is simply not recorded (thinner data, not a silent
    fail).  These prove the P70 pass^k instrument already honours that discipline on
    SYNTHETIC embodied receipts — no robot is run and no score is this factory's own.
    """

    def _env_receipt(self, task: str, task_success) -> dict:
        # Adapter convention (evidence-instruments gate 6 / R291): the receipt's
        # ``passed`` carries the ENVIRONMENT verdict, not the model's claim.
        return {
            "event": "task_outcome",
            "project": "updates/dogfood/p71-embodied",
            "task": task,
            "harness": "uni-robot-agent",
            "detail": {"passed": task_success, "scale": [0, 1]},
        }

    def test_environment_verdict_not_agent_self_report(self):
        # Agent CLAIMED completion but the physical end-state says failure -> the
        # receipt is graded from the environment, so it is NOT a pass.
        self.assertFalse(passk.is_success(self._env_receipt("stack_bowls", False)["detail"]))
        self.assertTrue(passk.is_success(self._env_receipt("stack_bowls", True)["detail"]))

    def test_unavailable_verdict_thins_data_not_counts_as_fail(self):
        # Two episodes were run, but only ONE had a graded environment verdict; the
        # other's ``task_success`` was None so the adapter records NO receipt.  One
        # run per task never reaches k=2 -> pass^k withheld, honestly "not measurable"
        # (M5.12) rather than inflating the denominator with a fabricated fail.
        outcomes = [self._env_receipt("pick_place", True)]
        rep = passk.reliability(outcomes, k=2)
        self.assertEqual(rep["tasks_measured"], 0)
        self.assertIsNone(rep["pass_k"])
        self.assertIn("not measurable", passk.render(rep))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
