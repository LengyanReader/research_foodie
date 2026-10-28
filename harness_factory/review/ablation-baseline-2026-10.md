# Structural ablation baseline · 结构性消融基线（P40 · D1 阶段 C 第一片）

> **中文速览。** M5.12（component-ablation）在本库的**第一次真实运行**：38 个能力逐一隔离剪除、重跑记分集。
> 结果：**10 个承重单元**（消融即掉分——恰为 5 任务 must 集并集，同时验证了记分集对承重单元的检测灵敏性）、
> **28 个在本地面非承重**（含义是**留出集覆盖面**窄于能力集，不是「不重要」）；全部掉分仅在 capabilities 轴——
> 模块选择由规则引擎驱动、能力只注释（M0.4 的架构在数据上自证）。**诚实边界**：确定性分数无方差，M5.12 的配对
> 检验在本地面不可做；performance+token 轴的效果级消融需真实模型运行——那是阶段 C 的剩余部分。

**Updated:** 2026-10-28 · **Round:** P40 (D1 stage C, slice 1) · **Judge:** machine (预声明 5 项判据) · **Effect score:** 1.0 (5/5)

## 1. Procedure · 程序（预声明于工作前）

- **消融单元 = 能力**（数据驱动的中间层）：每次从 `data/capabilities.json` 剪除一个单元，在**全新子进程**中重跑
  `scoreboard.run_all()`（注册表缓存按进程隔离），try/finally 恢复原文件；结束时 `git diff` 验证干净。
- 38/38 单元消融完毕（脚本动态枚举）；原始逐消融结果（机器可读 JSON）在
  `updates/dogfood/p40-ablation-baseline/ablation-results.json`（未入版本控制），本报告承载蒸馏表。
- 对照 M5.12 的口径：单单元反事实 ✓；「每任务中位数」在确定性分数上退化为分数本身 ✓（记为退化，不是假装做了统计）；
  **配对检验：本地面无方差可测——不可做，如实声明**（A4）。

## 2. Findings · 发现

### 2.1 Protected set · 承重集（10 个，消融即掉分）

| unit | 掉分（任务.轴:基线→消融后） |
|---|---|
| verification-gate | unit-tests.capabilities 1→0.5 |
| eval-driven-development | unit-tests 1→0.5；model-choice 1→0.5 |
| traceable-sources | lit-review 1→0.75；deep-research 1→0.667 |
| evidence-bounded-generation | lit-review 1→0.75；kg-dh 1→0.75；deep-research 1→0.667 |
| prose-polish | lit-review 1→0.75；deep-research 1→0.667 |
| loop-discipline | lit-review 1→0.75 |
| ontology-as-contract | kg-dh 1→0.75 |
| entity-resolution | kg-dh 1→0.75 |
| schema-evolution | kg-dh 1→0.75 |
| model-portfolio-discipline | model-choice 1→0.5 |

承重集恰为 5 任务 must_capabilities 的并集——这不是巧合而是**双向验证**：记分集声称钉住这些单元，消融证明
它真的检测得到它们的缺席（若检测不到，留出集就是摆设）。**凡消融掉分者即受保护**：任何对这 10 个能力的剪除
或触发改动，都必须是一次记录理由的有意基线编辑（M0.5），不得静默。

### 2.2 Holdout coverage gap · 留出集覆盖面（28 个非承重）

其余 28 个能力在本地面上消融无差——**其中不乏结构性重要的**（context-budget-policy · untrusted-content-discipline
· sandboxed-execution · resumable-memory · cost-budget-caps…）。正确读法：**不是这些能力不重要，而是当前 must 集
没有钉住它们**。留出集的敏感面窄于能力集——这是本次基线暴露的真实缺口，登记为阶段 C 的后续切片候选
（扩 must 集 = 有意的基线编辑；或接受并声明覆盖面边界）。

### 2.3 Architecture confirmation · 架构自证

全部 38 次消融的掉分**只出现在 capabilities 轴**（modules/structure/emission 三轴从不掉分）。这正是 M0.4 的设计
承诺：「能力只匹配与注释，绝不启用规则引擎未启用的模块」——数据上自证。副作用：能力层的回归只能被 capabilities
轴看见，模块层回归要靠 must_modules（当前 5 任务钉 M2/M3/M4/M5）。

## 3. Honest boundary · 诚实边界（A4）

- 本地面是**确定性**的（同输入同分数）：M5.12 要求的两单侧配对检验、α=0.05 保护集、留出梯的统计部分**在此无方差
  可检验**——本报告不假装做了统计。
- **performance + token 两轴的效果级消融需真实模型运行**（同任务裸跑 vs 带单元 vs 剪单元，M2.13 固定模型与档位）
  ——这是 D1 阶段 C 的剩余部分，需要用户环境的真实运行批次；本片只完成**结构性基线**（哪些单元承重、地面是否
  灵敏、保护集是什么）。
- 单次运行、N=1：一切结论是方向性与结构性的，不是统计结论（M0.1/M0.2 纪律）。

## 4. Provenance · 溯源

- 判据预声明：`updates/dogfood/p40-ablation-baseline/tasks/PLAN.md`（工作前写入）；验收 5 项全过（machine, 5/5）
- 脚本与原始结果：`updates/dogfood/p40-ablation-baseline/{run_ablation.py, ablation-results.json}`（未入版本控制）
- 方法依据：M5.12（`core/06`）· P23 记分集（`review/scored-task-set-2026-10.md` §3）· P16.8 的手动剪除先例
- 轨迹：tool home `updates/traces.jsonl` 第 2 行（`task_outcome`, judge=machine, score=1.0）
