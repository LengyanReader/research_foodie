"""Append-only journal, report, and proposal writers for the refresh loop.

Everything the loop produces is a reviewable file; nothing here mutates the
catalogs (M0.4/M0.8/M0.9). Accepting a candidate only writes a *proposal* stub a
human then merges.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path
from typing import Any

from .collect import Candidate
from .curate import Audited


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (slug or "candidate")[:60]


def append_journal(path: str | Path, lines: list[str]) -> None:
    """Append timestamped lines to an append-only journal (never rewrites)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stamp = _now()
    with p.open("a", encoding="utf-8") as fh:
        for line in lines:
            fh.write(f"- {stamp}  {line}\n")


def write_queue(path: str | Path, audited: list[Audited]) -> None:
    """Write accepted candidates as a pending JSONL queue."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        for item in audited:
            if not item.accepted:
                continue
            row = item.candidate.to_dict()
            row["status"] = "pending"
            row["score"] = round(item.score, 2)
            row["reasons"] = item.reasons
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_queue(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def save_queue(path: str | Path, rows: list[dict[str, Any]]) -> None:
    p = Path(path)
    with p.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_report(
    path: str | Path,
    audited: list[Audited],
    trend: dict[str, Any],
    watchlist: dict[str, Any],
    run: dict[str, Any],
) -> None:
    """Write the human-facing refresh report (bilingual)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    accepted = [a for a in audited if a.accepted]
    rejected = [a for a in audited if not a.accepted]

    lines: list[str] = []
    lines.append("# Refresh report · 更新报告")
    lines.append("")
    lines.append(f"**Generated:** {run.get('created', _now())}  ")
    lines.append(f"**Cadence:** {watchlist.get('cadence', 'n/a')}  ")
    lines.append(
        f"**Providers:** {', '.join(run.get('providers', [])) or 'none'}  "
        f"**Since:** {run.get('since') or 'any'}"
    )
    lines.append("")
    lines.append("> 中文速览：以下为本轮自主检索到的新候选来源（仅提案，未经人工确认不写入正文）。")
    lines.append("> 热点/趋势见下方 Hot topics；尚未覆盖的主题见 Coverage gaps。")
    lines.append("")
    lines.append("## Summary · 概览")
    lines.append("")
    lines.append(f"- Accepted (new, traceable): **{trend['accepted']}**")
    lines.append(f"- Rejected (dup/untraceable): **{trend['rejected']}**")
    lines.append(f"- Known ids in corpus: **{trend['known_ids']}**")
    lines.append("")

    lines.append("## Hot topics · 热点")
    lines.append("")
    if trend["hot_topics"]:
        lines.append("| topic | hits |")
        lines.append("|---|---|")
        for row in trend["hot_topics"]:
            lines.append(f"| {row['topic']} | {row['count']} |")
    else:
        lines.append("_(none this run)_")
    lines.append("")

    lines.append("## Coverage gaps · 覆盖缺口")
    lines.append("")
    gaps = trend.get("coverage_gaps") or []
    lines.append(", ".join(gaps) if gaps else "_(full coverage this run)_")
    lines.append("")

    lines.append("## Frontier probes · 边界探测")
    lines.append("")
    probes = trend.get("frontier_probes") or []
    lines.append("\n".join(f"- {q}" for q in probes) if probes else "_(none)_")
    lines.append("")

    lines.append("## Accepted candidates · 采纳候选")
    lines.append("")
    if accepted:
        lines.append("| score | kind | title | id/url |")
        lines.append("|---|---|---|---|")
        for item in accepted:
            c = item.candidate
            ref = c.external_id or c.url
            lines.append(f"| {item.score:.1f} | {c.kind} | {c.title} | {ref} |")
    else:
        lines.append("_(none)_")
    lines.append("")

    lines.append("## Rejected · 已剔除")
    lines.append("")
    for item in rejected[:50]:
        c = item.candidate
        why = "; ".join(item.reasons) or "rejected"
        lines.append(f"- {c.title or '(untitled)'} — {why}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Accept with: `harness refresh-apply --root . --accept <id|url> ...`")
    p.write_text("\n".join(lines), encoding="utf-8")


def write_proposal(root: str | Path, row: dict[str, Any]) -> Path:
    """Write a single reviewable proposal stub for an accepted candidate."""
    proposals = Path(root) / "updates" / "proposals"
    proposals.mkdir(parents=True, exist_ok=True)
    cand = Candidate.from_dict(row)
    ref = cand.external_id or cand.url or "(missing)"
    slug = _slug(cand.title or ref)
    target = proposals / f"{slug}.md"
    body = [
        f"# Proposal: {cand.title or '(untitled)'}",
        "",
        f"- **Kind:** {cand.kind}",
        f"- **Topics:** {', '.join(cand.topics) or 'n/a'}",
        f"- **Published:** {cand.published or 'unknown'}",
        f"- **Reference:** {ref}",
        f"- **Source:** {cand.source_kind}  ·  **Retrieved:** {cand.retrieved_at}",
        f"- **Verified:** {cand.verified}",
        "",
        "## Summary",
        "",
        cand.summary or "_(no summary provided)_",
        "",
        "## Suggested merge targets (human applies)",
        "",
        "- [ ] `review/references.md` (+ `review/references.bib`)",
        "- [ ] `review/harness-catalog.md` or `review/ai-harness-survey.md`",
        "- [ ] `src/harness_factory/data/modules.json` / `domains.json` (if it changes a rule)",
        "",
    ]
    target.write_text("\n".join(body), encoding="utf-8")
    return target
