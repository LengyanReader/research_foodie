"""Structural integrity guards for shipped docs and emitted harness files.

Motivated by a real defect: a previous session's raw assistant/tool-call markup
(DeepSeek-style ``<|DSML| …>`` blocks plus scratchpad notes) was accidentally
written into ``GUIDE.md``, and an unbalanced code fence in the emitted
``AGENTS.md`` swallowed the rest of the document.  Content-level greps for a few
known strings did NOT catch either.  These tests check *structure* instead.
"""

from __future__ import annotations

import re
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

_FENCE = re.compile(r"```.*?```", re.S)
_LINK = re.compile(r"\]\(([^)\s]+)\)")


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


class DocLinkIntegrityTest(unittest.TestCase):
    """Every relative markdown link in a shipped doc must resolve, so a pointer an
    agent reads actually leads to a file (a dead pointer wastes a capability)."""

    def test_relative_links_resolve(self):
        offenders = []
        for path in _shipped_files():
            text = _read(path)
            if text is None:
                continue
            body = _FENCE.sub("", text)
            for raw in _LINK.findall(body):
                if raw.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = raw.split("#", 1)[0]
                # Skip placeholders and runtime-generated paths (absent in a fresh checkout).
                if not target or target.startswith(("<", "updates/", ".harness/")):
                    continue
                candidates = [path.parent / target, HARNESS / target, ROOT / target]
                if not any(c.exists() for c in candidates):
                    offenders.append(f"{path.relative_to(ROOT)} -> {raw}")
        self.assertEqual(offenders, [], f"unresolved relative links: {offenders}")


class P17ClauseAnchorTest(unittest.TestCase):
    """The two clauses P17 landed must stay anchored to their evidence and their test.

    A clause without its source row is a rule with no provenance; one whose failure
    modes have been quietly dropped from the text is a rule that only remembers half
    of what the cases showed. These guards are deliberately about *content presence*,
    not wording, so the prose can be edited without fighting the test.
    """

    def test_stage_funnel_clause_names_its_three_stages(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        self.assertIsNotNone(text)
        self.assertIn("M3.15", text)
        section = text.split("M3.15", 1)[1][:1500]
        for stage in ("evidence found", "kept", "used correctly"):
            self.assertIn(stage, section)

    def test_pointer_clause_names_all_three_failure_modes(self):
        text = _read(HARNESS / "core/05-provenance-and-integrity.md")
        self.assertIsNotNone(text)
        self.assertIn("M4.16", text)
        section = text.split("M4.16", 1)[1][:2600]
        for mode in ("Dangling", "Stale", "Unsupported"):
            self.assertIn(mode, section, f"failure mode {mode} missing from M4.16")

    def test_case_review_keeps_one_row_per_case(self):
        text = _read(HARNESS / "review/domain-harness-cases-2026-10.md")
        self.assertIsNotNone(text)
        table = text.split("## 6. Cross table", 1)[1].split("## 7.", 1)[0]
        self.assertIn("C1 schema", table)
        rows = [
            line
            for line in table.splitlines()
            if line.startswith("| ") and "Case |" not in line and not line.startswith("|---")
        ]
        self.assertEqual(len(rows), 4, f"cross table lost a case: {rows}")
        for ref in ("[R136]", "[R148]", "[R128]", "[R238]"):
            self.assertIn(ref, table, f"{ref} missing from the cross table")


class P19ClauseAnchorTest(unittest.TestCase):
    """The three clauses P19 landed must keep their evidence and their object.

    These are content-presence guards, not wording guards: the prose can be
    edited freely as long as each clause still names the mechanism it exists
    for and still appears in the source map.  Dropping one of those silently is
    how a rule decays into a slogan.
    """

    def test_append_only_compaction_names_the_provider_constraint(self):
        text = _read(HARNESS / "core/02-context-engineering.md")
        self.assertIsNotNone(text)
        self.assertIn("M1.11", text)
        section = text.split("M1.11", 1)[1][:2200]
        for token in ("preserved thinking", "forward-only", "addition"):
            self.assertIn(token, section, f"{token!r} missing from M1.11")

    def test_effort_clause_names_the_gate_and_the_comparison_trap(self):
        text = _read(HARNESS / "core/03-long-running-agents.md")
        self.assertIsNotNone(text)
        self.assertIn("M2.13", text)
        section = text.split("M2.13", 1)[1][:2600]
        for token in ("per stage", "gate", "xhigh", "cache"):
            self.assertIn(token, section, f"{token!r} missing from M2.13")

    def test_serving_model_clause_names_requested_and_served(self):
        text = _read(HARNESS / "core/05-provenance-and-integrity.md")
        self.assertIsNotNone(text)
        self.assertIn("M4.17", text)
        section = text.split("M4.17", 1)[1][:2600]
        for token in ("requested", "served", "substitution", "not a measurement"):
            self.assertIn(token, section, f"{token!r} missing from M4.17")

    def test_new_clauses_have_source_rows(self):
        text = _read(HARNESS / "sources/source-map.md")
        self.assertIsNotNone(text)
        for clause in ("M1.11", "M2.13", "M4.17"):
            self.assertIn(f"| {clause} ", text, f"{clause} has no source-map row")


if __name__ == "__main__":
    unittest.main()
