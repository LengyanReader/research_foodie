"""Data model for the harness compiler.

A task is reduced to a :class:`FeatureVector`; the vector is compiled into a
:class:`HarnessPlan` made of :class:`ModulePlan` entries (M0-M8). Nothing here
fabricates task substance -- the model only describes and selects (M0.4).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

# --- Allowed feature values (closed vocabularies keep rules checkable) --------

HORIZONS = ("one_shot", "session", "multi_session", "long_running")
VERIFIABILITY = ("high", "medium", "low")
STAKES = ("low", "medium", "high")
GROUNDING = ("off", "preferred", "required")
ARTIFACTS = ("code", "document", "dataset", "knowledge_base", "plan", "mixed")
TOOL_SURFACES = ("none", "read", "read_write", "external")
COLLABORATION = ("solo", "human_review", "multi_agent")

FEATURE_FIELDS = (
    "horizon",
    "verifiability",
    "stakes",
    "grounding",
    "artifact",
    "tool_surface",
    "collaboration",
    "domain",
)

FEATURE_CHOICES: dict[str, tuple[str, ...]] = {
    "horizon": HORIZONS,
    "verifiability": VERIFIABILITY,
    "stakes": STAKES,
    "grounding": GROUNDING,
    "artifact": ARTIFACTS,
    "tool_surface": TOOL_SURFACES,
    "collaboration": COLLABORATION,
}

_HORIZON_ORDER = {v: i for i, v in enumerate(HORIZONS)}


def _at_least(value: str, level: str) -> bool:
    """True if ``value`` is at least ``level`` on the horizon ladder."""
    return _HORIZON_ORDER.get(value, 0) >= _HORIZON_ORDER.get(level, 0)


@dataclass
class TaskSpec:
    """The raw task handed to the compiler."""

    text: str = "unspecified task"
    domain: str | None = None
    goal: str | None = None
    notes: str | None = None


@dataclass
class FeatureVector:
    """Task features that drive module selection."""

    horizon: str = "session"
    verifiability: str = "medium"
    stakes: str = "medium"
    grounding: str = "preferred"
    artifact: str = "mixed"
    tool_surface: str = "read_write"
    collaboration: str = "solo"
    domain: str = "general"
    source: str = "rules"  # rules | llm | flags | mixed
    notes: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        for name, choices in FEATURE_CHOICES.items():
            value = getattr(self, name)
            if value not in choices:
                errors.append(f"{name}={value!r} not in {choices}")
        if not self.domain:
            errors.append("domain must be non-empty")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ModulePlan:
    """One core module (M0-M8) as selected for this task."""

    module_id: str
    title_en: str = ""
    title_zh: str = ""
    rule_en: str = ""
    enabled: bool = False
    params: dict[str, Any] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class HarnessPlan:
    """The compiled plan: task + features + module decisions."""

    task: TaskSpec
    features: FeatureVector
    modules: list[ModulePlan] = field(default_factory=list)
    version: str = ""
    created: str = ""
    files: list[str] = field(default_factory=list)

    def enabled_modules(self) -> list[ModulePlan]:
        return [m for m in self.modules if m.enabled]

    def params(self) -> dict[str, Any]:
        """Flatten enabled-module params into one dict (later modules win)."""
        merged: dict[str, Any] = {}
        for module in self.enabled_modules():
            merged.update(module.params)
        return merged

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "created": self.created,
            "task": asdict(self.task),
            "features": self.features.to_dict(),
            "modules": [m.to_dict() for m in self.modules],
            "files": sorted(self.files),
        }
