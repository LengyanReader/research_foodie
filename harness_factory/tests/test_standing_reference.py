"""Guard: the standing-reference convention must exist in the entry, the root
READMEs, and every emitted AGENTS.md.

A user should be able to open a conversation by pointing at this directory once,
and have the factory stay active for the whole conversation (SKILL.md documents
it; the emitted AGENTS.md carries it into the target project).
"""

from __future__ import annotations

import unittest
from pathlib import Path

from harness_factory.assemble import build_files
from harness_factory.classify import classify
from harness_factory.derive import derive
from harness_factory.spec import TaskSpec

HARNESS = Path(__file__).resolve().parent.parent  # .../harness_factory
ROOT = HARNESS.parent  # repo root

# Markers that must be present for the convention to be usable/revocable.
EN_MARKER = "STANDING REFERENCE"
EN_REVOKE = "stop using harness_factory"
ZH_MARKER = "常驻引用"
ZH_REVOKE = "停止使用 harness_factory"


class EntryDocTest(unittest.TestCase):
    def test_skill_md_documents_standing_reference(self):
        text = (HARNESS / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(EN_MARKER, text)
        self.assertIn(EN_REVOKE, text)

    def test_root_readmes_document_standing_reference(self):
        en = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(EN_MARKER, en)
        self.assertIn(EN_REVOKE, en)
        zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn(ZH_MARKER, zh)
        self.assertIn(ZH_REVOKE, zh)


class EmittedHarnessTest(unittest.TestCase):
    def test_agents_md_carries_standing_reference(self):
        task = TaskSpec(text="set up an agent workflow for a small tool over several sessions")
        plan = derive(task, classify(task))
        files = build_files(plan)
        self.assertIn("AGENTS.md", files)
        agents = files["AGENTS.md"]
        self.assertIn(EN_MARKER, agents)
        self.assertIn(EN_REVOKE, agents)


if __name__ == "__main__":
    unittest.main()
