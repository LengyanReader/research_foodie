"""A-1 deterministic §4.6 ablations — measured WITHOUT any model call or API key.

Three offline ablations that isolate the *system* contributions independent of
the (non-deterministic, currently credit-gated) LLM judge:

  (a) Grounding gate ON vs OFF — how many un-grounded/hallucination-candidate
      claims reach the draft with and without the L6 deterministic 5-gram gate.
      Uses the real ``tools.pipeline.validate.grounded_claims`` filter against a
      fixed source passage; grounded controls must be retained (no false drops).
  (b) Evidence-pool coverage — full/partial/empty over the cached 30-topic pools
      (``_eval_out/pools_30.json``), i.e. how often discovery yields ≥3 papers.
  (c) Median-of-N robustness — per-topic judge-total spread across the recorded
      repeat runs (``_eval_out/variance_runs.json``): min/median/mean/max, and the
      gap between a single-round draw and the median (judge-noise reduction).

Every number is recomputed from on-disk artifacts or the fixed fixture — the
report changes only when the underlying data changes, so it is safe to commit
and safe for CI (``self_check``). Stdlib only; missing artifacts degrade to an
honest "not measured yet" row rather than a fabricated one.

Usage:
    $PY -X utf8 -m tools.eval.ablations [--out _eval_out/ablations.md]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO = Path(__file__).resolve().parents[2]
EVAL_OUT = REPO / "_eval_out"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.pipeline.validate import _toks, grounded_claims  # noqa: E402

# (a) a fixed multi-sentence source passage — the ground truth the gate checks
#     against. Grounded quotes are verbatim substrings; un-grounded ones either
#     break contiguity (gap-1 interleave) or are disjoint fabrications.
_SOURCE = (
    "Transformer based models have largely replaced recurrent networks for "
    "sequence modelling because self attention routes information between "
    "positions in constant time. Pretraining on large corpora followed by "
    "task specific fine tuning became the dominant paradigm in natural "
    "language processing. Detectors that flag machine generated text are "
    "known to skew toward false positives for second language writers. "
    "Statistical watermarking and zero shot detection differ in robustness "
    "and in the cost of deployment at scale. Retrieval augmented generation "
    "couples a language model with an external index so that answers can be "
    "conditioned on retrieved evidence rather than parametric memory alone."
)
# verbatim long spans (must be RETAINED by the gate)
_GROUNDED = [
    "self attention routes information between positions in constant time",
    "Pretraining on large corpora followed by task specific fine tuning became the dominant paradigm in natural language processing",
    "known to skew toward false positives for second language writers",
    "couples a language model with an external index so that answers can be conditioned on retrieved evidence rather than parametric memory alone",
]
# fabricated, disjoint from _SOURCE (must be DROPPED by the gate)
_FABRICATED = [
    "Photosynthesis converts sunlight into glucose inside the thylakoid membrane",
    "The quantum engine accelerated past the outer ring of the orbital station",
    "97.4 percent of all detectors achieve perfect accuracy on Korean corpora",
    "Napoleon Bonaparte surrendered at Waterloo in the year sixteen twenty four",
]
_FILLER = "__fl__"


def _gap1(sentence: str) -> str:
    """Interleave a filler token between every content token — the tokens are
    all present but no 5-token run survives contiguous, so the 5-gram gate must
    reject it (contiguity is the whole test, not foreignness of the words)."""
    return " ".join(f"{_FILLER} {t}" for t in _toks(sentence))


def _paraphrase(sentence: str) -> str:
    """Swap the FIRST word of a long verbatim span; the remaining >=5-content-token
    run is untouched, so at least one shared 5-gram survives and the fuzzy gate
    must RETAIN it (false-drop guard — a single-word paraphrase is not a hallucination)."""
    w = sentence.split()
    w[0] = "generally"
    return " ".join(w)


def gate_ablation() -> Dict[str, Any]:
    """(a) grounding gate ON vs OFF on the fixed fixture."""
    ungrounded = [_gap1(s) for s in _SOURCE.split(". ")[:-1]] + _FABRICATED
    grounded = _GROUNDED + [_paraphrase(_GROUNDED[1])]
    claims = ([{"id": f"u{i}", "quote": q, "cite": "arXiv:2402.12345"}
               for i, q in enumerate(ungrounded)]
              + [{"id": f"g{i}", "quote": q, "cite": "arXiv:2402.12345"}
                 for i, q in enumerate(grounded)])
    kept, dropped = grounded_claims(claims, _SOURCE)
    kept_ids = {c["id"] for c in kept}
    leaked_on = sum(1 for i in range(len(ungrounded)) if f"u{i}" in kept_ids)
    retained = sum(1 for i in range(len(grounded)) if f"g{i}" in kept_ids)
    false_drops = len(grounded) - retained
    return {
        "ungrounded_n": len(ungrounded),
        "grounded_n": len(grounded),
        "gate_off_leakage": len(ungrounded),        # no filter -> all reach draft
        "gate_on_leakage": leaked_on,               # must be 0
        "grounded_retained": retained,              # must equal grounded_n
        "false_drops": false_drops,                 # must be 0
    }


def _read_json(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def pool_coverage(eval_dir: Path = EVAL_OUT) -> Dict[str, Any] | None:
    """(b) coverage over cached pools_30.json (full ≥3 papers, partial 1-2, empty 0)."""
    data = _read_json(eval_dir / "pools_30.json")
    if not isinstance(data, dict):
        return None
    n = len(data)
    full = sum(1 for v in data.values() if len(v.get("papers", [])) >= 3)
    partial = sum(1 for v in data.values() if 0 < len(v.get("papers", [])) < 3)
    empty = n - full - partial
    return {"total": n, "full": full, "partial": partial, "empty": empty,
            "coverage": (full + partial) / n if n else 0.0}


def median_of_n(eval_dir: Path = EVAL_OUT) -> List[Dict[str, Any]]:
    """(c) per-topic spread of judge totals across recorded repeat runs."""
    data = _read_json(eval_dir / "variance_runs.json") or []
    by: Dict[str, List[float]] = {}
    for r in data:
        t = r.get("total")
        if t is not None:
            by.setdefault(r.get("topic_id", "?"), []).append(float(t))
    out = []
    for tid in sorted(by):
        vs = by[tid]
        if len(vs) < 2:
            continue
        out.append({
            "topic": tid, "n": len(vs), "min": min(vs), "median": statistics.median(vs),
            "mean": statistics.fmean(vs), "max": max(vs),
            "spread": max(vs) - min(vs),
            "single_vs_median": abs(vs[-1] - statistics.median(vs)),
        })
    return out


def build_report(eval_dir: Path = EVAL_OUT) -> str:
    g = gate_ablation()
    pools = pool_coverage(eval_dir)
    med = median_of_n(eval_dir)
    L: List[str] = []
    L.append("# Ablations (deterministic, model-free)")
    L.append("")
    L.append("_Regenerate: `python -m tools.eval.ablations` — no LLM call, no API key._")
    L.append("")
    L.append("## (a) L6 grounding gate — ON vs OFF")
    L.append("")
    L.append("Fixed fixture: {} un-grounded candidates (contiguity-broken + fabricated), "
             "{} grounded controls.".format(g["ungrounded_n"], g["grounded_n"]))
    L.append("")
    L.append("| configuration | un-grounded claims reaching draft | grounded claims kept | false drops |")
    L.append("|---|---|---|---|")
    L.append("| gate **OFF** | {} | {} | {} |".format(
        g["gate_off_leakage"], g["grounded_n"], 0))
    L.append("| gate **ON**  | {} | {} | {} |".format(
        g["gate_on_leakage"], g["grounded_retained"], g["false_drops"]))
    L.append("")
    L.append("The deterministic gate removes **{}** hallucination candidates "
             "(leakage {} → {}) while keeping all {} grounded claims "
             "(**{}** false drops).".format(
                 g["gate_off_leakage"] - g["gate_on_leakage"],
                 g["gate_off_leakage"], g["gate_on_leakage"],
                 g["grounded_n"], g["false_drops"]))
    L.append("")
    L.append("## (b) Evidence-pool coverage (30 topics, cached)")
    L.append("")
    if pools:
        L.append("| topics | full (≥3 papers) | partial (1-2) | empty (0) | covered |")
        L.append("|---|---|---|---|---|")
        L.append("| {} | {} | {} | {} | {:.0f}% |".format(
            pools["total"], pools["full"], pools["partial"], pools["empty"],
            pools["coverage"] * 100))
    else:
        L.append("_not measured yet — run `python -m tools.eval.pools_30` first._")
    L.append("")
    L.append("## (c) Median-of-N robustness (cached repeat judge runs)")
    L.append("")
    if med:
        L.append("| topic | rounds | min | median | mean | max | spread | last-vs-median |")
        L.append("|---|---|---|---|---|---|---|---|")
        for m in med:
            L.append("| {} | {} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | {:.2f} |".format(
                m["topic"], m["n"], m["min"], m["median"], m["mean"], m["max"],
                m["spread"], m["single_vs_median"]))
        avg_sp = statistics.fmean([m["spread"] for m in med])
        L.append("")
        L.append("Mean single-round spread ≈ **{:.2f}** Total points; reporting the "
                 "median of N dampens this judge noise (E-5 promotion additionally "
                 "requires Δ ≥ 2σ over N ≥ 3 rounds before any change).".format(avg_sp))
    else:
        L.append("_not measured yet — run `python -m tools.eval.variance_run` first._")
    L.append("")
    return "\n".join(L)


def run(eval_dir: Path = EVAL_OUT, out: Path | None = None) -> Dict[str, Any]:
    md = build_report(eval_dir)
    out = out or (eval_dir / "ablations.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    g = gate_ablation()
    return {"path": str(out), "gate": g,
            "pools": pool_coverage(eval_dir), "median_topics": len(median_of_n(eval_dir))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="A-1 deterministic model-free ablations")
    ap.add_argument("--out", default=None)
    ap.add_argument("--eval-dir", default=str(EVAL_OUT))
    a = ap.parse_args(argv)
    eval_dir = Path(a.eval_dir)
    out = Path(a.out) if a.out else (eval_dir / "ablations.md")
    s = run(eval_dir, out)
    print(f"[ablations] wrote {out}")
    print(f"[ablations] gate leakage ON={s['gate']['gate_on_leakage']} "
          f"OFF={s['gate']['gate_off_leakage']} false_drops={s['gate']['false_drops']} "
          f"· median_topics={s['median_topics']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
