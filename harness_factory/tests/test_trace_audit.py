"""Guards for the D1 stage-B rules auditor (P25): every rule fires on its pattern,
stays silent below threshold, and the proposal path is journal-only."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory import trace, trace_audit


def _write(kb: Path, lines: list[dict]) -> None:
    for line in lines:
        trace.record_trace(kb / trace.TRACES_REL, line)


class RulesDataTest(unittest.TestCase):
    def test_rules_are_valid(self):
        self.assertEqual(trace_audit.validate_rules(), [])

    def test_rules_reject_phantom_names(self):
        rules = trace_audit.load_rules()
        rules[0]["event"] = "opinion"
        self.assertTrue(any("unknown event" in p for p in trace_audit.validate_rules(rules)))
        rules = trace_audit.load_rules()
        rules[0]["mutation"] = "Rewrite"
        self.assertTrue(any("M5.3 vocabulary" in p for p in trace_audit.validate_rules(rules)))


class AuditRulesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def _proposals(self, by_rule=None):
        proposals = trace_audit.audit(self.tmp)
        if by_rule:
            return [p for p in proposals if p["rule"] == by_rule]
        return proposals

    def test_gate_miss_repeat_fires_at_threshold(self):
        lines = []
        for i in range(3):
            lines.append(
                trace.make_trace(
                    "gate_miss", project=f"p{i}", task="t", harness="h",
                    detail={"failed_gates": ["check-py-runs"]},
                )
            )
        _write(self.tmp, lines)
        proposals = self._proposals("gate-miss-repeat")
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]["mutation"], "Deepen")
        self.assertEqual(proposals[0]["group"], ["check-py-runs"])
        self.assertEqual(proposals[0]["count"], 3)

    def test_gate_miss_below_threshold_is_silent(self):
        _write(
            self.tmp,
            [trace.make_trace("gate_miss", project="p", task="t", harness="h",
                              detail={"failed_gates": ["check-py-runs"]})],
        )
        self.assertEqual(self._proposals("gate-miss-repeat"), [])

    def test_capability_unused_fires_per_capability(self):
        lines = []
        for i in range(3):
            lines.append(
                trace.make_trace(
                    "capability_unused", project=f"p{i}", task="t", harness="h",
                    detail={"capability": "prose-polish"},
                )
            )
        _write(self.tmp, lines)
        self.assertEqual(len(self._proposals("capability-unused-repeat")), 1)

    def test_low_outcome_counts_only_numeric_scores_at_or_below_max(self):
        lines = [
            trace.make_trace("task_outcome", project="p1", task="lit-review", harness="h",
                             detail={"judge": "human", "score": 1}),
            trace.make_trace("task_outcome", project="p2", task="lit-review", harness="h",
                             detail={"judge": "human", "score": 2}),
            trace.make_trace("task_outcome", project="p3", task="lit-review", harness="h",
                             detail={"judge": "human", "score": 4}),
            trace.make_trace("task_outcome", project="p4", task="lit-review", harness="h",
                             detail={"judge": "human", "score": "B"}),
        ]
        _write(self.tmp, lines)
        proposals = self._proposals("low-outcome")
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]["count"], 2)  # 1 and 2 fire; 4 and the grade do not

    def test_declared_scale_makes_perfect_scores_not_low(self):
        # P45.R1: 1.0 on a declared [0,1] scale is PERFECT -- the scale-blind
        # rule used to file it as a low outcome.
        _write(self.tmp, [
            trace.make_trace("task_outcome", project="p1", task="lit-review", harness="h",
                             detail={"judge": "machine", "score": 1.0, "scale": [0, 1]}),
            trace.make_trace("task_outcome", project="p2", task="lit-review", harness="h",
                             detail={"judge": "machine", "score": 1.0, "scale": [0, 1]}),
        ])
        self.assertEqual(self._proposals("low-outcome"), [])

    def test_declared_scale_low_scores_still_fire(self):
        _write(self.tmp, [
            trace.make_trace("task_outcome", project="p1", task="lit-review", harness="h",
                             detail={"judge": "machine", "score": 0.2, "scale": [0, 1]}),
            trace.make_trace("task_outcome", project="p2", task="lit-review", harness="h",
                             detail={"judge": "machine", "score": 0.3, "scale": [0, 1]}),
        ])
        self.assertEqual(len(self._proposals("low-outcome")), 1)

    def test_scale_validation_rejects_inverted_or_nonnumeric(self):
        line = trace.make_trace("task_outcome", project="p", task="t", harness="h",
                                detail={"judge": "human", "score": 1, "scale": [1, 0]})
        self.assertIn("scale", "; ".join(trace.validate(line)))
        line = trace.make_trace("task_outcome", project="p", task="t", harness="h",
                                detail={"judge": "human", "score": 1, "scale": ["a", "b"]})
        self.assertIn("scale", "; ".join(trace.validate(line)))
        line = trace.make_trace("task_outcome", project="p", task="t", harness="h",
                                detail={"judge": "human", "score": 1, "scale": [0, 1]})
        self.assertEqual(trace.validate(line), [])

    def test_emit_writes_journal_and_report_only(self):
        _write(
            self.tmp,
            [trace.make_trace("gate_miss", project=f"p{i}", task="t", harness="h",
                              detail={"failed_gates": ["check-py-runs"]}) for i in range(3)],
        )
        proposals = trace_audit.audit(self.tmp)
        journal, report = trace_audit.emit(self.tmp, proposals)
        self.assertTrue(journal.exists())
        self.assertTrue(report.exists())
        self.assertIn("gate-miss-repeat", report.read_text(encoding="utf-8"))
        # the SSOT stays untouched: the only writes are the journal + report
        self.assertEqual(sorted(p.name for p in (self.tmp / "updates").iterdir()),
                         ["TRACE-EVOLUTION.md", "traces-proposals.jsonl", "traces.jsonl"])


if __name__ == "__main__":
    unittest.main()
