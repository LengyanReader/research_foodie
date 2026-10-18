"""Drift guards for the capability SSOT (``src/harness_factory/data/capabilities.json``).

The map is hand-edited when requirements change (``tasks/PLAN.md`` §"Requirement
→ harness mechanism"), so these tests pin its *shape*: required keys, module ids
that actually exist, and a ``when`` DSL confined to the closed feature
vocabulary. The 2026-10 frontier row (``review/frontier-2026-10.md``) is also
exercised end-to-end through ``match`` -- a capability that never discriminates
is documentation, not a mechanism.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from harness_factory.capabilities import DOC_PATH, capability_ids, match
from harness_factory.registry import data_file, module_ids
from harness_factory.spec import FEATURE_FIELDS, FeatureVector

_ROOT = Path(__file__).resolve().parents[1]
_REQUIRED = {"title_en", "title_zh", "when", "modules", "why"}
_ALLOWED_WHEN_KEYS = set(FEATURE_FIELDS) | {"min_horizon", "any"}
_BACKTICKED = re.compile(r"`([a-z][a-z0-9-]*)`")


def _caps() -> dict:
    with data_file("capabilities.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def _active(**kwargs: str) -> set[str]:
    return {c["id"] for c in match(FeatureVector(**kwargs))}


class CapabilityShapeTest(unittest.TestCase):
    def test_entries_have_the_required_keys(self):
        caps = _caps()
        self.assertTrue(caps)
        for cid, cap in caps.items():
            self.assertEqual(_REQUIRED, set(cap), cid)
            self.assertTrue(cap["title_en"] and cap["title_zh"], cid)
            self.assertTrue(str(cap["why"]).strip(), cid)

    def test_ids_are_kebab_case(self):
        for cid in _caps():
            self.assertRegex(cid, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_modules_exist(self):
        known = set(module_ids())
        for cid, cap in _caps().items():
            self.assertTrue(cap["modules"], cid)
            for module in cap["modules"]:
                self.assertIn(module, known, f"{cid} -> {module}")

    def test_when_dsl_uses_only_known_keys(self):
        def walk(cond: dict, cid: str) -> None:
            for key, value in cond.items():
                self.assertIn(key, _ALLOWED_WHEN_KEYS, f"{cid}.{key}")
                if key == "any":
                    self.assertIsInstance(value, list, cid)
                    self.assertTrue(value, cid)
                    for sub in value:
                        self.assertIsInstance(sub, dict, cid)
                        walk(sub, cid)

        for cid, cap in _caps().items():
            self.assertIsInstance(cap["when"], dict, cid)
            walk(cap["when"], cid)

    def test_overview_doc_lists_every_capability(self):
        doc = DOC_PATH.read_text(encoding="utf-8")
        self.assertIn(f"**{len(capability_ids())} capabilities", doc)
        for cid in capability_ids():
            self.assertIn(f"`{cid}`", doc)

    def test_router_only_cites_real_capabilities(self):
        text = (_ROOT / "reference" / "capability-router.md").read_text(encoding="utf-8")
        cited: set[str] = set()
        for line in text.splitlines():
            if not line.startswith("|"):
                continue
            cells = line.split("|")
            if len(cells) > 2:  # column 2 = capability ids
                cited.update(_BACKTICKED.findall(cells[2]))
        self.assertTrue(cited, "router table not parsed")
        self.assertEqual(set(), cited - set(capability_ids()), "unknown capability in router")


class FrontierCapabilityTest(unittest.TestCase):
    """`match` must fire each new capability on its trigger, and nowhere else."""

    def test_context_budget_on_whenever_the_window_is_used(self):
        self.assertIn("context-budget-policy", _active())
        self.assertNotIn(
            "context-budget-policy", _active(horizon="one_shot", tool_surface="none")
        )

    def test_untrusted_content_needs_an_untrusted_channel(self):
        self.assertNotIn("untrusted-content-discipline", _active())
        self.assertIn("untrusted-content-discipline", _active(tool_surface="external"))
        self.assertIn("untrusted-content-discipline", _active(grounding="required"))
        self.assertIn("untrusted-content-discipline", _active(artifact="document"))

    def test_durable_execution_only_for_multi_session_and_up(self):
        self.assertNotIn("durable-execution", _active())
        self.assertIn("durable-execution", _active(horizon="multi_session"))
        self.assertIn("durable-execution", _active(horizon="long_running"))

    def test_cost_caps_for_external_or_long_runs(self):
        self.assertNotIn("cost-budget-caps", _active())
        self.assertIn("cost-budget-caps", _active(tool_surface="external"))
        self.assertIn("cost-budget-caps", _active(horizon="multi_session"))

    def test_eval_driven_development_for_high_verifiability(self):
        self.assertNotIn("eval-driven-development", _active())
        self.assertIn("eval-driven-development", _active(verifiability="high"))


class WorkflowPatternCapabilityTest(unittest.TestCase):
    """Loop & graph engineering must fire only where the topology exists."""

    def test_loop_discipline_for_agentic_write_loops(self):
        self.assertIn("loop-discipline", _active())  # default surface is read_write
        self.assertIn("loop-discipline", _active(horizon="multi_session"))
        self.assertNotIn(
            "loop-discipline", _active(horizon="one_shot", tool_surface="none")
        )

    def test_graph_orchestration_needs_branching_or_workers(self):
        self.assertNotIn("graph-orchestration", _active())  # solo, session-long
        self.assertIn("graph-orchestration", _active(collaboration="multi_agent"))
        self.assertIn("graph-orchestration", _active(horizon="multi_session"))

    def test_loop_and_graph_are_distinct(self):
        self.assertIn("loop-discipline", _active(collaboration="multi_agent"))
        self.assertNotIn("graph-orchestration", _active(horizon="session", tool_surface="read_write"))


class DisciplineCapabilityTest(unittest.TestCase):
    """The three evidence instruments fire only for the fields whose claims need them."""

    def test_formal_verification_for_formal_claims(self):
        self.assertNotIn("formal-verification", _active())
        self.assertIn("formal-verification", _active(domain="logic"))
        self.assertIn("formal-verification", _active(domain="mathematics"))
        self.assertIn("formal-verification", _active(verifiability="high", artifact="code"))

    def test_dimensional_analysis_for_physical_quantities(self):
        self.assertNotIn("dimensional-analysis", _active())
        self.assertIn("dimensional-analysis", _active(domain="physics"))
        self.assertIn("dimensional-analysis", _active(domain="engineering"))

    def test_empirical_measurement_for_empirical_claims(self):
        self.assertNotIn("empirical-measurement", _active())
        self.assertIn("empirical-measurement", _active(domain="cognitive-science"))
        self.assertIn("empirical-measurement", _active(domain="medicine"))
        self.assertNotIn("empirical-measurement", _active(domain="physics"))
