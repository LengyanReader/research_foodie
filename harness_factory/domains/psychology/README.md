# Domain · Psychology & cognitive science · 心理与认知科学域
> Wiring `core/` modules into pre-registered, replication-aware behavioral research.
> 把 `core/` 模块接线成「预注册、可复现」的行为科学研究流程。
**Updated:** 2026-10-12

---

## 中文速览
心理与认知域的目标是**在预注册与统计功效约束下得到可复现的行为结论**。以 L0–L5 编排 `core/`：L0 假设与预注册（M7/M4）、L1 刺激与测量设计（M1/M3）、L2 数据采集（伦理/知情同意，M6/M2）、L3 分析（功效、效应量，M3）、L4 稳健性与重复（M3/M4）、L5 出稿（开放材料，M7）。域特有风险：**事后假设（HARKing）**、**低功效样本**、**p-hacking**、**测量信效度不足**、**伦理/知情同意缺失**。

---

## What this domain is for · 用途
Produce behavioral findings that could survive replication — with hypotheses and analyses pre-specified, adequate power, validated measures, and open materials — rather than the best-looking result from a garden of forking paths.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Hypotheses & pre-registration | M0, M7, M4 | analysis plan fixed first |
| L1 | Design stimuli & measures | M1, M3 | validated instruments |
| L2 | Collect data (ethics) | M6, M2 | consent/IRB; append-only data |
| L3 | Analyze (power, effect sizes) | M3 | pre-specified contrasts |
| L4 | Robustness / replication | M3, M4 | sensitivity; independent sample |
| L5 | Report with open materials | M7, M4 | data/code/measures shared |

## Module combination · 模块组合
- **M0** — a significant p-value is not an effect; report effect sizes + CIs.
- **M1** — load only the constructs in scope and their validated measures.
- **M2** — multi-wave studies persist state; raw responses immutable.
- **M3** — gate: pre-specified analysis executed as registered.
- **M4** — hypothesis ↔ analysis ↔ result ledger; flag exploratory findings as such.
- **M5** — replication outcomes feed a human-gated synthesis.
- **M7** — open materials are governed; participant privacy is a hard gate.

## Discipline-specific risks · 领域特有风险
- **HARKing** (hypothesizing after results are known).
- **Underpowered samples**.
- **p-hacking / forking paths**.
- **Invalid or unreliable measures**.
- **Missing ethics / informed consent**.
- **Over-generalizing** beyond the sampled population.

**Information outlets · 信息源**：本领域的高质量门户 / 期刊 / 预印本 / 数据库 / 媒体见 `../reference/outlet-map.md`（机器可读：`data/sources.json` 的 `outlets` 组；`harness sources --group outlets` 查看）。

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/social-science/README.md`.
