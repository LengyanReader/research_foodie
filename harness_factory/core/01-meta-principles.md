# M0 · Meta-Principles · 十条承重不变式

> The load-bearing invariants every other module assumes. If a harness violates one of these, the rest collapses.
> 所有其他模块的前提。违反其一，其余皆塌。

**Updated:** 2026-10-12

---

## 中文速览

这是全库的**宪法**。十条不变式按「**真相 > 效率**」的优先级排序。前四条是**诚信类**（不可动摇）：M0.1 真相优先、M0.2 来源可溯、M0.3 先验证再称完成、M0.4 自动化只做「观察/记录/排序」。中三条是**工程类**：M0.5 单一事实来源、M0.6 上下文最小高信噪、M0.7 可续接/幂等。后三条是**治理类**：M0.8 破坏性动作须人工确认、M0.9 变更留痕可回滚、M0.10 让 harness 本身可演化。**冲突时，序号小者胜。**

---

## M0.1 — Truth before throughput · 真相优先于产出

A harness exists to make an agent *more correct over long horizons*, not *faster at producing plausible text*. When speed, elegance, or completeness conflict with accuracy, accuracy wins. Never let a mechanism that "helps finish the task" (summarizing, auto-filling, extrapolating) invent content.

**Test:** Does this optimization change *what is claimed* or only *how fast it's produced*? The former is forbidden.

## M0.2 — Source-grounding · 来源可溯

Every factual claim must trace to a primary source — an official repo, a paper (with ID/DOI), or an official doc page — recorded with an access date. Claims that cannot be verified are marked **unverified**, never presented as fact.

**Corollary:** Prefer primary over secondary. Distinguish *what the source says* from *what you infer from it*. (Deep procedure: M4.)

## M0.3 — Verify before "done" · 先验证再称完成

"Done" is a *verified state*, not a *feeling of completion*. Define the acceptance test before starting; run it before declaring completion; never mark a task done on intention. (Procedure: M3.)

## M0.4 — Machines observe, humans decide substance · 机器只观察，实质靠人决断

Automated mechanisms may **observe, record, count, and rank**. They must **never** fabricate, silently mutate, or delete *substantive* output to make a task look complete. A self-scoring script may rank hypotheses; it may not write the finding. A dedup pass may flag near-duplicates; it may not merge two claims into one the author never made.

**Why:** the harness's value is that its outputs can be trusted at a glance. The moment automation can embellish, that trust is gone.

## M0.5 — Single source of truth · 单一事实来源

Each fact, config value, or definition lives in exactly one canonical place; other appearances *reference* it. Duplication is the primary source of drift. (Procedure: M7.)

## M0.6 — Minimal high-signal context · 最小高信噪**

Give the model the *smallest set of tokens that maximizes the probability of the correct next action*. More context is not better context; irrelevant tokens are a tax on attention. (Procedure: M1.)

## M0.7 — Resumable & idempotent · 可续接、幂等

Any step that can run twice must be safe to run twice. Any long process must be resumable from an externalized state after an interruption, without redoing completed, expensive, or side-effecting work. (Procedure: M2.)

## M0.8 — Human gate on destructive / irreversible acts · 破坏性动作人工拦

Irreversible or wide-blast-radius actions — deleting data, pushing, publishing, spending money, contacting people — require explicit human authorization, even when the agent is confident. Reversible local edits do not. (Procedure: M8.)

## M0.9 — Changes are visible and reversible · 变更可回滚

Every substantive change to the harness or its outputs should be a reviewable, attributable diff with a way back. Append-only ledgers and version control are default. (Procedure: M7.)

## M0.10 — The harness evolves · harness 自身可演化

A harness that cannot learn from its failures will keep failing the same way. Collect signals from real runs and route them back into controlled improvements. (Procedure: M5.)

---

## Priority when principles collide · 冲突时的优先级

```
M0.1 Truth  ≻  M0.2 Trace  ≻  M0.3 Verify  ≻  M0.4 Observe-only
   ≻  M0.5 SSOT  ≻  M0.8 Human-gate  ≻  M0.6 Context  ≻  M0.7 Resumable
   ≻  M0.9 Reversible  ≻  M0.10 Evolvable
```

When two rules conflict, the **lower-numbered** one wins; record the conflict and the resolution (M4, M9).

---

## Checklist

- [ ] Every automated step is classifiable as *observe/record/rank* — none mutates substance.
- [ ] Every externalized fact has a source + access date, or an `unverified` tag.
- [ ] Each task had its acceptance test written *before* work began.
- [ ] A location (or a script) exists to resume each long process from cold.
- [ ] Irreversible actions are gated behind an explicit human decision.

## Anti-patterns

- **Auto-summarize-to-close.** A mechanism rewrites findings so the task looks finished. (Violates M0.4, M0.1.)
- **Confident unverified claims.** Numbers or citations stated without provenance. (Violates M0.2.)
- **"Done" without a test.** Completion asserted from the agent's own impression. (Violates M0.3.)
- **Duplicate sources of truth.** A config in three files that silently disagree. (Violates M0.5.)
- **Context dumping.** Whole files pasted "just in case". (Violates M0.6.)
- **Point-of-no-return autonomy.** An agent pushing/deleting without a gate. (Violates M0.8.)
