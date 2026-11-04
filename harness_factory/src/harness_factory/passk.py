"""Reliability of recorded task outcomes as **pass^k** (P70).

The external agent benchmarks this factory catalogues in P70 do not score a
capability by a single pass. τ-bench / τ²-bench (R282/R283) and ThinkingBox
(R279) report **pass^k** — the probability that *k independent runs of the same
task all succeed*. A one-shot pass@1 hides an undependable agent: ThinkingBox's
own headline is that pass@1 and 20-of-20 consistency diverge sharply, and
τ-bench's airline leaderboard falls from Pass^1 0.46 to Pass^4 0.22. Repetition,
not the best single run, is the trust test.

This module reads that quantity off **our own** dogfood, so the capability
demonstration can be scored on the same bar. It aggregates facts and never
judges: what counts as a *pass* is read from the ``task_outcome`` receipt
(``trace.py``) — a ``passed`` flag, or a score at the top of its declared
``scale`` — never invented here (M0.4). It reads the D1 trace stream only; it
never touches the SSOT and never leaves the machine.

Estimator (following τ-bench): for a task run ``n`` times with ``c`` successes,
the unbiased probability that any ``k`` of those runs all succeed is
``C(c, k) / C(n, k)``; a task contributes only when ``n >= k``. Report the mean
of that over contributing tasks, alongside pass@1 for the divergence.
"""

from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from . import config
from . import trace as _tr

PASS_TOKENS = {"pass", "passed", "ok", "success", "solved", "resolved", "1", "true"}
FAIL_TOKENS = {"fail", "failed", "error", "wrong", "0", "false", ""}


def is_success(detail: dict[str, Any] | None) -> bool:
    """Did this outcome receipt pass? Read the pass-signal from the receipt.

    Priority: an explicit ``passed`` bool, else a numeric ``score`` at the top of
    its declared ``scale`` (full marks), else a numeric ``score`` >= 1.0, else a
    string verdict against :data:`PASS_TOKENS`. An unreadable receipt is *not* a
    pass (never guessed) - the caller sees it excluded from the count.
    """
    if not isinstance(detail, dict):
        return False
    if isinstance(detail.get("passed"), bool):
        return detail["passed"]
    score = detail.get("score")
    scale = detail.get("scale")
    if isinstance(score, bool):
        return score
    if (
        isinstance(scale, (list, tuple)) and len(scale) == 2
        and isinstance(score, (int, float))
    ):
        return score == scale[1]  # full marks on the declared scale
    if isinstance(score, (int, float)):
        return score >= 1.0
    if isinstance(score, str):
        return score.strip().lower() in PASS_TOKENS
    return False


def load_outcomes(home: "str | Path | None" = None) -> list[dict[str, Any]]:
    """Every ``task_outcome`` receipt in the tool home's trace stream."""
    root = Path(home) if home is not None else config.home()
    path = root / _tr.TRACES_REL
    return [ln for ln in _tr.read_traces(path) if ln.get("event") == "task_outcome"]


def group_by_task(outcomes: list[dict[str, Any]]) -> dict[tuple, list[bool]]:
    """Group receipts into per-(project, task, harness) lists of pass booleans."""
    groups: dict[tuple, list[bool]] = defaultdict(list)
    for o in outcomes:
        key = (o.get("project"), o.get("task"), o.get("harness"))
        groups[key].append(is_success(o.get("detail") or {}))
    return dict(groups)


def pass_k(runs: list[bool], k: int) -> "float | None":
    """τ-bench pass^k estimate for one task: C(c, k) / C(n, k), or None if n < k."""
    n = len(runs)
    if k <= 0 or n < k:
        return None
    c = sum(1 for r in runs if r)
    denom = math.comb(n, k)
    return math.comb(c, k) / denom if denom else None


def reliability(outcomes: list[dict[str, Any]], k: int) -> dict[str, Any]:
    """Aggregate pass^k over all tasks with ``>= k`` runs, with pass@1 for contrast."""
    groups = group_by_task(outcomes)
    per_task = {key: pass_k(runs, k) for key, runs in groups.items()}
    measured = [v for v in per_task.values() if v is not None]
    pass_at1 = [
        sum(runs) / len(runs) for runs in groups.values() if runs
    ]
    return {
        "k": k,
        "tasks_total": len(groups),
        "tasks_measured": len(measured),          # tasks with >= k recorded runs
        "pass_at_1": (round(sum(pass_at1) / len(pass_at1), 4) if pass_at1 else None),
        "pass_k": (round(sum(measured) / len(measured), 4) if measured else None),
        # the divergence the benchmarks warn about: reliable < one-shot
        "gap": (
            round(sum(pass_at1) / len(pass_at1) - sum(measured) / len(measured), 4)
            if (pass_at1 and measured)
            else None
        ),
    }


def run(root: "str | Path | None" = None, *, k: int = 2) -> dict[str, Any]:
    """Compute pass^k over the live trace stream (default home via ``HARNESS_HOME``)."""
    outcomes = load_outcomes(root)
    rep = reliability(outcomes, k)
    rep["outcomes_read"] = len(outcomes)
    return rep


def render(rep: dict[str, Any]) -> str:
    """Human-readable report; a task set too thin to measure is reported honestly."""
    lines = [f"reliability (pass^{rep['k']} from task_outcome receipts)"]
    lines.append(
        f"  outcomes read : {rep.get('outcomes_read', '?')} across {rep['tasks_total']} tasks"
    )
    if rep["tasks_measured"] == 0:
        lines.append(
            f"  pass^{rep['k']}        : not measurable - no task has >= {rep['k']} runs "
            f"(record repeated trials first; M5.12)"
        )
        return "\n".join(lines)
    lines.append(f"  tasks with >= {rep['k']} runs : {rep['tasks_measured']}")
    lines.append(f"  pass@1 (one-shot)  : {rep['pass_at_1']}")
    lines.append(f"  pass^{rep['k']} (reliable) : {rep['pass_k']}")
    if rep["gap"] is not None:
        lines.append(f"  reliability gap    : {rep['gap']}  (one-shot minus reliable)")
    return "\n".join(lines)
