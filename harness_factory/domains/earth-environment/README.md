# Domain · Earth & environmental science · 地球与环境科学域
> Wiring `core/` modules into a spatiotemporal data pipeline with model/data provenance.
> 把 `core/` 模块接线成「带时空数据与模型溯源」的地球环境流程。
**Updated:** 2026-10-12

---

## 中文速览
地球/环境域的目标是**在明确的时空栅格上给出经独立数据校验的结论**。以 L0–L5 编排 `core/`：L0 界定区域·时段·问题（M7）、L1 汇整空间与观测数据（M4/M6）、L2 建模或分析（M3）、L3 独立数据验证（M3/M4）、L4 不确定性量化（M4）、L5 出图与台账（M7）。域特有风险：**时空尺度不匹配**、**外推越界**、**代理数据（proxy）当作直接观测**、**缺失数据被静默填补**。

---

## What this domain is for · 用途
Produce a defensible statement about a place and period — a climate trend, a geological interpretation, an environmental assessment — where the spatiotemporal domain, data sources, model assumptions, and uncertainty are all explicit and independently checkable.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Define region, period & question | M0, M7 | explicit spatial/temporal frame |
| L1 | Assemble geospatial/observational data | M6, M4 | cite datasets, resolution, accuracy |
| L2 | Model or analyze | M3 | state assumptions & parameterization |
| L3 | Validate vs independent data | M3, M4 | withhold, cross-sensor check |
| L4 | Quantify uncertainty | M4 | ensemble/CI; no point-estimate claims |
| L5 | Report (map + ledger) | M7, M4 | reproducible grids & code |

## Module combination · 模块组合
- **M0** — a colored map is not a finding; the claim must survive scrutiny.
- **M1** — carry one resolution/CRS at a time to avoid silent resampling.
- **M2** — multi-decadal or multi-scene runs are resumable; raw scenes immutable.
- **M3** — gate on independent validation and honest skill scores.
- **M4** — data ↔ grid ↔ model-version ledger; mark interpolated/proxy values.
- **M6** — geospatial stack pinned (GDAL/PROJ/CRS versions recorded).
- **M7** — publication and data-sharing are governed acts.

## Discipline-specific risks · 领域特有风险
- **Scale mismatch** (pixel vs process) and **CRS/resampling** errors.
- **Extrapolating** beyond the observed space/time.
- **Proxy mistaken for direct measurement**.
- **Silent gap-filling** of missing data.
- **Model tuning to a target period** (overfitting the past).

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/data-science/README.md`.
