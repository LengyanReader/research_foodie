"""Project cases: the project -> factory half of the mutual-learning loop.

Each time the tool configures a harness for a project it can also record a
**case**: the project's profile, the derived features, and the capabilities +
modules chosen. Cases are observe-only and append-only
(``updates/cases.jsonl``). :mod:`harness_factory.evolution` audits them: a
capability that keeps showing up but is missing from the registry becomes a
human-gated proposal.
"""

from __future__ import annotations

import datetime as _dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

from .spec import HarnessPlan
from .profile import ProjectProfile


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def build_case(profile: ProjectProfile, plan: HarnessPlan) -> dict[str, Any]:
    """Assemble a case row from a profile + the plan derived for it."""
    enabled = [m.module_id for m in plan.enabled_modules()]
    return {
        "created": _now(),
        "project": profile.name,
        "path": profile.path,
        "task": plan.task.text,
        "domain": plan.features.domain,
        "domain_hint": profile.domain_hint,
        "stacks": profile.stacks,
        "features": plan.features.to_dict(),
        "harness_capabilities": list(plan.capabilities),
        "project_capabilities": list(profile.capabilities),
        "modules": enabled,
    }


def append_case(root: str | Path, case: dict[str, Any]) -> Path:
    """Append one case to ``<root>/updates/cases.jsonl`` (never rewrites)."""
    path = Path(root) / "updates" / "cases.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(case, ensure_ascii=False) + "\n")
    return path


def load_cases(root: str | Path) -> list[dict[str, Any]]:
    path = Path(root) / "updates" / "cases.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def aggregate(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Frequency tables over cases (capability / domain / module)."""
    project_caps: Counter[str] = Counter()
    harness_caps: Counter[str] = Counter()
    domains: Counter[str] = Counter()
    modules: Counter[str] = Counter()
    for case in cases:
        project_caps.update(case.get("project_capabilities", []))
        harness_caps.update(case.get("harness_capabilities", []))
        if case.get("domain"):
            domains[case["domain"]] += 1
        modules.update(case.get("modules", []))
    return {
        "cases": len(cases),
        "project_capabilities": dict(project_caps.most_common()),
        "harness_capabilities": dict(harness_caps.most_common()),
        "domains": dict(domains.most_common()),
        "modules": dict(modules.most_common()),
    }
