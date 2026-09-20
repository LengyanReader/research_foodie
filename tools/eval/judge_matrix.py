"""D-3 cross-model judge matrix — score the same frozen manuscripts through
several judge vantages and report whether they *agree* (PLAN §8 Phase D, WS-D).

The self-evolution loop's reward-hacking guard (design §7) says a score delta
should survive a *different* judge before a human considers promoting a
prompt/judge bump. This harness is the measurement side of that rule:

    rows    = the frozen health proxies (P-A / P-B / P-C) rendered manuscripts
    columns = each judge you name (profile name, or `opencode`/`openai` model)
    cells   = mean of the 16 DAS-Bench criteria (optionally L-3 median-of-N)
    footer  = per-row cross-judge spread + a rank-agreement summary

Honest single-model reality: on this host the only *free* judge is
`opencode/big-pickle`, so the default matrix is one column. Adding a second
vantage is the point — pass `--judges` with a `judge-strong` profile (needs
OPENAI_API_KEY) or any OpenAI-compatible model. A one-column matrix still runs
and records provenance; it just can't corroborate (spread 0) — the report says
so rather than pretending.

Deterministic mock backend makes this testable offline (see test_pipeline mock
route + `--backend openai --base-url http://127.0.0.1:8201/v1`).

Usage:
  python -m tools.eval.judge_matrix                       # default judge(s)
  python -m tools.eval.judge_matrix --judges free-opencode,judge-strong
  python -m tools.eval.judge_matrix --rounds 3            # L-3 median per cell
  # offline/deterministic: start tools.llm.mock_openai_server, then
  python -m tools.eval.judge_matrix --judges mock-api \
      --backend openai --base-url http://127.0.0.1:8201/v1
"""
from __future__ import annotations

import argparse
import statistics
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.eval.bench_eval import SCENARIOS, score_survey, median_bench
from tools.llm.client import LLMClient
from tools.llm.profiles import load_profile, clients_for, ProfileError

REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_OUT = REPO_ROOT / "_eval_out"
REPORT = EVAL_OUT / "judge_matrix.md"
MANUSCRIPTS = EVAL_OUT / "manuscripts"
PROXIES = ["P-A", "P-B", "P-C"]


def _artifact(tid: str) -> Optional[str]:
    p = MANUSCRIPTS / f"{tid}_manuscript.md"
    if not p.is_file():
        return None
    art = p.read_text(encoding="utf-8")
    if "\n## Sources (" in art:
        art = art.split("\n## Sources (", 1)[0].rstrip()
    return art


def _cell(client: LLMClient, topic: str, artifact: str, rounds: int) -> Dict[str, Any]:
    """Score one (manuscript, judge): single call, or L-3 median over `rounds`
    slightly-varied temperatures to damp judge noise."""
    if rounds <= 1:
        b = score_survey(client, topic, artifact)
        vals = list(b.get("scores", {}).values())
        return {"total": round(statistics.mean(vals), 2) if vals else None,
                "coverage": b.get("coverage", 0), "rounds": 1,
                "judge_model": b.get("judge_model", "?")}
    runs = [score_survey(client, topic, artifact, temperature=0.2 + 0.15 * i)
            for i in range(rounds)]
    m = median_bench(runs)
    vals = list(m.get("scores", {}).values())
    return {"total": round(statistics.mean(vals), 2) if vals else None,
            "coverage": m.get("coverage", 0), "rounds": m.get("median_rounds", rounds),
            "judge_model": m.get("judge_model", "?")}


def _judge_clients(specs: List[str], backend: Optional[str],
                   base_url: Optional[str]) -> List[Dict[str, Any]]:
    """Resolve each judge spec to (label, client). A spec is a profile name
    (`free-opencode`/`judge-strong` -> its judge lane) or a bare model on the
    `--backend` (default opencode)."""
    out: List[Dict[str, Any]] = []
    for spec in specs:
        try:
            prof = load_profile(spec)
            _, jc = clients_for(prof)
            out.append({"label": f"{spec}:{prof.lane('judge').model}", "client": jc,
                       "profile": spec})
            continue
        except ProfileError:
            pass
        out.append({"label": spec,
                    "client": LLMClient(backend=backend or "opencode", model=spec,
                                        base_url=base_url),
                    "profile": f"{backend or 'opencode'}/{spec}"})
    return out


def _render(rows: List[Dict[str, Any]], judges: List[Dict[str, Any]],
            rounds: int) -> str:
    heads = " | ".join(j["label"] for j in judges)
    L = ["# Cross-model judge matrix (WS-D D-3)", "",
         f"> Generated: {time.strftime('%Y-%m-%d %H:%M')} · rows = frozen proxies "
         f"{PROXIES} · cells = mean of DAS-Bench 16 · median-of-{rounds} per cell",
         f"> {len(judges)} judge vantage(s). Promotion rule: a delta is only "
         f"corroborated when a *different* judge shows the same direction.", ""]
    if len(judges) < 2:
        L.append("> **single vantage** — this matrix cannot corroborate (spread is "
                 "trivially 0). Add a second judge via `--judges` (e.g. "
                 "`judge-strong`) to make D-3 meaningful.")
    L += ["", f"| proxy | {heads} | spread | agree? |", "|---|" + "---|" * (len(judges) + 2)]
    for r in rows:
        cells = " | ".join("" if r["cells"][j["label"]] is None
                           else str(r["cells"][j["label"]]) for j in judges)
        L.append(f"| {r['topic_id']} | {cells} | {r['spread']} | "
                 f"{'yes' if r['agree'] else 'n/a'} |")
    L += ["", "## Provenance (D-4)", ""]
    for j in judges:
        L.append(f"- `{j['label']}` — profile {j['profile']}")
    L.append("")
    return "\n".join(L)


def build_matrix(specs: List[str], rounds: int, backend: Optional[str],
                 base_url: Optional[str]) -> Dict[str, Any]:
    judges = _judge_clients(specs, backend, base_url)
    rows: List[Dict[str, Any]] = []
    for tid in PROXIES:
        topic = next((s["topic"] for s in SCENARIOS if s["topic_id"] == tid), f"proxy {tid}")
        art = _artifact(tid)
        cells: Dict[str, Any] = {}
        for j in judges:
            if art is None:
                cells[j["label"]] = None
                continue
            cells[j["label"]] = _cell(j["client"], topic, art, rounds)["total"]
        vals = [v for v in cells.values() if v is not None]
        spread = round(max(vals) - min(vals), 2) if len(vals) >= 2 else 0.0
        rows.append({"topic_id": tid, "cells": cells, "spread": spread,
                     "agree": len(vals) >= 2 and spread <= 1.0})
    return {"judges": judges, "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser(description="D-3 cross-model judge matrix")
    ap.add_argument("--judges", default="free-opencode",
                    help="comma-separated profile names or model ids")
    ap.add_argument("--rounds", type=int, default=1,
                    help="L-3 median-of-N per cell (N>=2 damps judge noise)")
    ap.add_argument("--backend", default=None, help="backend for bare model specs")
    ap.add_argument("--base-url", default=None)
    a = ap.parse_args()
    specs = [s.strip() for s in a.judges.split(",") if s.strip()]

    EVAL_OUT.mkdir(parents=True, exist_ok=True)
    mat = build_matrix(specs, max(1, a.rounds), a.backend, a.base_url)
    REPORT.write_text(_render(mat["rows"], mat["judges"], max(1, a.rounds)),
                      encoding="utf-8")
    print(f"[judge_matrix] wrote {REPORT} · {len(mat['judges'])} judge(s) "
          f"· median-of-{a.rounds}")
    for r in mat["rows"]:
        print(f"  {r['topic_id']}: spread={r['spread']} agree={r['agree']} {r['cells']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
