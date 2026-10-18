"""Structural integrity guards for shipped docs and emitted harness files.

Motivated by a real defect: a previous session's raw assistant/tool-call markup
(DeepSeek-style ``<|DSML| …>`` blocks plus scratchpad notes) was accidentally
written into ``GUIDE.md``, and an unbalanced code fence in the emitted
``AGENTS.md`` swallowed the rest of the document.  Content-level greps for a few
known strings did NOT catch either.  These tests check *structure* instead.
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

SKIP_DIRS = {"_archive", ".git", "__pycache__", "updates"}
# Append-only logs may legitimately *quote* leaked text (e.g. this very repair).
LOG_FILES = {"PROGRESS.md", "CHANGELOG.md", "ASSESSMENT.md"}
# Markers that only ever appear in raw assistant output, never in shipped docs.
LEAK_MARKERS = (
    "DSML",
    "oldString",
    "newString",
    "Let me do the edits",
    "Accept interruption",
    "<|tool",
    "parameter name=",
)


def _shipped_files(include_logs: bool = True) -> list[Path]:
    files = [
        p
        for p in HARNESS.rglob("*")
        if p.is_file()
        and not (SKIP_DIRS & set(p.parts))
        and p.suffix in {".md", ".tmpl"}
        and (include_logs or p.name not in LOG_FILES)
    ]
    files += [ROOT / "README.md", ROOT / "README.zh-CN.md", ROOT / "AGENTS.md", ROOT / "CHANGELOG.md"]
    return files


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _fence_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip().startswith("```"))


class NoLeakedArtifactsTest(unittest.TestCase):
    def test_no_raw_assistant_or_tool_markup(self):
        offenders = []
        for path in _shipped_files(include_logs=False):
            text = _read(path)
            if text is None:
                continue
            for marker in LEAK_MARKERS:
                if marker in text:
                    offenders.append(f"{path.relative_to(ROOT)} :: {marker}")
        self.assertEqual(offenders, [], f"leaked assistant/tool markup: {offenders}")


class CodeFenceBalanceTest(unittest.TestCase):
    def test_shipped_docs_have_balanced_fences(self):
        offenders = []
        for path in _shipped_files():
            text = _read(path)
            if text is None:
                continue
            n = _fence_lines(text)
            if n % 2:
                offenders.append(f"{path.relative_to(ROOT)} :: {n} fence lines")
        self.assertEqual(offenders, [], f"unbalanced code fences: {offenders}")

    def test_emitted_files_have_balanced_fences(self):
        task = TaskSpec(text="long research pipeline across sessions")
        files = build_files(derive(task, classify(task)))
        offenders = {n: _fence_lines(t) for n, t in files.items() if _fence_lines(t) % 2}
        self.assertEqual(offenders, {}, f"unbalanced fences in emitted files: {offenders}")

    def test_emitted_files_have_no_unfilled_placeholders(self):
        task = TaskSpec(text="long research pipeline across sessions")
        files = build_files(derive(task, classify(task)))
        offenders = [n for n, t in files.items() if "{{" in t or "}}" in t]
        self.assertEqual(offenders, [], f"unfilled placeholders in emitted files: {offenders}")


class GuideStandingReferenceTest(unittest.TestCase):
    """GUIDE.md Example 4 must document the standing reference + revocation."""

    def test_guide_documents_standing_reference(self):
        text = (HARNESS / "GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("STANDING REFERENCE", text)
        self.assertIn("stop using harness_factory", text)


class LoadIndexWiringTest(unittest.TestCase):
    """Every skill-index entry must resolve, and the shipped entry points must
    name the new reference docs (so an L0 reader can find them without the CLI)."""

    def test_every_index_path_exists(self):
        from harness_factory import skill

        missing = [entry.path for entry in skill.index() if not (HARNESS / entry.path).exists()]
        self.assertEqual(missing, [])

    def test_entry_docs_name_cross_language(self):
        for name in ("SKILL.md", "core/05-provenance-and-integrity.md", "reference/capability-router.md"):
            text = (HARNESS / name).read_text(encoding="utf-8")
            self.assertIn("cross-language", text, f"{name} does not link the cross-language doc")


if __name__ == "__main__":
    unittest.main()
