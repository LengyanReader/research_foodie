from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory import evolution, skill
from harness_factory.assemble import build_files
from harness_factory.capabilities import annotate, match
from harness_factory.derive import derive
from harness_factory.learning import aggregate, append_case, build_case, load_cases
from harness_factory.profile import profile_project, render_profile_md
from harness_factory.spec import FeatureVector, TaskSpec


def _make_project(root: Path) -> Path:
    (root / "tests").mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (root / "tests" / "test_x.py").write_text("def test_a():\n    assert True\n", encoding="utf-8")
    (root / "main.py").write_text("print('hi')\n", encoding="utf-8")
    return root


class SkillTest(unittest.TestCase):
    def test_index_and_read(self):
        self.assertTrue(skill.index())
        self.assertIsNotNone(skill.find("M0"))
        text = skill.read("derivation-rules")
        self.assertIn("Feature vector", text)
        self.assertIsNone(skill.read("does-not-exist"))
        self.assertIn("derivation-rules", skill.render_index())


class CapabilitiesTest(unittest.TestCase):
    def test_match_defaults(self):
        caps = {c["id"] for c in match(FeatureVector())}
        self.assertIn("baseline-discipline", caps)
        self.assertIn("verification-gate", caps)

    def test_high_stakes_and_long_horizon(self):
        f = FeatureVector(horizon="long_running", stakes="high")
        caps = {c["id"] for c in match(f)}
        self.assertIn("high-stakes-guardrails", caps)
        self.assertIn("human-review-gate", caps)
        self.assertIn("long-horizon-autonomy-control", caps)

    def test_annotate_adds_reasons_and_ids(self):
        plan = derive(TaskSpec(text="write a report"), FeatureVector())
        self.assertTrue(plan.capabilities)
        m0 = next(m for m in plan.modules if m.module_id == "M0")
        self.assertTrue(any(r.startswith("capability:") for r in m0.reasons))

    def test_build_files_has_provenance(self):
        plan = derive(TaskSpec(text="task"), FeatureVector())
        files = build_files(plan)
        self.assertIn(".harness/PROVENANCE.md", files)
        self.assertIn("Capabilities", files[".harness/PROVENANCE.md"])


class ProfileTest(unittest.TestCase):
    def test_detects_stack_and_capabilities(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_project(Path(tmp))
            profile = profile_project(root, goal="build a tool")
            self.assertEqual(profile.name, Path(tmp).name)
            self.assertIn("python", profile.stacks)
            self.assertIn("has-tests", profile.capabilities)
            self.assertIn("packaged", profile.capabilities)
            md = render_profile_md(profile)
            self.assertIn("PROFILE", md)
            self.assertIn("Capabilities", md)

    def test_profile_embeds_in_harness(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_project(Path(tmp))
            profile = profile_project(root, goal="build a tool")
            plan = derive(TaskSpec(text="build a tool"), FeatureVector())
            extra = {"profile_md": render_profile_md(profile), "profile_note": "- profiled"}
            files = build_files(plan, extra=extra)
            self.assertIn(".harness/PROFILE.md", files)
            self.assertIn("profiled", files[".harness/PROVENANCE.md"])


class LearningTest(unittest.TestCase):
    def test_case_roundtrip_and_aggregate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_project(Path(tmp))
            profile = profile_project(root, goal="g")
            plan = derive(TaskSpec(text="g"), FeatureVector())
            case = build_case(profile, plan)
            append_case(tmp, case)
            cases = load_cases(tmp)
            self.assertEqual(len(cases), 1)
            agg = aggregate(cases)
            self.assertEqual(agg["cases"], 1)
            self.assertIn("has-tests", agg["project_capabilities"])


class MutualLearningTest(unittest.TestCase):
    def test_recurring_capability_becomes_proposal(self):
        src = {"groups": {"projects": []}}
        wl = {"topics": [{"id": "agent-harness"}]}
        cases = [
            {"project_capabilities": ["custom-thing"], "modules": ["M0"]},
            {"project_capabilities": ["custom-thing"], "modules": ["M0"]},
        ]
        audits = evolution.audit(src, wl, [], cases=cases)
        self.assertIn("missing_capability", {a.kind for a in audits})
        proposals = evolution.propose(audits)
        self.assertTrue(
            any(p.action == "add_capability" and p.target == "custom-thing" for p in proposals)
        )


if __name__ == "__main__":
    unittest.main()
