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


def generate(home: Path | None = None) -> dict[str, Any]:
    """Compute the self-model from the SSOT."""
    caps = _load("capabilities.json")
    doms = _load("domains.json")
    cat = _load("harnesses.json")
    cycles = _load("cycles.json")

    capabilities = sorted(caps.keys())
    domains = sorted(k for k in doms if k != "general")
    catalog_count = len(cat.get("harnesses", []))
    total_cycles = len(cycles.get("cycles", []))
    clauses_anchored = sum(
        1 for c in cycles.get("cycles", [])
        for cl in c.get("added", {}).get("clauses", [])
    )
    references = _count_references()

    # P66: the battery axes are read from the experiment registry itself
    # (battery.json), not from the scoreboard task set - the two counts were
    # different things and the old "all_have_effect_metric" was a constant.
    battery = _load("battery.json")
    battery_families = battery.get("families", [])
    battery_done = sum(1 for f in battery_families if f.get("status") == "done")

    # capability trigger coverage: which domains have at least one keyed capability
    domain_keyed: dict[str, list[str]] = {}
    for cid, c in caps.items():
        w = c.get("when", {})
        if "domain" in w:
            ds = w["domain"] if isinstance(w["domain"], list) else [w["domain"]]
            for x in ds:
                domain_keyed.setdefault(x, []).append(cid)
    domains_without_capability = [d for d in domains if d not in domain_keyed]

    # operating-procedure coverage (P65's emission surface, P66's audit of it)
    caps_without_procedure = sorted(cid for cid, c in caps.items() if not c.get("procedure"))

    # topic wiring coverage, computed from the SSOT (the P59 measure) rather
    # than copied from the last evolve report (a stale constant by design)
    uncovered_topics = _uncovered_topics()

    # trace health
    trace_stats = _trace_stats(home=home)

    return {
        "capabilities": {"total": len(capabilities), "ids": capabilities},
        "domains": {"total": len(domains), "without_keyed_capability": domains_without_capability},
        "catalog": {"total": catalog_count},
        "clauses": {"anchored_total": clauses_anchored},
        "references": {"total": references},
        "cycles": {"total": total_cycles},
        "battery": {
            "families": len(battery_families),
            "done": battery_done,
            "updated": battery.get("updated", ""),
        },
        "traces": trace_stats,
        "gaps": {
            "domains_without_capability": domains_without_capability,
            "caps_without_procedure": caps_without_procedure,
            "uncovered_topics": uncovered_topics,
        },
    }


def _uncovered_topics() -> list[str]:
    """Topic ids that no tracked source carries (evolve's high-severity audit).
    The topic authority is the watchlist (what evolution.snapshot uses), not a
    copy - P66: same input, same answer, no stale constant."""
    from .refresh import load_watchlist

    src = _load("sources.json")
    wired: set[str] = set()
    for group in src.get("groups", {}).values():
        for entry in group:
            wired.update(entry.get("topics", []))
    topic_ids = [t["id"] for t in load_watchlist().get("topics", [])]
    return [t for t in topic_ids if t not in wired]


def _count_references() -> int:
    """Count the highest R-number in references.md."""
    refs = Path(__file__).resolve().parent.parent.parent / "review" / "references.md"
    if not refs.exists():
        return 0
    import re
    nums = re.findall(r"^- R(\d+)\.", refs.read_text(encoding="utf-8"), re.MULTILINE)
    return max((int(n) for n in nums), default=0)


def _trace_stats(home: "Path | None" = None) -> dict[str, Any]:
    """Trace statistics from the tool home (if available). ``home`` defaults to
    :func:`config.home` so ``HARNESS_HOME`` redirection works (tests simulate)."""
    from . import config, trace as _tr

    root = Path(home) if home is not None else config.home()
    traces = root / _tr.TRACES_REL
    items = _tr.read_traces(traces)
    events: dict[str, int] = {}
    for d in items:
        e = d.get("event", "?")
        events[e] = events.get(e, 0) + 1
    return {"total": len(items), "events": events}


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
    b = model["battery"]
    lines.append(f"  battery: {b['done']}/{b['families']} families done (registry updated {b['updated']})")
    gaps = model["gaps"]
    if gaps["domains_without_capability"]:
        lines.append(f"  gaps: {len(gaps['domains_without_capability'])} domains without keyed capability")
    if gaps.get("caps_without_procedure"):
        lines.append(f"  gaps: {len(gaps['caps_without_procedure'])} capabilities without operating procedures: {', '.join(gaps['caps_without_procedure'])}")
    if gaps.get("uncovered_topics"):
        lines.append(f"  uncovered topics: {', '.join(gaps['uncovered_topics'])}")
    return chr(10).join(lines)
