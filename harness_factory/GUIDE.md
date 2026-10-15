# harness-factory · Project Guide & Cookbook
# harness-factory · 项目介绍与使用指南

> **Give any task the agent harness it needs — and keep the know-how current.**
> **为任意任务生成它所需的 agent harness —— 并让这套 know-how 持续自我更新。**

**Updated:** 2026-10-14 · **Status:** working tool (P2) · **Version:** 0.1.0 · **License:** MIT
**Reader:** anyone who wants an LLM agent to do real work reliably (research, coding, data, ops, writing).
**读者：** 希望让 LLM 智能体**可靠地**完成真实工作（科研 / 编码 / 数据 / 运维 / 写作）的人。

---

## 中文速览

**一句话。** `harness-factory` 把「**任务**」编译成该任务所需的 **agent harness**（上下文工程 · 外部记忆 · 验证门禁 · 来源考证 · 工具/技能 · 变更治理 · 协作协议），并用一个**人类把关的自我更新循环**让这套知识库不被冻结。

**一句话指令词（贴给任意 vibe-coding 助手）。**「把本仓库当 skill，读 `harness_factory/SKILL.md`，为我的任务『<目标>』推导并落盘所需 harness（`AGENTS.md` + `tasks/*` + `.harness/*`，每条选择写入 `.harness/manifest.json`），最后跑 `check`；只提案、不编造任务内容。」

**怎么用（三种）。**
1. **L0 面向 agent（免安装）**：把 vibe-coding 助手指向本仓库 + 一句任务目标，它读 `harness_factory/SKILL.md` 自行推导并落盘 harness。
2. **L1 命令行（免安装）**：`PYTHONPATH=src python -m harness_factory derive --task "…"`。
3. **L2 安装成包**：**已取消**（见 `tasks/DISTRIBUTION.md` §8）。

**核心公式。** `任务 → 8 轴特征向量 → 选模块 M0–M8 → 生成脚手架`，每步的理由写入 `.harness/manifest.json`，可解释、可复核。

**它不做什么（M0.4）。** 只做**分类 / 选择 / 生成 / 观察 / 排序**；绝不编造任务实质内容；破坏性动作（推送 / 发布 / 删除 / 花钱）必须人工确认。

**本文件。** 完整介绍 + 命令速查 + **9 个可运行的实例**（含「网球出界判定」全流程、「读物阅读近乎无损」、「深度调研至 Anthropic 水准」、「对标最高标准棘轮」与「新 harness 反哺回本仓库」的闭环）。

---

## 1. What is harness-factory · 它是什么

**EN.** A capable model is not a reliable worker. Between *the model* and *a task done right* there is always a **harness**: the context you feed it, the memory you externalize, the tools you expose, the gates that decide "done", the provenance that keeps it honest, and the loop that makes the harness itself improve. `harness-factory` is a **library of portable harness patterns** (`core/`, `domains/`, `review/`) plus a **compiler** (`src/harness_factory/`) that turns a task into a concrete harness, and a **human-gated self-update loop** that keeps the knowledge current.

**中文。** 一个能力强的模型并不等于可靠的工人。**模型**与**把事情做对**之间永远隔着一层 **harness**：你喂给它的上下文、你外部化的记忆、你暴露的工具、判定「完成」的门禁、让它诚实的溯源，以及让它自己变好的循环。`harness-factory` = 一个**跨域提炼的 harness 模式库**（`core/` `domains/` `review/`）+ 一个把**任务编译成 harness** 的**编译器**（`src/harness_factory/`）+ 一个**人类把关的自我更新循环**。

**Two halves, one repo · 两半，一个仓库**

| Half · 部分 | Lives in · 位置 | Role · 作用 |
|---|---|---|
| **Pattern library** · 模式库 | `core/` `domains/` `review/` `sources/` | Domain-neutral harness patterns + domain compositions + sourced survey. · 跨域通用模式 + 域内编排 + 有出处的综述。 |
| **Compiler & loop** · 编译器与循环 | `src/harness_factory/` | Classify → derive → assemble → check + self-update. · 分类→推导→生成→校验 + 自我更新。 |

The bridge between them is machine-readable: `data/{modules,capabilities,domains,harnesses}.json` (M0.5 single source of truth). · 两者之间由**机器可读**的 `data/*.json` 桥接（单一事实来源）。

---

## 2. Core concepts · 核心概念

### 2.1 A harness is a composition, not a template · harness 是「组合」而非「模板」

**EN.** A harness is *not* a fixed template. It is a **composition of modules selected by the task's features**. That is what makes the factory "inclusive": to cover a new kind of task, you add a **feature value** or a **domain**, not a new branch everywhere.

**中文。** harness **不是**固定模板，而是**由任务特征选出的模块组合**。这正是它能「包容」的原因：要覆盖一类新任务，只需加一个**特征取值**或一个**领域**，而不是到处加分支。

```
        task (text or flags)
              │
              ▼
    classify  ──► FeatureVector        (8 axes, rules-first; optional LLM fills gaps)
              │     horizon · verifiability · stakes · grounding
              │     artifact · tool_surface · collaboration · domain
              ▼
    derive    ──► HarnessPlan          (M0–M8 enabled? with what params? + reasons)
              │
              ▼
    assemble  ──► files on disk        (AGENTS.md · tasks/* · .harness/*)
              │
              ▼
    check     ──► gate                (manifest validates; no placeholders)
```

### 2.2 The 8 feature axes · 8 个特征轴

These describe *the kind of work*, not the topic. · 描述**工作的性质**，而非话题。

| axis · 轴 | choices · 取值 | meaning · 含义 |
|---|---|---|
| `horizon` | `one_shot` · `session` · `multi_session` · `long_running` | how far the work spans · 工作跨度 |
| `verifiability` | `high` · `medium` · `low` | can we mechanically check "done"? · 能否机械校验 |
| `stakes` | `low` · `medium` · `high` | cost of being wrong · 出错代价 |
| `grounding` | `off` · `preferred` · `required` | must claims be sourced? · 是否强制溯源 |
| `artifact` | `code` · `document` · `dataset` · `knowledge_base` · `plan` · `mixed` | what is produced · 产出物 |
| `tool_surface` | `none` · `read` · `read_write` · `external` | how much the agent touches the world · 触达世界的程度 |
| `collaboration` | `solo` · `human_review` · `multi_agent` | who else is involved · 协作形态 |
| `domain` | 24 disciplines (below) · 24 个学科 | weak prior for defaults · 默认值的弱先验 |

### 2.3 Modules M0–M8 · 核心模块

| id | module · 模块 | enabled when · 启用条件 |
|---|---|---|
| **M0** | Meta-principles · 元原则 | always · 始终 |
| **M1** | Context engineering · 上下文工程 | always · 始终 |
| **M2** | Long-running / memory · 长时程/记忆 | `horizon ≥ session` |
| **M3** | Verification & gates · 验证与门禁 | always · 始终 |
| **M4** | Provenance & integrity · 来源与完整性 | `grounding ≥ preferred` or cited artifact · 或产出物需引用 |
| **M5** | Self-evolution · 自演化 | `horizon ≥ multi_session` |
| **M6** | Tools & skills · 工具与技能 | `tool_surface ≠ none` |
| **M7** | Change governance · 变更治理 | always · 始终 |
| **M8** | Collaboration & sessions · 协作与会话 | `collaboration ≠ solo` or `stakes = high` |

### 2.4 Capability map · 能力映射

Requirements match **capabilities**, which *annotate* the enabled modules and are recorded in the manifest. New requirements are added by editing JSON, not code. · 需求匹配**能力**，能力**标注**已启用模块并写入 manifest。新增需求改 JSON 即可，无需改代码。

| capability · 能力 | modules | when (data-driven) · 触发 |
|---|---|---|
| `baseline-discipline` | M0,M1,M7 | always · 始终 |
| `verification-gate` | M3 | always · 始终 |
| `resumable-memory` | M2 | `min_horizon=session` |
| `traceable-sources` | M4 | grounding/artifact |
| `self-improving-loop` | M5 | `min_horizon=multi_session` |
| `tool-use` | M6 | tool_surface |
| `human-review-gate` | M8 | collaboration/stakes |
| `high-stakes-guardrails` | M3,M8 | `stakes=high` |
| `reproducible-experiments` | M3,M4,M5 | domain ∈ {data-science, research} ∧ verifiability=high |
| `long-horizon-autonomy-control` | M2,M3,M8 | multi_session ∧ high stakes |

### 2.5 Domains · 学科门类

Data-driven taxonomy of **24 disciplines + `general` fallback**, grouped by faculty (each non-general domain has a `domains/<id>/README.md`). · **24 个学科 + `general` 兜底**，按 faculty 分组（每个非 general 域都有 `domains/<id>/README.md`）。

> `domains/writing/README.md` is **registered** in `domains.json`/`rubrics.json` (faculty `humanities`), so `--domain writing` is selectable in the CLI. · `writing` 已注册进 SSOT（faculty `humanities`），CLI 可选 `--domain writing`。

`deep-research` · `research` · `reading` · `writing` · `excellence` · `knowledge-management` · `data-science` · `devops` · `software-engineering` · `engineering` · `physics` · `chemistry` · `biology` · `earth-environment` · `mathematics` · `medicine` · `economics-finance` · `psychology` · `social-science` · `law` · `humanities` · `education` · `arts-design` · `model-selection` · `general`

### 2.6 Consumption modes · 消费形态

| mode · 形态 | how · 方式 | install? |
|---|---|---|
| **L0** agent-native | point an assistant at this repo + a task goal; it reads `harness_factory/SKILL.md` + `core/` + `data/*.json` and derives itself · 把助手指向本仓库，它自读自推 | no · 免 |
| **L1** CLI-from-path | `PYTHONPATH=<repo>/src python -m harness_factory …` | no · 免 |
| **L2** installed package | **cancelled** as a channel · **已取消** | — |

---

## 3. Install & run · 安装与运行

**Prerequisites · 前置条件:** Python 3.10+ (stdlib only; no third-party deps) for L1. For L0, none. · L1 只需 Python 3.10+（纯标准库）；L0 无需任何环境。

```bash
# --- L1: from the repo path (no install) · 从仓库路径调用（免安装）---
cd harness_factory
export PYTHONPATH=src            # Windows PowerShell: $env:PYTHONPATH="src"
python -m harness_factory --version     # harness-factory 0.1.0
python -m harness_factory --help

# Optional: a convenient alias · 可选：加个别名
alias harness='python -m harness_factory'   # then: harness derive --task "…"
```

Run the tests (stdlib `unittest`, no deps) · 跑测试：

```bash
cd harness_factory
PYTHONPATH=src python -m unittest discover -s tests     # 128 tests OK
```

---

## 4. Quickstart · 快速上手（5 分钟）

```bash
# 1) See the harness a task needs (explainable: which rule fired, and why)
PYTHONPATH=src python -m harness_factory derive \
    --task "write a literature review with citations over several weeks"

# 2) Get machine-readable output
PYTHONPATH=src python -m harness_factory derive \
    --task "add unit tests to the parser" --json

# 3) Emit the harness into ANY directory (default ./<task-slug>)
PYTHONPATH=src python -m harness_factory init \
    --task "add unit tests to the parser" --out C:\work\parser-task

# 4) Gate: verify the emitted harness (manifest + no placeholders)
PYTHONPATH=src python -m harness_factory check --dir C:\work\parser-task

# 5) Explain it later
PYTHONPATH=src python -m harness_factory explain --dir C:\work\parser-task
```

Real output of step 3 · 第 3 步的真实输出：

```text
harness written to C:\work\parser-task (9 files)
  + .harness/PROVENANCE.md
  + .harness/check.py
  + .harness/gates.md
  + .harness/ledger.md
  + .harness/manifest.json
  + .harness/skills/README.md
  + AGENTS.md
  + tasks/PLAN.md
  + tasks/PROGRESS.md
self-check: OK
```

---

## 5. Command reference · 命令速查

| command · 命令 | EN | 中文 |
|---|---|---|
| `derive --task …` | Show the derived plan (no writes). | 显示推导出的方案（不写文件）。 |
| `init --task … [--out D]` | Write the harness scaffold to `D`. | 把 harness 脚手架写入目录。 |
| `explain --dir D` | Explain a generated manifest. | 解读已生成的 manifest。 |
| `check --dir D` | Run the harness self-check (gate). | 运行自检门禁。 |
| `gate --dir D` | Run the runtime gates (structural + executes the emitted `check.py`). | 运行运行时门禁（结构 + 执行产出的 `check.py`）。 |
| `harvest --dir D [--root KB]` | Harvest observed signals → `<kb>/updates/signals.jsonl` (observe-only). | 采集观测信号（只读，只追加）。 |
| `plugins [--validate]` | List/validate third-party domain & template plugins. | 列出/校验第三方域与模板插件。 |
| `skill [name]` | Print the agent load-index, or one module. | 打印 agent 载入索引或单个模块。 |
| `capabilities` | Show the capability map. | 显示能力映射表。 |
| `profile --project P` | Scan a project (observe-only) → `PROFILE.md`. | 扫描项目（只读）→ 画像。 |
| `learn --task … --project P` | Record a case → `updates/cases.jsonl`. | 记录一个案例。 |
| `cases` | Aggregate learned cases. | 聚合案例。 |
| `catalog [id] [--class …]` | Unified harness catalog: list/search/filter. | 统一 harness 目录：列出/搜索/筛选。 |
| `standard … [--domain D]` | Frontier-standard ratchet: bar/score/audit/raise/frontier on the domain rubric. | 最高标准棘轮：定标杆/评分/审计/提升/前沿。 |
| `sources [--group G]` | List tracked sources. | 列出已追踪信源。 |
| `intel [--since D]` | Pull tracked feeds → `updates/INTEL.md`. | 抓取信源 → 情报简报。 |
| `evolve [--dry-run]` | Audit coverage/gaps + stale apex bars → proposals. | 审计覆盖/缺口与过期的最高标准 → 提案。 |
| `evolve-apply --accept …` | Human gate → `updates/accepted.json`. | 人工采纳提案。 |
| `refresh [--provider all --intel]` | Pull new/leading sources (proposal only). | 抓取新前沿信源（只出提案）。 |
| `refresh-apply --accept …` | Human gate → proposal stubs. | 人工采纳候选。 |
| `doctor` | Show resolved paths / config / LLM status. | 显示路径/配置/LLM 状态。 |
| `self-update` | Refresh the tool's own catalog from defaults. | 从内置默认刷新自身目录。 |

Flags common to `derive`/`init` · 公共参数：`--domain --goal --project --horizon --verifiability --stakes --grounding --artifact --tool-surface --collaboration --llm --json` (`init` adds `--out --force`).

**Exit codes · 退出码:** `init`/`check` return non-zero when the self-check gate fails, so they compose in CI. · 门禁失败返回非零，便于接入 CI。

---

## 6. Worked examples · 实例

### Example 1 — A coding task · 编码任务

**Goal · 目标:** add unit tests to the parser. · 给解析器加单元测试。

```bash
PYTHONPATH=src python -m harness_factory derive --task "add unit tests to the parser"
```

Real output (abridged) · 真实输出（节选）：

```text
Task   : add unit tests to the parser
Domain : general

  [+] M0 Meta-principles
  [+] M1 Context engineering
  [+] M2 Long-running agents      {"memory_depth": "session"}
  [+] M3 Verification & gates     {"gate_strictness": "standard"}
  [+] M4 Provenance & integrity   {"provenance": "preferred"}
  [-] M5 Self-evolution           (horizon=session < multi_session)
  [+] M6 Tools & skills
  [+] M7 Change governance
  [-] M8 Collaboration & sessions (collaboration=solo, stakes=medium)
```

**Read it · 解读.** The task was inferred as `verifiability=high` (tests are mechanically checkable), `horizon=session`, `stakes=medium`. So M3 is on with a `standard` gate, M5 is off (single session), M4 is on (`grounding=preferred`). Every line shows the **reason** it fired. · 任务被推断为可高可验证、单会话、中风险，因此启用验证门禁、关闭自演化，且每行都给出**触发理由**。

---

### Example 2 — A multi-week research task · 多周科研任务

**Goal · 目标:** a literature review with citations over weeks. · 带引用的文献综述，跨数周。

```bash
PYTHONPATH=src python -m harness_factory derive \
    --task "write a literature review with citations over several weeks" \
    --domain research --horizon multi_session --grounding required
```

**What changes · 变化.** `--horizon multi_session` turns **M5 (self-evolution)** on; `--grounding required` makes **M4 (provenance)** strict; the capability map adds `reproducible-experiments` and `traceable-sources`. The emitted `.harness/PROVENANCE.md` and `.harness/gates.md` now demand a **claim ledger** (claim → source → access date → status) and a **definition of done written before work**. · 多会话打开 M5，强制溯源打开 M4，并附加「可复现实验」「来源可溯」两项能力；产出的溯源台账与门禁要求「先定义完成、每条主张可溯源」。

---

### Example 3 — End-to-end: Tennis out-of-bounds on a phone · 端到端：手机端网球出界判定

**Requirement · 需求.** From a relatively clear tennis video, decide whether the ball is out of bounds. **Hard constraint:** must run acceptably on an iPhone 14 and equivalent Android (on-device, near real-time). We need full requirement analysis, solution, implementation path, and evaluations — with every method's **premises, applicability, fit, and feasibility** assessed. New harnesses discovered along the way should feed back into the factory. · 从相对清晰的网球视频判断球是否出界；**硬约束**：iPhone 14 及同级安卓能跑得动（端侧、近实时）。需要全方位需求分析/方案/实现路径/评估，并对方法的前提/适用条件/匹配度/可行性做充分评估；产出的新 harness 反哺本仓库。

**Step 1 — Profile the project (observe-only) · 画像（只读）**

```bash
PYTHONPATH=src python -m harness_factory profile --project ./tennis-obb --goal "on-device out-of-bounds"
# -> <home>/updates/profile/tennis-obb.{json,md}
```

**Step 2 — Derive with the hard constraints as flags · 把硬约束写成特征**

```bash
PYTHONPATH=src python -m harness_factory derive \
  --task "on-device tennis ball out-of-bounds from video; Feasibility/premises/applicability/fit assessment; iPhone14-class real-time" \
  --horizon multi_session --verifiability high --stakes medium \
  --grounding required --artifact mixed --tool-surface read_write --collaboration human_review
```

Resulting modules · 得到的模块（全部 M0–M8 启用）:

```text
M0 M1 M2 M3 M4 M5 M6 M7 M8   enabled
capabilities: baseline-discipline, verification-gate, resumable-memory,
              traceable-sources, self-improving-loop, tool-use,
              human-review-gate, reproducible-experiments
```

**Step 3 — Emit & gate · 生成与门禁**

```bash
PYTHONPATH=src python -m harness_factory init \
  --task "on-device tennis out-of-bounds (iPhone14-class real-time)" \
  --horizon multi_session --verifiability high --grounding required \
  --artifact mixed --tool-surface read_write --collaboration human_review \
  --out ./tennis-obb
PYTHONPATH=src python -m harness_factory check --dir ./tennis-obb   # self-check: OK
```

**How the harness forces a rigorous evaluation · harness 如何强制「充分评估」.** The emitted `.harness/gates.md` + `PROVENANCE.md` make these **non-optional**, each criterion **default-FAIL** and passable only with **observed evidence**:

| assessment · 评估维度 | forced artifact · 强制产出 | module |
|---|---|---|
| **Premises · 前提** | Assumptions table (assumption → how verified → `verified`/`unverified`), access dates. · 假设表（假设→验证方式→状态）。 | M4 |
| **Applicability · 适用条件** | Applicability matrix: method × condition × met? × evidence (lighting, occlusion, camera angle, frame rate, court-line visibility). · 适用性矩阵。 | M3 |
| **Fit · 匹配程度** | Task-fit comparison on **task subsets**, not overall metrics. · 任务子集上的适配度对比。 | M4 + `model-selection` |
| **Feasibility · 可行性** | Feasibility matrix + **hard gates**: FPS ≥ target, P95 latency, peak RAM, model size, quantization, on-device export path (ONNX / CoreML / ExecuTorch). Each has a **failure condition** and **evidence**. · 可行性矩阵 + 硬门禁（FPS/延时/内存/体积/量化/导出路径），每项都有失败条件与证据。 | M3 + M7 |

Discovery & evidence come from the catalog (Step 4): `paperswithcode`, `elicit`, `consensus`, `connected-papers`, `researchrabbit` (class `discovery`); `lm-eval-harness`, `helm`, `simple-evals`, `lighteval` (class `evaluation`). · 发现与证据来自目录里的 discovery / evaluation 类条目。

**Step 4 — Find the tools · 找工具**

```bash
PYTHONPATH=src python -m harness_factory catalog --class discovery
PYTHONPATH=src python -m harness_factory catalog --class evaluation
PYTHONPATH=src python -m harness_factory catalog --module M3      # everything that verifies
PYTHONPATH=src python -m harness_factory catalog lm-eval-harness  # one entry in detail
```

**Step 5 — Feed back into the factory · 反哺回本仓库**

```bash
# (a) record the project as a case (observe-only, append-only)
PYTHONPATH=src python -m harness_factory learn \
  --task "on-device tennis out-of-bounds" --project ./tennis-obb

# (b) the evolution audit turns recurring/bespoke needs into human-gated proposals
PYTHONPATH=src python -m harness_factory evolve --dry-run
PYTHONPATH=src python -m harness_factory evolve          # writes proposals only
PYTHONPATH=src python -m harness_factory evolve-apply --accept <id|target>
```

If the project repeatedly needs a capability not in `data/capabilities.json` (e.g. `on-device-quantization`), the audit emits a **`missing_capability`** proposal — never auto-applied. If it produced a reusable harness (e.g. `mobile-vision-eval`), you add it to `data/harnesses.json` and regenerate the index (Step 6). · 若某能力反复缺失 → `missing_capability` 提案；若产出可复用 harness → 写入 `data/harnesses.json` 并重生成索引。

**Step 6 — Register the new harness · 注册新 harness**

```bash
# edit src/harness_factory/data/harnesses.json (add the entry), then:
PYTHONPATH=src python -m harness_factory catalog --write    # regenerate review/harness-index.md
PYTHONPATH=src python -m unittest discover -s tests         # drift guard + all tests
```

> **Boundary · 边界.** The factory will **propose** (`updates/*.jsonl`), but you **decide** which entries land in the SSOT (`data/*.json`). It never silently rewrites the catalog (M0.4/M0.8). · 工厂**只提案**，**由你决定**是否写入 SSOT；它绝不静默改写目录。

---

### Example 4 — Agent-native (L0) workflow · 面向 agent 的用法

**EN.** Instead of driving the CLI yourself, **point a coding assistant at this repository and give it a task goal.** The assistant reads [`SKILL.md`](SKILL.md) (cardinal rules + load-index + output contract), loads only the modules it needs, derives with `reference/derivation-rules.md` + `data/*.json`, emits the output contract, fills `PROVENANCE.md` honestly, and can `profile`/`learn` the project so the factory keeps improving.

**中文。** 你也可以不自己敲命令：**把编码助手指向本仓库 + 一句任务目标**。助手读 [`SKILL.md`](SKILL.md)（核心规则 + 载入索引 + 输出契约），按需只载入需要的模块，用 `reference/derivation-rules.md` + `data/*.json` 推导，落盘输出契约，如实填写 `PROVENANCE.md`，并可 `profile`/`learn` 让工厂持续变好。

```text
User  →  "Set up the agent harness for this repo; goal: on-device tennis out-of-bounds."
Agent →  reads harness_factory/SKILL.md, runs (or reasons through) derive,
         emits AGENTS.md + tasks/* + .harness/*, fills PROVENANCE.md,
         runs .harness/check.py, then records a case via `learn`.
```

The assistant-loadable index is live · 可实时打印索引：

```bash
PYTHONPATH=src python -m harness_factory skill          # the whole load-index
PYTHONPATH=src python -m harness_factory skill M4       # just the provenance module
```

---

### Example 5 — Discovery & model selection · 发现与选型

**EN.** For "which method/model fits my task", use the `model-selection` domain (L0 requirements → L1 discovery → L2 evidence → L3 fit-for-task eval → L4 gate → L5 record). The catalog is the discovery surface.

**中文。** 面对「哪种方法/模型适配我的任务」，用 `model-selection` 域（需求→发现→证据→任务适配评估→门禁→记录）。目录即发现面。

```bash
# browse by intent · 按意图浏览
PYTHONPATH=src python -m harness_factory catalog --class discovery
PYTHONPATH=src python -m harness_factory catalog --kind eval-framework
PYTHONPATH=src python -m harness_factory catalog --search evidence
PYTHONPATH=src python -m harness_factory catalog --tracked          # only sources.json-tracked
PYTHONPATH=src python -m harness_factory catalog consensus          # detail for one entry
```

Real detail output · 单条详情：

```text
claude-code — Claude Code · Claude Code
  class : coding / kind: terminal-agent
  vendor: Anthropic    ecosystem: anthropic
  maps  : M1, M6, M7
  en    : Terminal agent with a skills/subagent model and permission gates.
  zh    : 带技能/子 agent 模型与权限门禁的终端 agent。
  url   : https://docs.anthropic.com/en/docs/claude-code
  tracked: sources.json::anthropic-claude-code
  tags  : terminal, skills, permissions
```

`--module M3` answers "what can verify my work?"; `--vendor`/`--tag` narrow by provider/theme; `--markdown`/`--write` emit the generated index (`review/harness-index.md`). · `--module M3` 回答「什么能验证我的工作」；`--vendor/--tag` 收窄；`--write` 重生成索引。

---

### Example 6 — Self-update & evolution · 自我更新与演化

**EN.** The knowledge base must not freeze. The loop is **signal → audit → propose → human-gate**, and it is *observe-only*: it never edits the catalogs.

**中文。** 知识库不能冻结。循环是 **信号→审计→提案→人工把关**，且**只读**：绝不改目录。

```bash
# tracked sources: labs, vendor harnesses, venues, people, self-media
PYTHONPATH=src python -m harness_factory sources --group projects

# pull tracked feeds -> bilingual intel brief
PYTHONPATH=src python -m harness_factory intel --since 2026-01-01

# structural audit: coverage / empty groups / stale sources / untracked / missing capability
PYTHONPATH=src python -m harness_factory evolve --dry-run
# real output:
#   entities=64  coverage=100%  intel=0
#   audits=0  proposals=0
PYTHONPATH=src python -m harness_factory evolve             # writes updates/EVOLUTION.md + evolution.jsonl
PYTHONPATH=src python -m harness_factory evolve-apply --accept <id|target>   # -> updates/accepted.json
```

**Checkpoint · 自检:** `doctor` shows resolved paths, config, catalog files, and LLM status. · `doctor` 显示路径/配置/目录文件/LLM 状态。

---

### Example 7 — Reading a book, losslessly · 读物阅读：近乎无损

**EN.** Reading is its own domain (`reading`). The goal: **classify the material → acquire the original → extract every dimension by type → keep it near-lossless → escalate to a human when the original cannot be obtained.**

**中文。** 阅读是一个独立领域（`reading`）：**判定类型 → 获取原文 → 按类型穷尽提炼 → 近乎无损 → 拿不到原文则通知人工。**

```bash
# 1) Derive a reading harness (genre drives which dimensions apply)
PYTHONPATH=src python -m harness_factory derive \
  --task "read this book chapter by chapter; extract key points, highlights, author intent, argument, quotes losslessly" \
  --domain reading --horizon multi_session --verifiability high --grounding required

# 2) Find acquisition + parsing + annotation + distillation tools
PYTHONPATH=src python -m harness_factory catalog --class reading
PYTHONPATH=src python -m harness_factory catalog project-gutenberg   # one entry in detail

# 3) Tracked book libraries (public-domain / borrowable / open-access)
PYTHONPATH=src python -m harness_factory sources --group libraries
```

**What the reading pipeline guarantees · 阅读流水线保证:**

| layer · 层 | guarantee · 保证 | module |
|---|---|---|
| L0 Identify · 判型 | genre + language + edition + confidence; ambiguous → confirm with human | M0,M7 |
| L1 Acquire · 获取 | original + source + access date + license; **unobtainable → notify human** | M6,M4 |
| L2 Normalize · 归一 | chapter-structured text + content hash (pins the version) | M6,M2 |
| L3 Extract · 提炼 | the genre's dimension set (`extraction-dimensions.md`) | M1,M4 |
| L4 Distill · 蒸馏 | **anchored verbatim quotes**; quote ≠ inference; coverage ledger | M1,M3 |
| L5 Verify · 校验 | every claim resolves to an anchor; gaps/ambiguity flagged (three-state) | M3,M4 |
| L6 Record · 记录 | provenance ledger; fail-loud on unobtainable/ambiguous items | M4,M7,M8 |

**Dimensions · 维度 (exhaustive).** Bibliographic · structural · key points · highlights · **author intent** · rhetoric · argument map · evidence · themes/characters/timeline · terminology · **anchored quotes** · assumptions · contradictions · unresolved questions · actionables · fidelity report — full checklist in [`domains/reading/extraction-dimensions.md`](domains/reading/extraction-dimensions.md). · 书目/结构/要点/重点/**作者意图**/修辞/论证/证据/主题人物时间线/术语/**带锚引文**/前提/矛盾/未解问题/可执行项/保真报告。

> **Boundary · 边界.** With no obtainable original, the harness **stops and asks a human** — it never fabricates the source text (M0.1/M0.2/M4). · 拿不到原文时**停止并询问人工**，绝不编造原文。

---

### Example 8 — Deep research to an Anthropic-grade bar · 深度调研

**EN.** Give the factory a topic and it derives a **plan → parallel search → screen → extract → synthesize → verify → iterate** loop, then reports with coverage + confidence. The method is in [`domains/deep-research/method.md`](domains/deep-research/method.md); the tools are the `deep-research` catalog class.

**中文。** 给工厂一个课题，它推导出 **规划→并行检索→筛选→抽取→综合→校验→迭代** 闭环，并给出带覆盖率与置信度的报告。方法见 `domains/deep-research/method.md`，工具见 `deep-research` 目录类。

```bash
# 1) Derive a deep-research harness (multi-hop, high verifiability, required grounding)
PYTHONPATH=src python -m harness_factory derive \
  --task "do deep research on <topic>: decompose, multi-source search, cite everything, keep contradictions, state gaps" \
  --domain deep-research --horizon multi_session --verifiability high --grounding required

# 2) Tools: agents + web/academic search + retrieval + crawl + screening + eval
PYTHONPATH=src python -m harness_factory catalog --class deep-research
PYTHONPATH=src python -m harness_factory catalog --kind academic-search
PYTHONPATH=src python -m harness_factory catalog --kind research-eval

# 3) Tracked tools/agents
PYTHONPATH=src python -m harness_factory sources --group tools
```

**What "Anthropic-grade" requires · 判据:**

| criterion · 判据 | guarantee · 保证 | module |
|---|---|---|
| Scope fidelity · 切题 | restate + confirm the actual question before searching | M0,M7 |
| Breadth · 广度 | orchestrator + **parallel subagents**; ≥2 independent source types on contested points | M1,M6 |
| Citation integrity · 引文 | every claim → checkable source; quotes verbatim; `unverified` fenced | M0.2,M4 |
| Contradiction honesty · 矛盾 | disagreements shown, not averaged | M0.1,M3 |
| Coverage & calibration · 覆盖/校准 | per-sub-question coverage; confidence stated and matched | M4,M5 |
| Separation of duties · 分权 | searcher ≠ synthesizer ≠ verifier ≠ evaluator | M3 |
| Iteration · 迭代 | gap detection → new queries → stop criteria | M2,M5 |
| Self-eval · 自评 | rubric scores the brief; ≤1 on any criterion → don't ship | M3,M7 |

> **Boundary · 边界.** No source → no claim; absent/contested evidence is reported, never fabricated (M0.1/M0.2/M4). · 无源不下断言；缺失/争议如实呈现，绝不编造。

---

### Example 9 — Aim at the highest standard (the ratchet) · 对标最高标准（棘轮）

**EN.** `excellence` turns "make it world-class" into a measurable, monotone loop: **name the best-known bar → baseline → gap audit → raise → ratchet (never regress) → track the moving frontier**. The mechanism is in [`domains/excellence/standard-ladder.md`](domains/excellence/standard-ladder.md); the `frontier-standard` capability fires it (M3+M5+M8).

**中文。** `excellence` 把「做到世界一流」变成可测量、只升不降的闭环：**定标杆→对标→差距审计→提升→棘轮（不回退）→跟踪移动前沿**。机制见 `domains/excellence/standard-ladder.md`；`frontier-standard` 能力触发它（M3+M5+M8）。

```bash
# Derive a frontier-standard harness: high verifiability + multi-session => capability fires
PYTHONPATH=src python -m harness_factory derive \
  --task "raise this research brief to the best-known standard; measure gaps and ratchet" \
  --domain excellence --verifiability high --horizon multi_session --grounding required --stakes high

# Inspect the capabilities map (requirement -> capability -> modules)
PYTHONPATH=src python -m harness_factory capabilities
PYTHONPATH=src python -m harness_factory catalog --kind research-eval   # where to read the bar

# Run the ratchet: name a sourced bar, score on the domain rubric, audit, raise (never regress)
PYTHONPATH=src python -m harness_factory standard --domain deep-research bar brief \
  --level R4 --name "SOTA deep-research report" --source https://openai.com/index/introducing-deep-research/
PYTHONPATH=src python -m harness_factory standard --domain deep-research score brief \
  --set fidelity=2 --set coverage=3 --set contradiction-honesty=2 --set calibration=1
PYTHONPATH=src python -m harness_factory standard --domain deep-research audit brief  # gaps, largest first
PYTHONPATH=src python -m harness_factory standard --domain deep-research raise brief  # ratchet the floor
# gaps -> harness configuration (which modules to enable, which catalog tools to wire)
PYTHONPATH=src python -m harness_factory standard --domain deep-research plan brief
```

**Applied to this project · 反身应用.** The factory holds *itself* to the same bar: `harness standard --domain software-engineering plan harness-factory` scores the repo against Anthropic's documented engineering practice and emits the config to close its own gaps — see [`domains/excellence/self-standard.md`](domains/excellence/self-standard.md). · 项目把同一标杆用在自己身上：`plan harness-factory` 对照 Anthropic 公开工程实践打分并给出配置，见 `self-standard.md`。

**Lever map · 差距映射.** `data/levers.json` maps each rubric dimension to the modules (M0–M8) and catalog tool-kinds that close it — anchored to Claude/Anthropic's documented practice where one exists (e.g. `fidelity` → a citation agent; `coverage` → 3–5 parallel subagents). `standard plan` grounds the tool suggestions in `data/harnesses.json`.

**Per-domain rubrics · 分域评分表.** Every domain carries its own weighted rubric in `data/rubrics.json` (unknown domains fall back to `default`), so the same ratchet works for code, math, law, medicine, the arts, etc. · 每个域在 `data/rubrics.json` 有各自加权评分表（未知域回退 `default`），同一棘轮适用于代码、数学、法律、医学、艺术等。

**The ratchet in one line · 棘轮一行:** `floor_next = max(floor,achieved)` — the floor is a promise: no future submission may score below it without a human-approved exception. · 下限是承诺：未获人工豁免，后续产出不得低于它。

**The bar ladder · 标杆阶梯:** R1 floor (correct) → R2 peer → R3 strong → R4 leader (SOTA) → R5 frontier (best exemplar) → R6 moving (as SOTA advances).

> **Boundary · 边界.** A bar with no measurable, sourced reference is `unverified`; excellence is **never self-declared** (M0.4/M0.8). · 无据可测的标杆标为 `unverified`；优秀**绝不自我宣称**。

---

### Example 10 — Run the emitted harness; extend with plugins · 运行产出的 harness；用插件扩展

**EN.** Two P3/P4 additions close the loop around an **emitted** harness. **Runtime hooks** turn the artifact into a runnable object: `harness gate` runs the structural self-check *and* executes the emitted `.harness/check.py` (hard gates decide the exit code; M2/M4/M6/M8 content gates are advisory reminders of what evidence is still owed — M0.3). `harness harvest` reads observable signals (domain, modules, gate outcomes, progress/ledger counts) plus any `.harness/signals.jsonl` the agent appended, and writes ONE observation line to `<kb>/updates/signals.jsonl` — **observe-only**, feeding the M5 evolution loop. **Plugins** extend the catalog without touching the SSOT: a `domain` plugin merges into the registry + rubrics (so `--domain <plugin-id>` becomes selectable) and may emit extra templates; a `template` plugin registers a reusable emitted file.

**中文。** P3/P4 两项给**产出的** harness 补上闭环。**运行时钩子**把产物变成可运行对象：`harness gate` 既跑结构自检，又**执行**产出的 `.harness/check.py`（硬门决定退出码；M2/M4/M6/M8 内容门作为「还欠什么证据」的提示——M0.3）。`harness harvest` 采集可观测信号（域、模块、门禁结果、进度/账本行数）以及 agent 追加的 `.harness/signals.jsonl`，向 `<kb>/updates/signals.jsonl` 追加**一行**观测——**只读**，喂给 M5 演化闭环。**插件**在不改 SSOT 的前提下扩展目录：`domain` 插件并入注册表与评分表（`--domain <插件id>` 可选）并可额外产出模板；`template` 插件注册可复用的产出文件。

```bash
# Run the runtime gates over an emitted harness (exit 0 = mechanically sound)
PYTHONPATH=src python -m harness_factory gate --dir ./my-task
# Harvest observed signals (observe-only; writes only under <kb>/updates/)
PYTHONPATH=src python -m harness_factory harvest --dir ./my-task --root ~/.harness
# List/validate third-party plugins (HARNESS_PLUGINS_DIR, else <data>/plugins)
PYTHONPATH=src python -m harness_factory plugins --validate
```

A minimal `domain` plugin (`plugins/<id>/plugin.json`):

```json
{
  "id": "my-domain", "kind": "domain", "version": "0.1.0",
  "title_en": "My Domain", "summary": "One line.", "faculty": "general",
  "artifact": "document", "grounding": "preferred",
  "signals": ["my trigger phrase"],
  "extra_templates": ["my-appendix"],
  "rubric": {"dimensions": [
    {"dim": "clarity", "weight": 0.6}, {"dim": "rigor", "weight": 0.4}
  ]}
}
```

Validation is strict: the `id` must match the directory, vocabularies (`artifact`/`grounding`) are closed, rubric weights must sum to ~1, a `template` needs its `<name>.tmpl`, and a plugin may **not** shadow a built-in domain (it is reported and ignored). · 校验是严格的：`id` 必须等于目录名，`artifact`/`grounding` 取闭集，评分权重需合计约 1，模板需有 `.tmpl`，且插件**不得**遮蔽内置域（会被报告并忽略）。

---

## 7. What it produces · 生成物

```text
<out>/
  AGENTS.md               operating manual for the task (bilingual) · 任务操作手册（双语）
  tasks/PLAN.md           plan-first scaffold · 计划优先脚手架
  tasks/PROGRESS.md       append-only progress log + handoff · 追加式进度与交接
  .harness/manifest.json  the decision record: features, capabilities, modules, reasons, files
  .harness/gates.md       definition of done (hard/soft gates) · 完成定义
  .harness/PROVENANCE.md  derivation record (which rule/capability fired; mark unverified) · 溯源记录
  .harness/check.py       standalone self-check (stdlib only) · 独立自检
  .harness/ledger.md      (if M2) append-only state · 追加式状态
  .harness/skills/README.md (if M6) progressive skill index · 技能渐进索引
  .harness/decisions.md   (if M8) decision log · 决策日志
  .harness/PROFILE.md     (if --project) read-only scan of the target project · 目标项目只读画像
```

Every emitted file is plain Markdown/Python — no lock-in, no runtime dependency. · 全部为纯 Markdown/Python，无锁定、无运行时依赖。

---

## 8. Self-evolution & mutual learning · 自演化与相互学习

| concept · 概念 | mechanism · 机制 | writes? |
|---|---|---|
| **Snapshot · 快照** | `profile` (project) + `evolution.snapshot()` (coverage/metrics) | observe-only |
| **Audit · 审计** | `uncovered_topic` · `empty_group` · `stale_source` · `untracked_source` · `missing_capability` | observe-only |
| **Propose · 提案** | `add_source` `populate_group` `retire_or_refresh` `track_source` `add_capability` | `updates/*.jsonl` only |
| **Human gate · 人工把关** | `evolve-apply` → `updates/accepted.json` (reversible) | accepted.json only |
| **Mutual learning · 相互学习** | `profile` → `learn` (case) → `evolution` audit → proposal | append-only cases |

**EN.** Projects teach the factory: `profile` describes a target project (observe-only), `learn` records a case, and `evolution` turns a capability that keeps recurring but is absent from the registry into a **human-gated** proposal. The factory never edits its own SSOT — it proposes; you decide.

**中文。** 项目反哺工厂：`profile` 描述目标项目（只读），`learn` 记录案例，`evolution` 把「反复出现但注册表里没有的能力」变成**受人类把关**的提案。工厂从不自改 SSOT —— 它提案，你决定。

**Deliberately NOT automated · 刻意不自动化.** Consolidation / dedup / taxonomy merge / capability pruning are high-semantic-risk. They stay in the human loop (they would risk breaking the non-overlapping signal constraint and domain READMEs). This is a *safety* choice, not a gap. · 整合/去重/学科合并/能力精简风险高，留在人类环节（避免破坏信号非重叠约束与域 README）。这是**安全**选择，不是缺陷。

---

## 9. Design principles · 设计原则（M0）

Priority chain (higher wins on conflict) · 优先级链（冲突时高者胜）：

> **Truth ≻ Trace ≻ Verify ≻ Observe-only ≻ SSOT ≻ Human-gate ≻ Context ≻ Resumable ≻ Reversible ≻ Evolvable**

- **Truth before throughput** · 真实先于吞吐：never invent content to look finished.
- **Provenance or `unverified`** · 有据可溯或不标注为事实：every load-bearing claim traceable, or explicitly flagged with an access date.
- **Verify before "done"** · 验证先于完成：`done` is an observed state with evidence, not a feeling.
- **Machines observe, humans decide** · 机器观察、人类定夺：automation may classify/record/rank, never fabricate or silently mutate.
- **Human gate + reversible** · 人工把关 + 可逆：irreversible acts (delete/push/publish/spend/contact) need authorization.

---

## 10. Troubleshooting / FAQ · 排障与常见问题

| symptom · 现象 | cause & fix · 原因与处理 |
|---|---|
| `No module named harness_factory` | `PYTHONPATH` not set. Run `$env:PYTHONPATH="src"` (Windows) / `export PYTHONPATH=src` (bash) from `harness_factory/`, or use L0. · 未设 PYTHONPATH。 |
| `check` fails / non-zero exit | Manifest invalid or placeholder text remains. Open `.harness/manifest.json`; re-run `init --force`. · manifest 无效或残留占位符。 |
| Domain always `general` | Task text lacks domain signals. Pass explicit `--domain`. · 任务文本缺域信号，显式指定 `--domain`。 |
| Stale catalog when using home | Home shadowing. Bundled is authoritative by default; only set `HARNESS_USE_HOME_CATALOG=1` if you intentionally seeded a home catalog. Run `doctor`. · 库内为权威；home 需显式启用。 |
| `evolve` proposes nothing | That is healthy: 100% coverage, no gaps. It only proposes on a real gap. · 覆盖率满、无缺口，属正常。 |
| Want to change defaults | Edit `data/*.json` (SSOT), then `catalog --write` + run tests. · 改 `data/*.json` 后重生成索引并跑测试。 |

**Environment variables · 环境变量:** `HARNESS_HOME` (tool home) · `HARNESS_DATA_DIR` (data precedence) · `HARNESS_USE_HOME_CATALOG=1` (opt into home catalog) · `HARNESS_LLM_*` (optional LLM assist).

---

## 11. Status & roadmap · 状态与路线

- **P0 done** — pattern library. · 模式库。
- **P1 done** — CLI compiler (`derive`/`init`/`explain`/`check`), rules engine, stdlib tests. · CLI 编译器。
- **P1.5–P1.7 done** — self-update loop, cross-project home KB, intel tracking + self-evolution. · 自我更新/跨项目/情报/演化。
- **P1.8 done** — agent-native mode (`harness_factory/SKILL.md`, `harness skill`), project learning (`profile`/`learn`/`cases`), capability mechanism; packaging cancelled. · 面向 agent + 项目学习 + 能力机制。
- **P2 (in progress)** — **24 disciplines** + faculty taxonomy; unified **harness catalog** (`data/harnesses.json`, 127 entries) + `catalog` CLI + generated `review/harness-index.md` (drift-guarded); **discovery/evaluation coverage** (`model-selection` domain, eval frameworks, discovery tools, registries/leaderboards/indices); **reading/acquisition coverage** (`reading` domain + 20 acquisition/parser/annotation/distillation tools + `libraries` sources); **deep-research coverage** (`deep-research` domain + `method.md` playbook + 43 research-agent/search/academic/retrieval/crawl/screening/eval tools + `tools` sources); **frontier-standard capability** (`excellence` domain + `standard-ladder.md` ratchet + `frontier-standard` capability) now **executable**: `standard.py` + `harness standard bar|score|audit|raise|plan|frontier`, per-domain rubrics (`data/rubrics.json`), gap→lever map (`data/levers.json`), and the `stale_frontier` audit; and **`writing` domain** registered in the SSOT (`data/domains.json` + `data/rubrics.json`), so `--domain writing` is selectable. Remaining: LLM discovery/classification hardening; feed/entity expansion. · 学科扩展 + 目录统一 + 发现/评估 + 阅读/获取 + 深度调研 + 最高标准能力（可执行棘轮）+ 写作域（已注册）。
- **P3 done** — **runtime hooks**. `runtime.py`: a **gate runner** (`harness gate`) that runs the structural check + executes the emitted `.harness/check.py` (hard gates decide pass/fail; M2/M4/M6/M8 gates are advisory), and **signal harvest** (`harness harvest`, observe-only) that appends one observation to `<kb>/updates/signals.jsonl`. · 运行时钩子：门禁执行 + 信号采集。
- **P4 done** — **plugin protocol**. `plugins.py`: read-only discovery of third-party `domain`/`template` plugins (`HARNESS_PLUGINS_DIR`), merged into the registry + rubrics (never mutating the SSOT), strict validation, CLI `harness plugins`. · 第三方域/模板插件协议。

---

## 12. See also · 延伸阅读

- [`README.md`](README.md) — positioning · structure · layout. · 定位与结构。
- [`introduction.md`](introduction.md) — problem · mental model · design rationale. · 问题与心智模型。
- [`SKILL.md`](SKILL.md) — agent-native entry (cardinal rules + output contract). · agent 入口。
- `core/00-index.md` → `core/01-meta-principles.md` → M1–M8 — the ten invariants and modules. · 十条不变式与模块。
- `domains/<id>/README.md` — per-discipline workflows. · 各学科工作流。
- `review/harness-index.md` — unified harness lookup (generated). · 统一 harness 索引（自动生成）。
- `tasks/{PLAN.md,PROGRESS.md,REFRESH.md,DISTRIBUTION.md}` — roadmap, log, loop, packaging. · 路线/日志/循环/打包。

> **Generalization rule · 泛化铁律.** A pattern earns a place here only if it survives removal of its originating project. · 一条模式只有「去掉其来源项目后仍成立」才有资格留在这里。
