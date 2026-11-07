"""The experiment registry (P53): the battery as data, so any agent session can
pick up, execute, and record the next trial without being told which one.

Self-experimentation, mechanically: ``data/battery.json`` holds the measured
task families (the scoreboard set plus bound extra families, P67) with
pre-declared judge checks (M5.13), declared scales
(P47), grounding practice, and status. ``harness battery`` lists the state;
``harness battery --next`` prints the full spec of the next pending family for
an agent to execute; receipts flow back as scaled traces (M5.14 pool) and the
registry row flips to done. The registry never runs a trial itself - the
conditions need model judgment - but it removes every other excuse not to run
one: the spec, the criteria, and the report format are all in the data.
"""

from __future__ import annotations

import datetime as _dt
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from .registry import data_file

BATTERY_FILE = "battery.json"


@lru_cache(maxsize=1)
def load_battery() -> dict[str, Any]:
    with data_file(BATTERY_FILE).open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_battery(board: dict[str, Any] | None = None) -> list[str]:
    """Registry well-formedness (M0.5): families match the scoreboard, done
    families have both receipts, pending families have pre-declared checks."""
    board = board or load_battery()
    problems: list[str] = []
    fams = board.get("families") or []
    if not fams:
        problems.append("battery has no families")
        return problems
    try:
        scoreboard_ids = {
            e["id"] for e in json.loads(
                (Path(__file__).resolve().parent / "data" / "scoreboard.json")
                .read_text(encoding="utf-8")
            )["tasks"]
        }
    except Exception:
        scoreboard_ids = None
    seen: set[str] = set()
    for fam in fams:
        tid = fam.get("task_id")
        if not tid:
            problems.append("family without task_id")
            continue
        if tid in seen:
            problems.append(f"duplicate family {tid!r}")
        seen.add(tid)
        # P67: families beyond the scoreboard set are allowed only when bound
        # to their receipts' home trial projects (trial_projects) - the
        # registry<->traces reconciliation that the cron-parsing and
        # reading-extraction trials showed was missing.
        tps = fam.get("trial_projects")
        if scoreboard_ids is not None and tid not in scoreboard_ids:
            if not tps:
                problems.append(f"{tid}: not a scoreboard task id and not bound to trial_projects")
        if tps is not None:
            if not (isinstance(tps, list) and all(isinstance(p, str) and p for p in tps)):
                problems.append(f"{tid}: trial_projects must be a list of project paths")
            else:
                for p in tps:
                    if not _norm_path(p).startswith("updates/dogfood"):
                        problems.append(f"{tid}: trial project {p!r} outside updates/dogfood")
        status = fam.get("status")
        if status not in ("done", "pending"):
            problems.append(f"{tid}: status must be done|pending, got {status!r}")
        scale = fam.get("scale")
        if not (isinstance(scale, list) and len(scale) == 2 and scale[0] < scale[1]):
            problems.append(f"{tid}: scale must be [lo, hi] with lo < hi (P47)")
        checks = fam.get("judge_checks")
        if not (isinstance(checks, list) and checks):
            problems.append(f"{tid}: judge_checks must be declared before execution (M5.13)")
        if status == "done":
            results = fam.get("results") or {}
            # P74: a determinism test has no bare condition to run — requiring a
            # numeric A-bare would force fabricating a 0.0 (M0.4). Declare
            # "control_arm": "none" instead and the bare check is waived; the
            # harness arm stays numeric regardless.
            control_arm = fam.get("control_arm")
            if control_arm == "none":
                if "A-bare" not in results:
                    problems.append(f"{tid}: control_arm=none requires an explicit results.A-bare entry (use the string \"N/A ...\")")
            else:
                if not isinstance(results.get("A-bare"), (int, float)):
                    problems.append(f"{tid}: done family missing numeric results.A-bare (or declare control_arm=none)")
            if not isinstance(results.get("B-harness"), (int, float)):
                problems.append(f"{tid}: done family missing numeric results.B-harness")
            if not fam.get("round"):
                problems.append(f"{tid}: done family missing the round that ran it")
        if status == "pending" and not fam.get("spec"):
            problems.append(f"{tid}: pending family needs a spec (task/conditions/judge)")
    return problems


def next_pending(board: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """The first pending family in registry order - what an autonomous session
    should pick up next."""
    board = board or load_battery()
    for fam in board.get("families") or []:
        if fam.get("status") == "pending":
            return fam
    return None


def _norm_path(p: str) -> str:
    return p.replace("\\", "/").strip("/").lower()


def paired_projects(traces_lines: list[dict[str, Any]]) -> set[str]:
    """Projects whose task_outcome receipts cover BOTH conditions (a trial ran)."""
    conds: dict[str, set[str]] = {}
    for line in traces_lines:
        if line.get("event") != "task_outcome":
            continue
        cond = (line.get("detail") or {}).get("condition")
        if cond:
            conds.setdefault(_norm_path(line.get("project", "")), set()).add(cond)
    return {p for p, c in conds.items() if {"A-bare", "B-harness"} <= c}


def receipted_projects(traces_lines: list[dict[str, Any]]) -> set[str]:
    """P74: projects with at least one task_outcome receipt (any condition).

    The one-armed counterpart of :func:`paired_projects`, used for
    ``control_arm=none`` (determinism) families whose receipts are
    B-harness-only by design.
    """
    out: set[str] = set()
    for line in traces_lines:
        if line.get("event") == "task_outcome" and line.get("project"):
            out.add(_norm_path(line.get("project", "")))
    return out


def reconcile(board: dict[str, Any] | None = None,
              traces_lines: list[dict[str, Any]] | None = None) -> dict[str, list[str]]:
    """Bidirectional registry<->receipts metabolism (P67).

    ``unregistered_trials``: paired receipts whose project is bound to no
    family - an experiment that ran but was never filed (the P62 failure mode:
    cron-parsing and reading-extraction executed with receipts, no registry
    row). ``declared_without_receipts``: registered trial projects with no
    paired receipts - a row claiming a run that the traces cannot show.
    Observe-only: it lists facts, a human decides what to register (M0.4/M0.8).
    """
    board = board or load_battery()
    declared: set[str] = set()
    determinism: set[str] = set()
    for fam in board.get("families") or []:
        if fam.get("status") == "pending":
            # P70: a pending family names a *planned* trial_project, not one that
            # ran. It asserts no receipts yet, so it must not surface as
            # declared_without_receipts (that would flag a plan as a phantom run).
            continue
        for proj in fam.get("trial_projects") or []:
            declared.add(_norm_path(proj))
            # P74: a control_arm=none family (determinism test) has no bare arm
            # by design, so it can never show the BOTH-condition receipts that
            # paired_projects demands. Its binding is receipted by any
            # task_outcome instead — still trace-verified, just one-armed.
            if fam.get("control_arm") == "none":
                determinism.add(_norm_path(proj))
    paired = paired_projects(traces_lines or [])
    receipted = receipted_projects(traces_lines or [])
    return {
        "unregistered_trials": sorted(paired - declared),
        "declared_without_receipts": sorted((declared - determinism) - paired
                                            | (determinism - receipted)),
    }


def mark_done(task_id: str, results: dict[str, float], round_id: str,
              board_path: Path | None = None) -> None:
    """Flip a family to done after both receipts are recorded (caller harvests
    the traces first; the registry records the outcome, never the verdict)."""
    path = board_path or data_file(BATTERY_FILE)
    board = json.loads(Path(path).read_text(encoding="utf-8"))
    fam = next((f for f in board["families"] if f.get("task_id") == task_id), None)
    if fam is None:
        raise ValueError(f"unknown battery family: {task_id!r}")
    fam["status"] = "done"
    fam["results"] = dict(results)
    fam["round"] = round_id
    board["updated"] = _dt.date.today().isoformat()  # was hardcoded 2026-10-28 (P66)
    Path(path).write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8", newline="\n")


def render(board: dict[str, Any] | None = None) -> str:
    board = board or load_battery()
    lines = ["battery (experiment registry)"]
    done = pending = 0
    for fam in board.get("families") or []:
        tid, status = fam.get("task_id"), fam.get("status")
        if status == "done":
            done += 1
            r = fam.get("results") or {}
            lines.append(
                f"  [{tid:<18}] done   round={fam.get('round')}  "
                f"A-bare={r.get('A-bare')}  B-harness={r.get('B-harness')}  scale={fam.get('scale')}"
            )
        else:
            pending += 1
            lines.append(f"  [{tid:<18}] PENDING  (spec ready: 'harness battery --next')")
    lines.append(f"  {done} done / {pending} pending over {done + pending} families")
    if pending:
        nxt = next_pending(board)
        if nxt:
            lines.append(f"  next: {nxt['task_id']} — {nxt.get('grounding', '')[:70]}")
    return "\n".join(lines)
