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
from pathlib import Path
from typing import Any

from .registry import data_file
from .spec import FeatureVector, HarnessPlan, _at_least


@lru_cache(maxsize=1)
def capabilities() -> dict[str, dict[str, Any]]:
    """The capability catalog."""
    with data_file("capabilities.json").open(encoding="utf-8") as fh:
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


# --------------------------------------------------------------------------- #
# Generated overview doc (CAPABILITIES.md) — drift-guarded by the test suite.
# --------------------------------------------------------------------------- #

DOC_PATH = Path(__file__).resolve().parents[2] / "CAPABILITIES.md"

_FEATURE_ZH = {
    "horizon": "时间跨度",
    "verifiability": "可验证性",
    "stakes": "风险",
    "grounding": "来源要求",
    "artifact": "产物",
    "tool_surface": "工具面",
    "collaboration": "协作",
    "domain": "领域",
}


def _when_text(when: dict[str, Any]) -> str:
    """Render a ``when`` clause as a short human-readable string."""

    def one(cond: dict[str, Any]) -> str:
        parts: list[str] = []
        for key, value in cond.items():
            if key == "any":
                continue
            if key == "min_horizon":
                parts.append(f"horizon ≥ {value}")
                continue
            vals = value if isinstance(value, list) else [value]
            zh = _FEATURE_ZH.get(key, key)
            parts.append(f"{key} ∈ {{{', '.join(str(v) for v in vals)}}} ({zh})")
        return " and ".join(parts) or "always"

    if not when:
        return "always · 总是"
    if "any" in when:
        alts = []
        for c in when["any"]:
            text = one(c)
            alts.append(f"({text})" if " and " in text else text)
        rest = {k: v for k, v in when.items() if k != "any"}
        if rest:
            text = one(rest)
            alts.append(f"({text})" if " and " in text else text)
        return " OR ".join(alts)
    return one(when)


def render_doc() -> str:
    """Generate ``CAPABILITIES.md`` from ``capabilities.json`` + ``modules.json``."""
    from .registry import modules as _module_meta

    caps = capabilities()
    mods = _module_meta()
    lines = [
        "# Harness capabilities · Harness 能力总览",
        "",
        "> **Generated** from `src/harness_factory/data/capabilities.json` + `modules.json` — "
        "**do not edit by hand**; run `harness capabilities --write` (also refreshed by "
        "`harness catalog --write`) to regenerate.",
        "> **生成文档**：由上述 SSOT 生成，**请勿手改**；用 `harness capabilities --write` 重新生成"
        "（`harness catalog --write` 亦会同步刷新）。",
        "",
        f"**{len(caps)} capabilities · {len(mods)} modules (M0–M8)**",
        "",
        "---",
        "",
        "## Purpose · 目的",
        "",
        "A harness is the durable scaffolding around an agent: the invariants it must hold, the context it "
        "may load, the memory it externalises, the gates that define \"done\", the provenance it records, "
        "the tools/skills it may use, the governance over its changes, and how it collaborates with humans. "
        "This repository compiles a *task-specific* harness instead of shipping one fixed scaffold.",
        "",
        "**Capabilities are the middle layer** between a task's features and the modules that get enabled. "
        "Each capability is one reusable *requirement* (e.g. \"verification gate\", \"resumable memory\", "
        "\"sandboxed execution\") that fires when the task's feature vector matches its `when` clause, and "
        "then **annotates** the already-enabled modules with *why* they matter (M0.4: it augments "
        "explainability, it never overrides the rule engine).",
        "",
        "> 中文速览：harness 是围绕 agent 的耐久脚手架。**能力（capability）**是「任务特征 → 启用模块」"
        "之间的**数据驱动中间层**：每条能力是一个可复用的**要求**，由任务特征向量匹配 `when` 触发，"
        "给已启用模块**标注理由**——只增可解释性，绝不改变规则引擎的决定（M0.4）。",
        "",
        "## How it works · 工作机制",
        "",
        "```",
        "task text ──▶ feature vector ──▶ capability.match(when) ──▶ annotate enabled modules",
        "            (classify)           (data/capabilities.json)      → .harness/manifest.json",
        "```",
        "",
        "1. **Classify** the goal into the 8-axis feature vector (`horizon`, `verifiability`, `stakes`, "
        "`grounding`, `artifact`, `tool_surface`, `collaboration`, `domain`).",
        "2. **Match** every capability whose `when` clause holds for that vector.",
        "3. **Annotate** the enabled modules with the matching capability ids + reasons; record all of it in "
        "`.harness/manifest.json` for review.",
        "",
        "## Modules · 模块 (M0–M8)",
        "",
        "| id | module | one-line rule | doc |",
        "|---|---|---|---|",
    ]
    for mid, meta in sorted(mods.items()):
        lines.append(
            f"| {mid} | {meta.get('title_en', '')} · {meta.get('title_zh', '')} "
            f"| {meta.get('rule_en', '')} | `core/{Path(meta.get('doc', '')).name}` |"
        )
    lines += [
        "",
        "## Capabilities · 能力清单",
        "",
    ]
    for cid, meta in caps.items():
        mods_of = ", ".join(meta.get("modules", [])) or "_(annotation only)_"
        lines.append(f"### `{cid}` — {meta.get('title_en', cid)} · {meta.get('title_zh', '')}")
        lines.append("")
        lines.append(f"- **Fires when · 触发条件:** {_when_text(meta.get('when', {}))}")
        lines.append(f"- **Modules · 关联模块:** {mods_of}")
        lines.append(f"- **Why · 理由:** {meta.get('why', '')}")
        lines.append("")
    lines += [
        "---",
        "",
        "## Evolution · 演化",
        "",
        "This document is **generated**, so it evolves with the project: add or tune a capability by editing "
        "`data/capabilities.json` and re-running `harness capabilities --write` (the test suite also guards "
        "it for drift). The self-evolution loop may *propose* new capabilities from observed projects, but "
        "the change is **human-gated and reversible** (M0.4/M0.8). · 本文档自动演化：改 SSOT 后重生成即可；"
        "自我演化循环只**提案**新能力，交由人类把关（M0.4/M0.8）。",
        "",
        "## See also · 参见",
        "",
        "- Rule table + feature vocab: [`reference/derivation-rules.md`](reference/derivation-rules.md).",
        "- Core modules M0–M8: [`core/00-index.md`](core/00-index.md).",
        "- Whole-factory map (modules · capabilities · domains · CLI): [`HARNESS-MAP.md`](HARNESS-MAP.md).",
        "- Tool catalog: [`review/harness-index.md`](review/harness-index.md) (`harness catalog`).",
        "",
    ]
    return "\n".join(lines)


def write_doc(path: Path | None = None) -> Path:
    target = path or DOC_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_doc(), encoding="utf-8")
    return target
