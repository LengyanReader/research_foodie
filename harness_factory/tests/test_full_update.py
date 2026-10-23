"""Guards for the one-command full update (P30): all phases run, the report
lands, failures are isolated and never faked (M0.3)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from harness_factory import full_update


class FullUpdateTest(unittest.TestCase):
    def test_offline_full_update_runs_all_phases_and_writes_report(self):
        tmp = Path(tempfile.mkdtemp())
        report = full_update.run_full_update(tmp, offline=True)
        names = [p["name"] for p in report["phases"]]
        self.assertEqual(
            names,
            ["intel", "probe-domains", "trace-audit", "evolve", "cycle-audit", "scoreboard"],
        )
        self.assertEqual(report["phases"][0]["status"], "skipped")
        for phase in report["phases"][1:]:
            self.assertEqual(phase["status"], "ok", phase)
        path = tmp / full_update.REPORT_REL
        self.assertTrue(path.exists())
        self.assertIn("FULL-UPDATE", path.read_text(encoding="utf-8"))
        self.assertIn("Human gate", path.read_text(encoding="utf-8"))

    def test_failed_phase_reports_and_never_fakes(self):
        report = {
            "ts": "t",
            "root": "r",
            "offline": True,
            "phases": [
                {"name": "x", "status": "error", "error": "boom"},
                {"name": "y", "status": "ok", "result": {}},
            ],
        }
        text = full_update.render(report)
        self.assertIn("ERROR boom", text)
        self.assertNotIn("fake", text.lower())


if __name__ == "__main__":
    unittest.main()
