"""The self-update (refresh) orchestrator.

Loop shape (M5): **signal -> audit -> mutation-proposal -> journal**, with a hard
human gate. This module never edits the catalogs; it writes:

    updates/queue.jsonl       accepted candidates, pending human review
    updates/REPORT.md         bilingual human report (hot topics, gaps)
    updates/JOURNAL.md        append-only log of every run
    updates/proposals/*.md    per-accepted-candidate merge stubs (on apply)
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any, Callable

from .collect import (
    Candidate,
    collect,
    feed_provider,
    file_provider,
    llm_provider,
    resolve_youtube_feed,
    verify_url,
)
from .curate import Audited, curate, known_keys, trends
from .extract import extract_intel, write_intel
from .journal import append_journal, load_queue, save_queue, write_proposal, write_queue, write_report
from . import config
from .registry import data_dir

_CORPUS = (
    "references.md",
    "references.bib",
    "harness-catalog.md",
    "ai-harness-survey.md",
    "masters-playbook.md",
)


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def load_watchlist(path: str | Path | None = None) -> dict[str, Any]:
    target = Path(path) if path else data_dir() / "watchlist.json"
    return json.loads(target.read_text(encoding="utf-8"))


def load_sources(path: str | Path | None = None) -> dict[str, Any]:
    target = Path(path) if path else data_dir() / "sources.json"
    return json.loads(target.read_text(encoding="utf-8"))


def default_providers(
    inbox: str | Path,
    since: str | None,
    max_items: int,
    discover: Callable[..., list[dict[str, Any]]] | None = None,
    sources: dict[str, Any] | None = None,
    feed: bool = False,
) -> tuple[list[Callable[[dict[str, Any]], list[Candidate]]], list[str]]:
    providers: list[Callable[[dict[str, Any]], list[Candidate]]] = []
    names: list[str] = []
    providers.append(file_provider(inbox))
    names.append("file")
    if feed and sources is not None:
        providers.append(feed_provider(sources, resolver=resolve_youtube_feed))
        names.append("feed")
    if discover is not None:
        providers.append(llm_provider(since=since, max_items=max_items, discover=discover))
        names.append("llm")
    else:
        from . import llm as _llm

        if _llm.available():
            providers.append(llm_provider(since=since, max_items=max_items))
            names.append("llm")
    return providers, names


def run_refresh(
    root: str | Path,
    *,
    providers: list[Callable[[dict[str, Any]], list[Candidate]]] | None = None,
    provider_names: list[str] | None = None,
    watchlist: dict[str, Any] | None = None,
    watchlist_path: str | Path | None = None,
    inbox: str | Path | None = None,
    since: str | None = None,
    max_items: int = 10,
    verify: bool = False,
    dry_run: bool = False,
    discover: Callable[..., list[dict[str, Any]]] | None = None,
    sources: dict[str, Any] | None = None,
    feed: bool = False,
    intel: bool = False,
    enrich: Callable[[str], str | None] | None = None,
) -> dict[str, Any]:
    """Run one refresh cycle; return a summary dict (no catalogs touched)."""
    root = Path(root)
    wl = watchlist or load_watchlist(watchlist_path)
    inbox_path = Path(inbox) if inbox else root / "updates" / "inbox.jsonl"

    if providers is None:
        providers, names = default_providers(
            inbox_path, since, max_items, discover, sources=sources, feed=feed
        )
    else:
        names = provider_names or ["custom"]

    candidates = collect(providers, wl)
    if verify:
        for cand in candidates:
            if cand.url:
                cand.verified = verify_url(cand.url)

    corpus_root = config.resolve_corpus_root(root)
    known = known_keys([corpus_root / name for name in _CORPUS])
    audited = curate(candidates, known, wl)
    trend = trends(audited, wl, known)

    intel_items = []
    if intel and sources is not None:
        intel_items = extract_intel(candidates, sources, wl, enrich=enrich)

    run = {"created": _now(), "providers": names, "since": since, "dry_run": dry_run}
    summary = {
        "created": run["created"],
        "providers": names,
        "collected": len(candidates),
        "accepted": trend["accepted"],
        "rejected": trend["rejected"],
        "intel_items": len(intel_items),
        "hot_topics": trend["hot_topics"],
        "coverage_gaps": trend["coverage_gaps"],
        "root": str(root),
    }

    if dry_run:
        return summary

    updates = root / "updates"
    write_queue(updates / "queue.jsonl", audited)
    write_report(updates / "REPORT.md", audited, trend, wl, run)
    if intel and sources is not None:
        write_intel(root, intel_items, created=run["created"])
    append_journal(
        updates / "JOURNAL.md",
        [
            f"refresh providers={','.join(names) or 'none'} "
            f"collected={len(candidates)} accepted={trend['accepted']} rejected={trend['rejected']} "
            f"intel={len(intel_items)}",
        ],
    )
    return summary


def apply_accepted(root: str | Path, accept: list[str]) -> list[str]:
    """Human-gated apply: mark queue rows accepted + write proposal stubs.

    ``accept`` matches a candidate's external_id, url, or 0-based queue index.
    Never edits the catalogs.
    """
    root = Path(root)
    queue = root / "updates" / "queue.jsonl"
    rows = load_queue(queue)
    wanted = {a.strip().lower() for a in accept if a.strip()}
    applied: list[str] = []

    for index, row in enumerate(rows):
        cand = Candidate.from_dict(row)
        keys = {cand.external_id.lower(), cand.url.rstrip("/").lower(), str(index)}
        if wanted & {k for k in keys if k}:
            row["status"] = "accepted"
            write_proposal(root, row)
            applied.append(cand.title or cand.external_id or cand.url)

    save_queue(queue, rows)
    if applied:
        append_journal(
            root / "updates" / "JOURNAL.md",
            [f"apply accepted={len(applied)}: " + "; ".join(applied)],
        )
    return applied
