# Scored task set · 本库自己的打分任务集（P23）

> **中文速览。** 关闭 P16.9 的重访触发（「本库有打分任务集」），给 `component-ablation`（M5.12）一个能跑
> 的留出集，也给 D1 阶段 C（带测量的晋升）补上它的前置依赖。**5 个任务 × 5 条确定性轴**（路由 · 能力覆盖 ·
> 模块覆盖 · 结构自检 · 干净发射），全部**1.0 基线**由 `tests/test_scoreboard.py` 钉死——分数变动必须是
> `data/scoreboard.json` 的一次**有意编辑**，绝不静默漂移。所有 allowed/must 值来自 2026-10-23 的一次实测
> `classify+derive`，不是凭记忆写的（M0.4）。**非目标**：这是 harness **发射质量**的分，不是任务质量基准，
> 也不替代 `harness standard` 的逐域 rubric。

**Updated:** 2026-10-23 · **Round:** P23 · **Closes:** P16.9 (done_in P23) · **Unblocks:** M5.12 ablation, D1 stage C

## 1. The set · 任务集

| id | task | allowed domains | must capabilities | must modules |
|---|---|---|---|---|
| lit-review | Write a literature review with citations over several weeks | research, deep-research | traceable-sources · evidence-bounded-generation · prose-polish · loop-discipline | M2 M4 M8 |
| unit-tests | Add unit tests to the parser | general, software-engineering | verification-gate · eval-driven-development | M3 |
| kg-dh | 构建方志人物知识图谱，做检索增强问答，注明来源 | digital-humanities | ontology-as-contract · entity-resolution · evidence-bounded-generation · schema-evolution | M2 M4 |
| deep-research | Deep research report on agent memory systems with citations | deep-research | traceable-sources · evidence-bounded-generation · prose-polish | M2 M4 |
| model-choice | 在 GPT 和 Claude 之间选一个模型来跑评测 | model-selection | model-portfolio-discipline · eval-driven-development | M2 M4 |

## 2. The scoring function · 打分函数（5 轴，全确定性）

1. **routing** — 分类落域 ∈ allowed 集合（0/1）。
2. **capabilities** — must 能力 ⊆ 实际命中能力（覆盖率 0..1）。
3. **modules** — must 模块 ⊆ 实际启用模块（覆盖率 0..1）。
4. **structure** — 发射的脚手架过 `check_harness`（文件齐、manifest 合法、无占位符，0/1）。
5. **emission** — 发射文件中无未渲染的 `{{…}}`（0/1）。

`total = mean(5 axes)`。离线、无 LLM、无网络（M0.4：只测量，不发明）。运行：
`harness scoreboard [--task <id>] [--json]`。

## 3. How ablation consumes it · 消融怎么用它

M5.12 的对照口径是**同一任务上全部消融的中位数**——本集就是那批任务：对一个发射物做单单元剪枝后
（按实现边界改 `data/scoreboard.json` 的 must 集、或剪掉一个模块的发射产物），重跑 `scoreboard`，
对比 `total` 与 token 两轴。**基线是 1.0**，所以任何剪枝引起的分数下降都落在 [0,1] 内可读。

## 4. What it is not · 非目标（写死）

- **不是任务质量基准**：分数衡量的是 harness **发射**（路由对不对、该给的给没给、产物能不能过自检），
  不是任务本身做得好不好——那需要每个任务的 rubric（`harness standard` 的职责）。
- **不是逐域 rubric**：不与 `data/rubrics.json` 抢活。
- **不自动晋升**：分数变动触发的是**人工裁决**（改 baseline 或修引擎），不触发任何自动变更（M0.4/M0.8）。

## 5. Verification

`PYTHONPATH=src python -m unittest discover -s tests` → **305 OK**（+3 守卫）；
`harness cycle audit` → **19 cycles · 0 hard · 0 gaps**；P16.9 → `done`（`done_in: P23`）；
HARNESS-MAP 重生成（新子命令 `scoreboard`）。CLI 实测输出：

```
  [lit-review    ] domain=research           total=1.0000
  [unit-tests    ] domain=general            total=1.0000
  [kg-dh         ] domain=digital-humanities total=1.0000
  [deep-research ] domain=deep-research      total=1.0000
  [model-choice  ] domain=model-selection    total=1.0000
  overall=1.0000 over 5 task(s)
```
