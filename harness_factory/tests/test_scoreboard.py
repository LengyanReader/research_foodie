"""Guards for the scored task set (P23): full baseline pinned, phantom ids rejected.

The baseline assertion is the holdout's alarm: if a classifier/derive change moves
a task's score off 1.0, this test fails and the change is a *deliberate* edit of
``data/scoreboard.json`` (with a reason), never a silent drift (M0.5).
"""

from __future__ import annotations

import unittest

from harness_factory import scoreboard


class ScoreboardDataTest(unittest.TestCase):
    def test_board_is_valid(self):
        self.assertEqual(scoreboard.validate_scoreboard(), [])

    def test_phantom_ids_are_rejected(self):
        board = scoreboard.load_scoreboard()
        board["tasks"][0]["allowed_domains"].append("no-such-domain")
        self.assertTrue(any("unknown domain" in p for p in scoreboard.validate_scoreboard(board)))

        board = scoreboard.load_scoreboard()
        board["tasks"][1]["must_capabilities"].append("no-such-capability")
        self.assertTrue(any("unknown capability" in p for p in scoreboard.validate_scoreboard(board)))

        board = scoreboard.load_scoreboard()
        board["tasks"][1]["must_modules"].append("M99")
        self.assertTrue(any("unknown module" in p for p in scoreboard.validate_scoreboard(board)))


class ScoreboardBaselineTest(unittest.TestCase):
    def test_every_task_scores_the_full_baseline(self):
        reports = scoreboard.run_all()
        self.assertGreaterEqual(len(reports), 4, "the scored task set shrank")
        for report in reports:
            self.assertEqual(
                report["total"],
                1.0,
                f"{report['id']} regressed off the 1.0 baseline: {report['scores']}",
            )
        ids = [r["id"] for r in reports]
        self.assertEqual(len(ids), len(set(ids)), "duplicate task ids")


class EffectAxisTest(unittest.TestCase):
    """P24: the effect axis is defined for every task but never invented.

    Effect answers "did the task go well" — a different claim from the five
    structural axes. Until a real run records a full receipt, every task must
    report unmeasured, and validate_scoreboard must refuse a receipt that is
    missing its judge, score, or date (M0.4).
    """

    def test_every_task_declares_an_effect_metric(self):
        for entry in scoreboard.load_scoreboard()["tasks"]:
            self.assertTrue(
                entry.get("effect_metric"),
                f"{entry['id']}: effect_metric missing — the effect axis is undefined for this task",
            )

    def test_effect_is_unmeasured_and_outside_the_structural_total(self):
        for report in scoreboard.run_all():
            self.assertEqual(report["effect"]["status"], "unmeasured")
            self.assertTrue(report["effect"]["metric"])
            self.assertEqual(len(report["scores"]), 5, "effect must not join the structural axes")

    def test_partial_effect_receipt_is_rejected(self):
        board = scoreboard.load_scoreboard()
        board["tasks"][0]["effect"] = {"status": "measured", "score": 4.5}
        self.assertTrue(any("effect" in p for p in scoreboard.validate_scoreboard(board)))

        board = scoreboard.load_scoreboard()
        board["tasks"][0]["effect"] = {
            "status": "measured", "score": 4.5, "judge": "human", "measured_on": "23-10-2026",
        }
        self.assertTrue(any("measured_on" in p or "effect" in p
                            for p in scoreboard.validate_scoreboard(board)))

    def test_full_effect_receipt_is_accepted_and_reported(self):
        board = scoreboard.load_scoreboard()
        entry = dict(board["tasks"][0])
        entry["effect"] = {
            "status": "measured", "score": 4.5, "judge": "human", "measured_on": "2026-10-23",
        }
        board["tasks"] = [entry]
        self.assertEqual(scoreboard.validate_scoreboard(board), [])
        report = scoreboard.run_task(entry)
        self.assertEqual(report["effect"]["status"], "measured")
        self.assertEqual(report["effect"]["score"], 4.5)
        self.assertIn("effect=measured", scoreboard.render([report]))


if __name__ == "__main__":
    unittest.main()
