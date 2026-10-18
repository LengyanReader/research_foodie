"""Turn a :class:`HarnessPlan` into concrete files (in memory or on disk)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .capabilities import capabilities as _capabilities
from .config import factory_root as _factory_root
from .registry import domains as _domains
from .render import render, render_template
from .spec import HarnessPlan

# output path -> template file
_TEMPLATE_MAP = {
    "AGENTS.md": "AGENTS.md.tmpl",
    "tasks/PLAN.md": "tasks_PLAN.md.tmpl",
    "tasks/PROGRESS.md": "tasks_PROGRESS.md.tmpl",
    ".harness/gates.md": "gates.md.tmpl",
    ".harness/check.py": "check.py.tmpl",
    ".harness/ledger.md": "ledger.md.tmpl",
    ".harness/skills/README.md": "skills_README.md.tmpl",
    ".harness/decisions.md": "decisions.md.tmpl",
    ".harness/capabilities.local.md": "capabilities_local.md.tmpl",
    ".harness/PROVENANCE.md": "PROVENANCE.md.tmpl",
}

_MANIFEST = ".harness/manifest.json"
_POINTER = ".harness/pointer.json"
_PROFILE = ".harness/PROFILE.md"
_SKILLS_DIR = ".harness/skills"
_PORTABLE_SKILL_TEMPLATE = "skills_SKILL.md.tmpl"


def _enabled(plan: HarnessPlan, module_id: str) -> bool:
    return any(m.module_id == module_id and m.enabled for m in plan.modules)


def skill_name(plan: HarnessPlan) -> str:
    """The Agent Skills ``name`` for the emitted harness (also its directory name).

    Must be lowercase letters/digits/hyphens, no leading/trailing hyphen (Agent
    Skills spec). Domain ids already satisfy this, so ``harness-<domain>`` is safe.
    """
    slug = "".join(c if (c.isalnum() or c == "-") else "-" for c in plan.features.domain.lower())
    slug = slug.strip("-") or "general"
    return f"harness-{slug}"[:64].rstrip("-")


def skill_path(plan: HarnessPlan) -> str:
    return f"{_SKILLS_DIR}/{skill_name(plan)}/SKILL.md"


def _selected_files(plan: HarnessPlan) -> list[str]:
    names = [
        "AGENTS.md",
        "tasks/PLAN.md",
        "tasks/PROGRESS.md",
        ".harness/gates.md",
        ".harness/check.py",
        ".harness/PROVENANCE.md",
        ".harness/capabilities.local.md",
    ]
    if _enabled(plan, "M2"):
        names.append(".harness/ledger.md")
    if _enabled(plan, "M6"):
        names.append(".harness/skills/README.md")
        names.append(skill_path(plan))
    if _enabled(plan, "M8"):
        names.append(".harness/decisions.md")
    names.append(_MANIFEST)
    names.append(_POINTER)
    return sorted(names)


def _evidence_instrument(plan: HarnessPlan) -> str:
    """Name the instrument this harness must use (M3.10 · match the instrument to the claim).

    Derived from the matched capabilities, so an emitted harness states *what evidence would
    settle its claim* before any work starts -- instead of discovering at the end that the
    "proof" was an opinion or the "result" had no interval.
    """
    caps = set(plan.capabilities)
    lines = [
        f"- **{family}** — {detail} (`reference/evidence-instruments.md#{anchor}`)."
        for cid, family, detail, anchor in _INSTRUMENTS
        if cid in caps
    ]
    if not lines and ({"reproducible-experiments", "eval-driven-development"} & caps):
        lines.append(
            "- **re-runnable pipeline + frozen golden cases** — the check reproduces the result from "
            "recorded inputs and versions, and the evaluation set is frozen *before* the change "
            "(`reference/evidence-instruments.md#computational-provenance`)."
        )
    if not lines:
        lines.append(
            "- **observed evidence for the artefact** — name the concrete artefact the claim rests on "
            "(test run, log, metric, source + access date) *before* claiming done; a claim with no "
            "named instrument is unverified (M3.1, M3.10)."
        )
    return "\n".join(lines)


# capability -> (instrument family, what the gate must observe, anchor in the instrument map)
_INSTRUMENTS: tuple[tuple[str, str, str, str], ...] = (
    (
        "formal-verification",
        "machine-checked derivation",
        "a compiled proof (Lean 4 / Rocq / Isabelle / Agda), a verified obligation (Dafny / Z3), or an "
        "explored state space (TLA+ / Alloy) — with the toolchain version recorded and **no placeholder "
        "left** (`sorry`, `Admitted`, `postulate`)",
        "formal-claims",
    ),
    (
        "dimensional-analysis",
        "units + propagated uncertainty",
        "every quantity carries its unit and an uncertainty with a stated coverage factor (Pint / "
        "uncertainties, GUM) — **no unit-free numbers**",
        "physical-quantities",
    ),
    (
        "empirical-measurement",
        "effect size + interval + reliability",
        "a pre-registered primary analysis (or a declared deviation), an effect size **with an interval**, "
        "and a reliability estimate for the measure (PsychoPy / jsPsych, lme4 / statsmodels / Stan, OSF)",
        "empirical-claims",
    ),
)


def _context(plan: HarnessPlan, params: dict[str, Any]) -> dict[str, Any]:
    f = plan.features
    domain_meta = _domains().get(f.domain, _domains().get("general", {}))
    enabled = plan.enabled_modules()

    modules_line = ", ".join(m.module_id for m in enabled)
    modules_table = "\n".join(
        f"| {m.module_id} | {m.title_en} / {m.title_zh} | {m.rule_en} |" for m in enabled
    )
    modules_reasons_table = "\n".join(
        f"| {m.module_id} | {m.title_en} / {m.title_zh} | {m.rule_en} | {'; '.join(m.reasons)} |"
        for m in enabled
    )
    cap_catalog = _capabilities()
    cap_rows = []
    for cid in plan.capabilities:
        meta = cap_catalog.get(cid, {})
        title = meta.get("title_en", cid)
        cap_rows.append(f"| {cid} | {title} — {meta.get('why', '')} |")
    capabilities_table = "\n".join(cap_rows) or "| _(none matched)_ | |"
    capabilities_line = ", ".join(plan.capabilities) or "(none)"
    evidence_instrument = _evidence_instrument(plan)
    workflow = domain_meta.get("workflow", [])
    workflow_list = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(workflow))

    gates_strict = params.get("gate_strictness", "standard")
    hard_gates = [
        "- [ ] All referenced files exist and are fully rendered (no template placeholders).",
        "- [ ] `.harness/manifest.json` validates.",
    ]
    if _enabled(plan, "M4"):
        hard_gates.append(
            "- [ ] Every load-bearing claim has a source + access date, or is marked `unverified`."
        )
    soft_gates = ["- [ ] Deliverable matches the stated goal."]
    if _enabled(plan, "M8"):
        soft_gates.append("- [ ] Reviewer approved the deliverable.")

    skill = skill_name(plan)
    skill_desc = (
        f'Derived agent workflow for "{(plan.task.text or "").strip()[:60]}" '
        f"(domain {f.domain}; modules {modules_line}). Load when resuming this "
        "project's agent work to apply its context, memory, verification, and "
        "governance rules."
    )[:1024]

    return {
        "version": plan.version,
        "created": plan.created,
        "task_text": plan.task.text,
        "task_short": (plan.task.text or "").strip()[:80],
        "goal": plan.task.goal or "(state the goal in tasks/PLAN.md)",
        "skill_name": skill,
        "skill_description": skill_desc,
        "domain": f.domain,
        "domain_title": domain_meta.get("title_en", f.domain),
        "domain_zh": domain_meta.get("name_zh", ""),
        "domain_summary": domain_meta.get("summary", ""),
        "f_horizon": f.horizon,
        "f_verifiability": f.verifiability,
        "f_stakes": f.stakes,
        "f_grounding": f.grounding,
        "f_artifact": f.artifact,
        "f_tool_surface": f.tool_surface,
        "f_collaboration": f.collaboration,
        "f_source": f.source,
        "features_line": (
            f"horizon={f.horizon}, verifiability={f.verifiability}, stakes={f.stakes}, "
            f"grounding={f.grounding}, artifact={f.artifact}, tool_surface={f.tool_surface}, "
            f"collaboration={f.collaboration}, domain={f.domain}"
        ),
        "modules_line": modules_line,
        "modules_table": modules_table,
        "modules_reasons_table": modules_reasons_table,
        "capabilities_line": capabilities_line,
        "capabilities_table": capabilities_table,
        "evidence_instrument": evidence_instrument,
        "profile_note": "",
        "workflow_list": workflow_list,
        "gate_strictness": gates_strict,
        "hard_gates": "\n".join(hard_gates),
        "soft_gates": "\n".join(soft_gates),
        "gates_extra": (
            "\n> Provenance is required: prefer primary sources; mark anything you cannot trace as "
            "`unverified`."
            if _enabled(plan, "M4")
            else ""
        ),
        "memory_extra": (
            "- Keep durable state in `.harness/ledger.md` (append-only) and resume from it."
            if _enabled(plan, "M2")
            else ""
        ),
        "collaboration_extra": (
            "- Escalate irreversible decisions to a human; log them in `.harness/decisions.md`."
            if _enabled(plan, "M8")
            else ""
        ),
        "memory_depth": params.get("memory_depth", "session"),
        "tool_surface": params.get("tool_surface", f.tool_surface),
        "collaboration": params.get("collaboration", f.collaboration),
        "autonomy": params.get("autonomy", "medium"),
        "evolution_cadence": params.get("evolution_cadence", "off"),
        "provenance": params.get("provenance", f.grounding),
        "dod_list": "\n".join(
            ["- [ ] Deliverable matches the goal", "- [ ] Hard gates pass with attached evidence"]
            + (["- [ ] Sources recorded for every claim"] if _enabled(plan, "M4") else [])
        ),
    }


def build_files(
    plan: HarnessPlan,
    extra: dict[str, str] | None = None,
    factory_root: str | None = None,
) -> dict[str, str]:
    """Return ``{relative_path: content}`` for the whole harness.

    ``extra`` may inject optional artifacts (e.g. ``{"profile_md": ...,
    "profile_note": ...}``), used when a project profile is attached.

    ``factory_root`` pins the path recorded in ``.harness/pointer.json`` and in
    ``AGENTS.md``; by default it is auto-detected (:func:`config.factory_root`).
    """
    from . import plugins, pointer

    extra = extra or {}
    params = plan.params()
    ctx = _context(plan, params)
    ctx["profile_note"] = extra.get("profile_note", "")

    root = Path(factory_root) if factory_root else _factory_root()
    if root is not None and not (root / "SKILL.md").is_file():
        root = None  # pinned to a directory that is not a factory checkout
    ctx["factory_root"] = root.as_posix() if root else "<harness_factory path>"

    plugin_targets = plugins.domain_template_targets(plan.features.domain)

    names = _selected_files(plan)
    if extra.get("profile_md"):
        names = [*names, _PROFILE]
    names = sorted({*names, *plugin_targets})
    plan.files = names
    ctx["files_list"] = "\n".join(f"- `{name}`" for name in names)

    files: dict[str, str] = {}
    for name in names:
        if name == _MANIFEST:
            continue
        if name == _POINTER:
            files[name] = pointer.render(
                pointer.build(
                    str(root) if root else None, created=plan.created, version=plan.version
                )
            )
            continue
        if name == _PROFILE:
            files[name] = extra["profile_md"]
            continue
        if name in plugin_targets:
            try:
                template_text = plugin_targets[name].read_text(encoding="utf-8")
            except OSError:
                continue
            files[name] = render(template_text, ctx)
            continue
        if name == skill_path(plan):
            files[name] = render_template(_PORTABLE_SKILL_TEMPLATE, ctx)
            continue
        files[name] = render_template(_TEMPLATE_MAP[name], ctx)

    files[_MANIFEST] = json.dumps(plan.to_dict(), ensure_ascii=False, indent=2) + "\n"
    return files


def write_harness(
    plan: HarnessPlan,
    out_dir: str | Path,
    force: bool = False,
    extra: dict[str, str] | None = None,
    factory_root: str | None = None,
) -> list[str]:
    """Write the harness to ``out_dir``; return the written paths.

    Checks all destinations before writing anything, so a collision leaves the
    tree untouched.
    """
    out = Path(out_dir)
    files = build_files(plan, extra=extra, factory_root=factory_root)

    if not force:
        clashes = [name for name in files if (out / name).exists()]
        if clashes:
            raise FileExistsError(
                "refusing to overwrite existing files (use --force): " + ", ".join(sorted(clashes))
            )

    written: list[str] = []
    for name, content in files.items():
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        written.append(name)
    return sorted(written)
