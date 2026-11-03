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

    def test_bare_condition_excluded_from_low_outcome_grouping(self):
        # P62: the bare condition is the control arm (M5.12) - its low score is
        # expected, not a harness defect. Two bare lows -> no proposal.
        _write(self.tmp, [
            trace.make_trace("task_outcome", project="p1", task="survey", harness="h",
                             detail={"judge": "machine", "score": 0.2, "scale": [0, 1], "condition": "A-bare"}),
            trace.make_trace("task_outcome", project="p2", task="survey", harness="h",
                             detail={"judge": "machine", "score": 0.4, "scale": [0, 1], "condition": "A-bare"}),
        ])
        self.assertEqual(self._proposals("low-outcome"), [])

    def test_harness_condition_lows_still_fire(self):
        _write(self.tmp, [
            trace.make_trace("task_outcome", project="p1", task="survey", harness="h",
                             detail={"judge": "machine", "score": 0.2, "scale": [0, 1], "condition": "B-harness"}),
            trace.make_trace("task_outcome", project="p2", task="survey", harness="h",
                             detail={"judge": "machine", "score": 0.3, "scale": [0, 1], "condition": "B-harness"}),
        ])
        self.assertEqual(len(self._proposals("low-outcome")), 1)

    def test_mixed_bare_plus_one_harness_is_below_threshold(self):
        # bare excluded, harness count = 1 < min_count 2 -> no proposal
        _write(self.tmp, [
            trace.make_trace("task_outcome", project="p1", task="survey", harness="h",
                             detail={"judge": "machine", "score": 0.1, "scale": [0, 1], "condition": "A-bare"}),
            trace.make_trace("task_outcome", project="p2", task="survey", harness="h",
                             detail={"judge": "machine", "score": 0.2, "scale": [0, 1], "condition": "B-harness"}),
        ])
        self.assertEqual(self._proposals("low-outcome"), [])

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


class VocabularyV2RulesTest(unittest.TestCase):
    """P66, third leg of the vocabulary-v2 contract: every event the trace
    vocabulary accepts, an audit rule must read (a sensor nothing reads is
    dead weight). Simulated receipts - no real trace data touched."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def _proposals(self, by_rule=None):
        proposals = trace_audit.audit(self.tmp)
        if by_rule:
            return [p for p in proposals if p["rule"] == by_rule]
        return proposals

    def test_every_v2_event_has_an_audit_rule(self):
        ruled = {r["event"] for r in trace_audit.load_rules()}
        for event in ("context_pressure", "tool_error", "human_preference", "latency_anomaly"):
            self.assertIn(event, ruled)

    def test_context_pressure_repeat_fires_and_below_is_silent(self):
        _write(self.tmp, [
            trace.make_trace("context_pressure", project=f"p{i}", task="kg-build", harness="h",
                             detail={"tokens_used": 180_000}) for i in range(3)])
        self.assertEqual(len(self._proposals("context-pressure-repeat")), 1)
        p = self._proposals("context-pressure-repeat")[0]
        self.assertEqual(p["group"], "kg-build")
        self.assertEqual(p["mutation"], "Deepen")

    def test_tool_error_repeat_groups_by_tool(self):
        _write(self.tmp, [
            trace.make_trace("tool_error", project="p", task=f"t{i}", harness="h",
                             detail={"tool": "cron-parser", "error": "ValueError"}) for i in range(3)])
        proposals = self._proposals("tool-error-repeat")
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]["group"], "cron-parser")
        self.assertEqual(proposals[0]["mutation"], "Register")

    def test_human_preference_repeat_promotes_standing_directives(self):
        _write(self.tmp, [
            trace.make_trace("human_preference", project=f"p{i}", task="t", harness="h",
                             detail={"preference": "answer in Chinese first"}) for i in range(2)])
        proposals = self._proposals("human-preference-repeat")
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]["mutation"], "Promote")
        self.assertEqual(proposals[0]["count"], 2)

    def test_latency_anomaly_repeat_fires_per_operation(self):
        _write(self.tmp, [
            trace.make_trace("latency_anomaly", project=f"p{i}", task="t", harness="h",
                             detail={"operation": "catalog-embed", "ms": 9000}) for i in range(3)])
        self.assertEqual(len(self._proposals("latency-anomaly-repeat")), 1)

    def test_v2_receipts_without_detail_keys_read_as_nothing(self):
        # tool_error groups by detail.tool: a receipt without it cannot be
        # attributed to a tool, so it must stay below the rules (the template
        # contract names the required detail keys for exactly this reason).
        _write(self.tmp, [
            trace.make_trace("tool_error", project=f"p{i}", task="t", harness="h",
                             detail={"error": "boom"}) for i in range(5)])
        self.assertEqual(self._proposals("tool-error-repeat"), [])


if __name__ == "__main__":
    unittest.main()
