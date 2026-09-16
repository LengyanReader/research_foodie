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
import time
from typing import Dict, Any, Optional, List

from tools.llm.client import LLMClient, Message
from tools.pipeline.state import PipelineState
from tools.pipeline.corpus import discover, resolved_evidence
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
    ):
        self.client = client
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

        # STORM-style outline rail: thesis + sections + key_points, grounded
        # in the evidence window and the research question.
        q = question or f"What does {state.get('paper_id','')} establish?"
        r2 = self.client.chat(
            [
                Message(role="system",
                        content=("Extract a research outline that answers the "
                                 "question, as JSON {\"thesis\":str,\"sections\":"
                                 "[{\"heading\":str,\"key_points\":[str]}]}. "
                                 "2-4 sections; every key_point is one "
                                 "evidence-backed finding from the excerpt.")),
                Message(role="user",
                        content=f"Question: {q}\n\nExcerpt:\n{context}"),
            ],
            json_mode=True,
            max_tokens=500,
        )
        outline = parse_json_dict(r2.text)
        sections = outline.get("sections") if isinstance(outline, dict) else None
        if not isinstance(sections, list) or not sections:
            outline = {"thesis": q, "sections": [{"heading": "Overview",
                                                    "key_points": [q]}]}
        return {"taxonomy": {"topics": topics}, "outline": outline}

    def _write(self, state: Dict[str, Any]) -> Dict:
        """Per-paper claim plans → merged evidence-backed claims → draft.

        Multi-paper S_write (Session 12): one claim-plan extraction per source
        paper (≤3), each grounded against ITS OWN markdown before merge — this
        is what makes each arXiv ID in the output traceable to a real local
        parse instead of a single-paper summary.
        """
        papers = state.get("papers") or []
        paper_id = state.get("paper_id", "")

        claims: List[Dict] = []
        dropped: List[Dict] = []
        for p in papers[:3]:
            md = p.get("md", "")
            pid = p.get("arxiv_id", paper_id)
            source = md[:MAX_SOURCE_CHARS]
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

        # --- draft paragraph (STORM co-writer style: outline-driven) ---
        outline = state.get("outline", {})
        sections = outline.get("sections") if isinstance(outline, dict) else []
        headings = " | ".join(
            s.get("heading", "") for s in sections if isinstance(s, dict)
        ) or "general"
        topics = state.get("taxonomy", {}).get("topics", ["general"])
        sources_line = "; ".join(
            f"arXiv:{p.get('arxiv_id','')} ({p.get('label','')})"
            for p in papers
        ) or paper_id
        claims_snippet = json.dumps(claims[:6], ensure_ascii=False)
        r2 = self.client.chat(
            [
                Message(role="system",
                        content=("Write an outline-driven bilingual (EN + 中文) "
                                 "research summary: one short paragraph per "
                                 "outline section. Synthesize across the given "
                                 "source papers; attribute each factual claim "
                                 "inline to its arXiv ID (e.g. (arXiv:2304.02819)) "
                                 "matching the claims. Be precise; do not invent "
                                 "facts.")),
                Message(role="user",
                        content=f"Outline sections: {headings}\nTopics: {', '.join(topics)}\nSources: {sources_line}\nClaims: {claims_snippet}"),
            ],
            max_tokens=700,
        )
        return {
            "claims": claims,
            "draft": r2.text,
            "dropped_claims": dropped,
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
        """Assemble the final structured output (Sources + claim attribution)."""
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
        lines = [
            f"# {paper_id}",
            f"\n## Topics\n{', '.join(topics)}",
            f"\n## Sources ({len(papers)})\n{source_lines}" if source_lines else "",
            f"\n## Outline\n{outline_lines}" if outline_lines else "",
            f"\n## Draft\n{draft}",
            f"\n## Claims ({len(claims)})",
        ]
        for c in claims[:6]:
            conf = c.get("confidence", "?")
            txt = c.get("claim", c.get("text", ""))
            cite = c.get("cite", "")
            tag = f" [{c.get('paper_id', '')}]" if multi else ""
            lines.append(f"- [{conf}]{tag} {txt}  ({cite})")
        return {"output": "\n".join(lines)}

    # ------------------------------------------------------------------
    # P3 AI judge gate (DAS-Bench-style rubric review)
    # ------------------------------------------------------------------

    def _judge(self, state: Dict[str, Any]) -> Dict:
        """Run the DAS-Bench-style AI judge over the finalized draft."""
        from tools.pipeline.judge import judge_draft
        verdict = judge_draft(state, self.client)
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
