# Domain · Medicine / clinical · 医学与临床域
> Wiring `core/` modules into evidence-graded, high-stakes, human-in-the-loop clinical reasoning.
> 把 `core/` 模块接线成「循证分级、高风险、人类在环」的临床推理流程。
**Updated:** 2026-10-12

---

## 中文速览
医学域的目标是**在最高风险等级上仍保持循证与把关**。以 L0–L5 编排 `core/`：L0 界定临床问题（PICO，M7）、L1 证据评价（M4/M1）、L2 鉴别诊断/方案推理（M3）、L3 **高风险门（临床医师复核）**（M8/M0.8）、L4 记录与引用（M4）、L5 随访与审计（M5/M3）。域特有风险：**把建议当诊断**、**证据过时/分级不当**、**遗漏禁忌与相互作用**、**个体差异外推**、**AI 输出未把关**。

> **This domain is not a medical device and gives no clinical advice.** It only wires harness *patterns*; every clinical action is human-gated (M0.4/M0.8).

---

## What this domain is for · 用途
Structure clinical reasoning so that evidence is graded, uncertainty is explicit, and no high-stakes act (diagnosis, prescription, triage) proceeds without authorized human review.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Define the clinical question | M0, M7 | PICO; scope of decision |
| L1 | Appraise evidence | M4, M1 | grade sources; note recency |
| L2 | Reason to differential / plan | M3 | separate reasoning from decision |
| L3 | High-stakes gate | M8, M0.8 | clinician review; no auto-action |
| L4 | Document with citations & caveats | M4 | traceable, uncertainty flagged |
| L5 | Follow-up / audit | M5, M3 | outcomes close the loop |

## Module combination · 模块组合
- **M0** — never present a suggestion as a diagnosis.
- **M1** — load only de-identified, need-to-know context.
- **M2** — longitudinal cases persist as append-only, auditable state.
- **M3** — default-FAIL gate on high-stakes steps; verify before "counsel".
- **M4** — every recommendation links to graded evidence with a date.
- **M5** — follow-up outcomes feed a human-gated audit, not auto-learning on patients.
- **M8** — human-in-the-loop is mandatory, not optional.

## Discipline-specific risks · 领域特有风险
- **Advice presented as diagnosis**.
- **Stale / mis-graded evidence**.
- **Missed contraindications / interactions**.
- **Extrapolating** across populations.
- **Un-gated AI output** influencing care.
- **PHI exposure** — privacy is a hard gate (M4/M7).

**Information outlets · 信息源**：本领域的高质量门户 / 期刊 / 预印本 / 数据库 / 媒体见 `../reference/outlet-map.md`（机器可读：`data/sources.json` 的 `outlets` 组；`harness sources --group outlets` 查看）。

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/biology/README.md`.
