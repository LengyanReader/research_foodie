# Frontier standard · The ratchet mechanism · 最高标准·棘轮机制

> How to define "the highest standard", measure against it, and improve **monotonically** — without self-declaration.
> 如何定义「最高标准」、对标测量并**单调提升**——且不自我宣称。
**Updated:** 2026-10-13 · Companion to `domains/excellence/README.md`.

---

## 0. The bar ledger · 标杆台账
One append-only record per objective (M2/M4). Without it there is no ratchet. · 每个目标一份只追加台账；没有它就没有棘轮。

```yaml
objective: <what is being raised>       # e.g. "research brief on X"
rubric:    [ {dim, weight, how_measured, scale: 0-3} ... ]   # fixed; same for artifact & bar
bar:       { level: R1..R6, name, source, url|id, checked_at, is_apex: true }   # the standard
artifact_scores: [ {dim, score, evidence} ]   # current output, same rubric
floor:     { score_total, at, evidence }      # highest total ever accepted (ratchet)
gap:       [ {dim, ours, bar, delta, why} ]   # sorted desc by weighted delta
plan:      [ {lever, targets: [dim], expected_delta, status} ]
history:   [ {at, total, note} ]               # monotone non-decreasing totals
```

## 1. L0 — Fix the apex bar · 定标
Name the **current best-known standard** for this objective and make it **checkable** (M4/M0.1):
- **Benchmark/leaderboard** — the current SOTA entry (id + score + date). See `catalog --kind research-eval`, `--class evaluation`.
- **Exemplar** — the canonical top human/expert work (paper, product, artifact) others copy.
- **Spec** — a formal standard/rubric (e.g. PRISMA, IEEE, WCAG, a style guide).

Rules · 规则: prefer a **measurable** bar over an adjective; record `checked_at`; if the bar is a person/opinion, mark confidence; **a human confirms** the bar before it's used (M0.8). **No named, sourced bar ⇒ do not claim excellence** — the objective stays `unverified`.

## 2. L1 — Baseline · 对标
Score the current artifact on the **exact same rubric** used for the bar. Same instrument, both sides (M3) — otherwise the gap is meaningless. Record evidence per dimension.

## 3. L2 — Dimension gap audit · 差距审计
Compute weighted deltas and sort. State the **binding constraint** (the single dimension whose improvement most raises the total). Never average a large deficit away (M0.1).

## 4. L3–L4 — Improve & re-verify · 提升与复测
Pick the **largest** weighted gap; choose one lever; predict the delta; apply; **re-measure on the same rubric**; keep evidence. One lever at a time keeps attribution honest.

## 5. L5 — Ratchet · 棘轮（只升不降）
Adopt the new total as the **floor** only if it **≥** the previous floor; otherwise **revert** (M0.9). The floor is the promise: no future submission may score below it without an explicit, human-approved exception.

```
floor_{n+1} = max(floor_n, achieved_{n+1})      # monotone, never regresses
```

## 6. L6 — Track the moving frontier · 跟踪移动前沿
"Highest" is a **moving target** (M5). On a cadence (per_session / periodic):
1. **Re-check** whether the bar advanced (new SOTA / new exemplar) — `checked_at` staleness is a signal.
2. If it moved, **re-baseline** both artifact and bar; recompute the gap; raise the floor target.
3. Log the re-baseline as a journal entry; the ratchet follows the frontier, not a frozen snapshot.

## 7. L7 — Record · 记录
Append to the ledger: bar (with provenance), rubric, scores, floor, history. Reproducible, auditable, resumable (M2/M4/M0.9).

---

## Measurement vs. verification vs. evolution · 三者的区别
| | question · 问题 | output · 产出 | module |
|---|---|---|---|
| Verification (M3) | is it correct/complete? | pass/fail gate | M3 |
| **Excellence (this)** | **is it as good as the best?** | **gap + ratchet** | **M3,M5,M8** |
| Self-evolution (M0.10/M5) | how does the *system* improve? | proposals + journal | M5 |

## Guardrails · 护栏
- **No self-declared excellence** — the bar and the "we reached it" claim are human-confirmed (M0.8).
- **No unfalsifiable bar** — every standard must be measurable and sourced (M0.1/M4).
- **No regression** — the ratchet floor binds unless a human signs off; reverts are logged (M0.9).
- **No frozen bar** — re-baseline on cadence; stale `checked_at` triggers the frontier loop.
- **Reversibility** — every raise is a reviewable diff; deleting the ledger rolls it back (M0.9).

## Rubric template · 评分模板（示例）
| dim · 维度 | weight | 0–3 anchor | how measured |
|---|---|---|---|
| Fidelity · 保真 | 0.25 | 0 fabricated, all sourced | claim↔source audit |
| Coverage · 覆盖 | 0.20 | ≥ target sources, gaps stated | coverage ledger |
| Rigor · 严谨 | 0.20 | contradictions kept, calibrated | contradiction list |
| Clarity · 清晰 | 0.15 | decision-grade, answer-first | blind reader test |
| Novelty · 洞见 | 0.10 | beyond the obvious sources | comparison to exemplar |
| Polish · 打磨 | 0.10 | top-venue-level presentation | rubric spot-check |

> Aggregate = Σ weight × score. Compare artifact vs bar on the **same** column set; ratchet the total.
