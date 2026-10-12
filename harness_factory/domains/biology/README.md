# Domain · Biology / life sciences · 生物学生命科学域
> Wiring `core/` modules into a protocol-, sequence- and evidence-grounded life-science workflow.
> 把 `core/` 模块接线成「以方案、序列与证据为据」的生命科学流程。
**Updated:** 2026-10-12

---

## 中文速览
生物域的目标是**让每份数据都挂在可复现的方案与可溯的序列/样本上**。以 L0–L5 编排 `core/`：L0 提出生物学问题（M7）、L1 证据回顾（M1/M4）、L2 方案/分析设计（M6/M3）、L3 数据获取（湿实验或干分析，M6/M2）、L4 统计与生物学验证（M3/M4）、L5 出稿（M7）。域特有风险：**批次效应**、**多重比较未校正**、**样本污染/混淆**、**序列/版本漂移**、**过度外推**。

---

## What this domain is for · 用途
Answer a biological question with reproducible evidence — a protocol result, a sequencing analysis, an ecological survey — where samples, references, and versions are traceable and statistical claims are calibrated to the design.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Frame the biological question | M0, M7 | mechanism + scope; plan-first |
| L1 | Review prior evidence | M1, M4 | cite datasets/papers with access dates |
| L2 | Design protocol / analysis | M6, M3 | controls, power, version pinning |
| L3 | Acquire data (wet or dry) | M6, M2 | raw reads/samples immutable; hash |
| L4 | Statistical & biological validation | M3, M4 | multiple-testing; effect sizes |
| L5 | Report with provenance | M7, M4 | data/code availability; no auto-push |

## Module combination · 模块组合
- **M0** — a correlation in omics is a hypothesis, not a mechanism.
- **M1** — load the reference genome/panel actually used, not "latest".
- **M2** — large batches and long analyses must be resumable; raw data append-only.
- **M3** — gate on pre-specified contrasts, controls, and multiplicity control.
- **M4** — sample ↔ read ↔ reference ↔ version ledger; flag unverified annotation.
- **M6** — bioinformatics stack pinned (aligner/annotator versions recorded).
- **M7** — releases (data, code) are governed; ethics/IRB constraints enforced.

## Discipline-specific risks · 领域特有风险
- **Batch effects** mistaken for biology.
- **P-hacking / multiple comparisons** without correction.
- **Contamination / sample swaps** undetected.
- **Reference-version drift** making results irreproducible.
- **Over-generalizing** from one cell line / cohort / ecosystem.

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/medicine/README.md` · `../domains/data-science/README.md`.
