"""Frontier standard: the bar ledger and the monotone ratchet (see domains/excellence/).

This module is the *executable* form of the ``frontier-standard`` capability. It only
*measures and records*: it names a sourced bar, scores an artifact on the domain rubric
(``data/rubrics.json``), computes the weighted gap, and ratchets a floor that may only
rise. Adopting a new floor is an explicit human-gated step (M0.8); the module never
self-declares excellence (M0.4).
"""

from __future__ import annotations

import datetime as _dt
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

from .registry import data_file

LEVELS = ("R1", "R2", "R3", "R4", "R5", "R6")
LEVEL_NAMES = {
    "R1": "floor (correct / complete)",
    "R2": "peer (competent)",
    "R3": "strong (recognized practice)",
    "R4": "leader (current SOTA)",
    "R5": "frontier (best exemplar)",
    "R6": "moving (as SOTA advances)",
}
_SCALE_MAX = 3.0


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


@lru_cache(maxsize=1)
def rubrics() -> dict[str, dict[str, Any]]:
    with data_file("rubrics.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def rubric_for(domain: str) -> dict[str, Any]:
    """The rubric for ``domain`` (falls back to ``default``)."""
    table = rubrics()
    return table.get(domain) or table["default"]


def dimensions(domain: str) -> list[str]:
    return [d["dim"] for d in rubric_for(domain)["dimensions"]]


@lru_cache(maxsize=1)
def levers() -> dict[str, Any]:
    path = data_file("levers.json")
    if not path.exists():
        return {"default": {"modules": ["M3", "M4"], "kinds": [], "tools": [], "note": ""}}
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def lever_for(dim: str) -> dict[str, Any]:
    """How to close a gap in ``dim`` (modules + catalog kinds), default fallback."""
    return levers().get("by_dim", {}).get(dim) or levers()["default"]


def suggested_bar(domain: str) -> dict[str, Any] | None:
    """A curated, sourced bar for a domain, if one is recorded (else None)."""
    return levers().get("domain_bars", {}).get(domain)


# --- ledger I/O ---------------------------------------------------------------

def load_ledger(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"objectives": {}}


def save_ledger(path: str | Path, ledger: dict[str, Any]) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def objective(ledger: dict[str, Any], name: str, domain: str = "general") -> dict[str, Any]:
    obj = ledger.setdefault("objectives", {}).setdefault(
        name,
        {
            "domain": domain,
            "bar": None,
            "scores": {},
            "total": None,
            "floor": 0.0,
            "history": [],
            "frontier_checked_at": None,
        },
    )
    if domain and obj.get("domain") in (None, "general") and domain != "general":
        obj["domain"] = domain
    return obj


# --- operations ---------------------------------------------------------------

def set_bar(
    ledger: dict[str, Any],
    name: str,
    level: str,
    bar_name: str,
    source: str,
    checked: str | None = None,
    domain: str = "general",
) -> dict[str, Any]:
    if level not in LEVELS:
        raise ValueError(f"level must be one of {LEVELS}")
    if not source or not source.startswith("http"):
        raise ValueError("the bar needs a checkable, sourced reference (http...) (M0.1/M4)")
    obj = objective(ledger, name, domain)
    obj["bar"] = {
        "level": level,
        "level_name": LEVEL_NAMES[level],
        "name": bar_name,
        "source": source,
        "checked_at": checked or _now(),
        "is_apex": level in ("R4", "R5", "R6"),
    }
    return obj["bar"]


def weighted_total(domain: str, scores: dict[str, float]) -> float:
    for key, raw in scores.items():
        val = float(raw)
        if val < 0 or val > _SCALE_MAX:
            raise ValueError(f"score for {key!r} must be within 0..{_SCALE_MAX:g}")
    total = 0.0
    for d in rubric_for(domain)["dimensions"]:
        total += d["weight"] * float(scores.get(d["dim"], 0.0))
    return round(total, 4)


def record_scores(
    ledger: dict[str, Any], name: str, scores: dict[str, float], domain: str | None = None
) -> float:
    obj = objective(ledger, name, domain or "general")
    dom = domain or obj.get("domain", "general")
    obj["scores"] = {k: float(v) for k, v in scores.items()}
    obj["total"] = weighted_total(dom, obj["scores"])
    obj["history"].append({"at": _now(), "total": obj["total"], "note": "scored"})
    return obj["total"]


def audit(ledger: dict[str, Any], name: str, domain: str | None = None) -> list[dict[str, Any]]:
    obj = objective(ledger, name, domain or "general")
    dom = domain or obj.get("domain", "general")
    return audit_from(obj, dom)


def ratchet(
    ledger: dict[str, Any], name: str, force: bool = False, domain: str | None = None
) -> dict[str, Any]:
    """Adopt the achieved total as the new floor iff it does not regress.

    Returns a summary: {accepted, regressed, floor, total}. On a regression the
    floor is left untouched unless ``force`` (logged as a forced override).
    """
    obj = objective(ledger, name, domain or "general")
    if obj.get("total") is None:
        raise ValueError("score the objective first (`standard score ...`)")
    total = float(obj["total"])
    floor = float(obj.get("floor", 0.0))
    regressed = total < floor
    accepted = force or not regressed
    if accepted:
        new_floor = max(floor, total)
        obj["floor"] = new_floor
        obj["history"].append(
            {"at": _now(), "total": total, "note": "forced override" if (regressed and force) else "ratchet"}
        )
    else:
        new_floor = floor
    return {
        "accepted": accepted,
        "regressed": regressed,
        "floor": round(new_floor, 4),
        "total": total,
        "forced": bool(regressed and force),
    }


def check_regression(ledger: dict[str, Any], name: str, domain: str | None = None) -> dict[str, Any]:
    """Report (without mutating) whether the current total is below the floor."""
    obj = objective(ledger, name, domain or "general")
    total = obj.get("total")
    floor = float(obj.get("floor", 0.0))
    if total is None:
        return {"scored": False, "regressed": False, "floor": round(floor, 4), "total": None}
    return {
        "scored": True,
        "regressed": float(total) < floor,
        "floor": round(floor, 4),
        "total": round(float(total), 4),
    }


def mark_frontier(
    ledger: dict[str, Any], name: str, checked: str | None = None, domain: str | None = None
) -> str:
    obj = objective(ledger, name, domain or "general")
    obj["frontier_checked_at"] = checked or _now()
    obj["history"].append({"at": _now(), "total": obj.get("total"), "note": "frontier re-checked"})
    return obj["frontier_checked_at"]


def plan(
    ledger: dict[str, Any], name: str, domain: str | None = None, top: int | None = None
) -> dict[str, Any]:
    """Turn the gap audit into a harness configuration: per-gap modules + catalog tools.

    Reads the domain rubric (``data/rubrics.json``) for gaps and the lever map
    (``data/levers.json``) for remediation, then grounds tool suggestions in the
    catalog (``data/harnesses.json``). Observe-only; the human adopts (M0.8).
    """
    from . import catalog

    obj = objective(ledger, name, domain or "general")
    dom = domain or obj.get("domain", "general")
    rows = [r for r in audit_from(obj, dom) if r["weighted_gap"] > 0]
    if top is not None:
        rows = rows[:top]

    module_rank: Counter[str] = Counter()
    tools: list[str] = []
    nodes: list[dict[str, Any]] = []
    for r in rows:
        lv = lever_for(r["dim"])
        kinds = list(lv.get("kinds", []))
        node_tools: list[str] = []
        for kind in kinds:
            for entry in catalog.filter_rows(kind=kind)[:3]:
                hid = entry["id"]
                if hid not in node_tools:
                    node_tools.append(hid)
                if hid not in tools:
                    tools.append(hid)
        for m in lv.get("modules", []):
            module_rank[m] += 1
        nodes.append(
            {
                "dim": r["dim"],
                "zh": r.get("zh", ""),
                "weight": r["weight"],
                "ours": r["ours"],
                "gap": r["weighted_gap"],
                "modules": list(lv.get("modules", [])),
                "kinds": kinds,
                "tools": node_tools,
                "note": lv.get("note", ""),
                "claude": lv.get("claude", ""),
            }
        )

    return {
        "objective": name,
        "domain": dom,
        "bar": obj.get("bar"),
        "suggested_bar": None if obj.get("bar") else suggested_bar(dom),
        "floor": float(obj.get("floor", 0.0)),
        "total": obj.get("total"),
        "nodes": nodes,
        "modules": [m for m, _ in module_rank.most_common()],
        "tools": tools,
    }


# --- rendering ----------------------------------------------------------------

def render(ledger: dict[str, Any], name: str | None = None, domain: str | None = None) -> str:
    objs = ledger.get("objectives", {})
    if name:
        if name not in objs:
            return f"(no objective {name!r})"
        return _render_one(name, objs[name], domain)
    if not objs:
        return "(empty ledger — define a bar with `standard bar <objective> ...`)"
    lines = []
    for key, obj in objs.items():
        bar = obj.get("bar") or {}
        lines.append(
            f"{key:<28} dom={obj.get('domain','general'):<16} "
            f"bar={bar.get('level','—')} {'· ' + bar.get('name', '') if bar.get('name') else ''}"
        )
        lines.append(
            f"{'':28} floor={obj.get('floor', 0.0):<6.3f} total={obj.get('total') if obj.get('total') is not None else '—'}"
        )
    return "\n".join(lines)


def _render_one(name: str, obj: dict[str, Any], domain: str | None) -> str:
    dom = domain or obj.get("domain", "general")
    rubric = rubric_for(dom)
    bar = obj.get("bar")
    lines = [
        f"objective : {name}",
        f"domain    : {dom}  ({rubric['title_en']} · {rubric['title_zh']})",
    ]
    if bar:
        lines.append(
            f"bar       : {bar['level']} · {bar.get('level_name','')} · {bar['name']}\n"
            f"            {bar['source']}  (checked {bar['checked_at']})"
        )
    else:
        lines.append("bar       : (none — define with `standard bar ...`)")
    lines.append(f"floor     : {float(obj.get('floor', 0.0)):.3f}")
    lines.append(f"total     : {obj.get('total') if obj.get('total') is not None else '—'} (scale max 3.000)")
    lines.append("gap (desc) :")
    for row in audit_from(obj, dom):
        lines.append(
            f"  {row['dim']:<22} {row.get('zh',''):<8} w={row['weight']:.2f} "
            f"ours={row['ours']:.0f}/3  gap={row['weighted_gap']:.3f}"
        )
    if obj.get("frontier_checked_at"):
        lines.append(f"frontier  : checked {obj['frontier_checked_at']}")
    return "\n".join(lines)


def render_plan(p: dict[str, Any]) -> str:
    dom = p["domain"]
    rubric = rubric_for(dom)
    lines = [f"plan · {p['objective']}  ({dom})"]
    bar = p.get("bar")
    if bar:
        lines.append(f"bar  : {bar.get('level')} · {bar.get('name')}  ({bar.get('source')})")
    elif p.get("suggested_bar"):
        sb = p["suggested_bar"]
        lines.append(f"bar  : (none set) -> suggested {sb.get('level')} · {sb.get('name')}")
        lines.append(f"       source: {sb.get('source')}")
    lines.append(f"floor: {p['floor']:.3f}   total: {p.get('total') if p.get('total') is not None else '—'}")
    if not p["nodes"]:
        lines.append("(no open gaps — at/above the bar on every dimension)")
        return "\n".join(lines)
    lines.append("")
    lines.append("largest gaps -> configuration · 最大差距 -> 配置")
    for n in p["nodes"]:
        lines.append(
            f"  [{n['dim']}] {n.get('zh','')}  w={n['weight']:.2f} ours={n['ours']:.0f}/3 gap={n['gap']:.3f}"
        )
        cfg = f"    modules: {', '.join(n['modules']) or '—'}"
        if n["kinds"]:
            cfg += f"   tools<-{'/'.join(n['kinds'])}"
        lines.append(cfg)
        if n["tools"]:
            lines.append(f"    try: {', '.join(n['tools'])}")
        if n["note"]:
            lines.append(f"    why: {n['note']}")
        if n.get("claude"):
            lines.append(f"    claude: {n['claude']}")
    lines.append("")
    lines.append(f"enable modules · 启用模块: {', '.join(p['modules']) or '—'}")
    if p["tools"]:
        lines.append(f"wire tools · 挂载工具: {', '.join(p['tools'])}")
    lines.append("(observe-only — a human adopts this; M0.8)")
    return "\n".join(lines)


def audit_from(obj: dict[str, Any], dom: str) -> list[dict[str, Any]]:
    scores = obj.get("scores", {})
    rows: list[dict[str, Any]] = []
    for d in rubric_for(dom)["dimensions"]:
        ours = float(scores.get(d["dim"], 0.0))
        rows.append(
            {
                "dim": d["dim"],
                "zh": d.get("zh", ""),
                "weight": d["weight"],
                "ours": ours,
                "weighted_gap": round((_SCALE_MAX - ours) * d["weight"], 4),
            }
        )
    rows.sort(key=lambda r: r["weighted_gap"], reverse=True)
    return rows
