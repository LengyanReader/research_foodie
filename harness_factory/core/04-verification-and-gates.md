# M3 · Verification & Gates · 验证与门禁
> Deciding "done" — with evidence, not feelings.
> 判定「完成」——靠证据，不靠感觉。
**Updated:** 2026-10-18

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
10. **Match the instrument to the claim (M3.10).** Verify with the instrument that can *refute* it: a **machine-checked derivation** for formal results (proof assistant, checked model, SAT/SMT counterexample); **units, dimensional consistency and error propagation** for physical quantities; **effect sizes with intervals plus a reliability coefficient** for empirical measurements. Prose agreement is evidence for none of the three - reading it and nodding is not a gate. The concrete **claim → instrument → catalogued tool → gate evidence** map is `reference/evidence-instruments.md`; an emitted harness states its own instrument in the *Evidence instrument* section of `AGENTS.md`.
11. **Declare the inferential frame (M3.11).** A statistical claim is a claim about a *model*, not about the data: name the frame (frequentist or Bayesian), state the likelihood/priors and the assumptions they encode, and check the computation actually converged (R-hat and effective sample size for MCMC - not eyeballed traces). Report the estimate as an **interval / credible interval**; a p-value or a point estimate alone is not the result. Sources: `[R111]` (Bayesian workflow), `[R112]` (rank-normalised R-hat).
12. **Certify the computation (M3.12).** When the claim rests on a *computed* invariant (an algebraic normal form, a homology group, a knot polynomial, a triangulation's property), the algorithm is part of the evidence: run it under exact or certified arithmetic (or record the precision), handle degeneracies explicitly instead of inheriting floating-point noise, and **re-derive the result independently** or on a perturbed input. An unchecked CAS/solver output is a conjecture. `[R114]` (interval arithmetic).
13. **Declare the method and its assumptions (M3.13).** Before executing, name the **method** (the procedure), the *assumptions* it licenses, and where it stops being valid - the design, review, or analysis methodology the field expects, not a generic recipe. A method whose assumptions are unmet does not transfer: a systematic review without a registered protocol, a causal claim without an identification strategy, a qualitative coding without a codebook and double-coding, a trial without its reporting standard. The field → methodology-system → "what the harness must enforce" map is `reference/methodology-map.md`.

> **中文**：先定义完成；构建者≠评判者（新窗口、无写权限）；默认失败+证据门；硬门/软门分离；验证「验证器」；三态+弃权；精炼循环；置信度校准；证据 > 断言；**按主张选仪器**——形式命题用机器可核验的推导（证明助手/模型检验/SAT 反例），物理量用量纲一致与误差传递，实证主张用效应量+区间+信度系数；「读一遍觉得对」不是门。此外：**统计主张**要声明推断框架、模型与先验、收敛诊断，并以区间而非点或 p 值作答；**计算得到的量**（代数标准形、同调群、纽结多项式）要么精确/带界算，要么独立重算，未核验的 CAS 输出只是猜想；**方法**要连同其假设与失效边界一起声明——方法假设不成立就不迁移（无注册方案的综述、无识别策略的因果主张、无编码手册与双编码的质性研究，都不算完成）。

## Checklist
- [ ] Acceptance test written before work began.
- [ ] The evaluator runs in a fresh context with no write access.
- [ ] Criteria start `false`; evidence is required to pass each.
- [ ] Hard vs soft gates labeled; soft gates human-gated.
- [ ] The verifier itself is spot-checked against known cases.
- [ ] Ambiguity can be marked `uncertain`/abstained, not forced to pass.
- [ ] The instrument matches the claim (formal proof / units & error / effect size & reliability).
- [ ] The inferential frame, model/priors and convergence diagnostics are stated; the answer is an interval (M3.11).
- [ ] A computed invariant is exact/certified and independently re-derived, not a raw solver output (M3.12).
- [ ] The method, its assumptions and its validity boundary are declared before work (M3.13).

## Anti-patterns
- **Self-grading in the same context.** Author's bias leaks into the verdict.
- **Done-by-feeling.** No test, no evidence.
- **All-green forever.** A gate that never fails (unverified verifier).
- **Binary coercion.** Forcing pass/fail on genuinely ambiguous work.
- **Rewriting to pass.** Mutating the artifact to satisfy the gate (M0.4).
- **Unit-free numbers and p-only claims.** A quantity with no unit/error, or a result with a p-value and no effect size or reliability.
- **Convergence-by-eyeball.** Declaring a sampler "converged" from a trace plot, or reporting a point estimate from a model whose R-hat/ESS were never checked.
- **Floating-point geometry.** Trusting an unstabilised predicate or an unchecked CAS output as if the computation were the proof.
- **Method-by-vibes.** Applying a named method (PRISMA, DiD, grounded theory, design science) without its protocol, assumptions, or reporting standard.

## See also
`01-meta-principles.md` (M0.3, M0.1, M0.4) · `04-verification-and-gates.md` (this) compared with `06-self-evolution.md` (M5) · `09-collaboration-and-sessions.md` (M8).
