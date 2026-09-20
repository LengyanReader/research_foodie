"""OpenResearch-style **parallel autoresearch** orchestrator.

This captures the one capability that is genuinely unique to OpenResearch
(``openresearch.sh`` / alphaXiv): *a single research direction is fanned out
across several independent research threads, each pursued in its own isolated
"worktree", run in parallel, and then merged with its divergences surfaced* —
their tagline "give each research direction its own agent; they work in
parallel, in isolated worktrees".

Our main graph (`tools/pipeline/graph.py`) is the opposite shape: one question →
one sequential survey. So this is not a re-implementation of a rail we already
have (arXiv/STORM/DAS discovery is elsewhere) — it is a genuinely new control
pattern layered *on top* of the existing deterministic primitives:

  * **fan-out**  — ``plan_directions`` derives K orthogonal lenses of the query;
  * **isolation** — each direction gets its own on-disk worktree directory (the
    filesystem analogue of a git worktree; a direction writes *only* there);
  * **parallel** — directions are dispatched concurrently (``ThreadPoolExecutor``);
  * **merge**    — ``merge`` unions the per-direction evidence pools and reports
    which sources each direction uniquely surfaced (the "divergence" signal).

Model-free **by construction**: the whole loop runs on primitives already in the
repo (`corpus.resolved_evidence` + the L6 `validate.grounded_claims` gate) against
the local MinerU-parsed corpus, so the complete autoresearch cycle executes with
**zero LLM and zero API key**. Claims are extractive (verbatim spans of the
source they cite), so they pass the grounding gate by design; a future model lane
would attach at ``run_direction`` (draft each direction) without changing the
orchestration. The OpenResearch ``orx`` CLI itself is not a dependency — the
binary is uninstalled and its free hosted model is credit-gated (see Session 24);
what is imported here is its *method*, faithfully and runnable offline.

Usage:
    $PY -X utf8 -m tools.pipeline.autoresearch "how reliable are AI-text detectors?" \
        --directions 4 [--backend seed|arxiv] [--out _eval_out/autoresearch]
"""
from __future__ import annotations

import argparse
import concurrent.futures as _fx
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.pipeline.corpus import resolved_evidence  # noqa: E402
from tools.pipeline.validate import grounded_claims, _toks  # noqa: E402

DEFAULT_ROOT = REPO / "_eval_out" / "autoresearch"

# The orthogonal lenses a research direction is decomposed into. Kept generic
# (not tuned to any one query) so fan-out is a structural property, not a trick.
FACETS: List[Dict[str, str]] = [
    {"id": "mechanism", "label": "Method / mechanism",
     "cue": "method architecture technique approach model"},
    {"id": "evidence", "label": "Evidence / results",
     "cue": "results accuracy benchmark dataset evaluation performance"},
    {"id": "limits", "label": "Limitations / failure modes",
     "cue": "limitations error bias failure robustness unreliable"},
    {"id": "context", "label": "Prior work / comparison",
     "cue": "compared baseline prior work survey related review"},
    {"id": "impact", "label": "Applications / implications",
     "cue": "application deployment practice implications use cases"},
]


def _slug(text: str, maxlen: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen] or "query"


def _sentences(md: str) -> List[str]:
    """Crude but deterministic sentence split over parsed markdown (paragraph →
    sentence), dropping headings / boilerplate lines."""
    out: List[str] = []
    for para in re.split(r"\n\s*\n", md):
        for sent in re.split(r"(?<=[.!?])\s+", para.strip()):
            s = sent.strip()
            if len(s) >= 40 and not s.startswith(("#", "|", "-", "*")):
                out.append(s)
    return out


def plan_directions(question: str, k: int = 4) -> List[Dict[str, str]]:
    """Fan the query out into K orthogonal research directions (deterministic).

    Each direction is ``question`` narrowed by one facet lens; the facet *cue*
    words steer the downstream lexical retrieval so independent threads can
    surface genuinely different sources (the divergence the merge reports).
    """
    facets = FACETS[:max(1, min(k, len(FACETS)))]
    return [
        {
            "id": f"{i}-{f['id']}",
            "facet": f["label"],
            "subquestion": f"{question} {f['cue']}".strip(),
        }
        for i, f in enumerate(facets)
    ]


def _surface_claims(subquestion: str, paper_md: str, arxiv_id: str, n: int = 3) -> List[Dict[str, str]]:
    """Top-``n`` sentences of the paper most relevant to this direction's
    sub-question, as extractive (verbatim) grounded claims."""
    qtok = set(_toks(subquestion))
    scored = []
    for s in _sentences(paper_md):
        st = _toks(s)
        if not st:
            continue
        overlap = sum(1 for t in st if t in qtok)
        scored.append((overlap / (len(st) ** 0.5), s))  # length-normalised
    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {"claim": s, "quote": s, "cite": f"arXiv:{arxiv_id}"}
        for _, s in scored[:n]
    ]


class Worktree:
    """An isolated per-direction workspace — the filesystem analogue of an
    OpenResearch/git worktree. A direction writes only inside ``dir``."""

    def __init__(self, root: Path, direction_id: str):
        self.dir = root / f"wt-{_slug(direction_id)}"
        self.direction_id = direction_id

    def reset(self) -> "Worktree":
        if self.dir.exists():
            for p in sorted(self.dir.rglob("*"), reverse=True):
                if p.is_file():
                    p.unlink()
        self.dir.mkdir(parents=True, exist_ok=True)
        return self

    def write(self, name: str, content: str) -> Path:
        p = self.dir / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p


def run_direction(run_root: Path, direction: Dict[str, str],
                  backend: str | None = None, limit: int = 3,
                  claims_per_paper: int = 3) -> Dict[str, Any]:
    """Pursue one direction inside its own worktree; return a status summary.

    Deterministic + offline: resolve this direction's evidence pool, surface
    extractive claims per paper, keep only those the L6 grounding gate retains.
    """
    wt = Worktree(run_root, direction["id"]).reset()
    ev = resolved_evidence(direction["subquestion"], limit=limit, backend=backend)
    grounded_total, dropped_total = 0, 0
    for paper in ev:
        cands = _surface_claims(direction["subquestion"], paper["md"],
                                paper["arxiv_id"], claims_per_paper)
        kept, dropped = grounded_claims(cands, paper["md"])
        grounded_total += len(kept)
        dropped_total += len(dropped)
        wt.write(f"claims/{paper['arxiv_id']}.json",
                 json.dumps({"paper": paper["arxiv_id"], "kept": kept,
                             "dropped": dropped}, ensure_ascii=False, indent=2))
    sources = [p["arxiv_id"] for p in ev]
    wt.write("direction.json", json.dumps(
        {"direction": direction, "sources": sources,
         "grounded": grounded_total, "dropped": dropped_total},
        ensure_ascii=False, indent=2))
    lines = [f"# {direction['facet']}", "",
             f"*sub-question:* {direction['subquestion']}", "",
             f"- sources resolved: {len(sources)} ({', '.join(sources) or '—'})",
             f"- grounded claims kept: {grounded_total} (dropped by L6 gate: {dropped_total})", ""]
    for paper in ev:
        cj = wt.dir / "claims" / f"{paper['arxiv_id']}.json"
        if cj.exists():
            kept = json.loads(cj.read_text(encoding="utf-8"))["kept"]
            lines.append(f"## {paper['label']} (`arXiv:{paper['arxiv_id']}`)")
            lines += [f"- {c['quote']}" for c in kept] + [""]
    wt.write("findings.md", "\n".join(lines))
    return {"direction": direction, "sources": sources,
            "grounded": grounded_total, "dropped": dropped_total,
            "worktree": str(wt.dir)}


def merge(results: List[Dict[str, Any]], question: str, run_root: Path) -> Path:
    """Union the isolated directions; surface which sources diverge between them."""
    results = sorted(results, key=lambda r: r["direction"]["id"])  # order-stable
    union: set = set()
    per_dir: Dict[str, set] = {}
    for r in results:
        s = set(r["sources"])
        per_dir[r["direction"]["id"]] = s
        union |= s
    shared = set.intersection(*per_dir.values()) if per_dir else set()
    # unique-to-a-direction = sources NO other direction surfaced (true divergence)
    unique: Dict[str, List[str]] = {}
    for d, s in per_dir.items():
        others = set().union(*(t for k, t in per_dir.items() if k != d)) if len(per_dir) > 1 else set()
        unique[d] = sorted(s - others)

    lines = [
        "# OpenResearch-style Autoresearch — merged result",
        "",
        f"**Question:** {question}",
        f"**Directions (isolated worktrees):** {len(results)}",
        "",
        "| direction | facet | sources | grounded claims | unique-to-this-direction |",
        "|---|---|---:|---:|---|",
    ]
    for r in results:
        d = r["direction"]
        uq = [x for x in unique.get(d["id"], []) if x]
        lines.append(f"| `{d['id']}` | {d['facet']} | {len(r['sources'])} | "
                     f"{r['grounded']} | {', '.join(uq) or '—'} |")
    lines += [
        "",
        f"**Union evidence pool** ({len(union)} distinct sources): {', '.join(sorted(union)) or '—'}",
        f"**Sources every direction agreed on:** {', '.join(sorted(shared)) or '—'}",
        "",
        "_Divergence (per-direction unique sources) is the autoresearch signal:_ "
        "independent threads, run in isolation, surfaced different primary papers "
        "for the same top-level question; the merge keeps them all rather than "
        "collapsing to one survey's view.",
    ]
    out = run_root / "AUTORESEARCH.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def research(question: str, directions: int = 4, root: Path = DEFAULT_ROOT,
             backend: str | None = None, parallel: bool = True,
             limit: int = 3) -> Dict[str, Any]:
    """Full autoresearch cycle: fan-out → isolated parallel worktrees → merge."""
    run_root = root / _slug(question)
    run_root.mkdir(parents=True, exist_ok=True)
    planned = plan_directions(question, directions)
    if parallel and len(planned) > 1:
        with _fx.ThreadPoolExecutor(max_workers=len(planned)) as ex:
            results = list(ex.map(
                lambda d: run_direction(run_root, d, backend, limit), planned))
    else:
        results = [run_direction(run_root, d, backend, limit) for d in planned]
    report = merge(results, question, run_root)
    return {
        "question": question,
        "run_root": str(run_root),
        "report": str(report),
        "n_directions": len(results),
        "directions": [r["direction"]["id"] for r in results],
        "worktrees": [r["worktree"] for r in results],
        "union_sources": sorted({s for r in results for s in r["sources"]}),
        "total_grounded": sum(r["grounded"] for r in results),
        "total_dropped": sum(r["dropped"] for r in results),
    }


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="OpenResearch-style parallel autoresearch (model-free)")
    ap.add_argument("question", help="research question to fan out across directions")
    ap.add_argument("--directions", type=int, default=4, help="number of orthogonal lenses (1-5)")
    ap.add_argument("--backend", default=None, choices=[None, "seed", "arxiv", "orx"],
                    help="S_lit rail for evidence resolution (default env S_LIT_BACKEND)")
    ap.add_argument("--limit", type=int, default=3, help="max papers per direction")
    ap.add_argument("--out", default=str(DEFAULT_ROOT), help="run root")
    ap.add_argument("--sequential", action="store_true", help="disable parallel dispatch")
    args = ap.parse_args(argv)
    res = research(args.question, directions=args.directions,
                   root=Path(args.out), backend=args.backend,
                   parallel=not args.sequential, limit=args.limit)
    print(f"[autoresearch] {res['n_directions']} isolated directions -> "
          f"{len(res['union_sources'])} union sources, "
          f"{res['total_grounded']} grounded claims (gate dropped {res['total_dropped']})")
    print(f"[autoresearch] merged report: {res['report']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
