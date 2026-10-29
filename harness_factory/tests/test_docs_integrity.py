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
                      "独立重推导", "12 条真实轨迹", "5/5", "0.19"):
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
        self.assertEqual(len(board["families"]), 7, "expected all seven scoreboard families")
        done = [f for f in board["families"] if f["status"] == "done"]
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


if __name__ == "__main__":
    unittest.main()
