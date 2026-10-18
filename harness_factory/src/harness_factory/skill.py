"""Agent-native entry point: the load-index and module reader (L0 consumption).

A vibe-coding assistant pointed at this repository can read ``SKILL.md`` and then
load only the modules it needs. ``harness skill`` prints the index; ``harness
skill <name>`` prints one file. This module owns the index so both the CLI and the
skill manifest stay in sync.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_DATA = ROOT / "src" / "harness_factory" / "data"


@dataclass(frozen=True)
class Skill:
    name: str
    group: str
    path: str
    description: str


def _domain_skills() -> tuple[Skill, ...]:
    """Domain entries derived from ``domains.json`` so new domains auto-appear."""
    try:
        data = json.loads((_DATA / "domains.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ()
    out: list[Skill] = []
    for did, meta in data.items():
        if did == "general":
            continue
        label = meta.get("title_en", did)
        zh = meta.get("name_zh", "")
        out.append(Skill(did, "domains", f"domains/{did}/README.md", f"{label} · {zh}"))
    return tuple(out)


# Ordered index: overview -> modules -> domains (dynamic) -> reference/review -> catalogs.
_HEAD: tuple[Skill, ...] = (
    Skill("skill", "overview", "SKILL.md", "Cardinal rules + load-index + output contract. Read first."),
    Skill("index", "overview", "core/00-index.md", "Library index (how core/domains/review fit)."),
    Skill("map", "overview", "HARNESS-MAP.md", "Whole-factory map: modules/capabilities/domains/CLI + how to regenerate."),
    Skill("M0", "modules", "core/01-meta-principles.md", "Meta-principles: truth/traceability outrank speed."),
    Skill("M1", "modules", "core/02-context-engineering.md", "Context is scarce; curate, don't dump."),
    Skill("M2", "modules", "core/03-long-running-agents.md", "Externalize memory; resumable runs."),
    Skill("M3", "modules", "core/04-verification-and-gates.md", "Define done first; verify the verifier."),
    Skill("M4", "modules", "core/05-provenance-and-integrity.md", "Every fact traceable; uncertain = uncertain."),
    Skill("M5", "modules", "core/06-self-evolution.md", "signal->audit->mutation->journal, human-gated."),
    Skill("M6", "modules", "core/07-tools-and-skills.md", "Minimal toolset; progressive skills."),
    Skill("M7", "modules", "core/08-change-governance.md", "Single source of truth; reviewable diffs."),
    Skill("M8", "modules", "core/09-collaboration-and-sessions.md", "Explicit contracts; escalate; hand off state."),
)

_TAIL: tuple[Skill, ...] = (
    Skill("capability-router", "reference", "reference/capability-router.md", "Start here: situation -> capability -> module -> file (external-task router)."),
    Skill("derivation-rules", "reference", "reference/derivation-rules.md", "Markdown mirror of the derive.py rule table (for L0)."),
    Skill("requirement-refinement", "reference", "reference/requirement-refinement.md", "R0-R5: restate -> elevate -> classify -> offer -> confirm -> converge."),
    Skill("capability-flow", "reference", "reference/capability-flow.md", "Bidirectional flow: concretize (task-local) <-> distill (factory, human-gated)."),
    Skill("evidence-instruments", "reference", "reference/evidence-instruments.md", "M3.10 made concrete: claim type -> instrument -> catalogued tool -> gate evidence."),
    Skill("methodology-map", "reference", "reference/methodology-map.md", "M3.13 made concrete: field -> methodology system -> what the harness must enforce."),
    Skill("cross-language", "reference", "reference/cross-language.md", "M4.10 made concrete: meaning-unit alignment, corroboration by back-translation, term handling (not word-for-word)."),
    Skill("outlet-map", "reference", "reference/outlet-map.md", "Field -> high-quality information outlets / portals / media, with what each is NOT for (sources.json `outlets`)."),
    Skill("capabilities", "overview", "CAPABILITIES.md", "Generated overview: purpose + every harness capability (requirement -> modules)."),
    Skill("reference", "review", "review/references.md", "Source-grounded reference list."),
    Skill("harness-catalog", "review", "review/harness-catalog.md", "Prose taxonomy of harnesses & self-evolution methods."),
    Skill("harness-index", "review", "review/harness-index.md", "Generated lookup index of all cataloged harnesses."),
    Skill("integration-map", "review", "review/integration-map-2026-10.md", "Scope/status roadmap: what is integrated, next, and deliberately out of scope."),
    Skill("survey", "review", "review/ai-harness-survey.md", "AI harness survey."),
    Skill("source-map", "sources", "sources/source-map.md", "Where every claim comes from."),
    Skill("modules.json", "catalogs", "src/harness_factory/data/modules.json", "Machine-readable module catalog."),
    Skill("capabilities.json", "catalogs", "src/harness_factory/data/capabilities.json", "Requirement->capability->modules map."),
    Skill("domains.json", "catalogs", "src/harness_factory/data/domains.json", "Machine-readable discipline/domain catalog."),
    Skill("harnesses.json", "catalogs", "src/harness_factory/data/harnesses.json", "Unified harness catalog (SSOT for the index)."),
    Skill("sources.json", "catalogs", "src/harness_factory/data/sources.json", "Tracked entities + feeds."),
    Skill("watchlist.json", "catalogs", "src/harness_factory/data/watchlist.json", "Refresh topics + frontier probes."),
)

_INDEX: tuple[Skill, ...] = _HEAD + _domain_skills() + _TAIL


def index() -> list[Skill]:
    return list(_INDEX)


def find(name: str) -> Skill | None:
    key = (name or "").strip()
    for entry in _INDEX:
        if entry.name.lower() == key.lower():
            return entry
    return None


def read(name: str) -> str | None:
    entry = find(name)
    if entry is None:
        return None
    path = ROOT / entry.path
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def render_index() -> str:
    lines = ["harness-factory skill index · 可按需加载的模块", ""]
    group = None
    for entry in _INDEX:
        if entry.group != group:
            group = entry.group
            lines.append(f"[{group}]")
        lines.append(f"  {entry.name:<20} {entry.description}")
        lines.append(f"  {'':<20} -> {entry.path}")
    lines.append("")
    lines.append("Load one with: harness skill <name>   (or read the path directly)")
    return "\n".join(lines)
