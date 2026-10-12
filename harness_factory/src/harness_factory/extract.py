"""Extract "useful info" (intel) from tracked sources.

Deterministic by default: relevance scoring + entity/topic tagging + a one-line
brief drawn from the item's *own* title/summary. An optional LLM summary can be
enabled, but this module never invents facts (M0.4): without an LLM the brief is
a verbatim excerpt, not a paraphrase.
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from .collect import Candidate, iter_entities
from .curate import topic_keywords

_GROUP_TITLES = {
    "projects": "Projects & labs · 项目与机构",
    "harnesses": "Vendor harnesses · 厂商 Harness / SDK / 协议",
    "venues": "Venues & papers · 刊物与论文",
    "people": "Leading figures · 领军人物与言行",
    "media": "Self-media · 自媒体",
}

_GROUP_ORDER = ("projects", "harnesses", "venues", "people", "media")


@dataclass
class IntelItem:
    title: str
    url: str
    entity: str
    entity_name: str
    group: str
    kind: str
    topics: list[str] = field(default_factory=list)
    published: str = ""
    relevance: float = 0.0
    signals: list[str] = field(default_factory=list)
    brief: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def entity_index(sources: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    """Map ``entity id -> (group, entity)``."""
    return {e.get("id", ""): (group, e) for group, e in iter_entities(sources)}


def _recency(published: str) -> float:
    if not published or len(published) < 4 or not published[:4].isdigit():
        return 0.0
    year = int(published[:4])
    if year >= 2026:
        return 1.0
    if year == 2025:
        return 0.6
    if year == 2024:
        return 0.3
    return 0.0


def extract_one(
    cand: Candidate,
    entity: dict[str, Any],
    group: str,
    kws: dict[str, set[str]],
) -> IntelItem:
    text = f"{cand.title} {cand.summary}".lower()
    score = 0.0
    signals: list[str] = []

    for topic in entity.get("topics", []):
        for kw in kws.get(topic, set()):
            if kw and kw.lower() in text:
                score += 0.5
                signals.append(f"kw:{kw}")
    name = (entity.get("name") or "").lower()
    if name and name in text:
        score += 0.5
        signals.append(f"entity:{entity.get('id', '')}")
    score += _recency(cand.published)
    if cand.published:
        signals.append(f"date:{cand.published}")

    brief = (cand.summary or cand.title or cand.url)[:240]
    return IntelItem(
        title=cand.title,
        url=cand.url,
        entity=cand.entity,
        entity_name=entity.get("name", cand.entity),
        group=group,
        kind=cand.kind,
        topics=[str(t) for t in entity.get("topics", [])],
        published=cand.published,
        relevance=round(score, 2),
        signals=sorted(set(signals)),
        brief=brief,
    )


def extract_intel(
    candidates: list[Candidate],
    sources: dict[str, Any],
    watchlist: dict[str, Any],
    enrich: Callable[[str], str | None] | None = None,
) -> list[IntelItem]:
    """Turn candidates into ranked intel items (best first)."""
    idx = entity_index(sources)
    kws = topic_keywords(watchlist)
    items: list[IntelItem] = []
    for cand in candidates:
        group, entity = idx.get(
            cand.entity,
            ("", {"id": cand.entity, "name": cand.entity, "topics": cand.topics}),
        )
        items.append(extract_one(cand, entity, group, kws))
    items.sort(key=lambda i: i.relevance, reverse=True)

    if enrich is not None:
        for item in items:
            summary = enrich(f"{item.title}. {item.brief}")
            if summary:
                item.brief = summary
    return items


def write_intel(root: str | Path, items: list[IntelItem], created: str | None = None) -> None:
    """Write ``updates/intel.jsonl`` (snapshot) and ``updates/INTEL.md`` (human report)."""
    updates = Path(root) / "updates"
    updates.mkdir(parents=True, exist_ok=True)
    created = created or _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()

    with (updates / "intel.jsonl").open("w", encoding="utf-8") as fh:
        for item in items:
            fh.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")

    lines = ["# Intel report · 情报提取", ""]
    lines.append(f"**Generated:** {created}  ·  **Items:** {len(items)}")
    lines.append("")
    lines.append("> 中文速览：按跟踪对象汇总的**新条目**（项目/机构、刊物/论文、领军人物、自媒体）。")
    lines.append("> 每条含相关度、标签与**原文摘录**（未经 LLM 时不改写，M4）。")
    lines.append("")

    by_group: dict[str, list[IntelItem]] = {}
    for item in items:
        by_group.setdefault(item.group, []).append(item)

    for group in _GROUP_ORDER:
        group_items = by_group.get(group, [])
        lines.append(f"## {_GROUP_TITLES.get(group, group)}")
        lines.append("")
        if not group_items:
            lines.append("_(none this run)_")
            lines.append("")
            continue
        lines.append("| rel | entity | title | date | link |")
        lines.append("|---|---|---|---|---|")
        for item in group_items:
            lines.append(
                f"| {item.relevance:.1f} | {item.entity_name} | {item.title} "
                f"| {item.published or '—'} | {item.url} |"
            )
        lines.append("")

    (updates / "INTEL.md").write_text("\n".join(lines), encoding="utf-8")


def load_intel(root: str | Path) -> list[dict[str, Any]]:
    path = Path(root) / "updates" / "intel.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
