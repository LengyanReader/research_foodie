"""Structural integrity guards for shipped docs and emitted harness files.

Motivated by a real defect: a previous session's raw assistant/tool-call markup
(DeepSeek-style ``<|DSML| …>`` blocks plus scratchpad notes) was accidentally
written into ``GUIDE.md``, and an unbalanced code fence in the emitted
``AGENTS.md`` swallowed the rest of the document.  Content-level greps for a few
known strings did NOT catch either.  These tests check *structure* instead.
"""

from __future__ import annotations

import json
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


class P20ClauseAnchorTest(unittest.TestCase):
    """P20 landed one clause (M3.16) and four data outlets; keep their objects.

    Content-presence guards, not wording guards: the prose may be edited as
    long as the clause still names the disclosure card, both valid protocols
    and the *incomplete* fallback, and the AST10 / MCP / METR pointers stay
    where the router and the audit can find them.
    """

    def test_disclosure_clause_names_the_card_and_both_protocols(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        self.assertIsNotNone(text)
        self.assertIn("M3.16", text)
        anchor = "A comparison discloses its harness (M3.16)"
        self.assertIn(anchor, text, "M3.16 clause title missing")
        section = text.split(anchor, 1)[1][:2600]
        for token in ("ETCSOVG", "locked-harness", "factorial", "variance", "incomplete"):
            self.assertIn(token, section, f"{token!r} missing from M3.16")

    def test_disclosure_clause_has_checklist_line_and_antipattern(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        self.assertIn("(M3.16).", text.split("## Checklist")[1], "no M3.16 checklist line")
        self.assertIn("Unnamed-harness comparison", text, "M3.16 anti-pattern missing")

    def test_m316_has_source_row(self):
        text = _read(HARNESS / "sources/source-map.md")
        self.assertIsNotNone(text)
        self.assertIn("| M3.16 ", text, "M3.16 has no source-map row")

    def test_group_W_refs_and_scan_renumbering(self):
        text = _read(HARNESS / "review/references.md")
        self.assertIsNotNone(text)
        self.assertIn("## W.", text, "group W missing")
        for ref in ("R243", "R244", "R245", "R251"):
            self.assertIn(ref, text, f"{ref} missing from references.md")
        scan = _read(HARNESS / "review/harness-landscape-scan-2026-10.md")
        self.assertIsNotNone(scan)
        self.assertIn("applied as round P20", scan, "scan doc not marked applied")

    def test_ast10_mcp_and_metr_pointers_landed_in_data(self):
        levers = _read(HARNESS / "src/harness_factory/data/levers.json")
        self.assertIsNotNone(levers)
        self.assertIn("AST10", levers, "security lever lost its AST10 pointer")
        caps = _read(HARNESS / "src/harness_factory/data/capabilities.json")
        self.assertIsNotNone(caps)
        self.assertIn("R245", caps, "capability provenance lost the AST10 citation")
        self.assertIn("tasks/get", caps, "durable-execution lost the MCP Tasks pointer")
        self.assertIn("R249", caps, "long-horizon-autonomy-control lost the METR refresh")


class CountDriftGuardTest(unittest.TestCase):
    """Hand-maintained counts in the entry docs must match the SSOT and the suite.

    A count copied by hand decays the moment a round lands (A.3 #6): the
    workspace AGENTS.md once claimed 27 domains / 242 tests while the SSOT
    carried 31 domains and the suite ran 284, and its bare unittest command
    fails without the src path.  These guards compare the written numbers
    against data/domains.json and the discovered test suite, so drift fails
    CI instead of misleading the next agent.
    """

    _DOMAIN_RE = re.compile(r"(\d+)\s*学科(?:门类)?\s*\+\s*general")
    _TEST_RE = re.compile(r"当前 \*\*(\d+)\*\* 用例")

    @staticmethod
    def _domains() -> dict:
        return json.loads(
            (HARNESS / "src/harness_factory/data/domains.json").read_text(encoding="utf-8")
        )

    def test_agents_md_domain_count_matches_ssot(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        m = self._DOMAIN_RE.search(text)
        self.assertIsNotNone(m, "AGENTS.md lost its domain-count line")
        expected = len(self._domains()) - 1  # minus the general fallback
        self.assertEqual(
            int(m.group(1)), expected,
            f"AGENTS.md domain count stale: {m.group(1)} vs SSOT {expected}",
        )

    def test_readme_domain_counts_match_ssot(self):
        expected = len(self._domains()) - 1
        for name in ("README.md", "README.zh-CN.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            m = self._DOMAIN_RE.search(text)
            self.assertIsNotNone(m, f"{name} lost its domain-count line")
            self.assertEqual(
                int(m.group(1)), expected,
                f"{name} domain count stale: {m.group(1)} vs SSOT {expected}",
            )

    def test_readme_trees_list_every_domain(self):
        domain_ids = set(self._domains()) - {"general"}
        for name in ("README.md", "README.zh-CN.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            trees = [b for b in _FENCE.findall(text) if "HARNESS-MAP" in b and "├── domains/" in b]
            self.assertEqual(len(trees), 1, f"{name}: expected exactly one layout tree")
            missing = sorted(d for d in domain_ids if f"{d}/" not in trees[0])
            self.assertEqual(missing, [], f"{name} layout tree missing: {missing}")

    def test_agents_md_test_count_matches_suite(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        m = self._TEST_RE.search(text)
        self.assertIsNotNone(m, "AGENTS.md lost its test-count claim")
        actual = unittest.defaultTestLoader.discover(str(HARNESS / "tests")).countTestCases()
        self.assertEqual(
            int(m.group(1)), actual,
            f"AGENTS.md test count stale: {m.group(1)} vs suite {actual}",
        )

    def test_agents_md_gate_command_names_pythonpath(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        line = next(l for l in text.splitlines() if "Test gate" in l)
        self.assertIn(
            "PYTHONPATH=src", line,
            "the bare unittest command fails without the src path (CI sets it)",
        )


class P26ClauseAnchorTest(unittest.TestCase):
    """The four clauses P26 landed must stay anchored: each names its mechanism
    in its own module and keeps its source-map row (content presence, not wording)."""

    def test_m6_clauses_are_anchored(self):
        text = _read(HARNESS / "core/07-tools-and-skills.md")
        self.assertIsNotNone(text)
        for token in ("M6.10", "M6.11", "progressive", "concrete argument"):
            self.assertIn(token, text, f"{token!r} missing from the M6 module")

    def test_m7_clause_is_anchored(self):
        text = _read(HARNESS / "core/08-change-governance.md")
        self.assertIsNotNone(text)
        self.assertIn("M7.10", text)
        self.assertIn("rollback", text)

    def test_m8_clause_is_anchored(self):
        text = _read(HARNESS / "core/09-collaboration-and-sessions.md")
        self.assertIsNotNone(text)
        self.assertIn("M8.11", text)
        self.assertIn("artifact", text)

    def test_new_clauses_have_source_rows(self):
        text = _read(HARNESS / "sources/source-map.md")
        self.assertIsNotNone(text)
        for clause in ("M6.10", "M6.11", "M7.10", "M8.11"):
            self.assertIn(f"| {clause} ", text, f"{clause} has no source-map row")


if __name__ == "__main__":
    unittest.main()
