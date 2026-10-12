# research_foodie → Harness Factory

> **A generalizable library of agent-harness patterns — plus an executable compiler that derives
> the harness any task needs.**
> 跨域提炼的 **agent harness 模式库**，外加一个**把任务编译成所需 harness**的可执行工具。

**Updated:** 2026-10-12 · **Status:** active · **License:** MIT

> 中文速览：本仓库现聚焦 **`harness_factory/`**——一个「agent harness」模式库 + `harness` CLI。
> *Harness* = 让 LLM 智能体在**跨会话、长时程、有限上下文**下把任务做稳的**一整套外部化方法**
> （上下文工程 · 外部记忆 · 验证门禁 · 来源考证 · 自我演化 · 工具/技能 · 变更治理 · 协作协议）。
> 工具只做**分类/选择/生成/观察/排序**，绝不编造任务实质；所有循环产物先作为**提案**，由人确认。详见
> [`harness_factory/README.md`](harness_factory/README.md) 与 [`introduction.md`](harness_factory/introduction.md)。

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

# fastest path: point your vibe-coding assistant at this repo + a task goal.
# It reads SKILL.md and derives/emits the harness itself (no install). Or use the CLI:
PYTHONPATH=src python -m harness_factory derive --task "write a literature review with citations"
harness derive --task "write a literature review with citations over several weeks"
harness init   --task "add unit tests to the parser" --out ./my-task   # --out defaults to ./<slug>
harness check  --dir ./my-task
harness skill                            # agent load-index; `harness skill M4` prints a module
harness capabilities                     # requirement -> capability -> modules map

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

**Consumption modes.** L0 — an assistant reads `SKILL.md` + `core/` + `data/*.json` and derives itself
(no install); L1 — run the CLI from the path (`PYTHONPATH=src python -m harness_factory …`);
L2 — an installed package. **L2 (packaging) is cancelled as a distribution channel** — see
[`harness_factory/tasks/DISTRIBUTION.md`](harness_factory/tasks/DISTRIBUTION.md) §8.

**Two roots.** The **tool home** (catalogs, corpus, cycle output) lives in user space
(`%LOCALAPPDATA%\harness-factory`, overridable with `HARNESS_HOME`); each **target project** receives
its generated files via `init --out` (or directly from the agent). In path mode the home is optional.

> 中文速览：最灵活用法是**把 vibe-coding 助手指向本仓库 + 任务目标**，助手读 `SKILL.md` 自行推导并落盘
> harness（免安装）；需要可复现时再用**路径调用 CLI** 的 L1 模式。`profile/learn/cases` 让工厂**从项目中学习**；
> 打包（`uv tool install`/PyPI）作为分发渠道**已取消**。

---

## Layout · 结构

```
harness_factory/          the project (start at its README)
├── README.md             定位 · 结构 · 用法
├── SKILL.md              agent-native entry (cardinal rules + load-index + output contract)
├── introduction.md        简介：是什么 · 心智模型 · Quickstart
├── reference/             derivation-rules.md（规则表的 agent 可读镜像）
├── core/                  跨域通用主干模式（M0–M9）
├── domains/               科研 / 知识管理 / 数据科学 / DevOps 四域编排
├── review/                文献综述 · harness 总览 · 实践者 playbook · 参考文献
├── sources/               提炼溯源表（模式 ← 一手材料）
├── src/harness_factory/   工具源码 + data/（modules·capabilities·domains·watchlist·sources.json）+ templates/
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
| Mental model + quickstart | [`harness_factory/introduction.md`](harness_factory/introduction.md) |
| Core harness invariants | `harness_factory/core/01-meta-principles.md` |
| Domain playbooks | `harness_factory/domains/*/README.md` |
| Literature & catalog | `harness_factory/review/` |
| Plans & progress | `harness_factory/tasks/PLAN.md`, `harness_factory/tasks/PROGRESS.md` |
| Self-update + evolution | `harness_factory/tasks/REFRESH.md`, `harness_factory/src/harness_factory/evolution.py` |

Licensed under MIT — see [`LICENSE`](LICENSE). 中文入口见 [`README.zh-CN.md`](README.zh-CN.md)。
