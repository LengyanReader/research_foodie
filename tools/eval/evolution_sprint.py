"""E-3 self-evolution cadence runner — one command, one screen (Session 22).

This is the *scheduled measurement + regression detection* heart of WS-C Phase
X (design `docs/design/self-evolution-mechanism.md`, PLAN §8 Phase X). It does
exactly one thing: run the frozen-subset health cycle, then push every signal
through the self-evolution loop's **external-measurement-only** pipeline:

    health_check.run_cycle  (E-2: mock · judge sanity · pools · L6 gate coverage)
        -> verify_deps       (E-4: version/dep drift becomes verdicts too)
        -> tickets_from_verdicts (E-3: FAIL/WARN open/feed a debug ticket; PASS closes)
        -> feedback_stats     (E-5: real-gold quota on the feedback corpus)
        -> promotion_check    (E-5: a repair is *eligible* only after N>=3 sustained
                               cadences AND >=2sigma AND no mock/gold regression)
        -> log_cadence        (E-3: one dated line; streaks feed promotion)
        -> _eval_out/evolution_sprint.md  (human review screen)

HONEST BOUNDARY (the loop never mutates itself): it writes ONLY ledger files
under `_eval_out/` (tickets · deps · feedback stats · cadence log · this report).
It NEVER edits code or prompts and NEVER commits — a promotion here is an
*eligibility flag* a human acts on after an explicit green-light (AGENTS.md).

Usage:
  python -m tools.eval.evolution_sprint --quick   # zero-LLM (mock+pools+gate+deps)
  python -m tools.eval.evolution_sprint           # full cycle (adds ~1.5 min judge)
  python -m tools.eval.evolution_sprint --report-only   # render board, no re-measure

Exit code: `0` GREEN · `1` WARN · `2` FAIL (max of health + dep findings).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List

from tools.eval import evolution as evo
from tools.eval.health_check import FROZEN_PROXY, run_cycle

REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_OUT = REPO_ROOT / "_eval_out"
SPRINT = EVAL_OUT / "evolution_sprint.md"


def _dep_verdicts(deps: Dict[str, Any]) -> List[Dict[str, str]]:
    """E-4: turn dependency-ledger findings into health-style verdicts so a
    missing required tool opens a ticket, a missing optional one warns, and a
    version drift is recorded (never silently). Every *healthy* pin also emits a
    PASS so `tickets_from_verdicts` auto-closes a previously-open `deps:<pin>`
    ticket once it recovers (dedupe is one-open-per-component)."""
    bad = set(deps.get("missing_required", [])) | set(deps.get("missing_optional", [])) \
        | set(deps.get("changed", []))
    v: List[Dict[str, str]] = []
    for name in deps.get("missing_required", []):
        v.append({"level": "FAIL", "check": f"deps:{name}",
                  "detail": "pinned required tool missing (environment/pin)"})
    for name in deps.get("missing_optional", []):
        v.append({"level": "WARN", "check": f"deps:{name}",
                  "detail": "optional tool missing (render/OCR live rail degraded)"})
    for name in deps.get("changed", []):
        if name in deps.get("missing_required", []) or name in deps.get("missing_optional", []):
            continue
        entry = deps["tools"].get(name, {})
        v.append({"level": "WARN", "check": f"deps:{name}",
                  "detail": f"version drift {entry.get('changed_from', '?')} -> "
                            f"{entry.get('version', '?')} (re-baseline if intended)"})
    for name in deps.get("tools", {}):
        if name not in bad:
            v.append({"level": "PASS", "check": f"deps:{name}",
                      "detail": f"{deps['tools'][name].get('version', '')} verified"})
    return v


def _promotion_signals(verdicts: List[Dict[str, str]], current: Dict[str, Any],
                       base: Dict[str, Any]) -> List[Dict[str, Any]]:
    """For every proxy the judge flagged, ask the E-5 promotion rule whether a
    repair is *eligible yet* — needs a sustained streak across cadences AND a
    >=2sigma delta AND no mock regression. This never changes anything; it only
    reports what a human may consider promoting."""
    out: List[Dict[str, Any]] = []
    mock_ok = bool(current.get("mock", {}).get("all_pass"))
    jvar = (base or {}).get("judge_variance", {}) or {}
    for tid in FROZEN_PROXY:
        check = f"judge:{tid}"
        flagged = any(v["check"] == check and v["level"] in ("WARN", "FAIL")
                      for v in verdicts)
        if not flagged:
            continue
        cur = (current.get("judge", {}).get(tid) or {}).get("total")
        b = jvar.get(tid) or {}
        n = evo.sustained_signal(check, min_cadences=evo.PROMOTION_MIN_ROUNDS)
        out.append(evo.promotion_check(
            check, cur, b.get("mean"), b.get("sd"),
            n_rounds=max(n, 1), regression_ok=mock_ok))
    return out


def _render(verdicts, deps, actions, fb, promos, exit_code, provenance,
            quick, elapsed) -> str:
    color = ("GREEN", "WARN", "FAIL")[exit_code] if exit_code < 3 else "?"
    L = ["# Evolution sprint / 自我演化周期 (WS-C Phase X, E-3)", "",
         f"> Generated: {time.strftime('%Y-%m-%d %H:%M')} · verdict **{color}** "
         f"(exit {exit_code}) · mode {'quick (zero-LLM)' if quick else 'full cycle'} "
         f"· {elapsed:.0f}s",
         f"> Trigger discipline: signals come only from external measurement "
         f"(mock regression · judge sanity · pool coverage · L6 gate mutation · "
         f"dep drift). The loop writes ledgers only — no code/prompt changes, no commits.",
         f"> Provenance (D-4): {provenance}", ""]

    L += ["## 1 · Health verdicts (E-2 frozen subset)", ""]
    for v in verdicts:
        L.append(f"- **[{v['level']}]** `{v['check']}` — {v['detail']}")

    L += ["", "## 2 · Dependency & version ledger (E-4)", ""]
    L.append("| pin | version | status | severity |")
    L.append("|---|---|---|---|")
    for name, e in deps.get("tools", {}).items():
        L.append(f"| {name} | {e.get('version','')} | {e.get('status','')} "
                 f"| {e.get('severity','')} |")

    L += ["", "## 3 · Debug-ticket board (E-3)", "",
          f"- opened this cadence: {actions['opened'] or 'none'}",
          f"- fed with new evidence: {actions['updated'] or 'none'}",
          f"- closed (symptom did not reproduce): {actions['closed'] or 'none'}"]
    open_t = evo.open_tickets()
    if open_t:
        L += ["", "| id | component | fix class | opened | last delta |", "|---|---|---|---|---|"]
        for t in open_t:
            L.append(f"| {t['id']} | {t['component']} | {t['fix_class']} "
                     f"| {t['opened']} | {t['evidence'][-1]['delta'][:60]} |")

    L += ["", "## 4 · Feedback corpus & real-gold quota (E-5)", "",
          f"- rows: {fb['n']} · gold-anchored: {fb['gold']} · share: {fb['share']:.0%}",
          f"- anti-model-collapse quota (>=50% real gold over >=10 rows): "
          f"{'OK' if fb['quota_ok'] else 'BELOW FLOOR'}"
          + ("" if fb["enforced"] else " (not yet enforced — corpus < 10 rows)")]

    L += ["", "## 5 · Promotion eligibility (E-5 rule: N>=3 rounds AND >=2sigma AND no regression)", ""]
    if promos:
        for p in promos:
            L.append(f"- `{p['component']}` -> **{p['verdict']}** — {p.get('detail', '')}")
        L += ["", "> `eligible` = a human may now consider a versioned prompt/judge bump "
              "(re-baseline before/after, revertable). The loop does not promote itself."]
    else:
        L.append("- no flagged judge proxy to assess this cadence")

    L += ["", "---", "_Honest boundary: this file and the ledger JSONs under "
          "`_eval_out/` are the only outputs. Any repair is a human decision "
          "(AGENTS.md no-unsolicited-change)._", ""]
    return "\n".join(L)


def sprint(quick: bool = False, profile_name: str | None = None,
           backend: str | None = None, model: str | None = None,
           report_only: bool = False) -> int:
    EVAL_OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    if report_only:
        deps = evo._load_json(evo.DEPS_F, {"tools": {}})
        fb = evo.feedback_stats()
        open_t = evo.open_tickets()
        print(f"[sprint] report-only: {len(open_t)} open tickets, "
              f"feedback {fb['n']} rows (gold {fb['share']:.0%})")
        return 0

    # 1) E-2 health cycle (writes health_check.md)
    cyc = run_cycle(quick=quick, profile_name=profile_name, backend=backend, model=model)
    verdicts: List[Dict[str, str]] = list(cyc["verdicts"])

    # 2) E-4 dep drift -> more verdicts
    deps = evo.verify_deps()
    dverdicts = _dep_verdicts(deps)
    verdicts += dverdicts

    # 3) E-3 push every verdict onto the ticket board
    actions = evo.tickets_from_verdicts(verdicts)

    # 4) E-5 feedback-corpus health + promotion eligibility (report only)
    fb = evo.feedback_stats()
    promos = _promotion_signals(verdicts, cyc.get("current", {}), cyc.get("base", {}))
    if not fb["quota_ok"]:
        verdicts.append({"level": "WARN", "check": "feedback:gold_quota",
                         "detail": f"real-gold share {fb['share']:.0%} < 50% floor "
                                   f"(model-collapse guard)"})

    # 5) combined exit code (health + dep + feedback findings)
    levels = {"FAIL": 2, "WARN": 1, "SKIP": 0, "PASS": 0}
    exit_code = max([cyc["exit_code"]] + [levels[v["level"]] for v in verdicts])

    # 6) E-3 cadence log (one dated line; streaks behind promotion)
    evo.log_cadence({
        "date": time.strftime("%Y-%m-%d"), "exit_code": exit_code,
        "verdicts": verdicts, "quick": quick,
        "provenance": cyc.get("provenance", ""), "deps_changed": deps.get("changed", []),
        "tickets_opened": actions["opened"], "tickets_closed": actions["closed"],
    })

    # 7) one-screen human review report
    elapsed = time.time() - t0
    SPRINT.write_text(
        _render(verdicts, deps, actions, fb, promos, exit_code,
                cyc.get("provenance", ""), quick, elapsed),
        encoding="utf-8")
    evo.append_feedback("cadence_note", "evolution_sprint",
                        {"exit_code": exit_code, "quick": quick,
                         "n_verdicts": len(verdicts)},
                        provenance={"note": cyc.get("provenance", "")})

    # 8) refresh the scheduled capability × benchmark snapshot (user 2026-09-20:
    #    "定时给出各项功能在 benchmark 上的表现" + keep current config in docs).
    #    Reads the ledgers just written; changes nothing else.
    try:
        from tools.eval import capability_report
        cap = str(capability_report.write_report(EVAL_OUT))
    except Exception as e:  # never let the snapshot break the cadence
        cap = f"(capability_report skipped: {type(e).__name__}: {e})"

    print(f"\n[sprint] wrote {SPRINT}")
    print(f"[sprint] refreshed {cap}")
    for v in verdicts:
        print(f"  [{v['level']:<4}] {v['check']:<20} {v['detail'][:70]}")
    print(f"\n[sprint] exit_code={exit_code} "
          f"({('GREEN','WARN','FAIL')[exit_code] if exit_code < 3 else '?'}) "
          f"· open tickets={len(evo.open_tickets())}")
    return exit_code


def main() -> int:
    ap = argparse.ArgumentParser(description="E-3 self-evolution cadence sprint")
    ap.add_argument("--quick", action="store_true",
                    help="zero-LLM cycle (mock + pools + gate coverage + deps)")
    ap.add_argument("--report-only", action="store_true",
                    help="render current board without re-measuring")
    ap.add_argument("--backend", default=None, help="override judge backend")
    ap.add_argument("--model", default=None)
    ap.add_argument("--profile", default=None)
    a = ap.parse_args()
    return sprint(quick=a.quick, profile_name=a.profile,
                  backend=a.backend, model=a.model, report_only=a.report_only)


if __name__ == "__main__":
    raise SystemExit(main())
