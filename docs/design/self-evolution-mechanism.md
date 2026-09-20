# Self-Evolution Mechanism — Research, Argument & Evaluation (工具自我演化机制：调研·论证·评估)

> **中文速览**
> 本文档回答一个问题：**"让 research_foodie 自我演化"在 2026 年做什么、不做做什么、以及为什么。**调查了一手证据（arXiv/官方文档，2026-09-20 核证），核心结论：
> 1. **自我演化 ≠ 让模型自己改自己。** 已有强证据：LLM 的"内在自校正"在推理上几乎无效甚至有害（Huang et al. 2023a；GPT-4 发现逻辑错误仅 52.9%）；真正有效的自修**必须依赖外部信号**（执行反馈、单元测试、判题器）。→ 我们的演化触发源必须是**外部测量**（判题/接地门/变异注入），绝不靠"让模型再想想"。
> 2. **可借鉴的正确范式**：自演化 LLM 的四相循环（**经验获取→经验精炼→更新→评估**，Tao et al. 2024）；**提示级（token 空间）演化**而非权重更新（Reflexion、Voyager 技能库）；**指标门控的程序化提示优化**（DSPy、GEPA——GEPA 用 678 次 rollout 胜过 GRPO 的 24,000 次，且仅需文本反馈）——但 GEPA 需要强反射模型（Phase R）；**持续评测/漂移窗口**（Evidently/promptfoo/WhyLabs 的"参考集 vs 当前集"快照门禁）；**变异测试**加固机械门（mutmut）。
> 3. **必须设防的失败模式**：**模型坍缩**（递归吃自生成数据会让分布尾消失；混入真实数据可避免——Seddik et al. 2024 给出界）→ 反馈语料必须锚定一手真实证据并带来源标签；**判题噪声**（我们实测 P-A ±0.53）→ 演化阈值必须方差感知（先做 judge 中位数）。诚实边界：本地做"调度测量 + 回归检测 + 人工在环修复 + 版本化反馈"；不做自动改码、不自动 commit、不改权重、不做无人值守 prompt 演化。

- `Updated`: 2026-09-20
- `Status`: design/analysis, evidence verified 2026-09-20 against arXiv / official docs
- `Companions`: `docs/PLAN.md §8 Phase X` (the executable plan) · `docs/TOOL-COMPARISON.md` (stage reuse lane) · AGENTS.md (governance, no unsolicited commits)

---

## 1. Problem framing / 问题界定

What the repo currently has (measured): a deterministic L6 gate (verbatim 5-gram grounding, zero LLM), a 4-axis AI judge (matrix v1), mock regression 34/34, a QA panel n=31, pools 22/30, and **measured judge variance P-A 3.88±0.53**. What "self-evolution" should mean here is therefore not "get smarter weights" (we don't train; cost-zero is a stated invariant) but:

> Keep the pipeline's *measured* capability from silently decaying (model/backend/tooling drift), and let accumulated evidence **bump versioned prompts/judges/configs** — behind a human gate.

Self-evolution is only as trustworthy as its feedback signal. The rest of this document argues what that signal can/cannot be.

## 2. What fails: intrinsic self-correction / 会失败的方案：内在自校正

- **Huang et al. 2023a (arXiv:2310.01798, "Large Language Models Cannot Self-Correct Reasoning Yet")** — *intrinsic* self-correction (model reviews its own output, no external feedback): on GSM8K the model keeps its first answer 74.7% of the time, and when it does change, correct→incorrect happens more often than incorrect→correct; reported improvements in the literature come from *oracle/external* feedback, and vanish when the labels are removed. Multi-agent debate adds no advantage over self-consistency at equal compute.
- **Tyen et al. 2023 (arXiv:2311.08516, "LLMs cannot find reasoning errors, but can correct them!" + BIG-Bench Mistake)** — decomposes self-correction into *mistake finding* vs *output correction*; state-of-the-art GPT-4 correctly locates a logical mistake only **52.87%** (direct step-level prompting) even on unambiguous cases, while correction *given* the mistake works well.

**Direct implication (design rule #1): never rely on a model (judge, writer, or agent) diagnosing its own errors on stale output.** The evolution loop must be driven by:
- deterministic mechanical signals (our L6 gate), and
- adversarial/external difficulty (mutation of inputs — §5), and
- measurements from a *different* vantage than what produced the artifact (judge on manuscript, gold tokens on QA).

Evidence that external signals work (so the loop has a safe engine):
- **Self-Debugging (Chen et al. 2023/ICLR 2024, arXiv:2304.05128)** — giving the model *execution feedback* (unit-test pass/fail + error) improves code up to **+12%**; without tests, "rubber-duck" self-explanation still gives +2–3% but far less. External testable ground truth is the lever.
- **"Revisit Self-Debugging with Self-Generated Tests" (ACL 2025, arXiv:2501.12793)** — *self-generated* tests help but are noisy/weak vs gold tests. → our equivalent: **gold** (parsed paper text, gold_tokens) must stay the reference; model-generated mutation is a supplement, never the ground truth.

## 3. What works: the canonical self-evolution cycle / 可借鉴范式：四相循环

Tao et al. 2024 (**arXiv:2404.14387**) formalize self-evolution of LLMs as iterative cycles of **experience acquisition → experience refinement → updating → evaluation**; Gao et al. 2025 (**arXiv:2507.21046**, self-evolving agents survey) adds *what/when/how* to evolve, intra- vs inter-test-time stages, and feedback types (scalar reward vs textual feedback). These map 1:1 onto our repo:

| Phase | Canonical | research_foodie equivalent |
|---|---|---|
| Acquisition | collect experiences | `_eval_out/baselines.json` freeze + JSONL of every judged run + user corrections (§E1/E5) |
| Refinement | filter/noise-reduce | health-check diff → "debug tickets" (symptom→δ→hypothesis→fix class); drop delta ≤ judge-noise (§E2/E3) |
| Updating | change weights **or** prompts/memory | bump **versioned prompt/judge/config**, mutation-tested (§E5; DSPy/GEPA in Phase R) |
| Evaluation | measure against held-out | cadence run against frozen baselines; reference-vs-current snapshot (Evidently/promptfoo pattern, §4) |

Two evidence-backed "update mediums" we adopt, two we reject:
- **Adopt — token-space memory/skill library** (no weight change):
  - **Reflexion (Shinn et al., NeurIPS 2023, arXiv:2303.11366)** — converts binary/scalar feedback into natural-language *experience* stored in episodic memory; +11% HumanEval, +20% HotPotQA, +22% AlfWorld; memory truncated to last-3 reflections. → our "feedback corpus + skill/ticket ledger" (docs + JSONL), retrieved by baseline-diff.
  - **Voyager (Wang et al., NeurIPS 2023, arXiv:2305.16291)** — an ever-growing **skill library** (interpretable, compositional programs) + iterative prompting w/ environment feedback + self-verification; top-1 skill retrieval 80.2% → top-5 96.5%; removing the automatic curriculum drops discovery −93%; 4-shot attempt cap. → our runbook = skill library; component fixes are retrieved by the *measured failing axis*.
- **Reject — weight-space or fully-autonomous updates** (insufficient evidence / violates invariants): weight RL needs thousands of rollouts + compute (DSPy vs RL evidence below shows prompt-level is enough at our scale); autonomous evolution contradicts `AGENTS.md`.

## 4. Updating that is metric-gated: programmatic prompt evolution / 指标门控的提示演化

The "updating" phase should be as principled as possible — and there is now strong evidence that *prompt/program-level* evolution (not weights) is both enough and sample-efficient:

- **DSPy (Khattab et al., ICLR 2024, arXiv:2310.03714)** — programs compiled against a user metric self-bootstrap: >25% (Llama-2-13B: >65%) over few-shot prompting; 770M-param T5 pipelines competitive with GPT-3.5 expert prompt chains. DSPy Assertions (arXiv:2312.13382) add constraint-driven self-refinement + backtracking.
- **MIPRO (Opsahl-Ong et al., EMNLP 2024, arXiv:2406.11695)** — optimizes instructions + few-shot demos per module with credit-assignment across a multi-stage program.
- **GEPA (Agrawal et al., ICLR 2026 Oral, arXiv:2507.19457)** — reflective prompt evolution using **text feedback** (not just scalar scores): beats GRPO by up to **19–20pp while using up to 35× fewer rollouts** (IFBench: 678 rollouts → 38.61% vs GRPO 35.88% @ 24,000); beats MIPROv2 by >10pp; Pareto-frontier selection; **requires a strong reflection LM** (`gpt-5` class) — i.e., a Phase R dependency in our environment.
- **TextGrad (Yuksekgonul et al., arXiv:2406.07496; Nature 2025)** — textual "gradients" backpropagated through compound AI graphs; instance + prompt optimization.

**Decision:** our E-5 "versioned prompt/judge bumps" is a *manual, metric-gated* mini-DSPy/GEPA: every prompt/judge/config revision is a numbered artifact, re-baselined before/after, revertable, and only promoted when a measured delta clears variance-aware thresholds (§6). Full automated GEPA/DSPy compilation is parked in Phase R (needs an OpenAI-compatible strong reflection LM — same gate as everything else ≥300B).

## 5. Hardening the gate: adversarial & mutation testing / 门禁加固：对抗与变异测试

Because LLMs cannot be trusted to find their own mistakes (BIG-Bench Mistake, §2), the **deterministic gate must be adversarially exercised by an external generator** — this is the highest-value, lowest-cost "evolutionary" act available to us:

- **Mutation testing** (Python: `mutmut`, boxed/mutmut, PyPI 3.x; MIT-license-family OSS) — introduce small code/assertion mutations; surviving mutants = assertions that don't actually protect. Used to strengthen test suites and as CI gate.
- **Pattern applied to research_foodie:** each cadence, *synthesize mutated claim/quote/citation strings* (insert a swapped verb, replace a 5-gram fragment, reorder citation ID, drop a bilingual sentence) and assert the **L6 mechanical gate rejects them**; record kill-rate as `gate_coverage`. Any surviving mutant → debug ticket → fix the gate, not the prompt. This directly measures "would our fabrication shield still fire today?" with **zero LLM cost** and no self-reference.

## 6. Measuring the loop: continuous evaluation & drift / 测量循环：持续评测与漂移

MLOps practice gives the "evaluation" phase its shape: compare **current snapshots against a frozen reference** and gate on deltas:

- **Evidently AI** (open-source, Apache 2.0, evidentlyai.com) — "no model lasts forever"; 100+ checks, data-drift/quality/metric test suites runnable in CI/CD; reference-vs-current comparison.
- **promptfoo** (MIT; part of OpenAI since 2026, GitHub 25k★) — test-driven LLM development: declarative test cases → `eval` → asserts → CI/CD gate; red-teaming generates adversarial inputs; "stop the trial-and-error approach".
- **WhyLabs** drift algorithms (Hellinger recommended, KL, JS, PSI) — all compare inference vs a **baseline/reference set**.
- **DriftBench** (2026 industry pattern) — daily benchmark runs with *fixed prompts + deterministic scoring* to surface model/vendor drift. *directionally* useful, treat as unverified.

**Constraints this imposes on us (design rules #2–3):**
- (#2) **Variance-aware thresholds.** Our own measured judge noise is ±0.53 on P-A — a naive "score dropped 0.4 → alarm" would be false approximately half the time. Evolution cannot outrun measurement noise: adopt **judge median-of-3** (Phase L-3) before trusting any cadence delta; thresholds expressed in judge-noise units (e.g., alarm at ≥2σ≈±0.5, warn at ≥1σ).
- (#3) **Consistent substrate.** DriftBench's trick — fixed prompts & deterministic scoring — means our health subset must be *frozen* (fixed scenarios P-A/P-B/P-C + mock 34/34 + gold QA-6/7), never curated retroactively to pass.

## 7. Failure modes we must design out / 必须设计的防线

| Risk | Evidence | Mitigation (baked into Phase X) |
|---|---|---|
| **Model / representation collapse** (recursive self-consumption erases distribution tails) | Shumailov et al. 2024, Nature 631:755–759 (arXiv:2305.17493); Seddik et al. 2024 (arXiv:2404.05090): collapse unavoidable on synthetic-only; **mixing real data within a bound avoids it** | Feedback corpus stays **anchored to real primary sources** (parsed papers, gold tokens, arXiv truth); every record provenance-tagged; a **floor quota of real ground truth** in each cadence (≥ gold QA + gold_tokens checks); we never fine-tune, so the collapse vector is only in *prompt selection*—guarded by the same anchoring |
| **Reward hacking / judge gaming** — the loop "improves" the judge-friendliness of prompts while true quality drops | (implicit in judge-LM literature; our own judge is a weak free model) | separate **deterministic** axes always co-gate (L6 + gate_coverage §5); judge median; periodic adjudicator swap → deltas must survive a *different* judge before promotion (Phase R) |
| **Feedback-loop noise** — evolving on a single round's scores | measured ±0.53 | thresholds in σ-units; promotion requires N≥3 rounds & ≥2σ delta & no regression on mock/gold |
| **Lock-in to a moving free backend** — opencode model availability changes silently | DriftBench/Evidently rationale | backends pinned + verified per cadence (§E4); score deltas attributed to *backend/model* not just prompts |
| **Autocratic mutation** | AGENTS.md (no unsolicited commits) + blueprint human-checkpoint doctrine | the loop **only writes PROGRESS/baselines/JSONL**; any code/prompt change requires explicit user green-light (E-3) |

## 8. Feasibility × value matrix / 可行性与价值矩阵

Rated 1–5; "now" = local zero-cost, "R" = Phase R gated on strong-LM/GPU/key.

| Mechanism | Evidence | Feas (now) | Feas (R) | Value | Verdict |
|---|---|---|---|---|---|
| Baselines freeze + health-check regression gate (E1/E2) | Evidently/promptfoo/WhyLabs pattern | 5 | — | 4 | **do now (L-6 bundles it)** |
| Judge median-of-3 before trusting deltas (L-3) | our ±0.53 measurement | 5 | — | 4 | **prerequisite, do now** |
| Mutation/adversarial gate coverage (`gate_coverage`) | Huang 2023a · Tyen 2023 (BIG-Bench Mistake) · mutmut | 4 | — | 4 | **do now, zero-LLM** |
| Versioned prompt/judge registry, metric-gated manual bumps (E-5) | DSPy/MIPRO/GEPA metric-gating | 4 | — | 3 | **do now (manual)**, automate in R |
| Periodic cadence + tickets (E-3) + version ledger (E-4) | Reflexion memory · Voyager skill library · runbook | 4 | — | 3 | **do now** |
| Feedback corpus with provenance floor (E-5b) | Model collapse (Shumailov/Seddik) | 4 | — | 3 | **do now** |
| Automated prompt evolution (GEPA / DSPy compile) | GEPA 2507.19457 (35× cheaper than GRPO) | 1 | 3 | 3 | Phase R (needs strong reflection LM) |
| Adjudicator swap / multi-judge promotion delta | judge literature; our weak-judge constraint | 1 | 3 | 3 | Phase R |
| Scheduled CI hook + alerting (E-6) | Evidently CI/CD, DriftBench | 2 | 3 | 2 | Phase R (needs stable runtime + remote runner) |

**Ordering rationale:** measurement fidelity (median, frozen subset, gate_coverage) *before* any updating; updating stays manual and versioned until a strong-LM gate exists.

## 9. Rollout / 落地顺序

1. Freeze `_eval_out/baselines.json` (E-1) — 1 artifact, zero LLM.
2. Add `gate_coverage` mutation check on L6 (E-2b) — deterministic, minutes.
3. Implement judge median-of-3 in bench path (L-3) — prerequisite for trustworthy deltas.
4. Build `health_check.py` + bundle into `self_check.ps1` (E-2/L-6) — one command, <10 min.
5. Weekly cadence in PROGRESS (E-3), version ledger (E-4), JSONL feedback with provenance floor (E-5).
6. Phase R: GEPA/DSPy compile + adjudicator swap + scheduled alerting, only when the ≥300B endpoint exists.

## 10. References (verified 2026-09-20) / 参考来源

- Tao et al., *A Survey on Self-Evolution of Large Language Models*, arXiv:2404.14387 (v2, 2024).
- Gao et al., *A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve*, arXiv:2507.21046 (2025; TMLR 2026).
- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, arXiv:2310.01798 (ACL 2023).
- Tyen, Mansar, Chen, Regan, *LLMs cannot find reasoning errors, but can correct them! (BIG-Bench Mistake)*, arXiv:2311.08516 (2023).
- Chen et al., *Teaching Large Language Models to Self-Debug*, arXiv:2304.05128 (ICLR 2024).
- Chen et al., *Revisit Self-Debugging with Self-Generated Tests (RGD)*, arXiv:2501.12793 (ACL 2025).
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*, arXiv:2303.11366 (NeurIPS 2023).
- Wang et al., *Voyager: An Open-Ended Embodied Agent with Large Language Models*, arXiv:2305.16291 (NeurIPS 2023).
- Khattab et al., *DSPy: Compiling Declarative LM Calls into Self-Improving Pipelines*, arXiv:2310.03714 (ICLR 2024); DSPy Assertions arXiv:2312.13382.
- Opsahl-Ong et al., *Optimizing Instructions and Demonstrations for Multi-Stage LM Programs (MIPRO)*, arXiv:2406.11695 (EMNLP 2024).
- Agrawal et al., *GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning*, arXiv:2507.19457 (ICLR 2026 Oral); reference numbers pp.-table-verified from HTML.
- Yuksekgonul et al., *TextGrad: Automatic "Differentiation" via Text*, arXiv:2406.07496 (2024; Nature 2025).
- Shumailov et al., *AI Models Collapse When Trained on Recursively Generated Data*, Nature 631:755–759 (2024); *The Curse of Recursion*, arXiv:2305.17493.
- Seddik et al., *How Bad is Training on Synthetic Data? A Statistical Analysis of LLM Collapse*, arXiv:2404.05090 (2024).
- Evidently AI, evidentlyai.com (ML/AI monitoring, test suites in CI/CD; Apache-2.0) — accessed 2026-09-20.
- promptfoo, github.com/promptfoo/promptfoo (evals, asserts, red-teaming, MIT; OpenAI 2026) — accessed 2026-09-20.
- WhyLabs documentation, docs.whylabs.ai/docs/drift-algorithms (Hellinger/KL/JS/PSI vs reference set) — accessed 2026-09-20.
- mutmut, pypi.org/project/mutmut (Python mutation testing) — accessed 2026-09-20.
- DriftBench AI (driftbench.ai industry description; **directional/unverified**) — accessed 2026-09-20.
- Our own measurements: PROGRESS Session 19b (judge variance P-A 3.88±0.53 · mock 34/34 · panel n=31 · pools 22/30).