"""Generate ``HARNESS-MAP.md``: one page that shows the whole factory at a glance.

Everything on the map comes from a surface that already exists -- the JSON
catalogs (``data/*.json``), the CLI parser, the skill index, or the emitted
templates -- so the map cannot drift from reality: ``render_doc()`` is compared
with the file on disk by the test suite, exactly like ``CAPABILITIES.md``.

Observe-only (M0.4): this module reads catalogs and renders a view. It never
edits an SSOT.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../harness_factory
DOC_PATH = ROOT / "HARNESS-MAP.md"
_TEMPLATES = Path(__file__).resolve().parent / "templates"

_FACULTY_ZH = {
    "meta": "元",
    "formal-sciences": "形式科学",
    "engineering": "工程",
    "natural-sciences": "自然科学",
    "health": "健康",
    "social-sciences": "社会科学",
    "law": "法学",
    "humanities": "人文学科",
    "education": "教育",
    "arts": "艺术",
}


def _faculties(domains: dict) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for did, meta in domains.items():
        groups.setdefault(meta.get("faculty", "general"), []).append(did)
    return {k: sorted(v) for k, v in sorted(groups.items())}


def _cli_commands() -> list[tuple[str, str]]:
    """Top-level subcommands + their help, read straight from the parser."""
    import argparse

    from . import cli

    out: list[tuple[str, str]] = []
    for action in cli.build_parser()._actions:
        if not isinstance(action, argparse._SubParsersAction):
            continue
        helps = {a.dest: (a.help or "") for a in action._choices_actions}
        out.extend((name, helps.get(name, "")) for name in action.choices)
    return out


def _template_files() -> list[str]:
    if not _TEMPLATES.is_dir():
        return []
    return sorted(
        p.relative_to(_TEMPLATES).as_posix() for p in _TEMPLATES.rglob("*") if p.is_file()
    )


def summary() -> dict[str, int]:
    """Headline counts, each read from its SSOT (used by ``harness map`` / tests)."""
    from . import catalog, standard
    from .capabilities import capabilities
    from .registry import domains, modules

    levers = standard.levers() or {}
    by_dim = levers.get("by_dim") or {}
    return {
        "modules": len(modules()),
        "capabilities": len(capabilities()),
        "domains": len(domains()),
        "catalog_entries": len(catalog.items()),
        "catalog_classes": len(catalog.classes()),
        "catalog_kinds": len(catalog.kinds()),
        "rubrics": len(standard.rubrics()),
        "levers": len(by_dim),
        "cli_commands": len(_cli_commands()),
        "templates": len(_template_files()),
    }


def render_doc() -> str:
    """Render the whole map from the current catalogs + CLI + templates."""
    from . import catalog, skill, standard
    from .capabilities import _when_text, capabilities
    from .registry import domains, modules

    mods = modules()
    caps = capabilities()
    doms = domains()
    items = catalog.items()
    class_rows = catalog.classes()
    kinds = catalog.kinds()
    rubrics = standard.rubrics()
    levers = standard.levers()
    commands = _cli_commands()
    templates = _template_files()

    facs = _faculties(doms)
    disciplines = [d for d in doms if d != "general"]
    by_class = {c["id"]: sum(1 for e in items if e.get("class") == c["id"]) for c in class_rows}
    load_index = [s for s in skill.index() if s.group != "domains"]

    lines: list[str] = []
    add = lines.append

    add("# Harness Map · Harness 地图")
    add("")
    add(
        "> **Generated** from the catalogs + the CLI + the skill index -- **do not edit by "
        "hand**; run `harness map --write` (also refreshed by `harness catalog --write`)."
    )
    add(
        "> **生成文档**：由 SSOT 与 CLI 生成，**请勿手改**；用 `harness map --write` 重新生成"
        "（`harness catalog --write` 亦会同步刷新）。"
    )
    add("")
    add(
        f"**{len(mods)} modules (M0–M8) · {len(caps)} capabilities · {len(doms)} domains · "
        f"{len(items)} catalog entries · {len(commands)} CLI subcommands**"
    )
    add("")
    add("---")
    add("")
    add("## 中文速览")
    add("")
    add(
        "这张地图把 harness_factory **所有部件**画在一页上：9 个核心模块（M0–M8）、"
        f"{len(caps)} 条能力（capability，任务特征 → 模块）、{len(doms)} 个学科域、"
        f"{len(items)} 条工具目录、{len(commands)} 个 CLI 子命令、以及 L0/L1 两种消费形态。"
        "它回答三个问题：**(1)** 有哪些部件；**(2)** 每个部件的数据源（SSOT）在哪；"
        "**(3)** 改完 SSOT 后跑哪条命令同步。整份文档**由代码生成**（`harness map --write`），"
        "并由 `tests/test_harness_map.py` 做漂移守卫——因此它随每次更新自动保持一致。"
    )
    add("")
    add("## 0 · At a glance · 一览")
    add("")
    add("| surface · 面 | count | SSOT | view |")
    add("|---|---|---|---|")
    add(f"| Core modules | {len(mods)} (M0–M8) | `data/modules.json` | `core/00-index.md` |")
    add(
        f"| Capabilities | {len(caps)} | `data/capabilities.json` | "
        "[`CAPABILITIES.md`](CAPABILITIES.md) |"
    )
    add(
        f"| Domains | {len(doms)} ({len(disciplines)} + `general`) | `data/domains.json` | "
        "`domains/<id>/README.md` |"
    )
    add(
        f"| Tool catalog | {len(items)} ({len(class_rows)} classes × {len(kinds)} kinds) | "
        "`data/harnesses.json` | [`review/harness-index.md`](review/harness-index.md) |"
    )
    add(f"| Rubrics | {len(rubrics)} | `data/rubrics.json` | `domains/excellence/standard-ladder.md` |")
    add(f"| Levers | {len(levers.get('by_dim', {}))} | `data/levers.json` | `harness standard plan` |")
    add(f"| CLI subcommands | {len(commands)} | `src/harness_factory/cli.py` | §7 below |")
    add(f"| Emitted templates | {len(templates)} | `src/harness_factory/templates/` | §8 below |")
    add("")
    add("## 1 · The map · 全景")
    add("")
    add("```")
    add("              you point an assistant at this directory (or paste the standing line)")
    add("                                    │")
    add("              ┌─────────────────────┴─────────────────────┐")
    add("              │ L0 · agent-native        L1 · CLI-from-path │")
    add("              │ SKILL.md + core/ + data  python -m harness_factory")
    add("              └─────────────────────┬─────────────────────┘")
    add("                                    ▼")
    add("   task ──▶ feature vector ──▶ capability match ──▶ modules M0–M8 ──▶ emitted harness")
    add("            (classify.py)       (capabilities.json)   (derive.py)      (.harness/, tasks/, AGENTS.md)")
    add("                                                                              │")
    add("                          ┌───────────────────────────────────────────────────┘")
    add("                          ▼")
    add("   updates/  ◀──proposals──(M5 self-evolution)── read: review/ · sources/ · updates/")
    add("             human gate")
    add("```")
    add("")
    add("## 2 · How a task becomes a harness · 任务 → harness")
    add("")
    add(
        "1. **Classify** the goal into the 8-axis feature vector "
        "(`horizon·verifiability·stakes·grounding·artifact·tool_surface·collaboration·domain`)."
    )
    add("2. **Match** every capability whose `when` matches that vector (`data/capabilities.json`).")
    add(
        "3. **Select** the core modules M0–M8 the rules enable, with per-module reasons "
        "(`derive.py`)."
    )
    add(
        "4. **Annotate** the enabled modules with the matching capabilities -- explainability "
        "only, never an override (M0.4)."
    )
    add(
        "5. **Emit** the scaffold (`init`): `AGENTS.md`, `tasks/PLAN.md`, `tasks/PROGRESS.md`, "
        "`tasks/decisions.md`, `tasks/gates.md`, `tasks/ledger.md`, `.harness/*` (manifest, "
        "pointer, capabilities ledger, PROVENANCE) and `.harness/check.py`."
    )
    add("")
    add("## 3 · Core modules · 核心模块 (M0–M8)")
    add("")
    add("| id | module | rule | doc |")
    add("|---|---|---|---|")
    for mid, meta in sorted(mods.items()):
        title = f"{meta.get('title_en', '')} · {meta.get('title_zh', '')}"
        add(f"| {mid} | {title} | {meta.get('rule_en', '')} | `{meta.get('doc', '')}` |")
    add("")
    add(f"## 4 · Capabilities · 能力（{len(caps)}）")
    add("")
    add(
        "A capability is a *reusable requirement*: it fires when the task's feature vector "
        "matches its `when`, then **annotates** the already-enabled modules with why they "
        "matter (M0.4). Trigger renderer shared with `CAPABILITIES.md`; full text (fires-when "
        "+ why) there."
    )
    add("")
    add("| capability | modules | fires when |")
    add("|---|---|---|")
    for cid, meta in caps.items():
        modules_of = ", ".join(meta.get("modules", [])) or "--"
        add(f"| `{cid}` | {modules_of} | {_when_text(meta.get('when', {}))} |")
    add("")
    add("## 5 · Domains · 学科域")
    add("")
    add(
        f"{len(doms)} domains across {len(facs)} faculties (`general` is the always-available "
        "fallback). Each domain is a *workflow + signals + artifact* hint; it adds no rule "
        "(M0.5)."
    )
    add("")
    add("| faculty | domains |")
    add("|---|---|")
    for fac, ids in facs.items():
        label = f"{fac} · {_FACULTY_ZH[fac]}" if fac in _FACULTY_ZH else fac
        add(f"| {label} | {', '.join('`' + i + '`' for i in ids)} |")
    add("")
    add(f"## 6 · Tool catalog · 工具目录（{len(items)}）")
    add("")
    add(
        "`data/harnesses.json` indexes third-party agent harnesses, frameworks, protocols, "
        "evaluation tools and safety work, each mapped to the modules it exercises. Lookup "
        "with `harness catalog`."
    )
    add("")
    add("| class | entries |")
    add("|---|---|")
    for row in class_rows:
        add(f"| {row.get('id')} · {row.get('en', '')} | {by_class.get(row.get('id'), 0)} |")
    add("")
    add(f"## 7 · CLI surface · 命令行（{len(commands)} subcommands）")
    add("")
    add("`PYTHONPATH=<harness_factory>/src python -m harness_factory <cmd>` (or the installed `harness`).")
    add("")
    add("| cmd | what it does |")
    add("|---|---|")
    for name, help_text in commands:
        add(f"| `{name}` | {help_text.strip() or '--'} |")
    add("")
    add("## 8 · Entry points & load order · 入口与加载顺序")
    add("")
    add(
        "The agent-native load index (`harness skill`). Read top-down; load only what you need "
        "(M0.6). Domain READMEs are omitted here -- see §5."
    )
    add("")
    add("| load | path | why |")
    add("|---|---|---|")
    for entry in load_index:
        add(f"| `{entry.name}` | `{entry.path}` | {entry.description} |")
    add("")
    add("## 9 · Data sources → views · SSOT 与生成视图")
    add("")
    add("| SSOT | drives | generated view |")
    add("|---|---|---|")
    add("| `data/modules.json` | M0–M8 + params | `core/*` (hand), §3 |")
    add("| `data/capabilities.json` | requirement → modules | `CAPABILITIES.md` |")
    add("| `data/harnesses.json` | tool catalog | `review/harness-index.md` |")
    add("| `data/domains.json` | disciplines + signals | `domains/<id>/README.md` |")
    add("| `data/rubrics.json` | per-domain excellence bar | `harness standard` |")
    add("| `data/levers.json` | gap → modules/tools | `harness standard plan` |")
    add("| `data/watchlist.json` | M5 frontier probes | `updates/REPORT.md` |")
    add("| `data/sources.json` | tracked entities + feeds + per-field `outlets` | `updates/INTEL.md` |")
    add("")
    add("## 10 · Keeping this current · 如何保持同步")
    add("")
    add("This document is **generated**: edit an SSOT, regenerate, done.")
    add("")
    add("| after you edit… | run | refreshes |")
    add("|---|---|---|")
    add("| any `data/*.json` | `harness catalog --write` | `review/harness-index.md` + `CAPABILITIES.md` + `HARNESS-MAP.md` |")
    add("| `data/capabilities.json` | `harness capabilities --write` | `CAPABILITIES.md` |")
    add("| anything | `harness map --write` | this file |")
    add("")
    add(
        "`tests/test_harness_map.py` fails when the file is stale; the fix is always "
        "`harness map --write`. An emitted harness reads the factory through "
        "`.harness/pointer.json`, and the standing reference lives in `SKILL.md`."
    )
    add("")
    add("## See also · 参见")
    add("")
    add("- [`CAPABILITIES.md`](CAPABILITIES.md) -- the same guarantees, per capability.")
    add("- [`reference/capability-router.md`](reference/capability-router.md) -- *situation → capability → file*.")
    add("- [`review/harness-index.md`](review/harness-index.md) -- the tool catalog.")
    add("- [`GUIDE.md`](GUIDE.md) · [`introduction.md`](introduction.md) -- usage, mental model.")
    add("")
    return "\n".join(lines)


def write_doc(path: Path | None = None) -> Path:
    target = path or DOC_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_doc(), encoding="utf-8")
    return target
