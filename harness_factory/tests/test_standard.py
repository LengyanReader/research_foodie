import json
import tempfile
import unittest
from pathlib import Path

from harness_factory.registry import domains
from harness_factory import evolution, standard


class RubricCoverageTest(unittest.TestCase):
    def test_every_domain_has_a_rubric(self):
        table = standard.rubrics()
        self.assertIn("default", table)
        for did in domains():
            self.assertIn(did, table, f"missing rubric for domain {did!r}")

    def test_weights_sum_to_one(self):
        for did, rubric in standard.rubrics().items():
            total = round(sum(d["weight"] for d in rubric["dimensions"]), 6)
            self.assertEqual(total, 1.0, f"{did}: weights sum to {total}")

    def test_rubric_for_falls_back(self):
        self.assertEqual(
            standard.rubric_for("no-such-domain"), standard.rubrics()["default"]
        )
        self.assertTrue(standard.dimensions("deep-research"))


class RatchetTest(unittest.TestCase):
    def _ledger(self):
        return {"objectives": {}}

    def test_bar_requires_checkable_source(self):
        ledger = self._ledger()
        with self.assertRaises(ValueError):
            standard.set_bar(ledger, "o", "R4", "x", "not-a-url")
        bar = standard.set_bar(ledger, "o", "R4", "x", "https://example.org", "2026-01-01")
        self.assertTrue(bar["is_apex"])

    def test_score_and_ratchet_monotone(self):
        ledger = self._ledger()
        dom = "deep-research"
        dims = standard.dimensions(dom)
        total = standard.record_scores(ledger, "o", {d: 2 for d in dims}, dom)
        self.assertAlmostEqual(total, 2.0, places=4)
        first = standard.ratchet(ledger, "o", domain=dom)
        self.assertTrue(first["accepted"])
        self.assertAlmostEqual(first["floor"], 2.0, places=4)

    def test_regression_refused_unless_forced(self):
        ledger = self._ledger()
        dom = "research"
        dims = standard.dimensions(dom)
        standard.record_scores(ledger, "o", {d: 3 for d in dims}, dom)
        standard.ratchet(ledger, "o", domain=dom)
        standard.record_scores(ledger, "o", {d: 1 for d in dims}, dom)
        refused = standard.ratchet(ledger, "o", domain=dom)
        self.assertTrue(refused["regressed"])
        self.assertFalse(refused["accepted"])
        self.assertAlmostEqual(refused["floor"], 3.0, places=4)
        forced = standard.ratchet(ledger, "o", force=True, domain=dom)
        self.assertTrue(forced["accepted"])
        self.assertTrue(forced["forced"])

    def test_out_of_range_score_rejected(self):
        ledger = self._ledger()
        with self.assertRaises(ValueError):
            standard.record_scores(ledger, "o", {"fidelity": 5}, "excellence")


class PlanTest(unittest.TestCase):
    def _ledger(self):
        ledger = {"objectives": {}}
        standard.set_bar(
            ledger, "o", "R5", "x", "https://www.anthropic.com/engineering/building-effective-agents",
            "2026-01-01", "deep-research",
        )
        standard.record_scores(
            ledger, "o",
            {"fidelity": 1, "coverage": 1, "contradiction-honesty": 1, "calibration": 1},
            "deep-research",
        )
        return ledger

    def test_levers_have_default_and_cover(self):
        lv = standard.levers()
        self.assertIn("default", lv)
        self.assertIn("by_dim", lv)
        for domain in domains():
            for d in standard.dimensions(domain):
                lever = standard.lever_for(d)
                self.assertIn("modules", lever)

    def test_suggested_bar_is_sourced(self):
        bar = standard.suggested_bar("deep-research")
        self.assertIsNotNone(bar)
        self.assertTrue(bar["source"].startswith("http"))
        self.assertIsNone(standard.suggested_bar("no-such-domain"))

    def test_plan_nodes_sorted_with_modules_and_tools(self):
        p = standard.plan(self._ledger(), "o", "deep-research")
        self.assertTrue(p["nodes"])
        gaps = [n["gap"] for n in p["nodes"]]
        self.assertEqual(gaps, sorted(gaps, reverse=True))
        self.assertIn("M3", p["modules"])
        fidelity = next(n for n in p["nodes"] if n["dim"] == "fidelity")
        self.assertTrue(set(fidelity["modules"]) & {"M3", "M4"})
        self.assertTrue(fidelity["claude"])

    def test_plan_suggests_bar_when_unset(self):
        ledger = {"objectives": {}}
        standard.objective(ledger, "o", "deep-research")
        p = standard.plan(ledger, "o", "deep-research")
        self.assertIsNone(p["bar"])
        self.assertIsNotNone(p["suggested_bar"])

    def test_rendered_plan_mentions_claude(self):
        out = standard.render_plan(standard.plan(self._ledger(), "o", "deep-research"))
        self.assertIn("claude:", out)
        self.assertIn("observe-only", out)


class StaleFrontierAuditTest(unittest.TestCase):
    NOW = "2026-10-14T00:00:00+00:00"
    EMPTY_SRC = {"groups": {}}
    EMPTY_WL = {"topics": []}

    def _objectives(self):
        return {
            "fresh": {
                "bar": {"level": "R4", "name": "x", "is_apex": True},
                "frontier_checked_at": "2026-10-10T00:00:00+00:00",
            },
            "stale": {
                "bar": {"level": "R5", "name": "y", "is_apex": True},
                "frontier_checked_at": "2026-06-01T00:00:00+00:00",
            },
            "never": {"bar": {"level": "R4", "name": "z", "is_apex": True}},
            "unbarred": {"bar": None, "floor": 2.0},
        }

    def _audits(self):
        return evolution.audit(
            self.EMPTY_SRC,
            self.EMPTY_WL,
            [],
            standard_objectives=self._objectives(),
            now=self.NOW,
            frontier_max_age_days=90,
        )

    def test_only_stale_and_never_and_unbarred_flagged(self):
        subjects = {a.subject for a in self._audits() if a.kind == "stale_frontier"}
        self.assertEqual(subjects, {"stale", "never", "unbarred"})

    def test_severity_by_case(self):
        sev = {a.subject: a.severity for a in self._audits() if a.kind == "stale_frontier"}
        self.assertEqual(sev["stale"], "medium")
        self.assertEqual(sev["never"], "high")
        self.assertEqual(sev["unbarred"], "high")

    def test_proposal_is_recheck_frontier(self):
        proposals = {p.target: p for p in evolution.propose(self._audits())}
        self.assertIn("stale", proposals)
        self.assertEqual(proposals["stale"].action, "recheck_frontier")

    def test_no_objectives_no_audit(self):
        audits = evolution.audit(self.EMPTY_SRC, self.EMPTY_WL, [], now=self.NOW)
        self.assertEqual([a for a in audits if a.kind == "stale_frontier"], [])

    def test_run_evolution_reads_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            updates = Path(tmp) / "updates"
            updates.mkdir(parents=True)
            (updates / "standard.json").write_text(
                json.dumps({"objectives": self._objectives()}, ensure_ascii=False),
                encoding="utf-8",
            )
            summary = evolution.run_evolution(tmp, self.EMPTY_SRC, self.EMPTY_WL, dry_run=True)
            subjects = {a["subject"] for a in summary["audits"] if a["kind"] == "stale_frontier"}
            self.assertEqual(subjects, {"stale", "never", "unbarred"})


if __name__ == "__main__":
    unittest.main()
