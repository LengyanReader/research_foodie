# Domain · Law · 法学域
> Wiring `core/` modules into authority-first legal analysis with citation-currency checks.
> 把 `core/` 模块接线成「权威优先、引证时效核验」的法律分析流程。
**Updated:** 2026-10-12

---

## 中文速览
法学域的目标是**让每个结论都挂在现行有效的权威依据上**。以 L0–L5 编排 `core/`：L0 界定法律问题（M7）、L1 检索支配性权威（M4/M6）、L2 时效核验（good law，M3/M4）、L3 IRAC 推理（M3）、L4 风险与不确定性标注（M4）、L5 交付与引证（M7）。域特有风险：**过时法条/被推翻判例**、**管辖错配**、**把 dicta 当 holding**、**引证失实**、**越界提供法律意见的外观**。

> **Not legal advice.** This domain wires harness *patterns* only; outputs require licensed human review (M0.8).

---

## What this domain is for · 用途
Structure legal work so that every assertion rests on controlling, currently-valid authority — statutes, regulations, and cases — with jurisdiction and currency explicit and uncertainty honestly flagged.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Frame the legal issue | M0, M7 | jurisdiction + question |
| L1 | Find controlling authority | M4, M6 | statutes, regs, binding cases |
| L2 | Check currency (good law) | M3, M4 | overruled? amended? effective date |
| L3 | Reason to conclusion (IRAC) | M3 | issue-rule-application-conclusion |
| L4 | Flag risk & uncertainty | M4 | circuit splits, open questions |
| L5 | Deliver with citations | M7, M4 | pinpoint cites; no auto-filing |

## Module combination · 模块组合
- **M0** — a plausible reading is not controlling authority.
- **M1** — load only the jurisdiction and issue-relevant materials.
- **M2** — long matters persist state; keep a research audit trail.
- **M3** — gate: authority verified current and on-point before reliance.
- **M4** — the spine: every proposition has a pinpoint, dated citation.
- **M6** — legal-research tools minimal; verify sources, never invent case names.
- **M7** — filings/deliverables are governed; no auto-send (M0.8).

## Discipline-specific risks · 领域特有风险
- **Stale authority** (overruled / superseded).
- **Jurisdiction mismatch**.
- **Treating dicta as holding**.
- **Fabricated or mis-pinpointed citations** (a cardinal sin, M0.2).
- **Appearing to give legal advice** without a licensed reviewer.

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md`.
