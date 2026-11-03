"""Trend-review scaffold (P69): the standing routine work the loop could never do -
turning this run's intelligence stream into the *raw material* of a periodic
industry/literature review.

Routine asked by the user (2026-11-03): after every full update, write (a) an
AI-industry and adjacent-field trend analysis, (b) a harness-direction literature
review, (c) a survey of other interesting/promising AI directions - complete,
primary-source grounded, dialectical about the frontier, bilingual.

Division of labor (M0.4 - the engine aggregates, it never opines):

* this module = deterministic aggregation over ``updates/intel.jsonl``: items are
  bucketed into the four review clusters by their tracked topics, scored, and
  emitted as a provenance table (title · source · date · link per row);
* the ANALYSIS itself (trend reading, literature synthesis, dialectics) is written
  by a human or agent into ``review/trend-review-<date>.md`` - every factual claim
  must resolve to a primary source (citations-lifeline), which is exactly why the
  scaffold carries links, not summaries.

``harness full-update`` runs the aggregation as its final phase, so the scaffold
regenerates automatically every round; the writing procedure is the standing task
registered in ``tasks/PLAN.md`` (§Routine) and ``AGENTS.md`` §6.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any

INTEL_REL = "updates/intel.jsonl"
REPORT_REL = "updates/TREND.md"
#: The committed bridge between the (untracked) live stream and the CI-built page:
#: ``harness trend --write`` refreshes this from updates/intel.jsonl on the dev
#: machine; ``harness pages`` reads it so GitHub Pages renders the trend section
#: from checked-in data alone (updates/ never enters version control).
SNAPSHOT_NAME = "trend-snapshot.json"

#: Review clusters, in emission order. An item counts in EVERY cluster whose topics
#: it carries (breadth, not partition -- a harness paper tagged with several topics
#: shows up under each theme it actually touches), so cluster counts may exceed the
#: item total by design; ``untracked`` counts items that match no cluster at all.
#: The cluster ids are stable keys for tests and for the writer's section anchors.
CLUSTERS: list[dict[str, Any]] = [
    {
        "id": "industry",
        "title_en": "AI industry & adjacent fields · 全行业与相关领域趋势",
        "topics": {"mcp-skills-ecosystem", "ai-tool-stack",
                   "scholarly-infrastructure", "scholarly-discovery"},
    },
    {
        "id": "harness",
        "title_en": "Harness directions - literature review · harness 方向文献综述",
        "topics": {"agent-harness", "self-evolving-agents", "context-engineering",
                   "agent-memory", "evaluation-gates", "provenance-integrity",
                   "multi-agent-collaboration", "agent-skills-tools"},
    },
    {
        "id": "trajectories",
        "title_en": "Other promising trajectories · 其他有趣且有潜力的方向",
        "topics": {"deep-research", "retrieval-grounding", "ambition-and-agency",
                   "research-evaluation", "citation-integrity"},
    },
    {
        "id": "domains",
        "title_en": "Field-by-field signals · 各学科领域信号",
        "topics": {"physics", "chemistry", "biology", "medicine", "earth-environment",
                   "mathematics", "statistics", "computer-science", "economics-finance",
                   "psychology", "social-science", "law", "humanities", "education",
                   "arts-design", "linguistics", "digital-humanities",
                   "cognitive-science", "classical-texts-dh"},
    },
]


def _load_intel(root: str | Path) -> list[dict[str, Any]]:
    path = Path(root) / INTEL_REL
    if not path.exists():
        return []
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue  # unreadable lines are counted, never hidden
        if isinstance(obj, dict):
            items.append(obj)
    return items


def aggregate(items: list[dict[str, Any]], *, top: int = 15,
              recent_days: int = 30, now: str | None = None) -> dict[str, Any]:
    """Bucket intel items into the review clusters (pure, injectable)."""
    ref = now or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
    try:
        ref_date = _dt.date.fromisoformat(ref[:10])
    except ValueError:
        ref_date = _dt.date.today()
    horizon = (ref_date - _dt.timedelta(days=recent_days)).isoformat()

    buckets = {c["id"]: [] for c in CLUSTERS}
    untracked = 0
    for it in items:
        topics = set(it.get("topics") or [])
        matched = False
        for cluster in CLUSTERS:
            if topics & cluster["topics"]:
                buckets[cluster["id"]].append(it)
                matched = True  # multi-membership: keep checking the other clusters
        if not matched:
            untracked += 1

    def _pack(rows: list[dict[str, Any]]) -> dict[str, Any]:
        recent = [r for r in rows if (r.get("published") or "")[:10] >= horizon]
        recent.sort(key=lambda r: (-(r.get("relevance") or 0.0),
                                   r.get("published") or ""), reverse=False)
        return {
            "count": len(rows),
            "recent": len(recent),
            "entities": sorted({r.get("entity_name") or r.get("entity") or "?"
                                for r in rows}),
            "top": recent[:top],
        }

    return {
        "generated": ref,
        "horizon": horizon,
        "items": len(items),
        "untracked": untracked,
        "clusters": {c["id"]: _pack(buckets[c["id"]]) for c in CLUSTERS},
    }


def render(model: dict[str, Any]) -> str:
    by_id = {c["id"]: c for c in CLUSTERS}
    lines = [
        "TREND-REVIEW scaffold · 趋势综述脚手架",
        "",
        f"generated={model['generated']}  ·  intel items={model['items']}"
        f"  ·  30d horizon={model['horizon']}  ·  untracked={model['untracked']}",
        "",
        "> 中文速览：本文件是**例行工作的原材料**，不是分析本身。每次 full-update 自动重生成："
        "四个综述簇的近期条目（按相关度排序、带出处链接）。分析（行业趋势判断、harness 文献综述、"
        "有趣方向梳理、前沿辩证）须由人或 agent 写入 `review/trend-review-<date>.md`，"
        "每条形实声明回一手源（引用即生命线）；无分析=未完成（M5.11 证伪检查）。「其他/未见簇」"
        "条目是脱管信号，先核再入册。",
        "> This scaffold is raw material, not analysis: the engine aggregates and cites; the review is authored.",
        "",
    ]
    for cid, pack in model["clusters"].items():
        cluster = by_id[cid]
        lines.append(f"## {cluster['title_en']}")
        lines.append("")
        lines.append(f"items={pack['count']}  recent(30d)={pack['recent']}  "
                     f"sources={len(pack['entities'])}")
        lines.append("")
        if pack["top"]:
            lines.append("| rel | published | source | title | link |")
            lines.append("|---|---|---|---|---|")
            for r in pack["top"]:
                title = (r.get("title") or "").replace("|", "/")
                lines.append(
                    f"| {r.get('relevance', 0):.1f} | {(r.get('published') or '?')[:10]}"
                    f" | {r.get('entity_name') or r.get('entity') or '?'}"
                    f" | {title} | {r.get('url') or ''} |"
                )
        else:
            lines.append("_no scored items this window · 本窗口无命中条目_")
        lines.append("")
    lines.append("## Method · 写法（例行规程）")
    lines.append("")
    lines.append(
        "1. 复制四簇结构到 `review/trend-review-<date>.md`（中英双语；信息无损、准确典雅简明）。"
    )
    lines.append(
        "2. 每条要引用的形实声明：回一手源核验（官方仓库/规范/arXiv 原文），带访问日期；未核验标 *unverified*。"
    )
    lines.append(
        "3. 辩证面：每个被看好的方向给出最强反例/局限（如本仓库 GraphRAG 维护模式先例）；区分「趋势」与「声量」。"
    )
    lines.append(
        "4. harness 文献综述优先引用仓库既有参考库（`review/references.md` R1–R281+），新增文献按 §Q… 分节续编。"
    )
    lines.append(
        "5. 新来源/新实体过 tool-router §5 入表门后入 `sources.json`（人审 M0.8）。"
    )
    lines.append("")
    lines.append(
        "Human gate · 人工裁决：脚手架只聚合不改写（M4）；分析质量与引证由撰写者负责。"
    )
    return "\n".join(lines)


def to_snapshot(model: dict[str, Any], *, top: int = 8) -> dict[str, Any]:
    """Compact, committed-friendly roll-up of the aggregate (for the CI page).
    Keeps only the counts, source breadth, and the top rows per cluster."""
    by_id = {c["id"]: c for c in CLUSTERS}
    snap: dict[str, Any] = {
        "generated": model["generated"],
        "horizon": model["horizon"],
        "items": model["items"],
        "untracked": model["untracked"],
        "clusters": {},
    }
    for cid, pack in model["clusters"].items():
        snap["clusters"][cid] = {
            "title": by_id[cid]["title_en"],
            "count": pack["count"],
            "recent": pack["recent"],
            "sources": len(pack["entities"]),
            "top": [
                {
                    "rel": round(float(r.get("relevance") or 0.0), 1),
                    "date": (r.get("published") or "?")[:10],
                    "source": r.get("entity_name") or r.get("entity") or "?",
                    "title": (r.get("title") or "").strip(),
                    "url": r.get("url") or "",
                }
                for r in pack["top"][:top]
            ],
        }
    return snap


def snapshot_path() -> Path:
    return Path(__file__).resolve().parent / "data" / SNAPSHOT_NAME


def save_snapshot(snap: dict[str, Any]) -> Path:
    path = snapshot_path()
    path.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_snapshot() -> dict[str, Any] | None:
    path = snapshot_path()
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def run(
    root: str | Path,
    *,
    write: bool = False,
    top: int = 15,
    snapshot_top: int = 8,
    commit_snapshot: bool = False,
) -> dict[str, Any]:
    """Aggregate the run's intel stream into the review scaffold.

    ``write`` emits ``updates/TREND.md`` under *root* (the local raw material, always
    contained to the knowledge home). ``commit_snapshot`` additionally refreshes the
    committed ``data/trend-snapshot.json`` bridge -- set only by the operator's
    ``harness trend --write`` (the close-out ritual), never by ``full-update``, which
    must not mutate the SSOT."""
    model = aggregate(_load_intel(root), top=top)
    out: dict[str, Any] = {"clusters": {c: p["count"] for c, p in model["clusters"].items()},
                          "untracked": model["untracked"], "items": model["items"],
                          "recent_30d": {c: p["recent"] for c, p in model["clusters"].items()}}
    if write:
        path = Path(root) / REPORT_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(model), encoding="utf-8")
        out["wrote"] = REPORT_REL
    if commit_snapshot:
        out["snapshot_wrote"] = save_snapshot(to_snapshot(model, top=snapshot_top)).name
    return out
