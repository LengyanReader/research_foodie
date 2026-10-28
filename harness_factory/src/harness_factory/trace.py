"""Trace recording for the D1 loop (P22 · D1a, extended in P24): traces are facts, not opinions.

The D1 design doc (`updates/2026-10-23-trace-driven-evolution-design.md`, a
human-gated proposal) names the schema this module implements: a closed
event vocabulary, required fields, append-only local storage, and a legacy
reader that treats pre-P22 lines as the ``signal`` event so nothing collected
before becomes unreadable.

P24 added the vocabulary's only result-side event, ``task_outcome``: the six
process events say where a harness misbehaved, but nothing recorded how the
task itself ended. A outcome line carries the *judge's* verdict
(``detail.judge`` is ``human`` or ``machine``) plus a ``detail.score`` — the
machine records the verdict, the human (or a task-family metric) makes it
(M0.4).

Traces never touch the SSOT and never leave the machine (offline by default);
they are proposal input for the M5 loop, not an automatic change (M0.4/M0.8).
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any

TRACE_VERSION = 1
TRACES_REL = "updates/traces.jsonl"
PROJECT_TRACES_REL = ".harness/traces.jsonl"

# Closed vocabulary (design doc §2): six process events, all mechanically
# producible, plus the one result-side event (P24).
EVENTS = frozenset(
    {
        "gate_miss",  # a runtime gate run failed
        "human_correction",  # a human rewrote plan/output (the strongest signal)
        "re_derive",  # the same task was re-derived (first selection insufficient)
        "capability_unused",  # matched but never referenced (working-set.json)
        "check_fail",  # the emitted self-check failed
        "context_eviction",  # M1.10 eviction receipts aggregated
        "task_outcome",  # the task's final result as judged (P24): the result fact the six process events cannot carry
    }
)
LEGACY_EVENT = "signal"  # lines recorded before P22 read back under this event

REQUIRED_FIELDS = ("v", "ts", "project", "task", "harness", "event")


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def make_trace(
    event: str,
    *,
    project: str,
    task: str,
    harness: str,
    detail: dict[str, Any] | None = None,
    model: dict[str, str] | None = None,
    session: str | None = None,
    revision: str | None = None,
) -> dict[str, Any]:
    """Build one trace line (design doc §2 schema). Raises ``ValueError`` on a bad event."""
    if event not in EVENTS:
        raise ValueError(f"unknown trace event: {event!r} (vocabulary: {sorted(EVENTS)})")
    trace: dict[str, Any] = {
        "v": TRACE_VERSION,
        "ts": _now(),
        "project": project,
        "task": task,
        "harness": harness,
        "event": event,
    }
    if detail:
        trace["detail"] = detail
    if model:
        trace["model"] = model
    if session:
        trace["session"] = session
    if revision:
        trace["revision"] = revision
    return trace


def validate(trace: dict[str, Any]) -> list[str]:
    """Return a list of problems; empty means the line is a well-formed trace."""
    if not isinstance(trace, dict):
        return ["trace is not a JSON object"]
    problems: list[str] = []
    if trace.get("v") != TRACE_VERSION:
        problems.append(f"trace version is {trace.get('v')!r}, expected {TRACE_VERSION}")
    for field in REQUIRED_FIELDS:
        if field == "v":  # checked as an int above
            continue
        if not isinstance(trace.get(field), str) or not trace[field]:
            problems.append(f"missing required field {field!r}")
    if trace.get("event") not in EVENTS:
        problems.append(f"unknown event {trace.get('event')!r}")
    if "detail" in trace and not isinstance(trace["detail"], dict):
        problems.append("'detail' must be a JSON object")
    if trace.get("event") == "task_outcome":
        # An outcome line without a judge and a score carries no information:
        # who verdicted, and what the verdict was (M0.4 — the machine records
        # the judgement, it never makes it).
        detail = trace.get("detail")
        if not isinstance(detail, dict):
            problems.append("task_outcome requires a detail object with judge + score")
        else:
            if detail.get("judge") not in ("human", "machine"):
                problems.append("task_outcome detail.judge must be 'human' or 'machine'")
            score = detail.get("score")
            if isinstance(score, bool) or not isinstance(score, (int, float, str)) or score == "":
                problems.append("task_outcome detail.score must be a number or non-empty string")
            # A declared scale ([lo, hi]) makes the score interpretable across
            # metric families (P45.R1: 1.0 is perfect on [0,1] and low on [0,5]).
            scale = detail.get("scale")
            if scale is not None:
                ok = (
                    isinstance(scale, list) and len(scale) == 2
                    and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in scale)
                    and scale[0] < scale[1]
                )
                if not ok:
                    problems.append("task_outcome detail.scale must be [lo, hi] with lo < hi")
    return problems


def record_trace(path: str | Path, trace: dict[str, Any]) -> None:
    """Append one validated trace line (append-only; raises on a bad line)."""
    problems = validate(trace)
    if problems:
        raise ValueError("; ".join(problems))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(trace, ensure_ascii=False) + "\n")


def read_traces(path: str | Path) -> list[dict[str, Any]]:
    """Read a traces file. Legacy lines (free text, or JSON without a valid
    ``event``) read back as ``{"event": "signal", ...}`` so pre-P22 records stay usable."""
    path = Path(path)
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            out.append({"v": None, "event": LEGACY_EVENT, "raw": line})
            continue
        if not isinstance(data, dict):
            out.append({"v": None, "event": LEGACY_EVENT, "raw": line})
        elif data.get("event") not in EVENTS:
            out.append({"event": LEGACY_EVENT, **data})
        else:
            out.append(data)
    return out


def collect_traces(project_root: str | Path, kb_root: str | Path) -> tuple[int, int]:
    """Pull a project's local traces into the knowledge base (offline, human-run).

    Returns ``(copied, rejected)``; rejected lines are counted and reported by the
    caller, never silently dropped (M0.4).
    """
    src = Path(project_root) / PROJECT_TRACES_REL
    if not src.exists():
        return 0, 0
    dst = Path(kb_root) / TRACES_REL
    copied = rejected = 0
    for line in src.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            rejected += 1
            continue
        if not isinstance(data, dict) or validate(data):
            rejected += 1
            continue
        record_trace(dst, data)
        copied += 1
    return copied, rejected
