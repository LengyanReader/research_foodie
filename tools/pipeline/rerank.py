"""L-1 relevance re-rank — lightweight mirror of PaperQA2's RCS (retrieve-and-
score) step (PLAN §8 Phase L, Session 22).

Before this module, S_write fed the claim-extraction LLM the *raw first
≤20 000 chars* of each paper — our worst retrieval gap when the answer sits
mid-paper (measured: QA-3-style cold misses). Here, paragraph windows of each
paper are ranked against the survey question + outline key-points with a
cheap lexical Okapi-BM25 scorer (stdlib only, no embedding model, no network),
and only the top-scoring windows — within the SAME character budget — reach
the extraction call.

Guarantees (the "no harm" fallback in the L-1 acceptance):
  * paper fits the budget  → whole paper, mode "full"   (identical to pre-L-1)
  * query has no tokens    → raw leading slice, mode "raw" (pre-L-1 behavior)
  * nothing matches        → raw leading slice, mode "raw"
  * otherwise              → top windows re-assembled in DOCUMENT ORDER so
    section context stays contiguous; the first block is always kept as the
    title/abstract anchor.

Usage:
    from tools.pipeline.rerank import select_windows
    source, meta = select_windows(md, "watermark detection robustness ...",
                                  budget=20000)
    # meta = {"mode": "bm25"|"full"|"raw", "n_chosen", "n_total", "chars"}
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List, Tuple

from tools.pipeline.validate import _toks  # shared stopword-filtered content tokens

# Okapi parameters — the standard lexical-IR defaults (Robertson et al. 2004);
# no tuning needed at this scale (≤ a few hundred windows per paper).
_K1 = 1.5
_B = 0.75
_MIN_BLOCK = 40  # blocks shorter than this merge into the previous one


def _blocks(md: str) -> List[str]:
    """Paragraph windows from MinerU markdown; tiny fragments merged so a
    stray heading or caption never becomes a degenerate zero-signal window."""
    raw = [b.strip() for b in (md or "").split("\n\n") if b.strip()]
    merged: List[str] = []
    for b in raw:
        if merged and len(b) < _MIN_BLOCK:
            merged[-1] = merged[-1] + "\n" + b
        else:
            merged.append(b)
    return merged


def _bm25(query_toks: List[str], doc_toks: List[List[str]]) -> List[float]:
    """Okapi-BM25 score of every window against the query tokens."""
    n = len(doc_toks)
    if not n or not query_toks:
        return [0.0] * n
    avgdl = sum(len(d) for d in doc_toks) / n or 1.0
    qset = set(query_toks)
    df = Counter()
    for toks in doc_toks:
        for t in qset & set(toks):
            df[t] += 1
    scores: List[float] = []
    for toks in doc_toks:
        tf = Counter(toks)
        dl = len(toks)
        s = 0.0
        for t in qset:
            f = tf.get(t, 0)
            if not f:
                continue
            idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
            s += idf * f * (_K1 + 1) / (f + _K1 * (1 - _B + _B * dl / avgdl))
        scores.append(s)
    return scores


def select_windows(md: str, query: str, budget: int = 20000,
                   anchor_first: bool = True) -> Tuple[str, Dict]:
    """Return (source_text, meta): the top-BM25 paragraph windows of `md`
    against `query`, re-assembled in document order within `budget` chars.

    `meta` is JSON-safe and recorded per paper in the pipeline state
    (`source_windows`) so every run shows *which* windows the extractor saw.
    """
    meta: Dict = {"mode": "raw", "n_chosen": 0, "n_total": 0, "chars": 0,
                  "budget": budget}
    if not md:
        return "", meta
    if len(md) <= budget:
        meta.update(mode="full", n_chosen=1, n_total=1, chars=len(md))
        return md, meta

    blocks = _blocks(md)
    meta["n_total"] = len(blocks)
    qt = _toks(query or "")

    def _raw() -> Tuple[str, Dict]:
        out = md[:budget]
        meta.update(mode="raw", n_chosen=1, chars=len(out))
        return out, meta

    if not qt or not blocks:
        return _raw()

    doc_toks = [_toks(b) for b in blocks]
    scores = _bm25(qt, doc_toks)
    if not any(s > 0 for s in scores):
        return _raw()  # nothing relevant found → keep the old head-slice behavior

    order = sorted(range(len(blocks)), key=lambda i: (-scores[i], i))
    chosen: List[int] = []
    used = 0
    if anchor_first:
        if len(blocks[0]) >= budget:
            meta.update(mode="bm25", n_chosen=1, chars=budget)
            return blocks[0][:budget], meta
        chosen.append(0)
        used += len(blocks[0])
    for i in order:
        if i in chosen or scores[i] <= 0:
            continue  # only relevant windows — filler stays out
        if used + len(blocks[i]) + 2 > budget:
            continue  # try a smaller window that still fits (not strict prefix)
        chosen.append(i)
        used += len(blocks[i]) + 2
    chosen.sort()  # document order → section context preserved
    text = "\n\n".join(blocks[i] for i in chosen)
    meta.update(mode="bm25", n_chosen=len(chosen), chars=len(text))
    return text, meta
