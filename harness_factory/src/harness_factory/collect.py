"""Collect candidate sources for the self-update loop.

Providers are deliberately dumb: they only *fetch/propose* raw candidates. All
auditing, dedupe, and ranking happens in :mod:`harness_factory.curate`, and
nothing is written to the catalogs without a human gate (M0.4, M0.8).
"""

from __future__ import annotations

import datetime as _dt
import email.utils
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

_KINDS = ("paper", "repo", "doc", "post", "video", "podcast", "newsletter", "other")


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Candidate:
    """A proposed addition to the knowledge base (untrusted until audited)."""

    title: str = ""
    url: str = ""
    external_id: str = ""
    kind: str = "other"
    entity: str = ""  # tracked source id (projects/venues/people/media)
    topics: list[str] = field(default_factory=list)
    summary: str = ""
    published: str = ""
    source_kind: str = "file"  # file | llm | manual
    retrieved_at: str = ""
    verified: bool = False
    notes: list[str] = field(default_factory=list)

    def key(self) -> str:
        return (self.external_id or self.url or "").strip().lower()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Candidate":
        kind = str(data.get("kind", "other")).lower()
        if kind not in _KINDS:
            kind = "other"
        topics = data.get("topics") or []
        if isinstance(topics, str):
            topics = [t.strip() for t in topics.split(",") if t.strip()]
        cand = cls(
            title=str(data.get("title", "")).strip(),
            url=str(data.get("url", "")).strip(),
            external_id=str(data.get("external_id", "") or data.get("id", "")).strip(),
            kind=kind,
            entity=str(data.get("entity", "")).strip(),
            topics=[str(t) for t in topics],
            summary=str(data.get("summary", "")).strip(),
            published=str(data.get("published", "")).strip(),
            source_kind=str(data.get("source_kind", "file")),
            retrieved_at=str(data.get("retrieved_at") or _now()),
        )
        if not cand.title and not cand.url:
            cand.notes.append("empty candidate")
        return cand


def verify_url(url: str, timeout: float = 10.0) -> bool:
    """Best-effort reachability check (HEAD, then GET fallback)."""
    if not url:
        return False
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(
            url,
            method=method,
            headers={"User-Agent": "harness-factory/refresh"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as resp:
                if 200 <= getattr(resp, "status", 200) < 400:
                    return True
        except (urllib.error.URLError, TimeoutError, ValueError, OSError):
            continue
    return False


def load_inbox(path: str | Path) -> list[Candidate]:
    """Read candidates from a ``.jsonl`` or a JSON array file."""
    p = Path(path)
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.lstrip().startswith("["):
        data = json.loads(text)
        return [Candidate.from_dict(d) for d in data if isinstance(d, dict)]
    out: list[Candidate] = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(Candidate.from_dict(json.loads(line)))
    return out


def file_provider(inbox: str | Path) -> Callable[[dict[str, Any]], list[Candidate]]:
    def _run(_watchlist: dict[str, Any]) -> list[Candidate]:
        candidates = load_inbox(inbox)
        for cand in candidates:
            cand.source_kind = "file"
        return candidates

    return _run


def llm_provider(
    since: str | None = None,
    max_items: int = 10,
    discover: Callable[..., list[dict[str, Any]]] | None = None,
) -> Callable[[dict[str, Any]], list[Candidate]]:
    def _run(watchlist: dict[str, Any]) -> list[Candidate]:
        if discover is None:
            from . import llm as _llm

            fetch = _llm.discover_items
        else:
            fetch = discover
        topics = list(watchlist.get("topics", []))
        # frontier probes ride along as extra topics
        for probe in watchlist.get("frontier_probes", []):
            topics.append({"id": probe.get("id", "frontier"), "queries": [probe.get("query", "")]})
        raw = fetch(topics, since=since, max_items=max_items) or []
        out: list[Candidate] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            cand = Candidate.from_dict(item)
            cand.source_kind = "llm"
            cand.retrieved_at = _now()
            out.append(cand)
        return out

    return _run


def collect(
    providers: Iterable[Callable[[dict[str, Any]], list[Candidate]]],
    watchlist: dict[str, Any],
) -> list[Candidate]:
    """Run every provider and concatenate their candidates."""
    out: list[Candidate] = []
    for provider in providers:
        out.extend(provider(watchlist))
    return out


# --- Feed (RSS / Atom) providers ---------------------------------------------

_ATOM = "{http://www.w3.org/2005/Atom}"
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
_YT_CHANNEL = re.compile(r'"(?:channelId|externalId)":"(UC[\w-]{20,})"')


def http_get(url: str, timeout: float = 20.0) -> str | None:
    """GET a URL and return decoded text, or ``None`` on any failure."""
    request = urllib.request.Request(url, headers={"User-Agent": "harness-factory/refresh"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            data = resp.read()
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None
    return data.decode("utf-8", errors="replace")


def iter_entities(sources: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Flatten the ``groups`` map into ``(group, entity)`` pairs."""
    groups = sources.get("groups", sources)
    out: list[tuple[str, dict[str, Any]]] = []
    if isinstance(groups, dict):
        for group, entities in groups.items():
            if isinstance(entities, list):
                out.extend((group, e) for e in entities if isinstance(e, dict))
    return out


def _clean(text: str) -> str:
    return _WS.sub(" ", _TAG.sub(" ", text or "")).strip()[:500]


def _norm_date(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    try:
        return email.utils.parsedate_to_datetime(value).date().isoformat()
    except (TypeError, ValueError):
        return value[:10] if len(value) >= 10 else value


def _mk_candidate(title, link, ext, pub, desc, entity) -> Candidate:
    return Candidate(
        title=_clean(title),
        url=(link or "").strip(),
        external_id=(ext or link or "").strip(),
        kind=str(entity.get("kind", "other")).lower(),
        entity=str(entity.get("id", "")),
        topics=[str(t) for t in entity.get("topics", [])],
        summary=_clean(desc),
        published=_norm_date(pub),
        source_kind="feed",
    )


def parse_feed(xml_text: str, entity: dict[str, Any], group: str = "media") -> list[Candidate]:
    """Parse RSS 2.0 or Atom into candidates. Never raises on malformed XML."""
    if not xml_text:
        return []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    items = root.findall(".//item")  # RSS 2.0
    if items:
        out = []
        for item in items:
            out.append(
                _mk_candidate(
                    item.findtext("title"),
                    item.findtext("link"),
                    item.findtext("guid"),
                    item.findtext("pubDate"),
                    item.findtext("description"),
                    entity,
                )
            )
        return out

    entries = root.findall(f"{_ATOM}entry") or root.findall(".//entry")  # Atom
    out = []
    for entry in entries:
        link_el = entry.find(f"{_ATOM}link")
        link = link_el.get("href", "") if link_el is not None else ""
        out.append(
            _mk_candidate(
                entry.findtext(f"{_ATOM}title"),
                link,
                entry.findtext(f"{_ATOM}id"),
                entry.findtext(f"{_ATOM}published") or entry.findtext(f"{_ATOM}updated"),
                entry.findtext(f"{_ATOM}summary") or entry.findtext(f"{_ATOM}content"),
                entity,
            )
        )
    return out


def resolve_youtube_feed(
    url: str, fetcher: Callable[[str], str | None] | None = None
) -> str | None:
    """Resolve a ``youtube.com/@handle`` page to its channel RSS feed URL."""
    fetch = fetcher or http_get
    html = fetch(url)
    if not html:
        return None
    match = _YT_CHANNEL.search(html)
    if not match:
        return None
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={match.group(1)}"


def feed_provider(
    sources: dict[str, Any],
    fetcher: Callable[[str], str | None] | None = None,
    resolver: Callable[..., str | None] | None = None,
    since: str | None = None,
) -> Callable[[dict[str, Any]], list[Candidate]]:
    """A provider that pulls every entity feed in ``sources`` (RSS/Atom/YouTube)."""
    fetch = fetcher or http_get
    resolve = resolver or resolve_youtube_feed

    def _run(_watchlist: dict[str, Any]) -> list[Candidate]:
        out: list[Candidate] = []
        for _group, entity in iter_entities(sources):
            feed = entity.get("feed")
            if not feed and entity.get("resolve") == "youtube":
                feed = resolve(entity.get("url", ""), fetch)
            if not feed:
                continue
            xml = fetch(feed)
            for cand in parse_feed(xml or "", entity):
                if since and cand.published and cand.published < since:
                    continue
                cand.retrieved_at = _now()
                out.append(cand)
        return out

    return _run
