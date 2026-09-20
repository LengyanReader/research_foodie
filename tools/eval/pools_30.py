"""Build a local 3-paper evidence pool for all 30 DAS-Bench topics, then
optionally judge a sample end-to-end — the "does the pipeline scale to
arbitrary topics" battery (Session 19).

Two steps, resumable:
  python -m tools.eval.pools_30 --step build            # all 30 topics
  python -m tools.eval.pools_30 --step judge --judge 10 # first 10 with pools
Incremental manifest `_eval_out/pools_30.json` is saved after each topic so a
crash only loses the current topic. Papers are parsed via the same windowed
MinerU machinery as tools/eval/add_paper.py (≤6 pp/window, distinct -o dirs,
sub-split on flake); parsed ids are registered in-memory for the judge step —
corpus.py is never mutated.

Judge step writes a standalone markdown report `_eval_out/pools_30_report.md`
with family means (BSC/MAR/TSQ/HDQ/Total) for the judged sample.
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

MANIFEST = Path("_eval_out/pools_30.json")
REPORT = Path("_eval_out/pools_30_report.md")
TOPICS_JSON = Path("external/DAS/DAS-Bench/benchmark/topics.json")


def _load_topics() -> List[Dict[str, str]]:
    return json.loads(TOPICS_JSON.read_text(encoding="utf-8"))


def _load_manifest() -> Dict[str, Any]:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def build_step(limit: int = 3, tries_per_window: int = 2, ids_sel=None) -> int:
    from tools.pipeline.corpus import discover

    man = _load_manifest()
    done = set(man)
    topics = _load_topics()
    if ids_sel:
        topics = [t for t in topics if t["topic_id"] in set(ids_sel)]
    for t in topics:
        key = t["topic_id"]
        if key in done:
            print(f"[pools] {key} already in manifest, skip")
            continue
        q = t["topic"]
        print(f"[pools] {key} «{q[:60]}» searching…")
        try:
            cands = discover(q, backend="arxiv")[:6]
        except Exception as e:  # network hiccup → record empty pool
            print(f"[pools]   discover FAIL {e}")
            cands = []
        pools: List[Dict[str, str]] = []
        attempted: set = set(_id_refs(man))
        for c in cands:
            cid = c["arxiv_id"]
            if cid in attempted:
                continue
            attempted.add(cid)
            md_path = _parse_one(cid, tries_per_window=tries_per_window)
            if md_path:
                pools.append({"arxiv_id": cid, "title": c.get("title", ""),
                              "label": c.get("label", cid), "path_md": str(md_path)})
            if len(pools) >= limit:
                break
        man[key] = {"topic_id": key, "topic": q, "papers": pools,
                    "candidates": [c["arxiv_id"] for c in cands]}
        MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1),
                            encoding="utf-8")
        covered = f"{len(pools)}/{limit}"
        print(f"[pools] {key} -> {covered} {'OK' if pools else 'EMPTY'}", flush=True)
        time.sleep(1)
    return sum(1 for v in man.values() if v.get("papers"))


def _id_refs(man: Dict[str, Any]) -> List[str]:
    ids: List[str] = []
    for v in man.values():
        for p in v.get("papers", []):
            ids.append(p["arxiv_id"])
    return ids


def _parse_one(cid: str, tries_per_window: int) -> Path | None:
    from tools.eval.add_paper import _download, _parse, MINERU_OUT

    pdf = Path("_demo_downloads") / f"{cid}.pdf"
    try:
        _download(cid, pdf)
    except Exception as e:
        print(f"[pools]   download {cid} FAIL {e}")
        return None
    md = MINERU_OUT / cid / f"{cid}.md"
    if md.is_file():
        print(f"[pools]   {cid} cached")
        return md
    try:
        merged = _parse(pdf, cid)
        return merged if merged.is_file() else None
    except SystemExit as e:
        print(f"[pools]   parse {cid} FAIL {e}")
        return None


def judge_step(judge_n: int, out: Path = REPORT) -> None:
    import json as _json
    import statistics

    from tools.eval.bench_eval import run_scenarios, _family_avgs
    from tools.llm.client import LLMClient

    CACHE = Path("_eval_out/pools_cache")
    CACHE.mkdir(parents=True, exist_ok=True)

    man = _load_manifest()
    ready = [k for k in man if man[k].get("papers")]
    if not ready:
        print("[pools] no pools ready — run --step build first")
        return
    sel = ready[:judge_n]

    existing = {p.stem for p in CACHE.glob("*.json")}
    todo = [k for k in sel if k not in existing]
    if todo:
        client = LLMClient(backend="opencode")
        print(f"[pools] judging {len(todo)} topics (cached: {len(sel)-len(todo)}): {todo}")
        for key in todo:
            v = man[key]
            papers = []
            for p in v["papers"]:
                md = Path(p["path_md"])
                papers.append({"arxiv_id": p["arxiv_id"], "label": p["title"][:160],
                               "path": p["path_md"], "md": md.read_text(encoding="utf-8")})
            scen = {"kind": "pool", "topic_id": "P-" + key,
                    "topic": v["topic"], "question": v["topic"], "papers": papers}
            print(f"[pools] .. {scen['topic_id']} «{v['topic'][:48]}»", flush=True)
            try:
                rows = run_scenarios(client, [scen])
            except Exception as e:  # keep going: network/opencode hiccups
                print(f"[pools]    PARTIAL FAIL {type(e).__name__}: {str(e)[:120]}")
                continue
            _save_cache(rows, CACHE)
            r = rows[0]
            b = r.get("bench") or {}
            fa = _family_avgs(b.get("scores") or {})
            print(f"[pools]    -> papers={len(rows[0].get('papers') or [])} "
                  f"n_cited={r.get('n_cited')} "
                  f"BSC={_f(fa.get('BSC'))} MAR={_f(fa.get('MAR'))} "
                  f"TSQ={_f(fa.get('TSQ'))} HDQ={_f(fa.get('HDQ'))}", flush=True)

    # ---- assemble the report from cache ----
    rows = []
    for key in sel:
        p = CACHE / f"{key}.json"
        if p.exists():
            rows.append(_json.loads(p.read_text(encoding="utf-8")))
    if not rows:
        print("[pools] nothing judged yet")
        return
    L: List[str] = [f"# 30-topic evidence pool battery — judged sample (Session 19)\n",
                    "Updated: 2026-09-17 · judge backend: opencode local",
                    f"Pool build: 30/30 topics, {sum(1 for k in ready)} with ≥1 parsed paper; "
                    f"judged first {len(rows)} of those end-to-end (full pipeline + DAS-16).",
                    ""]
    fams: Dict[str, List[float]] = {f: [] for f in ("BSC", "MAR", "TSQ", "HDQ")}
    totals: List[float] = []
    for r in rows:
        b = r.get("bench") or {}
        scores = b.get("scores") or {}
        fa = _family_avgs(scores)
        L.append(f"| {r['scenario']['topic_id']} | {r['scenario']['topic'][:48]} "
                 f"| papers={len(r.get('papers') or [])} n_cited={r.get('n_cited')} "
                 f"| {_f(fa.get('BSC'))} {_f(fa.get('MAR'))} {_f(fa.get('TSQ'))} "
                 f"{_f(fa.get('HDQ'))} |")
        for f in fams:
            if fa.get(f) is not None:
                fams[f].append(fa[f])
        tot = [v for v in scores.values()]
        if tot:
            totals.append(statistics.mean(tot))
    L.append("")
    m = lambda xs: statistics.mean(xs) if xs else None  # noqa: E731
    L.append("| **sample mean** | "
             f"**{_f(m(fams['BSC']))} {_f(m(fams['MAR']))} "
             f"{_f(m(fams['TSQ']))} {_f(m(fams['HDQ']))} | "
             f"Total {_f(m(totals))} (n={len(totals)}) |")
    L.append("")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"[pools] report -> {out}")


# reuse bench cache serializer (JSON-safe rows)


def _save_cache(rows, cache_dir):
    import json as _json
    cache_dir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        safe = dict(r)
        safe["scenario"] = dict(r["scenario"])
        safe["papers"] = [dict(p) for p in r.get("papers") or []]
        (cache_dir / f"{r['scenario']['topic_id'].replace('P-', '')}.json").write_text(
            _json.dumps(safe, ensure_ascii=False), encoding="utf-8")


def _f(x, nd: int = 2) -> str:
    return "-" if x is None else f"{x:.{nd}f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", choices=("build", "judge"), default="build")
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--judge", type=int, default=10)
    ap.add_argument("--ids", default="", help="smoke: only these topic ids, e.g. 003,030")
    a = ap.parse_args()
    if a.step == "build":
        n = build_step(limit=a.limit,
                       ids_sel=[x.strip() for x in a.ids.split(",") if x.strip()] or None)
        print(f"[pools] done: {n}/30 topics have >=1 parsed paper "
              f"(manifest: {MANIFEST})")
    else:
        judge_step(a.judge)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())