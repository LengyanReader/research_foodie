"""Drift guard for the generated whole-factory map (``HARNESS-MAP.md``).

The map is rendered from the JSON catalogs, the CLI parser, the skill index and
the template directory -- so it can only be wrong when it is *stale*. This
mirrors ``CapabilitiesDocTest``: regenerate, or the test names the command.
"""

from __future__ import annotations

import unittest

from harness_factory import harness_map
from harness_factory.capabilities import capability_ids
from harness_factory.registry import module_ids


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


if __name__ == "__main__":
    unittest.main()
