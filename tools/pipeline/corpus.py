"""S_lit (L1 discovery) support — seed corpus + pluggable live backends.

Discovery rails (env `S_LIT_BACKEND`, default **`seed`**):
  * `seed`  — deterministic offline keyword scoring over SEED_MANIFEST. Always
              available; keeps tests stable.
  * `arxiv` — live arXiv API (`export.arxiv.org/api/query`, free, no key) —
              the same backend family OpenResearch/orx `discover keyword` uses.
              Falls back to the seed manifest if the API is unreachable.
  * `orx`   — shell out to the OpenResearch CLI (`orx discover keyword <q>`)
              when the `orx` binary is on PATH (not installed in this env as of
              2026-09-16 — Rust source only in `external/orx`); falls back to
              `arxiv`, then seed.

Every seed ID below was verified against a primary source in `docs/PROGRESS.md`
(2026-09-15); labels are short descriptors, **not** asserted official titles.
The manifest is an honest seed set for the minimal-vertical demo.

Network correction 2026-09-16: export.arxiv.org was measured unreachable on
2026-09-15 (Session 6), but now answers 200 in ~1 s — the live `arxiv` rail is
therefore exercised. `orx` binary still absent.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

ARXIV_API = "https://export.arxiv.org/api/query"

# Each entry: arxiv_id (verified), label (descriptor), keywords (discovery terms).
# Verdiering (verification) ledger: docs/PROGRESS.md Session 1/3.
SEED_MANIFEST: List[Dict[str, str]] = [
    {
        "arxiv_id": "2304.02819",
        "label": "GPT detectors are biased against non-native English writers (Liang et al., Patterns 4(7) 2023)",
        "keywords": "gpt detector bias non-native english writers ai-generated detection",
    },
    {
        "arxiv_id": "2409.13740",
        "label": "Scientific Q&A using agents with toolkit (PaperQA2)",
        "keywords": "paperqa scientific qa agents retraction litqa literature",
    },
    {
        "arxiv_id": "2608.18034",
        "label": "Deep Academic Survey (DAS)",
        "keywords": "das deep academic survey taxonomy claim review benchmark",
    },
    {
        "arxiv_id": "2510.24701",
        "label": "DeepResearch (Tongyi) — open research-agent model",
        "keywords": "deepresearch tongyi research agent model search",
    },
    {
        "arxiv_id": "2306.15666",
        "label": "Weber-Wulff et al. — testing of detection tools for AI-generated text",
        "keywords": "weber-wulff detection tools ai-generated text test",
    },
    {
        "arxiv_id": "1706.03762",
        "label": "Attention is all you need (Vaswani et al. 2017)",
        "keywords": "attention transformer self-attention vaswani sequence",
    },
    {
        "arxiv_id": "1810.04805",
        "label": "BERT: pre-training of deep bidirectional transformers (Devlin et al. 2019)",
        "keywords": "bert pre-training bidirectional transformer devlin nlp",
    },
]


def _tokenize(question: str) -> List[str]:
    return [t for t in re.split(r"\W+", question.lower()) if len(t) > 2]


def discover(question: str, limit: int = 3, backend: Optional[str] = None) -> List[Dict[str, str]]:
    """Candidate discovery over seed manifest + optional live rails.

    `backend` overrides env `S_LIT_BACKEND` (default `seed`). Live rails fall
    back to the seed manifest on any failure so the pipeline never dies on the
    network. Seed scoring stays deterministic → integration tests are stable.
    """
    backend = (backend or os.getenv("S_LIT_BACKEND", "seed") or "seed").lower()
    if backend not in ("seed", "arxiv", "orx"):
        raise ValueError(f"unknown S_LIT_BACKEND: {backend!r} (expected seed | arxiv | orx)")

    live: List[Dict[str, str]] = []
    if backend in ("arxiv", "orx"):
        if backend == "orx" and orx_discover is not None:
            live = list(orx_discover(question)) if shutil.which("orx") else []
        if not live:
            live = fetch_arxiv(question)
    return _merge([live, seed_candidates(question)], limit)


def seed_candidates(question: str, limit: int = 3) -> List[Dict[str, str]]:
    """Deterministic offline discovery over the seed manifest (keyword scoring)."""
    tokens = _tokenize(question)
    if not tokens:
        return []
    scored: List[tuple] = []
    for entry in SEED_MANIFEST:
        hay = f"{entry['label']} {entry['keywords']}".lower()
        score = sum(1 for t in tokens if t in hay)
        if entry["arxiv_id"] in question:
            score += 5
        if score:
            scored.append((score, entry))
    scored.sort(key=lambda x: (-x[0], x[1]["arxiv_id"]))
    return [dict(e) for _, e in scored[:limit]]


_ID_RE = re.compile(r"\b(\d{4}\.\d{4,5})\b")
_TAG_RE = re.compile(r"<[^>]+>")


def fetch_arxiv(question: str, limit: int = 5, timeout: int = 15) -> List[Dict[str, str]]:
    """Live arXiv API discovery (relevance sort) → [{arxiv_id, title, summary}].

    Same free/no-key backend family as OpenResearch/orx `discover keyword`.
    Returns [] on any failure (timeout/DNS) so callers fall back gracefully.
    """
    q = urllib.parse.quote(question)
    url = f"{ARXIV_API}?search_query=all:{q}&start=0&max_results={limit}&sortBy=relevance"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
    except Exception:
        return []
    hits: List[Dict[str, str]] = []
    for entry in re.findall(r"<entry>.*?</entry>", body, flags=re.S):
        ids = _ID_RE.findall(entry)
        if not ids:
            continue
        title_m = re.search(r"<title[^>]*>(.*?)</title>", entry, flags=re.S)
        summ_m = re.search(r"<summary[^>]*>(.*?)</summary>", entry, flags=re.S)
        title = _strip_xml(title_m.group(1)) if title_m else ""
        summary = _strip_xml(summ_m.group(1)) if summ_m else ""
        hits.append({
            "arxiv_id": ids[0],
            "label": title[:160],
            "keywords": f"{title} {summary}".lower()[:1500],
        })
    return hits


def _strip_xml(s: str) -> str:
    return " ".join(re.sub(r"\s+", " ", _TAG_RE.sub(" ", s)).strip().split())


def orx_discover(question: str, timeout: int = 60) -> List[Dict[str, str]]:
    """OpenResearch (orx) CLI discovery — `orx discover keyword <question>`.

    Only used when the `orx` binary is on PATH (env `S_LIT_BACKEND=orx`; not
    present in this dev env as of 2026-09-16). Parsed IDs are best-effort from
    stdout/stderr; any failure → [] (caller falls back to `arxiv`, then seed).
    """
    cmd = ["orx", "discover", "keyword", question]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        blob = f"{proc.stdout} {proc.stderr}"
    except Exception:
        return []
    ids = _ID_RE.findall(blob)
    return [{"arxiv_id": i, "label": "orx discover result", "keywords": question} for i in dict.fromkeys(ids)]


def _merge(groups: List[List[Dict[str, str]]], limit: int) -> List[Dict[str, str]]:
    seen: set = set()
    out: List[Dict[str, str]] = []
    for group in groups:
        for e in group:
            if e["arxiv_id"] not in seen:
                seen.add(e["arxiv_id"])
                out.append(e)
            if len(out) >= limit:
                return out
    return out


# Local parsed-corpus mapping: arxiv_id -> parsed markdown relative to repo root.
# Populated as papers are parsed with MinerU; exact-path resolution from cwd.
CORPUS_MD_DIR = Path("_demo_downloads/mineru_out_ds0509")
_LOCAL_MD: Dict[str, str] = {
    "2304.02819": "liang2023_test/auto/liang2023_test.md",
    # Weber-Wulff et al. 2023, "Testing of detection tools for AI-generated
    # text" — merged from 8 MinerU `-m txt` page-windows (46pp; see PROGRESS
    # Session 10 for the OCR-rec stage 502 flakiness workaround).
    "2306.15666": "weber_wulff_2306_15666/auto/weber_wulff_2306_15666.md",
}


def md_path_for(arxiv_id: str) -> Optional[Path]:
    """Return the local MinerU-parsed markdown for an arXiv ID, if present."""
    rel = _LOCAL_MD.get(arxiv_id)
    if not rel:
        return None
    p = CORPUS_MD_DIR / rel
    return p if p.is_file() else None