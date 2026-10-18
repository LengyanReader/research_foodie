# Domain · Chemistry · 化学域
> Wiring `core/` modules into a reaction- and structure-grounded synthesis workflow with safety gates.
> 把 `core/` 模块接线成「以反应与结构为据、带安全门」的化学流程。
**Updated:** 2026-10-18

---

## 中文速览
化学域的目标是**让每个分子/产率/条件都可溯源，且实验安全风险被显式声明**。以 L0–L5 编排 `core/`：L0 定目标与假设（M7）、L1 文献与机理（M1/M4）、L2 合成/计算方案（M6）、L3 执行与表征（M6/M2）、L4 结构/纯度/产率验证（M3/M4）、L5 出稿（M7）。域特有风险：**结构误判**、**纯度/产率夸大**、**未标注的危害与处置**、**不可复现的条件**。

---

## What this domain is for · 用途
Move from a target molecule or transformation to an evidence-backed result — a characterized compound, a computed mechanism, a validated protocol — with conditions, safety, and characterization fully recorded so another lab can reproduce it.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Define target / hypothesis | M0, M7 | structure + purpose; plan-first |
| L1 | Literature & mechanism | M1, M4 | cite conditions; note conflicts |
| L2 | Plan synthesis / computation | M6, M3 | feasibility + safety screening |
| L3 | Run & characterize | M6, M2 | raw spectra immutable; append-only |
| L4 | Verify structure & yield | M3, M4 | independent technique (NMR/MS/XRD) |
| L5 | Report (safety-aware) | M7, M4 | hazards, disposal, provenance |

## Module combination · 模块组合
- **M0** — a plausible structure is not an identified one; require evidence.
- **M1** — load only the relevant precedent, not the whole literature.
- **M2** — multi-step syntheses span sessions; log every batch reproducibly.
- **M3** — gate: characterization agrees across techniques; yield reported honestly.
- **M4** — claim ↔ spectrum ↔ condition ledger; mark unverified intermediates.
- **M6** — instruments/computation stack pinned and fail-loud (e.g. Gaussian, RDKit).
- **M7** — protocols are reviewable; no auto-sharing of hazardous procedures outside the gate.

## Instruments · 仪器
- **Structure & property** — `rdkit` (canonical identifiers, substructure search, descriptors) with the toolkit version recorded.
- **Accession-backed records** — `rcsb-pdb` (experimental vs computed structures) · `uniprot` (sequence, reviewed / unreviewed); quote the database release.
- **Gate evidence** — canonical id **+** accession **+** version; a compound *name* alone is not an identification.
- Full map: `../reference/evidence-instruments.md#chemical--biological-claims`.

## Discipline-specific risks · 领域特有风险
- **Structure misassignment** from a single technique.
- **Yields/burn-in reported without conditions** (solvent, temp, time, purity).
- **Safety blind spots** — hazards and disposal omitted from the record.
- **Non-reproducible "optimized" conditions**.

**Information outlets · 信息源**：本领域的高质量门户 / 期刊 / 预印本 / 数据库 / 媒体见 `../reference/outlet-map.md`（机器可读：`data/sources.json` 的 `outlets` 组；`harness sources --group outlets` 查看）。

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/biology/README.md`.
