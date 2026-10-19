"""Capability-expansion cycles: registry, definition-of-done, gap surface.

SSOT = ``data/cycles.json``. A *cycle* is one round of capability expansion,
deepening, update or evolution of this factory. This module makes a round a
first-class object instead of a habit:

- **registry** - load the recorded cycles and the roadmap (planned + deferred),
  so a round is traceable and a deferral cannot be silently dropped;
- **definition-of-done** - the bar a capability must clear is *data* in the
  registry (clause, discriminator, guard, provenance, router, reachable), and
  ``audit`` checks it against the live SSOT rather than restating it in prose;
- **gap surface** - what is thin right now: capabilities with no router row, no
  provenance row, no guard test; clauses referenced but not anchored in their
  own module. This is the *input to the next cycle*, which is what makes the
  loop perpetual rather than episodic.

Observe-only: it reads the SSOT and the shipped docs, never writes them.
The procedure is ``reference/capability-cycle.md``; the round contract is
clause **M5.10** in ``core/06-self-evolution.md``.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from .registry import data_file

ROOT = Path(__file__).resolve().parents[2]  # harness_factory/

CYCLE_STATUSES = ("done", "active", "planned")
ROADMAP_STATUSES = ("planned", "deferred", "done")

# Module id -> the core doc that owns it (mirrors core/00-index.md).
MODULE_DOCS = {
    "M0": "01-meta-principles.md",
    "M1": "02-context-engineering.md",
    "M2": "03-long-running-agents.md",
    "M3": "04-verification-and-gates.md",
    "M4": "05-provenance-and-integrity.md",
    "M5": "06-self-evolution.md",
    "M6": "07-tools-and-skills.md",
    "M7": "08-change-governance.md",
    "M8": "09-collaboration-and-sessions.md",
}

_CLAUSE = re.compile(r"\b(M[0-8]\.\d{1,2})\b")
# A clause is *anchored* in a doc when it names a clause there: either as a
# heading (`## M0.4 - ...`) or inside a bold clause title (`**... (M3.11).**`).
# A bare inline `(M0.4)` is a *citation* from another module - by design, and
# deliberately not an anchor.
_CLAUSE_HEAD = re.compile(r"^#{2,6}\s*(M[0-8]\.\d{1,2})\b", re.M)
_CLAUSE_BOLD = re.compile(r"^\s*\d+\.\s+\*\*[^*\n]{0,240}?\((M[0-8]\.\d{1,2})\)[^*\n]{0,240}?\*\*", re.M)
_REF = re.compile(r"\bR(\d{1,3})\b")
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------- #
# load
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=1)
def registry() -> dict[str, Any]:
    with data_file("cycles.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def cycles() -> list[dict[str, Any]]:
    return list(registry().get("cycles") or [])


def roadmap() -> list[dict[str, Any]]:
    return list(registry().get("roadmap") or [])


def definition_of_done() -> list[dict[str, Any]]:
    return list(registry().get("definition_of_done") or [])


def by_id(cycle_id: str) -> dict[str, Any] | None:
    for cycle in cycles():
        if cycle.get("id") == cycle_id:
            return cycle
    return None


def roadmap_by_id(item_id: str) -> dict[str, Any] | None:
    for item in roadmap():
        if item.get("id") == item_id:
            return item
    return None


# --------------------------------------------------------------------------- #
# read the live SSOT + shipped docs
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


@lru_cache(maxsize=1)
def _capabilities() -> dict[str, dict[str, Any]]:
    with data_file("capabilities.json").open(encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def _domains() -> dict[str, dict[str, Any]]:
    with data_file("domains.json").open(encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def reference_ids() -> set[str]:
    """Every ``R<n>`` id present in ``review/references.md``."""
    return {f"R{m}" for m in _REF.findall(_read(ROOT / "review" / "references.md"))}


@lru_cache(maxsize=1)
def clause_anchors() -> dict[str, set[str]]:
    """Clause label -> the ``core/`` files that *anchor* it (heading or bold title)."""
    found: dict[str, set[str]] = {}
    for doc in sorted((ROOT / "core").glob("*.md")):
        text = _read(doc)
        labels = set(_CLAUSE_HEAD.findall(text)) | set(_CLAUSE_BOLD.findall(text))
        for label in labels:
            found.setdefault(label, set()).add(doc.name)
    return found


@lru_cache(maxsize=1)
def predicate_vocabulary() -> dict[str, tuple[str, ...]]:
    """The `when` predicates a capability may use - read from the engine, not invented.

    ``capabilities._cond_matches`` supports ``any``, ``min_horizon`` and plain
    feature axes; ``domain`` is validated against the live domain registry.
    """
    from .spec import FEATURE_CHOICES, HORIZONS

    vocab = {name: tuple(choices) for name, choices in FEATURE_CHOICES.items()}
    vocab["min_horizon"] = tuple(HORIZONS)
    vocab["domain"] = ()
    return vocab


@lru_cache(maxsize=1)
def _router_text() -> str:
    return _read(ROOT / "reference" / "capability-router.md")


@lru_cache(maxsize=1)
def _source_map_text() -> str:
    return _read(ROOT / "sources" / "source-map.md")


@lru_cache(maxsize=1)
def _tests_text() -> str:
    return "\n".join(_read(p) for p in sorted((ROOT / "tests").glob("*.py")))


@lru_cache(maxsize=1)
def _loadable_docs() -> set[str]:
    from . import skill

    return {entry.path for entry in skill.index()}


def _when_problems(
    cid: str,
    cond: Any,
    vocab: dict[str, tuple[str, ...]],
    domains: dict[str, Any],
) -> list[str]:
    """Validate one capability trigger against the engine's predicate vocabulary.

    Mirrors ``capabilities._cond_matches``: ``any`` (a list of conditions),
    ``min_horizon`` (at-least on the ladder), and plain feature axes (scalar or
    list membership). A predicate the engine cannot evaluate is a capability
    that silently never fires - which is exactly the drift worth catching.
    """
    out: list[str] = []
    if cond is None:
        return out
    if not isinstance(cond, dict):
        return [f"{cid}: `when` must be an object"]

    if "any" in cond:
        branches = cond["any"]
        if not isinstance(branches, list) or not branches:
            out.append(f"{cid}: `when.any` must be a non-empty list of conditions")
        else:
            for sub in branches:
                out.extend(_when_problems(cid, sub, vocab, domains))
        cond = {k: v for k, v in cond.items() if k != "any"}

    for key, value in cond.items():
        values = value if isinstance(value, list) else [value]
        if key == "min_horizon":
            for v in values:
                if v not in vocab["min_horizon"]:
                    out.append(
                        f"{cid}: `when.min_horizon` = {v!r} is not on the horizon ladder "
                        f"({', '.join(vocab['min_horizon'])})"
                    )
            continue
        if key == "domain":
            for v in values:
                if v not in domains:
                    out.append(f"{cid}: `when.domain` = {v!r} is not a registered domain")
            continue
        if key not in vocab:
            out.append(
                f"{cid}: `when` uses an undeclared predicate {key!r} - it can never fire "
                f"(declared: {', '.join(sorted(vocab))})"
            )
            continue
        for v in values:
            if v not in vocab[key]:
                out.append(
                    f"{cid}: `when.{key}` = {v!r} is not a declared choice ({', '.join(vocab[key])})"
                )
    return out


# --------------------------------------------------------------------------- #
# audit
# --------------------------------------------------------------------------- #
def audit() -> dict[str, Any]:
    """Check the registry + the definition-of-done against the live SSOT.

    ``problems`` are hard: they mean the registry, or a clause it claims, is
    wrong. ``gaps`` are soft: real wiring that is missing, i.e. the worklist the
    next cycle should draw from.
    """
    reg = registry()
    problems: list[str] = []
    gaps: list[str] = []

    # 0 - registry shape
    if not _ISO.match(str(reg.get("updated", ""))):
        problems.append("registry `updated` is not an ISO date")
    dod = reg.get("definition_of_done") or []
    if not dod:
        problems.append("`definition_of_done` is empty")
    for entry in dod:
        if not entry.get("key") or not entry.get("check"):
            problems.append(f"definition_of_done entry is incomplete: {entry!r}")
        elif not isinstance(entry.get("hard"), bool):
            problems.append(f"definition_of_done '{entry.get('key')}' needs a boolean `hard`")

    recs = cycles()
    seen: set[str] = set()
    for cycle in recs:
        cid = cycle.get("id")
        if not cid:
            problems.append("a cycle has no id")
            continue
        if cid in seen:
            problems.append(f"duplicate cycle id: {cid}")
        seen.add(cid)
        if cycle.get("status") not in CYCLE_STATUSES:
            problems.append(f"{cid}: status {cycle.get('status')!r} not in {CYCLE_STATUSES}")
        if not _ISO.match(str(cycle.get("date", ""))):
            problems.append(f"{cid}: date is not an ISO date")
        for key in ("title_en", "title_zh", "slices"):
            if not cycle.get(key):
                problems.append(f"{cid}: missing `{key}`")

    # 1 - registered: every id a cycle claims exists in the live SSOT
    caps = _capabilities()
    doms = _domains()
    refs = reference_ids()
    for cycle in recs:
        cid = cycle.get("id", "?")
        added = cycle.get("added") or {}
        for cap in added.get("capabilities") or []:
            if cap not in caps:
                problems.append(f"{cid}: capability {cap!r} is not in data/capabilities.json")
        for dom in added.get("domains") or []:
            if dom not in doms:
                problems.append(f"{cid}: domain {dom!r} is not in data/domains.json")
        for ref in added.get("references") or []:
            if ref not in refs:
                problems.append(f"{cid}: reference {ref!r} is not in review/references.md")

    # 2 - clause: a label belongs to its own module doc, and core/ agrees
    anchors = clause_anchors()
    for cycle in recs:
        cid = cycle.get("id", "?")
        for label in (cycle.get("added") or {}).get("clauses") or []:
            want = MODULE_DOCS[label.split(".")[0]]
            where = sorted(anchors.get(label, ()))
            if not where:
                problems.append(f"{cid}: clause {label} is claimed but anchored nowhere in core/")
            elif want not in where:
                problems.append(
                    f"{cid}: clause {label} is anchored in core/{', core/'.join(where)} "
                    f"but {label.split('.')[0]} lives in core/{want}"
                )
    # Note: the reverse direction (a label cited in another module's doc) is *not*
    # checked. Cross-module citation is a feature - `**Separate builder from critic
    # (M0.3).**` legitimately cites M0.3 from inside an M3 clause - so "this label
    # appears in the wrong file" cannot be distinguished from a citation without
    # parsing each item's own label. The forward check above is the load-bearing one.

    # 3 - discriminator: the trigger must be expressible in the engine's vocabulary
    vocab = predicate_vocabulary()
    for cid, meta in sorted(caps.items()):
        for problem in _when_problems(cid, meta.get("when") or {}, vocab, doms):
            problems.append(problem)
    by_registration: dict[str, list[str]] = {}
    for cid, meta in caps.items():
        signature = json.dumps(
            [meta.get("when") or {}, meta.get("modules") or [], meta.get("title_en") or ""],
            sort_keys=True,
            ensure_ascii=False,
        )
        by_registration.setdefault(signature, []).append(cid)
    for ids in by_registration.values():
        if len(ids) > 1:
            problems.append(
                "duplicate capability registration (same `when`, `modules` and title): "
                f"{', '.join(sorted(ids))} - that is a consolidation (M0.5), not an addition"
            )

    # 4 - roadmap integrity (a deferral must carry a reason and a trigger)
    rseen: set[str] = set()
    for item in roadmap():
        rid = item.get("id")
        if not rid:
            problems.append("a roadmap item has no id")
            continue
        if rid in rseen:
            problems.append(f"duplicate roadmap id: {rid}")
        if rid in seen:
            problems.append(f"roadmap id {rid} collides with a cycle id")
        rseen.add(rid)
        if item.get("status") not in ROADMAP_STATUSES:
            problems.append(f"roadmap {rid}: status {item.get('status')!r} not in {ROADMAP_STATUSES}")
        if not item.get("reason"):
            problems.append(f"roadmap {rid}: no reason recorded (a deferral must say why)")
        if not item.get("revisit_when"):
            problems.append(f"roadmap {rid}: no revisit trigger recorded (a deferral must say when)")

    # 5 - gaps: missing wiring for what already exists (soft, the next-cycle input)
    router = _router_text()
    source_map = _source_map_text()
    tests = _tests_text()
    for cid in sorted(caps):
        if cid not in router:
            gaps.append(f"router: reference/capability-router.md never routes to {cid}")
        if cid not in tests:
            gaps.append(f"guard: no test under tests/ mentions {cid}")
    for label in sorted(anchors):
        if label not in source_map:
            gaps.append(f"provenance: sources/source-map.md never maps {label} to a source")
    loadable = _loadable_docs()
    for doc in sorted((ROOT / "reference").glob("*.md")):
        if f"reference/{doc.name}" not in loadable:
            gaps.append(f"reachable: reference/{doc.name} exists but `harness skill` does not list it")

    counts: dict[str, int] = {status: 0 for status in CYCLE_STATUSES}
    for cycle in recs:
        counts[str(cycle.get("status"))] = counts.get(str(cycle.get("status")), 0) + 1
    road_counts: dict[str, int] = {status: 0 for status in ROADMAP_STATUSES}
    for item in roadmap():
        road_counts[str(item.get("status"))] = road_counts.get(str(item.get("status")), 0) + 1

    metrics = {
        "updated": reg.get("updated"),
        "cycles": len(recs),
        "cycles_by_status": counts,
        "roadmap": len(roadmap()),
        "roadmap_by_status": road_counts,
        "definition_of_done": len(dod),
        "capabilities": len(caps),
        "domains": len(doms),
        "clauses_anchored": len(anchors),
        "references": len(refs),
        "problems": len(problems),
        "gaps": len(gaps),
    }
    return {"ok": not problems, "problems": problems, "gaps": gaps, "metrics": metrics}


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_index() -> str:
    out: list[str] = []
    out.append("# Capability cycles · 能力演化循环")
    out.append("")
    out.append(
        "> One row per round of capability expansion. `added` is re-checked against the live SSOT by "
        "`harness cycle audit`; deferrals live in `harness cycle roadmap`. SSOT: `data/cycles.json`."
    )
    out.append("")
    out.append("| cycle | date | status | +cap | +dom | clauses | catalog | outlets | title |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for cycle in cycles():
        added = cycle.get("added") or {}
        clauses = ", ".join(added.get("clauses") or []) or "-"
        out.append(
            f"| {cycle.get('id')} | {cycle.get('date')} | {cycle.get('status')} "
            f"| {len(added.get('capabilities') or [])} | {len(added.get('domains') or [])} "
            f"| {clauses} | +{added.get('catalog_delta', 0)} | +{added.get('outlets_delta', 0)} "
            f"| {cycle.get('title_en', '')} |"
        )
    planned = sum(1 for i in roadmap() if i.get("status") == "planned")
    deferred = sum(1 for i in roadmap() if i.get("status") == "deferred")
    out.append("")
    out.append(f"Roadmap: {planned} planned · {deferred} deferred (`harness cycle roadmap`).")
    return "\n".join(out) + "\n"


def render_detail(cycle_id: str) -> str | None:
    cycle = by_id(cycle_id)
    if cycle is None:
        return None
    added = cycle.get("added") or {}
    out: list[str] = []
    out.append(f"# {cycle.get('id')} · {cycle.get('title_en')}")
    out.append("")
    out.append(f"**{cycle.get('title_zh', '')}** · {cycle.get('date')} · **{cycle.get('status')}**")
    out.append("")
    if cycle.get("note"):
        out.append(f"> {cycle['note']}")
        out.append("")
    out.append("## Slices · 切片")
    for slice_ in cycle.get("slices") or []:
        out.append(f"- {slice_}")
    out.append("")
    out.append("## Added · 新增")
    for key in ("capabilities", "domains", "clauses"):
        values = added.get(key) or []
        out.append(f"- **{key}** ({len(values)}): {', '.join(values) if values else '-'}")
    for key in ("catalog_delta", "instruments_delta", "outlets_delta"):
        if added.get(key):
            out.append(f"- **{key}**: +{added[key]}")
    refs = added.get("references") or []
    if refs:
        out.append(f"- **references** ({len(refs)}): {refs[0]}-{refs[-1]}")
    if cycle.get("sources_groups"):
        out.append(f"- **sources groups**: {', '.join(cycle['sources_groups'])}")
    return "\n".join(out) + "\n"


def render_roadmap() -> str:
    out: list[str] = []
    out.append("# Roadmap · 路线图")
    out.append("")
    out.append(
        "> Planned work and **deliberate non-additions**. Every entry carries a reason and a revisit "
        "trigger, so a deferral is a decision rather than an omission."
    )
    out.append("")
    out.append("| id | status | cycle | source | item | reason | revisit when |")
    out.append("|---|---|---|---|---|---|---|")
    for item in roadmap():
        out.append(
            f"| {item.get('id')} | {item.get('status')} | {item.get('cycle') or '-'} "
            f"| {item.get('source', '')} | {item.get('title_en', '')} "
            f"| {item.get('reason', '')} | {item.get('revisit_when', '')} |"
        )
    return "\n".join(out) + "\n"


def render_audit(result: dict[str, Any] | None = None, show_gaps: int = 12) -> str:
    result = result or audit()
    metrics = result["metrics"]
    out: list[str] = []
    out.append("# Cycle audit · 循环审计")
    out.append("")
    out.append(
        f"**{'OK' if result['ok'] else 'PROBLEMS'}** · {metrics['cycles']} cycles · "
        f"{metrics['roadmap']} roadmap items · {metrics['capabilities']} capabilities · "
        f"{metrics['clauses_anchored']} clauses anchored"
    )
    out.append("")
    out.append("## Problems (hard) · 硬问题")
    if result["problems"]:
        for problem in result["problems"]:
            out.append(f"- {problem}")
    else:
        out.append("- none")
    out.append("")
    out.append(f"## Gaps (soft, the next-cycle worklist) · 缺口（下一轮输入）: {len(result['gaps'])}")
    for gap in result["gaps"][:show_gaps]:
        out.append(f"- {gap}")
    if len(result["gaps"]) > show_gaps:
        out.append(f"- ... {len(result['gaps']) - show_gaps} more (`harness cycle audit --json`)")
    return "\n".join(out) + "\n"
