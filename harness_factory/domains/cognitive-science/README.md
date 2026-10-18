# Domain · Cognitive science · 认知科学域
> Wiring `core/` modules into cognitive claims: an operationalised construct, a pre-specified design, a model, and a replicable result.
> 把 `core/` 模块接线成认知主张：构念可操作化、设计预先登记、显式模型、结果可复现。
**Updated:** 2026-10-18

---

## 中文速览
认知科学域的目标是**让「关于心智的主张」可反驳、可复现**：先把构念操作化（构念→任务→指标，M0/M1）；设计先行（条件、控制、被试量与功效；M3/M7）；数据要么采、要么由**显式认知模型**生成（M6）；分析报**效应量 + 区间**并做**模型比较/多重比较控制**（M3/M4）；对结果做复制或压力测试（M5）；交付含材料、数据、代码与预登记（M4/M7）。域特有风险：**构念与任务脱节**、**事后假设（HARKing）**、**只报 p 不报效应量**、**测量信度未验**、**模型不可识别/等价模型未比**、**高度可塑的分析路径**。

---

## What this domain is for · 用途
Turn a claim about cognition (*this manipulation affects working memory*) into something another lab can re-run: a stated construct and its operationalisation, a design fixed before the data, a model whose predictions are compared (not just fitted), and a report with materials, data and analyses. Sits between psychology, neuroscience, linguistics and computational modelling.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Construct & operationalisation | M0, M1 | what is measured, by which task and index |
| L1 | Design & power | M3, M7 | conditions, controls, sample size; pre-registered |
| L2 | Data or simulation | M6 | collect, or generate from an explicit model |
| L3 | Analysis (gate) | M3, M4 | effect sizes + intervals; multiplicity and model comparison |
| L4 | Replication / stress test | M3, M5 | hold-out, new sample, sensitivity analysis |
| L5 | Report | M7, M4 | materials, data, code, pre-registration link |

## Module combination · 模块组合
- **M0** — a construct is a claim; operationalise it before measuring it.
- **M1** — hypotheses, design and analysis plan live in context, fixed before the data.
- **M2** — multi-session studies checkpoint data collection and analysis state.
- **M3** — the gate is effect size with an interval, not a thresholded p-value.
- **M4** — pre-registration, materials and analysis code are provenance for the claim.
- **M5** — replication failure is a signal to update the model, not to bury the study.
- **M6** — cognitive models and neural measures are instruments: fit, identify, and compare them.
- **M7** — human-subjects ethics, consent and de-identification gate release.

## Instruments · 仪器
- **Task runtime** — `psychopy` (lab timing) · `jspsych` (browser studies).
- **Pre-registration gate** — `osf` / registered reports; a deviation from the registered analysis is declared and dated.
- **Modelling** — `lme4` (clustered / longitudinal) · `statsmodels` · `stan` (full-Bayesian intervals); where analytic choices are arbitrary, report the multiverse / sensitivity spread.
- **Gate evidence** — effect size **with an interval** + a reliability estimate for the measure; a bare p-value fails the gate (`[R103]`).
- Full map: `../reference/evidence-instruments.md#empirical-claims`.

## Discipline-specific risks · 领域特有风险
- **Construct–task gap** (the task measures something else).
- **HARKing** (hypotheses stated after the results are known).
- **p-only reporting** (no effect size, interval or power).
- **Unreliable measurement** (no test-retest / internal-consistency check).
- **Equivalent models** (a fitted model claimed without comparing alternatives).
- **Analytic flexibility** (many pipelines; only the significant one reported).

## See also
`../psychology/README.md` · `../medicine/README.md` · `../core/00-index.md` · `../sources/source-map.md` · `../review/disciplines-crosswalk-2026-10.md`.
