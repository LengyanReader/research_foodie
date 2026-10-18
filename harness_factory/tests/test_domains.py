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
        }
        for text, expected in cases.items():
            self.assertEqual(self._domain(text), expected, text)

    def test_falls_back_to_general(self):
        self.assertEqual(self._domain("do the thing"), "general")


if __name__ == "__main__":
    unittest.main()
