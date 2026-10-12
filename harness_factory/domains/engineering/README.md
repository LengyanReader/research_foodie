# Domain · Engineering · 工程学域
> Wiring `core/` modules into a constraint-driven design-and-build workflow with bench verification.
> 把 `core/` 模块接线成「约束驱动、以台架验证」的工程设计与建造流程。
**Updated:** 2026-10-12

---

## 中文速览
工程域的目标是**在明确约束下给出经实测验证的设计**。以 L0–L5 编排 `core/`：L0 需求与约束（M7）、L1 计算/建模（M1/M3）、L2 设计与仿真（M3/M6）、L3 建造/原型（M6/M2）、L4 按规格测试（M3/M4）、L5 文档与放行（M7）。域特有风险：**约束漂移**、**仿真与实测脱节**、**公差/裕度缺失**、**失效模式未分析（FMEA）**、**安全检查被跳过**。

---

## What this domain is for · 用途
Take a requirement to a verified artifact — a part, a circuit, a structure — where constraints are explicit, the design is simulated, the prototype is tested to spec, and failure modes are analyzed before release.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Requirements & constraints | M0, M7 | budget, tolerance, safety factor |
| L1 | Calculate / model | M1, M3 | assumptions stated; units checked |
| L2 | Design & simulate | M3, M6 | FEA/EDA/SPICE; margins |
| L3 | Build / prototype | M6, M2 | revision-controlled CAD/BOM |
| L4 | Test to spec | M3, M4 | bench data vs requirement (gate) |
| L5 | Document & release | M7, M4 | drawings, BOM, provenance |

## Module combination · 模块组合
- **M0** — a simulated pass is not a physical pass; verify on the bench.
- **M1** — load the governing constraint, not the whole spec dump.
- **M2** — prototypes iterate across sessions; keep revisions and test logs.
- **M3** — gate: measured values within tolerance; safety factors honored.
- **M4** — requirement ↔ analysis ↔ test-result ledger; record deviations.
- **M6** — toolchain pinned (CAD/FEA/EDA versions); fail-loud on unit mismatch.
- **M7** — releases (BOM, drawings) are governed; no unapproved changes.

## Discipline-specific risks · 领域特有风险
- **Constraint drift** — requirements quietly relaxed to fit the design.
- **Simulation–reality gap** without a bench check.
- **Missing tolerances / safety margins**.
- **Failure modes not analyzed** (no FMEA).
- **Safety gates skipped** under schedule pressure.

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/devops/README.md` · `../domains/software-engineering/README.md`.
