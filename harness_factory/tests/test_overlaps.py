"""Guards for P31: discipline intersections are named, not dropped.

Overlaps are declared data (domains.json `overlaps`), the near-domain report
makes the runner-up visible, and a strong neighbour contributes its
domain-keyed capabilities to the union. These guards pin all three behaviours
and the routing battery that motivated the round.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from harness_factory.assemble import build_files
from harness_factory.classify import classify
from harness_factory.derive import derive
from harness_factory.spec import TaskSpec

DATA = Path(__file__).resolve().parent.parent / "src/harness_factory/data"


def _plan(text: str):
    task = TaskSpec(text=text)
    return task, derive(task, classify(task))


class OverlapsDataTest(unittest.TestCase):
    def test_every_overlap_target_exists(self):
        domains = json.loads((DATA / "domains.json").read_text(encoding="utf-8"))
        problems = []
        for did, meta in domains.items():
            for alt in meta.get("overlaps", {}):
                if alt not in domains:
                    problems.append(f"{did} -> {alt}")
        self.assertEqual(problems, [], f"overlap targets that do not exist: {problems}")

    def test_overlaps_are_declared_for_the_known_intersections(self):
        domains = json.loads((DATA / "domains.json").read_text(encoding="utf-8"))
        for pair in (("digital-humanities", "history"), ("statistics", "data-science")):
            a, b = pair
            self.assertTrue(
                b in domains[a].get("overlaps", {}) or a in domains[b].get("overlaps", {}),
                f"overlap {a} <-> {b} is not declared",
            )


class RoutingBatteryTest(unittest.TestCase):
    """The 8-sample battery from the P31 evaluation: each case names an
    acceptable set, and the motivating misroute must surface its other half."""

    CASES = {
        "vague": ("帮我做点研究", {"general"}),
        "plan-artifact": ("写一份下周的会议议程和行动计划", {"general"}),
        "zh-history": ("梳理清代江南的方志修纂传统", {"digital-humanities", "history"}),
        "en-music": ("Compose a soundtrack for a documentary", {"arts-design"}),
        "fr": ("Rédiger une revue de littérature avec citations", {"research"}),
        "plan": ("make a project plan", {"general"}),
        "frontier": ("Build a neuro-symbolic reasoner for legal texts", {"law"}),
        "safety": ("Conduct a red-team audit of our coding agent and write the safety case", {"ai-safety"}),
    }

    def test_battery_routes_into_the_allowed_sets(self):
        for name, (text, allowed) in self.CASES.items():
            task, plan = _plan(text)
            self.assertIn(
                plan.features.domain, allowed,
                f"{name}: {plan.features.domain!r} not in {allowed}",
            )

    def test_fangzhi_intersection_names_history(self):
        task, plan = _plan("梳理清代江南的方志修纂传统")
        self.assertIn("history", [s["domain"] for s in plan.secondary_domains])


class SecondaryDomainTest(unittest.TestCase):
    def test_strong_neighbour_contributes_its_capabilities(self):
        task, plan = _plan("Bayesian regression on a dataset with model evaluation")
        sec = {s["domain"]: s for s in plan.secondary_domains}
        self.assertIn("statistics", sec)
        self.assertIn("statistical-inference", sec["statistics"]["added_capabilities"])
        self.assertIn("statistical-inference", plan.capabilities)

    def test_clean_task_has_no_secondary_domains(self):
        task, plan = _plan("Add unit tests to the parser")
        self.assertEqual(plan.secondary_domains, [])

    def test_emitted_harness_names_the_intersection(self):
        task = TaskSpec(text="Bayesian regression on a dataset with model evaluation")
        files = build_files(derive(task, classify(task)))
        self.assertIn("Secondary domains", files["AGENTS.md"])
        self.assertIn("statistics", files["AGENTS.md"])
        # and a clean task's AGENTS.md carries no empty intersection stanza
        task2 = TaskSpec(text="Add unit tests to the parser")
        files2 = build_files(derive(task2, classify(task2)))
        self.assertNotIn("Secondary domains", files2["AGENTS.md"])


if __name__ == "__main__":
    unittest.main()
