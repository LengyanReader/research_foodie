from __future__ import annotations

import unittest

from harness_factory.classify import classify
from harness_factory.spec import TaskSpec


class ClassifyTest(unittest.TestCase):
    def test_domain_from_keywords(self):
        feats = classify(TaskSpec(text="write a literature review with citations"))
        self.assertEqual(feats.domain, "research")

    def test_high_verifiability_from_tests(self):
        feats = classify(TaskSpec(text="add unit tests and make the benchmark pass"))
        self.assertEqual(feats.verifiability, "high")

    def test_high_stakes_from_deploy(self):
        feats = classify(TaskSpec(text="deploy to production and delete old data"))
        self.assertEqual(feats.stakes, "high")

    def test_horizon_long_running(self):
        feats = classify(TaskSpec(text="a long-running continuous project"))
        self.assertEqual(feats.horizon, "long_running")

    def test_horizon_from_weeks(self):
        # P36: "week" was absent from the horizon vocabulary, so the flagship
        # README example ("over several weeks") landed on the session default
        # and never enabled M5 (self-evolution) or durable memory.
        feats = classify(TaskSpec(text="write a literature review with citations over several weeks"))
        self.assertEqual(feats.horizon, "multi_session")
        self.assertEqual(
            classify(TaskSpec(text="写一篇文献综述，持续数周，跨多个会话完成")).horizon,
            "multi_session",
        )

    def test_literature_review_is_not_human_review(self):
        # P36: bare "review" fired the collaboration cue, so every literature
        # review was read as a human-in-the-loop review workflow (M8 + lowered
        # autonomy) — a misfire that once reached the scored holdout baseline.
        feats = classify(TaskSpec(text="write a literature review with citations over several weeks"))
        self.assertEqual(feats.collaboration, "solo")
        self.assertNotEqual(
            classify(TaskSpec(text="systematic review of the screening literature")).collaboration,
            "human_review",
        )

    def test_review_requests_still_fire_human_review(self):
        # Guard against over-removal: the compound verb-request forms keep firing.
        for text in (
            "review my PR before it merges",
            "run a code review on this module",
            "act as the reviewer for this draft",
        ):
            self.assertEqual(
                classify(TaskSpec(text=text)).collaboration, "human_review", text
            )

    def test_overrides_win(self):
        feats = classify(TaskSpec(text="quick draft"), overrides={"stakes": "high"})
        self.assertEqual(feats.stakes, "high")
        self.assertEqual(feats.source, "flags")

    def test_explicit_domain_override(self):
        feats = classify(TaskSpec(text="do something vague"), overrides={"domain": "devops"})
        self.assertEqual(feats.domain, "devops")

    def test_defaults_to_general(self):
        feats = classify(TaskSpec(text="bake a cake"))
        self.assertEqual(feats.domain, "general")

    def test_explicit_artifact_cue_beats_the_domain_default(self):
        # the domain is a scenario prior; "report" is evidence about this task
        feats = classify(TaskSpec(text="write a report from these interviews"))
        self.assertEqual(feats.artifact, "document")

    def test_explicit_source_demand_raises_grounding(self):
        feats = classify(TaskSpec(text="write a literature review with citations"))
        self.assertEqual(feats.grounding, "required")

    def test_grounding_stays_preferred_without_a_cue(self):
        self.assertNotEqual(classify(TaskSpec(text="bake a cake")).grounding, "required")


if __name__ == "__main__":
    unittest.main()
