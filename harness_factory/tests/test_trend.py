"""P69 simulation tests for the trend-review scaffold (pure, injected, offline).

These exercise the routine-work engine the way the loop actually calls it - over
synthetic intel items - so a bad bucketing or a non-deterministic scaffold fails
here, not in a live ``full-update``.  Nothing touches the committed snapshot: the
snapshot round-trip is run against a patched temp path.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from harness_factory import trend


def _item(topics, *, rel=2.0, date="2026-10-20", src="E", title="T", url="https://x/1"):
    return {"topics": topics, "relevance": rel, "published": date,
            "entity_name": src, "title": title, "url": url}


class AggregateTest(unittest.TestCase):
    def test_multimembership_counts_item_in_every_theme_it_touches(self):
        items = [_item(["agent-harness", "evaluation-gates", "mcp-skills-ecosystem"])]
        m = trend.aggregate(items, now="2026-11-01")
        # one item touching an industry topic (mcp) and two harness topics
        self.assertEqual(m["clusters"]["industry"]["count"], 1)
        self.assertEqual(m["clusters"]["harness"]["count"], 1)
        self.assertEqual(m["items"], 1)
        self.assertEqual(m["untracked"], 0)

    def test_agent_harness_is_a_harness_not_an_industry_signal(self):
        # P69 rebalance: the core harness topic must NOT be swallowed by industry
        m = trend.aggregate([_item(["agent-harness"])], now="2026-11-01")
        self.assertEqual(m["clusters"]["harness"]["count"], 1)
        self.assertEqual(m["clusters"]["industry"]["count"], 0)

    def test_unmatched_items_are_counted_as_untracked(self):
        m = trend.aggregate([_item(["some-brand-new-topic"])], now="2026-11-01")
        self.assertEqual(m["untracked"], 1)
        self.assertEqual(sum(c["count"] for c in m["clusters"].values()), 0)

    def test_recent_window_and_momentum(self):
        items = [
            _item(["agent-memory"], date="2026-10-30"),
            _item(["agent-memory"], date="2026-06-01"),
        ]
        m = trend.aggregate(items, now="2026-11-01", recent_days=30)
        h = m["clusters"]["harness"]
        self.assertEqual(h["count"], 2)     # both touch harness
        self.assertEqual(h["recent"], 1)    # only one is inside the 30d horizon

    def test_domain_cluster_sees_field_tagged_items(self):
        m = trend.aggregate([_item(["digital-humanities"])], now="2026-11-01")
        self.assertEqual(m["clusters"]["domains"]["count"], 1)


class SnapshotTest(unittest.TestCase):
    def test_snapshot_is_compact_and_caps_top(self):
        items = [_item(["agent-harness"], rel=3.0 - i * 0.1, url=f"https://x/{i}")
                 for i in range(20)]
        for i, it in enumerate(items):
            it["entity_name"] = f"src-{i % 5}"  # P77: varied sources so the top is fillable
        m = trend.aggregate(items, now="2026-11-01")
        snap = trend.to_snapshot(m, top=5)
        self.assertEqual(snap["clusters"]["harness"]["count"], 20)
        self.assertEqual(len(snap["clusters"]["harness"]["top"]), 5)
        # P77: the per-source cap holds at snapshot level too (5 sources x max 3)
        from collections import Counter

        per_source = Counter(r["source"] for r in snap["clusters"]["harness"]["top"])
        self.assertLessEqual(max(per_source.values()), 3)
        row = snap["clusters"]["harness"]["top"][0]
        self.assertEqual(set(row), {"rel", "date", "source", "title", "url"})
        self.assertEqual(snap["items"], 20)

    def test_snapshot_roundtrip_against_temp_path(self):
        items = [_item(["mcp-skills-ecosystem"])]
        snap = trend.to_snapshot(trend.aggregate(items, now="2026-11-01"))
        tmp = Path(tempfile.mkdtemp()) / "snap.json"
        with mock.patch.object(trend, "snapshot_path", return_value=tmp):
            trend.save_snapshot(snap)
            loaded = trend.load_snapshot()
        self.assertEqual(loaded, json.loads(tmp.read_text(encoding="utf-8")))
        self.assertEqual(loaded["clusters"]["industry"]["count"], 1)


class RenderTest(unittest.TestCase):
    def test_scaffold_is_bilingual_and_names_the_method(self):
        m = trend.aggregate([_item(["agent-harness"])], now="2026-11-01")
        text = trend.render(m)
        self.assertIn("中文速览", text)
        self.assertIn("raw material, not analysis", text)
        self.assertIn("Method · 写法", text)
        self.assertTrue(("引用即生命线" in text) or ("一手源" in text),
                        "the method must carry the citations-lifeline rule")
        for section in ("AI industry", "Harness directions",
                        "Other promising trajectories", "Field-by-field signals"):
            self.assertIn(section, text)

    def test_run_writes_trend_under_root_only(self):
        # the loop must stay contained to root: TREND.md lands there; with no
        # commit_snapshot the packaged SSOT snapshot is never touched.
        home = Path(tempfile.mkdtemp())
        (home / "updates").mkdir()
        (home / "updates" / "intel.jsonl").write_text(
            json.dumps(_item(["agent-harness"], url="https://x/a")), encoding="utf-8")
        out = trend.run(home, write=True)
        self.assertTrue((home / "updates" / "TREND.md").exists())
        self.assertEqual(out["clusters"]["harness"], 1)
        self.assertIn("recent_30d", out)
        self.assertNotIn("snapshot_wrote", out)  # commit_snapshot defaults False


if __name__ == "__main__":
    unittest.main()
