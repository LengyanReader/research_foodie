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
from harness_factory.registry import data_file, domains, module_ids
from harness_factory.spec import FEATURE_CHOICES, FEATURE_FIELDS, HORIZONS, FeatureVector

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


def _router_capabilities() -> set[str]:
    text = (_ROOT / "reference" / "capability-router.md").read_text(encoding="utf-8")
    cited: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = line.split("|")
        if len(cells) > 2:  # column 2 = capability ids
            cited.update(_BACKTICKED.findall(cells[2]))
    return cited


def _branches(when: dict) -> list[dict]:
    """One conjunctive condition per satisfiable branch of ``when``."""
    branches = when.get("any")
    if not branches:
        return [when]
    rest = {k: v for k, v in when.items() if k != "any"}
    return [dict(b, **rest) for b in branches] if rest else [dict(b) for b in branches]


class CatalogReachabilityTest(unittest.TestCase):
    """No capability may be silently dead, and none may be unreachable.

    The catalogue is data, so a typo in a ``when`` value -- or a domain that does
    not exist -- fails *open*: nothing raises, the requirement simply never
    applies, and the review that added it still reads as done. These guards are
    data-driven on purpose: they name no capability, so tomorrow's entries are
    covered without editing the test.
    """

    def test_condition_values_are_declared(self):
        for cid, cap in _caps().items():
            for cond in _branches(cap["when"]):
                for key, value in cond.items():
                    values = value if isinstance(value, list) else [value]
                    if key == "min_horizon":
                        self.assertIn(value, HORIZONS, cid)
                    elif key == "domain":
                        for v in values:
                            self.assertIn(v, domains(), f"{cid}: unknown domain {v!r}")
                    else:
                        for v in values:
                            self.assertIn(v, FEATURE_CHOICES[key], f"{cid}.{key}={v!r}")

    def test_every_capability_fires_on_some_vector(self):
        for cid, cap in _caps().items():
            fired = False
            for cond in _branches(cap["when"]):
                fv = FeatureVector()
                for key, value in cond.items():
                    if key == "min_horizon":
                        fv.horizon = value
                    else:
                        setattr(fv, key, value[0] if isinstance(value, list) else value)
                self.assertEqual([], fv.validate(), cid)
                if cid in {c["id"] for c in match(fv)}:
                    fired = True
                    break
            self.assertTrue(fired, f"{cid}: no vector satisfies its `when` clause")

    def test_every_capability_is_reachable_from_the_router_doc(self):
        missing = set(capability_ids()) - _router_capabilities()
        self.assertEqual(missing, set(), f"capabilities absent from the router: {missing}")


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


class TriggerCoverageTest(unittest.TestCase):
    """P12: every capability left unguarded by the first `harness cycle audit`.

    The audit's *guard* axis asks a plain question - does any test name this
    capability? - because the failure it stands for is "the capability never
    fires and nobody notices". These ten were the answer to that worklist; each
    test pins the declared trigger *and* the quiet vector it must not fire on,
    so a later edit to `when` cannot widen a capability silently.
    """

    # A deliberately quiet task: only the undiscriminating floor fires here.
    QUIET = dict(
        horizon="one_shot",
        verifiability="low",
        stakes="low",
        grounding="off",
        artifact="code",
        tool_surface="none",
        collaboration="solo",
        domain="general",
    )

    def test_ambition_elevation_fires_from_a_single_session_up(self):
        self.assertNotIn("ambition-elevation", _active(**self.QUIET))
        self.assertIn("ambition-elevation", _active(horizon="session"))

    def test_bidirectional_capability_flow_is_always_available(self):
        # declared with an empty `when`: the flow applies to the work itself
        self.assertIn("bidirectional-capability-flow", _active(**self.QUIET))

    def test_cross_field_crew_needs_workers_or_a_long_run(self):
        self.assertNotIn("cross-field-crew", _active(**self.QUIET))
        self.assertIn("cross-field-crew", _active(collaboration="multi_agent"))
        self.assertIn("cross-field-crew", _active(horizon="long_running"))

    def test_expert_instruments_fire_when_claims_are_checkable_or_long(self):
        self.assertNotIn("expert-instruments", _active(**self.QUIET))
        self.assertIn("expert-instruments", _active(verifiability="high"))
        self.assertIn("expert-instruments", _active(horizon="multi_session"))

    def test_frontier_standard_needs_the_excellence_domain_or_a_high_bar(self):
        self.assertNotIn("frontier-standard", _active(**{**self.QUIET, "verifiability": "high"}))
        self.assertIn("frontier-standard", _active(domain="excellence"))
        self.assertIn(
            "frontier-standard", _active(verifiability="high", horizon="multi_session")
        )

    def test_reproducible_experiments_only_for_data_science_and_research(self):
        self.assertNotIn("reproducible-experiments", _active(verifiability="high"))
        self.assertNotIn("reproducible-experiments", _active(domain="data-science"))
        self.assertIn(
            "reproducible-experiments", _active(domain="data-science", verifiability="high")
        )
        self.assertIn("reproducible-experiments", _active(domain="research", verifiability="high"))
        # statistics keeps its own instrument instead
        self.assertNotIn(
            "reproducible-experiments", _active(domain="statistics", verifiability="high")
        )

    def test_resumable_memory_from_a_single_session_up(self):
        self.assertNotIn("resumable-memory", _active(**self.QUIET))
        self.assertIn("resumable-memory", _active(horizon="session"))

    def test_self_improving_loop_only_across_sessions(self):
        self.assertNotIn("self-improving-loop", _active(horizon="session"))
        self.assertIn("self-improving-loop", _active(horizon="multi_session"))

    def test_tool_use_whenever_a_tool_surface_is_open(self):
        self.assertNotIn("tool-use", _active(**self.QUIET))
        for surface in ("read", "read_write", "external"):
            with self.subTest(tool_surface=surface):
                self.assertIn("tool-use", _active(tool_surface=surface))

    def test_traceable_sources_when_grounding_matters_or_docs_are_produced(self):
        self.assertNotIn("traceable-sources", _active(**self.QUIET))
        self.assertIn("traceable-sources", _active(grounding="required"))
        for artifact in ("document", "dataset", "knowledge_base"):
            with self.subTest(artifact=artifact):
                self.assertIn("traceable-sources", _active(artifact=artifact))


class KnowledgeEngineeringCapabilityTest(unittest.TestCase):
    """P14: a knowledge base is a different *artifact*, and each of these fires on it.

    The four clauses behind them are M3.14 and M4.11-M4.13; the case that produced
    them is `review/knowledge-and-dh-crosswalk-2026-10.md`. Each test pins both the
    trigger it must fire on and the quiet vector it must stay off, so a later edit
    cannot widen it into the general floor.
    """

    QUIET = TriggerCoverageTest.QUIET

    def test_ontology_as_contract_fires_on_a_knowledge_base(self):
        self.assertNotIn("ontology-as-contract", _active(**self.QUIET))
        self.assertIn(
            "ontology-as-contract", _active(**{**self.QUIET, "artifact": "knowledge_base"})
        )
        self.assertIn("ontology-as-contract", _active(domain="knowledge-management"))
        self.assertIn("ontology-as-contract", _active(domain="digital-humanities"))

    def test_entity_resolution_fires_where_records_may_denote_one_entity(self):
        self.assertNotIn("entity-resolution", _active(**self.QUIET))
        self.assertIn(
            "entity-resolution", _active(**{**self.QUIET, "artifact": "knowledge_base"})
        )
        self.assertIn("entity-resolution", _active(domain="digital-humanities"))
        # the interpretive humanities domain counts too: prosopography is close reading
        self.assertIn("entity-resolution", _active(domain="humanities"))

    def test_evidence_bounded_generation_is_about_answers_over_a_knowledge_base(self):
        self.assertNotIn("evidence-bounded-generation", _active(**self.QUIET))
        self.assertIn(
            "evidence-bounded-generation", _active(**{**self.QUIET, "artifact": "knowledge_base"})
        )
        self.assertIn("evidence-bounded-generation", _active(domain="knowledge-management"))
        # grounding=required is enough: a research-domain answer *over a corpus* needs the
        # same pointer gate as a knowledge base (P17.3: PaperQA2's shape did not fire it)
        self.assertIn("evidence-bounded-generation", _active(grounding="required"))
        # ...but a preference is not a contract
        self.assertNotIn("evidence-bounded-generation", _active(grounding="preferred"))

    def test_schema_evolution_fires_where_a_schema_outlives_the_round(self):
        self.assertNotIn("schema-evolution", _active(**self.QUIET))
        self.assertIn(
            "schema-evolution", _active(**{**self.QUIET, "artifact": "knowledge_base"})
        )
        self.assertIn("schema-evolution", _active(domain="digital-humanities"))
        self.assertIn("schema-evolution", _active(domain="knowledge-management"))


class ReaderAndSelfModelCapabilityTest(unittest.TestCase):
    """P15: the reader gate and the self-model.

    Two clauses carry this round: **M4.14** (write for the reader) and **M5.11**
    (know your own edges). Each test pins the trigger it must fire on and the
    quiet vector it must stay off, so neither can widen into the general floor —
    a prose gate that fires on every task would be ignored, and a self-model that
    fires within a single session would be a step, not a round.
    """

    QUIET = TriggerCoverageTest.QUIET

    def test_prose_polish_fires_on_a_document_and_not_on_code(self):
        self.assertNotIn("prose-polish", _active(**self.QUIET))
        self.assertIn("prose-polish", _active(**{**self.QUIET, "artifact": "document"}))
        # a code artifact is not polished by this gate
        self.assertNotIn("prose-polish", _active(artifact="code"))

    def test_prose_polish_is_not_a_verification_gate(self):
        # high verifiability must not be read as "the prose is therefore fine"
        self.assertNotIn("prose-polish", _active(verifiability="high"))
        # and it is not the traceability floor: sourcing alone does not fire it
        self.assertNotIn("prose-polish", _active(grounding="required"))

    def test_gap_seeking_fires_across_sessions_only(self):
        self.assertNotIn("gap-seeking", _active(**self.QUIET))
        self.assertNotIn("gap-seeking", _active(horizon="session"))
        self.assertIn("gap-seeking", _active(horizon="multi_session"))

    def test_gap_seeking_sits_beside_the_evolution_loop(self):
        # it is a companion of self-improving-loop, never a replacement for it
        self.assertIn("self-improving-loop", _active(horizon="multi_session"))
        self.assertIn("gap-seeking", _active(horizon="multi_session"))


class ExpressionAndAblationCapabilityTest(unittest.TestCase):
    """P16: choose the form, and make a module earn its place.

    **M4.15** (`expression-design`) and **M5.12** (`component-ablation`). The
    discriminator matters here: expression design must not be a second copy of
    prose-polish, so it is pinned on the artefact where prose does *not* apply
    (a dataset has a schema, a data dictionary and a chart to choose between,
    and no sentences to polish). Ablation must not fire on every long task, so
    it is pinned on the conjunction it actually needs - rounds to amortise the
    cost *and* a score to ablate against.
    """

    QUIET = TriggerCoverageTest.QUIET

    def test_expression_design_fires_on_document_and_dataset(self):
        self.assertNotIn("expression-design", _active(**self.QUIET))
        self.assertIn("expression-design", _active(artifact="document"))
        self.assertIn("expression-design", _active(artifact="dataset"))
        # code has its own conventions; this gate is about reader-facing form
        self.assertNotIn("expression-design", _active(artifact="code"))

    def test_expression_design_is_not_a_duplicate_of_prose_polish(self):
        # the discriminator: a dataset needs a form chosen, but there is no prose to polish
        self.assertIn("expression-design", _active(artifact="dataset"))
        self.assertNotIn("prose-polish", _active(artifact="dataset"))

    def test_expression_design_is_not_a_sourcing_gate(self):
        # grounding alone must not fire it: a well-sourced diagram can still be the wrong form
        self.assertNotIn("expression-design", _active(grounding="required"))

    def test_component_ablation_needs_rounds_and_a_score(self):
        self.assertNotIn("component-ablation", _active(**self.QUIET))
        # rounds without a measurable score: nothing to ablate against
        self.assertNotIn("component-ablation", _active(horizon="multi_session"))
        # a score within one session: no harness to prune
        self.assertNotIn(
            "component-ablation", _active(**{**self.QUIET, "verifiability": "high"})
        )
        self.assertIn(
            "component-ablation",
            _active(**{**self.QUIET, "horizon": "multi_session", "verifiability": "high"}),
        )

    def test_component_ablation_sits_beside_the_eval_and_evolution_gates(self):
        both = _active(**{**self.QUIET, "horizon": "multi_session", "verifiability": "high"})
        self.assertIn("eval-driven-development", both)
        self.assertIn("self-improving-loop", both)
        self.assertIn("component-ablation", both)


class MathStatsCapabilityTest(unittest.TestCase):
    """P10: statistics and certified computation fire only on their own fields."""

    def test_statistical_inference_only_for_statistics(self):
        self.assertNotIn("statistical-inference", _active())
        self.assertIn("statistical-inference", _active(domain="statistics"))
        # the empirical domains keep their own instrument, not this one
        self.assertNotIn("statistical-inference", _active(domain="data-science"))
        self.assertNotIn("statistical-inference", _active(domain="psychology"))

    def test_certified_computation_only_for_geometry_topology(self):
        self.assertNotIn("certified-computation", _active())
        self.assertIn("certified-computation", _active(domain="geometry-topology"))
        # mathematics keeps formal-verification; the clause M3.12 covers its computations
        self.assertNotIn("certified-computation", _active(domain="mathematics"))


class ModelPortfolioCapabilityTest(unittest.TestCase):
    """P19: model selection gets a capability of its own, on its own domain only.

    The gap this closes was structural: `domains/model-selection/README.md`
    documented an L0-L5 pipeline while no capability fired on the domain, so a
    selection task derived floor modules only. The trigger is deliberately the
    domain itself - a model choice is a measurement on your own hold-out, not a
    property of another artefact - and the negative cases keep it from leaking
    into neighbouring domains.
    """

    def test_model_portfolio_fires_on_model_selection(self):
        self.assertIn("model-portfolio-discipline", _active(domain="model-selection"))

    def test_model_portfolio_does_not_fire_by_default(self):
        self.assertNotIn("model-portfolio-discipline", _active())
        self.assertNotIn("model-portfolio-discipline", _active(domain="data-science"))
        self.assertNotIn("model-portfolio-discipline", _active(domain="software-engineering"))
