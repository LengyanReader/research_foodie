# BATTERY · 真实场景模拟使用的例行程序（P51 起常设）

> **中文速览。** 2026-10-28 用户指示：「把设计或模拟真实场景的使用作为例行内容，对 harness 的能力和更新进行测试
> 和评估」。本文件是**常设程序**：何时跑、跑什么、判分怎么定、收据流向哪里。设计总表与历史结果：
> [`review/experiment-battery-2026-10.md`](../review/experiment-battery-2026-10.md)。它已入轮次完成定义
> （`data/cycles.json` DoD 的软轴 **battery**）：触能力/模板/域信号的轮次必须报告重跑了哪些族、收据如何，或说明为何不适用。

**Updated:** 2026-11-04 · **Owner:** 每 P 轮的执行者 · **收据流向:** tool home traces → trace-audit → 提案

## 1. When · 何时跑

| 触发 | 跑什么 |
|---|---|
| 轮次的 added 块触及 **capabilities / templates / 域信号**（M5.10 契约） | 受影响任务族的配对试验（裸奔 vs harness），收据入轨迹 |
| 发射模板或门禁文本变更 | 受影响族的 **B 条件回归**（harness 条件须保持满分——它就是模板的留出集） |
| 每次真实任务收尾 | `harvest --event task_outcome`（含失败；M5.14）→ `collect` → `trace-audit` |
| 周期性（随 refresh/full-update） | `harness scoreboard` + `trace-audit`（已入 full-update 七相环，P66 起尾相为 self-model） |

## 2. What · 试验组（九族已测 + 一族待跑，锚定前沿评测实践）

见 [`review/experiment-battery-2026-10.md`](../review/experiment-battery-2026-10.md) §1 总表。**注册表（P53）**：实验状态是数据——`data/battery.json`（族 × 判据 × 尺度 × 状态 × 结果 × 试验项目绑定）；`harness battery` 看全局，`harness battery --next` 打印下一个待测族的完整 spec（任何 agent 会话据此**自行**执行并回写收据，完成后 `battery.mark_done` 翻状态）。当前 **9/9 已测**：lit-review 0.2 vs 1.0 · model-choice 0.0 vs 1.0 · unit-tests 0.552 vs 1.0 · proof-verification 0.0 vs 1.0 · bayesian-stats 0.2 vs 1.0 · kg-dh 0.0 vs 1.0 · deep-research 0.4 vs 1.0 · reading-extraction 0.78 vs 0.94 · cron-parsing 0.727 vs 1.0（裸奔 vs harness，scale [0,1]）。

**P70 第十族（待跑 pending，判据已先声明、结果留空＝不臆造）：`agent-eval-reliability`** — 把外部基准的**可靠性口径**落成可跑试验：同一任务同种外壳独立跑 ≥k 次，按**终端/环境状态**（非模型自报）判分，用 `harness passk` 报 **pass@1 与 pass^k**（τ-bench [R282] / ThinkingBox [R279] 标尺；OSWorld [R285] / Terminal-Bench [R289] 状态判分；HAL [R288] 模型×外壳×基准披露 + 污染检查，见 references §AE R282–R290）。样本不足时读作「不可测」（M5.11/M5.12），绝不臆造分数。`battery.reconcile` 跳过 pending 族（计划不声称已有收据）。
**P71 具身映射：** 该族的物理域对应物 `uni-robot-agent` [R291] 给出两件可即刻迁移的东西——① **无特权输入**（不给仿真深度/不成败信号/不写任务专用技能）判据＝本族 A-bare 臂的模板（特权变体须单列 B 臂，不得混入当能力）；② **四类失败分类**：视觉理解 · 空间定位 · 几何编码 · 具身推理（作者自陈为相关性非因果），可作 A-bare 失败归因的外部对照。RoboDojo 以**环境终态**判分，与 OSWorld/Terminal-Bench 同构，判分语义已延伸至物理域（见 `reference/evidence-instruments.md` 门禁 6）。
**P67 代谢注记：** reading-extraction 与 cron-parsing 两族在 P62 已执行并留有双侧收据，但当时未入册——P67 追溯登记，并给全部九族绑定 `trial_projects`（试验项目 ↔ 注册表双向对账 `battery.reconcile`，守卫测试常驻）；两族的判据可见于收据（checks_total/defects）但未在跑前入册，M5.13 之缺口如实登记。历史设计：
lit-review 0.2 vs 1.0 · model-choice 0.0 vs 1.0 · unit-tests 0.552 vs 1.0 · proof-verification 0.0 vs 1.0 ·
bayesian-stats 0.2 vs 1.0（裸奔 vs harness，scale [0,1]）。

## 3. How · 纪律（每一组都必须过）

1. **判据先于执行**（M5.13）：检查单写入试验项目 `tasks/PLAN.md`，判分者可机械执行；
2. **判分者自身要过门**（M3.19）：隐藏重放套件先写好存档（LHTB：重放的才算；条件自带测试不是分数），
   判分者的接口假定要先验证——P50 的判分者自己被抓过一次；
3. **收据带尺度**（P45.R1/P47）：`scale: [lo, hi]` 入 detail；
4. **诚实边界入档**：N=1/条件、同模型同会话（污染声明）、token=proxy、非受控实验——单次只出方向性信号；
5. **发现反哺**：裸奔失败模式按 RHB 分类标注入 M5.14 池；harness 条件失手处=发射物缺口，反哺模板/子句。

## 4. Receipt flow · 收据流

`harvest --event task_outcome --detail '{...scale...}'` → tool home `traces.jsonl` → `trace-audit`
（规则表 `data/trace-rules.json`）→ `updates/traces-proposals.jsonl` + `TRACE-EVOLUTION.md` → 人工裁决。
轨迹只追加；提案制不变（M0.4/M0.8）。
