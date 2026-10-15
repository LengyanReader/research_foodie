# research_foodie → Harness Factory

> **跨域提炼的 agent harness 模式库，外加一个把任务编译成所需 harness 的可执行工具。**
> A generalizable library of agent-harness patterns, plus an executable compiler.

**更新：** 2026-10-14 · **状态：** 活跃 · **许可：** MIT

## 这是什么

**Agent harness** = 让 LLM 智能体在**跨会话、长时程、有限上下文**条件下把任务稳定做对的**一整套
外部化方法**：上下文工程、外部记忆、验证门禁、来源考证、自我演化、工具/技能接口、变更治理、
协作协议。模型是引擎；harness 是车体、仪表盘、安全带与维护手册。

本仓库包含两部分：

1. **模式库** —— 从具体项目中提炼、但**写成与具体项目无关**的 harness 模式（`core/`、`domains/`、
   `review/`、`sources/`）。原项目仅作**出处示例（Exemplar）**标注，不构成定义。
2. **`harness` CLI** —— 分类任务、选取所需模块、生成可运行的 harness 脚手架，并按周期
   **自我更新**自身知识库。

**设计立场。** 编译器只做**分类 / 选择 / 生成**，绝不编造任务实质；每次推导都记录在
`.harness/manifest.json`。`refresh`/`evolve` 循环是**观察式**的：只审计、计数、排序，把**提案**写入
`updates/`，交由人工确认。详见 [`core/01-meta-principles.md`](harness_factory/core/01-meta-principles.md)。

## 快速开始

> **给 vibe-coding 助手的用法（两步：先配置，再提任务）。** ① **配置**（贴一次，可复用）：「把本仓库当 skill 使用：读
> `harness_factory/SKILL.md`，按需加载 `core/*.md`、`data/*.json`、`domains/<名>/README.md`；此后我给你的任务，请据此推导并
> 落盘所需 harness（`AGENTS.md` + `tasks/*` + `.harness/*`，写入 `.harness/manifest.json`），最后跑 `check`；只提案、不编造任务内容。」
> ② **任务**（同一轮接着写，或下一轮再发）：直接写目标，或直接附上文件/目录。完整模板见下方 [「给 agent 的提示词模板」](#给-agent-的提示词模板) 一节。

```bash
cd harness_factory

# 最灵活：两步——先贴「配置」（如何引用与使用本工具），再给任务目标；读 harness_factory/SKILL.md 自行推导（免安装）
# 或走确定性路径（同样免安装）：
PYTHONPATH=src python -m harness_factory derive --task "…" --json

# 任意任务 → 生成 harness（规则 M0–M8；可选 LLM 辅助）
harness derive --task "write a literature review with citations over several weeks"
harness init   --task "add unit tests to the parser" --out ./my-task   # --out 默认 ./<slug>
harness check  --dir ./my-task
harness gate   --dir ./my-task          # 运行时门禁：结构自检 + 执行产出的 check.py
harness harvest --dir ./my-task         # 只读采集：向 <kb>/updates/signals.jsonl 追加一行信号
harness plugins --validate              # 第三方域/模板插件（只读叠加 SSOT）

# 面向 agent 的助手命令 + 项目画像/学习（观察式）
harness skill                            # agent 加载索引；`harness skill M4` 打印某模块
harness capabilities                     # 需求 → 能力 → 模块 映射
harness catalog --class deep-research    # 统一 harness 目录：列出/搜索/筛选
harness profile --project ./myproj --goal "…"   # → updates/profile/<slug>.{json,md}
harness learn   --task "…" --project ./myproj   # → updates/cases.jsonl
harness cases

# 最高标准棘轮：对标最好标杆（每个域都有各自评分表）
harness standard --domain deep-research bar brief --level R4 --name "SOTA report" --source https://…
harness standard --domain deep-research score brief --set fidelity=2 --set coverage=3
harness standard --domain deep-research audit brief   # 加权差距，从大到小
harness standard --domain deep-research raise brief   # 固化新下限（拒绝回退）
harness standard --domain deep-research plan brief    # 差距 → harness 配置（模块 + 工具）

# 自我更新 + 情报提取 + 自演化（全部人工确认、可回退）
harness refresh --provider all --intel   # 跟踪来源 → 提案 + updates/INTEL.md
harness sources                          # 列出全部跟踪对象（机构/harness/刊物/人物/自媒体）
harness evolve                           # 覆盖/缺口审计 → updates/EVOLUTION.md（提案）
harness evolve-apply --accept <id|target>
```

**消费层级。** **L0**——助手读 `harness_factory/SKILL.md` + `core/` + `data/*.json` 自行推导（最灵活、免安装）；
**L1**——不安装，直接路径调用 CLI（`PYTHONPATH=src python -m harness_factory …`，确定性）；
**L2**——安装包，作为**分发渠道已取消**（理由见 `harness_factory/tasks/DISTRIBUTION.md` §8）。

**两个根。** **工具主目录**（目录库、语料、循环产物）位于用户空间
（`%LOCALAPPDATA%\harness-factory`，可用 `HARNESS_HOME` 覆盖）；每个**目标项目**通过 `init --out`
接收生成文件。路径/L0 模式下主目录是可选的。

## 给 agent 的提示词模板

分**两步**用起来：**配置**只贴一次——它固定不变，存成编辑器片段或写进项目规则文件即可；之后每次只给**任务**——
同一轮接着写，或下一轮再发（也可直接附文件 / 目录 / 链接）。

**① 配置（贴一次，可复用）**

```text
把本仓库当 skill 使用：读 harness_factory/SKILL.md，按需加载 reference/derivation-rules.md、core/*.md、
data/*.json、domains/<名>/README.md。此后我给你的任务，请据此推导并落盘所需 harness（AGENTS.md +
tasks/* + .harness/*，每条选择写入 .harness/manifest.json），最后跑 check；只提案、不编造任务内容（M0.4）。
若我这条只发了配置、还没给任务，请确认收到并等待，不要提前推导。
```

**② 任务（同一轮接着写，或下一轮再发）**

直接写目标，或附上文件 / 目录 / 链接。例：

```text
为现有 Python 项目补全类型注解与单元测试，保证可验证闭环。
```

**变体任务句**（接在配置之后）：

| 场景 | 任务句 |
|---|---|
| 新项目 / 新任务搭 harness | 「为『<目标>』推导并落盘所需 harness。」 |
| 只想先看方案、不落盘 | 「先为『<目标>』推导 harness 方案（逐模块给出规则与理由、能力匹配），**只出方案不写文件**。」 |
| 拆解现有项目、学习其能力 | 「用 `profile` 视角扫描 `<项目路径>`，产出 `PROFILE.md` 并作为一个 case 记录（observe-only）；只观察、不改动该项目。」 |
| 按最高标准定目标 | 「按 `domains/excellence/standard-ladder.md`，为『<目标>』定一个 R4 级 apex bar，列出加权 gap 与补齐配置。」 |

**域任务句**（可选，接在配置之后）：

- **writing 域** —— 「用 writing 域为我建写作 harness：先定 thesis 与 outline，每条 claim 强制配**可溯源**证据
  （semantic-scholar / crossref / openalex），初稿后做 originality check 与校验，再按 `writing` rubric 自评并**棘轮固化**（不回退）。」
- **excellence 域** —— 「用 excellence 域的最高标准棘轮处理 <产出物>：先指名一个**可溯源**的最高标杆（R4+，给出来源），
  按本域 rubric 打分 → 审计最大差距 → 逐项提升 → 把达标分固化为**新下限**（未获人工豁免不得回退），并定期复核标杆是否前移。」

**存起来 · 确定性运行。** 把 ① 配置存为编辑器片段，或写进目标项目的规则文件（`AGENTS.md`、`.cursor/rules`、
`CLAUDE.md` 等）使其常驻；想要可复现、机器可验证的路径就用 CLI（L1，免安装）：

```bash
PYTHONPATH=harness_factory/src python -m harness_factory derive --task "<goal>"
PYTHONPATH=harness_factory/src python -m harness_factory init   --task "<goal>" --out <project>
PYTHONPATH=harness_factory/src python -m harness_factory check  --dir <project>
```

## 结构

```
harness_factory/          项目主体（先读其 README）
├── README.md             定位 · 结构 · 用法
├── SKILL.md              agent 入口（硬规则 + 加载索引 + 输出契约）
├── introduction.md        简介：是什么 · 心智模型 · Quickstart
├── reference/             derivation-rules.md（规则表的 agent 可读镜像）
├── core/                  跨域通用主干模式（M0–M9）
├── domains/               24 个学科门类 + general 兜底（每域一个 README；含 writing 写作域）
├── review/                文献综述 · harness 分类总览与索引（catalog/index）
├── sources/               提炼溯源表（模式 ← 一手材料）
├── src/harness_factory/   工具源码 + data/（modules·capabilities·domains·harnesses·rubrics·levers·watchlist·sources.json）+ templates/
├── tests/                 标准库 unittest（无外部依赖）
├── tasks/                 PLAN · PROGRESS · REFRESH · DISTRIBUTION
└── _archive/              旧目录归档（docs/ external/ tools/ …，已移出版本控制）
```

完整文档见 [`harness_factory/README.md`](harness_factory/README.md)。

## 文档地图

| 想要什么 | 去哪里 |
|---|---|
| 定位、结构、用法 | [`harness_factory/README.md`](harness_factory/README.md) |
| **agent 直接使用（L0）** | [`harness_factory/SKILL.md`](harness_factory/SKILL.md)、`harness_factory/reference/derivation-rules.md` |
| **可复制的提示词模板（配置 + 任务句）** | [本文件「给 agent 的提示词模板」](#给-agent-的提示词模板) |
| 心智模型 + 快速上手 | [`harness_factory/introduction.md`](harness_factory/introduction.md) |
| 核心 harness 不变式 | `harness_factory/core/01-meta-principles.md` |
| 各域 playbook | `harness_factory/domains/*/README.md` |
| 文献与总览 | `harness_factory/review/` |
| 计划与进度 | `harness_factory/tasks/PLAN.md`、`harness_factory/tasks/PROGRESS.md` |
| 自我更新 + 演化 | `harness_factory/tasks/REFRESH.md`、`harness_factory/src/harness_factory/evolution.py` |

MIT 许可 —— 见 [`LICENSE`](LICENSE)。English entry: [`README.md`](README.md)。
