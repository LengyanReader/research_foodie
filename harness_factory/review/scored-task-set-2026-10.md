# Scored task set · 本库自己的打分任务集（P23 · effect 轴 P24）

> **中文速览。** 关闭 P16.9 的重访触发（「本库有打分任务集」），给 `component-ablation`（M5.12）一个能跑
> 的留出集，也给 D1 阶段 C（带测量的晋升）补上它的前置依赖。**5 个任务 × 5 条确定性结构轴**（路由 · 能力覆盖 ·
> 模块覆盖 · 结构自检 · 干净发射），全部**1.0 基线**由 `tests/test_scoreboard.py` 钉死——分数变动必须是
> `data/scoreboard.json` 的一次**有意编辑**，绝不静默漂移。所有 allowed/must 值来自 2026-10-23 的一次实测
> `classify+derive`，不是凭记忆写的（M0.4）。**P24 增补第 6 轴 · effect（任务效果）**：每任务声明自己的
> `effect_metric`（该任务族的机器可判分指标），但**真实测量落地前一律 `unmeasured`，不编数**；测得值须带
> 完整收据（score + judge + measured_on）且**永不进结构总分**——结构与效果是两种主张，分开报告、分开钉死。
> **非目标**：结构分不替代 `harness standard` 的逐域 rubric；effect 轴在测量前不提供任何质量结论。

**Updated:** 2026-10-28 · **Round:** P23 (+P24 effect axis, +P44 coverage widening: 7 tasks, 17/38 units pinned) · **Closes:** P16.9 (done_in P23) · **Unblocks:** M5.12 ablation, D1 stage C

## 1. The set · 任务集

| id | task | allowed domains | must capabilities | must modules | effect metric (P24) |
|---|---|---|---|---|---|
| lit-review | Write a literature review with citations over several weeks | research, deep-research | traceable-sources · evidence-bounded-generation · prose-polish · loop-discipline | M2 M4 M5 | citation-verifiability（引用可核验率） |
| unit-tests | Add unit tests to the parser | general, software-engineering | verification-gate · eval-driven-development | M3 | test-suite-pass-rate（交付测试套件确定性通过且覆盖目标模块） |
| kg-dh | 构建方志人物知识图谱，做检索增强问答，注明来源 | digital-humanities | ontology-as-contract · entity-resolution · evidence-bounded-generation · schema-evolution | M2 M4 | answer-evidence-precision（答句证据指针可解析率，M4.13） |
| deep-research | Deep research report on agent memory systems with citations | deep-research | traceable-sources · evidence-bounded-generation · prose-polish | M2 M4 | citation-verifiability（同 lit-review） |
| model-choice | 在 GPT 和 Claude 之间选一个模型来跑评测 | model-selection | model-portfolio-discipline · eval-driven-development | M2 M4 | decision-audit-pass-rate（选型记录含 id/版本/档位 M4.17 + 留出集结果） |
| proof-verification | Formally verify that this distributed protocol satisfies its safety property, using a proof assistant | mathematics, logic, geometry-topology | formal-verification · verification-gate · traceable-sources · evidence-bounded-generation | M3 M4 | machine-checked acceptance（证明助手无 admit/sorry 接受且陈述匹配，天然 machine-judge） |
| bayesian-stats | Fit a bayesian hierarchical model to this dataset and report the credible interval with convergence diagnostics | statistics, data-science | statistical-inference · verification-gate · traceable-sources · evidence-bounded-generation | M3 M4 | inference validity（R-hat/ESS 收敛诊断 + 独立重推导复现区间，天然 machine-judge） |

## 2. The scoring function · 打分函数（5 条结构轴，全确定性 + 1 条 effect 轴）

结构轴（进 `total`，基线 1.0）：

1. **routing** — 分类落域 ∈ allowed 集合（0/1）。
2. **capabilities** — must 能力 ⊆ 实际命中能力（覆盖率 0..1）。
3. **modules** — must 模块 ⊆ 实际启用模块（覆盖率 0..1）。
4. **structure** — 发射的脚手架过 `check_harness`（文件齐、manifest 合法、无占位符，0/1）。
5. **emission** — 发射文件中无未渲染的 `{{…}}`（0/1）。

effect 轴（P24，**不进 `total`**）：

6. **effect** — 任务效果。每任务的 `effect_metric` 定义了「真实运行会测什么」；测量前恒为
   `unmeasured`（0 也好 1 也好都是编造，M0.4）。一次真实测量落地为该任务的
   `effect: {status: "measured", score, judge: human|machine, measured_on}`，`validate_scoreboard`
   拒绝任何缺 judge / 缺 score / 缺日期的收据。与 trace 的 `task_outcome` 事件同构：**机器记判决，
   不做判决**（`judge=machine` 只在该任务族有已定义度量器时合法；机器判决者同样受 M3.18 约束——偏差面声明、未强制面审计、难度/模型变化重审）。

`total = mean(5 structural axes)`。离线、无 LLM、无网络（M0.4：只测量，不发明）。运行：
`harness scoreboard [--task <id>] [--json]`。

## 3. How ablation consumes it · 消融怎么用它

M5.12 的对照口径是**同一任务上全部消融的中位数**——本集就是那批任务：对一个发射物做单单元剪枝后
（按实现边界改 `data/scoreboard.json` 的 must 集、或剪掉一个模块的发射产物），重跑 `scoreboard`，
对比 `total` 与 token 两轴。**基线是 1.0**，所以任何剪枝引起的分数下降都落在 [0,1] 内可读。

**基线有意编辑记录（P36，2026-10-28）。** lit-review 的 must_modules 由 M2 M4 **M8** 改为 M2 M4 **M5**：M8 来自
一次分类误判——裸词 `review` 命中 human_review 协作线索，把「文献综述」读成了「人审工作流」；P36 同时修掉了
horizon 词表缺 `week` 的问题（"over several weeks" 从此正确落 multi_session，M5 启用、M8 关闭）。基线跟着修好
的引擎走，理由按 M0.5 记在 `data/scoreboard.json` 的 note 里——这正是「分数变动必须是有意编辑」机制的设计用途。

effect 轴给消融的第二问（「剪掉的东西对**任务效果**有影响吗」）提供了落点：同一任务在裸跑 / 全
harness / 剪枝配置下各跑真实运行，效果分记进各自任务的 `effect` 收据——但这是**运行时**的测量，
scoreboard 只承载与守护它，不产生它。

## 4. What it is not · 非目标（写死）

- **结构分不是任务效果**：5 条结构轴衡量的是 harness **发射**（路由对不对、该给的给没给、产物能不能过自检）。
  任务效果是 effect 轴的事，而 effect 在真实测量前**不提供任何质量结论**（连「效果差」都不说，只说「未测量」）。
- **不是逐域 rubric**：不与 `data/rubrics.json` 抢活。
- **不自动晋升**：分数变动触发的是**人工裁决**（改 baseline 或修引擎），不触发任何自动变更（M0.4/M0.8）。

## 5. Verification

P23 落地时：`PYTHONPATH=src python -m unittest discover -s tests` → 305 OK；`harness cycle audit`
→ 19 cycles · 0 hard · 0 gaps；P16.9 → `done`（`done_in: P23`）；HARNESS-MAP 重生成（新子命令
`scoreboard`）。P24 增补后：测试 **315 OK**（+6 trace 守卫 · +4 effect 守卫，见 PROGRESS 同日条目）；
结构基线仍全 1.0；CLI 实测输出：

```
  [lit-review    ] domain=research           total=1.0000  routing=1 capabilities=1 modules=1 structure=1 emission=1  effect=unmeasured
  [unit-tests    ] domain=general            total=1.0000  routing=1 capabilities=1 modules=1 structure=1 emission=1  effect=unmeasured
  [kg-dh         ] domain=digital-humanities total=1.0000  routing=1 capabilities=1 modules=1 structure=1 emission=1  effect=unmeasured
  [deep-research ] domain=deep-research      total=1.0000  routing=1 capabilities=1 modules=1 structure=1 emission=1  effect=unmeasured
  [model-choice  ] domain=model-selection    total=1.0000  routing=1 capabilities=1 modules=1 structure=1 emission=1  effect=unmeasured
  overall=1.0000 over 5 task(s)
```
