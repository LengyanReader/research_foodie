"""Deterministic L6 validation gate (stdlib-only, no LLM).

Mechanical rigor runs BEFORE any AI judge or human gate (blueprint §3/§5):
  * structure — required state keys present, output length sensible
  * cites     — every claim cites a well-formed arXiv ID (with or without the
                `arXiv:` prefix) or DOI
  * grounding — every claim that carries a `quote` shares a 5-content-token
                sequence with the source (n-gram contiguity) — catches
                hallucinated quotes that paraphrase → no shared n-gram;
                exact verbatim matches reported as a quality metric
  * bilingual — draft contains both CJK and Latin (informational)

The gate only FAILS on structure/cites/grounding. A claim without a `quote`
is reported in `missing_quotes` but does not fail the gate: quote capture is
a model behavior we strengthen in prompts, not a hard mechanical invariant.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

ARXIV_RE = re.compile(r"(?:arXiv\s*:)?\d{4}\.\d{4,5}", re.I)
DOI_RE = re.compile(r"doi\s*:\s*10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)

# Common function words excluded from phrase-level grounding keys.
_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "that", "as", "is", "are", "was", "were", "been", "by", "at", "from",
    "this", "these", "those", "it", "its", "their", "they", "we", "not",
    "but", "while", "which", "who", "can", "may", "be",
}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def _toks(s: str) -> list:
    return [t for t in re.split(r"\W+", _norm(s)) if t and t not in _STOP]


def _contig5(toks: list) -> set:
    return {" ".join(toks[i:i + 5]) for i in range(len(toks) - 4)}


def _wellformed_cite(cite: str) -> bool:
    return bool(ARXIV_RE.search(cite) or DOI_RE.search(cite))


def _unfence(text: str) -> str:
    """Strip a markdown code-fence wrapper around an LLM JSON reply."""
    t = (text or "").strip()
    if t.startswith("```"):
        t = re.sub(r"^```[A-Za-z0-9_\-]*\s*", "", t)
        t = re.sub(r"```\s*$", "", t).strip()
    return t


def parse_json_list(text: str) -> list:
    """Best-effort parse of a JSON list (or {"claims": [...]}) from an LLM reply."""
    import json
    t = _unfence(text)
    try:
        obj = json.loads(t)
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            if isinstance(obj.get("claims"), list):
                return obj["claims"]
            if any(k in obj for k in ("claim", "quote", "cite")):
                return [obj]  # single claim object wrapped by a terse model
    except Exception:
        pass
    m = re.search(r"\[[\s\S]*?\]", t)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, list):
                return obj
        except Exception:
            pass
    return []


def parse_json_dict(text: str) -> Dict[str, Any] | None:
    """Best-effort parse of a JSON object from an LLM reply."""
    import json
    t = _unfence(text)
    try:
        obj = json.loads(t)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass
    m = re.search(r"\{[\s\S]*?\}", t)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return None


def grounded_claims(claims: List[Dict[str, Any]], source_md: str):
    """Deterministic grounding filter used at write time.

    Drops claims whose `quote` shares no 5-content-token sequence with the
    source (mechanical sanitization — hallucinated claims never reach the
    draft). Claims without a `quote` are kept (reported as missing_quotes by
    validate). Returns (kept, dropped).
    """
    src5 = _contig5(_toks(_norm(source_md)))
    kept: List[Dict[str, Any]] = []
    dropped: List[Dict[str, Any]] = []
    for c in claims:
        q = (c.get("quote") or "").strip()
        if q and not (set(_contig5(_toks(q))) & src5):
            dropped.append(c)
        else:
            kept.append(c)
    return kept, dropped


def validate(result: Dict[str, Any], source_md: str, require_bilingual: bool = True) -> Dict[str, Any]:
    """Return a deterministic validation report; `passed` is the gate verdict."""
    checks: Dict[str, Dict[str, Any]] = {}
    fails: List[str] = []
    warnings: List[str] = []

    claims: List[Dict[str, Any]] = result.get("claims", [])
    src = _norm(source_md or "")

    # -- structure ---------------------------------------------------------
    missing = [k for k in ("output", "claims", "taxonomy", "draft") if k not in result]
    out_len = len(result.get("output", ""))
    ok = not missing and out_len > 50
    checks["structure"] = {
        "ok": ok,
        "detail": f"missing={missing or 'none'}; output_len={out_len}",
    }
    if not ok:
        fails.append("structure")

    # -- cites ---------------------------------------------------------------
    empty, bad = [], []
    for c in claims:
        cite = (c.get("cite") or "").strip()
        if not cite:
            empty.append(c.get("id", "?"))
        elif not _wellformed_cite(cite):
            bad.append(c.get("id", "?"))
    ok = not empty and not bad
    checks["cites"] = {
        "ok": ok,
        "detail": f"claims={len(claims)} empty_cite={list(empty)} malformed={list(bad)}",
    }
    if not ok:
        fails.append("cites")

    # -- grounding ------------------------------------------------------------
    # Verbatim match is ideal; local 3B models paraphrase, so we gate on a
    # shared 5-content-token sequence (hallucinated claims almost never reuse
    # five contiguous content words), and report exactness as a quality metric.
    src_toks = _toks(src)
    src5 = _contig5(src_toks)
    ungrounded: List[str] = []          # fails the gate (fuzzy)
    not_verbatim: List[str] = []        # quality only
    claims_with_quote = 0
    for c in claims:
        q = (c.get("quote") or "").strip()
        if not q:
            continue  # no quote captured -> not a hard failure
        claims_with_quote += 1
        fid = c.get("id", "?")
        if not (set(_contig5(_toks(q))) & src5):
            ungrounded.append(fid)
        elif _norm(q)[:120] not in src:
            not_verbatim.append(fid)
    ok = not ungrounded
    checks["grounding"] = {
        "ok": ok,
        "detail": (f"claims_with_quote={claims_with_quote} "
                   f"fuzzy_ungrounded={list(ungrounded)} "  # hallucination risk
                   f"paraphrased_not_verbatim={list(not_verbatim)}"),
    }
    if not ok:
        fails.append("grounding")

    # -- bilingual (informational) -------------------------------------------
    draft = result.get("draft", "") or ""
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", draft))
    has_lat = bool(re.search(r"[A-Za-z]", draft))
    if require_bilingual and not (has_cjk and has_lat):
        warnings.append("bilingual")
    checks["bilingual"] = {
        "ok": (has_cjk and has_lat) or not require_bilingual,
        "detail": f"cjk={has_cjk} latin={has_lat}",
    }

    missing_quotes = sum(1 for c in claims if not (c.get("quote") or "").strip())

    # -- multi-paper (informational, Session 12) --------------------------------
    # How many DISTINCT source papers the final claims actually cite. Quality
    # metric against a 1-paper summary; not a hard gate.
    cited_ids: List[str] = []
    for c in claims:
        pid = (c.get("paper_id") or "").strip()
        if pid and pid not in cited_ids:
            cited_ids.append(pid)
            continue
        if not pid:
            m = ARXIV_RE.search(c.get("cite") or "")
            if m:
                ext = m.group(0).lstrip("arXiv:").strip()
                if ext not in cited_ids:
                    cited_ids.append(ext)
    n_avail = len(result.get("papers") or [])
    checks["multi_paper"] = {
        "ok": n_avail <= 1 or len(cited_ids) >= 2,
        "detail": (f"papers_available={n_avail} n_papers_cited={len(cited_ids)} "
                   f"cited={cited_ids or 'none'}"),
    }
    if not checks["multi_paper"]["ok"]:
        warnings.append("multi_paper")

    # -- score (0..1) ----------------------------------------------------------
    n = len(claims)
    if n:
        cite_ok = sum(1 for c in claims if (c.get("cite") or "").strip() and _wellformed_cite(c["cite"])) / n
        src5 = _contig5(_toks(src))
        grd_ok = sum(
            1 for c in claims
            if not (c.get("quote") or "").strip()
            or bool(set(_contig5(_toks(c["quote"]))) & src5)
        ) / n
        score = (cite_ok + grd_ok) / 2.0
    else:
        score = 0.0

    return {
        "passed": not fails,
        "score": score,
        "checks": checks,
        "warnings": warnings,
        "missing_quotes": missing_quotes,
        "n_papers_cited": len(cited_ids),
        "verbatim_quotes": sum(
            1 for c in claims
            if (c.get("quote") or "").strip() and _norm(c["quote"])[:120] in src
        ),
    }