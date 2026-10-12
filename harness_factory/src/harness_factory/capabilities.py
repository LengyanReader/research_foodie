"""Match a :class:`FeatureVector` against the capability map (requirement mechanism).

Capabilities are the *data-driven* middle layer between a requirement (task
features) and module selection. Each entry in ``data/capabilities.json`` is
``{title_en/zh, when, modules, why}``; adding a requirement means editing JSON,
not code. This module only *matches* and *annotates* -- it never enables a module
the rule engine did not enable (M0.4).
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from .registry import data_dir
from .spec import FeatureVector, HarnessPlan, _at_least


@lru_cache(maxsize=1)
def capabilities() -> dict[str, dict[str, Any]]:
    """The capability catalog."""
    with (data_dir() / "capabilities.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def capability_ids() -> list[str]:
    return list(capabilities().keys())


def _cond_matches(cond: dict[str, Any], features: FeatureVector) -> bool:
    if not cond:
        return True
    if "any" in cond:
        return any(_cond_matches(c, features) for c in cond["any"])
    for key, value in cond.items():
        if key == "min_horizon":
            if not _at_least(features.horizon, value):
                return False
            continue
        current = getattr(features, key, None)
        if isinstance(value, list):
            if current not in value:
                return False
        elif current != value:
            return False
    return True


def match(features: FeatureVector) -> list[dict[str, Any]]:
    """Return the active capabilities (id + metadata) for ``features``."""
    active: list[dict[str, Any]] = []
    for cid, meta in capabilities().items():
        if _cond_matches(meta.get("when", {}), features):
            active.append({"id": cid, **meta})
    return active


def annotate(plan: HarnessPlan) -> list[str]:
    """Record capability reasons on enabled modules; return the active ids.

    Only *enabled* modules are annotated -- the capability map adds explainability,
    it does not change the rule engine's decisions.
    """
    active = match(plan.features)
    by_module: dict[str, list[str]] = {}
    for cap in active:
        for module_id in cap.get("modules", []):
            by_module.setdefault(module_id, []).append(cap["id"])

    for module in plan.modules:
        caps = by_module.get(module.module_id)
        if module.enabled and caps:
            module.reasons.append("capability: " + ", ".join(caps))

    return [cap["id"] for cap in active]
