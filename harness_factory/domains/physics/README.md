# Domain · Physics · 物理学域
> Wiring `core/` modules into a measurement-grounded, unit-checked physics workflow.
> 把 `core/` 模块接线成「以测量为据、量纲自洽」的物理学流程。
**Updated:** 2026-10-18

---

## 中文速览
物理域的目标是**让每个数字都可溯源、每个结论都经得起量纲与误差检验**。以 L0–L5 编排 `core/`：L0 提问与假设（M7）、L1 装置/推导设计（M1/M3）、L2 采集测量（M6）、L3 分析与误差传播（M3/M4）、L4 与理论对表（M4）、L5 出稿（M7）。域特有风险：**量纲/单位错误**、**系统误差未标注**、**选择性报告**。工具链本地优先（Python/numpy、ROOT、Jupyter、LaTeX）。

---

## What this domain is for · 用途
Turn a physical question into a reproducible result — a measurement, a simulation, a derivation — where every quantity carries units, provenance, and an uncertainty, and where the analysis could be re-run by a skeptic to the same number.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Question & hypotheses | M0, M7 | falsifiable statement; plan-first |
| L1 | Apparatus / derivation | M1, M3 | minimal context; define the acceptance test |
| L2 | Acquire measurements | M6, M2 | raw data immutable; hash + timestamp |
| L3 | Analyze & propagate error | M3, M4 | units checked; systematics named |
| L4 | Cross-check vs theory | M4 | independent method / known constant |
| L5 | Report | M7, M4 | figures + ledger; no auto-publish |

## Module combination · 模块组合
- **M0** — truth before throughput: a cleaner number is not a truer number.
- **M1** — carry only the relevant theory and data window per step.
- **M2** — long simulation/DAQ runs must be resumable; raw data is append-only.
- **M3** — the gate is dimensional consistency + an independent recomputation.
- **M4** — the spine: data → reduction → figure, each with provenance; uncertainties explicit.
- **M6** — acquisition/analysis stack: minimal, pinned versions, fail-loud.
- **M7** — results are reviewable diffs; publishing a claim is a governed act.

## Instruments · 仪器
- **Units & dimension discipline** — `pint`; **uncertainty propagation** — `uncertainties` (first order), with the GUM (`[R107]`) defining how a budget is combined and reported (coverage factor `k`).
- **Simulation credibility** — declare whether V&V was performed and what it covered (`[R108]`), plus a sensitivity / UQ assessment.
- **Gate evidence** — dimensionally consistent expressions **and** a stated uncertainty budget; no unit-free numbers, no "value ± nothing".
- Full map: `../reference/evidence-instruments.md#physical-quantities`.

## Discipline-specific risks · 领域特有风险
- **Unit / dimensional slips** silently change the answer — gate on units.
- **Under-reported systematics** (rounding a systematic to zero).
- **Cherry-picked runs** — keep every run in an append-only ledger.
- **Digging for a target p-value** — pre-state the test and stopping rule.

**Information outlets · 信息源**：本领域的高质量门户 / 期刊 / 预印本 / 数据库 / 媒体见 `../reference/outlet-map.md`（机器可读：`data/sources.json` 的 `outlets` 组；`harness sources --group outlets` 查看）。

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/data-science/README.md` (shared experiment discipline).
