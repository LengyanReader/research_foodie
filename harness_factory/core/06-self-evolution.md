# M5 · Self-Evolution · 自演化
> Making the harness improve itself — signal → audit → mutation → journal, human-gated.
> 让 harness 自我改进——信号 → 审计 → 变异 → 日志，人类把关。
**Updated:** 2026-10-20

---

## 中文速览
一个不能从失败中学习的 harness 会以同样方式反复失败（M0.10）。M5 定义**受控的自我改进回路**：**信号**（真实运行中的失败/低效）→ **审计**（可否泛化？是否一次性？）→ **变异**（受控地改动 harness 自身）→ **日志**（可回滚、可归因）。变异类型：Promote / Register / Deepen / Fission / Archive / Consolidate。**全部人类把关**（M0.8）；用留出集衡量是否真变好；警惕**误演化**（reward hacking、目标漂移）。AI 侧的对应工作谱系（Self-Refine/Reflexion、ADAS、Gödel Agent、FunSearch/AlphaEvolve/OpenEvolve、SEAL、Voyager）见 `review/harness-catalog.md` §3。上游：M0.10、M0.4。下游：M7（变更治理）。

**循环层面另有契约（M5.10）**：一次能力拓展 / 深化 / 更新 / 演化即一个**轮次**，须登记于 `data/cycles.json`，并按**完成定义**（子句 · 判别力 · 门禁 · 溯源 · 路由 · 可达）逐项过关；**有意不做**的事须登记为带**理由**与**重访触发条件**的路线图条目。`harness cycle audit` 同时报告**硬问题**与剩余**缺口面**——后者就是下一轮的输入，故循环可持续而非偶发。过程见 `reference/capability-cycle.md`。

**自知之明的契约（M5.11）**：回路假定 harness 知道自己**缺什么**，而这本身是个主张。三件产物：**自我模型**（每条能力指向能证伪它的证据——守卫测试 / 已交付文件 / 实测运行）、**缺口登记册**（`cycle audit` 的机械面 **+** 带理由与重访触发的路线图条目）、以及每轮一次的**反证检查**（挑一个自称的强项，故意去打碎它）。依据是不对称：自我报告便宜且不可靠，外部检验昂贵但决定性——无外部反馈的自我纠错甚至会变差（`arXiv:2310.01798`），校准很差（`arXiv:1706.04599`），模型只掌握部分知识边界（`arXiv:2207.05221`/`2305.18153`）。**探索有界**：留出集、预算、书面停止条件；**新颖不等于价值**，未覆盖方向只能作为候选，仍须过本轮完成定义。前沿的「自我改进 agent」细读之下都是**搜索 + 一个可信的评估器**——所以钱要花在评估与溯源上。

**组件消融（M5.12）**：回路只**加**不减，模块数于是被误读为能力。对冲办法：**留下的组件必须扛过一次干预**。**留存 ≠ 贡献**——模块在成功时在场，不能说明它促成了成功；agent 基准里模型、产物、harness 的效应通常**混杂**（`arXiv:2609.36630`）。做法：按实现边界切成**耦合功能单元**（工具与其使用说明算一个），为每个单元定义「移除」的反事实，**一次只摘一个**；基准取**同一任务上全部消融的中位数**，而不是那一次完整 harness 运行（单次运行只是一个噪声样本）；**性能与 token 两轴分报**，各做单侧配对检验，绝不并成一个加权分；显著伤害红线者进**保护集**，其余按另一轴排序，在**留出集**上重复评估，报 **Pareto 前沿**而非单一赢家。要预期**非单调**：摘掉「判断任务完成」的机制反而**更贵**（agent 会继续调用）。全剪枝基线仍能得分，说明的是**任务覆盖**不够，不是模块无用。消融要留在测试里，否则下一轮又把剪掉的加回来。注意 `cycle audit` 只查结构（缺行·缺守卫·缺溯源），它无法判断某条子句是否承重——这条子句才是那个测量（`arXiv:2610.04178`，代码 `github.com/UCSB-NLP-Chang/SHarP`）。

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

11. **Know your own edges (M5.11).** The loop above assumes the harness can tell *what it is missing*; that is a separate claim and needs its own discipline. Three artefacts: (a) a **self-model** — what the harness covers, each claim paired with the evidence that supports it (a guard test, a shipped file, a measured run), never a self-attributed strength; (b) a **gap register** in two halves — the `cycle audit` surface (mechanical: missing rows, guards, provenance) *and* the roadmap entries that record uncovered directions with a reason and a revisit trigger (M5.10); (c) a **disconfirming check** — once per round, pick a claimed strength and try to *falsify* it, not confirm it. The reason is an asymmetry, not modesty: self-report is cheap and unreliable while an external check is decisive. Verbalised confidence is poorly calibrated `[R202]`, and a model asked to correct itself with no external feedback often makes the answer worse `[R201]`; models hold only a partial map of what they know `[R203]`, `[R204]`, and introspection recovers some facts about themselves, not all `[R205]`. So a self-attributed strength is admissible only with an external check, and disagreement between self-assessment and check routes to the check (sampling agreement is a cheap *router* signal, not a verdict `[R207]`). Exploration is **bounded**: a holdout, a budget, a written stop condition, and the rule that novelty is not value — an uncovered direction is a **candidate**, and adoption still clears this round's definition-of-done (M5.10). Open-ended search works by keeping diversity rather than chasing one optimum `[R208]`, `[R209]`, and a direction is interesting when it yields learnable structure, not when it is merely unfamiliar `[R210]`, `[R211]`; which question deserves the next unit of budget is a decision, not a hunch `[R217]`. The frontier's "self-improving agents" are, read closely, **search plus a trusted evaluator** `[R212]`, `[R213]`, `[R214]` — so the investment belongs in evaluation and provenance (M3, M4), not in introspection. Full treatment: [`../review/self-model-and-gap-seeking-2026-10.md`](../review/self-model-and-gap-seeking-2026-10.md).

12. **A module earns its place by ablation (M5.12).** The loop above only *adds* - signal, audit, mutation - so left alone it grows monotonically until module count reads as capability. The counterweight: **what is in the harness must survive an intervention.** Retention is not contribution; that a module is present when the task succeeds says nothing about whether it caused the success, and in agent benchmarks the model, artifact and harness effects are often **confounded** `[R234]`. So measure it. Partition the harness into **coupled functional units** at implementation boundaries - a tool and its usage instructions are one unit - and define what "removed" means for each as a **counterfactual** ("with this off, the harness does X instead"), because a unit whose removal cannot be described is not a unit `[R235]`. Ablate **one unit at a time** and compare against the **median over all ablations on the same task**, never against the single full-harness run: the full run is one noisy draw, and using it as the baseline distorts every estimate in the same direction `[R235]`. Report **two** axes - performance and token cost - as two one-sided paired tests, and never merge them into one weighted score: they answer different questions and a sum hides which one moved. Protect the units whose removal significantly hurts the red line, rank the rest by the other axis, evaluate the ladder on a **held-out** set with repeats, and report the **Pareto frontier** rather than a winner - the winner is a policy choice about what a token costs *you*. Expect **non-monotonicity**: removing a unit can **raise** cost, because the unit that recognises task completion is also the one that stops the model calling itself `[R235]`. Read the all-pruned baseline correctly: if a harness with every optional unit removed still scores, the finding is about **task coverage**, not about the units. Keep the ablation in the test suite, or next round re-adds what this round pruned. Note what this is *not*: `harness cycle audit` reports missing rows, guards and provenance - a **structural** criticism. It cannot say whether a clause is load-bearing, and this clause is the measurement that can.

## Checklist
- [ ] Signals come from real runs, not speculation.
- [ ] Each mutation passes an audit (pattern? generalizes? M0-consistent?).
- [ ] Mutations are typed, minimal, and journale with a rollback path.
- [ ] Improvement is measured on a holdout, not the tuning set.
- [ ] Substantive mutations are human-gated.
- [ ] The round is in `data/cycles.json` and passes `harness cycle audit`; its non-additions carry a reason and a revisit trigger (M5.10).
- [ ] Each claimed strength names its evidence, and one of them was **attacked** this round rather than confirmed (M5.11).
- [ ] Exploration is bounded (holdout, budget, stop condition) and no self-report was accepted as a sign-off (M5.11).
- [ ] Each harness module is a coupled functional unit whose removal is defined as a counterfactual (M5.12).
- [ ] The ablation baseline is the per-task median over ablations, not the full-harness run (M5.12).
- [ ] Performance and cost were reported as two axes, never one weighted score (M5.12).
- [ ] The protected set came from significance on the *other* axis, and pruning stopped at its size (M5.12).
- [ ] The verdict names the task set, the model and the development-set size; the all-pruned baseline was read as task coverage (M5.12).
- [ ] The ablation lives in the test suite, so the next round cannot silently re-add what was pruned (M5.12).

## Anti-patterns
- **Unbounded self-modification.** The harness rewrites itself with no audit or gate.
- **Overfit promotion.** A fix for one instance becomes a global rule.
- **Metric-free promotion.** "Feels better" without a measured gain.
- **Silent mutation.** Changes with no journal entry and no way back.
- **Capability without safety.** Raising power while relaxing containment.
- **Round without closure.** A cycle opens, produces good prose, and is never marked done or audited — so the same gap is rediscovered next time.
- **Silent deferral.** A capability that was deliberately *not* added is dropped without a reason or a revisit trigger, and the decision evaporates.
- **Self-report as sign-off.** "The harness handles X" because a doc says so; no guard, no run, no external check (M5.11).
- **Novelty-as-value.** Adopting a direction because it is uncovered rather than because it would change an outcome (M5.11).
- **Unbounded exploration.** Probing new scope with no budget, holdout or stop condition — the acquisition of capability the harness cannot verify.
- **Monotone growth.** Every failure adds a module, none is ever removed; the harness becomes an archaeology of past incidents (M5.12).
- **Module count as capability.** "We have 40 skills" offered as a claim about strength (M5.12).
- **Argument-by-plausibility.** Keeping a unit because a story can be told about why it helps, with no intervention behind it (M5.12).
- **Baseline by memory.** Comparing a pruned configuration against one remembered run of the full harness (M5.12).
- **One blended score.** A weighted sum of quality and cost that hides which one moved (M5.12).
- **Redundancy universalism.** Generalising "harnesses are mostly redundant" from one benchmark to every harness; the literature's own counter-example is a retrieval harness whose every module pulls weight (M5.12).
- **All-pruned misreading.** Concluding a module is worthless because the task set never exercised it (M5.12).
- **Ablation as ritual.** Running the ablation, then restoring every module "to be safe" — the measurement changed no decision (M5.12).

## See also
`01-meta-principles.md` (M0.10, M0.4, M0.8) · `../review/harness-catalog.md` §3, §8 · `08-change-governance.md` (M7) · `04-verification-and-gates.md` (M3) · `../reference/capability-cycle.md` (how to run a round; `harness cycle`) · `../review/self-model-and-gap-seeking-2026-10.md` (M5.11 — self-model, gap register, bounded exploration) · `../review/harness-ablation-2026-10.md` (M5.12 — retention vs contribution, the ablation procedure, its limits).
