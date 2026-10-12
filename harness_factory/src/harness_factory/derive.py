"""Compile a :class:`FeatureVector` into a :class:`HarnessPlan`.

The rules are explicit and each decision records a human-readable reason, so a
derivation is always explainable ("which rule fired?") and reproducible. The
engine only *selects and parameterizes* modules; it never writes task content
(M0.4).
"""

from __future__ import annotations

import datetime as _dt

from ._version import __version__
from .capabilities import annotate as _annotate_capabilities
from .registry import modules as _modules
from .spec import FeatureVector, HarnessPlan, ModulePlan, TaskSpec, _at_least

# Artifacts whose nature implies provenance discipline.
_GROUNDING_ARTIFACTS = ("document", "dataset", "knowledge_base")


def _gate_strictness(f: FeatureVector) -> str:
    if f.verifiability == "low" or f.stakes == "high":
        return "strict"
    if f.verifiability == "high" and f.stakes == "low":
        return "relaxed"
    return "standard"


def _autonomy(f: FeatureVector) -> str:
    if f.stakes == "high" or f.verifiability == "low":
        return "low"
    if f.stakes == "low" and f.verifiability == "high":
        return "high"
    return "medium"


def _mk(mid: str, enabled: bool, params: dict | None, reasons: list[str]) -> ModulePlan:
    meta = _modules().get(mid, {})
    return ModulePlan(
        module_id=mid,
        title_en=meta.get("title_en", ""),
        title_zh=meta.get("title_zh", ""),
        rule_en=meta.get("rule_en", ""),
        enabled=enabled,
        params=params or {},
        reasons=reasons,
    )


def derive(task: TaskSpec, features: FeatureVector) -> HarnessPlan:
    """Return the harness plan for ``features``."""
    errors = features.validate()
    if errors:
        raise ValueError("invalid feature vector: " + "; ".join(errors))

    mods: list[ModulePlan] = []

    # M0 -- always (the constitution).
    mods.append(_mk("M0", True, {}, ["always: load-bearing invariants (M0)"]))

    # M1 -- always (every task reads context).
    mods.append(
        _mk(
            "M1",
            True,
            {"context_policy": "index-first; minimal high-signal set"},
            ["always: context is consumed by every step (M0.6)"],
        )
    )

    # M2 -- memory when work spans at least a session.
    if _at_least(features.horizon, "session"):
        depth = "session" if features.horizon == "session" else "durable"
        mods.append(
            _mk(
                "M2",
                True,
                {"memory_depth": depth},
                [f"horizon={features.horizon} >= session"],
            )
        )
    else:
        mods.append(_mk("M2", False, {}, [f"horizon={features.horizon} is one_shot"]))

    # M3 -- always (define done before work).
    mods.append(
        _mk(
            "M3",
            True,
            {"gate_strictness": _gate_strictness(features)},
            [
                "always: verify before done (M0.3)",
                f"strictness from verifiability={features.verifiability}, stakes={features.stakes}",
            ],
        )
    )

    # M4 -- provenance when grounding matters or the artifact is cited material.
    needs_ground = features.grounding in ("preferred", "required") or (
        features.artifact in _GROUNDING_ARTIFACTS
    )
    if needs_ground:
        provenance = features.grounding if features.grounding != "off" else "preferred"
        mods.append(
            _mk(
                "M4",
                True,
                {"provenance": provenance},
                [f"grounding={features.grounding}, artifact={features.artifact}"],
            )
        )
    else:
        mods.append(
            _mk("M4", False, {}, [f"grounding={features.grounding}, artifact={features.artifact}"])
        )

    # M5 -- evolution loop when work spans multiple sessions.
    if _at_least(features.horizon, "multi_session"):
        cadence = "per_session" if features.horizon == "multi_session" else "periodic"
        mods.append(
            _mk(
                "M5",
                True,
                {"evolution_cadence": cadence},
                [f"horizon={features.horizon} >= multi_session"],
            )
        )
    else:
        mods.append(_mk("M5", False, {}, [f"horizon={features.horizon} < multi_session"]))

    # M6 -- tools/skills when the task touches the world.
    if features.tool_surface != "none":
        mods.append(
            _mk(
                "M6",
                True,
                {"tool_surface": features.tool_surface},
                [f"tool_surface={features.tool_surface}"],
            )
        )
    else:
        mods.append(_mk("M6", False, {}, ["tool_surface=none"]))

    # M7 -- always (change governance).
    mods.append(
        _mk(
            "M7",
            True,
            {"commit_policy": "conventional commits; commit ok; never auto-push"},
            ["always: single source of truth + reviewable diffs (M0.5/M0.9)"],
        )
    )

    # M8 -- collaboration when others are involved or stakes are high.
    if features.collaboration != "solo" or features.stakes == "high":
        mods.append(
            _mk(
                "M8",
                True,
                {"collaboration": features.collaboration, "autonomy": _autonomy(features)},
                [f"collaboration={features.collaboration}, stakes={features.stakes}"],
            )
        )
    else:
        mods.append(
            _mk(
                "M8",
                False,
                {},
                [f"collaboration={features.collaboration}, stakes={features.stakes}"],
            )
        )

    created = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()
    plan = HarnessPlan(
        task=task,
        features=features,
        modules=mods,
        version=__version__,
        created=created,
    )
    plan.capabilities = _annotate_capabilities(plan)
    return plan
