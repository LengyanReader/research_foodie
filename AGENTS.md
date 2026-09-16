# AGENTS.md — research_foodie workspace principles

> 工作区原则 · Workspace principles for AI coding assistants and contributors.
> Derived from conventions observed in sibling workspaces (`cookbooks`, `m_flow`) and adapted for this repository.

## 1. 语言政策 / Language policy

- **中英双语为主 / English and Chinese are both primary languages**（覆盖 `cookbooks` 中 "English only" 的默认约定，用户已显式升级为双语）。
- 每个正式文档（`docs/**`）应同时提供：
  - **Master body** — English by default（便于引用与检索）；
  - **中文摘要/关键决策注释** — a Chinese executive summary or key-decision notes, usually as a `> 中文速览` block at the top, or a mirrored `## 中文` section for core design docs.
- 代码、配置、标识符使用英文；文案与说明可双语。
- 中文文件的既有内容保持原样；翻译须忠实，不堆砌术语。

## 2. 仓库地图 / Repository map

```
docs/
  refs/                    外部调研与参考资料 (external research/reference material)
    ai-research-tools-workflow-guide.md
  design/                  架构与设计文档 (architecture/design docs)
    research-foodie-blueprint.md
  PLAN.md                  执行计划 (bilingual)
  PROGRESS.md              进度日志 (bilingual)
AGENTS.md                  本文件
README.md                  项目入口
LICENSE                    MIT License
```

## 3. 质量门 / Quality gates

- **引用即生命线 / Citations are the lifeline.** 任何事实性声明必须可溯源到一手资料（arXiv ID / DOI / 官方仓库 / 官方文档页），并在文档中给出来源与访问日期。无法验证的声明必须标记为 *unverified*，不得冒充事实。
- **日期显式化 / Dates are explicit.** 所有"当前状态"类陈述带 `as of <date>`。
- **价格与榜单数字视为方向性 / Pricing & leaderboard numbers are directional.** 如原文惯例，给范围并标注来源。
- 文档审校：`rg`/grep 检查遗留占位符、未完成段落（`TODO`/`TBD`）、失效链接与不一致的日期。
- 本阶段（Phase 0/1）为纯文档工作，无代码/测试门禁；进入实现阶段后再引入 `ruff`/`mypy`/`pytest`（对齐 `m_flow` 约定）。

## 4. 约定 / Conventions

- **文件/文档命名**：小写、`-` 分隔（`research-foodie-blueprint.md`）。
- **Markdown 规范**：ATX 标题、代码围栏带语言、表格用于结构化对比；每文档顶部给 `Updated: <date>`。
- **提交信息**：Follow [Conventional Commits](https://www.conventionalcommits.org/)，如 `docs(guide): add references section`。
- **不主动提交（No unsolicited commits）**：只有用户显式要求才 `git commit`。
- **不新增无必要的文件**：优先编辑既有文件；新文档须服务于计划、追踪或交付物。
- **避免冗余输出**：生成内容保持精炼、信息密度高。

## 5. 工作链路原则 / Workflow principles (为什么存在 docs/PLAN.md 与 PROGRESS.md)

- **计划先行、进度可查 (/plan-first, track-as-you-go)。** 任何多步骤任务先写入 `docs/PLAN.md`，执行中把结果、修正、来源记入 `docs/PROGRESS.md`。
- **一手资料优先 / Primary sources first。** 校对与规划一律回到官方仓库、论文原文、官方文档，而非二手转述。
- **成本敏感 / Cost-sensitive。** 默认选择开源/免费、本地可跑的工具；付费 API 仅在质量关键步骤使用（用户环境：本地 Win11 CPU + 可远程 GPU 平台）。