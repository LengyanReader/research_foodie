# Domain · Economics & finance · 经济与金融域
> Wiring `core/` modules into identification-first analysis of markets and policy.
> 把 `core/` 模块接线成「识别优先」的经济与市场分析流程。
**Updated:** 2026-10-12

---

## 中文速览
经济金融域的目标是**让因果声明建立在可辩护的识别策略与稳健性检验上**。以 L0–L5 编排 `core/`：L0 假设与估计目标（M7）、L1 数据与来源汇整（M4/M6）、L2 识别/建模（M3）、L3 稳健性与敏感性（M3/M4）、L4 样本外/回测（M3）、L5 出稿（M7）。域特有风险：**相关当因果**、**前视偏差**、**幸存者偏差**、**过拟合回测**、**交易成本/摩擦忽略**、**数据修订（vintage）未记录**。

---

## What this domain is for · 用途
Turn a hypothesis about a market, policy, or asset into a defensible result — an estimate, a forecast, a backtest — with an explicit identification strategy, honest robustness, and out-of-sample discipline.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Hypothesis & estimand | M0, M7 | state the causal target |
| L1 | Assemble data & sources | M4, M6 | record vintage/revision |
| L2 | Identify / model | M3 | strategy stated before results |
| L3 | Robustness & sensitivity | M3, M4 | placebo, other specs |
| L4 | Backtest / out-of-sample | M3 | point-in-time; costs included |
| L5 | Report with provenance | M7, M4 | data/code availability |

## Module combination · 模块组合
- **M0** — a strong correlation is not an effect; name the identification.
- **M1** — load only the sample and specs currently under test.
- **M2** — long backtests checkpoint; keep the full trial ledger.
- **M3** — gate: pre-specified test + out-of-sample; verify before claiming.
- **M4** — data vintage ↔ result ledger; flag revised/estimated series.
- **M6** — data/quant stack pinned; fail-loud on lookahead in feature code.
- **M7** — results reviewable; no auto-trading or auto-publish (M0.8).

## Discipline-specific risks · 领域特有风险
- **Correlation ≠ causation** without a credible design.
- **Lookahead / survivorship bias**.
- **Backtest overfitting** (too many specs on one sample).
- **Ignoring costs, slippage, liquidity**.
- **Unlogged data revisions** (vintage drift).

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/data-science/README.md`.
