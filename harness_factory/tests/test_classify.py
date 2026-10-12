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


if __name__ == "__main__":
    unittest.main()
