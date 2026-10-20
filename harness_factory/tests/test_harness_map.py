"""Drift guard for the generated whole-factory map (``HARNESS-MAP.md``).

The map is rendered from the JSON catalogs, the CLI parser, the skill index and
the template directory -- so it can only be wrong when it is *stale*. This
mirrors ``CapabilitiesDocTest``: regenerate, or the test names the command.
"""

from __future__ import annotations

import re
import unittest

from harness_factory import harness_map
from harness_factory.capabilities import capability_ids, capabilities
from harness_factory.registry import module_ids, modules
from harness_factory.spec import FEATURE_FIELDS


class HarnessMapDocTest(unittest.TestCase):
    def test_generated_doc_matches_disk(self):
        self.assertEqual(
            harness_map.render_doc(),
            harness_map.DOC_PATH.read_text(encoding="utf-8"),
            "HARNESS-MAP.md is stale; run `harness map --write`",
        )

    def test_map_names_every_module_and_capability(self):
        text = harness_map.render_doc()
        for module in module_ids():
            self.assertIn(module, text)
        for cid in capability_ids():
            self.assertIn(f"`{cid}`", text)

    def test_summary_counts_are_positive(self):
        for key, value in harness_map.summary().items():
            self.assertGreater(value, 0, key)

    def test_headline_matches_the_summary(self):
        self.assertIn(f"**{harness_map.summary()['modules']} modules", harness_map.render_doc())


class ArchitectureDiagramTest(unittest.TestCase):
    def _diagram(self) -> str:
        diagram = harness_map.render_architecture()
        m = re.search(r"```mermaid\n(.*?)\n```", diagram, re.S)
        self.assertIsNotNone(m, "the architecture block must be a closed mermaid fence")
        return m.group(1)

    def test_diagram_is_a_flowchart_with_unique_node_ids(self):
        body = self._diagram()
        self.assertTrue(body.lstrip().startswith("flowchart "), body[:40])
        ids = re.findall(r"^\s*([A-Z][A-Z0-9]*)\[", body, re.M)
        self.assertGreaterEqual(len(ids), 10)
        self.assertEqual(len(ids), len(set(ids)), "duplicate node ids break the layout")

    def test_every_module_and_axis_appears_in_the_diagram(self):
        body = self._diagram()
        for mid in module_ids():
            self.assertIn(mid, body)
        with_counts = harness_map.axis_counts()
        for axis, count in with_counts.items():
            self.assertIn(axis, body)
            self.assertGreater(count, 0, f"{axis} has no capability")

    def test_diagram_is_in_the_doc_exactly_once(self):
        text = harness_map.render_doc()
        self.assertEqual(text.count("```mermaid"), 1)
        self.assertEqual(text.count("```"), 2, "one fenced block, opened and closed")


class AxisCountTest(unittest.TestCase):
    def test_gloss_covers_every_feature_axis(self):
        for table in (harness_map._AXIS_ASK_EN, harness_map._AXIS_ASK_ZH, harness_map._AXIS_ZH):
            self.assertEqual(set(table), set(FEATURE_FIELDS))

    def test_each_capability_is_counted_once_per_axis_it_uses(self):
        counts = harness_map.axis_counts()
        expected = 0
        for meta in capabilities().values():
            axes = harness_map._when_axes(meta.get("when", {}))
            expected += max(1, len(axes))
        self.assertEqual(sum(counts.values()), expected)
        self.assertEqual(counts["always"], sum(1 for m in capabilities().values() if not m["when"]))

    def test_an_unknown_axis_is_an_error_not_a_silent_drop(self):
        with self.assertRaises(ValueError):
            harness_map._when_axes({"nonsense": ["x"]})


class ModuleBoundaryTest(unittest.TestCase):
    """Every module states what it does *not* cover -- the map renders it as a column."""

    def test_every_module_has_a_bilingual_boundary(self):
        for mid, meta in modules().items():
            for key in ("excludes_en", "excludes_zh"):
                value = meta.get(key, "")
                self.assertTrue(value.strip(), f"{mid} is missing {key}")
                self.assertLessEqual(len(value), 220, f"{mid}.{key} is too long for one cell")

    def test_boundary_is_not_the_rule_restated(self):
        for mid, meta in modules().items():
            self.assertNotEqual(
                meta.get("excludes_en"), meta.get("rule_en"), f"{mid}: boundary repeats the rule"
            )


class WorkedExampleTest(unittest.TestCase):
    """The map shows real ``classify`` + ``derive`` output, not a hand-written sample."""

    def test_examples_are_derived_and_complete(self):
        examples = harness_map.worked_example()
        self.assertEqual(len(examples), 2)
        for ex in examples:
            self.assertEqual([k for k, _ in ex["features"]], list(FEATURE_FIELDS))
            self.assertTrue(ex["capabilities"])
            self.assertTrue(ex["enabled"])
            # a module is either enabled or disabled, never dropped
            self.assertEqual(
                len(ex["enabled"]) + len(ex["disabled"]), len(module_ids()), ex["label"]
            )

    def test_the_two_examples_differ_in_shape(self):
        first, second = harness_map.worked_example()
        self.assertNotEqual(first["capabilities"], second["capabilities"])

    def test_doc_shows_the_example_task_and_its_capability_count(self):
        text = harness_map.render_doc()
        for ex in harness_map.worked_example():
            self.assertIn(ex["task"], text)
            self.assertIn(f"命中能力（{len(ex['capabilities'])}）", text)


if __name__ == "__main__":
    unittest.main()
