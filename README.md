# research_foodie → Harness Factory

> **A generalizable library of agent-harness patterns — plus an executable compiler that derives
> the harness any task needs.**
> 跨域提炼的 **agent harness 模式库**，外加一个**把任务编译成所需 harness**的可执行工具。

**Updated:** 2026-10-14 · **Status:** active · **License:** MIT

> 中文速览：本仓库现聚焦 **`harness_factory/`**——一个「agent harness」模式库 + `harness` CLI。
> *Harness* = 让 LLM 智能体在**跨会话、长时程、有限上下文**下把任务做稳的**一整套外部化方法**
> （上下文工程 · 外部记忆 · 验证门禁 · 来源考证 · 自我演化 · 工具/技能 · 变更治理 · 协作协议）。
> 工具只做**分类/选择/生成/观察/排序**，绝不编造任务实质；所有循环产物先作为**提案**，由人确认。详见
> [`harness_factory/README.md`](harness_factory/README.md) 与 [`introduction.md`](harness_factory/introduction.md)。
>
> **给 agent 的用法（两步：先配置，再提任务）· Two steps for an agent.** ① **配置**（贴一次，可复用）：「把本仓库当 skill 使用：读
> `harness_factory/SKILL.md`，按需加载 `core/*.md`、`data/*.json`、`domains/<名>/README.md`；此后我给你的任务，请据此推导并落盘
> 所需 harness（`AGENTS.md` + `tasks/*` + `.harness/*`，写入 `.harness/manifest.json`），最后跑 `check`；只提案、不编造任务内容。」
> ② **任务**（同一轮接着写，或下一轮再发）：直接写目标，或直接附上文件/目录。详见
> [`harness_factory/SKILL.md`](harness_factory/SKILL.md)。

---

## What this is · 这是什么

An **agent harness** is everything *around* the model that turns a probabilistic text generator into
a reliable, long-running worker: the context you feed it, the memory you externalize, the tools you
expose, the gates that decide "done", the provenance that keeps it honest, and the loop that makes
the harness itself improve. The model is the engine; the harness is the vehicle, the dashboard, the
seatbelts, and the maintenance manual.

This repository holds two things:

1. **A pattern library** — cross-domain harness patterns distilled so they survive removal of their
   originating project (`core/`, `domains/`, `review/`, `sources/`).
2. **The `harness` CLI** — a compiler that classifies a task, selects the modules it needs, emits a
   runnable harness scaffold, and **self-updates** its own knowledge base on a cadence.

**Design stance.** The compiler only *classifies, selects, and emits* — it never fabricates task
substance. Every derivation is logged in `.harness/manifest.json`. The refresh/evolution loop is
*observe-only*: it audits, counts, and ranks, then writes proposals under `updates/` for a human to
merge. See [`harness_factory/core/01-meta-principles.md`](harness_factory/core/01-meta-principles.md).

---

## Quickstart · 快速开始

```bash
cd harness_factory

# fastest path: set the config once (how to reference/use this repo as a skill), then give the task —
# same turn or next. It reads harness_factory/SKILL.md and derives/emits the harness itself (no install). Or use the CLI:
PYTHONPATH=src python -m harness_factory derive --task "write a literature review with citations"
harness derive --task "write a literature review with citations over several weeks"
harness init   --task "add unit tests to the parser" --out ./my-task   # --out defaults to ./<slug>
harness check  --dir ./my-task
harness gate   --dir ./my-task          # runtime gates: structural + runs the emitted check.py
harness harvest --dir ./my-task         # observe-only: append a signal line to <kb>/updates/signals.jsonl
harness plugins --validate              # third-party domain/template plugins (read-only over the SSOT)
harness skill                            # agent load-index; `harness skill M4` prints a module
harness capabilities                     # requirement -> capability -> modules map
harness catalog --class deep-research    # unified harness catalog: list/search/filter

# frontier-standard ratchet: aim at the best-known bar (every domain has a rubric)
harness standard --domain deep-research bar brief --level R4 --name "SOTA report" --source https://…
harness standard --domain deep-research score brief --set fidelity=2 --set coverage=3
harness standard --domain deep-research audit brief   # weighted gap, largest first
harness standard --domain deep-research raise brief   # ratchet the floor (refuses a regression)
harness standard --domain deep-research plan brief    # gaps -> harness config (modules + tools)

# profile + learn from a real project (observe-only, project -> factory)
harness profile --project ./myproj --goal "…"
harness learn   --task "…" --project ./myproj   # -> updates/cases.jsonl
harness cases

# self-update + intel + self-evolution (all human-gated, all reversible)
harness refresh --provider all --intel   # tracked sources -> proposals + updates/INTEL.md
harness sources                          # every tracked entity (labs, harnesses, venues, people, media)
harness evolve                           # coverage/gap audit -> updates/EVOLUTION.md (proposals)
harness evolve-apply --accept <id|target>
```

**Consumption modes.** L0 — an assistant reads `harness_factory/SKILL.md` + `core/` + `data/*.json` and derives itself
(no install); L1 — run the CLI from the path (`PYTHONPATH=src python -m harness_factory …`);
L2 — an installed package. **L2 (packaging) is cancelled as a distribution channel** — see
[`harness_factory/tasks/DISTRIBUTION.md`](harness_factory/tasks/DISTRIBUTION.md) §8.

**Two roots.** The **tool home** (catalogs, corpus, cycle output) lives in user space
(`%LOCALAPPDATA%\harness-factory`, overridable with `HARNESS_HOME`); each **target project** receives
its generated files via `init --out` (or directly from the agent). In path mode the home is optional.

> 中文速览：最灵活用法是**两步——先贴「配置」（如何引用与使用本工具），再给「任务」**（同一轮接着写，或下一轮再发均可），
> 助手读 `harness_factory/SKILL.md` 自行推导并落盘 harness（免安装）；需要可复现时再用**路径调用 CLI** 的 L1 模式。
> `profile/learn/cases` 让工厂**从项目中学习**；打包（`uv tool install`/PyPI）作为分发渠道**已取消**。

---

## Layout · 结构

```
harness_factory/          the project (start at its README)
├── README.md             定位 · 结构 · 用法
├── SKILL.md              agent-native entry (cardinal rules + load-index + output contract)
├── PROMPTS.md            提示词模板（① 配置 + ② 任务句 + 域任务句，可复制）
├── introduction.md        简介：是什么 · 心智模型 · Quickstart
├── reference/             derivation-rules.md（规则表的 agent 可读镜像）
├── core/                  跨域通用主干模式（M0–M9）
├── domains/               24 个学科门类 + general 兜底（每域一个 README；含 writing 写作域）
├── review/                文献综述 · harness 总览 · 实践者 playbook · 参考文献
├── sources/               提炼溯源表（模式 ← 一手材料）
├── src/harness_factory/   工具源码 + data/（modules·capabilities·domains·harnesses·rubrics·levers·watchlist·sources.json）+ templates/
├── tests/                 标准库 unittest（无外部依赖）
├── tasks/                 PLAN · PROGRESS · REFRESH · DISTRIBUTION
└── _archive/              旧目录归档（docs/ external/ tools/ …，已移出版本控制）
```

See [`harness_factory/README.md`](harness_factory/README.md) for the full documentation.

---

## Documentation map · 文档地图

| What you want | Where |
|---|---|
| Positioning, layout, usage | [`harness_factory/README.md`](harness_factory/README.md) |
| **Use directly from an agent (L0)** | [`harness_factory/SKILL.md`](harness_factory/SKILL.md), `harness_factory/reference/derivation-rules.md` |
| **Copy-paste prompt templates (config + task)** | [`harness_factory/PROMPTS.md`](harness_factory/PROMPTS.md) |
| Mental model + quickstart | [`harness_factory/introduction.md`](harness_factory/introduction.md) |
| Core harness invariants | `harness_factory/core/01-meta-principles.md` |
| Domain playbooks | `harness_factory/domains/*/README.md` |
| Literature & catalog | `harness_factory/review/` |
| Plans & progress | `harness_factory/tasks/PLAN.md`, `harness_factory/tasks/PROGRESS.md` |
| Self-update + evolution | `harness_factory/tasks/REFRESH.md`, `harness_factory/src/harness_factory/evolution.py` |

Licensed under MIT — see [`LICENSE`](LICENSE). 中文入口见 [`README.zh-CN.md`](README.zh-CN.md)。
