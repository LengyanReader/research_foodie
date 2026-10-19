# M5 · Self-Evolution · 自演化
> Making the harness improve itself — signal → audit → mutation → journal, human-gated.
> 让 harness 自我改进——信号 → 审计 → 变异 → 日志，人类把关。
**Updated:** 2026-10-12

---

## 中文速览
一个不能从失败中学习的 harness 会以同样方式反复失败（M0.10）。M5 定义**受控的自我改进回路**：**信号**（真实运行中的失败/低效）→ **审计**（可否泛化？是否一次性？）→ **变异**（受控地改动 harness 自身）→ **日志**（可回滚、可归因）。变异类型：Promote / Register / Deepen / Fission / Archive / Consolidate。**全部人类把关**（M0.8）；用留出集衡量是否真变好；警惕**误演化**（reward hacking、目标漂移）。AI 侧的对应工作谱系（Self-Refine/Reflexion、ADAS、Gödel Agent、FunSearch/AlphaEvolve/OpenEvolve、SEAL、Voyager）见 `review/harness-catalog.md` §3。上游：M0.10、M0.4。下游：M7（变更治理）。

**循环层面另有契约（M5.10）**：一次能力拓展 / 深化 / 更新 / 演化即一个**轮次**，须登记于 `data/cycles.json`，并按**完成定义**（子句 · 判别力 · 门禁 · 溯源 · 路由 · 可达）逐项过关；**有意不做**的事须登记为带**理由**与**重访触发条件**的路线图条目。`harness cycle audit` 同时报告**硬问题**与剩余**缺口面**——后者就是下一轮的输入，故循环可持续而非偶发。过程见 `reference/capability-cycle.md`。

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

## The capability round · 能力循环

The loop above governs one **mutation**. A **round** (a cycle) governs many at once: it is the unit in which the capability set expands, deepens or is refreshed. Its failure mode is different — not a bad mutation, but a round that never closes, or a deferral that quietly disappears. So the round gets its own contract.

10. **The round is a mechanism, not a habit (M5.10).** Every capability round is recorded in `data/cycles.json` and must clear the **definition-of-done** before it is marked done: a **clause** (which invariant it answers to), a **discriminator** (a trigger the engine can actually evaluate — not a predicate it silently ignores), a **guard** (a test that fails if the wiring is removed), **provenance** (a first-party source in `sources/source-map.md`), a **router row** (findable from a *situation*, not only from its own name) and **reachability** (listed by `harness skill`, so one instruction reaches it). A round that adds a capability without these is not done, however good the prose is. What is deliberately **not** added becomes a `roadmap` entry with a **reason** and a **revisit trigger** — a deferral is a decision, not an omission. `harness cycle audit` reports the hard problems *and* the remaining **gap surface** (missing router rows, provenance rows, guards; clauses referenced but never anchored in their own module), and that surface is the seed of the next round. The round stays **proposal-first**: it ranks candidates and drafts slices; humans accept them (M0.4, M0.8). A round is **closed**, never "in progress forever": `active` is a state, not a resting place.

## Checklist
- [ ] Signals come from real runs, not speculation.
- [ ] Each mutation passes an audit (pattern? generalizes? M0-consistent?).
- [ ] Mutations are typed, minimal, and journale with a rollback path.
- [ ] Improvement is measured on a holdout, not the tuning set.
- [ ] Substantive mutations are human-gated.
- [ ] The round is in `data/cycles.json` and passes `harness cycle audit`; its non-additions carry a reason and a revisit trigger (M5.10).

## Anti-patterns
- **Unbounded self-modification.** The harness rewrites itself with no audit or gate.
- **Overfit promotion.** A fix for one instance becomes a global rule.
- **Metric-free promotion.** "Feels better" without a measured gain.
- **Silent mutation.** Changes with no journal entry and no way back.
- **Capability without safety.** Raising power while relaxing containment.
- **Round without closure.** A cycle opens, produces good prose, and is never marked done or audited — so the same gap is rediscovered next time.
- **Silent deferral.** A capability that was deliberately *not* added is dropped without a reason or a revisit trigger, and the decision evaporates.

## See also
`01-meta-principles.md` (M0.10, M0.4, M0.8) · `../review/harness-catalog.md` §3, §8 · `08-change-governance.md` (M7) · `04-verification-and-gates.md` (M3) · `../reference/capability-cycle.md` (how to run a round; `harness cycle`).
