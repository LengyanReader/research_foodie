# research_foodie → Harness Factory

> **跨域提炼的 agent harness 模式库，外加一个把任务编译成所需 harness 的可执行工具。**
> A generalizable library of agent-harness patterns, plus an executable compiler.

**更新：** 2026-10-12 · **状态：** 活跃 · **许可：** MIT

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

```bash
cd harness_factory

# 最灵活：把 vibe-coding 助手指向本仓库 + 任务目标，读 SKILL.md 自行推导（免安装）
# 或走确定性路径（同样免安装）：
PYTHONPATH=src python -m harness_factory derive --task "…" --json

# 任意任务 → 生成 harness（规则 M0–M8；可选 LLM 辅助）
harness derive --task "write a literature review with citations over several weeks"
harness init   --task "add unit tests to the parser" --out ./my-task   # --out 默认 ./<slug>
harness check  --dir ./my-task

# 面向 agent 的助手命令 + 项目画像/学习（观察式）
harness skill                            # agent 加载索引；`harness skill M4` 打印某模块
harness capabilities                     # 需求 → 能力 → 模块 映射
harness profile --project ./myproj --goal "…"   # → updates/profile/<slug>.{json,md}
harness learn   --task "…" --project ./myproj   # → updates/cases.jsonl
harness cases

# 自我更新 + 情报提取 + 自演化（全部人工确认、可回退）
harness refresh --provider all --intel   # 跟踪来源 → 提案 + updates/INTEL.md
harness sources                          # 列出全部跟踪对象（机构/harness/刊物/人物/自媒体）
harness evolve                           # 覆盖/缺口审计 → updates/EVOLUTION.md（提案）
harness evolve-apply --accept <id|target>
```

**消费层级。** **L0**——助手读 `SKILL.md` + `core/` + `data/*.json` 自行推导（最灵活、免安装）；
**L1**——不安装，直接路径调用 CLI（`PYTHONPATH=src python -m harness_factory …`，确定性）；
**L2**——安装包，作为**分发渠道已取消**（理由见 `harness_factory/tasks/DISTRIBUTION.md` §8）。

**两个根。** **工具主目录**（目录库、语料、循环产物）位于用户空间
（`%LOCALAPPDATA%\harness-factory`，可用 `HARNESS_HOME` 覆盖）；每个**目标项目**通过 `init --out`
接收生成文件。路径/L0 模式下主目录是可选的。

## 结构

```
harness_factory/          项目主体（先读其 README）
├── README.md             定位 · 结构 · 用法
├── SKILL.md              agent 入口（硬规则 + 加载索引 + 输出契约）
├── introduction.md        简介：是什么 · 心智模型 · Quickstart
├── reference/             derivation-rules.md（规则表的 agent 可读镜像）
├── core/                  跨域通用主干模式（M0–M9）
├── domains/               20 个学科门类（每域一个 README）
├── review/                文献综述 · harness 分类总览与索引（catalog/index）
├── sources/               提炼溯源表（模式 ← 一手材料）
├── src/harness_factory/   工具源码 + data/（modules·capabilities·domains·harnesses·watchlist·sources.json）+ templates/
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
| 心智模型 + 快速上手 | [`harness_factory/introduction.md`](harness_factory/introduction.md) |
| 核心 harness 不变式 | `harness_factory/core/01-meta-principles.md` |
| 各域 playbook | `harness_factory/domains/*/README.md` |
| 文献与总览 | `harness_factory/review/` |
| 计划与进度 | `harness_factory/tasks/PLAN.md`、`harness_factory/tasks/PROGRESS.md` |
| 自我更新 + 演化 | `harness_factory/tasks/REFRESH.md`、`harness_factory/src/harness_factory/evolution.py` |

MIT 许可 —— 见 [`LICENSE`](LICENSE)。English entry: [`README.md`](README.md)。
