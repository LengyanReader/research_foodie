# M3 · Verification & Gates · 验证与门禁
> Deciding "done" — with evidence, not feelings.
> 判定「完成」——靠证据，不靠感觉。
**Updated:** 2026-10-12

---

## 中文速览
「完成」是一个**被验证的状态**，不是一种感觉。M3 的核心动作：**开工前写下验收测试**；**构建者与评判者分离**（换一个全新上下文、无写权限的评估者）；**默认失败 + 证据门**（每条标准初始为 false，必须给出观察到的证据才能置真）；区分**硬门**（机械可判、必须过）与**软门**（需人类判断）；允许**三态**判定（通过/失败/不确定）与**弃权**，避免被迫二选一。上游：M0.3（先验证再称完成）、M0.1。下游：M5（用验证结果做演化信号）、M8（人类门）。

---

## The problem · 问题
Generators are optimistic and self-grading is biased. If the same context that produced an answer also grades it, "done" converges on "plausible." Verification must be **independent**, **evidence-based**, and **defined before the work starts**.

## Patterns · 模式

1. **Define done before work.** Write the acceptance test first. Vague criteria produce vague passes; granular criteria produce granular critiques.
2. **Separate builder from critic (M0.3).** Grade with a *fresh context* and *no write tools*; the evaluator sees only the artifact, not the author's reasoning. Same model can play both roles — in different windows.
3. **Default-FAIL contract.** Every criterion starts `false`. The agent may set it `true` only after **observing evidence** (a test result, a screenshot, a file, a log line). A hook denies a passing write without evidence.
4. **Hard gates vs soft gates.** Hard gates are mechanical and must pass (build, tests, schema, hash, citation format). Soft gates require human judgment (taste, relevance, ethical fit) and are explicitly marked human-gated (M0.8).
5. **Verify the verifier.** Periodically check the checker against known-good and known-bad inputs; a gate that always passes is no gate.
6. **Three-state judging + abstain.** Allow `pass` / `fail` / `uncertain`, and an explicit *abstain*. Forcing binary choice on genuinely ambiguous work manufactures false confidence.
7. **The refinement loop.** Iterate: produce → evaluate against criteria → revise → re-evaluate, until the gate passes or the budget ends. Log each cycle.
8. **Calibrate confidence.** Require the judge to state confidence and the evidence it used; track calibration over time.
9. **Evidence over assertion (M0.4).** No mechanism may mark a task complete by rewriting output to *look* complete. Evidence is a first-class artifact.

> **中文**：先定义完成；构建者≠评判者（新窗口、无写权限）；默认失败+证据门；硬门/软门分离；验证「验证器」；三态+弃权；精炼循环；置信度校准；证据 > 断言。

## Checklist
- [ ] Acceptance test written before work began.
- [ ] The evaluator runs in a fresh context with no write access.
- [ ] Criteria start `false`; evidence is required to pass each.
- [ ] Hard vs soft gates labeled; soft gates human-gated.
- [ ] The verifier itself is spot-checked against known cases.
- [ ] Ambiguity can be marked `uncertain`/abstained, not forced to pass.

## Anti-patterns
- **Self-grading in the same context.** Author's bias leaks into the verdict.
- **Done-by-feeling.** No test, no evidence.
- **All-green forever.** A gate that never fails (unverified verifier).
- **Binary coercion.** Forcing pass/fail on genuinely ambiguous work.
- **Rewriting to pass.** Mutating the artifact to satisfy the gate (M0.4).

## See also
`01-meta-principles.md` (M0.3, M0.1, M0.4) · `04-verification-and-gates.md` (this) compared with `06-self-evolution.md` (M5) · `09-collaboration-and-sessions.md` (M8).
