# BATTERY · 真实场景模拟使用的例行程序（P51 起常设）

> **中文速览。** 2026-10-28 用户指示：「把设计或模拟真实场景的使用作为例行内容，对 harness 的能力和更新进行测试
> 和评估」。本文件是**常设程序**：何时跑、跑什么、判分怎么定、收据流向哪里。设计总表与历史结果：
> [`review/experiment-battery-2026-10.md`](../review/experiment-battery-2026-10.md)。它已入轮次完成定义
> （`data/cycles.json` DoD 的软轴 **battery**）：触能力/模板/域信号的轮次必须报告重跑了哪些族、收据如何，或说明为何不适用。

**Updated:** 2026-10-28 · **Owner:** 每 P 轮的执行者 · **收据流向:** tool home traces → trace-audit → 提案

## 1. When · 何时跑

| 触发 | 跑什么 |
|---|---|
| 轮次的 added 块触及 **capabilities / templates / 域信号**（M5.10 契约） | 受影响任务族的配对试验（裸奔 vs harness），收据入轨迹 |
| 发射模板或门禁文本变更 | 受影响族的 **B 条件回归**（harness 条件须保持满分——它就是模板的留出集） |
| 每次真实任务收尾 | `harvest --event task_outcome`（含失败；M5.14）→ `collect` → `trace-audit` |
| 周期性（随 refresh/full-update） | `harness scoreboard` + `trace-audit`（已入 full-update 六相环） |

## 2. What · 试验组（七族，锚定前沿评测实践）

见 [`review/experiment-battery-2026-10.md`](../review/experiment-battery-2026-10.md) §1 总表。已测 5/7：
lit-review 0.2 vs 1.0 · model-choice 0.0 vs 1.0 · unit-tests 0.552 vs 1.0 · proof-verification 0.0 vs 1.0 ·
bayesian-stats 0.2 vs 1.0（裸奔 vs harness，scale [0,1]）。待跑：deep-research、kg-dh。

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
