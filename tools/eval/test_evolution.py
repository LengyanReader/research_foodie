"""Deterministic unit tests for the WS-C Phase X self-evolution primitives and
the Phase L retrieval/aggregation additions (Session 22).

Zero-LLM, zero-network, no side effects on the real `_eval_out/` — every file
path in `tools.eval.evolution` is redirected to a throwaway temp dir first.
Run:

    python -m tools.eval.test_evolution      # exits 0 on all-pass, 1 otherwise

Covers the loop's *guards*, not the LLM: ticket dedupe/auto-close, the
variance-aware promotion rule, the anti-model-collapse gold quota, dependency
drift classification (E-4), L-3 judge median, and the L-1 re-rank fallbacks.
"""
from __future__ import annotations

import io
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from tools.eval import evolution as evo  # noqa: E402


def _redirect(tmp: Path) -> None:
    """Point every evolution ledger at `tmp` so tests never touch _eval_out."""
    evo.EVAL_OUT = tmp
    evo.TICKETS_F = tmp / "tickets.json"
    evo.DEPS_F = tmp / "deps_ledger.json"
    evo.FEEDBACK_DIR = tmp / "feedback"
    evo.FEEDBACK_F = tmp / "feedback" / "feedback.jsonl"
    evo.REVISIONS_F = tmp / "revisions.json"
    evo.LOG_F = tmp / "evolution_log.jsonl"


# ---------------------------------------------------------------------------

def _assert(cond: bool, msg: str, failures: list) -> None:
    print(f"  {'PASS' if cond else 'FAIL'}: {msg}", flush=True)
    if not cond:
        failures.append(msg)


def _test_tickets(failures: list) -> None:
    print("== E-3 debug-ticket board ==", flush=True)
    V = lambda lvl, chk, det: {"level": lvl, "check": chk, "detail": det}  # noqa: E731
    a = evo.tickets_from_verdicts([V("FAIL", "gate_coverage", "kill_rate=0.5")])
    _assert(a["opened"] == [1], "FAIL opens exactly one ticket (id 1)", failures)
    b = evo.tickets_from_verdicts([V("WARN", "gate_coverage", "kill_rate=0.6")])
    _assert(not b["opened"] and b["updated"] == [1],
            "repeat FAIL/WARN on same component feeds evidence (no dupe)", failures)
    board = evo.load_tickets()
    _assert(len(board["tickets"][0]["evidence"]) == 2,
            "deduped ticket accumulated 2 evidence rows", failures)
    c = evo.tickets_from_verdicts([V("PASS", "gate_coverage", "100% killed")])
    _assert(c["closed"] == ["gate_coverage"], "PASS closes the open ticket", failures)
    d = evo.tickets_from_verdicts([V("SKIP", "gate_coverage", "n/a")])
    _assert(not evo.open_tickets(),
            "SKIP after close keeps board empty (absent measurement != fixed)", failures)


def _test_promotion(failures: list) -> None:
    print("== E-5 promotion rule (variance-aware, human-gated) ==", flush=True)
    p = evo.promotion_check("judge:P-A", None, 3.9, 0.53, n_rounds=5)
    _assert(p["verdict"] == "insufficient_data",
            "missing means → insufficient_data (never guess)", failures)
    p = evo.promotion_check("judge:P-A", 4.0, 3.9, 0.53, n_rounds=5)
    _assert(p["verdict"] == "noise", "delta 0.1 (<2σ) → noise", failures)
    p = evo.promotion_check("judge:P-A", 5.5, 3.9, 0.53, n_rounds=2)
    _assert(p["verdict"] == "not_yet", "big delta but N<3 rounds → not_yet", failures)
    p = evo.promotion_check("judge:P-A", 5.5, 3.9, 0.53, n_rounds=4)
    _assert(p["verdict"] == "eligible", "delta≥2σ AND N≥3 → eligible", failures)
    p = evo.promotion_check("judge:P-A", 5.5, 3.9, 0.53, n_rounds=4,
                            regression_ok=False)
    _assert(p["verdict"] == "blocked_regression",
            "mock/gold regression blocks promotion", failures)


def _test_feedback(failures: list) -> None:
    print("== E-5 feedback corpus + anti-collapse gold quota ==", flush=True)
    st = evo.feedback_stats()
    _assert(st["n"] == 0 and st["quota_ok"], "empty corpus: quota not enforced yet", failures)
    for i in range(evo.GOLD_QUOTA_MIN - 1):
        evo.append_feedback("judged_run", f"P-{i}", {"score": 4},
                            gold_anchored=True)
    st = evo.feedback_stats()
    _assert(not st["enforced"], f"below {evo.GOLD_QUOTA_MIN} rows quota not enforced", failures)
    evo.append_feedback("judged_run", "P-x", {"score": 4}, gold_anchored=False)
    st = evo.feedback_stats()  # now 10 rows: 9 gold, 1 self-generated → 90%
    _assert(st["enforced"] and st["share"] >= 0.5,
            "at quota floor with high gold share → OK", failures)
    for _ in range(9):  # push share under 50% with non-gold rows
        evo.append_feedback("cadence_note", "synthetic", {}, gold_anchored=False)
    st = evo.feedback_stats()
    _assert(not st["quota_ok"], "gold share below 50% floor → quota violated (WARN)", failures)


def _test_revisions(failures: list) -> None:
    print("== E-5 numbered revision ledger (human-gated bumps) ==", flush=True)
    r1 = evo.bump_revision("judge", {"delta": "+1.6 over 4 rounds"})
    r2 = evo.bump_revision("judge", {"delta": "+0.9 over 3 rounds"})
    _assert(r1["revision"] == 1 and r2["revision"] == 2,
            "revisions bump v1 -> v2 monotonically", failures)
    _assert(len(r2["history"]) == 2 and r2["history"][-1]["revision"] == 1,
            "v2 keeps the prior revision in its history chain (revertable)", failures)


def _test_cadence_streak(failures: list) -> None:
    print("== E-3 cadence streak history ==", flush=True)
    V = lambda lvl, chk: {"level": lvl, "check": chk, "detail": ""}  # noqa: E731
    for _ in range(3):
        evo.log_cadence({"date": "x", "exit_code": 1, "verdicts": [V("WARN", "judge:P-A")]})
    _assert(evo.sustained_signal("judge:P-A") == 3,
            "three WARN cadences → streak of 3", failures)
    evo.log_cadence({"date": "x", "exit_code": 0, "verdicts": [V("PASS", "judge:P-A")]})
    _assert(evo.sustained_signal("judge:P-A") == 0,
            "a PASS cadence resets the streak", failures)


def _test_dep_verdicts(failures: list) -> None:
    print("== E-4 dependency ledger → verdicts (drift never silent) ==", flush=True)
    from tools.eval.evolution_sprint import _dep_verdicts
    deps = {"tools": {"python": {"version": "3.12"}, "opencode_cli": {"version": ""},
                      "pandoc": {"version": "3.8", "changed_from": "3.7"}},
            "missing_required": ["opencode_cli"], "missing_optional": [],
            "changed": ["pandoc"]}
    vs = {v["check"]: v["level"] for v in _dep_verdicts(deps)}
    _assert(vs.get("deps:opencode_cli") == "FAIL", "missing required pin → FAIL", failures)
    _assert(vs.get("deps:pandoc") == "WARN", "version drift → WARN", failures)
    _assert(vs.get("deps:python") == "PASS", "healthy pin → PASS (auto-closes tickets)", failures)


def _test_median(failures: list) -> None:
    print("== L-3 judge median-of-N aggregation ==", flush=True)
    from tools.eval.bench_eval import median_bench, DAS_16
    c0, c1 = DAS_16[0][1], DAS_16[1][1]
    runs = [{"scores": {c0: 5, c1: 3}}, {"scores": {c0: 3, c1: 3}},
            {"scores": {c0: 4, c1: 5}}, {"error": "judge hiccup"}]
    m = median_bench(runs)
    _assert(m["scores"][c0] == 4, f"median of [5,3,4] → 4 (got {m['scores'][c0]})", failures)
    _assert(m["scores"][c1] == 3, "median of [3,3,5] → 3", failures)
    _assert(m["median_rounds"] == 3 and m["rounds_offered"] == 4,
            "errored round skipped but counted in offered", failures)
    _assert(median_bench([])["coverage"] == 0, "empty input → zero-coverage, no raise", failures)


def _test_rerank(failures: list) -> None:
    print("== L-1 BM25 relevance re-rank (no-harm fallbacks) ==", flush=True)
    from tools.pipeline.rerank import select_windows
    short = "alpha beta gamma"
    txt, meta = select_windows(short, "beta", budget=100)
    _assert(meta["mode"] == "full" and txt == short,
            "paper fits budget → whole paper (mode full)", failures)
    para = ["filler sentence number %d with several words here" % i for i in range(200)]
    para[150] = "watermark detection robustness against paraphrase attacks is measured"
    md = "\n\n".join(para)
    got, meta = select_windows(md, "watermark detection robustness paraphrase", budget=400)
    _assert(meta["mode"] == "bm25" and "watermark detection" in got,
            "long paper, mid-paper answer → BM25 surfaces the relevant window", failures)
    _assert(len(got) <= 400, f"selected windows respect the budget (got {len(got)}<=400)", failures)
    # title/abstract anchor (block 0) kept first for section context
    _assert(got.startswith(para[0]), "first kept window is the anchor block (doc order)", failures)
    _, meta2 = select_windows(md, "", budget=400)
    _assert(meta2["mode"] == "raw", "empty query → raw head slice (pre-L-1 behavior)", failures)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="rf_evo_test_"))
    _redirect(tmp)
    failures: list[str] = []
    try:
        for fn in (_test_tickets, _test_promotion, _test_feedback, _test_revisions,
                   _test_cadence_streak, _test_dep_verdicts, _test_median, _test_rerank):
            fn(failures)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    if failures:
        print(f"\n==== {len(failures)} FAILED ====", flush=True)
        return 1
    print("\n==== ALL PASS ====", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
