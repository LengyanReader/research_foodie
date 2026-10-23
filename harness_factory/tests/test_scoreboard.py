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


if __name__ == "__main__":
    unittest.main()
