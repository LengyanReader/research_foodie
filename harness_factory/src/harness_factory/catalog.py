"""Unified harness catalog: load / search / filter / render (SSOT = data/harnesses.json).

One machine-readable index of agent harnesses (coding agents, orchestration SDKs,
self-evolution methods, memory systems, protocols, evaluation tools, surveys, and
safety frameworks). It unifies the conceptual taxonomy in ``review/harness-catalog.md``
with the tracked vendor entities in ``data/sources.json`` (cross-linked by ``tracked``
id). ``review/harness-index.md`` is generated from this module so docs and data never
drift.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from .registry import data_file, modules as _modules

ROOT = Path(__file__).resolve().parents[2]
INDEX_DOC = ROOT / "review" / "harness-index.md"

_SEARCH_FIELDS = ("id", "name", "name_zh", "vendor", "ecosystem", "summary_en", "summary_zh")


@lru_cache(maxsize=1)
def catalog() -> dict[str, Any]:
    with data_file("harnesses.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def classes() -> list[dict[str, Any]]:
    return list(catalog().get("classes", []))


def class_ids() -> list[str]:
    return [c["id"] for c in classes()]


def kinds() -> list[dict[str, Any]]:
    return list(catalog().get("kinds", []))


def kind_ids() -> list[str]:
    return [k["id"] for k in kinds()]


def items() -> list[dict[str, Any]]:
    return list(catalog().get("harnesses", []))


def find(harness_id: str) -> dict[str, Any] | None:
    key = (harness_id or "").strip().lower()
    for entry in items():
        if entry["id"].lower() == key:
            return entry
    return None


def search(query: str, rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    q = (query or "").strip().lower()
    if not q:
        return list(rows if rows is not None else items())
    out: list[dict[str, Any]] = []
    for entry in rows if rows is not None else items():
        hay = " ".join(str(entry.get(f, "")) for f in _SEARCH_FIELDS)
        hay += " " + " ".join(entry.get("tags", []))
        hay += " " + " ".join(entry.get("maps_to", []))
        if q in hay.lower():
            out.append(entry)
    return out


def filter_rows(
    rows: list[dict[str, Any]] | None = None,
    *,
    klass: str | None = None,
    kind: str | None = None,
    vendor: str | None = None,
    tag: str | None = None,
    module: str | None = None,
    tracked_only: bool = False,
) -> list[dict[str, Any]]:
    out = list(rows if rows is not None else items())
    if klass:
        out = [e for e in out if e.get("class") == klass]
    if kind:
        out = [e for e in out if e.get("kind") == kind]
    if vendor:
        v = vendor.lower()
        out = [e for e in out if v in str(e.get("vendor", "")).lower()]
    if tag:
        t = tag.lower()
        out = [e for e in out if t in [str(x).lower() for x in e.get("tags", [])]]
    if module:
        out = [e for e in out if module in e.get("maps_to", [])]
    if tracked_only:
        out = [e for e in out if e.get("tracked")]
    return out


def _source_ids() -> set[str]:
    path = data_file("sources.json")
    if not path.exists():
        return set()
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    ids: set[str] = set()
    for entries in data.get("groups", {}).values():
        for entry in entries:
            ids.add(entry.get("id", ""))
    return ids


def validate() -> list[str]:
    """Return a list of problems (empty = healthy). Used by the test suite."""
    errors: list[str] = []
    cls, knd = set(class_ids()), set(kind_ids())
    mods = set(_modules().keys())
    src = _source_ids()
    seen: set[str] = set()

    for entry in items():
        hid = entry.get("id", "")
        if not hid:
            errors.append("entry without id")
            continue
        if hid in seen:
            errors.append(f"duplicate id: {hid}")
        seen.add(hid)
        if entry.get("class") not in cls:
            errors.append(f"{hid}: unknown class {entry.get('class')!r}")
        if entry.get("kind") not in knd:
            errors.append(f"{hid}: unknown kind {entry.get('kind')!r}")
        for m in entry.get("maps_to", []):
            if m not in mods:
                errors.append(f"{hid}: maps_to unknown module {m!r}")
        tracked = entry.get("tracked")
        if tracked and src and tracked not in src:
            errors.append(f"{hid}: tracked id {tracked!r} not in sources.json")
    return errors


def _entry_line(entry: dict[str, Any], vocab: dict[str, dict[str, Any]]) -> str:
    src = entry.get("paper") or entry.get("url") or ""
    track = f" · tracked:{entry['tracked']}" if entry.get("tracked") else ""
    return (
        f"| `{entry['id']}` | {entry.get('name')} · {entry.get('name_zh', '')} "
        f"| {vocab.get(entry.get('kind', ''), {}).get('zh', entry.get('kind', ''))} "
        f"| {', '.join(entry.get('maps_to', []))} | {src}{track} |"
    )


def render_index(
    rows: list[dict[str, Any]] | None = None, detailed: bool = False
) -> str:
    rows = list(rows if rows is not None else items())
    kv = {k["id"]: k for k in kinds()}
    lines = [f"harness catalog · {len(rows)} entries", ""]
    for c in classes():
        group = [e for e in rows if e.get("class") == c["id"]]
        if not group:
            continue
        lines.append(f"[{c['id']}] {c['en']} · {c['zh']}  ({len(group)})")
        for e in group:
            line = f"  {e['id']:<24} M={','.join(e.get('maps_to', [])):<14} {e.get('name')}"
            lines.append(line)
            if detailed:
                lines.append(f"    {e.get('summary_en', '')}")
                if e.get("tracked"):
                    lines.append(f"    tracked: {e['tracked']}")
        lines.append("")
    return "\n".join(lines)


def render_markdown() -> str:
    """Generate review/harness-index.md from the data (drift-guarded by tests)."""
    kv = {k["id"]: k for k in kinds()}
    all_rows = items()
    lines = [
        "# Harness Index · Harness 索引",
        "",
        "> Generated from `src/harness_factory/data/harnesses.json` — **do not edit by hand**; "
        "run `harness catalog --write` to regenerate.",
        "> 由 `data/harnesses.json` 生成，**请勿手改**；用 `harness catalog --write` 重新生成。",
        "",
        f"**Updated:** {catalog().get('updated', '')} · {len(all_rows)} entries · "
        f"{len(classes())} classes · companion to `harness-catalog.md` (the prose taxonomy).",
        "",
        "---",
        "",
        "## How to use · 用法",
        "",
        "```bash",
        "harness catalog                       # list everything",
        "harness catalog --class self-evolution",
        "harness catalog --kind memory-system",
        "harness catalog --module M5           # harnesses that exercise a core module",
        "harness catalog --search voyager",
        "harness catalog --tracked             # only entities also tracked in sources.json",
        "harness catalog claude-code           # detail one entry",
        "```",
        "",
        "---",
        "",
    ]
    for c in classes():
        group = [e for e in all_rows if e.get("class") == c["id"]]
        if not group:
            continue
        lines.append(f"## {c['en']} · {c['zh']}  ({len(group)})")
        lines.append("")
        lines.append("| id | name | kind | core modules | source |")
        lines.append("|---|---|---|---|---|")
        for e in group:
            lines.append(_entry_line(e, kv))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Cross-links · 交叉链接")
    lines.append("")
    lines.append("- Prose taxonomy & design lessons: [`harness-catalog.md`](harness-catalog.md).")
    lines.append("- Tracked feeds for these entities: `data/sources.json` (`harness sources`).")
    lines.append("- Core modules M0–M8: [`../core/00-index.md`](../core/00-index.md).")
    lines.append("")
    return "\n".join(lines)


def write_index(path: Path | None = None) -> Path:
    target = path or INDEX_DOC
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(), encoding="utf-8")
    return target
