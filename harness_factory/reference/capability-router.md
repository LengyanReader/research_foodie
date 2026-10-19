# Capability router · 能力路由表

> **Start here if you are an external task or project pointing at this repository.** This is the fast
> lookup from *"what is my situation / what do I need to strengthen?"* to the exact capability, module,
> and file to load. Load nothing else until a row fires. · 外部任务/项目引用本仓库时的**第一落点**：
> 由「我的情境 / 我要补哪一环」快速定位到**能力 → 模块 → 文件**。没有命中就不要加载其它内容。

**Updated:** 2026-10-19 · Load via `harness skill capability-router`. Machine-readable truth: `data/capabilities.json`, `data/modules.json`.

---

## 中文速览

这份表是**唯一的路由入口**：左边是「你会感知到的情境」（需求模糊、要提升野心、结论要可溯、要跑得久、涉及破坏性动作、要多智能体协作……），右边是**对应的能力 id（`data/capabilities.json`）、要加载的 core 模块、要读的文件**。用法：**按情境命中一行 → 只读那一行指向的文件**。若一行都不命中，默认只读 `SKILL.md` + `core/01-meta-principles.md`。想反过来（给我一个能力名，问它在什么情境触发）用 `harness capabilities`。

---

## How to use · 用法

1. Find the **situation** row that matches your task (a task may hit several rows).
2. Load only the **files** column — that is the smallest high-signal set (M0.6).
3. If the situation is a *requirement problem* (vague / under-aimed ask), run `reference/requirement-refinement.md` **before** deriving anything.
4. When done, send what you learned back with `reference/capability-flow.md` (distill direction).

> Rule of thumb: **route by situation, not by topic.** Two tasks in the same discipline can need different capabilities.

---

## Router table · 路由表

| You are facing… · 你的情境 | capability (`data/capabilities.json`) | load (core) | read (file) |
|---|---|---|---|
| An ask that is vague, under-specified, or under-aimed · 需求模糊/偏小 | `ambition-elevation` | M0, M3, M8 | [`reference/requirement-refinement.md`](requirement-refinement.md) |
| Any task at all (the floor) · 任何任务的底线 | `baseline-discipline`, `verification-gate` | M0, M1, M3, M7 | [`core/01-meta-principles.md`](../core/01-meta-principles.md), [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md) |
| Work that will span sessions / be resumed · 跨会话、需续接 | `resumable-memory`, `self-improving-loop` | M2, M5 | [`core/03-long-running-agents.md`](../core/03-long-running-agents.md), [`core/06-self-evolution.md`](../core/06-self-evolution.md) |
| Long context / tool output floods the window · 上下文膨胀 | `context-budget-policy` | M1, M2 | [`core/02-context-engineering.md`](../core/02-context-engineering.md), [`core/03-long-running-agents.md`](../core/03-long-running-agents.md) |
| Work must survive a crash and resume exactly · 需抗崩溃续跑 | `durable-execution` | M2, M3 | [`core/03-long-running-agents.md`](../core/03-long-running-agents.md), [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md) |
| Claims/citations/Facts must be traceable · 结论要可溯 | `traceable-sources` | M4 | [`core/05-provenance-and-integrity.md`](../core/05-provenance-and-integrity.md) |
| Untrusted docs / tool output / MCP servers · 接触不可信内容 | `untrusted-content-discipline` | M4, M6, M7 | [`core/05-provenance-and-integrity.md`](../core/05-provenance-and-integrity.md), [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md) |
| Runs where nobody watches the spend · 无人值守的花费 | `cost-budget-caps` | M3, M7 | [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md), [`core/08-change-governance.md`](../core/08-change-governance.md) |
| Changes to the harness must be re-scored · 需回归评测 | `eval-driven-development` | M3, M5 | [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md), [`core/06-self-evolution.md`](../core/06-self-evolution.md) |
| The result must match the best in the field · 要对标最高标准 | `frontier-standard` | M3, M5, M8 | [`domains/excellence/standard-ladder.md`](../domains/excellence/standard-ladder.md) |
| Shallow output / toy methods / self-grading · 结果太浅、自评自证 | `expert-instruments` | M3, M4, M6 | [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md), [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md) |
| Need perspectives from other fields; several workers · 要跨领域视角/多体 | `cross-field-crew` | M6, M8 | [`core/09-collaboration-and-sessions.md`](../core/09-collaboration-and-sessions.md) |
| Tools call the outside world / code executes · 触碰外部世界 | `tool-use`, `sandboxed-execution` | M6, M7 | [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md), [`core/08-change-governance.md`](../core/08-change-governance.md) |
| The capability itself must travel (a skill/plugin other harnesses load) · 能力本身要能跨 harness 携带 | `portable-skills` | M6 | [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md) |
| Others are involved / stakes are high · 他人参与/高风险 | `human-review-gate`, `high-stakes-guardrails` | M3, M8 | [`core/09-collaboration-and-sessions.md`](../core/09-collaboration-and-sessions.md) |
| Long, high-stakes autonomous run · 长时程高自主 | `long-horizon-autonomy-control` | M2, M3, M8 | [`core/03-long-running-agents.md`](../core/03-long-running-agents.md), [`core/09-collaboration-and-sessions.md`](../core/09-collaboration-and-sessions.md) |
| An agent that acts in a loop (tools, retries, re-plan) · agent 循环 | `loop-discipline` | M2, M3, M6 | [`core/03-long-running-agents.md`](../core/03-long-running-agents.md), [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md) |
| Branches, a pipeline, or several workers · 分支·流水线·多工作者 | `graph-orchestration` | M2, M8 | [`core/03-long-running-agents.md`](../core/03-long-running-agents.md), [`core/09-collaboration-and-sessions.md`](../core/09-collaboration-and-sessions.md) |
| A formal claim: proof, derivation, model, checker · 形式证明类主张 | `formal-verification` | M3, M4, M6 | [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md), [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md) |
| Physical quantities with units, error, tolerance · 带单位与误差的物理量 | `dimensional-analysis` | M3, M6 | [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md), [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md) |
| An empirical claim: study, measurement, reliability · 实证主张 | `empirical-measurement` | M3, M4 | [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md), [`core/05-provenance-and-integrity.md`](../core/05-provenance-and-integrity.md) |
| An analysis/experiment someone else must re-run · 分析/实验要他人可复现 | `reproducible-experiments` | M3, M4, M5 | [`core/04-verification-and-gates.md`](../core/04-verification-and-gates.md), [`reference/evidence-instruments.md`](evidence-instruments.md), [`domains/data-science/README.md`](../domains/data-science/README.md) |
| A statistical estimate / model / posterior · 统计估计与模型 | `statistical-inference` | M3, M4 | [`reference/evidence-instruments.md`](evidence-instruments.md), [`domains/statistics/README.md`](../domains/statistics/README.md) |
| A computed invariant: algebra, homology, knot, mesh · 计算得到的代数/拓扑量 | `certified-computation` | M3, M6 | [`reference/evidence-instruments.md`](evidence-instruments.md), [`domains/geometry-topology/README.md`](../domains/geometry-topology/README.md) |
| A named method (PRISMA, DiD, grounded theory, DoE, design science…) · 套用某套方法论 | `verification-gate`, `traceable-sources` | M3, M4 | [`reference/methodology-map.md`](methodology-map.md) |
| Text must cross languages (translate; bilingual report; EN↔ZH corroboration) · 跨语言搬运/双语交付 | `verification-gate`, `traceable-sources` | M3, M4 | [`reference/cross-language.md`](cross-language.md) |
| Need to know *where to look* in a field · 想知道某领域去哪查 | `traceable-sources` | M4 | [`reference/outlet-map.md`](outlet-map.md) |
| Growing the capability set (a round) · 要扩展或深化能力集 | `self-improving-loop` | M5, M7 | [`reference/capability-cycle.md`](capability-cycle.md), `harness cycle audit` |
| Unsure *what evidence would settle it* · 说不清用什么仪器 | `verification-gate`, `formal-verification`, `dimensional-analysis`, `empirical-measurement` | M3, M4 | [`reference/evidence-instruments.md`](evidence-instruments.md) |
| Picking a discipline to work in · 选学科门类 | — (route by *kind of work*) | — | [`domains/`](../domains) → `domains/<name>/README.md` |
| Choosing a model/method · 选模型/选方法 | — | — | [`domains/model-selection/README.md`](../domains/model-selection/README.md) |
| Want the capability list (capability → when it fires) · 反查能力 | `harness capabilities` | — | [`CAPABILITIES.md`](../CAPABILITIES.md) |
| Want the whole landscape (modules · capabilities · domains · catalog · CLI) · 想要全景 | `harness map` | — | [`HARNESS-MAP.md`](../HARNESS-MAP.md) |
| Want to learn from the work just done · 想反哺本仓库 | `bidirectional-capability-flow` | M0, M5, M7 | [`reference/capability-flow.md`](capability-flow.md) |

---

## Reverse lookup · 反查

```bash
# situation -> capability (this table, live)
PYTHONPATH=src python -m harness_factory capabilities
# capability -> the harness a goal needs
PYTHONPATH=src python -m harness_factory derive --task "<goal>" --json
# module -> one-line rule + doc
PYTHONPATH=src python -m harness_factory skill M3
```

## See also · 参见

- [`SKILL.md`](../SKILL.md) — the entry point and load-index (read first).
- [`reference/derivation-rules.md`](derivation-rules.md) — the rule table behind the router.
- [`reference/evidence-instruments.md`](evidence-instruments.md) — claim type → instrument → catalogued tool → gate evidence (M3.10).
- [`reference/methodology-map.md`](methodology-map.md) — field → methodology system → what the harness must enforce (M3.13).
- [`reference/cross-language.md`](cross-language.md) — meaning-unit (意群) alignment, corroboration by back-translation, term handling (M4.10).
- [`reference/outlet-map.md`](outlet-map.md) — field → high-quality information outlets / portals / media (`sources.json` `outlets`).
- [`CAPABILITIES.md`](../CAPABILITIES.md) — every capability and when it fires.
