# M5 · Self-Evolution · 自演化
> Making the harness improve itself — signal → audit → mutation → journal, human-gated.
> 让 harness 自我改进——信号 → 审计 → 变异 → 日志，人类把关。
**Updated:** 2026-10-12

---

## 中文速览
一个不能从失败中学习的 harness 会以同样方式反复失败（M0.10）。M5 定义**受控的自我改进回路**：**信号**（真实运行中的失败/低效）→ **审计**（可否泛化？是否一次性？）→ **变异**（受控地改动 harness 自身）→ **日志**（可回滚、可归因）。变异类型：Promote / Register / Deepen / Fission / Archive / Consolidate。**全部人类把关**（M0.8）；用留出集衡量是否真变好；警惕**误演化**（reward hacking、目标漂移）。AI 侧的对应工作谱系（Self-Refine/Reflexion、ADAS、Gödel Agent、FunSearch/AlphaEvolve/OpenEvolve、SEAL、Voyager）见 `review/harness-catalog.md` §3。上游：M0.10、M0.4。下游：M7（变更治理）。

---

## The problem · 问题
Naive self-improvement is how systems optimize the wrong thing and call it progress. The danger is not that the harness cannot change — it is that it changes **unboundedly**, **unaudited**, and **without a way back**. Evolution must be *signal-driven*, *scoped*, *measured*, and *reversible*.

## The loop · 回路

```
signals ──▶ audit ──▶ mutation ──▶ journal
  ▲                                    │
  └──────────── next run ──────────────┘
```

1. **Signals.** Collect only from *real* runs: recurring failures, wasted steps, repeated human corrections, gate misses, near-misses. A signal is evidence, not an opinion (M0.4).
2. **Audit.** Ask: is this a *one-off* or a *pattern*? Does the fix *generalize*, or does it overfit to this instance? Does it contradict M0? Reject unauditable signals.
3. **Mutation.** Apply a **typed, minimal** change to the harness itself. Recommended vocabulary:
   - **Promote** — raise a repeated fix into a permanent rule/guide/sensor.
   - **Register** — record a new capability/tool/source in the registry.
   - **Deepen** — add detail to an existing skill/rule.
   - **Fission** — split an overloaded module into two.
   - **Archive** — retire a dead rule/asset (with reason).
   - **Consolidate** — merge duplicates to restore SSOT (M0.5).
4. **Journal.** Write an append-only entry: signal, audit verdict, mutation diff, expected effect, rollback path (M0.9).
5. **Human gate (M0.8).** Substantive mutations — especially those altering verification, scope, or autonomy — require explicit human authorization. Machines may *propose* and *rank* mutations; humans *decide* (M0.4).

## Guardrails · 护栏

- **Measure on holdout.** A mutation is "better" only if it improves a metric on tasks it was not tuned on. No metric, no promotion.
- **Bound the blast radius.** Sandbox the change; canary it; keep a rollback.
- **Watch for misevolution.** Reward hacking, goal drift, and capability–safety violations are failure modes of self-improvement itself — gate capability increases behind stricter safety checks.
- **Slow the loop to the review cycle.** Fast, unbounded self-modification is a liability; align mutation cadence with human review.

> **中文**：信号→审计（可否泛化）→变异（Promote/Register/Deepen/Fission/Archive/Consolidate）→追加日志；全部人类把关；留出集衡量；沙箱+金丝雀+回滚；警惕误演化（reward hacking、目标漂移）。

## Checklist
- [ ] Signals come from real runs, not speculation.
- [ ] Each mutation passes an audit (pattern? generalizes? M0-consistent?).
- [ ] Mutations are typed, minimal, and journale with a rollback path.
- [ ] Improvement is measured on a holdout, not the tuning set.
- [ ] Substantive mutations are human-gated.

## Anti-patterns
- **Unbounded self-modification.** The harness rewrites itself with no audit or gate.
- **Overfit promotion.** A fix for one instance becomes a global rule.
- **Metric-free promotion.** "Feels better" without a measured gain.
- **Silent mutation.** Changes with no journal entry and no way back.
- **Capability without safety.** Raising power while relaxing containment.

## See also
`01-meta-principles.md` (M0.10, M0.4, M0.8) · `../review/harness-catalog.md` §3, §8 · `08-change-governance.md` (M7) · `04-verification-and-gates.md` (M3).
