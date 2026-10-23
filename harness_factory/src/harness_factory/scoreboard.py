"""The scored task set (P23): a minimal, repeatable scoreboard for the factory itself.

M5.12 (component-ablation) needs a holdout with scores; P16.9 recorded that this
repository has no scored task set for its own harness, which is what this module
provides: five canonical tasks, each scored on five deterministic axes. The 1.0
baseline per task is pinned by ``tests/test_scoreboard.py``, so an ablation can
re-run the same tasks against a pruned configuration and compare on the same
ground (a baseline change is a deliberate edit of ``data/scoreboard.json``, never
a silent drift).

Offline and deterministic (M0.4): the scoreboard measures, it never invents.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from .assemble import build_files
from .capabilities import capability_ids
from .check import check_harness
from .classify import classify
from .derive import derive
from .registry import domain_ids, module_ids
from .spec import TaskSpec

_SCOREBOARD = Path(__file__).resolve().parent / "data" / "scoreboard.json"
AXES = ("routing", "capabilities", "modules", "structure", "emission")


def load_scoreboard() -> dict[str, Any]:
    return json.loads(_SCOREBOARD.read_text(encoding="utf-8"))


def validate_scoreboard(board: dict[str, Any] | None = None) -> list[str]:
    """Phantom-id guard: the scoreboard may only name things the SSOT has (M0.5)."""
    board = board or load_scoreboard()
    problems: list[str] = []
    known_domains = set(domain_ids())
    known_caps = set(capability_ids())
    known_modules = set(module_ids())
    seen: set[str] = set()
    for entry in board.get("tasks", []):
        tid = entry.get("id")
        if not isinstance(tid, str) or not tid:
            problems.append("task without a string id")
            continue
        if tid in seen:
            problems.append(f"duplicate task id {tid!r}")
        seen.add(tid)
        for field in ("task", "allowed_domains", "must_capabilities", "must_modules"):
            if field not in entry:
                problems.append(f"{tid}: missing field {field!r}")
        for d in entry.get("allowed_domains", []):
            if d not in known_domains:
                problems.append(f"{tid}: unknown domain {d!r}")
        for c in entry.get("must_capabilities", []):
            if c not in known_caps:
                problems.append(f"{tid}: unknown capability {c!r}")
        for m in entry.get("must_modules", []):
            if m not in known_modules:
                problems.append(f"{tid}: unknown module {m!r}")
    if not board.get("tasks"):
        problems.append("scoreboard has no tasks")
    return problems


def run_task(entry: dict[str, Any]) -> dict[str, Any]:
    """classify -> derive -> emit -> check -> score for one task. Deterministic."""
    task = TaskSpec(text=entry["task"])
    vector = classify(task)
    plan = derive(task, vector)
    files = build_files(plan)

    enabled = {m.module_id for m in plan.modules if m.enabled}
    matched = set(plan.capabilities)

    routing_ok = vector.domain in entry["allowed_domains"]
    cap_hit = sum(1 for c in entry["must_capabilities"] if c in matched)
    mod_hit = sum(1 for m in entry["must_modules"] if m in enabled)
    emission_ok = all("{{" not in text and "}}" not in text for text in files.values())

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, text in files.items():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        structure_ok = not check_harness(root)

    scores = {
        "routing": 1.0 if routing_ok else 0.0,
        "capabilities": (cap_hit / len(entry["must_capabilities"])) if entry["must_capabilities"] else 1.0,
        "modules": (mod_hit / len(entry["must_modules"])) if entry["must_modules"] else 1.0,
        "structure": 1.0 if structure_ok else 0.0,
        "emission": 1.0 if emission_ok else 0.0,
    }
    return {
        "id": entry["id"],
        "domain": vector.domain,
        "capabilities": plan.capabilities,
        "modules": sorted(enabled),
        "scores": scores,
        "total": round(sum(scores.values()) / len(AXES), 4),
    }


def run_all() -> list[dict[str, Any]]:
    return [run_task(entry) for entry in load_scoreboard()["tasks"]]


def render(reports: list[dict[str, Any]]) -> str:
    lines = ["scoreboard"]
    for report in reports:
        axes = " ".join(f"{k}={v:g}" for k, v in report["scores"].items())
        lines.append(
            f"  [{report['id']:<14}] domain={report['domain']:<18} "
            f"total={report['total']:.4f}  {axes}"
        )
    overall = (sum(r["total"] for r in reports) / len(reports)) if reports else 0.0
    lines.append(f"  overall={overall:.4f} over {len(reports)} task(s)")
    return "\n".join(lines)
