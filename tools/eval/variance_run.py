"""Variance re-runs for the proxy canonical trio (P-A/P-B/P-C).

The local judge is a non-deterministic free model; DAS-style totals carry
run-to-run noise (observed ±0.3-0.4). This driver runs the trio N extra times
and records per-topic Total + family means to _eval_out/variance_runs.json,
then aggregates mean/sd across all rounds for a grounded stability figure.

Usage:
  $PY -X utf8 -m tools.eval.variance_run --rounds 2
"""

import argparse
import json
import statistics
from pathlib import Path

from tools.eval.bench_eval import SCENARIOS, run_scenarios, _family_avgs
from tools.llm.client import LLMClient

OUT = Path("_eval_out/variance_runs.json")
PROXY = [s for s in SCENARIOS if s["kind"] == "proxy"]


def _total(bench) -> float | None:
    scores = (bench or {}).get("scores") or {}
    return statistics.mean(scores.values()) if scores else None


def run_rounds(rounds: int) -> None:
    recs = []
    if OUT.exists():
        recs = json.loads(OUT.read_text(encoding="utf-8"))
    client = LLMClient(backend="opencode")
    for rd in range(1, rounds + 1):
        rows = run_scenarios(client, PROXY)
        for r in rows:
            tid = r["scenario"]["topic_id"]
            fa = _family_avgs((r.get("bench") or {}).get("scores") or {})
            recs.append({
                "round": len(recs) + 1,
                "topic_id": tid,
                "total": _total(r.get("bench")),
                "BSC": fa.get("BSC"), "MAR": fa.get("MAR"),
                "TSQ": fa.get("TSQ"), "HDQ": fa.get("HDQ"),
            })
            print(f"[var] round#{len(recs)} {tid} total={recs[-1]['total']} "
                  f"BSC={fa.get('BSC')} MAR={fa.get('MAR')} "
                  f"TSQ={fa.get('TSQ')} HDQ={fa.get('HDQ')}", flush=True)
        OUT.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
    _report(recs)


def _report(recs) -> None:
    by: dict = {}
    for r in recs:
        by.setdefault(r["topic_id"], []).append(r)
    print("\n[var] aggregate (n = runs per topic):")
    for tid, rs in sorted(by.items()):
        tots = [r["total"] for r in rs if r["total"] is not None]
        if not tots:
            continue
        m, sd = statistics.mean(tots), statistics.stdev(tots) if len(tots) > 1 else 0.0
        print(f"[var] {tid}: total {m:.2f} ± {sd:.2f} (n={len(tots)})  "
              f"BSC {statistics.mean([r['BSC'] for r in rs if r['BSC']]) if any(r['BSC'] for r in rs) else 0:.2f}  "
              f"MAR {statistics.mean([r['MAR'] for r in rs if r['MAR']]) if any(r['MAR'] for r in rs) else 0:.2f}  "
              f"TSQ {statistics.mean([r['TSQ'] for r in rs if r['TSQ']]) if any(r['TSQ'] for r in rs) else 0:.2f}  "
              f"HDQ {statistics.mean([r['HDQ'] for r in rs if r['HDQ']]) if any(r['HDQ'] for r in rs) else 0:.2f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=2)
    a = ap.parse_args()
    run_rounds(a.rounds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())