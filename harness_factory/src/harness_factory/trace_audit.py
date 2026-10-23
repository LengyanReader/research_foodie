"""The rules auditor for D1 stage B (P25): recorded traces -> mutation proposals.

Turns the facts collected by the P22/P24 trace machinery into *proposals* for
the M5 loop. Each rule in ``data/trace-rules.json`` names the trace event, the
grouping key, the threshold and the proposed mutation (M5.3 vocabulary). The
auditor only proposes - it writes ``updates/traces-proposals.jsonl`` and a
rendered ``updates/TRACE-EVOLUTION.md`` in the knowledge base, and never touches
``data|core|domains|templates`` (M0.4/M0.8). Proposals are human-gated; a
measured promotion additionally needs the holdout (D1 stage C, P23 scoreboard).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import trace as _trace

_RULES_FILE = Path(__file__).resolve().parent / "data" / "trace-rules.json"
PROPOSALS_REL = "updates/traces-proposals.jsonl"
REPORT_REL = "updates/TRACE-EVOLUTION.md"
MUTATIONS = frozenset({"Promote", "Register", "Deepen", "Fission", "Archive", "Consolidate"})


def load_rules() -> list[dict[str, Any]]:
    return json.loads(_RULES_FILE.read_text(encoding="utf-8"))["rules"]


def validate_rules(rules: list[dict[str, Any]] | None = None) -> list[str]:
    """Phantom-id guard: rules may only name trace events and M5.3 mutations that exist."""
    rules = rules or load_rules()
    problems: list[str] = []
    seen: set[str] = set()
    for rule in rules:
        rid = rule.get("id")
        if not isinstance(rid, str) or not rid:
            problems.append("rule without a string id")
            continue
        if rid in seen:
            problems.append(f"duplicate rule id {rid!r}")
        seen.add(rid)
        if rule.get("event") not in _trace.EVENTS:
            problems.append(f"{rid}: unknown event {rule.get('event')!r}")
        if rule.get("mutation") not in MUTATIONS:
            problems.append(f"{rid}: mutation {rule.get('mutation')!r} not in the M5.3 vocabulary")
        group_by = rule.get("group_by", "")
        if not (group_by.startswith("detail.") or group_by in ("task", "project", "harness", "event")):
            problems.append(f"{rid}: group_by {group_by!r} must name a detail field or a top-level key")
        if not isinstance(rule.get("min_count"), int) or rule["min_count"] < 1:
            problems.append(f"{rid}: min_count must be a positive integer")
    return problems


def _group_value(trace: dict[str, Any], group_by: str) -> Any:
    """Resolve the group key inside ``detail``; lists become sorted tuples."""
    parts = group_by.split(".")
    value: Any = trace
    for part in parts:
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    if isinstance(value, list):
        return tuple(sorted(str(v) for v in value))
    if isinstance(value, str):
        return value
    return None


def audit(kb_root: str | Path, rules: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Group the knowledge base's traces by rule pattern and emit proposals.

    A proposal carries the evidence (event, group key, count, example
    timestamps) and the proposed mutation; it asserts nothing about whether
    the mutation *should* be applied - that is a human decision (M0.8), and a
    measured promotion additionally needs the holdout (D1 stage C).
    """
    rules = rules or load_rules()
    traces = _trace.read_traces(Path(kb_root) / _trace.TRACES_REL)
    proposals: list[dict[str, Any]] = []
    for rule in rules:
        groups: dict[Any, list[dict[str, Any]]] = {}
        for line in traces:
            if line.get("event") != rule["event"]:
                continue
            if rule["event"] == "task_outcome":
                score = (line.get("detail") or {}).get("score")
                if not isinstance(score, (int, float)) or score > rule.get("score_max", 2):
                    continue  # grade strings and high scores are human territory
            key = _group_value(line, rule["group_by"])
            if key is None:
                continue
            groups.setdefault(key, []).append(line)
        for key, lines in groups.items():
            if len(lines) < rule["min_count"]:
                continue
            proposals.append(
                {
                    "rule": rule["id"],
                    "event": rule["event"],
                    "group": list(key) if isinstance(key, tuple) else key,
                    "count": len(lines),
                    "examples": [l.get("ts") for l in lines[: rule["min_count"]]],
                    "mutation": rule["mutation"],
                    "target": rule["target"],
                    "why": rule["why"],
                    "proposed_on": _trace._now(),
                }
            )
    proposals.sort(key=lambda p: (p["rule"], str(p["group"])))
    return proposals


def emit(kb_root: str | Path, proposals: list[dict[str, Any]]) -> tuple[Path, Path]:
    """Append proposals to the journal and rewrite the rendered report."""
    kb_root = Path(kb_root)
    journal = kb_root / PROPOSALS_REL
    journal.parent.mkdir(parents=True, exist_ok=True)
    with journal.open("a", encoding="utf-8") as fh:
        for proposal in proposals:
            fh.write(json.dumps(proposal, ensure_ascii=False) + "\n")
    report = kb_root / REPORT_REL
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render(proposals), encoding="utf-8")
    return journal, report


def render(proposals: list[dict[str, Any]]) -> str:
    if not proposals:
        return "TRACE-EVOLUTION\n\nNo trace-driven proposals this run (below threshold, or no traces).\n"
    lines = ["TRACE-EVOLUTION", f"", f"{len(proposals)} proposal(s), proposal-only (M0.4/M0.8):"]
    for p in proposals:
        lines.append(
            f"- [{p['rule']}] {p['mutation']} {p['target']} "
            f"({p['count']}x {p['event']}, group={p['group']})"
        )
    lines.append("")
    lines.append("Human gate: accept into `evolve-apply` only after review; a measured promotion additionally needs the holdout (D1 stage C).")
    return "\n".join(lines)
