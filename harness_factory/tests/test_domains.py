import unittest
from pathlib import Path

from harness_factory.classify import classify
from harness_factory.registry import domains
from harness_factory.spec import ARTIFACTS, GROUNDING, TaskSpec

ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = ROOT / "domains"

FACULTIES = {
    "meta",
    "formal-sciences",
    "natural-sciences",
    "engineering",
    "health",
    "social-sciences",
    "humanities",
    "law",
    "education",
    "arts",
}


class DomainsDataTest(unittest.TestCase):
    def test_breadth(self):
        data = domains()
        self.assertGreaterEqual(len(data), 18)
        for d in ("research", "software-engineering", "physics", "medicine", "law", "arts-design"):
            self.assertIn(d, data)

    def test_each_domain_wellformed(self):
        for did, meta in domains().items():
            self.assertIn(meta.get("artifact"), ARTIFACTS, f"{did}: bad artifact")
            self.assertIn(meta.get("grounding"), GROUNDING, f"{did}: bad grounding")
            self.assertIn(meta.get("faculty"), FACULTIES, f"{did}: bad faculty")
            self.assertTrue(meta.get("title_en"), f"{did}: missing title_en")
            self.assertTrue(meta.get("name_zh"), f"{did}: missing name_zh")
            self.assertTrue(meta.get("workflow"), f"{did}: empty workflow")
            self.assertIsInstance(meta.get("signals"), list, f"{did}: signals not a list")

    def test_readme_exists_for_each_domain(self):
        for did in domains():
            if did == "general":
                continue
            self.assertTrue(
                (DOMAINS_DIR / did / "README.md").exists(), f"missing domains/{did}/README.md"
            )

    def test_signals_are_distinctive_enough(self):
        seen: dict[str, str] = {}
        for did, meta in domains().items():
            for sig in meta.get("signals", []):
                self.assertNotIn(
                    sig, seen, f"signal {sig!r} shared by {seen.get(sig)} and {did}"
                )
                seen[sig] = did


class DomainsClassifyTest(unittest.TestCase):
    def _domain(self, text: str) -> str:
        return classify(TaskSpec(text=text)).domain

    def test_representative_tasks(self):
        cases = {
            "measure the quantum particle cross-section": "physics",
            "run a clinical trial and diagnosis workflow": "medicine",
            "prove the theorem with a formal proof": "mathematics",
            "close reading of an archive in philosophy": "humanities",
            "draft a contract under this jurisdiction": "law",
            "prove the modal logic formula in this proof theory": "logic",
            "annotate the treebank and measure inter-annotator agreement": "linguistics",
            "run an fmri experiment on working memory": "cognitive-science",
            "fit a bayesian hierarchical model and report the credible interval": "statistics",
            "compute the persistent homology of this point cloud": "geometry-topology",
        }
        for text, expected in cases.items():
            self.assertEqual(self._domain(text), expected, text)

    def test_falls_back_to_general(self):
        self.assertEqual(self._domain("do the thing"), "general")

    def test_task_families_reach_a_domain(self):
        """The families a user actually types, not the textbook vocabulary."""
        cases = {
            "add type hints and tests to a legacy python package": "software-engineering",
            "debug a production incident and write the postmortem": "devops",
            "design a poster series with a distinct visual identity": "arts-design",
            "write a short story in the style of Borges": "writing",
            "build an online course with exercises": "education",
            "design a pcb for a low-power sensor": "engineering",
            "把这批访谈整理成一份研究报告，注明来源": "general",  # artefact/sources still resolve
        }
        for text, expected in cases.items():
            self.assertEqual(self._domain(text), expected, text)

    def test_short_signals_do_not_fire_inside_longer_words(self):
        # "ci" inside "exercises" once made a course-design task devops;
        # "art" inside "partial" made prose arts-design.
        self.assertNotEqual(self._domain("build an online course with exercises"), "devops")
        self.assertNotEqual(self._domain("summarise the partial results in this article"), "arts-design")

    def test_explicit_model_choice_reaches_model_selection(self):
        # Generic neighbours carry "model"/"模型"/"eval"/"评测" and outvote the
        # selection domain's exact phrases by count; the cue is what makes the
        # domain reachable from the way people actually ask (P19).
        self.assertEqual(
            self._domain("帮我在 GPT 和 Claude 之间选一个模型，做一个可复现的适配性评测"),
            "model-selection",
        )
        self.assertEqual(
            self._domain("which model should we use for this classification task?"),
            "model-selection",
        )

    def test_model_comparison_alone_is_not_a_selection_task(self):
        # "模型对比" is also how an ablation or a literature review is phrased;
        # treating it as selection intent would steal those tasks.
        self.assertNotEqual(self._domain("写一篇模型对比的文献综述，注明来源"), "model-selection")


if __name__ == "__main__":
    unittest.main()
