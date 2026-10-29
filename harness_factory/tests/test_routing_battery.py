"""The extended routing battery (P55): every domain and the key capabilities must be
reachable from the way a user actually phrases the ask, in English and Chinese.

P18 ran 32 families against the 2026-10-20 surface; since then six domains, fourteen
capabilities, the intersection mechanism (P31) and new cues (P36/P51) landed without
the battery being extended. This file is the standing regression: one or two natural
sentences per family, asserting the routed domain AND the key capability that makes
the family's discipline plan-visible. A miss here is a matching-rate defect."""

from __future__ import annotations

import unittest

from harness_factory.classify import classify
from harness_factory.derive import derive
from harness_factory.spec import TaskSpec

# (task, expected domain, expected capability or None)
BATTERY = [
    # research family
    ("write a literature review with citations over several weeks", "research", "traceable-sources"),
    ("深度调研智能体记忆系统，多跳引用，注明来源", "deep-research", "traceable-sources"),
    ("systematic review of agent evaluation practices with evidence synthesis", "deep-research", None),
    # knowledge family
    ("organize our team knowledge base and keep the coverage ledger current", "knowledge-management", None),
    ("构建方志人物知识图谱，做检索增强问答，注明来源", "digital-humanities", "ontology-as-contract"),
    # engineering family
    ("add type hints and tests to a legacy python package", "software-engineering", None),
    ("debug a production incident and write the postmortem", "devops", None),
    ("design a pcb for a low-power sensor", "engineering", None),
    ("which model should we use for this classification task?", "model-selection", "model-portfolio-discipline"),
    ("分析这份数据集并拟合模型，给出可复现的实验", "data-science", "reproducible-experiments"),
    # formal sciences
    ("prove the theorem with a formal proof", "mathematics", None),
    ("fit a bayesian hierarchical model and report the credible interval", "statistics", "statistical-inference"),
    ("prove the modal logic formula in this proof theory", "logic", "formal-verification"),
    ("compute the persistent homology of this point cloud", "geometry-topology", "certified-computation"),
    # natural sciences
    ("measure the quantum particle cross-section", "physics", "dimensional-analysis"),
    ("synthesize this compound and check the yield stoichiometry", "chemistry", "dimensional-analysis"),
    ("run the genomics sequencing analysis on this sample", "biology", None),
    ("analyze the climate data for this region's hydrology", "earth-environment", "dimensional-analysis"),
    # health / social
    ("run a clinical trial and diagnosis workflow", "medicine", "empirical-measurement"),
    ("model the market equilibrium with econometrics", "economics-finance", "empirical-measurement"),
    ("run an fmri experiment on working memory", "cognitive-science", "empirical-measurement"),
    ("field survey of social attitudes with sampling", "social-science", "empirical-measurement"),
    ("国际关系研究：先界定地缘政治的概念，再说明案例选择的规则并留痕", "political-science", "concept-definition"),
    # humanities
    ("cross-check the chronicle accounts of the 1120 succession and note what the sources omit", "history", "source-criticism"),
    ("从认识论角度重构这篇伦理学论文的论证，评估其前提并坦诚反例", "philosophy", "argument-reconstruction"),
    ("annotate the treebank and measure inter-annotator agreement", "linguistics", None),
    ("close reading of this novel's chapter with annotations", "reading", None),
    ("write a short story in the style of Borges", "writing", "prose-polish"),
    ("draft a contract under this jurisdiction", "law", None),
    ("design a course with learning outcomes and assessment", "education", None),
    ("design a poster series with a distinct visual identity", "arts-design", None),
    # meta / safety / ideation
    ("build the safety case for this alignment claim: state the threat model, run red-team capability evals", "ai-safety", "safety-argumentation"),
    ("draft a project plan with the research questions we should pursue", "research", "research-question-generation"),
    ("为我们的智能体记忆研究起草提案，提出值得研究的问题清单，注明来源", "general", "research-question-generation"),
    # intent edges (P36 regressions)
    ("write a literature review with citations over several weeks", "research", None),  # weeks -> multi_session, review != human_review
]


class RoutingBatteryTest(unittest.TestCase):
    """P55: the standing matching-rate regression (P18's discipline, extended)."""

    def _plan(self, text: str):
        v = classify(TaskSpec(text=text))
        return v, derive(TaskSpec(text=text), v)

    def test_every_domain_and_key_capability_is_reachable(self):
        misses = []
        for txt, dom, cap in BATTERY:
            v, plan = self._plan(txt)
            if v.domain != dom:
                misses.append(f"[domain] {txt!r}: got {v.domain}, want {dom}")
            if cap and cap not in plan.capabilities:
                misses.append(f"[capability] {txt!r}: {cap!r} not fired (domain={v.domain})")
        self.assertEqual(misses, [], "\n".join(misses))

    def test_horizon_intents(self):
        self.assertEqual(classify(TaskSpec(text="a quick one-off script")).horizon, "one_shot")
        self.assertEqual(
            classify(TaskSpec(text="write a literature review with citations over several weeks")).horizon,
            "multi_session",
        )
        self.assertEqual(classify(TaskSpec(text="a long-running continuous monitor")).horizon, "long_running")

    def test_collaboration_intents(self):
        self.assertEqual(
            classify(TaskSpec(text="review my PR before it merges")).collaboration, "human_review"
        )
        self.assertEqual(
            classify(TaskSpec(text="write a systematic review of the literature")).collaboration,
            "solo",
        )

    def test_capability_precision_on_a_coding_task(self):
        v, plan = self._plan("add unit tests to the parser")
        for cap in ("prose-polish", "source-criticism", "argument-reconstruction",
                    "research-question-generation", "ontology-as-contract"):
            self.assertNotIn(cap, plan.capabilities, f"{cap!r} leaked into a coding task")


    def test_classify_command_inspects_intent(self):
        from harness_factory import cli
        import io, contextlib, json as _json
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.main(["classify", "--task", "draft a project plan with the research questions",
                             "--json"])
        self.assertEqual(code, 0)
        payload = _json.loads(buf.getvalue())
        self.assertEqual(payload["features"]["artifact"], "plan")
        self.assertIn("research-question-generation", payload["capabilities"])


if __name__ == "__main__":
    unittest.main()
