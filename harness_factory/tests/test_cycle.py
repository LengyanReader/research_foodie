"""Guards for the capability-cycle mechanism (SSOT = ``data/cycles.json``).

A *cycle* is one round of capability expansion. These tests make the mechanism
load-bearing rather than decorative:

- the registry must be internally consistent (every `added` id exists in the live
  SSOT, every claimed clause is anchored in its own ``core/`` doc, no duplicate
  registrations, every deferral carries a reason *and* a revisit trigger);
- ``cycle.audit()`` must report **no hard problems** - so a future round that
  forgets to anchor a clause, or that defers something without saying why,
  fails CI instead of drifting;
- the soft **gap surface** is stable in shape (it is the next round's input).

The gap list itself is deliberately *not* asserted empty: gaps are the worklist.
"""

from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path

from harness_factory import cycle
from harness_factory.cli import main

HARNESS = Path(__file__).resolve().parent.parent  # .../harness_factory


class CycleRegistryTest(unittest.TestCase):
    def test_registry_has_required_top_level_keys(self):
        reg = cycle.registry()
        for key in ("updated", "definition_of_done", "cycles", "roadmap"):
            self.assertIn(key, reg)

    def test_every_cycle_is_well_formed(self):
        for entry in cycle.cycles():
            cid = entry.get("id")
            self.assertTrue(cid, "every cycle needs an id")
            self.assertIn(entry.get("status"), cycle.CYCLE_STATUSES, cid)
            self.assertRegex(entry.get("date", ""), r"^\d{4}-\d{2}-\d{2}$", cid)
            self.assertTrue(entry.get("title_en"), cid)
            self.assertTrue(entry.get("title_zh"), cid)
            self.assertTrue(entry.get("slices"), cid)
            added = entry.get("added")
            self.assertIsInstance(added, dict, cid)
            for key in ("capabilities", "domains", "clauses", "references"):
                self.assertIsInstance(added.get(key, []), list, f"{cid}.{key}")

    def test_cycle_ids_are_unique(self):
        ids = [c["id"] for c in cycle.cycles()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_definition_of_done_is_data_with_severity(self):
        dod = cycle.definition_of_done()
        self.assertGreaterEqual(len(dod), 6)
        for entry in dod:
            self.assertTrue(entry.get("key"), entry)
            self.assertTrue(entry.get("check"), entry)
            self.assertIsInstance(entry.get("hard"), bool, entry)

    def test_deferrals_carry_a_reason_and_a_revisit_trigger(self):
        deferred = [item for item in cycle.roadmap() if item.get("status") == "deferred"]
        self.assertTrue(deferred, "the registry should record at least one deliberate non-addition")
        for item in deferred:
            self.assertTrue(item.get("reason"), item.get("id"))
            self.assertTrue(item.get("revisit_when"), item.get("id"))
            self.assertTrue(item.get("source"), item.get("id"))


class CycleDoDTest(unittest.TestCase):
    def test_no_hard_problems(self):
        """The mechanism gates itself: any hard problem fails the build."""
        result = cycle.audit()
        self.assertEqual([], result["problems"])
        self.assertTrue(result["ok"])

    def test_claimed_clauses_are_anchored_in_their_own_module(self):
        anchors = cycle.clause_anchors()
        for entry in cycle.cycles():
            for label in entry.get("added", {}).get("clauses", []):
                want = cycle.MODULE_DOCS[label.split(".")[0]]
                self.assertIn(label, anchors, f"{entry['id']}: {label} is not anchored in core/")
                self.assertIn(
                    want,
                    anchors[label],
                    f"{entry['id']}: {label} must be anchored in core/{want}",
                )

    def test_capability_triggers_use_only_declared_predicates(self):
        vocab = cycle.predicate_vocabulary()
        domains = cycle._domains()
        caps = cycle._capabilities()
        for cid, meta in caps.items():
            self.assertEqual(
                [], cycle._when_problems(cid, meta.get("when") or {}, vocab, domains), cid
            )

    def test_metrics_match_the_live_ssot(self):
        metrics = cycle.audit()["metrics"]
        self.assertEqual(len(cycle.cycles()), metrics["cycles"])
        self.assertEqual(len(cycle.roadmap()), metrics["roadmap"])
        self.assertEqual(len(cycle.definition_of_done()), metrics["definition_of_done"])
        self.assertEqual(len(cycle._capabilities()), metrics["capabilities"])
        self.assertEqual(len(cycle._domains()), metrics["domains"])


class CycleRenderTest(unittest.TestCase):
    def test_index_lists_every_cycle(self):
        text = cycle.render_index()
        for entry in cycle.cycles():
            self.assertIn(entry["id"], text)

    def test_detail_and_unknown_id(self):
        cid = cycle.cycles()[0]["id"]
        self.assertIn(cid, cycle.render_detail(cid) or "")
        self.assertIsNone(cycle.render_detail("no-such-cycle"))

    def test_roadmap_renders_reason_and_trigger(self):
        text = cycle.render_roadmap()
        for item in cycle.roadmap():
            self.assertIn(item["id"], text)
            self.assertIn(item["reason"][:40], text)

    def test_roadmap_says_where_a_done_item_landed(self):
        text = cycle.render_roadmap()
        done = [i for i in cycle.roadmap() if i.get("status") == "done" and i.get("done_in")]
        self.assertTrue(done, "a closed roadmap item should record where it landed")
        for item in done:
            self.assertIn(f"done in {item['done_in']}", text)

    def test_audit_render_is_honest_about_severity(self):
        text = cycle.render_audit(cycle.audit(), show_gaps=5)
        self.assertIn("## Problems (hard)", text)
        self.assertIn("## Gaps (soft", text)


class CycleCliTest(unittest.TestCase):
    def _run(self, *argv: str) -> tuple[int, str]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            code = main(list(argv))
        return code, buf.getvalue()

    def test_list_and_audit_exit_zero(self):
        code, out = self._run("cycle")
        self.assertEqual(0, code)
        self.assertIn("Capability cycles", out)

        code, out = self._run("cycle", "audit")
        self.assertEqual(0, code)
        self.assertIn("Cycle audit", out)

    def test_audit_json_is_machine_readable(self):
        code, out = self._run("cycle", "--json", "audit")
        self.assertEqual(0, code)
        data = json.loads(out)
        self.assertEqual({"ok", "problems", "gaps", "metrics"}, set(data))

    def test_show_unknown_cycle_is_an_error(self):
        code, _ = self._run("cycle", "show", "nope")
        self.assertEqual(2, code)


if __name__ == "__main__":
    unittest.main()
