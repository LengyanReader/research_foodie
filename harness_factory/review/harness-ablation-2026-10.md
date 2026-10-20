# Harness ablation: what earns its place · 组件消融：什么才配留下

> Where capability is retained, what it causally contributes, and how to prune a harness without guessing.
> 能力留在哪、它到底贡献了什么、以及如何不靠猜地剪掉多余模块。
**Updated:** 2026-10-20

## 0. Why this is its own concern

A harness grows by accretion. Something fails, so a prompt line is added; a tool call misfires, so a check is added;
the task goes badly, so a skill is attached. Nothing is ever removed, because removal has no evidence behind it —
and addition has a story behind it. The result is a system where **module count reads as capability** and nobody can
say which module the capability actually lives in.

This doc grounds clause **M5.12** and the capability `component-ablation`. The claim: a module's place is a
**measurable** question, and the measurement is an *intervention*, not an argument. It also states the limit — an
ablation measures marginal contribution on a task set, which is not the same as understanding the module.

**Method and grading.** This round read both papers **in full** (PDF downloaded, text extracted, method and results
sections read), not at abstract level:

| Source | What it is | Verification |
|---|---|---|
| Luo et al., *Distilling Agentic Systems* (R234, arXiv:2609.36630v1) | 57-page survey: where agent competence is retained | **Full text read** 2026-10-20 |
| Gao et al., *SHarP* (R235, arXiv:2610.04178v1) | 29-page method + experiments on harness pruning | **Full text read** 2026-10-20 |
| `UCSB-NLP-Chang/SHarP` (R236) | Official implementation, MIT, 4 harness adapters | Repo metadata + README fetched |
| WeChat explainer (`mp.weixin.qq.com/s/5S2e3n3…`) | Chinese popular summary of SHarP | **Second-hand — discovery only, never cited** |

---

## 1. What the second-hand summary got right, and what it dropped

The explainer is a good one, and it is still not a source. Comparing it against the paper is the cleanest
demonstration of why the no-laundering rule exists:

- **Kept:** the OpenHands headline (27 modules; 24 pruned; 29.44% → 35.00%), the median-over-ablations baseline, the
  paired t-tests, the protected set, the two symmetric strategies. Its description of the method is accurate.
- **Dropped:** that pruning the *last three* modules collapses the same run to **14.44%** — the single most useful
  fact in the paper for a designer, because it shows the frontier has a cliff and not a slope.
- **Dropped:** that **PaperQA2 is the counter-example** — its full harness is the best configuration, pruning only
  costs accuracy, and one pruned configuration is *more* expensive than the full harness.
- **Dropped:** that the all-pruned baselines for LIFE-harness remain competitive, which reframes the result as
  "these modules were never load-bearing **on these tasks**" rather than "these modules are redundant".

A summary that keeps the wins and drops the cliffs is exactly what a capability library must not ingest. The numbers
below are from the papers.

---

## 2. The ladder: retention, contribution, utility

R234's contribution is a vocabulary that separates three claims which are usually merged into one:

1. **Retention** — what the student/harness actually kept. Where it lives: **in the model**, **as artifacts**
   (prompts, skills, documents, corpora), **through the execution harness** (tools, control flow, verification), or
   **across substrates** (distributed over several).
2. **Causal contribution** — does the retained thing *cause* the improvement, or merely co-occur with it?
3. **Deployed utility** — does the improvement survive in the place it will actually run?

Why the middle rung matters: R234's benchmark table shows, for several widely used agent benchmarks, that **model, tool
and harness effects are confounded** — the row for APIBank says so in as many words. A benchmark can show that a
configuration works; it cannot tell you that the *tool* did it rather than the model behind it. Its recommendation is the
one this library adopts: **functional interventions and budget-matched execution** alongside any structural metric — and
"a reference topology is not automatically a ground truth: several graphs may realize equivalent control."

The same survey's evaluation section is unusually blunt about reporting: stochastic agents need repeated runs, paired
seeds, task-level frequencies, dispersion and intervals, and **category-level results beside macro and micro
averages** so that frequent easy tasks do not drown rare or safety-critical ones. "Component and synergy estimates use
the same paired task instances to reduce variance." And a scalar leaderboard score is meaningful **only** under fixed
weights and a fixed protocol.

For this repository, R234 is also external corroboration of its own thesis: if competence is retained in artifacts and
harnesses, not only in weights, then **the harness is a legitimate object of engineering** — which is the premise of
every module in `core/`.

---

## 3. The method: four steps, four decisions that matter

R235 (SHarP) adapts neural-network pruning to harnesses. The pipeline is four steps; the interesting content is in
the four decisions that make it work.

**Step 1 — Module identification (manual, by implementation boundary).** Harnesses have no predefined pruning units,
so the authors *manually* partition each one: a registered tool, an instruction block identified by its heading or
tags, a retrieved skill, a distinct processing mechanism. **Highly coupled elements — a tool and its usage
instructions — become one module.** For each module they must also define what "pruned" means operationally: removing
a search tool means removing the tool *and* its instructions *and* disabling access, not just deleting a line; pruning
a history-summarisation mechanism means always keeping the full history.

*Decision 1: the unit is the coupled functional unit, and "removed" must be defined per module.* A pruning unit that
cannot be described as a counterfactual ("with this off, the harness does X instead") is not a unit.

**Step 2 — Saliency by single-module ablation, against a robust baseline.** For module *i*, run the harness with only
*i* disabled over *n* development tasks, recording per-task score *y* and token cost *c*. The comparison baseline is
**not the full harness** — it is, per task, the **median across all single-module-ablated runs**. Two difference terms
follow: performance (score minus that median) and token (cost minus that median). Then **one-sided paired t-tests**
per module give two p-values: *performance saliency* and *efficiency saliency*.

*Decision 2: the baseline is the median over ablations, not the full harness.* The full harness is a single noisy
draw; if it happens to over- or under-perform on a task, every module's estimate is distorted in the same direction.
The median over *m* ablations is a stable reference within the same task. Cost of the whole procedure: **one extra
evaluation per module**, which is what makes it affordable at all.

**Step 3 — Protected set, then rank the rest.** For efficiency-oriented pruning, the protected set is
`G = {i : p_perf(i) ≤ 0.05}` — modules whose removal significantly hurts performance. The unprotected modules are
ranked by *efficiency* p-value and pruned greedily from the most expensive end, producing a ladder of configurations
from the full harness down to `|G|`. Performance-oriented pruning is the exact mirror image.

*Decision 3: the two dimensions are never merged into one score.* They answer different questions ("is it
load-bearing?" and "is it costing me?") and a weighted sum would hide which one moved. Protect on one axis, order on
the other.

**Step 4 — Evaluate the ladder on held-out data, with repeats.** Every configuration is evaluated on a validation set
**disjoint** from the development set, under matched conditions, three trials per task by default, reporting task
performance and token cost plus the **Pareto frontier**.

*Decision 4: report the frontier, not a winner.* The frontier makes the trade-off visible; the single best
configuration is a policy choice that depends on how much a token costs *you*.

---

## 4. What the measurements actually show

Five settings, four harnesses, one model (Qwen3.5-122B-A10B throughout), 50 development tasks per setting — except the
airline domain, which uses all 30 available training tasks, and retail, where 48 of the 50 are evaluable after two
unparseable outputs are excluded. Each ablation is run once per development task; the ladder gets R = 3 trials.

| Setting | Modules | Result |
|---|---|---|
| OpenHands / GAIA | 27 | Best at **24 pruned**: 29.44% → **35.00%**. All 27 pruned: **14.44%** |
| JIT agentfold / DeepPlanning-Shopping | 23 | Several smaller configurations match performance at lower cost; all-pruned is *more* expensive |
| LIFE-harness / τ²-bench airline | 44 | All-pruned remains competitive; modest decrease |
| LIFE-harness / τ²-bench retail | 48 | All-pruned *slightly better*; efficiency-oriented S43 reaches 87.5% |
| PaperQA2 / LitQA2 | 18 | **Full harness is best**; 15-pruned is more expensive than full |

Summary line from the paper: all four harnesses hold comparable performance while cutting **at least 10%** of token
cost, and two *improve* performance while cutting cost. The strategy comparison on DeepPlanning shows the two
strategies are not interchangeable: performance-oriented pruning reaches 82.5% match rate at −5.9% tokens, while
efficiency-oriented reaches 76.2% at −39.0% tokens — same saliency estimates, different policy.

**Three findings that cut against the obvious reading:**

- **Removing a module can *increase* cost.** The paper's motivating example: remove the mechanism that recognises task
  completion and the agent keeps calling the model after the task is done. So "fewer modules, cheaper" is false, and
  the two axes genuinely have to be measured.
- **Redundancy is not universal.** PaperQA2 is a literature-QA harness whose modules all pull weight; the OpenHands
  result does not generalise to it. Any library rule of the form "harnesses are ~90% redundant" would be a
  superstition built on one benchmark.
- **The all-pruned baseline is a statement about the task set.** When a harness with *every* optional module removed
  still scores competitively, the honest reading is that **those tasks did not exercise those modules** — not that the
  modules are worthless. This is the single most misreadable result in the paper and the reason M5.12 requires the
  task set to be named alongside the verdict.

---

## 5. What this changes here

The library already had `eval-driven-development` (re-score a change) and M5.10 (a round must close). Neither said
anything about **removing**, and neither separated "present" from "contributing". Hence:

1. **Clause M5.12** — a module earns its place by an intervention, not by an argument; the two axes are measured
   separately; the baseline is the median over ablations; the verdict names the task set; and the ablation is kept as
   a repeatable test, not a one-off script.
2. **Capability `component-ablation`** — fires when there are rounds to amortise the cost *and* a measurable score
   (multi-session × high verifiability). Without a score there is nothing to ablate against; within one session there
   is no harness to prune.
3. **The audit's own reading** — `harness cycle audit` reports missing router rows, guards and provenance, which is
   a *structural* criticism of this repository's harness. It cannot say whether a clause or capability is
   *load-bearing*. M5.12 names that gap honestly instead of pretending the audit covers it.

**Deliberate non-additions**, with reasons and revisit triggers:

- **No `harness-pruning` domain.** Pruning is a procedure over an existing harness, not a field of work; a domain
  would route by topic, which is the error the router's rule warns against.
- **No automatic pruner in the CLI.** The partitioning step is manual by construction (R235 does it manually too), so
  an automated pruner would only automate the part that was never the bottleneck. Revisit if module boundaries become
  declared in `data/`, at which point the ablation loop could be driven from the manifest.
- **No "redundancy ratio" metric for this repository.** The observable is task score, which this repo does not have
  for its own harness. A ratio computed from document counts would be exactly the proxy that Goodhart's law eats
  (M5.12, R216).

---

## 6. Limits, stated plainly

- **Marginal, not joint.** Single-module ablation bounds each module's marginal contribution *given the rest*; modules
  that substitute for each other will each look dispensable and be pruned together. R234's "component and synergy
  estimates on the same paired instances" is the direction of the fix, not a solved problem.
- **Task-set-relative.** Every verdict is conditional on the development and validation sets; the paper takes 50
  development tasks per setting (30 for airline, 48 evaluable for retail) and follows official splits where they exist.
- **One model.** All five settings use one base model. A module's saliency can plausibly move with the model; the paper
  does not test that, so neither does this doc.
- **n is small.** 50 dev tasks, and 30 for the airline domain. The paired t-test is doing real work here, and its
  assumptions (per-task differences, approximate normality of the mean difference) are worth checking before quoting a
  p-value near 0.05.
- **Ablation is not explanation.** Knowing that a module is load-bearing does not tell you *why*; it tells you where to
  look next.

## Checklist

- [ ] Each module is a coupled functional unit, and "removed" is defined for it as a counterfactual.
- [ ] The baseline is the per-task median over ablations, not the single full-harness run.
- [ ] Performance and cost are reported as two axes, never one weighted score.
- [ ] The protected set is derived from significance on the *other* axis, and pruning stops at its size.
- [ ] Evaluation is on a held-out set disjoint from the development set, with repeats.
- [ ] The verdict names the task set, the model and the number of development tasks.
- [ ] The all-pruned baseline is reported, and read as a statement about task coverage.
- [ ] The ablation lives in the test suite, so the next round cannot silently re-add what was pruned.
- [ ] Non-monotonic cost is expected: a removed module may raise spend.

## See also

`../core/06-self-evolution.md` (M5.10 round contract, M5.12 this clause) · `../core/04-verification-and-gates.md`
(M3 gates, holdout discipline) · `../reference/capability-cycle.md` (how a round closes) ·
`self-model-and-gap-seeking-2026-10.md` (why a self-report needs an external check) · R234–R236 in `references.md` §S.
