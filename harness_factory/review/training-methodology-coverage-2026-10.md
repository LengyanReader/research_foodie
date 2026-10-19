# Model-training methodology: coverage assessment · 模型训练方法论：覆盖度评估

> What the training stack contains, what this library covers, and where the boundary is drawn.
> 训练栈有什么、本仓库覆盖什么、边界画在哪。
**Updated:** 2026-10-20

## 0. The question, and the criterion

The library's axis is **harnessing** a model — context, tools, gates, provenance, orchestration, evolution — **not training
one**. So "is training covered?" has a precise answer only if the criterion is stated first:

> **In axis** = the harness can decide it at run time, without changing weights.
> **Adjacent** = the harness must *know about it* to choose, serve or evaluate a model — but does not do it.
> **Out of scope** = it changes weights, data or compute allocation during training; a different discipline with different
> failure modes.

Applying that criterion, the honest answer is: **the stack is surveyed (below) and the library covers the boundary, not the
stack.** That is a deliberate design choice, not an oversight — §5 records it as a non-addition with a revisit trigger.

**Method.** All rows come from one `id_list` batch against the arXiv API on **2026-10-20** (id, title, authors, date agree).
This is **abstract-level verification**: no PDF was opened, so any number quoted only in a paper's abstract is not relied on
here. Citations are `review/references.md` §O (R171–R191).

---

## 1. The stack, family by family

| Family | Canonical source | Verdict | Why |
|---|---|---|---|
| **Pretraining + scaling laws** | R171 Kaplan; R172 Chinchilla | **out** | Compute/architecture decisions made before any harness exists. |
| **Data curation / dedup / tokenizer** | — (no single canonical source entered) | **out** | Changes the corpus; harness sees only the result. |
| **Continual / curriculum learning** | — | **out** | Training-order decisions; a harness can *sequence tasks*, which is different. |
| **SFT / instruction tuning** | R173 InstructGPT; FLAN (2109.01652) | **out** | Weight update. The harness equivalent is a **prompt + skill + example set**. |
| **RLHF** | R174 Christiano; R173 | **out** | Reward model + policy optimisation. |
| **RLAIF / Constitutional AI** | R175 | **adjacent** | The *constitution* is a written policy; a harness can encode the same rules as gates/prompts — and should read them when selecting a model. |
| **DPO and variants** (IPO/KTO/ORPO) | R176 DPO; R177 IPO | **out** | Preference optimisation without a reward model, still a weight update. |
| **PEFT** (LoRA/QLoRA/adapters) | R178 LoRA; R179 QLoRA | **adjacent** | Cheap enough that "fine-tune instead of prompt" is a real decision; the harness should be able to *advise against it* when eval shows no gain. |
| **Distillation** | R180 | **adjacent** | Sequence-level distillation is a training method; **distilling behaviour into prompts/skills** is a harness method. Different artifact, same intent. |
| **Quantization** (GPTQ/AWQ/GGUF) | `arXiv:2210.17323` GPTQ; `arXiv:2306.00978` AWQ | **adjacent** | Changes what the harness can run locally; must be part of model selection and eval. |
| **MoE / long-context training** | `arXiv:2101.03961` Switch | **out** | Architecture/training. |
| **Reasoning RL** (PPO/GRPO, RLVR) | R181 GRPO; R182 DeepSeek-R1 | **out** (but read the eval) | The *result* changes model behaviour; the harness consumes it, does not produce it. |
| **Test-time compute** (self-consistency, best-of-n) | R207 (§Q) | **in** | Purely run-time: sampling, voting, budget. Already a harness concern (M3.8, M1). |
| **Post-training for agents / tool use** | R183 SWE-RL; R184 ReTool | **adjacent** | Explains *why* a model is good at tool loops; the harness still owns the loop, the guards and the tool surface (M6). |
| **Evaluation methodology** | R185 HELM; R186 MMLU; R187 LiveBench | **in** | This is the harness's own business: what to measure, contamination, saturation (M3). |
| **Model/knowledge editing** | R188 ROME; R189 MEMIT | **out** | Weight surgery; a harness should prefer retrieval/citation over editing. |
| **Safety alignment / red-teaming** | — | **adjacent** | The harness enforces guardrails at run time (M3.6); the training-side policy is a model-selection input. |
| **Sycophancy / reward hacking** | R191 sycophancy; R190 reward hacking | **adjacent** | Not the harness's to fix — but it must *detect* the symptom (agreement-as-quality) in evaluation. |

Two rows deserve emphasis because they are the ones people get wrong:

- **Evaluation is in axis.** R185 (HELM) argues for multi-metric, scenario-wide evaluation precisely because a single
  benchmark rewards overfitting. R187 (LiveBench) is a *design* response to contamination. A harness that reports one score
  is importing the training world's worst habit.
- **Sycophancy is a harness-visible defect.** R191 shows preference optimisation can train agreement rather than truth.
  A harness cannot un-train it, but it can refuse to treat "the model agreed with the reviewer" as evidence.

---

## 2. What a harness can enforce *without* training

This is the part that makes the boundary useful rather than defensive. Every item below is a legitimate substitute for a
fine-tune, and several are strictly better:

| Instead of… | Do this | Why |
|---|---|---|
| Fine-tuning on a style | A declared house style + a linter (M4.14, R199) | Reversible, inspectable, no eval regression. |
| Fine-tuning on facts | Retrieval + citations (M4.1, M4.13) | Facts change; weights do not. |
| Fine-tuning on a workflow | A skill/command + a gate (M6, M3) | Versioned and testable. |
| Distilling a big model | A model router + cost caps (M1, `cost-budget-caps`) | Cheaper to operate and to audit. |
| A custom eval suite | A held-out task set with a written criterion (M3.1) | The hard part is the criterion, not the harness. |
| "The model is better now" | A measured comparison on tasks it was not tuned on (M5.3) | Same standard the library already applies to itself. |

---

## 3. If the library ever added a training axis

The blocker is **not** effort; it is that the feature vector has no affordance for it. The current axes are `horizon`,
`verifiability`, `stakes`, `grounding`, `artifact`, `tool_surface`, `collaboration`, `domain`. None of them can distinguish
"train a model" from "use a model" — `artifact` can be `dataset` or `code`, but a training run is a *process*, not an
artifact, and `domain: model-selection` is about picking a model, not producing one.

So a training capability would need **a new axis**, something like `model_role: consume | adapt | produce`. Until that
exists, any `training-*` capability would be a predicate the engine silently ignores — exactly the failure M5.10 names
("a discriminator the engine can actually evaluate — not a predicate it silently ignores"). If such an axis is ever added,
the first capability would be `training-budget-discipline` (what may be trained, on what evidence, with what eval before
and after), not "how to train".

---

## 4. Honest flags: where 2026 moved past the classics

- **Scaling laws are not a recipe.** R171's compute-optimal curve was corrected by R172; both are 2020–2022 snapshots and
  neither predicts the reasoning-RL regime (R182).
- **MMLU is saturated** (R186). Citing it as evidence of capability in 2026 is a measurement error; R187 exists because of it.
- **"RLHF" now names a family**, not one pipeline (R173 → R174 → R175 → R176 all differ in what is optimised).
- **Quantization is no longer a quality cliff.** `arXiv:2210.17323` / `arXiv:2306.00978` changed the default; treating 4-bit as "degraded" is out of date.
- **Agentic post-training is the fastest-moving part** (R183, R184); any statement here has a short shelf life.
- **Abstract-level only.** Nothing in this doc rests on a number read out of a PDF.

---

## 5. Deliberate non-additions

- **No `training-*` capability.** No feature affordance to trigger it (§3); adding one would create a silently-ignored
  predicate. Recorded with a revisit trigger: *if a `model_role` (or equivalent) axis is added*.
- **No training-toolkit instruments.** `transformers`/`peft`/`trl`/`vLLM` are not **evidence instruments** (M3.10); they
  would be catalogued only if the library ever ran training, which it does not.
- **No claim of completeness beyond the families above.** The list is *bounded*, not exhaustive: it covers the families that
  a harness author is likely to be asked about.
- **No training advice.** This doc says what is out of scope and why; it does not teach how to train.

---

## 中文

**判据先写明。** **在轴内**＝harness 能在运行期决定、不改权重；**相邻**＝harness 必须知道它，才能选模型/部署/评估，但不亲自做；**不在轴内**＝改权重、改数据或改训练算力，属于另一门学科、另一套失败模式。

**结论：栈被梳理了，库覆盖的是"边界"，不是"栈"。** 这是设计选择，不是遗漏（§5 记为带重访触发条件的"有意不新增"）。

**关键两行。** ① **评估在轴内**——HELM（R185）主张多指标、多场景，正因为单一榜单奖励过拟合；LiveBench（R187）是对污染的**设计回应**。只报一个分数的 harness，等于把训练界最坏的习气搬了过来。
② **谄媚是 harness 可见的缺陷**——偏好优化可能训练出"同意"而非"正确"（R191）；harness 不能反训练它，但可以拒绝把"模型同意了评审"当作证据。

**不训练也能做的事。** 要风格→房规 + linter（M4.14）；要事实→检索 + 引用（M4.1/M4.13）；要流程→skill + 门禁（M6/M3）；要便宜→模型路由 + 成本上限；
"模型变好了"→在**未调过**的任务上实测（M5.3）。

**为什么不加 `training-*` 能力。** 卡点不是工作量，而是**特征向量没有对应的可判别维度**：现有八轴无法区分"训练一个模型"与"使用一个模型"
（`artifact=dataset/code` ≠ 训练过程；`domain=model-selection` 是选模型，不是造模型）。在加入类似 `model_role: consume|adapt|produce` 的轴之前，
任何 `training-*` 都会是引擎静默忽略的谓词——正是 M5.10 点名的失败。

**诚实的时效提醒。** 缩放律只是快照（R171 被 R172 修正，且都预测不了推理 RL 时代 R182）；MMLU 已饱和（R186）；"RLHF"现在是一个家族而非一条流水线；
4-bit 量化不再是质量悬崖（`arXiv:2210.17323` / `arXiv:2306.00978`）；agent 后训练是移动最快的一段（R183/R184）。本文件**全部为摘要级核验**，不依赖任何从 PDF 里读到的数字。
