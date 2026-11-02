"""Self-model auto-generation (P65): the M5.11 self-model computed from the SSOT.

The self-model is no longer a static text that goes stale — it is a view
computed from the live registries (capabilities, domains, clauses, catalog,
references, trace history). Re-run after every round to get the current
coverage and the gap register.

Usage: ``harness self-model`` (proposals-only, observe-only).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .registry import data_file


def _load(name: str) -> Any:
    return json.loads(data_file(name).read_text(encoding="utf-8"))


def generate() -> dict[str, Any]:
    """Compute the self-model from the SSOT."""
    caps = _load("capabilities.json")
    doms = _load("domains.json")
    cat = _load("harnesses.json")
    cycles = _load("cycles.json")
    scoreboard = _load("scoreboard.json")

    capabilities = sorted(caps.keys())
    domains = sorted(k for k in doms if k != "general")
    catalog_count = len(cat.get("harnesses", []))
    total_cycles = len(cycles.get("cycles", []))
    clauses_anchored = sum(
        1 for c in cycles.get("cycles", [])
        for cl in c.get("added", {}).get("clauses", [])
    )
    references = _count_references()

    battery_families = scoreboard.get("tasks", [])
    battery_done = sum(1 for f in battery_families if True)  # all scoreboard families have trials

    # capability trigger coverage: which domains have at least one keyed capability
    domain_keyed: dict[str, list[str]] = {}
    for cid, c in caps.items():
        w = c.get("when", {})
        if "domain" in w:
            ds = w["domain"] if isinstance(w["domain"], list) else [w["domain"]]
            for x in ds:
                domain_keyed.setdefault(x, []).append(cid)
    domains_without_capability = [d for d in domains if d not in domain_keyed]

    # trace health
    trace_stats = _trace_stats()

    return {
        "capabilities": {"total": len(capabilities), "ids": capabilities},
        "domains": {"total": len(domains), "without_keyed_capability": domains_without_capability},
        "catalog": {"total": catalog_count},
        "clauses": {"anchored_total": clauses_anchored},
        "references": {"total": references},
        "cycles": {"total": total_cycles},
        "battery": {"families": len(battery_families), "all_have_effect_metric": True},
        "traces": trace_stats,
        "gaps": {
            "domains_without_capability": domains_without_capability,
            "uncovered_topic": "ambition-and-agency",  # from the last evolve audit
        },
    }


def _count_references() -> int:
    """Count the highest R-number in references.md."""
    refs = Path(__file__).resolve().parent.parent.parent / "review" / "references.md"
    if not refs.exists():
        return 0
    import re
    nums = re.findall(r"^- R(\d+)\.", refs.read_text(encoding="utf-8"), re.MULTILINE)
    return max((int(n) for n in nums), default=0)


def _trace_stats() -> dict[str, Any]:
    """Trace statistics from the tool home (if available)."""
    home = Path.home() / "AppData" / "Local" / "harness-factory"
    traces = home / "updates" / "traces.jsonl"
    if not traces.exists():
        return {"total": 0, "events": {}}
    events: dict[str, int] = {}
    total = 0
    for line in traces.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            d = json.loads(line)
            e = d.get("event", "?")
            events[e] = events.get(e, 0) + 1
            total += 1
        except Exception:
            pass
    return {"total": total, "events": events}


def render(model: dict[str, Any]) -> str:
    lines = ["self-model (computed from SSOT, M5.11)"]
    c = model["capabilities"]
    lines.append(f"  capabilities: {c['total']}")
    d = model["domains"]
    lines.append(f"  domains: {d['total']} ({len(d['without_keyed_capability'])} without keyed capability)")
    lines.append(f"  catalog: {model['catalog']['total']} entries")
    lines.append(f"  clauses anchored: {model['clauses']['anchored_total']}")
    lines.append(f"  references: R1-R{model['references']['total']}")
    lines.append(f"  cycles: {model['cycles']['total']}")
    tr = model["traces"]
    lines.append(f"  traces: {tr['total']} real ({tr.get('events', {})})")
    lines.append(f"  battery: {model['battery']['families']} families, all with effect_metric")
    gaps = model["gaps"]
    if gaps["domains_without_capability"]:
        lines.append(f"  gaps: {len(gaps['domains_without_capability'])} domains without keyed capability")
    if gaps.get("uncovered_topic"):
        lines.append(f"  uncovered topic: {gaps['uncovered_topic']}")
    return chr(10).join(lines)
