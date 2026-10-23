"""Domain probe (P29): surface collected intel that no domain catches - the automated finder.

The refresh/intel direction pulls *known* topics; this is the reverse question:
which collected items does no domain's signal vocabulary map to? Unmapped items
are clustered by shared keywords and proposed as candidate domains or signal
fixes - **proposals only** (M0.4/M0.8); a human decides whether a cluster earns
a domain (the M0.5 discrimination bar) or a signal fix.

Offline and deterministic: it runs on already-collected ``updates/intel.jsonl``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .classify import classify
from .derive import derive
from .registry import domains
from .spec import TaskSpec

INTEL_REL = "updates/intel.jsonl"
PROBES_REL = "updates/DOMAIN-PROBES.md"

_STOP = frozenset(
    {
        "the", "and", "for", "with", "that", "this", "from", "are", "was", "have",
        "has", "into", "their", "they", "what", "when", "which", "will", "your",
        "about", "agent", "agents", "model", "models", "using", "based", "toward",
        "towards", "llm", "llms", "paper", "arxiv", "study", "new", "2026", "2025",
    }
)
_WORD = re.compile(r"[a-z][a-z0-9-]{3,}")


def _tokens(text: str) -> list[str]:
    return [w for w in _WORD.findall((text or "").lower()) if w not in _STOP]


def _all_signals() -> set[str]:
    out: set[str] = set()
    for entry in domains().values():
        for s in entry.get("signals", []):
            out.add(s.lower())
    return out


def _nearest_domain(tokens: list[str]) -> str:
    best, best_n = "general", 0
    for did, entry in domains().items():
        if did == "general":
            continue
        sig_tokens = {t for s in entry.get("signals", []) for t in _tokens(s)}
        n = len(set(tokens) & sig_tokens)
        if n > best_n:
            best, best_n = did, n
    return best


def _unmapped_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """An item is unmapped when it lands on `general` - no domain's signals caught it.

    A floor-capability landing on a *named* domain is a misroute (a different
    defect class), not an unmapped cluster; this probe only finds the unknown.
    """
    out = []
    for item in items:
        text = f"{item.get('title', '')} {item.get('brief', '')}"
        if not text.strip():
            continue
        vector = classify(TaskSpec(text=text[:500]))
        if vector.domain == "general":
            out.append(item)
    return out


def probe(kb_root: str | Path, max_clusters: int = 5, min_cluster: int = 2) -> list[dict[str, Any]]:
    """Cluster unmapped intel items by shared keywords and emit proposals.

    Clustering is greedy and disjoint: keywords are taken in descending
    frequency, each cluster consumes its items, and only clusters of at least
    ``min_cluster`` items are proposed (a singleton is an anecdote, not a
    pattern - M5). Each proposal names the keyword, the item count, example
    titles and the nearest existing domain (the cheapest signal fix), and does
    NOT assert that a new domain is warranted - that is the human gate (M0.8).
    """
    path = Path(kb_root) / INTEL_REL
    if not path.exists():
        return []
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    unmapped = _unmapped_items(items)
    if not unmapped:
        return []

    signals = _all_signals()
    freq: dict[str, list[dict[str, Any]]] = {}
    for item in unmapped:
        seen: set[str] = set()
        for token in _tokens(f"{item.get('title', '')} {item.get('brief', '')}"):
            if token in signals or token in seen:
                continue
            seen.add(token)
            freq.setdefault(token, []).append(item)

    proposals = []
    covered: set[int] = set()
    for token, members in sorted(freq.items(), key=lambda kv: -len(kv[1])):
        fresh = [m for m in members if id(m) not in covered]
        if len(fresh) < min_cluster:
            continue
        covered.update(id(m) for m in fresh)
        tokens = _tokens(" ".join(m.get("title", "") for m in fresh))
        proposals.append(
            {
                "keyword": token,
                "n_items": len(fresh),
                "examples": [m.get("title", "")[:120] for m in fresh[:3]],
                "nearest_domain": _nearest_domain(tokens),
                "suggested_action": (
                    "check whether the cluster is a discriminating work type (new domain, "
                    "M0.5 bar) or a missing signal on the nearest domain (data-only fix)"
                ),
            }
        )
        if len(proposals) >= max_clusters:
            break
    return proposals


def render(proposals: list[dict[str, Any]]) -> str:
    if not proposals:
        return "DOMAIN-PROBES\n\nNo unmapped intel clusters (everything collected maps to a domain).\n"
    lines = [
        "DOMAIN-PROBES",
        "",
        f"{len(proposals)} unmapped cluster(s) - proposals only (M0.4/M0.8):",
    ]
    for p in proposals:
        lines.append(
            f"- keyword `{p['keyword']}` ({p['n_items']} items, nearest domain: {p['nearest_domain']})"
        )
        for ex in p["examples"]:
            lines.append(f"    - {ex}")
    lines.append("")
    lines.append("Human gate: a cluster earns a domain only if it changes routing or gate content (M0.5); otherwise it is a signal fix on the nearest domain.")
    return "\n".join(lines)


def emit(kb_root: str | Path, proposals: list[dict[str, Any]]) -> Path:
    path = Path(kb_root) / PROBES_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(proposals), encoding="utf-8")
    return path
