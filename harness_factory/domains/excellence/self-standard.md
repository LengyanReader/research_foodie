# Self-standard · This project against Claude's bar · 本项目对标 Claude 最高标准

> Applying the frontier-standard ratchet **to harness_factory itself** — the project is held to the same bar it helps others aim at.
> 把最高标准棘轮**应用到 harness_factory 自身**——项目被要求达到它帮别人对标的那条标杆。
**Updated:** 2026-10-14 · Companion to `README.md` and `standard-ladder.md`.

---

## 中文速览

这份文档把「最高标准」这套机制**反身用在 harness_factory 上**：**定标 → 打分 → 差距审计 → 配置 harness → 提升 → 棘轮（只升不降）→ 跟踪前沿**。

- **标杆（R5）**：Anthropic 公开的工程实践——[*Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents)（简洁、透明、精雕 ACI）与 [*Writing effective tools for agents*](https://www.anthropic.com/engineering/writing-tools-for-agents)（工具要评估、职责单一、返回高信号）。
- **尺子**：`software-engineering` 评分表（`data/rubrics.json`），六维加权。
- **基线（2026-10-14）**：总分 **2.05 / 3.00**，下限棘轮至 2.05。
- **最大短板**：安全（1/3）> 正确性、测试、可维护（各 2/3）> 文档、性能（已达 3/3）。
- **配置（由 `harness standard plan` 产出，人工采纳）**：启用模块 **M3 校验 · M7 审查**；工具建议见下。
- **铁律**：标杆须可核验（M4）；「是否达到」由人工确认（M0.8）；本项目**绝不自我宣称**已达最高标准。

---

## 0. Why · 为什么反身应用

A harness factory that sells "aim at the highest standard" must itself be built to one. This document names that bar, records a baseline, and ratchets — using the project's own `harness standard` command, so the claim is checkable and reproducible, not rhetorical. · 造「最高标准」工具的项目，自身也必须有一个标准。本文给出标杆、记录基线与棘轮，且用项目自己的 `harness standard` 命令产出——可核验、可复现，而非空话。

## 1. The bar · 标杆（R5 · frontier exemplar）

| field · 字段 | value · 值 |
|---|---|
| level · 级 | **R5 frontier (best exemplar)** |
| name · 名称 | Anthropic engineering practice — *Building effective agents* + *Writing effective tools for agents* |
| source · 来源 | <https://www.anthropic.com/engineering/building-effective-agents> · <https://www.anthropic.com/engineering/writing-tools-for-agents> |
| benchmark · 参照 | Anthropic's three agent principles: **simplicity**, **transparency**, careful **agent-computer interface (ACI)** |
| checked · 复核 | 2026-10-14 (published 2024-12-19 / 2025-09-11) |

**What the bar demands, distilled · 标杆要求（提炼）**
1. 简洁优先——简单可组合的模式胜过复杂框架；先在**基础组件**上迭代，只有确证改善结果才加复杂度。
2. 透明——显式展示规划步骤；让 agent 的行为可观测、可调试。
3. 精雕 ACI——工具说明与评测与 HCI 同等重要；工具职责单一、返回高信号、token 高效。
4. 评测驱动——先有评测任务与可验证结果，再谈优化；用 LLM 评委 + **人工评审**互补。

## 2. The ruler · 尺子（`software-engineering` rubric）

| dim · 维度 | weight · 权重 | 内涵 |
|---|---|---|
| correctness · 正确性 | 0.25 | 行为符合规格；有 oracle/测试兜底 |
| tests · 测试 | 0.20 | 自动化、覆盖风险路径 |
| maintainability · 可维护 | 0.20 | 模块化、可逆小改动 |
| security · 安全 | 0.15 | 威胁建模、最小权限 |
| docs · 文档 | 0.10 | 决策与用法可查 |
| performance · 性能 | 0.10 | 有基准与画像 |

## 3. Baseline · 基线（2026-10-14）

| dim | ours · 现状 | weight | weighted gap |
|---|---|---|---|
| security | 1 / 3 | 0.15 | 0.300 |
| correctness | 2 / 3 | 0.25 | 0.250 |
| tests | 2 / 3 | 0.20 | 0.200 |
| maintainability | 2 / 3 | 0.20 | 0.200 |
| docs | 3 / 3 | 0.10 | 0.000 |
| performance | 3 / 3 | 0.10 | 0.000 |
| **total · 合计** | **2.05 / 3.00** | | **floor ratcheted to 2.05** |

> 打分依据（人工）：纯 stdlib、`unittest` 全绿、双语文档完备（`docs 3`、`performance 3`）；测试与正确性尚可但未穷尽（各 `2`）；安全**尚无正式威胁模型**（`1`）。此评分是**自评**，`unverified` 直到有独立的对照证据。

## 4. Configuration · 配置（`harness standard plan`, observe-only）

`harness standard --domain software-engineering plan harness-factory` 建议：

- **启用模块**：`M3`（校验/门禁）、`M7`（审查/可逆变更）。
- **工具建议（来自目录 `data/harnesses.json`）**：
  - `correctness` / `tests` → 评测框架类：`lm-eval-harness`, `helm`, `simple-evals`
  - `security` → 安全框架类：`saver`, `misevolution`
- **人工诠释（本项目实际做法）**：本仓库的 oracle 是 **stdlib `unittest` 套件 + `catalog.validate()` 漂移门**，而非 LLM 评测；因此把计划落地为——
  1. 为高风险路径补测试与属性校验（缩短 `correctness`/`tests` 差距）；
  2. 增补一份**威胁模型 / 最小权限**说明（关闭 `security` 差距）；
  3. 持续减小改动粒度、保持可逆（`maintainability`）。

## 5. The ratchet · 棘轮

`floor_next = max(floor, achieved)`。下限只升不降：任何后续变更不得使总分低于 2.05，除非人工显式豁免（`--force`）。标杆会移动——Anthropic 会更新实践——因此按 **`FRONTIER_MAX_AGE_DAYS`（90 天）** 复核；`harness evolve` 会对过期标杆发出 `stale_frontier` 提案。

```bash
# Reproduce · 复现
harness standard --domain software-engineering show harness-factory     # bar + floor + gap
harness standard --domain software-engineering audit harness-factory    # gaps, largest first
harness standard --domain software-engineering plan  harness-factory    # config: modules + tools
harness evolve --dry-run                                                # flags a stale frontier (>90d)
```

## 6. Boundary · 边界

- 标杆有据（M4）、可测（同一把尺子）；无独立证据时评分标 `unverified`。
- 「是否达到」由**人工**确认（M0.8）；工具只**度量与记录**，绝不自我加冕（M0.4）。
- 差距映射（`data/levers.json`）是**建议**，最终配置由人决定。

## See also
`README.md`（本域总览）· `standard-ladder.md`（棘轮机制）· `../../GUIDE.md`（Example 9）· `../../src/harness_factory/data/levers.json` · `../../src/harness_factory/data/rubrics.json`.
