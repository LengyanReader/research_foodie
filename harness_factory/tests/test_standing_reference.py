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
    """Every paste-ready rendering must keep the four load-bearing units *and* take a path parameter.

    P12's M4.10 worked example found that short renderings had dropped the
    *declare-what-you-used* duty and the floor invariants (M0.4 / M0.1-M0.2 /
    irreversible acts) - and then missed the READMEs, which are the copies users
    actually paste. A later user question exposed a second failure mode: the block
    assumed the factory sits at ``./harness_factory``, but a reader clones this
    repo anywhere, so its location must be a *parameter* (``<HF>``), not an
    assumption. Both gates are pinned here.

    Each assertion is scoped to the block itself (``①`` .. ``②``, the AGENTS.md
    blockquote, or a fenced ``text`` template) - the surrounding docs legitimately
    say ``reference/…``, because a reader already inside the factory resolves it there.
    """

    # (file, start marker, end marker, path-parameter marker): the five compressed copies,
    # the two full templates, and the authoritative SKILL.md block.
    BLOCKS = (
        (ROOT / "README.md", "①", "②", "<HF>"),
        (ROOT / "README.zh-CN.md", "①", "②", "<HF>"),
        (ROOT / "AGENTS.md", "> 「**常驻引用", "\n\n**Step 2 · 任务", "<HF>"),
        (HARNESS / "GUIDE.md", "①", "②", "<HF>"),
        (HARNESS / "introduction.md", "①", "②", "<HF>"),
        (ROOT / "README.md", "STANDING REFERENCE (until I revoke it)", "```", "<HF>"),
        (ROOT / "README.zh-CN.md", "常驻引用（直到我说", "```", "<HF>"),
        (HARNESS / "SKILL.md", "> **Single source of truth", "\n\n- **Durable form", "换成真实路径"),
    )
    COMPRESSED = 5  # the first five entries
    ENGLISH = (5, 7)  # the two full templates written in English, plus SKILL.md

    def _block(self, entry) -> str:
        path, start, end = entry[0], entry[1], entry[2]
        text = path.read_text(encoding="utf-8")
        i = text.index(start)
        return text[i : text.index(end, i + len(start))]

    def test_every_rendering_takes_a_path_parameter(self):
        """The factory is cloned somewhere; the block must ask for that location."""
        for entry in self.BLOCKS:
            path, marker = entry[0], entry[3]
            block = self._block(entry)
            name = path.as_posix()
            self.assertIn(marker, block, name)
            self.assertIn("harness check --dir", block, name)
            if marker == "<HF>":
                self.assertNotIn("`./harness_factory", block, name)
                self.assertNotIn("`harness_factory/SKILL.md`", block, name)

    def test_every_compressed_rendering_carries_the_four_units(self):
        for entry in self.BLOCKS[: self.COMPRESSED]:
            block = self._block(entry)
            name = entry[0].as_posix()
            self.assertIn("<HF>/reference/capability-router.md", block, name)
            self.assertIn("用了就声明", block, name)  # unit 4: capability + file
            self.assertIn("不编造任务内容", block, name)  # unit 8: M0.4
            self.assertIn("不可逆动作", block, name)  # unit 8: the human gate
            self.assertIn("停止使用 harness_factory", block, name)  # unit 5: revoke

    def test_the_english_renderings_keep_the_same_three_units(self):
        for i in self.ENGLISH:
            entry = self.BLOCKS[i]
            block = self._block(entry)
            name = entry[0].as_posix()
            self.assertIn("declare which capability", block, name)  # unit 4
            self.assertIn("Never fabricate", block, name)  # unit 8: M0.4
            self.assertIn("irreversible acts", block, name)  # unit 8: the human gate
            self.assertIn("stop using harness_factory", block, name)  # unit 5: revoke

    def test_no_compressed_rendering_reintroduces_the_fused_clause(self):
        """「只提案、不编造任务内容」 fused two units and read as *produce nothing*."""
        for entry in self.BLOCKS[: self.COMPRESSED]:
            self.assertNotIn("只提案、不编造", self._block(entry), entry[0].as_posix())

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
