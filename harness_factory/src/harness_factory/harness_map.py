"""Generate ``HARNESS-MAP.md``: one page that shows the whole factory at a glance.

Everything on the map comes from a surface that already exists -- the JSON
catalogs (``data/*.json``), the CLI parser, the skill index, or the emitted
templates -- so the map cannot drift from reality: ``render_doc()`` is compared
with the file on disk by the test suite, exactly like ``CAPABILITIES.md``.

Two additions make the page explain itself rather than merely list ids:

* **an architecture diagram** (``render_architecture``) -- the classify ->
  capability -> module -> artifact -> evolution flow, with counts read from the
  catalogs, so a reader sees the shape before the tables;
* **one worked example** (``worked_example``) -- ``classify`` + ``derive`` run on
  two fixed tasks, i.e. the real pipeline output, not a hand-written sample.

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

# The eight classifier axes: what each one *asks*. ``spec.FEATURE_CHOICES`` is the
# authority for the vocabulary; this table only adds the gloss. A test keeps the
# key sets identical, so a new axis cannot appear without a gloss.
_AXIS_ASK_EN = {
    "horizon": "How long does the work span?",
    "verifiability": "Can a machine decide it is right?",
    "stakes": "What does being wrong cost?",
    "grounding": "Must every claim carry a source?",
    "artifact": "What ships?",
    "tool_surface": "What may the agent touch?",
    "collaboration": "Who works alongside?",
    "domain": "Which discipline fires?",
}
_AXIS_ASK_ZH = {
    "horizon": "任务跨多久：一次做完，还是跨会话续跑",
    "verifiability": "结果能否被机器判定：测试/评分 vs. 人眼",
    "stakes": "做错的代价：要不要硬门禁、沙箱、人工复核",
    "grounding": "断言要不要来源：要不要溯源与证据分级",
    "artifact": "交付物是什么：决定验证方式与表达形式",
    "tool_surface": "agent 能碰什么：只读 / 读写 / 外部网络",
    "collaboration": "谁在一起干：单人 / 人工复核 / 多 agent",
    "domain": "命中哪个学科：加载该域的方法论与仪器",
}
_AXIS_ZH = {
    "horizon": "时间跨度",
    "verifiability": "可验证性",
    "stakes": "风险",
    "grounding": "来源要求",
    "artifact": "产物",
    "tool_surface": "工具面",
    "collaboration": "协作",
    "domain": "领域",
}

# Two fixed tasks whose derived harnesses differ in shape as well as in detail.
_EXAMPLES = (
    ("A · code", "为现有 Python 项目补全类型注解与单元测试，保证可验证闭环"),
    ("B · long-lived, high stakes", "长期维护一个生产级医疗问答系统，多次上线，出错代价高，需要人工复核"),
)


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


def _when_axes(when: dict) -> set[str]:
    """The classifier axes a ``when`` clause keys on (``min_horizon`` -> horizon).

    ``when`` is a small expression language: a plain dict is a conjunction, an
    ``any`` key is a disjunction. Anything else is a mistake worth raising, not
    silently dropping from the diagram.
    """
    conds: list[dict] = list(when.get("any", []))
    rest = {k: v for k, v in when.items() if k != "any"}
    if rest or not conds:
        conds.append(rest)
    axes: set[str] = set()
    for cond in conds:
        for key in cond:
            axes.add("horizon" if key == "min_horizon" else key)
    unknown = axes - set(_AXIS_ASK_EN)
    if unknown:
        raise ValueError(f"unknown when-axis {sorted(unknown)} in {when!r}")
    return axes


def axis_counts() -> dict[str, int]:
    """Capabilities per trigger axis, plus the unconditional ``always`` group.

    A capability that keys on two axes counts in both, so the values sum to more
    than the number of capabilities -- the map says so in its caption.
    """
    from .capabilities import capabilities

    counts = {"always": 0, **{axis: 0 for axis in _AXIS_ASK_EN}}
    for meta in capabilities().values():
        axes = _when_axes(meta.get("when", {}))
        if not axes:
            counts["always"] += 1
        for axis in axes:
            counts[axis] += 1
    return counts


def module_capability_counts() -> dict[str, int]:
    """How many capabilities annotate each module (reverse index size)."""
    from .capabilities import capabilities
    from .registry import modules

    counts = {mid: 0 for mid in modules()}
    for meta in capabilities().values():
        for mid in meta.get("modules", []):
            if mid in counts:
                counts[mid] += 1
    return counts


def worked_example() -> list[dict]:
    """Run ``classify`` + ``derive`` on the two fixed tasks (real output, no LLM)."""
    from .classify import classify
    from .derive import derive
    from .spec import TaskSpec

    out: list[dict] = []
    for label, text in _EXAMPLES:
        task = TaskSpec(text=text)
        features = classify(task, use_llm=False)
        plan = derive(task, features)
        out.append(
            {
                "label": label,
                "task": text,
                "features": [(k, getattr(features, k)) for k in _AXIS_ASK_EN],
                "capabilities": list(plan.capabilities),
                "enabled": [m.module_id for m in plan.modules if m.enabled],
                "disabled": [m.module_id for m in plan.modules if not m.enabled],
            }
        )
    return out


def _codes(ids: list[str]) -> str:
    return ", ".join(f"`{i}`" for i in ids)


def _first_clause(text: str, limit: int = 104) -> str:
    """Keep a summary to its first clause, so one row stays one line."""
    text = " ".join(text.split())
    for sep in (". ", "; ", " — ", ": "):
        head = text.split(sep)[0]
        if 0 < len(head) <= limit:
            text = head
            break
    if len(text) > limit:
        text = text[: limit - 1].rstrip(" ,;:") + "…"
    return text


def _gist(text: str, limit: int = 320) -> str:
    """First sentence of a capability's ``why``; the full text lives in CAPABILITIES.md.

    A first sentence is the shortest complete statement of *what the requirement
    buys you*; the safety cap only fires on a pathologically long sentence.
    """
    text = " ".join(text.split())
    head = text.split(". ")[0]
    if 0 < len(head) <= limit:
        text = head
    if len(text) > limit:
        text = text[: limit - 1].rstrip(" ,;:") + "…"
    return text


def render_architecture() -> str:
    """A Mermaid flowchart of the whole pipeline, counts read from the catalogs."""
    from .capabilities import capabilities

    caps = capabilities()
    counts = axis_counts()
    mod_counts = module_capability_counts()
    from .registry import modules

    mods = modules()

    lines: list[str] = ["```mermaid", "flowchart TD"]
    lines.append('    T["任务 · goal"]')
    lines.append('    REF["① 入口 · L0 常驻引用 SKILL.md<br/>或 L1 python -m harness_factory"]')
    lines.append(
        '    V["② 分类 · 8 轴特征向量<br/>horizon · verifiability · stakes · grounding'
        '<br/>artifact · tool_surface · collaboration · domain"]'
    )
    lines.append(f'    subgraph CAPS["③ 能力层 · {len(caps)} 条"]')
    lines.append(f'        A0["always · 总是 {counts["always"]}"]')
    for idx, axis in enumerate(_AXIS_ASK_EN, start=1):
        lines.append(f'        A{idx}["{axis} · {_AXIS_ZH[axis]} {counts[axis]}"]')
    lines.append("    end")
    lines.append(
        '    M["命中集合 + 注解 annotate<br/>只解释模块为何相关，不覆盖选择（M0.4）"]'
    )
    order = list(_AXIS_ASK_EN)
    rows = [
        f"{mid} {mods[mid].get('title_zh', '')} {mod_counts[mid]}" for mid in sorted(mods)
    ]
    chunks = [rows[i : i + 3] for i in range(0, len(rows), 3)]
    mod_label = "<br/>".join(" · ".join(c) for c in chunks)
    lines.append(f'    MODS["④ 模块 M0–M8（数字 = 关联能力数）<br/>{mod_label}"]')
    lines.append(
        '    O1["⑤ 产物 · AGENTS.md · tasks/*<br/>PLAN · PROGRESS · decisions · gates · ledger"]'
    )
    lines.append(
        '    O2["⑤ 产物 · .harness/*<br/>manifest · pointer · 能力台账 · PROVENANCE · check.py"]'
    )
    lines.append('    E["⑥ 演化 M5 · 采集信号 → 提案"]')
    lines.append('    U["updates/*（不入版本控制）"]')
    lines.append('    G{"人工闸门"}')
    lines += [
        "    T --> V",
        "    REF --> V",
        "    T --> A0",
    ]
    for idx in range(1, len(order) + 1):
        lines.append(f"    V --> A{idx}")
    lines.append("    A0 --> M")
    for idx in range(1, len(order) + 1):
        lines.append(f"    A{idx} --> M")
    lines += [
        "    M --> MODS",
        "    MODS --> O1",
        "    MODS --> O2",
        "    O1 --> E",
        "    E --> U",
        "    U --> G",
        "    G -->|接受| REF",
        "```",
    ]
    return "\n".join(lines)


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
    from .spec import FEATURE_CHOICES

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
    counts = axis_counts()
    mod_counts = module_capability_counts()
    examples = worked_example()

    # Reverse index: module -> capabilities that annotate it.
    caps_of: dict[str, list[str]] = {mid: [] for mid in mods}
    for cid, meta in caps.items():
        for mid in meta.get("modules", []):
            if mid in caps_of:
                caps_of[mid].append(cid)

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
        "这张地图把 harness_factory 的**部件与装配过程**放在一页：一张**能力架构图**"
        f"（§2：任务 → 8 轴特征 → {len(caps)} 条能力 → 9 个模块 → 产物 → 演化回路）、"
        "每个模块的**责任边界**（§4：管什么 / **不**负责什么 / 载着哪些能力）、"
        "两条**实跑出来的**任务样例（§3：同样的流水线，换任务就换答案）、"
        f"每条能力的**触发条件 + 买到了什么**（§5）、{len(doms)} 个学科域的产物类型与来源要求（§6）、"
        f"{len(items)} 条工具目录按类对应模块（§7）、{len(commands)} 个 CLI 子命令（§8），"
        "以及 SSOT → 生成视图的同步关系（§10–§11）。"
    )
    add("")
    add(
        "整份文档**由代码生成**（`harness map --write`），`tests/test_harness_map.py` 做漂移守卫："
        "图、表、样例读的是同一批数据，改 SSOT 后重生成即可，不会出现「文档说一套、代码做一套」。"
    )
    add("")
    add("## 0 · 速查 · At a glance")
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
    add(f"| CLI subcommands | {len(commands)} | `src/harness_factory/cli.py` | §8 below |")
    add(f"| Emitted templates | {len(templates)} | `src/harness_factory/templates/` | `harness init` output |")
    add("")
    add("## 1 · 怎么读 · How to read this map")
    add("")
    add("| 你的问题 | 从这节进 | 路径 |")
    add("|---|---|---|")
    add(
        "| 我有任务，该按什么规矩做？ | §2 图 → §3 八轴 → §5 能力 | "
        "分类出向量 → 命中能力 → 读该能力的 `要点` → 它指向的模块 → `core/0X` 原文 |"
    )
    add(
        "| 某条规矩管什么、**不**管什么？ | §4 模块矩阵 | "
        "看「保证 / 不负责」两列，再看 `doc` 一列 |"
    )
    add("| 这任务属于哪个学科？ | §6 学科域 | 命中信号 → 域的 `artifact` / `grounding` / 工作流 |")
    add("| 有没有现成工具？ | §7 工具目录 → `harness catalog` | 类 → 条目 → 对应模块 |")
    add("| 我要改或扩这套库 | §10 SSOT → §11 同步 | 改 `data/*.json` → 重生成 → 跑测试 |")
    add("")
    add(
        "一条固定读法：**任务 → §3 的向量 → §5 的 `fires when` → §5 的 `要点` → §4 里该能力对应的模块 → "
        "`core/` 原文**。能力只**解释**为什么某个模块相关，永不覆盖模块选择（M0.4）。"
    )
    add("")
    add("## 2 · 能力架构图 · Capability architecture")
    add("")
    add(render_architecture())
    add("")
    add(
        f"- 六层自上而下单向流动；只有一条回边（⑥ 演化），而且**必须过人工闸门**才回到入口。"
    )
    add(
        "- `always` 组由**任务本身**触发（不经向量判断），其余八组各由对应的分类轴触发。"
    )
    add(
        f"- 能力层按**触发轴**计数：一条能力可同时看多个轴（`traceable-sources` 同时看 `grounding` 与 "
        f"`artifact`），故各轴之和 {sum(counts.values())} > {len(caps)}，不是重复计算错误。"
    )
    add("- 图由 `harness_map.render_architecture()` 现算，不手绘；改 catalog 即改图。")
    add("")
    add("| 层 | 装什么 | 关键约束 | 代码 / SSOT |")
    add("|---|---|---|---|")
    add(
        "| ① 入口 | L0 常驻引用（`SKILL.md`，免安装）· L1 命令行 | 两形态**等价**，读的是同一批文件 | "
        "`SKILL.md` · `cli.py` |"
    )
    add("| ② 分类 | 8 轴特征向量 | 只**描述**任务，不编造任务内容（M0.4） | `classify.py` · `spec.py` |")
    add(
        f"| ③ 能力 | {len(caps)} 条可复用要求 | 命中即**注解**，永不覆盖模块选择（M0.4） | "
        "`data/capabilities.json` |"
    )
    add("| ④ 模块 | M0–M8 规则本体 | 按依赖排序，后序假定前序 | `data/modules.json` · `core/` |")
    add(
        "| ⑤ 产物 | `AGENTS.md` · `tasks/*` · `.harness/*` | 必须能自证：`check` / `gate` 可跑 | "
        "`derive.py` · `assemble.py` · `templates/` |"
    )
    add(
        "| ⑥ 演化 | 信号 → 提案 → 闸门 → 日志 | 只观察/提议，不直接改 SSOT（M5） | "
        "`evolution.py` · `data/cycles.json` |"
    )
    add("")
    add("## 3 · 八个轴与两个实例 · The eight axes, twice")
    add("")
    add("分类器只问八个问题，取值是闭集——所以规则可以被检查，而不是靠感觉：")
    add("")
    add("| 轴 · axis | 这一轴在问什么 | 取值 |")
    add("|---|---|---|")
    for axis, choices in FEATURE_CHOICES.items():
        values = " · ".join(f"`{c}`" for c in choices)
        add(f"| `{axis}` | {_AXIS_ASK_ZH[axis]}<br/>*{_AXIS_ASK_EN[axis]}* | {values} |")
    add(f"| `domain` | {_AXIS_ASK_ZH['domain']}<br/>*{_AXIS_ASK_EN['domain']}* | {len(doms)} 个域 id（§6） |")
    add("")
    add(
        "下面两段是 `classify` + `derive` 的**真实输出**（规则分类，未用 LLM；命令见 "
        "`harness derive --task \"…\"`）。同一条流水线，换任务就换答案："
    )
    add("")
    header = "| " + " | ".join(_AXIS_ASK_EN) + " |"
    rule = "|" + "---|" * len(_AXIS_ASK_EN)
    for ex in examples:
        add(f"**{ex['label']}** — `{ex['task']}`")
        add("")
        add(header)
        add(rule)
        add("| " + " | ".join(f"`{v}`" for _, v in ex["features"]) + " |")
        add("")
        add(f"- **命中能力（{len(ex['capabilities'])}）**：{_codes(ex['capabilities'])}")
        add(
            f"- **启用模块**：{' '.join(ex['enabled'])}"
            + (f" · **未启用**：{' '.join(ex['disabled'])}" if ex["disabled"] else " （全开）")
        )
        add("")
    only_b = [c for c in examples[1]["capabilities"] if c not in examples[0]["capabilities"]]
    only_a = [c for c in examples[0]["capabilities"] if c not in examples[1]["capabilities"]]
    add(
        f"**差别不在模块，在要求**：两例都启用了 M0–M4、M6、M7，但 B（长期 + 高代价 + 人工复核）"
        f"多出 {len(only_b)} 条：{_codes(only_b)}；A 独有 {_codes(only_a)}。"
        "这就是能力层的作用——模块回答「用哪些规矩」，能力回答「这些规矩在这单任务上意味着什么」。"
    )
    add("")
    add("## 4 · 模块 × 能力 · Modules and what they carry")
    add("")
    add(
        "「保证」是模块的规矩；「不负责」是它的**边界**——多数误用来自越界引用"
        "（拿 M3 去决定做什么、拿 M1 去判定对错、拿 M5 直接改 SSOT）。"
        "「能力数」是 `capabilities.json` 里 `modules` 字段的反向索引，回答「谁把这条模块拉进来」。"
    )
    add("")
    add("| id | module | guarantee · 保证 | boundary · 不负责 | 能力数 | doc |")
    add("|---|---|---|---|---|---|")
    for mid, meta in sorted(mods.items()):
        title = f"{meta.get('title_en', '')} · {meta.get('title_zh', '')}"
        excl = f"{meta.get('excludes_en', '')}<br/>*{meta.get('excludes_zh', '')}*"
        add(
            f"| {mid} | {title} | {meta.get('rule_en', '')} | {excl} | "
            f"{mod_counts[mid]} | `{meta.get('doc', '')}` |"
        )
    add("")
    add("<details>")
    add("<summary>反向索引：每个模块载着哪些能力（点击展开）</summary>")
    add("")
    for mid, meta in sorted(mods.items()):
        add(
            f"- **{mid} {meta.get('title_zh', '')}**（{mod_counts[mid]}）："
            f"{_codes(caps_of[mid]) or '--'}"
        )
    add("")
    add("</details>")
    add("")
    add(f"## 5 · 能力 · Capabilities（{len(caps)}）")
    add("")
    add(
        "一条能力是**可复用的要求**：任务的向量命中它的 `when`，它就规定「这件事必须做到什么」，"
        "并**注解**已启用的模块（M0.4）。`要点` 取 `why` 的**首句**；完整要求（多条句子的能力）"
        "见 [`CAPABILITIES.md`](CAPABILITIES.md)。"
    )
    add("")
    add("| capability | name | modules | fires when | 要点 · what it buys |")
    add("|---|---|---|---|---|")
    for cid, meta in caps.items():
        modules_of = ", ".join(meta.get("modules", [])) or "--"
        name = f"{meta.get('title_en', '')} · {meta.get('title_zh', '')}"
        add(
            f"| `{cid}` | {name} | {modules_of} | {_when_text(meta.get('when', {}))} | "
            f"{_gist(meta.get('why', ''))} |"
        )
    add("")
    add("## 6 · 学科域 · Domains")
    add("")
    add(
        f"{len(doms)} 个域分布在 {len(facs)} 个学科门类（`general` 是永远可用的兜底）。"
        "一个域**不加规则**（M0.5），它提供的是一套工作流 + 命中信号 + 产物类型 + 来源要求；"
        "`artifact` / `grounding` 两列是该域默认的交付物与取证强度。"
    )
    add("")
    for fac, ids in facs.items():
        label = f"{fac} · {_FACULTY_ZH[fac]}" if fac in _FACULTY_ZH else fac
        add(f"### {label}")
        add("")
        add("| domain | artifact · grounding | 要点 |")
        add("|---|---|---|")
        for did in ids:
            meta = doms[did]
            add(
                f"| `{did}` · {meta.get('name_zh', '')} | "
                f"`{meta.get('artifact', '--')}` · `{meta.get('grounding', '--')}` | "
                f"{_first_clause(meta.get('summary', ''))} |"
            )
        add("")
    add(f"## 7 · 工具目录 · Tool catalog（{len(items)}）")
    add("")
    add(
        "`data/harnesses.json` 收录第三方 agent harness、框架、协议、评测与安全工作，每条都映到它演练的模块。"
        "查具体条目用 `harness catalog search <kw>`；生成的逐条索引在 "
        "[`review/harness-index.md`](review/harness-index.md)。"
    )
    add("")
    add("| class | 中文 | entries | 主要模块 |")
    add("|---|---|---|---|")
    for row in class_rows:
        mods_of = ", ".join(row.get("maps_to", [])) or "--"
        add(
            f"| {row.get('id')} · {row.get('en', '')} | {row.get('zh', '')} | "
            f"{by_class.get(row.get('id'), 0)} | {mods_of} |"
        )
    add("")
    add(f"## 8 · CLI surface · 命令行（{len(commands)} subcommands）")
    add("")
    add(
        "`PYTHONPATH=<harness_factory>/src python -m harness_factory <cmd>`（或已安装的 `harness`）。"
        "日常只用五条：`derive`（看规划）· `init`（写脚手架）· `check` / `gate`（自证）· `skill`（取参考）。"
        "其余分三类：**看**（`map` `capabilities` `catalog` `sources` `cases` `doctor` `profile`）、"
        "**跑一轮演化**（`harvest` `evolve` `evolve-apply` `refresh` `refresh-apply` `intel` `cycle`）、"
        "**改库**（`catalog --write` `capabilities --write` `map --write` `self-update` `plugins` `standard`）。"
    )
    add("")
    add("| cmd | what it does |")
    add("|---|---|")
    for name, help_text in commands:
        add(f"| `{name}` | {help_text.strip() or '--'} |")
    add("")
    add("## 9 · Entry points & load order · 入口与加载顺序")
    add("")
    add(
        "The agent-native load index (`harness skill`). Read top-down; load only what you need "
        "(M0.6). Domain READMEs are omitted here -- see §6."
    )
    add("")
    add("| load | path | why |")
    add("|---|---|---|")
    for entry in load_index:
        add(f"| `{entry.name}` | `{entry.path}` | {entry.description} |")
    add("")
    add("## 10 · Data sources → views · SSOT 与生成视图")
    add("")
    add("| SSOT | drives | generated view |")
    add("|---|---|---|")
    add("| `data/modules.json` | M0–M8 + rules + boundaries | `core/*` (hand), §4 |")
    add("| `data/capabilities.json` | requirement → modules | `CAPABILITIES.md`, §2/§5 |")
    add("| `data/harnesses.json` | tool catalog | `review/harness-index.md`, §7 |")
    add("| `data/domains.json` | disciplines + signals | `domains/<id>/README.md`, §6 |")
    add("| `data/rubrics.json` | per-domain excellence bar | `harness standard` |")
    add("| `data/levers.json` | gap → modules/tools | `harness standard plan` |")
    add("| `data/watchlist.json` | M5 frontier probes | `updates/REPORT.md` |")
    add("| `data/sources.json` | tracked entities + feeds + per-field `outlets` | `updates/INTEL.md` |")
    add("| `data/cycles.json` | capability rounds + definition-of-done + roadmap | `harness cycle` |")
    add("")
    add("## 11 · Keeping this current · 如何保持同步")
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
    add("- [`review/harness-index.md`](review/harness-index.md) -- the tool catalog, entry by entry.")
    add("- [`GUIDE.md`](GUIDE.md) · [`introduction.md`](introduction.md) -- usage, mental model.")
    add("")
    return "\n".join(lines)


def write_doc(path: Path | None = None) -> Path:
    target = path or DOC_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_doc(), encoding="utf-8")
    return target
