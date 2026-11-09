# TREND · AI 趋势周报例行程序（P77 起常设）

> **中文速览。** 2026-11-07 用户指示：「把 AI 领域的趋势分析好好提升……后续可以按周更新」。本文件是**周更
> 常设程序**：何时跑、跑什么、纪律、产物流向。与 BATTERY.md（试验例行）同构：管线供原材料（M0.4 引擎只聚合），
> 综述由 agent 撰写（引用即生命线）。自动调度：每周一 09:00 本地时间（CronCreate 已建，标题「AI 趋势周报例行更新」）。

**Updated:** 2026-11-07 · **Owner:** 每 周一 的执行者（或任何 agent 会话）· the Monday runner (or any agent session) · bilingual per user directive 2026-11-07· **产物:** `review/trend-review-<date>.md` + `updates/TREND.md` + `data/trend-snapshot.json` + `docs/index.html`

## 1 · When · 何时跑

| 触发 | 跑什么 |
|---|---|
| **每周一 09:00（自动化）** | 完整周更流程（§2），产出当周 trend-review-<date>.md 并提交（不 push） |
| 每次 full-update（P69 契约） | `trend --write` 重聚合 + 快照；深度分析可顺延至当周例行 |
| 重大行业事件（人工触发） | 加急一期，同 §2 流程，窗口取事件前后一周 |

## 2 · What · 周更流程（七步）

1. **拉流（新鲜度）**：`harness intel --root . --since <上周一>` → `updates/intel.jsonl`（RSS；离线时如实声明，用 WebSearch 核验承重信号并标注）。
2. **聚合（原材料）**：`harness trend --root . --write` → 四簇 + **周际 delta**（对上一张 committed 快照）。同窗口才可比——`--since` 取上周一同日，否则在评审中声明窗口混杂。
3. **挑承重信号**：从 TREND.md 四簇 top（判别性打分 + 每源 ≤3 行）挑 5–10 条；**每条承重信号 WebSearch/WebFetch 一手核验**（官方 blog/repo/arXiv 原文），核验不了的标 feed 源或 *unverified*。
4. **撰写 `review/trend-review-<date>.md`**（周更模型，七节）：§1 本周信号表（信号·源·日期·判读·核验级）→ §2 行业全景与相邻领域 → §3 Harness 文献综述（**与 R1–R293 既有锚点对账**，新文献按最新 § 分节续编）→ §4 新兴方向（数据薄要诚实声明）→ §5 分析与预测（**论断表：证据/置信/反转条件**，每个看好方向给最强反例）→ §6 行动项（提案级/核对级/观察级分档，走提案流程不直改 core/data）→ §7 方法与数据附录（管线、升级、混杂声明）+ 溯源表（声明×一手源×访问日期）。
5. **接线**：`pages.py` ARTICLES 增加本期条目 → `harness pages --write`（仪表盘重生成）。
6. **登记**：`data/cycles.json` 注册本轮（added 块记 delta 变化与行动项）；`tasks/PROGRESS.md` 记录。
7. **门禁与提交**：全套件（`PYTHONPATH=src python -m unittest discover -s tests`）+ `cycle audit` → commit（**绝不 push**；Pages 由 pages.yml 部署）。

## 3 · Discipline · 纪律（每周都必须过）

1. **引用即生命线（M0.1/M0.2）**：承重信号逐条一手核验；转述标 *unverified*；日期显式（as of）。
2. **趋势 ≠ 声量**：区分"事件"与"过程"；头部源的高频发帖不构成趋势。
3. **辩证面强制**：每个被看好方向给最强反例/局限（M5.11 证伪检查；无分析=未完成）。
4. **delta 诚实**：窗口不一致必须在 §7 声明混杂；trajectories/domains 数据薄不硬编故事。
5. **提案制（M0.8）**：行动项只以提案回流，人审后才动 `data|core|domains|templates`。
6. **守卫测试跟随**：最新一期评审须含七节结构与溯源表（`P77TrendWeeklyTest` 钉最新一期，glob 取日期最大者——周更不破测试）。

## 4 · History · 期次

| 期 | 文件 | 数据窗口 | 备注 |
|---|---|---|---|
| 首期 | [review/trend-review-2026-11-07.md](../review/trend-review-2026-11-07.md) | 2026-10-24 → 11-07（2 周） | P77：管线三项升级 + delta 首用（窗口混杂已声明） |
| 第 2 期 | [review/trend-review-2026-11-09.md](../review/trend-review-2026-11-09.md) | 2026-11-02 → 11-09（1 周） | P79：首次例行自动化执行；DeepSeek 整合专评（feed 重锚提案 P79.R1）；P78 编号被并行会话占用顺延 |
| （前身） | [review/trend-review-2026-11-03.md](../review/trend-review-2026-11-03.md) | — | P69 全量综述（非周更模型），保留为深版底稿 |

## 5 · English · The weekly procedure in brief

> **What.** Standing weekly routine for the AI trend review (user directive 2026-11-07: "elevate the trend
> analysis and update it weekly"). Same shape as `BATTERY.md`: the deterministic pipeline supplies raw
> material (the engine aggregates and cites, M0.4); the review is authored with a citations-lifeline.
> Automated: **Mondays 09:00 local** (CronCreate, title 「AI 趋势周报例行更新」).

**Seven steps.**

1. **Pull** — `harness intel --root . --since <last Monday>` → `updates/intel.jsonl`. Offline: say so and
   gather signals via WebSearch instead; never fabricate intel (M0.4).
2. **Aggregate** — `harness trend --root . --write` → four clusters + weekly delta vs the previous
   committed snapshot. Keep the window aligned (same `--since` weekday), else disclose the confound in §7.
3. **Select load-bearing signals** — 5–10 from the TREND.md cluster tops (discriminator-scored, ≤3 rows per
   source); **verify each against a primary source** (official blog / repo / arXiv page, with access date);
   mark feed-sourced or *unverified* otherwise.
4. **Author `review/trend-review-<date>.md`** — seven sections, **bilingual (### 中文 / ### English per
   section, per the 2026-11-03 reference)**: weekly signals table → industry landscape → harness literature
   reconciliation against R1–R293 → emerging directions (disclose thin data) → thesis table
   (evidence · confidence · **reversal condition**) → tiered action items (proposal / check / observation —
   proposals only, never a direct edit to core/data) → method appendix + provenance table (claim × primary
   source × access date).
5. **Wire** — add the issue to `pages.py` ARTICLES → `harness pages --write`.
6. **Register** — cycles.json entry (P<number>) + `tasks/PROGRESS.md` + this file's §4 issue table.
7. **Gate & commit** — full suite + `cycle audit` → commit. **Never push** (Pages deploys via pages.yml).

**Discipline red lines.** Citations are the lifeline (M0.1/M0.2) · trend ≠ volume (an event is not a
process) · dialectics mandatory (strongest counter-example per favored direction, M5.11) · honest deltas
(window confounds disclosed; thin clusters stay thin on the page) · proposals only (M0.8) · the structure
guard (`P77TrendWeeklyTest`) globs the LATEST dated review, so the weekly cadence never breaks the suite.
