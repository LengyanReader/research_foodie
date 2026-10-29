"""The experiment registry (P53): the battery as data, so any agent session can
pick up, execute, and record the next trial without being told which one.

Self-experimentation, mechanically: ``data/battery.json`` holds the seven
scoreboard families with pre-declared judge checks (M5.13), declared scales
(P47), grounding practice, and status. ``harness battery`` lists the state;
``harness battery --next`` prints the full spec of the next pending family for
an agent to execute; receipts flow back as scaled traces (M5.14 pool) and the
registry row flips to done. The registry never runs a trial itself - the
conditions need model judgment - but it removes every other excuse not to run
one: the spec, the criteria, and the report format are all in the data.
"""

from __future__ import annotations

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
        if scoreboard_ids is not None and tid not in scoreboard_ids:
            problems.append(f"{tid}: not a scoreboard task id")
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
            for cond in ("A-bare", "B-harness"):
                if not isinstance(results.get(cond), (int, float)):
                    problems.append(f"{tid}: done family missing numeric results.{cond}")
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
    board["updated"] = "2026-10-28"
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
