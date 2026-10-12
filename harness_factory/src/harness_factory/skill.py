"""Agent-native entry point: the load-index and module reader (L0 consumption).

A vibe-coding assistant pointed at this repository can read ``SKILL.md`` and then
load only the modules it needs. ``harness skill`` prints the index; ``harness
skill <name>`` prints one file. This module owns the index so both the CLI and the
skill manifest stay in sync.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Skill:
    name: str
    group: str
    path: str
    description: str


# Ordered index: group -> entries. Paths are relative to the repo root.
_INDEX: tuple[Skill, ...] = (
    Skill("skill", "overview", "SKILL.md", "Cardinal rules + load-index + output contract. Read first."),
    Skill("index", "overview", "core/00-index.md", "Library index (how core/domains/review fit)."),
    Skill("M0", "modules", "core/01-meta-principles.md", "Meta-principles: truth/traceability outrank speed."),
    Skill("M1", "modules", "core/02-context-engineering.md", "Context is scarce; curate, don't dump."),
    Skill("M2", "modules", "core/03-long-running-agents.md", "Externalize memory; resumable runs."),
    Skill("M3", "modules", "core/04-verification-and-gates.md", "Define done first; verify the verifier."),
    Skill("M4", "modules", "core/05-provenance-and-integrity.md", "Every fact traceable; uncertain = uncertain."),
    Skill("M5", "modules", "core/06-self-evolution.md", "signal->audit->mutation->journal, human-gated."),
    Skill("M6", "modules", "core/07-tools-and-skills.md", "Minimal toolset; progressive skills."),
    Skill("M7", "modules", "core/08-change-governance.md", "Single source of truth; reviewable diffs."),
    Skill("M8", "modules", "core/09-collaboration-and-sessions.md", "Explicit contracts; escalate; hand off state."),
    Skill("academic-research", "domains", "domains/research/README.md", "Research domain workflow."),
    Skill("knowledge-management", "domains", "domains/knowledge-management/README.md", "KM domain workflow."),
    Skill("data-science", "domains", "domains/data-science/README.md", "Data-science domain workflow."),
    Skill("devops", "domains", "domains/devops/README.md", "DevOps domain workflow."),
    Skill("derivation-rules", "reference", "reference/derivation-rules.md", "Markdown mirror of the derive.py rule table (for L0)."),
    Skill("reference", "review", "review/references.md", "Source-grounded reference list."),
    Skill("harness-catalog", "review", "review/harness-catalog.md", "Catalog of harnesses/patterns."),
    Skill("survey", "review", "review/ai-harness-survey.md", "AI harness survey."),
    Skill("source-map", "sources", "sources/source-map.md", "Where every claim comes from."),
    Skill("modules.json", "catalogs", "src/harness_factory/data/modules.json", "Machine-readable module catalog."),
    Skill("capabilities.json", "catalogs", "src/harness_factory/data/capabilities.json", "Requirement->capability->modules map."),
    Skill("domains.json", "catalogs", "src/harness_factory/data/domains.json", "Machine-readable domain catalog."),
    Skill("sources.json", "catalogs", "src/harness_factory/data/sources.json", "Tracked entities + feeds."),
    Skill("watchlist.json", "catalogs", "src/harness_factory/data/watchlist.json", "Refresh topics + frontier probes."),
)


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
