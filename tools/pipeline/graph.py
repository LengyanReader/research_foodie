"""
Minimal LangGraph pipeline skeleton for research_foodie.

Architecture mirrors established open research-agent frameworks:
  * S_lit      — live discovery rails (OpenResearch/orx CLI + arXiv API, with a
                 local SEED manifest fallback) — see tools.pipeline.corpus.
  * S_org      — taxonomy + STORM-style outline (Stanford OVAL STORM:
                 question-driven outline, sections + key_points) from evidence.
  * S_write    — claim plan over the FULL paper text (PaperQA2-style
                 evidence-backed claims: claim + verbatim quote + section +
                 cite) then an outline-driven bilingual draft (STORM co-writer).
  * S_final    — assembled structured output.
  * L6 gate    — deterministic, mechanical validation (no LLM) — blueprint §3.
  * P3 judge   — DAS-Bench-style AI rubric review of the final draft
                 (tools.pipeline.judge), running after the mechanical gate.

State machine (mirrors blueprint §3.2; skeleton keeps the graph convergent):
    S_lit → S_org → S_write → (review) → S_final → gate → judge
                           └─ revise_para → S_write  (targeted re-entry)
The blueprint's *proactive* stale → S_lit re-discovery loop is intentionally
NOT wired in the skeleton to avoid unbounded loops; stale verdicts converge to
S_final (with the stale flag) and re-discovery is a P4 addition.

All LLM calls go through tools.llm.client.LLMClient — swap backends freely
(opencode CLI free model, any OpenAI-compatible API, or mock).

Usage:
    from tools.pipeline.graph import Pipeline
    from tools.llm.client import LLMClient
    c = LLMClient(backend="opencode")
    p = Pipeline(c)
    result = p.run(question="GPT detectors bias against non-native writers")
    #  pre-parsed mode:   p.run("liang2023", parsed_md)
    #  live discovery:    p.run(question=..., discovery_backend="arxiv")
    print(result["validation"])   # L6 gate + P3 judge report

No external deps beyond langgraph + stdlib.
"""
from __future__ import annotations

import json
import re
import time
from typing import Dict, Any, Optional, List

from tools.llm.client import LLMClient, Message
from tools.pipeline.state import PipelineState
from tools.pipeline.corpus import discover, resolved_evidence
from tools.pipeline.rerank import select_windows
from tools.pipeline.validate import (
    validate,
    grounded_claims,
    ARXIV_RE,
    parse_json_list,
    parse_json_dict,
)

MAX_SOURCE_CHARS = 20000  # full paper text budget given to the claim-plan step


class Pipeline:
    """Stateful research pipeline built on LangGraph."""

    def __init__(
        self,
        client: LLMClient,
        max_revisions: int = 3,
        judge_client: Optional[LLMClient] = None,
    ):
        self.client = client
        self.judge_client = judge_client or client
        self.max_revisions = max_revisions
        self.graph = self._build()

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------

    def _build(self):
        from langgraph.graph import StateGraph, END

        g = StateGraph(PipelineState)  # typed schema; iteration is an accumulator channel

        g.add_node("lit", self._lit)
        g.add_node("org", self._org)
        g.add_node("write", self._write)
        g.add_node("revise_para", self._revise_para)
        g.add_node("finalize", self._finalize)
        g.add_node("gate", self._gate)
        g.add_node("judge", self._judge)

        g.set_entry_point("lit")
        g.add_edge("lit", "org")
        g.add_edge("org", "write")
        g.add_conditional_edges(
            "write",
            self._review,
            {"pass": "finalize", "revise": "revise_para", "stale": "finalize"},
        )
        g.add_edge("revise_para", "write")
        g.add_edge("finalize", "gate")
        g.add_edge("gate", "judge")
        g.add_edge("judge", END)

        return g.compile()

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------

    def _lit(self, state: Dict[str, Any]) -> Dict:
        """Evidence discovery — split parsed markdown into chunks."""
        md = state.get("parsed_md", "")
        chunks = [p.strip() for p in md.split("\n\n") if p.strip()]
        return {"evidence_chunks": chunks}

    def _org(self, state: Dict[str, Any]) -> Dict:
        """Taxonomy + STORM-style outline (question-driven sections/key_points).

        S_org now reads a cross-paper evidence window: primary paper chunk
        block + one block from the second source, so taxonomy/outline reflect
        the whole evidence pool, not just the top paper.
        """
        papers = state.get("papers") or []
        chunks: List[str] = []
        for idx, p in enumerate(papers[:2]):
            md = p.get("md", "")
            block = [c.strip() for c in md.split("\n\n") if c.strip()]
            want = 5 if idx == 0 else 2      # primary dominates, secondary adds breadth
            chunks.extend(block[:want])
        context = "\n---\n".join(chunks)[:2000]
        question = state.get("question", "")
        resp = self.client.chat(
            [
                Message(role="system",
                        content="Extract 2-5 topics as JSON {\"topics\":[str]}. Be terse."),
                Message(role="user",
                        content=f"Paper: {state.get('paper_id','')}\n\n{context}"),
            ],
            json_mode=True,
            max_tokens=256,
        )
        obj = parse_json_dict(resp.text) or {}
        topics = obj.get("topics")
        if not isinstance(topics, list) or not topics:
            topics = ["general"]

        # L-2 perspective rail (STORM-inspired, prompt-only): enumerate the
        # reader perspectives the survey must serve, then let the outline
        # cover them. Parse failure → [] (outline proceeds, no harm).
        q = question or f"What does {state.get('paper_id','')} establish?"
        rp = self.client.chat(
            [
                Message(role="system",
                        content=("Propose 3-5 distinct reader perspectives whose "
                                 "information needs a survey on this question "
                                 "must cover, as JSON {\"perspectives\":[str]}. "
                                 "Each entry names a reader role plus its "
                                 "concern (e.g. 'practitioner: deployability'). "
                                 "Anchor on the question; be terse.")),
                Message(role="user",
                        content=f"Question: {q}\n\nExcerpt:\n{context}"),
            ],
            json_mode=True,
            max_tokens=220,
        )
        op = parse_json_dict(rp.text) or {}
        raw_persp = op.get("perspectives")
        perspectives = [str(p).strip() for p in raw_persp
                        if isinstance(p, (str, int)) and str(p).strip()][:5] \
            if isinstance(raw_persp, list) else []

        # STORM-style outline rail: thesis + sections + key_points, grounded
        # in the evidence window and the research question; L-2 makes the
        # outline answer every reader perspective enumerated above.
        r2 = self.client.chat(
            [
                Message(role="system",
                        content=("Extract a research outline that answers the "
                                 "question, as JSON {\"thesis\":str,\"sections\":"
                                 "[{\"heading\":str,\"key_points\":[str]}]}. "
                                 "4-6 sections (survey depth); every key_point is "
                                 "one evidence-backed finding from the excerpt.")),
                Message(role="user",
                        content=(f"Question: {q}\n"
                                 + (f"Perspectives to cover: {'; '.join(perspectives)}\n"
                                    if perspectives else "")
                                 + f"\nExcerpt:\n{context}")),
            ],
            json_mode=True,
            max_tokens=500,
        )
        outline = parse_json_dict(r2.text)
        sections = outline.get("sections") if isinstance(outline, dict) else None
        if not isinstance(sections, list) or not sections:
            outline = {"thesis": q, "sections": [{"heading": "Overview",
                                                    "key_points": [q]}]}
        return {"taxonomy": {"topics": topics}, "outline": outline,
                "perspectives": perspectives}

    def _write(self, state: Dict[str, Any]) -> Dict:
        """Per-paper claim plans → merged evidence-backed claims → draft.

        Multi-paper S_write (Session 12): one claim-plan extraction per source
        paper (≤3), each grounded against ITS OWN markdown before merge — this
        is what makes each arXiv ID in the output traceable to a real local
        parse instead of a single-paper summary.
        """
        papers = state.get("papers") or []
        paper_id = state.get("paper_id", "")

        # L-1 relevance re-rank query: the question + every outline key point,
        # so claim extraction sees the *relevant* passages of a long paper
        # instead of its raw first 20 000 chars. Grounding checks below still
        # verify quotes against the FULL paper md (no gate weakening).
        o_outline = state.get("outline", {}) or {}
        o_secs = o_outline.get("sections") if isinstance(o_outline, dict) else []
        key_points = " ".join(
            kp for s in (o_secs or []) if isinstance(s, dict)
            for kp in (s.get("key_points") or []) if isinstance(kp, str)
        )
        rk_query = f"{state.get('question', '')} {key_points}".strip()
        winlog: List[Dict] = []

        claims: List[Dict] = []
        dropped: List[Dict] = []
        for p in papers[:3]:
            md = p.get("md", "")
            pid = p.get("arxiv_id", paper_id)
            try:
                source, wmeta = select_windows(md, rk_query, MAX_SOURCE_CHARS)
            except Exception as e:  # noqa: BLE001 — fallback = pre-L-1 slice
                source = md[:MAX_SOURCE_CHARS]
                wmeta = {"mode": "raw", "error": type(e).__name__}
            wmeta = dict(wmeta, paper_id=pid)
            winlog.append(wmeta)
            r = self.client.chat(
                [
                    Message(role="system",
                            content=("Extract up to 4 evidence-backed claims as a JSON "
                                     "list [{\"id\":str,\"claim\":str,\"quote\":str,"
                                     "\"section\":str,\"cite\":str,"
                                     "\"confidence\":str(high|medium|low)}]. "
                                     "Only output claims you can copy an EXACT "
                                     "verbatim `quote` for from the paper text (≤25 "
                                     "words); if in doubt include fewer claims. "
                                     "quote MUST be copied verbatim; section = the "
                                     "heading that the quote appears under; "
                                     "cite = the arXiv ID, e.g. 'arXiv:2304.02819'.")),
                    Message(role="user",
                            content=f"Paper ID: {pid}\n\n{source}"),
                ],
                json_mode=True,
                max_tokens=600,
            )
            cs = parse_json_list(r.text)
            kept, dr = grounded_claims(cs, md)
            for c in kept:
                cite = (c.get("cite") or "").strip()
                m = ARXIV_RE.search(cite) if cite else None
                if m:
                    c["cite"] = "arXiv:" + m.group(0).lstrip("arXiv:").strip()
                c["paper_id"] = pid
                c["source"] = p.get("label", pid)
            claims.extend(kept)
            dropped.extend(dr)

        # --- per-section survey drafting (Session 13: survey-depth S_write) ---
        # Intro + one independent grounded paragraph per outline section +
        # conclusion = multi-paragraph, cross-paper, survey-grade artifact
        # (attacks the DAS-16 TSQ / MAR / Citation-Balance drag).
        outline = state.get("outline", {})
        sections = outline.get("sections") if isinstance(outline, dict) else []
        sections = [s for s in sections if isinstance(s, dict) and s.get("heading")][:6]
        headings = " | ".join(s.get("heading", "") for s in sections) or "general"
        topics = state.get("taxonomy", {}).get("topics", ["general"])
        sources_line = "; ".join(
            f"arXiv:{p.get('arxiv_id','')} ({p.get('label','')})"
            for p in papers
        ) or paper_id
        claims_snippet = json.dumps(claims, ensure_ascii=False)
        thesis = (outline.get("thesis") if isinstance(outline, dict) else "") or (state.get("question") or paper_id)

        helpers = {
            "intro": (
                "Write the INTRO of a bilingual (EN + 中文) research survey "
                "grounded in the sources: 2-3 sentences framing the question and "
                "thesis; then the roadmap sentence listing the sections. "
                "Cite inline (arXiv:id) where the framing leans on a source."
            ),
            "body": (
                "Write ONE section of a bilingual (EN + 中文) research survey. "
                "Use ONLY the claims below that match this section; write 150-300 "
                "words as 2-3 solid paragraphs (not bullets). Attribute EVERY "
                "factual sentence inline to its arXiv ID (e.g. (arXiv:2304.02819)) "
                "matching each claim's cite. Synthesize across the sources: where "
                "they agree cite both; where they conflict, name the disagreement "
                "explicitly; close with the open gap this leaves. Keep EN + 中文 "
                "faithful; do not invent facts or cites."
            ),
            "conclusion": (
                "Write the CONCLUSION of a bilingual (EN + 中文) research survey: "
                "synthesize the key takeaways across the sections, state the "
                "remaining gaps, cite inline (arXiv:id) where it leans on a source."
            ),
        }

        def _render(kind: str, heading: str = "", keys: str = "") -> str:
            return self.client.chat(
                [
                    Message(role="system",
                            content=helpers[kind] + (
                                " Output ONLY the section text; prefix it with "
                                "the heading line '## <heading>'." if kind == "body" else "")),
                    Message(role="user",
                            content=(f"Section: {heading}\nKey points: {keys}\n"
                                     if kind == "body" else "")
                                    + f"Sources: {sources_line}\n"
                                    + f"Thesis: {thesis}\n"
                                    + f"Claims: {claims_snippet}"),
                ],
                max_tokens=520 if kind == "body" else 320,
            ).text.strip()

        parts = [_render("intro")]
        parts += [_render("body", s.get("heading", ""),
                          "; ".join(s.get("key_points", []))) for s in sections]
        parts.append(_render("conclusion"))
        draft = "\n\n".join(p for p in parts if p)
        return {
            "claims": claims,
            "draft": draft,
            "dropped_claims": dropped,
            "source_windows": winlog,  # L-1 provenance: what the extractor saw
            "iteration": 1,  # accumulator channel: +1 per write visit
        }

    def _revise_para(self, state: Dict[str, Any]) -> Dict:
        """Targeted revision — improve an existing draft."""
        draft = state.get("draft", "")
        claims = state.get("claims", [])
        claims_snippet = json.dumps(claims[:3], ensure_ascii=False)
        r = self.client.chat(
            [
                Message(role="system",
                        content="Improve this draft: expand, make bilingual, add specificity. Output only the improved draft."),
                Message(role="user",
                        content=f"Current draft:\n{draft}\n\nSupporting claims: {claims_snippet}"),
            ],
            max_tokens=500,
        )
        return {"draft": r.text}

    def _finalize(self, state: Dict[str, Any]) -> Dict:
        """Assemble the final structured *manuscript* output.

        The artifact is a complete manuscript in Markdown: Title → Abstract →
        body sections (the survey draft) → evidence table → references, plus an
        audit annex (sources / outline / claims). MAR-relevant components
        (abstract, table, references) give the benchmark judge something to
        score; the same Markdown is what `render_manuscript` turns into PDF.
        """
        paper_id = state.get("paper_id", "")
        papers = state.get("papers") or []
        topics = state.get("taxonomy", {}).get("topics", [])
        claims = state.get("claims", [])
        draft = state.get("draft", "")
        outline = state.get("outline", {})
        sections = outline.get("sections") if isinstance(outline, dict) else []
        outline_lines = "\n".join(
            f"- {s.get('heading','')}: {'; '.join(s.get('key_points', []))}"
            for s in sections if isinstance(s, dict)
        )
        multi = len(papers) > 1
        source_lines = "\n".join(
            f"- arXiv:{p.get('arxiv_id','')} — {p.get('label','')}"
            for p in papers
        ) or f"- {paper_id} (pre-parsed input)"

        question = state.get("question") or paper_id
        title = question.strip()[:90] or paper_id

        intro = draft.split("\n\n", 1)[0] if draft else ""
        abstract = (intro[:800] or "No abstract available.").rstrip()

        # Q&A digest — the default 干货 frame: the main question, a one-line
        # answer pointer, the sub-questions (outline perspectives) and the
        # evidence-card counts behind each. Purely an index over already-grounded
        # content (no new model calls); the claims list below are the cards.
        ans_one = " ".join(abstract.strip().split())[:220] if abstract else "(no abstract)"
        qlines = [
            "## Q&A Digest (问答速览)",
            f"- **Q 研究问题**: {question}",
            f"- **A 一句话答案**: {ans_one}",
            "- **子问题（写作视角）** → 证据卡片见 Claims：",
        ]
        for s in sections if isinstance(sections, list) else []:
            if isinstance(s, dict) and s.get("heading"):
                kp = "; ".join(s.get("key_points", []))
                qlines.append(f"  - **{s['heading']}** — {kp}")
        qlines.append(f"- **证据卡片**: {len(claims)} 条声明，逐条带 paper_id（arXiv:xxxx）可溯源 → Sources {len(papers)} 篇")
        qa_digest = "\n".join(qlines)

        def _claim_arxiv(c: Dict[str, Any]) -> Optional[str]:
            pid = c.get("paper_id")
            if isinstance(pid, str) and pid:
                m = re.search(r"[\d]{4}\.[\d]{4,5}", pid)
                if m:
                    return m.group(0)
            m = re.search(r"arXiv:(\d{4}\.\d{4,5})", str(c.get("cite", "")))
            return m.group(1) if m else None

        table_rows = []
        for i, c in enumerate(claims[:12], 1):
            txt = (c.get("claim") or c.get("text") or "").replace("|", "/").strip()
            txt = (txt[:120] + "…") if len(txt) > 120 else txt
            cid = _claim_arxiv(c)
            source = f"arXiv:{cid}" if cid else (c.get("paper_id") or "?")
            conf = c.get("confidence", "?")
            table_rows.append(f"| {i} | {txt} | {source} | {conf} |")
        if table_rows:
            table = (
                "| # | Claim (abridged) | Source | Confidence |\n"
                "|---|--------------------|--------|------------|\n"
                + "\n".join(table_rows)
            )
        else:
            table = "_No claims extracted._"

        ref_ids: List[str] = []
        for c in claims:
            cid = _claim_arxiv(c)
            if cid and cid not in ref_ids:
                ref_ids.append(cid)
        for p in papers:
            pid2 = p.get("arxiv_id", "")
            if pid2 and pid2 not in ref_ids:
                ref_ids.append(pid2)
        refs = "\n".join(
            f"- [[{i}]](https://arxiv.org/abs/{rid}) arXiv:{rid}"
            for i, rid in enumerate(ref_ids, 1)
        ) or f"- arXiv:{paper_id}"

        lines = [
            f"# {title}",
            f"\n## Abstract\n{abstract}",
            f"\n{qa_digest}",
            f"\n## Intro\n{draft}",
            f"\n## Evidence Table\n{table}",
            f"\n## References\n{refs}",
            f"\n## Sources ({len(papers)})\n{source_lines}" if source_lines else "",
            f"\n## Outline\n{outline_lines}" if outline_lines else "",
            f"\n## Claims ({len(claims)})",
        ]
        for c in claims[:6]:
            conf = c.get("confidence", "?")
            txt = c.get("claim", c.get("text", ""))
            cite = c.get("cite", "")
            tag = f" [{c.get('paper_id', '')}]" if multi else ""
            lines.append(f"- [{conf}]{tag} {txt}  ({cite})")

        manuscript = "\n".join(lines)
        return {"output": manuscript, "manuscript": manuscript}

    # ------------------------------------------------------------------
    # P3 AI judge gate (DAS-Bench-style rubric review)
    # ------------------------------------------------------------------

    def _judge(self, state: Dict[str, Any]) -> Dict:
        """Run the DAS-Bench-style AI judge over the finalized draft."""
        from tools.pipeline.judge import judge_draft
        verdict = judge_draft(state, self.judge_client)
        validation = dict(state.get("validation") or {})
        validation["judge"] = verdict
        return {"validation": validation}

    # ------------------------------------------------------------------
    # Gate (deterministic L6 validation)
    # ------------------------------------------------------------------

    def _gate(self, state: Dict[str, Any]) -> Dict:
        papers = state.get("papers") or []
        md_all = "\n\n".join(p.get("md", "") for p in papers) or state.get("parsed_md", "")
        report = validate(state, md_all, require_bilingual=True)
        report["n_papers_cited"] = report.get("n_papers_cited", 0) or 0
        report["papers"] = [p.get("arxiv_id", "") for p in papers]
        return {"validation": report}

    # ------------------------------------------------------------------
    # Conditional edge
    # ------------------------------------------------------------------

    def _review(self, state: Dict[str, Any]) -> str:
        it = state.get("iteration", 0)
        if it > self.max_revisions:
            return "stale"
        claims = state.get("claims", [])
        draft = state.get("draft", "")
        if len(claims) >= 1 and len(draft) > 30:
            return "pass"
        return "revise"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        paper_id: Optional[str] = None,
        parsed_md: Optional[str] = None,
        question: Optional[str] = None,
        discovery_backend: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute the full pipeline and return the final state.

        Two entry patterns:
          (a) run("liang2023", parsed_md)  — existing unit-test / pre-parsed mode.
          (b) run(question="GPT detectors bias") — discovery-led: finds a
              candidate via a discovery rail (seed | arxiv | orx, env
              `S_LIT_BACKEND`; overridable via `discovery_backend`), resolves the
              evidence pool (papers with local MinerU parses), then runs the
              graph.
        """
        candidates: List[Dict[str, str]] = []
        papers: List[Dict[str, str]] = []
        if question:
            candidates = discover(question, backend=discovery_backend)
            papers = resolved_evidence(question, limit=3, backend=discovery_backend)
            if not paper_id and papers:
                # primary paper = top resolved evidence
                top = papers[0]
                paper_id = top["arxiv_id"]
                parsed_md = top["md"]
            if not papers:
                # nothing locally available — honest failure
                return {
                    "candidates": candidates,
                    "papers": [],
                    "output": "",
                    "draft": "",
                    "claims": [],
                    "taxonomy": {"topics": []},
                    "outline": {"thesis": "", "sections": []},
                    "validation": {"passed": False, "score": 0.0,
                                   "error": "no parsed corpus for candidate"},
                    "_elapsed": 0.0,
                }
        if not papers and parsed_md:
            # (a) pre-parsed single-paper mode — treated as a 1-paper evidence pool
            papers = [{
                "arxiv_id": paper_id or "unknown",
                "label": paper_id or "pre-parsed input",
                "path": "",
                "md": parsed_md,
            }]
        if not paper_id:
            paper_id = "unknown"
        t0 = time.time()
        state = {
            "paper_id": paper_id,
            "parsed_md": parsed_md or "",
            "papers": papers,
            "question": question or "",
            "candidates": candidates,
            "iteration": 0,
        }
        result = self.graph.invoke(state)
        result["_elapsed"] = time.time() - t0
        result["candidates"] = candidates
        return result
