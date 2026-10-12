from __future__ import annotations

import unittest

from harness_factory.derive import derive
from harness_factory.spec import FeatureVector, TaskSpec


def _plan(**features):
    base = dict(horizon="session", verifiability="medium", stakes="medium")
    base.update(features)
    feats = FeatureVector(**base)
    return derive(TaskSpec(text="t"), feats)


class DeriveTest(unittest.TestCase):
    def test_always_on_modules(self):
        plan = _plan()
        enabled = {m.module_id for m in plan.enabled_modules()}
        for mid in ("M0", "M1", "M3", "M7"):
            self.assertIn(mid, enabled)

    def test_memory_off_for_one_shot(self):
        plan = _plan(horizon="one_shot")
        m2 = next(m for m in plan.modules if m.module_id == "M2")
        self.assertFalse(m2.enabled)

    def test_evolution_on_for_multi_session(self):
        plan = _plan(horizon="multi_session")
        m5 = next(m for m in plan.modules if m.module_id == "M5")
        self.assertTrue(m5.enabled)
        self.assertEqual(m5.params["evolution_cadence"], "per_session")

    def test_gate_strict_when_verifiability_low(self):
        plan = _plan(verifiability="low")
        self.assertEqual(plan.params()["gate_strictness"], "strict")

    def test_gate_relaxed_when_high_verifiability_low_stakes(self):
        plan = _plan(verifiability="high", stakes="low")
        self.assertEqual(plan.params()["gate_strictness"], "relaxed")

    def test_m4_provenance_for_document_artifact(self):
        plan = _plan(artifact="document", grounding="off")
        m4 = next(m for m in plan.modules if m.module_id == "M4")
        self.assertTrue(m4.enabled)

    def test_m8_on_for_high_stakes(self):
        plan = _plan(stakes="high")
        m8 = next(m for m in plan.modules if m.module_id == "M8")
        self.assertTrue(m8.enabled)

    def test_invalid_feature_raises(self):
        with self.assertRaises(ValueError):
            derive(TaskSpec(text="t"), FeatureVector(horizon="forever"))


if __name__ == "__main__":
    unittest.main()
