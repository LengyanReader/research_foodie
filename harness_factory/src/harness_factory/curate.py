"""Audit, dedupe, score, rank, and trend-analyze candidate sources.

This is the observe/record/rank half of M5: it may drop untraceable items and
order the rest, but it never edits the catalogs or invents content (M0.4).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .collect import Candidate

_ARXIV_RE = re.compile(r"\b(\d{4}\.\d{4,5})\b")
_DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"'<>]+)")
_URL_RE = re.compile(r"https?://[^\s\"'<>)\]]+")


def extract_keys(text: str) -> set[str]:
    """Pull arXiv ids, DOIs, and URLs out of a blob of text (for dedupe)."""
    keys: set[str] = set()
    for match in _ARXIV_RE.findall(text):
        keys.add(match.lower())
    for match in _DOI_RE.findall(text):
        keys.add(match.lower())
    for match in _URL_RE.findall(text):
        keys.add(match.rstrip("/").lower())
    return keys


def known_keys(paths: list[str | Path]) -> set[str]:
    """Union of ids/urls already present in the given corpus files."""
    keys: set[str] = set()
    for path in paths:
        p = Path(path)
        if p.exists():
            try:
                keys |= extract_keys(p.read_text(encoding="utf-8"))
            except OSError:
                continue
    return keys


def _candidate_keys(cand: Candidate) -> set[str]:
    keys: set[str] = set()
    if cand.external_id:
        keys |= extract_keys(cand.external_id) or {cand.external_id.strip().lower()}
    if cand.url:
        keys.add(cand.url.rstrip("/").lower())
    return keys


@dataclass
class Audited:
    candidate: Candidate
    accepted: bool
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    duplicate: bool = False


def audit(cand: Candidate, known: set[str], topic_keywords: dict[str, set[str]]) -> Audited:
    """Decide whether a candidate is traceable and how relevant it is."""
    reasons: list[str] = []
    keys = _candidate_keys(cand)

    if not cand.title:
        reasons.append("drop: no title")
    if not keys:
        reasons.append("drop: no url or external_id (untraceable, M4)")
        return Audited(cand, accepted=False, reasons=reasons)

    if keys & known:
        return Audited(cand, accepted=False, duplicate=True, reasons=["dup: already in corpus"])

    score = 0.0
    text = f"{cand.title} {cand.summary}".lower()
    for topic in cand.topics:
        kws = topic_keywords.get(topic, set())
        hits = sum(1 for kw in kws if kw and kw.lower() in text)
        score += 1.0 + 0.5 * hits
    if cand.kind == "paper":
        score += 0.5
    if cand.published[:4].isdigit() and int(cand.published[:4]) >= 2024:
        score += 0.5

    if not cand.verified:
        reasons.append("unverified: url not checked")

    accepted = "drop: no title" not in reasons
    return Audited(cand, accepted=accepted, score=score, reasons=reasons)


def topic_keywords(watchlist: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for topic in watchlist.get("topics", []):
        kws = set(topic.get("keywords", []))
        kws |= {topic.get("id", ""), topic.get("name_zh", "")}
        out[topic.get("id", "")] = {k for k in kws if k}
    return out


def curate(
    candidates: list[Candidate],
    known: set[str],
    watchlist: dict[str, Any],
) -> list[Audited]:
    """Audit + dedupe (in-run and vs corpus) + rank, best first."""
    kws = topic_keywords(watchlist)
    seen: set[str] = set()
    audited: list[Audited] = []
    for cand in candidates:
        keys = _candidate_keys(cand)
        if keys & seen:
            audited.append(Audited(cand, accepted=False, duplicate=True, reasons=["dup: in run"]))
            continue
        result = audit(cand, known, kws)
        seen |= keys
        audited.append(result)
    audited.sort(key=lambda a: (a.accepted, a.score), reverse=True)
    return audited


def trends(
    audited: list[Audited],
    watchlist: dict[str, Any],
    known: set[str],
) -> dict[str, Any]:
    """Summarize hot topics (frequent + recent) and coverage gaps."""
    accepted = [a for a in audited if a.accepted]
    counts: dict[str, int] = {}
    for a in accepted:
        for topic in a.candidate.topics:
            counts[topic] = counts.get(topic, 0) + 1

    declared = [t.get("id", "") for t in watchlist.get("topics", [])]
    hot = sorted(
        ({"topic": t, "count": c} for t, c in counts.items()),
        key=lambda d: d["count"],
        reverse=True,
    )
    gaps = [t for t in declared if counts.get(t, 0) == 0]

    frontier = [p.get("query", "") for p in watchlist.get("frontier_probes", [])]
    return {
        "accepted": len(accepted),
        "rejected": len(audited) - len(accepted),
        "hot_topics": hot,
        "coverage_gaps": gaps,
        "frontier_probes": frontier,
        "known_ids": len(known),
    }
