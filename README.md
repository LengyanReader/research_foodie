# research_foodie → Harness Factory

> **A generalizable library of agent-harness patterns — plus an executable compiler that derives
> the harness any task needs.**
> 跨域提炼的 **agent harness 模式库**，外加一个**把任务编译成所需 harness**的可执行工具。

**Updated:** 2026-10-15 · **Status:** active · **License:** MIT

> 中文速览：本仓库现聚焦 **`harness_factory/`**——一个「agent harness」模式库 + `harness` CLI。
> *Harness* = 让 LLM 智能体在**跨会话、长时程、有限上下文**下把任务做稳的**一整套外部化方法**
> （上下文工程 · 外部记忆 · 验证门禁 · 来源考证 · 自我演化 · 工具/技能 · 变更治理 · 协作协议）。
> 工具只做**分类/选择/生成/观察/排序**，绝不编造任务实质；所有循环产物先作为**提案**，由人确认。详见
> [`harness_factory/README.md`](harness_factory/README.md) 与 [`introduction.md`](harness_factory/introduction.md)。
>
> **给 agent 的用法（两步：先配置，再提任务）· Two steps for an agent.** ① **配置**（贴一次，可复用）：「把本仓库当 skill 使用：读
> `harness_factory/SKILL.md`，按需加载 `core/*.md`、`data/*.json`、`domains/<名>/README.md`；此后我给你的任务，请据此推导并落盘
> 所需 harness（`AGENTS.md` + `tasks/*` + `.harness/*`，写入 `.harness/manifest.json`），最后跑 `check`；只提案、不编造任务内容。」
> ② **任务**（同一轮接着写，或下一轮再发）：直接写目标，或直接附上文件/目录。完整模板见下方
> [「Agent prompt templates」](#agent-prompt-templates--给-agent-的提示词模板) 一节。

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

**Offline by default.** Everything runs offline — `derive`, `init`, `check`, `gate`, `harvest`, `profile`, `learn`,
`cases`, `standard`, `catalog`, `plugins`, and `skill` need no network. Only `refresh` and `intel` (external
RSS/YouTube feeds) and the optional LLM classifier (`HARNESS_LLM_*`) reach the network.

**Two roots.** The **tool home** (catalogs, corpus, cycle output) lives in user space
(`%LOCALAPPDATA%\harness-factory`, overridable with `HARNESS_HOME`); each **target project** receives
its generated files via `init --out` (or directly from the agent). In path mode the home is optional.

> 中文速览：最灵活用法是**两步——先贴「配置」（如何引用与使用本工具），再给「任务」**（同一轮接着写，或下一轮再发均可），
> 助手读 `harness_factory/SKILL.md` 自行推导并落盘 harness（免安装）；需要可复现时再用**路径调用 CLI** 的 L1 模式。
> `profile/learn/cases` 让工厂**从项目中学习**；打包（`uv tool install`/PyPI）作为分发渠道**已取消**。

---

## Agent prompt templates · 给 agent 的提示词模板

Set the tool up in **two steps**: paste the **configuration** once — it never changes, so keep it in a snippet or
the project's rules file — then give the **task** each time, in the same turn or the next (attachments welcome).

**Step 1 · Configuration (paste once, reusable)**

```text
Treat this repository as a skill: read harness_factory/SKILL.md, and load reference/derivation-rules.md,
core/*.md, data/*.json, domains/<name>/README.md as needed. For any task I give you, derive and emit the
required harness (AGENTS.md + tasks/* + .harness/*, recording every choice in .harness/manifest.json), then
run `check`; propose only, never fabricate task substance (M0.4). If I've sent only the configuration with no
task yet, acknowledge and wait — don't derive in advance.
```

**Step 2 · Task (same turn or next)**

Just write the goal, or attach files / directories / links. Example:

```text
Add complete type annotations and unit tests to the existing Python project, with a verifiable closed loop.
```

**Variant task lines** (use after the configuration):

| Situation | Task line |
|---|---|
| Set up a harness for a new project/task | "Derive and emit the required harness for «<goal>»." |
| Want the plan only, no files | "Derive the harness plan for «<goal>» (per module: rule, reason, capability match) — plan only, write no files." |
| Dissect an existing project and learn from it | "Scan <project path> from the `profile` angle; emit `PROFILE.md` and record it as a case (observe-only); observe only — don't change the project." |
| Aim at the highest standard | "Using `domains/excellence/standard-ladder.md`, set an R4-level apex bar for «<goal>», list the weighted gaps and the config to close them." |

**Domain task lines** (optional, after the configuration):

- **writing** — "Build a writing harness with the writing domain: fix the thesis and outline first, force a
  traceable citation for every claim (semantic-scholar / crossref / openalex), run an originality check and
  verification after the first draft, then self-score against the `writing` rubric and ratchet the floor (no regressions)."
- **excellence** — "Process <artifact> with the excellence domain's highest-standard ratchet: name a traceable top
  bar (R4+, with sources), score against the domain rubric → audit the largest gap → improve → ratchet the achieved
  score into a new floor (no regression without a human exemption), and re-check whether the bar has moved."

**Save it · deterministic runs.** Keep Step 1 as an editor snippet or write it into the target project's rules file
(`AGENTS.md`, `.cursor/rules`, `CLAUDE.md`, …) so it is always in force. Prefer a reproducible, machine-verifiable
path? Use the CLI (L1, no install):

```bash
PYTHONPATH=harness_factory/src python -m harness_factory derive --task "<goal>"
PYTHONPATH=harness_factory/src python -m harness_factory init   --task "<goal>" --out <project>
PYTHONPATH=harness_factory/src python -m harness_factory check  --dir <project>
```

---

## Layout · 结构

```
harness_factory/          the project (start at its README)
├── README.md             定位 · 结构 · 用法
├── SKILL.md              agent-native entry (cardinal rules + load-index + output contract)
├── introduction.md        简介：是什么 · 心智模型 · Quickstart
├── reference/             derivation-rules.md（规则表的 agent 可读镜像）
├── core/                  跨域通用主干模式（M0–M8）
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
| **Copy-paste prompt templates** | [Agent prompt templates](#agent-prompt-templates--给-agent-的提示词模板) (in this file) |
| Mental model + quickstart | [`harness_factory/introduction.md`](harness_factory/introduction.md) |
| Core harness invariants | `harness_factory/core/01-meta-principles.md` |
| Domain playbooks | `harness_factory/domains/*/README.md` |
| Literature & catalog | `harness_factory/review/` |
| Plans & progress | `harness_factory/tasks/PLAN.md`, `harness_factory/tasks/PROGRESS.md` |
| Self-update + evolution | `harness_factory/tasks/REFRESH.md`, `harness_factory/src/harness_factory/evolution.py` |

Licensed under MIT — see [`LICENSE`](LICENSE). 中文入口见 [`README.zh-CN.md`](README.zh-CN.md)。
