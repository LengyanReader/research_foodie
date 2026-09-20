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

OUT = Path("_eval_out/variance_runs.json")
PROXY = [s for s in SCENARIOS if s["kind"] == "proxy"]


def _total(bench) -> float | None:
    scores = (bench or {}).get("scores") or {}
    return statistics.mean(scores.values()) if scores else None


def run_rounds(rounds: int, profile_name: str | None = None) -> None:
    from tools.llm.profiles import load_profile, clients_for, profile_header, ProfileError
    from tools.eval.run_ledger import ResumeLedger
    try:
        profile = load_profile(profile_name)
        draft_client, judge_client = clients_for(profile)
    except ProfileError as e:
        print(f"[var] profile error: {e}")
        raise
    print(f"[var] {profile_header(profile)}")

    recs = []
    if OUT.exists():
        recs = json.loads(OUT.read_text(encoding="utf-8"))
    if len(recs) >= rounds * len(PROXY):
        print(f"[var] all {rounds} requested rounds already recorded "
              f"(n={len(recs)} recs) — nothing to do (resume memory)")
        return

    # --- resume: skip rounds already recorded for this exact profile ----------
    fingerprint = f"variance|{profile.name}"
    print(f"[var] resume memory: {len(recs)}/{rounds * len(PROXY)} topic-records "
          f"on file — completing the remainder")
    led = ResumeLedger.open("variance_run", fingerprint)
    try:
        for target_round in range(1, rounds + 1):
            done_this_round = {r["topic_id"] for r in recs if r.get("round") == target_round}
            topics = [s for s in PROXY if s["topic_id"] not in done_this_round]
            if not topics:
                print(f"[var] round #{target_round} already complete — skip (resume)")
                continue
            for s in topics:
                rows = run_scenarios(draft_client, [s],
                                     judge_client=judge_client)
                r = rows[0]
                fa = _family_avgs((r.get("bench") or {}).get("scores") or {})
                rec = {
                    "round": target_round,
                    "topic_id": s["topic_id"],
                    "total": _total(r.get("bench")),
                    "BSC": fa.get("BSC"), "MAR": fa.get("MAR"),
                    "TSQ": fa.get("TSQ"), "HDQ": fa.get("HDQ"),
                }
                recs.append(rec)
                led.record(f"{target_round}:{s['topic_id']}", rec)
                print(f"[var] round#{rec['round']} {s['topic_id']} total={rec['total']} "
                      f"BSC={fa.get('BSC')} MAR={fa.get('MAR')} "
                      f"TSQ={fa.get('TSQ')} HDQ={fa.get('HDQ')}", flush=True)
                OUT.write_text(json.dumps(recs, ensure_ascii=False, indent=1),
                               encoding="utf-8")  # crash-safe: save every topic
        led.finish("done")
    except BaseException:
        led.finish("interrupted")
        raise
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
    ap.add_argument("--profile", default=None,
                    help="named profile from tools.llm.profiles (default: env LLM_PROFILE)")
    a = ap.parse_args()
    run_rounds(a.rounds, a.profile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())