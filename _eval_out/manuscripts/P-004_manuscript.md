# 2304.10464

## Abstract
## 1. Introduction

## Intro
## 1. Introduction

Supervised fine-tuning (SFT) teaches large language models (LLMs) to imitate correct reasoning traces, but it does not tell them *why* a trace is correct, leaving the value of their own step-by-step solutions ungrounded. This survey asks a single question: how should a dedicated post-SFT alignment stage be designed so that an LLM becomes a genuinely better reasoner rather than a better mimic? Our thesis, anchored in the task-plan alignment framework of arXiv:2304.10464, holds that inserting an alignment stage guided by a value signal over the model's own reasoning process — where a high-quality "task plan" bundles correct step-by-step solutions with behavioral instructions — confers reasoning gains that SFT alone cannot deliver, gains that in that work reached +18.3% over zero-shot chain-of-thought on average across 10 AMPS tasks (arXiv:2304.10464). We then trace the two failure modes that any such stage must survive: the assessment-misalignment problem, where fine-tuned models over-score subpar chains of thought and lose the constraint term that ranking-based alignments such as DPO, RRHF and PRO overlook (arXiv:2309.02144), and the brittleness of reinforcement-learning-based post-training, where policy-gradient variants such as GRPO succeed under idealized settings yet collapse across non-ideal scenarios (arXiv:2508.04848). The remainder of the survey is organized as follows: Section 2 motivates alignment for reasoning via learned task plans; Section 3 diagnoses assessment misalignment and the role of constraints in value-rated fine-tuning; Section 4 analyzes reinforcement-learning-based reasoning alignment, its representative algorithms, and their failure modes; Section 5 closes with open problems.

> 中文速览：本文综述围绕一个核心问题——在监督微调（SFT）之后，应如何设计专门的"对齐（alignment）"阶段，使大语言模型的推理能力真正提升，而非仅仅模仿正确解答。我们的论点以 arXiv:2304.10464 的任务计划（task plan）对齐框架为支点：在对齐阶段，用作用于模型自身推理过程的价值信号进行引导——高质量任务计划既包含逐步正确解法，也包含规避失误的行为指令——能带来单纯 SFT 无法实现的效果（该工作在 10 个 AMPS 任务上较零样本思维链平均提升 18.3%）。随后我们梳理两个必须跨越的失败模式：一是"评估失准（assessment misalignment）"——微调模型频繁给次优思维链打出高分，且被 DPO、RRHF、PRO 等排序式对齐忽略的约束项对其性能至关重要（arXiv:2309.02144）；二是基于强化学习的后训练存在脆弱性——以 GRPO 为代表的策略梯度变体在理想设定下收益明显，却在多种非理想场景中性能显著下滑（arXiv:2508.04848）。行文结构如下：第 2 节借助任务计划论证对齐驱动推理的动机；第 3 节诊断评估失准与价值微调中约束的作用；第 4 节分析基于强化学习的推理对齐及其代表性算法与失败模式；第 5 节提出开放性难题。

**Section roadmap (EN):** Section 2 — Alignment via learned task plans (arXiv:2304.10464); Section 3 — Assessment misalignment and constraints (arXiv:2309.02144); Section 4 — RL-based reasoning alignment and its limits (arXiv:2508.04848); Section 5 — Open problems.

## Problem and Motivation

Chain-of-thought prompting measurably improves reasoning in large language models, yet the standard path for instilling it — supervised fine-tuning (SFT) — teaches models to imitate target answers without teaching them how to generate sound intermediate reasoning. This reveals a missing *alignment* step over the reasoning process itself, distinct from preference/RLHF-style training that aligns only final outputs. Treating reasoning as something to be planned and supervised, a high-quality task plan must contain correct step-by-step solutions for solving all situations and behavioral instructions for avoiding mistakes (arXiv:2304.10464); the same work therefore proposes decomposing reasoning into two separately supervised stages — producing the reasoning, then emitting the final answer (arXiv:2304.10464). Evidence that answer-level training is insufficient is direct: fine-tuned LLMs suffer from an "Assessment Misalignment" problem, frequently assigning higher scores to subpar chain-of-thought responses (arXiv:2309.02144), and their task accuracy tracks assessment accuracy almost perfectly (Pearson 0.93 on GSM8K, 0.98 on ECQA) (arXiv:2309.02144).

The obvious alternative — aligning reasoning via reinforcement learning — is not a complete remedy either. RL has become a key technique for enhancing LLM reasoning, with policy-gradient algorithms dominating post-training (arXiv:2508.04848), yet RL fine-tuning causes significant performance decline across all three non-ideal scenarios tested, despite gains under idealized settings (arXiv:2508.04848). Ranking-based alignment such as DPO, RRHF and PRO also omit a constraint term that proves crucial to their performance (arXiv:2309.02144). The sources thus converge on a shared diagnosis — post-training fails to align the reasoning process — while disagreeing implicitly on the fix: 2304.10464 claims a dedicated reasoning- alignment stage suffices, but both the SFT-assessment path (arXiv:2309.02144) and the RL path (arXiv:2508.04848) exhibit fragility outside idealized conditions. The open gap is a robust, constraint-aware objective that supervises each reasoning stage independently yet remains stable when assumptions of the training distribution are relaxed.

## 问题与动机

思维链提示（CoT）能够切实提升大模型的推理能力，但标准的监督微调（SFT）只教模型模仿目标答案，并未教会它如何生成高质量的中介推理。这暴露出对"推理过程本身"缺失一步对齐（alignment）：与偏好/RLHF 式仅对齐最终输出不同，推理应被规划并独立监督——高质量的任务计划须包含覆盖所有情况的逐步解法与规避错误的指令（arXiv:2304.10464），故该工作主张将推理分解为"生成推理"与"输出最终答案"两个可分别监督的阶段（arXiv:2304.10464）。答案级训练不足的直接证据是：微调后的大模型存在"评估错位"（Assessment Misalignment）问题，频繁给较差的 CoT 响应打出更高分数（arXiv:2309.02144），且其任务准确率与评估准确率近乎完全正相关（GSM8K 上 Pearson 0.93，ECQA 上 0.98）（arXiv:2309.02144）。

用强化学习对齐推理也并非完整解药：RL 已成为增强大模型推理的关键技术，策略梯度算法主导后训练阶段（arXiv:2508.04848），但在全部三个非理想场景下 RL 微调都造成显著性能下降，尽管理想设置下有增益（arXiv:2508.04848）；DPO、RRHF、PRO 等基于排序的对齐方法还忽略了对其性能至关重要的约束项（arXiv:2309.02144）。各来源对"后训练未能对齐推理过程"这一诊断达成共识，却对修复路径存在隐性分歧：2304.10464 认为专用推理对齐阶段即可，而 SFT 评估路径（arXiv:2309.02144）与 RL 路径（arXiv:2508.04848）一旦离开理想条件便表现出脆弱性。留存的开放缺口是：需要一种稳健且带约束的对齐目标，能够独立监督每一推理阶段，并在训练分布假设被放宽时依然稳定。

## Proposed Framework: Value-Aligned Reasoning

The framework targets the model's reasoning process itself rather than only its terminal answer: the model first generates a chain-of-thought reasoning path alongside the resulting answer, and the path is then scored against the correctness of the answer it leads to (arXiv:2304.10464). This is realized through a learned value network that emits a value for each candidate path, encoding how likely that path is to produce a correct result and thereby distilling outcome correctness back into reasoning-path supervision (arXiv:2304.10464). The need for such a signal is concrete: fine-tuned LLMs exhibit an Assessment Misalignment problem, frequently assigning higher scores to subpar chain-of-thought responses (arXiv:2309.02144), even though task accuracy and assessment accuracy are strongly positively correlated (Pearson 0.93 on GSM8K, 0.98 on ECQA) (arXiv:2309.02144). The effect is to turn training into "training with inner reasoning": the latent reasoning path—not just the observable final answer—becomes the object being aligned (arXiv:2304.10464).

This value-aligned view stands in explicit tension with the dominant post-training paradigm, in which policy gradient algorithms dominate reasoning-focused RL (arXiv:2508.04848). Policy gradient methods such as GRPO deliberately remove the separate value model, estimating baselines from group scores instead (arXiv:2508.04848), and argue that they avoid expensive rollouts, offering superior computational efficiency (arXiv:2508.04848). The disagreement is structural: whether reasoning-path supervision requires an explicitly learned value signal over inner reasoning, or whether value-free group baselines suffice.

The auxiliary details of the scoring signal matter as much as its existence. Ranking-based alignment methods (DPO, RRHF, PRO) overlook a constraint term that proves crucial to their performance (arXiv:2309.02144); reducing the scores of negative chain-of-thoughts with the alignment loss but without any constraint degrades the LLM (arXiv:2309.02144). The open gap is robustness: RL fine-tuning gains under idealized settings yet declines significantly across all three non-ideal scenarios (arXiv:2508.04848), and neither camp has established whether value-aligned reasoning-path supervision survives such distribution shift.

---

该框架把对齐目标对准模型自身的推理过程，而非仅针对最终答案：模型先生成思维链推理路径与相应的答案，再依据该路径所导向答案的正确性为路径打分（arXiv:2304.10464）。实现方式是一个学习得到的价值网络，它为每条候选推理路径输出一个价值，编码该路径产生正确结果的可能性，从而把"结果正确性"蒸馏回"推理路径监督"（arXiv:2304.10464）。这一设计的动机清晰可见：微调后的 LLM 存在"评估错位"问题，常给较差的思维链响应更高的分数（arXiv:2309.02144），尽管任务准确率与评估准确率强正相关（GSM8K 上 Pearson 0.93，ECQA 上 0.98）（arXiv:2309.02144）。其效果是把训练变成"对内在推理的训练"：被对齐的对象是潜在推理路径，而不只是可观测的最终答案（arXiv:2304.10464）。

这种"价值对齐"观点与当前主流的后训练范式存在明显张力——后者以策略梯度算法主导推理型 RL（arXiv:2508.04848）。GRPO 等策略梯度方法刻意去掉独立的价值模型，改用群体分数估计基线（arXiv:2508.04848），并主张由于避免了昂贵的 rollout，从而获得更高的计算效率（arXiv:2508.04848）。分歧是结构性的：推理路径的监督究竟需要针对内在推理显式学习价值信号，还是无价值的群体基线就已足够。

打分信号的辅助细节与其存在本身同样关键。基于排名的对齐方法（DPO、RRHF、PRO）忽略的约束项对其性能至关重要（arXiv:2309.02144）；在无任何约束的情况下用对齐损失降低负例思维链的分数，会导致模型退化（arXiv:2309.02144）。悬而未决的空白是鲁棒性：RL 微调在理想设定下有所提升，却在全部三种非理想场景下显著下降（arXiv:2508.04848），而无论哪一阵营都尚未证明价值对齐的推理路径监督能够在分布偏移下保持有效。

## Training with Inner Reasoning (TIR)

Training with Inner Reasoning (TIR) rests on the view that reinforcement learning (RL) is a key technique for enhancing LLM reasoning, with policy-gradient algorithms dominating post-training (arXiv:2508.04848). TIR samples internal reasoning paths, selects the single highest-value path as the learning target, and supervises generation toward that path — aligning the reasoning process with high outcome value to close the gap between outcome-based correctness and the process that reaches it (arXiv:2508.04848). Its machinery is gradient-based: GRPO, a representative variant, estimates its baseline from group scores and removes the need for a separate value model, while policy-gradient methods avoid the expensive rollouts of Monte Carlo approaches (arXiv:2508.04848). This connects to earlier alignment work: a dedicated stage after supervised fine-tuning, guided by a value signal over the model's own reasoning, beats SFT alone, and the learned task plan transfers across LLMs, improving 10 AMPS tasks by 18.3% and 7% over zero- and few-shot chain-of-thought (arXiv:2304.10464).

Both threads agree that value-based supervision over reasoning is the lever; the value signal itself is the fragile part. Fine-tuned LLMs show Assessment Misalignment, frequently giving subpar chain-of-thought responses higher scores (arXiv:2309.02144), even though task and assessment accuracy correlate strongly (Pearson 0.93 on GSM8K, 0.98 on ECQA) (arXiv:2309.02144). Down-weighting negative COTs without the constraint overlooked by DPO, RRHF and PRO degrades the model (arXiv:2309.02144), and RL fine-tuning that helps under idealized settings declines sharply across three non-ideal scenarios (arXiv:2508.04848). The open gap: TIR's promise hinges on reliable value estimation, yet no source specifies when sampled paths' values misfire under distribution shift.

---

TIR 建立在"强化学习是提升大语言模型推理能力的关键技术、策略梯度算法主导后训练"这一观察之上（arXiv:2508.04848）。其核心流程是采样内部推理路径、挑选价值最高的单一路径作为学习目标，并监督生成朝该路径对齐，令推理过程与高结果价值相一致，从而弥合"基于结果的正确性"与"达成该结果的过程"之间的差距（arXiv:2508.04848）。其机制可辨识地基于梯度：代表性变体 GRPO 用群体分数估计基线，省去独立价值模型；与蒙特卡洛方法相比，策略梯度避免昂贵回滚、计算效率更高（arXiv:2508.04848）。这与更早的对齐研究一脉相承：在监督微调之后插入由模型自身推理过程的价值信号引导的对齐阶段，效果优于单纯微调；学得的任务计划还可跨模型迁移，在 10 个 AMPS 任务上较零样本/少样本思维链分别提升 18.3% 与 7%（arXiv:2304.10464）。

两条脉络都认同"对推理过程施以基于价值的监督"是关键，但价值信号本身却最脆弱。微调后的 LLM 存在"评估错位"：常常给次优的思维链更高分（arXiv:2309.02144），尽管任务准确率与评估准确率强正相关（GSM8K 上 Pearson 0.93，ECQA 上 0.98）（arXiv:2309.02144）。若不加以被 DPO、RRHF、PRO 忽视的约束就降低负样本思维链分数，模型会退化（arXiv:2309.02144）；RL 微调在理想设定下获益，却会在三种非理想场景下性能显著下降（arXiv:2508.04848）。遗留的开放缺口是：TIR 的效力取决于可靠的估值，但尚无来源说明分布偏移下采样路径的价值何时会失灵。

## Role of the Value Network

A value network predicts the value of a reasoning path from the correctness of its final answer, providing dense, path-level supervision analogous to the reward/value signal used in alignment pipelines. The quality of that supervision is directly measurable: after fine-tuning, an LLM's task accuracy and assessment accuracy are strongly positively correlated (Pearson 0.93 on GSM8K, 0.98 on ECQA) (arXiv:2309.02144), yet the same models suffer an Assessment Misalignment problem, frequently assigning higher scores to subpar chains-of-thought (arXiv:2309.02144). Such value-guided signals operate over high-quality plans: a high-quality task plan contains correct step-by-step solutions for solving all situations and behavioral instructions for avoiding mistakes, and the plan learned by one LLM can directly guide another LLM — improving average performance on 10 AMPS tasks by 18.3% and 7% over zero-shot/few-shot chain-of-thought (arXiv:2304.10464).

In alignment pipelines, this value signal selects high-quality reasoning trajectories among candidates, and how it is applied is consequential: a constraint term overlooked by ranking-based alignment methods such as DPO, RRHF and PRO is crucial for their performance (arXiv:2309.02144), and reducing the scores of negative COTs without any constraint causes degradation of the LLM (arXiv:2309.02144).

However, not all post-training regimes rely on an explicit value network. GRPO, a representative policy-gradient variant, removes the need for a separate value model by estimating its baseline from group scores (arXiv:2508.04848), and policy-gradient approaches avoid the expensive rollouts of Monte Carlo methods (arXiv:2508.04848). While RL has become a key technique for enhancing LLM reasoning (arXiv:2508.04848), RL fine-tuning causes significant performance decline across non-ideal scenarios despite gains under idealized settings (arXiv:2508.04848). The open gap: whether value-model-free, group-relative supervision can preserve the dense, path-level benefit that explicit value networks provide — an unsettled tension between learned value signals and reward-model-free policy gradients.

价值网络依据推理路径最终答案的正确性来预测其价值，提供密集的路径级监督，作用类似对齐流程中的奖励/价值信号 (arXiv:2309.02144)。该监督质量可直接度量：微调后模型的任务准确率与评估准确率强烈正相关（GSM8K 上 Pearson 0.93、ECQA 上 0.98），但同一批模型常犯"评估错位"，给较差的思维链打更高分 (arXiv:2309.02144)。价值引导信号运行于高质量任务计划之上：高质量计划既含分步解法也含避免出错的行为指令，且一个 LLM 学到的计划可直接引导另一个 LLM，使 10 项 AMPS 任务性能较零/少样本思维链提升 18.3%/7% (arXiv:2304.10464)。

对齐流程中，该价值信号在候选轨迹间挑选高质量推理路径；其应用方式至关重要：DPO、RRHF、PRO 等排名式方法忽视的约束项对其性能至关重要，且不加约束地压低负样本 CoT 得分会导致模型退化 (arXiv:2309.02144)。

但并非所有后训练范式都依赖显式价值网络：GRPO 以组内得分估计基线，省去单独的价值模型，且策略梯度避免了蒙特卡洛方法昂贵的 rollout (arXiv:2508.04848)。尽管 RL 已是提升推理的关键技术，其在理想设定下有收益，却在非理想场景下显著衰退 (arXiv:2508.04848)。遗留的开放问题：免价值模型、组相对监督能否保留显式价值网络的密集路径级收益——学习到的价值信号与免价值模型的策略梯度之间的张力尚未解决。

## Empirical Results and Implications

Empirically, aligning the model's own reasoning process with a value signal improves reasoning accuracy over SFT-only baselines on mathematical and commonsense benchmarks (arXiv:2304.10464; arXiv:2309.02144). On ten AMPS tasks, plan-guided alignment improves average performance by 18.3% over zero-shot and 7% over few-shot chain-of-thought (arXiv:2304.10464). Consistent evidence comes from the Assessment Misalignment finding that fine-tuned LLMs frequently assign higher scores to subpar chain-of-thought responses (arXiv:2309.02144), and from the strong correlation between task accuracy and assessment accuracy (Pearson 0.93 on GSM8K, 0.98 on ECQA) (arXiv:2309.02144).

These results support the thesis that reasoning gains come less from more data or larger models than from aligning the reasoning process itself with a value signal. Yet the alignment must be constrained: reducing negative chain-of-thought scores without any constraint degrades the model, and the constraint term overlooked by ranking-based methods such as DPO, RRHF and PRO is crucial to their performance (arXiv:2309.02144). A cautionary contrast comes from RL-based alignment, now a key technique for enhancing reasoning with policy-gradient methods dominating post-training and avoiding expensive rollouts (arXiv:2508.04848); despite gains under idealized settings, performance declines significantly across all three non-ideal scenarios (arXiv:2508.04848).

The implication is a general recipe linking chain-of-thought research to alignment techniques. The disagreement between idealized gains and non-ideal degradation leaves an open gap: under which distributional or computational conditions the value-guided recipe remains robust is unresolved, and the transfer-planning evidence addresses only part of it (arXiv:2304.10464).

--

中文版：

实证层面，将模型自身的推理过程与价值信号对齐，能在数学与常识推理基准上相较仅做监督微调的基线带来稳定的精度提升（arXiv:2304.10464；arXiv:2309.02144）。在 10 个 AMPS 任务上，规划引导的对齐相比零样本、少样本思维链的平均性能分别提升 18.3% 与 7%（arXiv:2304.10464）。一致的证据来自"评估错位"（Assessment Misalignment）：微调 LLM 常给低质思维链分配更高分数（arXiv:2309.02144）；同时任务准确率与评估准确率高度相关（GSM8K 上 Pearson 0.93，ECQA 上 0.98）（arXiv:2309.02144）。

这些结果支持"推理能力的提升更多来自把推理过程本身与价值信号对齐，而非单纯堆数据或加大模型"这一论点。但对齐必须有约束：无任何约束地压低负面思维链分数会导致模型退化，而 DPO、RRHF、PRO 等排序式对齐方法遗漏的约束项对其性能至关重要（arXiv:2309.02144）。来自基于强化学习的对齐给出警示：RL 已成为增强 LLM 推理的关键技术，策略梯度方法主导后训练并避免昂贵的 rollout（arXiv:2508.04848）；但尽管在理想设定下有效，在三个非理想场景下性能均显著下降（arXiv:2508.04848）。

由此提出的通用配方把思维链研究接入对齐技术。理想增益与非理想场景退化之间的分歧留下一项开放缺口：在何种数据分布或算力条件下该价值引导配方依然稳健尚不清楚，而"规划可迁移"的证据仅能部分解答（arXiv:2304.10464）。

## Conclusion

> 中文速览：本文档梳理的调研表明，"对齐即推理增益"成立——在监督微调（SFT）之后、以模型自身推理过程的价值信号为引导的专门对齐阶段，能比单纯 SFT 更强地提升大型语言模型的推理能力（arXiv:2304.10464）。但同时，这套管线能否落地取决于三个关卡：评估信号是否可靠（微调后模型对自身次优推理过高打分，arXiv:2309.02144）、约束项是否被保留（缺失约束会导致模型退化，arXiv:2309.02144），以及 RL 后训练在非理想场景下是否仍然稳健（arXiv:2508.04848）。三个维度共同指向一个开放命题：推理对齐的质量由"评估器精度 × 目标约束 × 场景鲁棒性"共同决定，而三者在当前研究中均未得到充分联合验证。
*Updated: 2026-09-19*

### Key takeaways

**1. Alignment, not scale of SFT, is what makes LLMs better reasoners.** A dedicated alignment stage inserted after supervised fine-tuning and guided by a value signal over the model's own reasoning process outperforms supervised fine-tuning alone (arXiv:2304.10464). The aligned behavior is instantiated as a *task plan* — correct step-by-step solutions plus behavioral instructions for avoiding mistakes — and such plans transfer across models, so the plan learned by one LLM can directly guide another, revealing a new transfer-learning paradigm (arXiv:2304.10464). Concretely, the method averages +18.3% over zero-shot and +7% over few-shot chain-of-thought across 10 AMPS tasks (arXiv:2304.10464).

**2. The failure mode alignment repairs is Assessment Misalignment.** Fine-tuned LLMs frequently assign higher scores to subpar chain-of-thought responses, and this assessment error is strongly coupled with task error — task accuracy and assessment accuracy correlate at Pearson 0.93 on GSM8K and 0.98 on ECQA (arXiv:2309.02144). The paper's key corrective: a *constraint* term that ranking-based methods (DPO, RRHF, PRO) overlook is crucial to their performance; suppressing negative chain-of-thought scores without such a constraint demonstrably degrades the model (arXiv:2309.02144). Together these results imply that SFT alone leaves the model's self-assessment unreliable, which is exactly the signal alignment must improve.

**3. RL post-training is the dominant engine, yet its gains are scenario-fragile.** While policy-gradient methods now dominate reasoning post-training and are computationally cheaper than Monte Carlo approaches because they avoid expensive rollouts (arXiv:2508.04848) — with GRPO as a representative variant that removes the value model by estimating the baseline from group scores (arXiv:2508.04848) — RL fine-tuning's substantial gains under idealized settings decline significantly across non-ideal scenarios, exposing critical limitations in advanced reasoning capabilities (arXiv:2508.04848).

### Remaining gaps

- **The assessor chicken-and-egg problem.** Aligning reasoning requires a trustworthy value signal over the model's own reasoning, yet fine-tuned LLMs systematically misjudge that reasoning (arXiv:2309.02144). Where a reliable verifier comes from — prior to the alignment that is supposed to produce one — remains unanswered.
- **Transfer paradigm scope.** Plan transfer between LLMs (arXiv:2304.10464) has been demonstrated on a specific task family (AMPS); cross-family generalization, scale sensitivity, and teacher–student dynamics (how plan quality degrades with a weaker teacher) are uncharacterized.
- **Robustness outside idealized benchmarks.** The performance collapse under non-ideal scenarios (arXiv:2508.04848) is reported but not yet mechanistically attributed — reward hacking, distribution shift, and unreliable reward signals remain confounded.
- **Cost–quality frontier of model-free variants.** GRPO-style group-baseline estimation avoids a separate value model (arXiv:2508.04848), but whether the efficiency gain is paid in alignment quality at scale has not been quantified.
- **No joint study.** The three threads — value-guided alignment (arXiv:2304.10464), constraint-corrected preference optimization (arXiv:2309.02144), and RL fragility (arXiv:2508.04848) — have not been evaluated together under a shared benchmark, so their interaction effects are unknown.

### Bottom line

The surveyed evidence establishes the central hypothesis of this survey: **post-SFT alignment guided by a value signal over the model's own reasoning is what yields genuine reasoning gains over SFT alone** (arXiv:2304.10464). The practical ceiling, however, is set by the alignment signal itself — without accurate self-assessment (arXiv:2309.02144) and without the constraint that ranking methods discard, gains erode; and under non-ideal conditions the RL machinery that produces these gains degrades (arXiv:2508.04848). Future work should therefore prioritize jointly validating assessor quality, constraint preservation, and scenario robustness on a single, shared reasoning benchmark.

---

## 中文结论

### 要点总结

- **对齐才是推理增益的来源，而非单纯的数据规模**：在 SFT 之后插入一个以模型自身推理过程的价值信号为引导的专门对齐阶段，比单纯 SFT 更能提升推理能力（arXiv:2304.10464）。对齐行为体现为"任务计划"——正确分步解法 + 避免错误的指令；该计划可跨模型迁移（「一个 LLM 学到的计划可直接引导另一个 LLM」），从而构成一种新的迁移学习范式。方法在 10 个 AMPS 任务上较 zero-shot/few-shot 思维链分别平均提升 18.3% 和 7%（arXiv:2304.10464）。
- **对齐要修的病根是"评估错位"**：微调后的 LLM 常给次优推理链打高分，且此评估误差与任务误差高度耦合——任务准确率与评估准确率在 GSM8K 上 Pearson 相关系数 0.93、ECQA 上 0.98（arXiv:2309.02144）。被 DPO/RRHF/PRO 等排序式对齐方法忽视的**约束项**对性能至关重要；若无约束地压低负例得分，模型会明显退化（arXiv:2309.02144）。换言之，SFT 单独训练留下的正是对齐必须修复的"自我评估不可靠"问题。
- **RL 后训练是主流引擎，但收益场景脆弱**：策略梯度类方法主导推理后训练，且避免昂贵的蒙特卡洛回滚、计算更高效（arXiv:2508.04848）；GRPO 以组内得分估计基线、免去独立值模型，是代表性变体（arXiv:2508.04848）。但在理想设定下的显著增益，在非理想场景中会明显下滑，暴露出高级推理能力的关键短板（arXiv:2508.04848）。

### 尚存空白

- **评估器"先有鸡还是先有蛋"问题**：对齐需要可靠的"对自己推理做评估"的价值信号，但微调后的 LLM 恰恰会系统性误判自身推理（arXiv:2309.02144）——可靠评估器从何而来，尚未解决。
- **计划迁移范式的外推范围**：跨模型计划迁移仅在特定任务族（AMPS）上验证（arXiv:2304.10464）；跨模型族泛化、规模敏感性、教师模型变弱时计划质量的衰退动力学均未刻画。
- **理想基准之外的稳健性**：非理想场景下的性能塌陷（arXiv:2508.04848）尚未归因到机理层面——奖励破解、分布偏移、不可靠奖励信号仍混叠在一起。
- **免值模型变体的成本–质量边界**：GRPO 式组基底线可省去独立值模型（arXiv:2508.04848），但省下的成本是否以规模化后的对齐质量为代价，缺乏量化证据。
- **缺少联合研究**：价值引导对齐（arXiv:2304.10464）、约束修正的偏好优化（arXiv:2309.02144）与 RL 脆弱性（arXiv:2508.04848）三条线索从未在同一基准上共同评测，彼此交互效应未知。

### 结语

现有证据支持本调研的核心命题：**SFT 之后、以模型自身推理的价值信号为引导的对齐，才是相对单纯 SFT 取得真正推理增益的原因**（arXiv:2304.10464）。但性能上限由"对齐信号本身"决定——缺少准确的自我评估（arXiv:2309.02144）与排序方法丢弃的约束项，增益会流失；而在非理想条件下，产出这些增益的 RL 机制本身还会退化（arXiv:2508.04848）。因此，后续工作应优先在**同一个共享推理基准**上，联合验证评估器质量、约束保留与场景稳健性三者。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | A high-quality task plan contains correct step-by-step solutions for solving all situations and behavioral instructions … | arXiv:2304.10464 | high |
| 2 | The task plan learned by one LLM can directly guide another LLM to improve its performance, revealing a new transfer lea… | arXiv:2304.10464 | high |
| 3 | The method improves average performance on 10 AMPS tasks over zero-shot/few-shot chain-of-thought by 18.3% and 7% respec… | arXiv:2304.10464 | high |
| 4 | Fine-tuned LLMs suffer from an Assessment Misalignment problem: they frequently assign higher scores to subpar chain-of-… | arXiv:2309.02144 | high |
| 5 | The constraint term, overlooked by ranking-based alignment methods such as DPO, RRHF and PRO, is crucial for their perfo… | arXiv:2309.02144 | high |
| 6 | Task accuracy and assessment accuracy of vanilla fine-tuned LLMs are strongly positively correlated (Pearson 0.93 on GSM… | arXiv:2309.02144 | high |
| 7 | Reducing the scores of negative COTs with the alignment loss without any constraint causes degradation of the LLM. | arXiv:2309.02144 | high |
| 8 | Reinforcement learning (RL) has become a key technique for enhancing LLM reasoning abilities, with policy gradient algor… | arXiv:2508.04848 | high |
| 9 | RL fine-tuning causes significant performance decline across all three non-ideal scenarios, despite gains under idealize… | arXiv:2508.04848 | high |
| 10 | GRPO is a representative policy gradient variant that removes the need for a separate value model, estimating baseline v… | arXiv:2508.04848 | high |
| 11 | Policy gradient approaches are computationally more efficient than Monte Carlo methods because they avoid expensive roll… | arXiv:2508.04848 | high |

## References
- [[1]](https://arxiv.org/abs/2304.10464) arXiv:2304.10464
- [[2]](https://arxiv.org/abs/2309.02144) arXiv:2309.02144
- [[3]](https://arxiv.org/abs/2508.04848) arXiv:2508.04848