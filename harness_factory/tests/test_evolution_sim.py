"""P67: the evolution detector exercised on synthetic registries (the P63
simulation pattern extended from trace-audit to the structural loop).

``evolution.audit`` is a pure function over injected data; the live-loop
numbers (92% coverage etc.) are the SAME computation on the real SSOT. This
file pins each detector leg - uncovered_topic, empty_group, stale_source,
untracked_source (host union + www normalization), missing_capability,
stale_frontier - on fixtures where the right answer is known by construction,
so a regression in any leg fails here rather than in next month's EVOLUTION.md.
"""

from __future__ import annotations

import unittest

from harness_factory import evolution


def _sources(**groups):
    base = {
        "topic_ids": [],
        "groups": {
            "projects": [
                {"id": "a-src", "name": "A", "url": "https://a.example.com/",
                 "feed": "https://a.example.com/rss", "topics": ["alpha"]},
            ],
            "harnesses": [
                {"id": "h1", "name": "H", "url": "https://h.example/", "topics": ["beta"]},
            ],
        },
    }
    base["groups"].update(groups)
    return base


class UncoveredTopicSimTest(unittest.TestCase):
    def test_uncovered_topic_fires_only_for_the_wiring_hole(self):
        wl = {"topics": [{"id": "alpha"}, {"id": "beta"}, {"id": "gamma"}]}
        audits = evolution.audit(_sources(), wl, now="2026-11-03T00:00:00+00:00")
        subjects = {a.subject for a in audits if a.kind == "uncovered_topic"}
        self.assertEqual(subjects, {"gamma"})  # alpha/beta are carried; gamma has no source

    def test_full_wiring_is_silent(self):
        wl = {"topics": [{"id": "alpha"}, {"id": "beta"}]}
        audits = evolution.audit(_sources(), wl, now="2026-11-03T00:00:00+00:00")
        self.assertEqual([a for a in audits if a.kind == "uncovered_topic"], [])


class EmptyGroupSimTest(unittest.TestCase):
    def test_empty_group_fires(self):
        audits = evolution.audit(_sources(outlets=[]), {"topics": ["x"] and []})
        fired = {a.subject for a in audits if a.kind == "empty_group"}
        self.assertIn("outlets", fired)
        self.assertNotIn("projects", fired)


class StaleSourceSimTest(unittest.TestCase):
    def test_feed_source_without_items_is_flagged(self):
        audits = evolution.audit(_sources(), {"topics": []}, intel_items=[],
                                 seen_entities={"h1"})
        fired = {a.subject for a in audits if a.kind == "stale_source"}
        self.assertIn("a-src", fired)  # has a feed, produced nothing this run

    def test_source_that_produced_is_clean(self):
        audits = evolution.audit(_sources(), {"topics": []}, seen_entities={"a-src"})
        self.assertEqual([a for a in audits if a.kind == "stale_source"], [])


class UntrackedSourceSimTest(unittest.TestCase):
    def test_candidate_on_new_host_fires_once(self):
        audits = evolution.audit(_sources(), {"topics": []},
                                 queue_rows=[{"url": "https://new.example/x"},
                                             {"url": "https://new.example/y"}])
        fired = [a.subject for a in audits if a.kind == "untracked_source"]
        self.assertEqual(fired, ["new.example"])

    def test_known_hosts_do_not_fire_even_on_feed_variants(self):
        # P59's fix pinned: www-variant and feed-domain hits are tracked
        audits = evolution.audit(_sources(), {"topics": []},
                                 queue_rows=[{"url": "https://www.a.example.com/post"},
                                             {"url": "https://h.example/thing"}])
        self.assertEqual([a for a in audits if a.kind == "untracked_source"], [])


class MissingCapabilitySimTest(unittest.TestCase):
    def test_recurring_unknown_capability_fires(self):
        cases = [{"project_capabilities": ["totally-new-cap"]},
                 {"project_capabilities": ["totally-new-cap", "verification-gate"]}]
        audits = evolution.audit(_sources(), {"topics": []}, cases=cases)
        fired = {a.subject for a in audits if a.kind == "missing_capability"}
        self.assertIn("totally-new-cap", fired)
        self.assertNotIn("verification-gate", fired)  # known cap never a gap

    def test_single_occurrence_is_below_threshold(self):
        audits = evolution.audit(_sources(), {"topics": []},
                                 cases=[{"project_capabilities": ["once-only"]}])
        self.assertEqual([a for a in audits if a.kind == "missing_capability"], [])


class StaleFrontierSimTest(unittest.TestCase):
    NOW = "2026-11-03T00:00:00+00:00"

    def test_apex_bar_older_than_the_window_fires(self):
        objectives = {"kg": {"bar": {"is_apex": True, "level": "R4", "name": "x"},
                             "frontier_checked_at": "2026-06-01T00:00:00+00:00"}}
        audits = evolution.audit(_sources(), {"topics": []},
                                 standard_objectives=objectives, now=self.NOW)
        fired = [a for a in audits if a.kind == "stale_frontier"]
        self.assertEqual([a.subject for a in fired], ["kg"])

    def test_fresh_check_is_clean_and_missing_check_fires_high(self):
        fresh = {"kg": {"bar": {"is_apex": True, "level": "R4"},
                        "frontier_checked_at": "2026-11-01T00:00:00+00:00"}}
        audits = evolution.audit(_sources(), {"topics": []},
                                 standard_objectives=fresh, now=self.NOW)
        self.assertEqual([a for a in audits if a.kind == "stale_frontier"], [])
        never = {"kg": {"bar": {"is_apex": True, "level": "R4"}}}
        audits = evolution.audit(_sources(), {"topics": []},
                                 standard_objectives=never, now=self.NOW)
        fired = [a for a in audits if a.kind == "stale_frontier"]
        self.assertEqual([a.severity for a in fired], ["high"])


class HealthyRegistrySimTest(unittest.TestCase):
    def test_no_false_positives_on_a_clean_small_registry(self):
        wl = {"topics": [{"id": "alpha"}, {"id": "beta"}]}
        audits = evolution.audit(_sources(), wl, seen_entities={"a-src", "h1"},
                                 queue_rows=[], cases=[], standard_objectives={})
        self.assertEqual(audits, [])


class P68ToolStackSimTest(unittest.TestCase):
    """P68: the standing tool-stack scan metabolizes through the SAME detector
    legs - a registered ai-tool-stack carrier that goes silent must surface as a
    stale_source, and a healthy wiring must stay clean (no phantom proposals)."""

    def _wired(self):
        srcs = _sources(tools=[
            {"id": "vllm", "name": "vLLM", "url": "https://github.com/vllm-project/vllm",
             "feed": "https://github.com/vllm-project/vllm/releases.atom",
             "topics": ["ai-tool-stack"]},
        ])
        srcs["topic_ids"] = ["alpha", "beta", "ai-tool-stack"]
        wl = {"topics": [{"id": "alpha"}, {"id": "beta"}, {"id": "ai-tool-stack"}]}
        return srcs, wl

    def test_silent_tool_feed_surfaces_as_stale_source(self):
        srcs, wl = self._wired()
        # seen_entities = entities that PRODUCED this run; vllm registered its
        # feed but delivered nothing, so it is absent - that is the stale leg.
        audits = evolution.audit(srcs, wl, seen_entities={"a-src"},
                                 queue_rows=[], cases=[], standard_objectives={})
        stale = {a.subject for a in audits if a.kind == "stale_source"}
        self.assertIn("vllm", stale, "a tool carrier whose feed delivered nothing must be flagged")
        self.assertNotIn("h1", stale, "feedless entities must not be false-flagged")

    def test_healthy_wiring_is_clean_and_covered(self):
        from harness_factory import evolution as evo

        srcs, wl = self._wired()
        m = evo.snapshot(srcs, wl)
        self.assertEqual(m["uncovered_topics"], [])
        self.assertAlmostEqual(m["topic_coverage"], 1.0)
        audits = evo.audit(srcs, wl, seen_entities={"a-src", "h1", "vllm"},
                           queue_rows=[], cases=[], standard_objectives={})
        self.assertEqual(audits, [])


if __name__ == "__main__":
    unittest.main()
