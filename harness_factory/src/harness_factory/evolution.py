"""Complete self-evolution cycle: **snapshot -> audit -> mutation-proposal -> journal**.

Distinct from :mod:`harness_factory.refresh` (which hunts for new *sources*): the
evolution pass inspects the registry and its own outputs and proposes *structural*
changes — cover uncovered watchlist topics, populate empty groups, review stale
entities — and records a metric snapshot so drift/cadence is observable
(M0.5 SSOT, M0.10 Evolvable).

Nothing here edits the tracked catalogs (M0.4). Proposals land in
``updates/evolution.jsonl`` + ``updates/EVOLUTION.md``. A human applies with
``evolution-apply``, which only writes ``updates/accepted.json`` — reversible, M0.9.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .collect import iter_entities
from .journal import append_journal, load_queue


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def _host(url: str) -> str:
    match = re.match(r"https?://([^/]+)/?", url or "")
    return match.group(1).lower() if match else ""


@dataclass
class Audit:
    kind: str  # uncovered_topic | empty_group | stale_source
    subject: str
    detail: str
    severity: str = "low"  # low | medium | high


@dataclass
class Proposal:
    id: str
    action: str  # add_source | populate_group | retire_or_refresh
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    severity: str = "low"
    status: str = "proposed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _pid(action: str, target: str) -> str:
    digest = hashlib.sha1(f"{action}:{target}".encode("utf-8")).hexdigest()[:8]
    return f"mut-{digest}"


def snapshot(
    sources: dict[str, Any],
    watchlist: dict[str, Any],
    intel_items: list[Any] | None = None,
) -> dict[str, Any]:
    """Compute observable metrics for one evolution tick."""
    intel_items = intel_items or []
    entities = iter_entities(sources)
    groups: dict[str, int] = {}
    for group, _entity in entities:
        groups[group] = groups.get(group, 0) + 1

    topic_ids = [t["id"] for t in watchlist.get("topics", [])]
    covered = {t for _g, e in entities for t in e.get("topics", [])}
    uncovered = [t for t in topic_ids if t not in covered]
    coverage = (len(topic_ids) - len(uncovered)) / len(topic_ids) if topic_ids else 1.0
    return {
        "entities": len(entities),
        "groups": groups,
        "topics": len(topic_ids),
        "uncovered_topics": uncovered,
        "topic_coverage": round(coverage, 3),
        "intel_items": len(intel_items),
    }


def audit(
    sources: dict[str, Any],
    watchlist: dict[str, Any],
    intel_items: list[Any] | None = None,
    seen_entities: set[str] | None = None,
    metrics: dict[str, Any] | None = None,
    queue_rows: list[dict[str, Any]] | None = None,
) -> list[Audit]:
    """Detect structural gaps from the registry + this run's intel + accepted queue."""
    metrics = metrics or snapshot(sources, watchlist, intel_items)
    out: list[Audit] = []

    for topic in metrics.get("uncovered_topics", []):
        out.append(Audit("uncovered_topic", topic, f"No tracked source covers '{topic}'.", "high"))

    for group, entries in sources.get("groups", {}).items():
        if not entries:
            out.append(Audit("empty_group", group, f"Source group '{group}' is empty.", "medium"))

    seen = seen_entities or set()
    if seen:
        for _group, entity in iter_entities(sources):
            has_feed = entity.get("feed") or entity.get("resolve") == "youtube"
            if has_feed and entity.get("id") not in seen:
                out.append(
                    Audit(
                        "stale_source",
                        entity.get("id", ""),
                        f"No new items from '{entity.get('name')}' this run.",
                        "low",
                    )
                )

    # Discovery -> registry: accepted candidates from sources not yet tracked.
    if queue_rows:
        known = {_host(e.get("url", "")) for _g, e in iter_entities(sources)}
        known.discard("")
        seen_hosts: set[str] = set()
        for row in queue_rows:
            host = _host(row.get("url", ""))
            if host and host not in known and host not in seen_hosts:
                seen_hosts.add(host)
                out.append(
                    Audit(
                        "untracked_source",
                        host,
                        f"Accepted candidate from untracked source '{host}'.",
                        "medium",
                    )
                )
    return out


def propose(audits: list[Audit]) -> list[Proposal]:
    """Map audits to human-gated mutation proposals."""
    out: list[Proposal] = []
    for a in audits:
        if a.kind == "uncovered_topic":
            out.append(
                Proposal(
                    _pid("add_source", a.subject),
                    "add_source",
                    a.subject,
                    {"topic": a.subject, "suggest": f"Track a source covering '{a.subject}'."},
                    a.detail,
                    a.severity,
                )
            )
        elif a.kind == "empty_group":
            out.append(
                Proposal(
                    _pid("populate_group", a.subject),
                    "populate_group",
                    a.subject,
                    {"group": a.subject},
                    a.detail,
                    a.severity,
                )
            )
        elif a.kind == "stale_source":
            out.append(
                Proposal(
                    _pid("review_source", a.subject),
                    "retire_or_refresh",
                    a.subject,
                    {"entity": a.subject},
                    a.detail,
                    a.severity,
                )
            )
        elif a.kind == "untracked_source":
            out.append(
                Proposal(
                    _pid("track_source", a.subject),
                    "add_source",
                    a.subject,
                    {"host": a.subject, "suggest": "Add this source to data/sources.json."},
                    a.detail,
                    a.severity,
                )
            )
    return out


def _seen(intel_items: list[Any]) -> set[str]:
    seen: set[str] = set()
    for item in intel_items:
        entity = getattr(item, "entity", None)
        if entity is None and isinstance(item, dict):
            entity = item.get("entity", "")
        if entity:
            seen.add(str(entity))
    return seen


def load_intel(root: str | Path) -> list[dict[str, Any]]:
    path = Path(root) / "updates" / "intel.jsonl"
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def run_evolution(
    root: str | Path,
    sources: dict[str, Any],
    watchlist: dict[str, Any],
    intel_items: list[Any] | None = None,
    queue_rows: list[dict[str, Any]] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """One full evolution tick; returns a summary (no catalogs touched)."""
    root = Path(root)
    if intel_items is None:
        intel_items = load_intel(root)
    if queue_rows is None:
        queue_rows = load_queue(root / "updates" / "queue.jsonl")

    metrics = snapshot(sources, watchlist, intel_items)
    audits = audit(sources, watchlist, intel_items, _seen(intel_items), metrics, queue_rows)
    proposals = propose(audits)

    created = _now()
    summary = {
        "created": created,
        "metrics": metrics,
        "audits": [asdict(a) for a in audits],
        "proposals": [p.to_dict() for p in proposals],
        "n_audits": len(audits),
        "n_proposals": len(proposals),
    }

    if dry_run:
        return summary

    updates = root / "updates"
    updates.mkdir(parents=True, exist_ok=True)
    _write_proposals(updates / "evolution.jsonl", proposals)
    _append_metrics(updates / "metrics.jsonl", created, metrics)
    write_evolution_report(updates / "EVOLUTION.md", summary, watchlist)
    append_journal(
        updates / "JOURNAL.md",
        [
            f"evolve entities={metrics['entities']} coverage={metrics['topic_coverage']} "
            f"audits={len(audits)} proposals={len(proposals)}",
        ],
    )
    return summary


def _write_proposals(path: Path, proposals: list[Proposal]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for proposal in proposals:
            fh.write(json.dumps(proposal.to_dict(), ensure_ascii=False) + "\n")


def _append_metrics(path: Path, created: str, metrics: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"created": created, **metrics}, ensure_ascii=False) + "\n")


def write_evolution_report(
    path: str | Path, summary: dict[str, Any], watchlist: dict[str, Any]
) -> None:
    metrics = summary["metrics"]
    proposals = summary["proposals"]
    lines: list[str] = []
    lines.append("# Evolution report · 自演化报告")
    lines.append("")
    lines.append(f"**Generated:** {summary['created']}  ·  **Cadence:** {watchlist.get('cadence', 'n/a')}")
    lines.append("")
    lines.append("> 中文速览：对来源注册表与自身产出的**结构审计**（主题覆盖、空分组、停滞来源），")
    lines.append("> 以及对应的**变更提案**。提案仅供人工确认，本工具不直接改写注册表。")
    lines.append("")

    lines.append("## Metrics · 指标")
    lines.append("")
    lines.append(f"- Entities: **{metrics['entities']}**  ·  Topics: **{metrics['topics']}**")
    lines.append(f"- Topic coverage: **{metrics['topic_coverage']:.0%}**  ·  Intel items this run: **{metrics['intel_items']}**")
    if metrics.get("groups"):
        lines.append("- Groups: " + ", ".join(f"{g}={n}" for g, n in metrics["groups"].items()))
    if metrics.get("uncovered_topics"):
        lines.append("- Uncovered: " + ", ".join(metrics["uncovered_topics"]))
    lines.append("")

    lines.append("## Audits · 审计")
    lines.append("")
    audits = summary.get("audits", [])
    if audits:
        lines.append("| severity | kind | subject | detail |")
        lines.append("|---|---|---|---|")
        for a in audits:
            lines.append(f"| {a['severity']} | {a['kind']} | {a['subject']} | {a['detail']} |")
    else:
        lines.append("_(no gaps detected)_")
    lines.append("")

    lines.append("## Proposals · 变更提案")
    lines.append("")
    if proposals:
        lines.append("| id | action | target | severity | rationale |")
        lines.append("|---|---|---|---|---|")
        for p in proposals:
            lines.append(
                f"| {p['id']} | {p['action']} | {p['target']} | {p['severity']} | {p['rationale']} |"
            )
    else:
        lines.append("_(nothing to propose)_")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Accept with: `harness evolve-apply --root . --accept <id|target> ...`")
    path.write_text("\n".join(lines), encoding="utf-8")


def load_proposals(root: str | Path) -> list[dict[str, Any]]:
    path = Path(root) / "updates" / "evolution.jsonl"
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def apply_accepted(root: str | Path, accept: list[str]) -> list[str]:
    """Human-gated apply: mark proposals accepted in ``updates/accepted.json``.

    ``accept`` matches a proposal's id or target. Reversible: only the accepted
    ledger is written, never the tracked catalogs.
    """
    root = Path(root)
    rows = load_proposals(root)
    wanted = {a.strip().lower() for a in accept if a.strip()}
    applied: list[dict[str, Any]] = []

    for row in rows:
        keys = {str(row.get("id", "")).lower(), str(row.get("target", "")).lower()}
        if wanted & {k for k in keys if k}:
            row["status"] = "accepted"
            row["accepted_at"] = _now()
            applied.append(row)

    if applied:
        ledger = root / "updates" / "accepted.json"
        existing: dict[str, dict[str, Any]] = {}
        if ledger.exists():
            for item in json.loads(ledger.read_text(encoding="utf-8")):
                existing[item.get("id", "")] = item
        for row in applied:
            existing[row["id"]] = row
        ledger.parent.mkdir(parents=True, exist_ok=True)
        ledger.write_text(
            json.dumps(list(existing.values()), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        append_journal(
            root / "updates" / "JOURNAL.md",
            [f"evolve-apply accepted={len(applied)}: " + "; ".join(r["id"] for r in applied)],
        )
    return [row["id"] for row in applied]
