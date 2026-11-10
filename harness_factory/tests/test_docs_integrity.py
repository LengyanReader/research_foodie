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


class P27SchoolsAndDomainsTest(unittest.TestCase):
    """P27 landed three domains and a school-of-thought table; keep the objects.

    Content-presence guards: the domains must exist in the SSOT with their
    rubrics, and the methodology map must keep the school rows that give the
    new fields their gate content (a school row lost is a gate gone silent)."""

    def test_new_domains_have_entries_and_rubrics(self):
        import json

        domains = json.loads(
            (HARNESS / "src/harness_factory/data/domains.json").read_text(encoding="utf-8")
        )
        rubrics = json.loads(
            (HARNESS / "src/harness_factory/data/rubrics.json").read_text(encoding="utf-8")
        )
        for domain in ("history", "philosophy", "political-science"):
            self.assertIn(domain, domains, f"{domain} missing from domains.json")
            self.assertIn(domain, rubrics, f"{domain} has no rubric")

    def test_school_rows_are_present(self):
        text = _read(HARNESS / "reference/methodology-map.md")
        self.assertIsNotNone(text)
        for token in (
            "Gadamer",
            "Husserl",
            "Popper",
            "Glaser",
            "Kahneman",
            "Brouwer",
            "四书章句集注",
            "Die Traumdeutung",
        ):
            self.assertIn(token, text, f"school row lost its anchor: {token!r}")


class P34ClauseAnchorTest(unittest.TestCase):
    """P34 landed two clauses (M3.17, sharpening M5.11's sampling-agreement aside
    into a gate obligation; M5.13, the acceptance-side twin of M5.12) from abstract-verified sources, plus the
    digest-intake outlets. Content-presence guards: the prose may be edited as
    long as each clause still names its mechanism, the unverified evidence level
    stays declared, and the registry rows (incl. the P33 backfill) hold.
    """

    def test_m317_clause_names_the_adjudication_rule(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        self.assertIsNotNone(text)
        anchor = "Agreement is not verification (M3.17)"
        self.assertIn(anchor, text, "M3.17 clause title missing")
        section = text.split(anchor, 1)[1][:2200]
        for token in ("disagreement", "consensus", "environmental evidence",
                      "requirements every rollout omitted", "[R254]", "never a vote"):
            self.assertIn(token, section, f"{token!r} missing from M3.17")

    def test_m317_checklist_line_and_antipattern(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        self.assertIn("(M3.17).", text.split("## Checklist")[1], "no M3.17 checklist line")
        self.assertIn("Selection by agreement", text, "M3.17 anti-pattern missing")

    def test_m513_clause_names_the_acceptance_gate(self):
        text = _read(HARNESS / "core/06-self-evolution.md")
        self.assertIsNotNone(text)
        anchor = "A self-edit is attributed and gated before acceptance (M5.13)"
        self.assertIn(anchor, text, "M5.13 clause title missing")
        section = text.split(anchor, 1)[1][:2600]
        for token in ("development set", "acceptance criteria", "cause",
                      "rejection bound", "[R256]", "[R252]"):
            self.assertIn(token, section, f"{token!r} missing from M5.13")

    def test_m513_checklist_lines_and_antipattern(self):
        text = _read(HARNESS / "core/06-self-evolution.md")
        checklist = text.split("## Checklist")[1].split("## Anti-patterns")[0]
        self.assertEqual(checklist.count("(M5.13)."), 2, "M5.13 should carry two checklist lines")
        self.assertIn("Ungated self-edit", text, "M5.13 anti-pattern missing")

    def test_p34_source_rows_and_reference_group(self):
        text = _read(HARNESS / "sources/source-map.md")
        self.assertIn("| M3.17 ", text, "M3.17 has no source-map row")
        self.assertIn("| M5.13 ", text, "M5.13 has no source-map row")
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("## X.", refs, "group X missing")
        for ref in ("R252", "R254", "R256", "R262"):
            self.assertIn(ref, refs, f"{ref} missing from references.md")
        bib = _read(HARNESS / "review/references.bib")
        for key in ("zhang2026veriharness", "liu2026vera", "dairai2026papers"):
            self.assertIn(key, bib, f"bib entry missing: {key}")

    def test_p34_review_doc_declares_the_evidence_level(self):
        doc = _read(HARNESS / "review/self-modifying-harnesses-2026-10.md")
        self.assertIsNotNone(doc, "P34 survey doc missing (linked from M3.17)")
        for token in ("abstract-verified", "unverified", "P34.R1", "CC BY-NC-SA"):
            self.assertIn(token, doc, f"survey doc lost its {token!r} declaration")
        self.assertIn("self-modifying-harnesses-2026-10.md",
                      _read(HARNESS / "core/04-verification-and-gates.md"))

    def test_p34_data_outlets_and_registry_rows(self):
        caps = _read(HARNESS / "src/harness_factory/data/capabilities.json")
        self.assertIn("(M3.17)", caps, "verification-gate why lost M3.17")
        self.assertIn("(M5.13)", caps, "self-improving-loop why lost M5.13")
        sources = _read(HARNESS / "src/harness_factory/data/sources.json")
        self.assertIn("dair-ai-x", sources, "digest account not tracked as media")
        cycles = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                            .read_text(encoding="utf-8"))
        by_id = {c["id"]: c for c in cycles["cycles"]}
        self.assertIn("P33", by_id, "P33 backfill missing from the registry")
        p34 = by_id.get("P34", {})
        self.assertEqual(p34.get("added", {}).get("clauses"), ["M3.17", "M5.13"])
        self.assertIn("P34.R1", {r["id"] for r in cycles["roadmap"]},
                      "full-text reread trigger not registered")


class P35ChannelTest(unittest.TestCase):
    """P35 completed the paper-discovery channels and wired them into the update
    loop. Guards: the new venue rows exist, arXiv cs.MA is a real feed, the defunct
    Papers with Code is retired in both SSOT surfaces, the survey + outlet-map gained
    the portal section, the watchlist discovery topic is present, and the registry
    records the round. Content-presence only - prose may be edited freely."""

    def test_new_paper_venues_registered(self):
        sources = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                             .read_text(encoding="utf-8"))
        venues = {e["id"]: e for e in sources["groups"]["venues"]}
        self.assertIn("hf-papers", venues, "Hugging Face Daily Papers not registered")
        self.assertIn("arxiv-cs-ma", venues, "arXiv cs.MA feed not registered")
        self.assertIn("export.arxiv.org/rss/cs.MA", venues["arxiv-cs-ma"].get("feed", ""))
        self.assertIn("api/daily_papers", venues["hf-papers"].get("api", ""))

    def test_paperswithcode_retired_in_both_surfaces(self):
        sources = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                             .read_text(encoding="utf-8"))
        pwc = next(e for e in sources["groups"]["projects"] if e["id"] == "paperswithcode")
        self.assertIsNone(pwc.get("feed"), "defunct PWC feed must not stay on the pull path")
        harnesses = json.loads((HARNESS / "src/harness_factory/data/harnesses.json")
                              .read_text(encoding="utf-8"))
        cat = next(e for e in harnesses["harnesses"] if e.get("id") == "paperswithcode")
        self.assertFalse(cat.get("verified"), "catalog PWC must be marked unverified")

    def test_watchlist_has_paper_discovery_topic(self):
        wl = json.loads((HARNESS / "src/harness_factory/data/watchlist.json")
                       .read_text(encoding="utf-8"))
        self.assertIn("scholarly-discovery", {t["id"] for t in wl["topics"]},
                      "paper-discovery topic missing from the loop's watchlist")

    def test_survey_added_portal_section_with_today_status(self):
        doc = _read(HARNESS / "review/scholarly-channels-2026-10.md")
        self.assertIsNotNone(doc)
        self.assertIn("## 8.", doc, "survey lost its AI-paper portals section")
        for token in ("Hugging Face Daily Papers", "api/daily_papers",
                      "Papers with Code", "defunct", "2026-10-27"):
            self.assertIn(token, doc, f"portal section lost {token!r}")

    def test_outlet_map_routing_section(self):
        doc = _read(HARNESS / "reference/outlet-map.md")
        self.assertIn("AI-paper discovery portals", doc, "outlet-map lost the portal section")
        for token in ("hf-papers", "arxiv-cs", "refresh --provider feed"):
            self.assertIn(token, doc, f"outlet-map portal section lost {token!r}")

    def test_registry_records_p35(self):
        cycles = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                           .read_text(encoding="utf-8"))
        p35 = next((c for c in cycles["cycles"] if c["id"] == "P35"), None)
        self.assertIsNotNone(p35, "P35 not registered")
        self.assertEqual(p35["added"]["outlets_delta"], 0, "P35 added no outlets")
        self.assertIn("P35.R1", {r["id"] for r in cycles["roadmap"]},
                      "JSON-API provider deferral not registered")


class P38RereadGuardTest(unittest.TestCase):
    """P38: the full-text reread upgraded the evidence level and resolved the ledger.

    The digest-body ledger (survey doc §4) was the P34.R1 checklist; this guard
    pins the reread's outcomes so a future edit cannot silently re-grade them:
    the survey doc carries the full-read grade, the located release pool and the
    in-kind corrections; references §X carries exactly eight upgraded entry
    markers; both landed clauses carry the promotion instead of the hedge.
    """

    def test_survey_doc_carries_grade_pool_and_corrections(self):
        doc = _read(HARNESS / "review/self-modifying-harnesses-2026-10.md")
        for token in (
            "full-read",                                    # the upgraded evidence level
            "huggingface.co/datasets/caiqizh/veriharness",  # the release pool located
            "composite score",                              # HERMES metric correction in kind
            "tolerance bound",                              # VERA threshold semantics corrected
            "$1,072.73",                                    # the $1,073 digest compression corrected
            "Sakana AI",                                    # the CMM attribution verified true
        ):
            self.assertIn(token, doc, f"reread outcome lost: {token!r}")

    def test_references_carry_exactly_eight_upgraded_markers(self):
        refs = _read(HARNESS / "review/references.md")
        self.assertEqual(
            refs.count("full-read 2026-10-28"), 8,
            "expected exactly the R252-R259 markers upgraded (R260/R261 stay abstract-level)",
        )

    def test_both_landed_clauses_carry_the_promotion(self):
        self.assertIn(
            "results verified against the HTML full text, 2026-10-28",
            _read(HARNESS / "core/04-verification-and-gates.md"),
            "M3.17 still carries the unreachable-full-text hedge",
        )
        m513 = _read(HARNESS / "core/06-self-evolution.md")
        self.assertIn(
            "read in full, 2026-10-28", m513,
            "M5.13 still carries an abstract-level hedge",
        )
        self.assertIn("tolerance bound", m513, "M5.13 lost VERA's two-bound exemplar")


class P37PoolCheckGuardTest(unittest.TestCase):
    """P37: the VeriHarness pool check is the first dogfood deliverable.

    Pins the measured numbers so a future edit cannot re-inflate the abstract's
    "~26,000" over the measured count, and the survey doc keeps its pointer.
    """

    def test_pool_report_keeps_the_measured_numbers(self):
        doc = _read(HARNESS / "review/veriharness-pool-check-2026-10.md")
        for token in ("23,197", "10.8%", "mixed-upstream-see-readme", "7/7",
                      "hf-mirror.com", "judge=machine"):
            self.assertIn(token, doc, f"pool-check report lost {token!r}")

    def test_survey_doc_points_at_the_pool_check(self):
        doc = _read(HARNESS / "review/self-modifying-harnesses-2026-10.md")
        self.assertIn("veriharness-pool-check-2026-10.md", doc)
        self.assertIn("23,197", doc, "survey doc must carry the measured count, not the abstract's")


class P39ClauseAnchorTest(unittest.TestCase):
    """P39: M3.18 (the judge is instrumented before its verdicts gate anything).

    Content guards: the clause names its four obligations with their sources,
    the checklist and anti-patterns carry it, references group Y exists with
    the R246 upgrade, and the effect-axis judge rule points at the clause.
    """

    def test_m318_clause_names_the_four_obligations(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        anchor = "The judge is instrumented before its verdicts gate anything (M3.18)"
        self.assertIn(anchor, text, "M3.18 clause title missing")
        section = text.split(anchor, 1)[1][:3200]
        for token in ("bias surface", "fails to enforce", "replayed artifacts",
                      "self-reports", "[R263]", "[R264]", "[R265]", "[R246]",
                      "golden set is trusted exactly as far"):
            self.assertIn(token, section, f"{token!r} missing from M3.18")

    def test_m318_checklist_and_antipatterns(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        self.assertIn("(M3.18).", text.split("## Checklist")[1], "no M3.18 checklist line")
        self.assertIn("Grading on self-report", text, "M3.18 anti-pattern missing")
        self.assertIn("Judge-validated-once", text, "M3.18 second anti-pattern missing")

    def test_references_group_y_and_r246_upgrade(self):
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("## Y.", refs, "group Y missing")
        for ref in ("R263", "R264", "R265"):
            self.assertIn(ref, refs, f"{ref} missing from references.md")
        self.assertIn("read 2026-10-28, P39", refs, "R246 not upgraded to read")
        self.assertNotIn("(*listed, not deep-read*; reported 46", refs,
                         "R246 still carries its listed-only marker")
        bib = _read(HARNESS / "review/references.bib")
        for key in ("wataoka2026selfpreference", "helff2026gaming", "thaman2026rewardhacking"):
            self.assertIn(key, bib, f"bib entry missing: {key}")
        smap = _read(HARNESS / "sources/source-map.md")
        self.assertIn("| M3.18 ", smap, "M3.18 has no source-map row")

    def test_effect_axis_judge_rule_points_at_m318_and_jspsych_flipped(self):
        self.assertIn("M3.18", _read(HARNESS / "review/scored-task-set-2026-10.md"),
                      "effect-axis judge rule does not mention M3.18")
        import json
        cat = json.loads((HARNESS / "src/harness_factory/data/harnesses.json")
                         .read_text(encoding="utf-8"))
        jspsych = next(e for e in cat["harnesses"] if e.get("id") == "jspsych")
        self.assertTrue(jspsych.get("verified"), "D6 not closed: jspsych still verified:false")


class P40AblationGuardTest(unittest.TestCase):
    """P40: the structural ablation baseline (D1 stage C slice 1).

    Pins the measured findings so a future edit cannot inflate the ground:
    10 load-bearing units, 28 unpinned (a coverage gap, not unimportance),
    and the honest statistical boundary.
    """

    def test_ablation_report_keeps_the_measured_findings(self):
        doc = _read(HARNESS / "review/ablation-baseline-2026-10.md")
        for token in ("10 个承重", "28 个", "must_capabilities 的并集",
                      "capabilities 轴", "无方差", "需真实模型运行"):
            self.assertIn(token, doc, f"ablation baseline lost {token!r}")


class P41ToolRouterTest(unittest.TestCase):
    """P41: tool-ecosystem routing (MCP servers / Agent Skills per task family).

    Guards: the router sheet exists, is registered in every load index, and
    carries its four-step loop + the 古籍整理 worked example; the new catalog
    block, feeds, outlets, watchlist topics and the round record are present.
    Content-presence only - prose may be edited freely.
    """

    def test_tool_router_registered_in_all_indexes(self):
        doc = _read(HARNESS / "reference/tool-router.md")
        self.assertIsNotNone(doc, "tool-router.md missing")
        self.assertIn("tool-router", _read(HARNESS / "SKILL.md"),
                      "SKILL.md load-index lost tool-router")
        self.assertIn('"tool-router"', _read(HARNESS / "src/harness_factory/skill.py"),
                      "harness skill index lost tool-router")
        self.assertIn("tool-router.md", _read(HARNESS / "reference/capability-router.md"),
                      "capability-router lost the tool-ecosystem row")

    def test_router_carries_the_loop_and_the_worked_example(self):
        doc = _read(HARNESS / "reference/tool-router.md")
        for token in ("Discover", "Evaluate", "Register", "Metabolize",
                      "Intake quality gate", "古籍整理", "tool poisoning", "2026-10-28"):
            self.assertIn(token, doc, f"router lost {token!r}")

    def test_mcp_and_skills_catalog_block_landed(self):
        cat = json.loads((HARNESS / "src/harness_factory/data/harnesses.json")
                         .read_text(encoding="utf-8"))
        kind_ids = {k["id"] for k in cat["kinds"]}
        self.assertIn("server-registry", kind_ids, "new kind server-registry not declared")
        self.assertIn("server-collection", kind_ids, "new kind server-collection not declared")
        sp = {e["id"] for e in cat["harnesses"] if e.get("class") == "skills-protocols"}
        for hid in ("mcp-registry", "mcp-servers-reference", "smithery", "glama",
                    "pulsemcp", "mcp-so", "anthropics-skills-lib", "skills-sh"):
            self.assertIn(hid, sp, f"skills-protocols block lost {hid}")

    def test_feeds_and_outlets_registered(self):
        sources = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                              .read_text(encoding="utf-8"))
        hids = {e["id"] for e in sources["groups"]["harnesses"] if isinstance(e, dict)}
        for sid in ("mcp-servers-repo", "mcp-registry-repo", "mcp-blog",
                    "anthropic-skills-repo", "vercel-skills"):
            self.assertIn(sid, hids, f"feed entity {sid} missing")
        agentskills = next(e for e in sources["groups"]["harnesses"] if e.get("id") == "agentskills")
        self.assertIsNotNone(agentskills.get("feed"), "agentskills feed still null after P41")
        outlets = {e["id"]: e for e in sources["groups"]["outlets"] if isinstance(e, dict)}
        for oid in ("ctext", "cbeta", "cbdb", "bdrc", "nlc-guji", "wikisource-zh", "inkstone"):
            self.assertIn(oid, outlets, f"classical-texts outlet {oid} missing")
        for oid in ("bdrc", "sinica-hanja", "marco-cbdb-sjtu"):
            self.assertFalse(outlets[oid]["verified"],
                             f"{oid} failed its probe - it must stay unverified until re-probed")

    def test_watchlist_discovery_topics(self):
        wl = json.loads((HARNESS / "src/harness_factory/data/watchlist.json")
                        .read_text(encoding="utf-8"))
        ids = {t["id"] for t in wl["topics"]}
        self.assertIn("mcp-skills-ecosystem", ids, "tool-ecosystem discovery topic missing")
        self.assertIn("classical-texts-dh", ids, "classical-texts topic missing")

    def test_survey_and_round_record(self):
        doc = _read(HARNESS / "review/mcp-skills-landscape-2026-10.md")
        for token in ("registry.modelcontextprotocol.io/v0/servers", "2025-12-18",
                      "Tool poisoning", "2026-10-28"):
            self.assertIn(token, doc, f"survey lost {token!r}")
        cycles = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                             .read_text(encoding="utf-8"))
        by_id = {c["id"]: c for c in cycles["cycles"]}
        self.assertIn("P41", by_id, "round not recorded")
        self.assertEqual(by_id["P41"]["added"]["catalog_delta"], 8)
        self.assertIn("P41.R1", {r["id"] for r in cycles["roadmap"]},
                      "CBETA MCP source-audit not registered as a deferred item")


class P42ClauseAnchorTest(unittest.TestCase):
    """P42: M8.11's boundary state vocabulary and the D8 closeout.

    Content guards: the deepening names both first-party sources and the
    branchable-vocabulary rule, references group Z exists with the R250
    upgrade, and D8 is closed in the roadmap.
    """

    def test_m811_names_the_boundary_vocabulary_rule(self):
        text = _read(HARNESS / "core/09-collaboration-and-sessions.md")
        for token in ("declared boundary vocabulary", "[R266]", "[R250]",
                      "Messages should not deliver outputs", "file-locked claiming"):
            self.assertIn(token, text, f"M8.11 deepening lost {token!r}")
        self.assertIn(
            "terminal vs needs-input distinguishable",
            text.split("## Checklist")[1],
            "no M8.11 boundary-vocabulary checklist line",
        )

    def test_references_group_z_and_r250_upgrade(self):
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("## Z.", refs, "group Z missing")
        self.assertIn("R266", refs)
        self.assertIn("read 2026-10-28, P42", refs, "R250 not upgraded to read")
        self.assertNotIn("(*listed, not deep-read*; **peer parallel sessions**", refs,
                         "R250 still carries its listed-only marker")
        bib = _read(HARNESS / "review/references.bib")
        self.assertIn("a2a2026specification", bib, "bib entry missing")
        smap = _read(HARNESS / "sources/source-map.md")
        self.assertIn("P42 adds", smap, "M8.11 source-map row not extended")

    def test_d8_closed_in_the_roadmap(self):
        import json
        d = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                       .read_text(encoding="utf-8"))
        d8 = next(r for r in d["roadmap"] if r["id"] == "D8")
        self.assertEqual(d8["status"], "done")
        self.assertEqual(d8.get("done_in"), "P42")


class P43ClauseAnchorTest(unittest.TestCase):
    """P43: the frontier sweep landed M5.14, M3.19, the M1.11 deepening, and the ACS cue."""

    def test_m514_and_m319_name_their_mechanisms(self):
        t6 = _read(HARNESS / "core/06-self-evolution.md")
        anchor = "Failures are mandatory signal (M5.14)"
        self.assertIn(anchor, t6, "M5.14 missing")
        sec = t6.split(anchor, 1)[1][:1800]
        for token in ("0 of 14", "diagnostics", "[R267]", "validation-to-test"):
            self.assertIn(token, sec, f"{token!r} missing from M5.14")
        t4 = _read(HARNESS / "core/04-verification-and-gates.md")
        anchor4 = "A benchmark declares its task validity and outcome validity (M3.19)"
        self.assertIn(anchor4, t4, "M3.19 missing")
        sec4 = t4.split(anchor4, 1)[1][:2200]
        for token in ("task validity", "outcome validity", "[R269]", "33%", "M3.18"):
            self.assertIn(token, sec4, f"{token!r} missing from M3.19")

    def test_m111_deepening_and_checklist_lines(self):
        t2 = _read(HARNESS / "core/02-context-engineering.md")
        for token in ("Θ(log n)", "[R268]", "Bloom filter", "compounding error"):
            self.assertIn(token, t2, f"M1.11 deepening lost {token!r}")
        self.assertIn("(M5.14).", _read(HARNESS / "core/06-self-evolution.md").split("## Checklist")[1])
        self.assertIn("(M3.19).", _read(HARNESS / "core/04-verification-and-gates.md").split("## Checklist")[1])

    def test_references_group_aa_and_acs_cue(self):
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("## AA.", refs)
        for ref in ("R267", "R268", "R269", "R270"):
            self.assertIn(ref, refs)
        for author in ("Wataoka", "Tirmazi", "Zhu, Yuxuan", "Liu, Yuxuan"):
            pass  # R263-265 checked in P39 guards; here check the new ones
        self.assertIn("Y. Liu, Z. Su", refs, "R267 authors missing")
        self.assertIn("H. Tirmazi", refs, "R268 authors missing")
        bib = _read(HARNESS / "review/references.bib")
        for key in ("feedbackdynamics2026", "compactiontheory2026", "abc2025benchmarks", "owasp2026acs"):
            self.assertIn(key, bib)
        frontier = _read(HARNESS / "review/frontier-2026-10.md")
        self.assertIn("[R270]", frontier, "ACS cue not closed with R270")


class P44CoverageGuardTest(unittest.TestCase):
    """P44: the holdout coverage widening (the deliberate edit P40 called for).

    Pins the widened board shape (7 tasks, the family-definitional musts,
    the two new effect_metrics) and the re-measured coverage numbers.
    """

    def test_board_carries_seven_tasks_and_the_widened_musts(self):
        from harness_factory import scoreboard

        board = scoreboard.load_scoreboard()
        self.assertEqual(len(board["tasks"]), 7, "expected 7 canonical tasks")
        by_id = {e["id"]: e for e in board["tasks"]}
        for tid in ("lit-review", "kg-dh", "deep-research"):
            for cap in ("untrusted-content-discipline", "context-budget-policy",
                        "resumable-memory", "tool-use"):
                self.assertIn(cap, by_id[tid]["must_capabilities"], f"{tid} lost {cap!r}")
        self.assertIn("reproducible-experiments", by_id["model-choice"]["must_capabilities"])
        self.assertIn("formal-verification", by_id["proof-verification"]["must_capabilities"])
        self.assertIn("statistical-inference", by_id["bayesian-stats"]["must_capabilities"])
        for tid in ("proof-verification", "bayesian-stats"):
            self.assertTrue(by_id[tid].get("effect_metric"), f"{tid}: effect_metric missing")

    def test_ablation_report_records_the_remeasurement(self):
        doc = _read(HARNESS / "review/ablation-baseline-2026-10.md")
        for token in ("10 → 17", "28 → 21", "proof-verification", "reproducible-experiments"):
            self.assertIn(token, doc, f"coverage widening record lost {token!r}")


class P45TrialGuardTest(unittest.TestCase):
    """P45: the paired trial's receipts and the scale-blindness finding."""

    def test_trial_doc_carries_results_and_boundary(self):
        doc = _read(HARNESS / "review/paired-trial-2026-10-28.md")
        for token in ("0.2", "1.0", "citation-verifiability", "2310.08560",
                      "N=1", "judge=machine"):
            self.assertIn(token, doc, f"trial doc lost {token!r}")

    def test_p45r1_registered(self):
        import json
        d = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                       .read_text(encoding="utf-8"))
        self.assertIn("P45.R1", {r["id"] for r in d["roadmap"]},
                      "scale-blindness finding not registered")


class P47ScaleGuardTest(unittest.TestCase):
    """P47: effect receipts may declare a scale; the low-outcome rule normalizes."""

    def test_scaled_receipts_roundtrip(self):
        from harness_factory import trace
        line = trace.make_trace("task_outcome", project="p", task="t", harness="h",
                                detail={"judge": "machine", "score": 1.0, "scale": [0, 1]})
        self.assertEqual(trace.validate(line), [])
        bad = trace.make_trace("task_outcome", project="p", task="t", harness="h",
                               detail={"judge": "machine", "score": 1.0, "scale": [5, 1]})
        self.assertIn("scale", "; ".join(trace.validate(bad)))


class P48ModelChoiceTrialGuardTest(unittest.TestCase):
    """P48: the second paired trial (model-choice) is recorded with scaled receipts."""

    def test_trial_doc_records_the_second_pair(self):
        doc = _read(HARNESS / "review/paired-trial-2026-10-28.md")
        # the second trial's numbers live in the P48 section appended to the same doc
        self.assertIn("decision-audit-pass-rate", doc, "second trial metric missing")
        self.assertIn("scale", doc, "the scaled receipts are not recorded")


class P49AcsGuardTest(unittest.TestCase):
    """P49: the ACS deep read deepened M6.11 and closed the reference chain."""

    def test_m611_names_the_enforcement_architecture(self):
        text = _read(HARNESS / "core/07-tools-and-skills.md")
        for token in ("[R271]", "modify", "fail-open", "deterministic policy layer"):
            self.assertIn(token, text, f"M6.11 deepening lost {token!r}")

    def test_r271_reference_chain(self):
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("R271", refs)
        self.assertIn("GenAI-Security-Project/agent-control-standard", refs)
        bib = _read(HARNESS / "review/references.bib")
        self.assertIn("owasp2026acsspec", bib)
        frontier = _read(HARNESS / "review/frontier-2026-10.md")
        self.assertIn("[R271]", frontier, "deep-read follow-up not marked done")


class P50BatteryGuardTest(unittest.TestCase):
    """P50: the experiment battery - three new paired trials, five families measured."""

    def test_battery_doc_carries_results_and_findings(self):
        doc = _read(HARNESS / "review/experiment-battery-2026-10.md")
        for token in ("0.552", "16/29", "逐位复现", "隐藏重放", "编译即接受",
                      "独立重推导", "16 条真实轨迹", "7/7", "0.19"):
            self.assertIn(token, doc, f"battery doc lost {token!r}")

    def test_hidden_replay_suite_exists_and_is_judge_first(self):
        suite = (HARNESS / "updates/dogfood/p50-battery/trial3-unit-tests/hidden_replay.py")
        if suite.exists():  # gitignored; only asserted when present on this machine
            text = suite.read_text(encoding="utf-8")
            self.assertIn("Hidden replay suite", text)
            self.assertIn("NOT the grade", text)


class P51IdeationGuardTest(unittest.TestCase):
    """P51: the ideation capability fills the P18 hole, M5.11 carries the calibration
    evidence, and the battery is a standing routine with a DoD axis."""

    def test_capability_fires_on_plan_artifacts(self):
        from harness_factory.spec import TaskSpec
        from harness_factory.classify import classify
        from harness_factory.derive import derive
        for txt in ("Draft a project plan with the research questions we should pursue",
                    "Write a research proposal outlining the open questions, cite sources",
                    "为我们的智能体记忆研究起草提案，提出值得研究的问题清单，注明来源"):
            plan = derive(TaskSpec(text=txt), classify(TaskSpec(text=txt)))
            self.assertIn("research-question-generation", plan.capabilities,
                          f"the ideation capability did not fire: {txt!r}")

    def test_m511_carries_the_calibration_numbers(self):
        text = _read(HARNESS / "core/06-self-evolution.md")
        for token in ("45.0-53.3%", "[R273]", "[R272]", "behavioral", "trading variance for bias"):
            self.assertIn(token, text, f"M5.11 deepening lost {token!r}")

    def test_battery_routine_is_standing(self):
        self.assertTrue((HARNESS / "tasks/BATTERY.md").exists(), "tasks/BATTERY.md missing")
        bat = _read(HARNESS / "tasks/BATTERY.md")
        for token in ("M5.14", "scale", "M3.19", "trace-audit"):
            self.assertIn(token, bat, f"battery routine lost {token!r}")
        import json
        d = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                       .read_text(encoding="utf-8"))
        battery = next(e for e in d["definition_of_done"] if e["key"] == "battery")
        self.assertFalse(battery["hard"], "the battery DoD axis must stay soft (non-retroactive)")
        cyc = _read(HARNESS / "reference/capability-cycle.md")
        self.assertIn("Battery step (P51, standing)", cyc)


class P52DomainCapabilityTest(unittest.TestCase):
    """P52: the four domain-keyed capabilities fire on their own domain and not on
    a neighbour - discrimination by construction."""

    def test_each_fires_on_its_domain_only(self):
        from harness_factory.spec import TaskSpec
        from harness_factory.classify import classify
        from harness_factory.derive import derive
        cases = [
            ("Cross-check the chronicle accounts of the 1120 succession and note what the sources omit", "history", "source-criticism"),
            ("从认识论角度重构这篇伦理学论文的论证，评估其前提并坦诚反例", "philosophy", "argument-reconstruction"),
            ("国际关系研究：先界定地缘政治的概念，再说明案例选择的规则并留痕", "political-science", "concept-definition"),
            ("Build the safety case for this alignment claim: state the threat model, run red-team capability evals, log the coverage", "ai-safety", "safety-argumentation"),
        ]
        for txt, dom, cap in cases:
            v = classify(TaskSpec(text=txt))
            self.assertEqual(v.domain, dom, f"{txt!r} routed to {v.domain}, expected {dom}")
            plan = derive(TaskSpec(text=txt), v)
            self.assertIn(cap, plan.capabilities, f"{cap!r} did not fire on: {txt!r}")

    def test_cross_domain_does_not_fire(self):
        from harness_factory.spec import TaskSpec
        from harness_factory.classify import classify
        from harness_factory.derive import derive
        plan = derive(TaskSpec(text="add unit tests to the parser"), classify(TaskSpec(text="add unit tests to the parser")))
        for cap in ("source-criticism", "argument-reconstruction", "concept-definition", "safety-argumentation"):
            self.assertNotIn(cap, plan.capabilities, f"{cap!r} leaked into a coding task")


class P53BatteryRegistryTest(unittest.TestCase):
    """P53: the experiment registry - the battery as data, self-experimentation made mechanical."""

    def test_registry_valid_and_complete(self):
        from harness_factory import battery
        self.assertEqual(battery.validate_battery(), [])
        board = battery.load_battery()
        # P67 metabolism: seven scoreboard families plus the two P62 trials
        # (reading-extraction, cron-parsing) that ran with receipts but were
        # never registered - the count moved 7 -> 9, retroactively.
        # P70: a 10th family (agent-eval-reliability) is registered PENDING
        # with pre-declared judge_checks but no results - the bar is set,
        # the run is not yet executed (M5.11: no fabricated score).
        self.assertGreaterEqual(len(board["families"]), 10, "the battery should have at least 10 families (7 scoreboard + extensions)")
        done = [f for f in board["families"] if f["status"] == "done"]
        self.assertGreaterEqual(len(done), 9, "every registered DONE family has both-condition receipts")
        for fam in done:
            self.assertIn("scale", fam) and self.assertIn("round", fam) and self.assertIn("results", fam)

    def test_next_pending_returns_a_full_spec(self):
        from harness_factory import battery
        fam = battery.next_pending()
        if fam is not None:
            for field in ("judge_checks", "scale", "spec"):
                self.assertIn(field, fam, f"pending family {fam['task_id']} lacks {field!r}")
            self.assertTrue(fam["spec"].get("task"), "spec.task missing")

    def test_cli_lists_the_registry(self):
        from harness_factory import cli
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.main(["battery"])
        self.assertEqual(code, 0)
        self.assertIn("battery (experiment registry)", buf.getvalue())


class P54ThinkingModesTest(unittest.TestCase):
    """P54: the thinking-modes section in methodology-map (cross-disciplinary reasoning modes)."""

    def test_seven_thinking_mode_rows_present(self):
        text = _read(HARNESS / "reference/methodology-map.md")
        self.assertIn("Thinking modes", text, "thinking-modes section missing")
        for token in ("Abduction", "Differential diagnosis", "Design iteration",
                      "Fermi estimation", "Thought experiment", "Explanation styles",
                      "Comparative method", "Peirce", "premature closure",
                      "Simon", "Hempel", "Przeworski"):
            self.assertIn(token, text, f"thinking-mode row lost {token!r}")

    def test_audit_doc_declares_non_exhaustion(self):
        doc = _read(HARNESS / "review/discipline-coverage-audit-2026-10.md")
        for token in ("没有", "穷尽", "M0.5", "probe-domains", "D3"):
            self.assertIn(token, doc, f"coverage audit lost {token!r}")


class P57OrgSweepTest(unittest.TestCase):
    """P57: the org-practices sweep - AAIF governance, superpowers reinjection, the new standards."""

    def test_template_reinjection_line_present(self):
        text = _read(HARNESS / "src/harness_factory/templates/AGENTS.md.tmpl")
        self.assertIn("After any context compaction", text, "post-compaction reinjection line missing")
        self.assertIn("pointer.json", text, "reinjection must name the pointer")

    def test_m111_carries_the_reinjection_exemplar(self):
        text = _read(HARNESS / "core/02-context-engineering.md")
        self.assertIn("[R277]", text, "M1.11 lost the superpowers exemplar")
        self.assertIn("reinjected after the pass", text)

    def test_catalog_and_references_record_the_sweep(self):
        cat = json.loads((HARNESS / "src/harness_factory/data/harnesses.json")
                         .read_text(encoding="utf-8"))
        ids = {e.get("id") for e in cat["harnesses"]}
        for rid in ("superpowers", "aaif", "open-responses", "openenv", "opensandbox"):
            self.assertIn(rid, ids, f"catalog entry missing: {rid}")
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("## AC.", refs)
        for ref in ("R276", "R277", "R278"):
            self.assertIn(ref, refs)
        bib = _read(HARNESS / "review/references.bib")
        self.assertIn("anthropic2026skillsaaif", bib)
        self.assertIn("vincent2026superpowers", bib)
        srcs = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                          .read_text(encoding="utf-8"))
        self.assertTrue(any(e.get("id") == "aaif" for e in srcs["groups"]["harnesses"]),
                        "aaif source entity missing")


class CommandSurfaceGuardTest(unittest.TestCase):
    """P58: the new-era commands must be documented in every entry doc.

    The zh README lost full-update/brief for three rounds (P30/P32 fixed only
    the EN side) and GUIDE lacked the entire measurement-era command set until
    P58 - both drifts happened because no guard watched the command lists.
    Five key commands, four entry docs, one check."""

    _DOCS = ("README.md", "README.zh-CN.md", "harness_factory/introduction.md",
             "harness_factory/GUIDE.md")
    _COMMANDS = ("harness scoreboard", "harness trace-audit", "harness battery",
                 "harness classify", "harness full-update")

    def test_key_commands_documented_in_every_entry_doc(self):
        missing = []
        for doc in self._DOCS:
            text = _read(ROOT / doc)
            for cmd in self._COMMANDS:
                # GUIDE's command table uses bare command names ("| `scoreboard` |"),
                # the other three docs use the full "harness <cmd>" form.
                bare = cmd.replace("harness ", "", 1)
                if cmd not in text and f"`{bare}" not in text:
                    missing.append(f"{doc}: {cmd}")
        self.assertEqual(missing, [], "command-surface drift: " + "; ".join(missing))


class P59FeedHealthTest(unittest.TestCase):
    """P59: the feed-health round - topic wiring closed, dead doors repaired,
    audit false positives fixed. Pins the SSOT wiring so a later edit cannot
    silently re-open a door or un-plug a topic carrier (the very defect P59
    found: watchlist topics registered with no entity carrying them)."""

    def test_survey_doc_carries_the_probe_facts(self):
        doc = _read(HARNESS / "review/feed-health-2026-11.md")
        for token in ("charonhub.deeplearning.ai/rss",
                      "rsshub.bestblogs.dev/anthropic/news",
                      "67% \u2192 91.7%", "2026-11-02",
                      "no official RSS", "neurips-blog", "archive-blog",
                      "ambition-and-agency", "topic earns sources"):
            self.assertIn(token, doc, f"feed-health survey lost {token!r}")

    def test_sources_topic_registry_and_wiring(self):
        srcs = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                          .read_text(encoding="utf-8"))
        for tid in ("mcp-skills-ecosystem", "classical-texts-dh",
                    "scholarly-discovery"):
            self.assertIn(tid, srcs["topic_ids"], f"{tid} missing from topic_ids")
        by_id = {e["id"]: e for g in srcs["groups"].values() for e in g}
        for eid in ("neurips-blog", "archive-blog"):
            self.assertIn(eid, by_id, f"new channel {eid} missing")
        mcp_carriers = [e for e in by_id.values()
                        if "mcp-skills-ecosystem" in e.get("topics", [])]
        self.assertGreaterEqual(len(mcp_carriers), 14,
                                "mcp-skills-ecosystem wiring regressed below 14 carriers")
        arxiv = by_id["arxiv-cs-ai"]
        self.assertIn("scholarly-discovery", arxiv.get("topics", []),
                      "arxiv door no longer carries scholarly-discovery")

    def test_dead_doors_stay_repaired_or_honest(self):
        srcs = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                          .read_text(encoding="utf-8"))
        by_id = {e["id"]: e for g in srcs["groups"].values() for e in g}
        self.assertIn("charonhub", by_id["the-batch"].get("feed", ""),
                      "the-batch feed door regressed to the 404 path")
        self.assertIn("bestblogs", by_id["anthropic"].get("feed", ""),
                      "anthropic mirror door regressed to the 404 path")
        for eid in ("meta-fair", "aaif"):
            self.assertIsNone(by_id[eid].get("feed"),
                              f"{eid} feed must stay null until a door is verified")

    def test_engine_host_normalization_and_known_union(self):
        from harness_factory import evolution
        self.assertEqual(evolution._host("https://WWW.latent.space/"), "latent.space")
        self.assertEqual(evolution._host(""), "")
        text = _read(HARNESS / "src/harness_factory/evolution.py")
        for token in ('e.get("feed", "")', 'e.get("api", "")'):
            self.assertIn(token, text,
                          f"untracked_source known-set lost the {token!r} union")

    def test_p59_cycle_and_roadmap_registered(self):
        d = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                       .read_text(encoding="utf-8"))
        self.assertIn("P59", {c["id"] for c in d["cycles"]}, "P59 cycle missing")
        self.assertIn("P59.R1", {r["id"] for r in d["roadmap"]},
                      "P59.R1 deferred item missing")


class P60WeeklySweepTest(unittest.TestCase):
    """P60: the weekly sweep - ThinkingBox/QueenBee/LegoSR entered with their roles."""

    def test_weekly_sweep_doc_carries_the_three_finds(self):
        doc = _read(HARNESS / "review/weekly-sweep-2026-11-02.md")
        for token in ("ThinkingBox", "QueenBee", "LegoSR", "77.61%", "SFT-Bank",
                      "20/20", "OpenEnv"):
            self.assertIn(token, doc, f"weekly sweep lost {token!r}")

    def test_catalog_and_references_record_the_entries(self):
        cat = json.loads((HARNESS / "src/harness_factory/data/harnesses.json")
                         .read_text(encoding="utf-8"))
        ids = {e.get("id") for e in cat["harnesses"]}
        for rid in ("thinkingbox", "queenbee", "legosr"):
            self.assertIn(rid, ids, f"catalog entry missing: {rid}")
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("## AD.", refs)
        for ref in ("R279", "R280", "R281"):
            self.assertIn(ref, refs)
        d1 = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                        .read_text(encoding="utf-8"))
        d1r = next(r for r in d1["roadmap"] if r["id"] == "D1")
        self.assertIn("QueenBee", d1r["reason"], "D1 stage-C precedent note missing")


class P63SimulationGuardTest(unittest.TestCase):
    """P63: the self-evolution deep upgrade - dedup and the simulation test."""

    def test_trace_audit_has_dedup(self):
        src = _read(HARNESS / "src/harness_factory/trace_audit.py")
        self.assertIn("traces-proposals.jsonl", src, "dedup: past proposals not read")
        self.assertIn("already emitted", src, "dedup comment missing")

    def test_simulation_doc_recorded(self):
        # the simulation is inline in P63's slices; the cycles entry is the record
        import json
        d = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                       .read_text(encoding="utf-8"))
        p63 = next((c for c in d["cycles"] if c["id"] == "P63"), None)
        self.assertIsNotNone(p63, "P63 not registered")
        self.assertIn("5 proposals with correct counts", p63["note"], "simulation result not recorded")


class P66WrapUpTest(unittest.TestCase):
    """P66: the wrap-up round - every P65 direction gets its last mile."""

    def test_self_model_has_consumers(self):
        # M0.4: engine surface without a consumer is dead weight. P65 shipped
        # self_model.py unconnected; P66 wired the CLI verb and the loop phase.
        src = _read(HARNESS / "src/harness_factory/cli.py")
        self.assertIn('"self-model"', src)
        self.assertIn("_cmd_self_model", src)
        fu = _read(HARNESS / "src/harness_factory/full_update.py")
        self.assertIn('"self-model"', fu, "full-update does not run the self-model")

    def test_self_model_cli_reports_the_live_registry(self):
        import contextlib
        import io

        from harness_factory import cli
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.main(["self-model"])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("families done", out)
        self.assertNotIn("all with effect_metric", out)  # the old constant line

    def test_vocab_v2_template_contract_names_the_events(self):
        tmpl = _read(HARNESS / "src/harness_factory/templates/AGENTS.md.tmpl")
        for event in ("context_pressure", "tool_error", "human_preference", "latency_anomaly"):
            self.assertIn(event, tmpl, f"template contract lost {event}")
        for key in ("detail.tool", "detail.preference", "detail.operation"):
            self.assertIn(key, tmpl, f"template contract lost {key}")

    def test_playbook_line_no_longer_dangles(self):
        tmpl = _read(HARNESS / "src/harness_factory/templates/AGENTS.md.tmpl")
        self.assertNotIn("harness_factory/domains/{{ domain }}", tmpl,
                         "hardcoded repo-relative playbook path is back")
        self.assertIn("{{ domain_playbook }}", tmpl)

    def test_p66_registered(self):
        d = json.loads((HARNESS / "src/harness_factory/data/cycles.json")
                       .read_text(encoding="utf-8"))
        p66 = next((c for c in d["cycles"] if c["id"] == "P66"), None)
        self.assertIsNotNone(p66, "P66 not registered")


class P67RegistryMetabolismTest(unittest.TestCase):
    """P67: the experiment registry metabolizes - executed paired trials and
    registry rows reconcile in BOTH directions (the P62 failure: trials ran,
    receipts existed, the registry never heard about it)."""

    def test_battery_md_is_current(self):
        bat = _read(HARNESS / "tasks/BATTERY.md")
        self.assertIn("15/15", bat, "BATTERY.md must reflect the registry count")
        self.assertIn("trial_projects", bat)
        self.assertNotIn("待跑：deep-research", bat, "stale pending list is back")
        self.assertIn("P76", bat, "the reliability family's genuine-variance upgrade must be recorded")
        self.assertIn("不区分条件", bat, "the honest null result must stay visible")

    def test_assessment_carries_the_erratum(self):
        doc = _read(HARNESS / "review/capability-system-assessment-2026-11.md")
        self.assertIn("勘误（P67", doc, "the 9/9-vs-7/7 erratum was not filed")

    def test_reconcile_flags_both_directions_simulated(self):
        from harness_factory import battery, trace

        lines = [
            trace.make_trace("task_outcome", project="updates/dogfood/p99-mystery",
                             task="mystery", harness="h",
                             detail={"judge": "machine", "score": 1.0, "scale": [0, 1],
                                     "condition": "A-bare"}),
            trace.make_trace("task_outcome", project="updates/dogfood/p99-mystery",
                             task="mystery", harness="h",
                             detail={"judge": "machine", "score": 1.0, "scale": [0, 1],
                                     "condition": "B-harness"}),
        ]
        board = {"families": [{"task_id": "lit-review",
                               "trial_projects": ["updates/dogfood/p45-paired-trial"]}]}
        rec = battery.reconcile(board, lines)
        self.assertEqual(rec["unregistered_trials"], ["updates/dogfood/p99-mystery"])
        self.assertEqual(rec["declared_without_receipts"], ["updates/dogfood/p45-paired-trial"])
        # backslashes as the real traces record them must normalize to the same key
        lines[0]["project"] = "updates\\dogfood\\p99-mystery"
        rec = battery.reconcile(board, lines)
        self.assertIn("updates/dogfood/p99-mystery", rec["unregistered_trials"])

    def test_control_arm_none_receipted_by_one_arm(self):
        """P74: a determinism family (control_arm=none) is receipted by
        B-harness-only traces; without the traces it still flags."""
        from harness_factory import battery, trace

        lines = [
            trace.make_trace("task_outcome", project="updates/dogfood/p67-reliability",
                             task="reliability-attempt-1", harness="h",
                             detail={"judge": "machine", "score": 1.0, "scale": [0, 1],
                                     "condition": "B-harness"}),
        ]
        det = {"task_id": "agent-eval-reliability", "status": "done",
               "control_arm": "none",
               "trial_projects": ["updates/dogfood/p67-reliability"]}
        rec = battery.reconcile({"families": [det]}, lines)
        self.assertNotIn("updates/dogfood/p67-reliability", rec["declared_without_receipts"],
                         "one-armed determinism receipts must satisfy the binding")
        rec = battery.reconcile({"families": [det]}, [])
        self.assertEqual(rec["declared_without_receipts"], ["updates/dogfood/p67-reliability"])
        # and the receipts must NOT read as an unregistered paired trial
        self.assertEqual(rec["unregistered_trials"], [])

    def test_real_traces_reconcile_clean(self):
        import os
        from harness_factory import battery, config, trace

        try:
            path = config.home() / trace.TRACES_REL
            if not path.exists():
                self.skipTest("no tool-home traces on this machine")
            lines = trace.read_traces(path)
        except OSError:
            self.skipTest("tool-home traces inaccessible on this machine")
        if not lines:
            self.skipTest("no tool-home trace records on this machine")
        rec = battery.reconcile(traces_lines=lines)
        self.assertEqual(rec["unregistered_trials"], [],
                         "a paired trial ran without a registry row (P62's failure)")
        self.assertEqual(rec["declared_without_receipts"], [],
                         "a registry row names a trial the traces cannot show")


class P68ToolEcosystemTest(unittest.TestCase):
    """P68: the outside-harness AI tool stack is surveyed from primary sources and
    wired into the standing loop - the scan must run itself every full-update
    (discover via watchlist queries + feed pulls, evaluate, register, metabolize).
    Pins the survey doc, the SSOT wiring, and the feed-pullability the loop needs."""

    def test_survey_doc_carries_the_verified_facts(self):
        doc = _read(HARNESS / "review/ai-tool-stack-scan-2026-11.md")
        self.assertIsNotNone(doc, "the P68 survey doc is missing")
        for token in ("2026-11-03", "maintenance mode", "NOASSERTION",
                      "arXiv:2504.19413", "arXiv:2404.16130", "ai-tool-stack"):
            self.assertIn(token, doc, f"survey lost the fact {token!r}")

    def test_topic_registered_and_carried(self):
        srcs = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                          .read_text(encoding="utf-8"))
        self.assertIn("ai-tool-stack", srcs["topic_ids"], "topic not declared")
        carriers = [e for e in srcs["groups"]["tools"]
                    if "ai-tool-stack" in e.get("topics", [])]
        self.assertGreaterEqual(len(carriers), 12,
                                "the tool-stack scan result was un-registered")
        ids = {e["id"] for e in carriers}
        for eid in ("mem0", "graphiti", "langfuse", "otel-genai", "e2b",
                    "instructor", "outlines", "promptfoo", "litellm", "vllm",
                    "nemo-guardrails", "ms-graphrag"):
            self.assertIn(eid, ids, f"verified tool {eid} missing from the registry")

    def test_every_carrier_is_feed_pullable(self):
        # The loop's discover leg pulls feeds; a carrier without one is a dead door
        # for the feed provider (it would still be LLM-discoverable, but the
        # deterministic half of the scan would silently skip it).
        srcs = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                          .read_text(encoding="utf-8"))
        for e in srcs["groups"]["tools"]:
            if "ai-tool-stack" in e.get("topics", []):
                self.assertTrue((e.get("feed") or "").startswith("https://"),
                                f"{e['id']} carries the topic but no pullable feed")

    def test_watchlist_topic_drives_discovery(self):
        wl = json.loads((HARNESS / "src/harness_factory/data/watchlist.json")
                        .read_text(encoding="utf-8"))
        topic = next((t for t in wl["topics"] if t["id"] == "ai-tool-stack"), None)
        self.assertIsNotNone(topic, "ai-tool-stack missing from the loop's watchlist")
        self.assertTrue(topic.get("queries"), "queries empty - the LLM scan has no marching orders")
        self.assertTrue(topic.get("keywords"), "keywords empty - relevance scoring has no signal")

    def test_tool_router_sheet_names_the_family(self):
        doc = _read(HARNESS / "reference/tool-router.md")
        self.assertIn("ai-tool-stack", doc)
        self.assertIn("4.1", doc, "the standing family section (§4.1) was removed")
        self.assertIn("review/ai-tool-stack-scan-2026-11.md", doc,
                      "the router sheet lost its pointer to the verified inventory")

    def test_live_snapshot_covers_the_new_topic(self):
        from harness_factory.evolution import iter_entities, snapshot

        srcs = json.loads((HARNESS / "src/harness_factory/data/sources.json")
                          .read_text(encoding="utf-8"))
        wl = json.loads((HARNESS / "src/harness_factory/data/watchlist.json")
                        .read_text(encoding="utf-8"))
        m = snapshot(srcs, wl)
        self.assertNotIn("ai-tool-stack", m["uncovered_topics"],
                         "topic declared in the watchlist with no source carrying it")


class P69RoutineTest(unittest.TestCase):
    """P69: the standing routine work (trend review + Pages dashboard) must stay
    wired end to end - the engine phase, the CLI verbs, the committed snapshot
    bridge, the deploy workflow, the authored analysis, and the workspace doc -
    and the published page must remain a self-contained, asset-free artifact."""

    def test_full_update_wires_the_eighth_phase(self):
        text = _read(HARNESS / "src/harness_factory/full_update.py")
        self.assertIn('"trend-review"', text, "phase 8 (trend-review) was unwired")
        self.assertIn("trend.run", text)
        self.assertIn("pages.run", text, "the loop must also rebuild the dashboard")

    def test_cli_exposes_trend_and_pages(self):
        text = _read(HARNESS / "src/harness_factory/cli.py")
        for token in ('"trend"', '"pages"', "_cmd_trend", "_cmd_pages"):
            self.assertIn(token, text, f"CLI lost {token!r}")

    def test_committed_snapshot_has_the_four_clusters(self):
        snap = json.loads((HARNESS / "src/harness_factory/data/trend-snapshot.json")
                          .read_text(encoding="utf-8"))
        self.assertEqual(set(snap["clusters"]),
                         {"industry", "harness", "trajectories", "domains"})
        for pack in snap["clusters"].values():
            self.assertTrue({"count", "recent", "top", "title"} <= set(pack))

    def test_page_build_is_offline_guarded_and_deployed(self):
        ci = _read(ROOT / ".github/workflows/ci.yml")
        self.assertIn("pages --write", ci, "CI no longer rebuilds the page")
        self.assertIn("zero external assets", ci, "CI lost the asset-free assertion")
        pages = _read(ROOT / ".github/workflows/pages.yml")
        self.assertIn("actions/deploy-pages", pages)
        self.assertIn("actions/upload-pages-artifact", pages)

    def test_published_page_is_self_contained(self):
        doc = (ROOT / "docs" / "index.html")
        self.assertTrue(doc.exists(), "the committed Pages artifact is missing")
        html = doc.read_text(encoding="utf-8")
        self.assertTrue(html.lstrip().lower().startswith("<!doctype html>"))
        self.assertIsNone(re.search(r"(?i)<(script|link|img)[ >]", html),
                          "the dashboard must carry zero external assets/JS")
        self.assertIn("Harness Factory", html)
        self.assertTrue((ROOT / "docs" / ".nojekyll").exists())

    def test_authored_analysis_covers_the_three_asks(self):
        doc = _read(HARNESS / "review/trend-review-2026-11-03.md")
        self.assertIsNotNone(doc, "the routine's worked-instance doc is missing")
        for part in ("行业全景与相邻领域", "Harness 文献综述",
                     "新兴方向", "分析与预测", "溯源表"):
            self.assertIn(part, doc, f"the review lost {part!r}")
        # citations-lifeline: it must anchor to the repo's full-read literature
        for anchor in ("R279", "R280", "arXiv:2606.27492", "引用即生命线", "unverified"):
            self.assertIn(anchor, doc, f"review lost anchor/source-discipline {anchor!r}")

    def test_agents_md_documents_the_routine(self):
        text = _read(ROOT / "AGENTS.md")
        for token in ("例行工作 / Routine work", "docs/index.html", "pages.yml",
                      "trend-review"):
            self.assertIn(token, text, f"AGENTS.md no longer documents {token!r}")


class P71EmbodiedHarnessTest(unittest.TestCase):
    """P71 integrated uni-robot-agent (arXiv:2611.01560, R291) — an embodied
    robot-use harness.  Content-presence guards: the registration, the core/03
    M2.14 pipelined-execution clause, the no-privileged-input fair-attribution
    gate in evidence-instruments, the widened watchlist probe, and the survey /
    battery crosswalk.  Scores stay *reported, not replicated* — none is
    asserted as this factory's own capability.
    """

    def test_r291_registered_in_references(self):
        text = _read(HARNESS / "review/references.md")
        self.assertIsNotNone(text)
        self.assertIn("## AF.", text, "\u00a7AF group missing")
        for token in ("R291", "uni-robot-agent", "Democratizing Robot-Use Agents", "arXiv:2611.01560"):
            self.assertIn(token, text, f"{token!r} missing from references.md")
        self.assertIn("R291: **2026-11-04**", text, "\u00a7AF access-date header missing")
        self.assertIn("R1\u2013R295", text, "\u4e2d\u6587\u901f\u89c8 range not reconciled to the current top reference")

    def test_r291_in_bibtex(self):
        bib = _read(HARNESS / "review/references.bib")
        self.assertIsNotNone(bib)
        self.assertIn("yuan2026democratizing", bib)
        self.assertIn("2611.01560", bib)

    def test_tool_registered_with_verified_feed_and_license(self):
        data = json.loads((HARNESS / "src/harness_factory/data/sources.json").read_text(encoding="utf-8"))
        tools = {t["id"]: t for t in data["groups"]["tools"]}
        self.assertIn("uni-robot-agent", tools)
        t = tools["uni-robot-agent"]
        self.assertTrue(t["feed"].endswith("releases.atom"), "feed must be a pullable releases atom")
        self.assertIn("mit", [x.lower() for x in t["tags"]], "license tag missing")
        self.assertTrue(set(t["topics"]) <= set(data["topic_ids"]), "tool topic not in topic_ids enum")
        self.assertIn("agent-harness", t["topics"])

    def test_core03_pipelining_clause_anchored(self):
        text = _read(HARNESS / "core/03-long-running-agents.md")
        self.assertIsNotNone(text)
        self.assertIn("M2.14", text)
        self.assertIn("Pipelined execution: overlap reasoning with tool execution (M2.14)", text, "M2.14 title missing")
        self.assertIn("R291", text, "M2.14 unsourced")
        self.assertIn("preserve order", text)
        self.assertIn("(M2.14, M2.11)", text.split("## Checklist")[1], "no M2.14 checklist row")
        self.assertIn("Serial inference-then-execute", text, "M2.14 anti-pattern missing")

    def test_evidence_instruments_fair_attribution_gate(self):
        text = _read(HARNESS / "reference/evidence-instruments.md")
        self.assertIsNotNone(text)
        self.assertIn("\u00a7AF", text, "source header not extended to \u00a7AF")
        self.assertIn("withhold privileged inputs", text, "gate 6 missing")
        self.assertIn("no-privileged-input", text)
        self.assertIn("R291", text)
        for cap in ("visual understanding", "spatial grounding", "geometric encoding", "embodied reasoning"):
            self.assertIn(cap, text, f"failure-taxonomy term {cap!r} missing")

    def test_watchlist_agent_harness_widened_for_embodied(self):
        data = json.loads((HARNESS / "src/harness_factory/data/watchlist.json").read_text(encoding="utf-8"))
        ah = next(t for t in data["topics"] if t["id"] == "agent-harness")
        joined = " ".join(ah["queries"] + ah["keywords"]).lower()
        for token in ("robot-use", "embodied"):
            self.assertIn(token, joined, f"agent-harness probe not widened with {token!r}")

    def test_survey_and_battery_embodied_crosswalk(self):
        survey = _read(HARNESS / "review/harness-evaluation-benchmarks-2026-11.md")
        self.assertIsNotNone(survey)
        self.assertIn("Embodied extension", survey)
        self.assertIn("R291", survey)
        battery = _read(HARNESS / "tasks/BATTERY.md")
        self.assertIsNotNone(battery)
        self.assertIn("R291", battery)
        self.assertIn("\u5177\u8eab\u6620\u5c04", battery, "battery embodied note missing")

    def test_p71_registered_in_cycle_ledger(self):
        from harness_factory import cycle
        entry = next((c for c in cycle.cycles() if c["id"] == "P71"), None)
        self.assertIsNotNone(entry, "P71 absent from cycles.json")
        self.assertEqual("done", entry["status"])
        self.assertIn("M2.14", entry["added"]["clauses"])
        self.assertIn("R291", entry["added"]["references"])


class P72WSPTest(unittest.TestCase):
    """P72: M5.13 scope extended to cover weight-space programming."""

    def test_m513_names_three_modalities(self):
        text = _read(HARNESS / "core/06-self-evolution.md")
        for token in ("weight-space programming", "[R292]", "M5.13(d)",
                      "0.016%", "MATH-500"):
            self.assertIn(token, text, f"M5.13 scope extension lost {token!r}")

    def test_references_have_r292_and_p72_registered(self):
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("R292", refs)
        self.assertIn("Weight-Space Programming", refs)
        self.assertIn("MIT CSAIL", refs)
        bib = _read(HARNESS / "review/references.bib")
        self.assertIn("takehi2026wsp", bib)
        from harness_factory import cycle
        entry = next((c for c in cycle.cycles() if c["id"] == "P72"), None)
        self.assertIsNotNone(entry, "P72 absent from cycles.json")
        self.assertEqual("done", entry["status"])
        self.assertIn("R292", entry["added"]["references"])


class P75RouterMarginTest(unittest.TestCase):
    """P75: the routing margin is visible evidence, and the P31 declared-overlap
    gate now covers the legitimate intersections the P74 assessment found gated
    (bayesian x clinical, review x comparative politics, climate policy,
    behavioral experiments x statistics) while generic-verb collisions
    (认识论 vs 重构) stay gated."""

    def _plan(self, text: str):
        from harness_factory.classify import classify
        from harness_factory.derive import derive
        from harness_factory.spec import TaskSpec

        task = TaskSpec(text=text)
        return derive(task, classify(task))

    def test_classify_json_exposes_routing_margin(self):
        from harness_factory import cli
        import io, contextlib, json as _json

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.main(["classify", "--task", "用贝叶斯方法分析临床试验数据并评估疗效", "--json"])
        self.assertEqual(code, 0)
        payload = _json.loads(buf.getvalue())
        self.assertIn("domain_scores", payload, "R1: routing scores absent from --json")
        self.assertIn("margin", payload)
        self.assertEqual(payload["domain_scores"][0][0], "statistics")
        # text mode names the runner-up too
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            cli.main(["classify", "--task", "用贝叶斯方法分析临床试验数据并评估疗效"])
        self.assertIn("runner-up", buf2.getvalue())

    def test_declared_intersections_are_reported(self):
        cases = [
            ("用贝叶斯方法分析临床试验数据并评估疗效", "medicine"),
            ("写一篇气候政策的比较政治学文献综述", "research"),
            ("为认知实验设计眼动实验并做统计分析", "statistics"),
        ]
        for txt, expected in cases:
            plan = self._plan(txt)
            reported = {e["domain"] for e in plan.secondary_domains}
            self.assertIn(expected, reported,
                          f"{expected} is a declared overlap of the routed domain "
                          f"({plan.features.domain}) but was not reported for {txt!r}")

    def test_union_still_adds_cross_domain_capabilities(self):
        plan = self._plan("写一篇气候政策的比较政治学文献综述")
        added = [c for e in plan.secondary_domains for c in e["added_capabilities"]]
        self.assertIn("empirical-measurement", added,
                      "the P31 union mechanism stopped adding the strong neighbour's capabilities")

    def test_generic_collision_stays_gated(self):
        plan = self._plan("从认识论角度重构论证")
        self.assertEqual(plan.secondary_domains, [],
                         "a generic-verb collision must not surface as a discipline intersection")
        se_only = {"test-first-development"}
        leaked = se_only & set(plan.capabilities)
        self.assertEqual(leaked, set(), "software-engineering capabilities leaked into a philosophy task")


class P76SignalBoundariesTest(unittest.TestCase):
    """P76: short-acronym signals need word-END boundaries (ci matched
    'citations', putting devops on a literature-review task), with plural
    tolerance (bugs still matches bug); the R1 routing note reaches the
    emission only on narrow wins (wide wins stay silent)."""

    def test_acronym_boundary_matrix(self):
        from harness_factory.classify import _sig_hit

        cases = [
            ("ci", "ci pipeline runs green", True),
            ("ci", "literature review with citations", False),
            ("doi", "resolve the doi first", True),
            ("doi", "keep doing this", False),
            ("bug", "fix the bugs", True),
            ("bug", "buggy behavior", False),
            ("bug", "submodule", False),
            ("eeg", "eeg recording", True),
            ("eeg", "eegs", True),
            ("pcb", "pcb design", True),
            ("pcb", "pcbuilder", False),
        ]
        bad = [(s, t, want, _sig_hit(s, t)) for s, t, want in cases if _sig_hit(s, t) != want]
        self.assertEqual(bad, [], f"signal boundary mismatches: {bad}")

    def test_lit_review_runner_up_is_not_devops(self):
        from harness_factory.classify import domain_scores

        scores = domain_scores("write a literature review with citations over several weeks".lower())
        self.assertEqual(scores[0][0], "research")
        self.assertNotIn("devops", [d for d, _ in scores],
                         "the ci/citations false hit must stay dead")

    def test_routing_note_only_on_narrow_wins(self):
        from harness_factory.assemble import build_files
        from harness_factory.classify import classify
        from harness_factory.derive import derive
        from harness_factory.spec import TaskSpec

        def _stanza(text):
            task = TaskSpec(text=text)
            plan = derive(task, classify(task))
            files = build_files(plan)
            return files["AGENTS.md"]

        narrow = _stanza("从认识论角度重构论证")
        self.assertIn("Routing note", narrow, "a margin-1 win must surface the runner-up")
        self.assertIn("software-engineering", narrow)
        wide = _stanza("design a poster series with a distinct visual identity")
        self.assertNotIn("Routing note", wide, "a wide win must stay silent (no noise)")


class P80ModelAxisTrialTest(unittest.TestCase):
    """P80: the receipt model axis (P79.R4) lands end-to-end — harvest --model
    writes trace.model={id,surface} (the R288/HAL model-x-scaffold idiom) — and
    the citation-resolution discriminative instance is registered as done with
    both arms' numeric results."""

    def test_model_axis_roundtrip(self):
        from harness_factory import trace

        line = trace.make_trace(
            "task_outcome", project="p//test", task="t", harness="h",
            model={"id": "glm-5.3-flash (zai-start-plan)", "surface": "zcode-session"},
            detail={"judge": "machine", "score": 1.0, "scale": [0, 1]},
        )
        self.assertEqual(line["model"]["id"], "glm-5.3-flash (zai-start-plan)")
        self.assertEqual(line["model"]["surface"], "zcode-session")
        # and without the flag the axis is absent (never guessed)
        bare_line = trace.make_trace(
            "task_outcome", project="p//test", task="t", harness="h",
            detail={"judge": "machine", "score": 1.0, "scale": [0, 1]},
        )
        self.assertNotIn("model", bare_line, "the model axis must be explicit, never inferred")

    def test_citation_resolution_family_registered_done(self):
        data = json.loads((HARNESS / "src/harness_factory/data/battery.json")
                          .read_text(encoding="utf-8"))
        fam = next(f for f in data["families"] if f["task_id"] == "citation-resolution")
        self.assertEqual(fam["status"], "done")
        self.assertEqual(fam["results"], {"A-bare": 0.0, "B-harness": 1.0})
        self.assertEqual(fam["round"], "P80")
        self.assertIn("updates/dogfood/p80-citation-resolution", fam["trial_projects"])
        self.assertIn("v1 (window-grab bug", fam["notes"], "the judge-erratum trail must be recorded in the registry")


class P77TrendWeeklyTest(unittest.TestCase):
    """P77: the trend pipeline upgrades (per-cluster discriminator scoring,
    per-source cap, hex-noise penalty, weekly delta) and the weekly review
    model. The review guard globs the LATEST dated review so the weekly
    cadence never breaks the suite."""

    def test_cluster_scores_discriminate(self):
        from harness_factory.trend import _cluster_score

        harness_item = {"relevance": 1.0, "title": "Agent harness context engineering"}
        industry_item = {"relevance": 1.0, "title": "Frontier lab funding round closes"}
        self.assertGreater(
            _cluster_score(harness_item, "harness", {"agent-harness"}),
            _cluster_score(industry_item, "harness", set()),
            "harness vocabulary must win the harness cluster over a generic industry item",
        )

    def test_hex_hash_titles_are_penalized(self):
        from harness_factory.trend import _cluster_score

        noisy = {"relevance": 2.0, "title": "fix(ui): localize skill 9a3ae43f5602"}
        clean = {"relevance": 2.0, "title": "fix(ui): localize skill strings"}
        self.assertLess(_cluster_score(noisy, "harness", set()),
                        _cluster_score(clean, "harness", set()))

    def test_top_rows_cap_per_source(self):
        from collections import Counter

        from harness_factory.trend import aggregate

        firehose = [
            {"title": f"agent eval paper {i}", "topics": ["agent-harness"],
             "entity_name": "arXiv cs.CL (new)", "published": "2026-11-0%d" % (i + 1),
             "relevance": 2.0, "url": "https://x/%d" % i}
            for i in range(6)
        ] + [
            {"title": "harness release notes", "topics": ["agent-harness"],
             "entity_name": "A Blog", "published": "2026-11-01",
             "relevance": 1.0, "url": "https://y"},
        ]
        model = aggregate(firehose, top=15, now="2026-11-07")
        tops = model["clusters"]["harness"]["top"]
        per_source = Counter(t.get("entity_name") for t in tops)
        self.assertLessEqual(max(per_source.values()), 3, "one firehose must not monopolize the top")

    def test_committed_snapshot_carries_weekly_delta(self):
        snap = json.loads((HARNESS / "src/harness_factory/data/trend-snapshot.json")
                          .read_text(encoding="utf-8"))
        for pack in snap["clusters"].values():
            self.assertIn("delta", pack, "weekly movement must be recorded per cluster")
            self.assertTrue({"count", "recent", "since"} <= set(pack["delta"]))

    def test_latest_weekly_review_has_the_full_structure(self):
        reviews = sorted((HARNESS / "review").glob("trend-review-*.md"))
        self.assertTrue(reviews, "no trend review exists")
        latest = _read(reviews[-1])
        for part in ("本周信号", "行业全景", "Harness 文献综述", "新兴方向",
                     "分析与预测", "行动项", "方法与数据附录", "溯源表"):
            self.assertIn(part, latest, f"{reviews[-1].name} lost {part!r}")
        # weekly model discipline: reversal conditions + provenance dates
        self.assertIn("反转条件", latest, "every thesis must carry a reversal condition")
        self.assertIn("访问日期", latest, "the provenance table must carry access dates")
        # dialectics: at least one explicit counter-example section marker
        self.assertIn("辩证", latest)


class P73CognitiveLearningTest(unittest.TestCase):
    """P73 integrated Dupoux, LeCun & Malik (arXiv:2603.15381, R293) - a
    cognitive-science critique of static AI learning plus the A-B-M tri-system /
    Evo-Devo scaffolding blueprint.  The harness-level landing is core/03 M2.15
    (epistemic meta-control: switch between observation and action on surprise).
    Content-presence guards only: the paper's foundational model-training scope
    is NOT implemented here (M0.4 / P15 boundary) - no JEPA trainer, no world
    model, no simulator.  Nothing is asserted as this factory's own capability.
    """

    def test_r293_registered_in_references(self):
        text = _read(HARNESS / "review/references.md")
        self.assertIsNotNone(text)
        self.assertIn("## AH.", text, "\u00a7AH group missing")
        for token in ("R293", "Why AI systems don't learn", "arXiv:2603.15381",
                      "Dupoux", "LeCun", "Malik"):
            self.assertIn(token, text, f"{token!r} missing from references.md")
        self.assertIn("R293: **2026-11-05**", text, "\u00a7AH access-date header missing")
        self.assertIn("R1\u2013R295", text, "\u4e2d\u6587\u901f\u89c8 range not reconciled to R293")

    def test_r293_in_bibtex(self):
        bib = _read(HARNESS / "review/references.bib")
        self.assertIsNotNone(bib)
        self.assertIn("dupoux2026whyaidontlearn", bib)
        self.assertIn("2603.15381", bib)

    def test_core03_epistemic_metacontrol_clause_anchored(self):
        text = _read(HARNESS / "core/03-long-running-agents.md")
        self.assertIsNotNone(text)
        self.assertIn("M2.15", text)
        self.assertIn(
            "Epistemic meta-control: dynamically switch between observation and action (M2.15)",
            text, "M2.15 title missing")
        self.assertIn("R293", text, "M2.15 unsourced")
        self.assertIn("pragmatic", text.lower())
        self.assertIn("epistemic", text.lower())
        self.assertIn("(M2.15)", text.split("## Checklist")[1], "no M2.15 checklist row")
        self.assertIn("Blind pragmatic looping", text, "M2.15 anti-pattern missing")
        # the foundational-training scope is explicitly NOT claimed (M0.4 / P15)
        self.assertNotIn("JEPA training loop implemented", text)

    def test_source_map_m215_row(self):
        text = _read(HARNESS / "sources/source-map.md")
        self.assertIsNotNone(text)
        m215 = [ln for ln in text.splitlines() if "M2.15" in ln]
        self.assertTrue(m215, "no M2.15 row in source-map.md")
        self.assertIn("R293", m215[0], "M2.15 source-map row missing R293 provenance")

    def test_survey_cognitive_autonomous_learning(self):
        survey = _read(HARNESS / "review/cognitive-autonomous-learning-2026-11.md")
        self.assertIsNotNone(survey, "P73 survey body missing")
        for token in ("System A", "System B", "System M", "Evo-Devo",
                      "2603.15381", "R293", "epistemic"):
            self.assertIn(token, survey, f"survey missing {token!r}")
        # boundary honored: no base-model training fabricated
        self.assertIn("No model training fabrication", survey)

    def test_watchlist_self_evolving_widened_for_metacontrol(self):
        data = json.loads((HARNESS / "src/harness_factory/data/watchlist.json").read_text(encoding="utf-8"))
        se = next(t for t in data["topics"] if t["id"] == "self-evolving-agents")
        joined = " ".join(se["queries"] + se["keywords"]).lower()
        for token in ("meta-control", "epistemic", "autonomous learning"):
            self.assertIn(token, joined, f"self-evolving-agents probe not widened with {token!r}")

    def test_survey_wired_into_dashboard(self):
        from harness_factory import pages
        rels = [r for (_zh, _en, r) in pages.ARTICLES]
        self.assertIn("cognitive-autonomous-learning-2026-11.md", rels,
                      "P73 survey not surfaced on the related-articles dashboard")

    def test_p73_registered_in_cycle_ledger(self):
        from harness_factory import cycle
        entry = next((c for c in cycle.cycles() if c["id"] == "P73"), None)
        self.assertIsNotNone(entry, "P73 absent from cycles.json")
        self.assertEqual("done", entry["status"])
        self.assertIn("M2.15", entry["added"]["clauses"])
        self.assertIn("R293", entry["added"]["references"])


class P67EvalEcosystemTest(unittest.TestCase):
    """P67: evaluator independence and scope non-transferability."""

    def test_m318a_has_evaluator_independence(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        for token in ("evaluator independence", "[R283]", "CoT trace access"):
            self.assertIn(token, text, f"M3.18(a) lost {token!r}")

    def test_m319_has_scope_declaration(self):
        text = _read(HARNESS / "core/04-verification-and-gates.md")
        self.assertIn("Scope must also be declared", text, "M3.19 scope non-transferability missing")

    def test_references_have_group_AF(self):
        refs = _read(HARNESS / "review/references.md")
        self.assertIn("## AF.", refs)
        for ref in ("R283", "R284", "R285"):
            self.assertIn(ref, refs)
        bib = _read(HARNESS / "review/references.bib")
        for key in ("chen2026emerging", "deepmind2026conjecture"):
            self.assertIn(key, bib)


if __name__ == "__main__":
    unittest.main()
