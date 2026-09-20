"""Grounded extractive-answer node (Qasper/BenchQA contract).

The survey graph answers *about* a paper; factoid QA (Qasper's dominant type)
asks the paper itself. This node turns one parsed paper into a terse, fully
cited answer — "answer the question, not the paper".

Kept deliberately small (single LLM call over the target paper markdown):
the benchmark QA scorer (`correctness`/`groundedness`) is the external check,
and the L6-style gates here are deterministic (citation present, non-empty).
"""

from typing import List

from tools.llm.client import LLMClient, Message
from tools.pipeline.corpus import md_path_for

_ANSWER_PROMPT = (
    "You are an evidence-extraction engine, not a survey writer.\n"
    "Answer the user's question STRICTLY from the provided source paper. Rules:\n"
    "1. Answer the exact question asked; if the paper does not state the answer, "
    "say so explicitly (no invention, no inference).\n"
    "2. Quote exact figures, metric names, and terms from the source.\n"
    "3. Cite the source inline as (arXiv:{paper_id}) at every factual claim.\n"
    "4. Under 250 words. Output as:\n"
    "## Answer (EN)\n<answer>\n\n## 中文速览\n<short Chinese version>\n\n"
    "## Source evidence\n<1-2 verbatim sentences from the paper supporting the answer>"
)


_YESNO_TAIL = (
    "5. This is a yes/no/maybe question. After the evidence, give a single "
    "conclusive line, exactly one of: 'Final decision: yes', 'Final decision: no', "
    "or 'Final decision: maybe' — no hedging, no alternatives."
)


def answer_question(
    client: LLMClient,
    question: str,
    paper_id: str,
    md: str,
    max_chars: int = 40_000,
    mode: str = "",
) -> str:
    """Return a grounded extractive answer for `question` from the paper markdown.

    `mode="yesno"` appends a strict yes/no/maybe conclusion instruction
    (PubMedQA-style questions).
    """
    prompt = _ANSWER_PROMPT.format(paper_id=paper_id)
    if mode == "yesno":
        prompt = _ANSWER_PROMPT.format(paper_id=paper_id) + "\n" + _YESNO_TAIL
    out = client.chat(
        [
            Message(role="system", content=prompt),
            Message(role="user",
                    content=f"Question: {question}\n\nSource paper:\n{md[:max_chars]}"),
        ],
        json_mode=False,
        max_tokens=800,
    )
    return out.text.strip()


def check_answer(answer: str, paper_id: str, require_cite: bool = True) -> dict:
    """Deterministic L6-style gate for the qa answer artifact."""
    errs: List[str] = []
    if not answer or len(answer) < 40:
        errs.append("output too short")
    if require_cite and paper_id and not answer.lower().count(f"arxiv:{paper_id}".lower()):
        errs.append("missing inline arXiv cite")
    ok = not errs
    return {
        "passed": ok,
        "score": 1.0 if ok else 0.0,
        "error": "; ".join(errs) if errs else "",
        "n_papers_cited": 1 if ok else 0,
        "cites": [f"arXiv:{paper_id}"] if paper_id else [],
        "verbatim_quotes": 1 if "## Source evidence" in answer else 0,
    }