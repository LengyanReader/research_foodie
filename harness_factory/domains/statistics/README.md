# Domain · Statistics · 统计域
> Wiring `core/` modules into an inferential claim that states its frame: declared model, convergence-checked computation, and intervals rather than point verdicts.
> 把 `core/` 模块接线成「框架先说清、模型先写明、算完要查收敛、回答给区间」的推断流程，而不是给出一个点值或一个 p 值。
**Updated:** 2026-10-18

---

## 中文速览
统计域的目标是**让「不确定」变成可核对的对象**：先固定**估计量/问题**与**推断框架**（频率派或贝叶斯）（M0/M1）；写明**模型**——似然、先验、以及它们编码的假设（M4）；拟合或采样后**检查诊断**（收敛、有效样本量）（M3）；把结论表达为**区间/可信区间**而非点或 p 值（M3）；再做**稳健性**（先验/似然/纳入选择）与**模型检验**（后验预测、敏感性）（M3/M4）；最后连同假设一起报告（M7）。域特有风险：**p 值当结论**、**不看收敛就报数**、**先验/模型隐式默认**、**多重比较不校正**、**把探索性分析写成验证性结论**。

---

## What this domain is for · 用途
Produce an estimate a skeptical reader can re-derive: the question and the inferential frame named, the model and its assumptions explicit, the computation shown to have converged, and the answer given as an interval you can defend. Covers applied statistics, Bayesian inference, regression and hierarchical models, and the statistical side of any empirical field.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Fix the estimand & frame | M0, M1 | frequentist or Bayesian; what quantity is being estimated |
| L1 | State the model | M1, M4 | likelihood, priors, assumptions each carries |
| L2 | Fit / sample | M3, M6 | the sampler/estimator and its settings, recorded |
| L3 | Diagnostics (gate) | M3 | convergence (R-hat, ESS), not an eyeballed trace |
| L4 | Uncertainty & robustness | M3, M4 | interval / credible interval; prior & likelihood sensitivity |
| L5 | Report | M7, M4 | estimate + interval + assumptions; exploratory vs confirmatory |

## Module combination · 模块组合
- **M0** — a number from a model is a claim about the model; say which model.
- **M1** — load the estimand, the design, and the analysis plan; a frame is not a default.
- **M2** — long chains/simulations checkpoint; a non-converging sampler is a loop to diagnose, not to hide.
- **M3** — the gate is convergence + an interval; a p-value alone is a **failed** statistical claim.
- **M4** — priors, likelihood, and exclusions are provenance: each choice is recorded, not implicit.
- **M6** — the toolkit is an instrument: pin versions; IRT/MCMC/INLA results travel with their settings.
- **M7** — "significant" is a governance claim; publication requires the interval and the diagnostics.

## Instruments · 仪器
Concrete tools for L2–L4 (catalog ids; full map: `../reference/evidence-instruments.md#statistical-estimates--causal-claims`):
- **Bayesian / probabilistic programming** — `pymc` · `numpyro` · `brms` · `r-inla` · `emcee` · `stan`.
- **Diagnostics & comparison** — `arviz` (R-hat, ESS, posterior predictive checks, model comparison).
- **General statistical environment** — `r-project` (the applied-statistics reference); `statsmodels` / `lme4` from the empirical row.
- **Causal effect (not correlation)** — `dowhy` (model → identify → estimate → refute); identification is the causal problem, estimation is secondary.
- **Gate evidence** — declared frame, stated model & priors, **R-hat/ESS reported**, and an interval. Sources: `[R111]` (Bayesian workflow), `[R112]` (rank-normalised R-hat).

## Methodology · 方法论
- **Bayesian workflow** `[R111]` — prior → model → compute → validate → compare → revise, *iteratively*: model checking and prior sensitivity are part of the claim, not an appendix.
- **Frequentist design** — pre-specified analysis, power, multiplicity control; an unregistered analysis is exploratory until labelled otherwise.
- **Causal identification** — name the assumption (back-door / IV / DiD / RD) and try to falsify it; a coefficient's significance is not identification.
- Full field → method → "what the harness must enforce" map: `../reference/methodology-map.md` (M3.13).

## Discipline-specific risks · 领域特有风险
- **p-value as the result** (no effect size, no interval).
- **Convergence-by-eyeball** (declaring a sampler converged from a trace plot; R-hat/ESS never checked).
- **Implicit priors / model** (a default that encodes a strong assumption, unstated).
- **Multiplicity ignored** (many comparisons, one unadjusted p).
- **Exploration sold as confirmation** (the hypothesis that survived the data is reported as if pre-specified).
- **Causal language from observational fit** ("predicts" rewritten as "causes").

## See also
`../mathematics/README.md` (exact derivation) · `../core/04-verification-and-gates.md` (M3.11) · `../reference/evidence-instruments.md` · `../reference/methodology-map.md` · `../review/integration-map-2026-10.md`.
