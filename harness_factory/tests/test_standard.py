import unittest

from harness_factory.registry import domains
from harness_factory import standard


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


if __name__ == "__main__":
    unittest.main()
