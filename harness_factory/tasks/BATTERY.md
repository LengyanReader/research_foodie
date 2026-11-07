# BATTERY · 真实场景模拟使用的例行程序（P51 起常设）

> **中文速览。** 2026-10-28 用户指示：「把设计或模拟真实场景的使用作为例行内容，对 harness 的能力和更新进行测试
> 和评估」。本文件是**常设程序**：何时跑、跑什么、判分怎么定、收据流向哪里。设计总表与历史结果：
> [`review/experiment-battery-2026-10.md`](../review/experiment-battery-2026-10.md)。它已入轮次完成定义
> （`data/cycles.json` DoD 的软轴 **battery**）：触能力/模板/域信号的轮次必须报告重跑了哪些族、收据如何，或说明为何不适用。

**Updated:** 2026-11-07 · **Owner:** 每 P 轮的执行者 · **收据流向:** tool home traces → trace-audit → 提案

## 1. When · 何时跑

| 触发 | 跑什么 |
|---|---|
| 轮次的 added 块触及 **capabilities / templates / 域信号**（M5.10 契约） | 受影响任务族的配对试验（裸奔 vs harness），收据入轨迹 |
| 发射模板或门禁文本变更 | 受影响族的 **B 条件回归**（harness 条件须保持满分——它就是模板的留出集） |
| 每次真实任务收尾 | `harvest --event task_outcome`（含失败；M5.14）→ `collect` → `trace-audit` |
| 周期性（随 refresh/full-update） | `harness scoreboard` + `trace-audit`（已入 full-update 七相环，P66 起尾相为 self-model） |

## 2. What · 试验组（15/15 已收口，注册表为 SSOT，锚定前沿评测实践）

见 [`review/experiment-battery-2026-10.md`](../review/experiment-battery-2026-10.md)（历史设计，冻结于 P50；现状以本节与注册表为准）。**注册表（P53）**：实验状态是数据——`data/battery.json`（族 × 判据 × 尺度 × 状态 × 结果 × 试验项目绑定）；`harness battery` 看全局，`harness battery --next` 无 pending 时打印完成状态。当前 **15/15 已测**（裸奔 vs harness，scale [0,1]）：

| family | A-bare | B-harness | round | 判分轴 |
|---|---|---|---|---|
| lit-review | 0.2 | 1.0 | P45 | citation-verifiability（引用解析，abs 页一手核验） |
| model-choice | 0.0 | 1.0 | P48 | decision-audit-pass-rate（M4.17 选型记录） |
| unit-tests | 0.552 | 1.0 | P50 | 隐藏重放套件 29 用例（RHB/LHTB：重放的才算） |
| proof-verification | 0.0 | 1.0 | P50 | miniF2F 编译即接受（M3.19） |
| bayesian-stats | 0.2 | 1.0 | P50 | 判分者独立重推导（M3.11） |
| kg-dh | 0.0 | 1.0 | P53 | answer-evidence-precision（M4.13 证据指针） |
| deep-research | 0.4 | 1.0 | P56 | citation-verifiability（更深主题） |
| reading-extraction | 0.78 | 0.94 | P62 | 收据内 checks_total |
| cron-parsing | 0.727 | 1.0 | P62 | 收据内 defects |
| agent-eval-reliability | 1.0 | 1.0 | P76 | pass^3 隐藏测试（终端状态机判，M3.18） |
| comprehensive | 0.8 | 1.0 | P65-ext | trial_projects 绑定（软匹配） |
| source-criticism | 0.4 | 1.0 | P65-ext | 史源批判能力配对 |
| argument-reconstruction | 0.2 | 1.0 | P65-ext | 论证重构能力配对 |
| kg-construction | 0.4 | 1.0 | P65-ext | KG 抽取四能力同时测 |
| research-question-generation | 0.4 | 1.0 | P65-ext | 研究问题生成（第 11 族起trial_projects 软匹配） |

**English summary · §2.** The registry (`data/battery.json`) is the SSOT: **15/15 families closed**, each
with pre-declared judge criteria (M5.13), a `scale: [lo, hi]` receipt (P47), and a bound trial project
(`battery.reconcile` reconciles both ways). Headline pattern — the harness arm holds 1.0 across families
while bare ranges 0.0–0.8; the one exception is informative: agent-eval-reliability (P76) reached **pass^3 =
1.0 on BOTH arms** because the task instance does not discriminate the conditions — recorded as an
observation (M5.11), never massaged. Open worklist: a discriminative reliability instance
(citation-resolution, where bare hallucinates from memory) and cross-session/cross-model variance.

**P76 可靠性族升级（真方差，取代 P67 确定性检验）：** `agent-eval-reliability` 以预声明 SPEC + 10 条隐藏测试（先于尝试写定，M5.13/M3.19）跑真配对方差：同一任务 × 3 次独立采样 × 双条件。**pass^3 = 1.0 双臂——实例不区分条件**，按观察记录（M5.11），不做修饰；方差为真（6 个 solution 哈希全异，每臂三条实现路径互异）。诚实边界：同会话同模型采样方差（行为学模拟 house 方法，P65 KG 先例）；收据按 `(project, task, harness)` 分组由 `harness passk` 计算。**下一轮 worklist：** 选判分可机判且 bare 有真实失败率的区分性实例（citation-resolution 类：bare 凭记忆易幻觉引用）+ 跨会话/跨模型方差（τ-bench 全设计 [R282/R279/R285/R288]，见 references §AE）。
**P71 具身映射（历史，仍适用）：** 该族的物理域对应物 `uni-robot-agent` [R291] 给出两件可即刻迁移的东西——① **无特权输入**判据＝A-bare 臂的模板（特权变体须单列 B 臂，不得混入当能力）；② **四类失败分类**：视觉理解 · 空间定位 · 几何编码 · 具身推理（作者自陈为相关性非因果）。RoboDojo 以**环境终态**判分，与 OSWorld/Terminal-Bench 同构（见 `reference/evidence-instruments.md` 门禁 6）。
**P67 代谢注记（历史）：** reading-extraction 与 cron-parsing 两族在 P62 已执行并留有双侧收据但当时未入册——P67 追溯登记并给全部族绑定 `trial_projects`（`battery.reconcile` 双向对账，守卫测试常驻）；两族判据未在跑前入册，M5.13 之缺口如实登记。

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
