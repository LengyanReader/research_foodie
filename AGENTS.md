# AGENTS.md — research_foodie workspace principles

> 工作区原则 · Workspace principles for AI coding assistants and contributors.
> Derived from conventions observed in sibling workspaces (`cookbooks`, `m_flow`) and adapted for this repository.

**Updated:** 2026-10-16

## 1. 语言政策 / Language policy

- **中英双语为主 / English and Chinese are both primary languages**（覆盖 `cookbooks` 中 "English only" 的默认约定，用户已显式升级为双语）。
- 每个正式文档（`harness_factory/**.md`）应同时提供：
  - **Master body** — English by default（便于引用与检索）；
  - **中文摘要/关键决策注释** — a Chinese executive summary or key-decision notes, usually as a `> 中文速览` block at the top, or a mirrored `## 中文` section for core design docs.
- 代码、配置、标识符使用英文；文案与说明可双语。
- 中文文件的既有内容保持原样；翻译须忠实，不堆砌术语。

## 2. 仓库地图 / Repository map

```
harness_factory/          项目主体 —— agent harness 模式库 + `harness` CLI（定位/用法见仓库根 README）
  GUIDE.md                项目指南与示例（中英对照）
  SKILL.md                agent 原生入口（硬规则 + 载入索引 + 输出契约）
  CAPABILITIES.md         生成的能力总览（目的 + 各 harness 能力；`harness capabilities --write`）
  introduction.md         简介：是什么 · 心智模型 · Quickstart
  core/                   跨域通用主干模式（M0–M8）
  domains/                学科门类编排（24 学科 + general 兜底；含 writing 写作域）
  review/                 文献综述 · harness 目录与索引（catalog · index · ambition-and-agency）
  sources/                提炼溯源表（模式 ← 一手材料）
  reference/              capability-router（情境→能力→模块→文件）· requirement-refinement（R0–R5 需求精炼与拔高）
                          · capability-flow（双向：下放具体化 ⇄ 回流提炼）· derivation-rules（规则表的 agent 可读镜像）
  src/harness_factory/    工具源码 + data/*.json（SSOT）+ templates/
  tests/                  标准库 unittest（无外部依赖）
  tasks/                  PLAN · PROGRESS · REFRESH · DISTRIBUTION · ASSESSMENT
  updates/                循环产物（提案 · 情报 · 演化 · 案例；不入版本控制）
  _archive/               旧目录归档（docs/ external/ tools/ …，已移出版本控制）
AGENTS.md                  本文件 · 工作区原则
README.md / README.zh-CN.md  项目入口（English / 中文）
CHANGELOG.md              变更日志
LICENSE                   MIT License
```

## 3. 质量门 / Quality gates

- **引用即生命线 / Citations are the lifeline.** 任何事实性声明必须可溯源到一手资料（arXiv ID / DOI / 官方仓库 / 官方文档页），并在文档中给出来源与访问日期。无法验证的声明必须标记为 *unverified*，不得冒充事实。
- **日期显式化 / Dates are explicit.** 所有"当前状态"类陈述带 `as of <date>`。
- **价格与榜单数字视为方向性 / Pricing & leaderboard numbers are directional.** 如原文惯例，给范围并标注来源。
- 文档审校：`rg`/grep 检查遗留占位符、未完成段落（`TODO`/`TBD`）、失效链接与不一致的日期。
- **测试门禁 / Test gate：** `harness_factory/tests` 为纯标准库 unittest（当前 **152** 用例，`python -m unittest discover -s tests`）。改动 `data/*.json`（SSOT）后须 `harness catalog --write` 重生成索引（同时刷新 `CAPABILITIES.md`）并全量跑测试；CI 见 `.github/workflows/ci.yml`。

## 4. 约定 / Conventions

- **文件/文档命名**：小写、`-` 分隔（如 `standard-ladder.md`）。
- **Markdown 规范**：ATX 标题、代码围栏带语言、表格用于结构化对比；每文档顶部给 `Updated: <date>`。
- **提交信息**：Follow [Conventional Commits](https://www.conventionalcommits.org/)，如 `docs(guide): add references section`。
- **不主动提交（No unsolicited commits）**：只有用户显式要求才 `git commit`。**已更新（2026-09-20，用户指示）**：日常文档/代码交付可**自动 commit**，但**绝不自动 push**；push 仅在被显式要求时进行。
- **不新增无必要的文件**：优先编辑既有文件；新文档须服务于计划、追踪或交付物。
- **避免冗余输出**：生成内容保持精炼、信息密度高。

## 5. 工作链路原则 / Workflow principles (为什么存在 tasks/PLAN.md 与 PROGRESS.md)

- **计划先行、进度可查 (/plan-first, track-as-you-go)。** 任何多步骤任务先写入 `harness_factory/tasks/PLAN.md`，执行中把结果、修正、来源记入 `harness_factory/tasks/PROGRESS.md`。
- **一手资料优先 / Primary sources first。** 校对与规划一律回到官方仓库、论文原文、官方文档，而非二手转述。
- **成本敏感 / Cost-sensitive。** 默认选择开源/免费、本地可跑的工具；付费 API 仅在质量关键步骤使用（用户环境：本地 Win11 CPU + 可远程 GPU 平台）。

## 6. 给 agent 的指令词：先配置，再提任务 / Directive for an agent: configure first, then task

**Step 1 · 常驻引用（贴一次，整段对话有效；写进项目规则文件可跨对话与子体）。** 权威版本见 `harness_factory/SKILL.md`
§"PASTE THIS EXACT INSTRUCTION"（含"停止使用"的撤销方式）；一句话版：

> 「**常驻引用（直到我明确撤销）**：把本仓库当 harness 能力参考。先读 `harness_factory/SKILL.md`，按
> `reference/capability-router.md` 路由、只加载命中行点名的文件；需求模糊/偏小时先跑 `reference/requirement-refinement.md`
> （R0–R5，等我确认）。推导 harness 时产出 `AGENTS.md` + `tasks/*` + `.harness/*`（含 `.harness/capabilities.local.md`），
> 最后跑 `check`；本地能力留在任务里，通用模式只以提案回流 `updates/`。**除非我说「停止使用 harness_factory」，一直沿用。**」

**Step 2 · 任务（同一轮接着写，或下一轮再发均可）。** 直接写目标，或直接附上文件/目录/链接，例如：
「为现有 Python 项目补全类型注解与单元测试，保证可验证闭环。」

这样配置一次、任务一句，输入更省事。用它触发 **L0（agent 原生，免安装）** 用法；需要确定性复现时走 **L1**：
`PYTHONPATH=harness_factory/src python -m harness_factory derive --task "…"`。