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

    def test_readmes_carry_the_usage_map(self):
        """'用法' lives in the READMEs: they must name the reference docs that turn a
        situation into a practice, plus the revocation phrase — so usage is findable
        without the CLI (and cannot silently lose a doc)."""
        refs = (
            "reference/capability-router.md",
            "reference/evidence-instruments.md",
            "reference/methodology-map.md",
            "reference/outlet-map.md",
            "reference/cross-language.md",
        )
        for path, revoke in (
            (ROOT / "README.md", EN_REVOKE),
            (ROOT / "README.zh-CN.md", ZH_REVOKE),
        ):
            text = path.read_text(encoding="utf-8")
            for ref in refs:
                self.assertIn(ref, text, f"{path.name} does not link {ref}")
            self.assertIn(revoke, text)

    def test_no_doc_still_quotes_the_old_config(self):
        """Every copy of the 'how to reference' text must be the standing version."""
        old = ("把本仓库当 skill 使用", "Treat this repository as a skill")
        skip = {"PROGRESS.md", "ASSESSMENT.md", "CHANGELOG.md"}
        offenders = []
        docs = [p for p in HARNESS.rglob("*.md") if p.name not in skip and "_archive" not in p.parts]
        docs += [ROOT / "README.md", ROOT / "README.zh-CN.md", ROOT / "AGENTS.md"]
        for path in docs:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if any(s in text for s in old):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], f"old config still quoted in: {offenders}")


class QuickStartFidelityTest(unittest.TestCase):
    """The *compressed* paste block must keep the four load-bearing units.

    P12's M4.10 worked example found that short renderings had dropped the
    *declare-what-you-used* duty and the floor invariants (M0.4 / M0.1-M0.2 /
    irreversible acts) - and then missed the READMEs, which are the copies users
    actually paste. This gate exists because that pass was scoped to "the
    guides": every copy of the compressed form must carry all four units, must
    name paths that resolve from the *target project's* root (``harness_factory/...``),
    and must name the check command concretely.

    Each assertion is scoped to the block itself (``①`` .. ``②``, or the AGENTS.md
    blockquote) - the surrounding docs legitimately say ``reference/…`` because a
    reader already inside the factory resolves it there.
    """

    BLOCKS = {
        ROOT / "README.md": ("①", "②"),
        ROOT / "README.zh-CN.md": ("①", "②"),
        ROOT / "AGENTS.md": ("> 「**常驻引用", "」"),
        HARNESS / "GUIDE.md": ("①", "②"),
        HARNESS / "introduction.md": ("①", "②"),
    }

    def _block(self, path: Path) -> str:
        start, end = self.BLOCKS[path]
        text = path.read_text(encoding="utf-8")
        i = text.index(start)
        return text[i : text.index(end, i + len(start))]

    def test_every_quick_start_carries_the_four_units(self):
        for path in self.BLOCKS:
            block = self._block(path)
            name = path.as_posix()
            self.assertIn("harness_factory/reference/capability-router.md", block, name)
            self.assertIn("用了就声明", block, name)  # unit 4: capability + file
            self.assertIn("不编造任务内容", block, name)  # unit 8: M0.4
            self.assertIn("不可逆动作", block, name)  # unit 8: the human gate
            self.assertIn("停止使用 harness_factory", block, name)  # unit 5: revoke

    def test_every_quick_start_names_a_runnable_check(self):
        for path in self.BLOCKS:
            self.assertIn("harness check --dir", self._block(path), path.as_posix())

    def test_no_quick_start_reintroduces_the_fused_clause(self):
        """「只提案、不编造任务内容」 fused two units and read as *produce nothing*."""
        for path in self.BLOCKS:
            self.assertNotIn("只提案、不编造", self._block(path), path.as_posix())

    def test_no_quick_start_uses_factory_relative_paths(self):
        """A block pasted into a target project cannot resolve ``reference/...``."""
        for path in self.BLOCKS:
            self.assertNotIn(
                "按 `reference/capability-router.md`", self._block(path), path.as_posix()
            )

    def test_the_named_paths_exist(self):
        for rel in (
            "harness_factory/SKILL.md",
            "harness_factory/reference/capability-router.md",
            "harness_factory/reference/requirement-refinement.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)


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
