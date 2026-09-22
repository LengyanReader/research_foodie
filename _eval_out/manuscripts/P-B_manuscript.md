# 2304.02819

## Abstract
**Intro**

## Intro
**Intro**

Whether GPT-output classifiers are trustworthy across populations has become a central question as such detectors are woven into academic-integrity pipelines. This survey advances the thesis, grounded in arXiv:2304.02819, that these detectors are systematically biased against non-native English writers—misclassifying over half of human-written TOEFL essays as AI-generated (61.22% average false-positive rate) while showing native-like phrasing sharply reduces that rate. We first synthesize the detection-bias evidence, then examine the linguistic mechanism linking abstract perplexity to authorship, review proposed mitigation strategies, and close with open methodological directions.

> **中文速览**：随着 AI 文本分类器进入学术诚信审查流程，检测器在不同人群间的可靠性成为关键问题。本综述依据 arXiv:2304.02819 论证一个核心论点——现有检测器对非母语英语写作者存在系统性偏见，将超过半数的人类 TOEFL 作文误判为 AI 生成（平均误报率 61.22%），而越接近母语风格、误报率越低。我们依次梳理检测偏差证据、困惑度与作者来源之间的语言学机制、缓解策略，并讨论未来开放方向。

Line 9 was truncated. Let me get the full claims JSON.## Overview

Liang et al. establish that commercial and open GPT detectors systematically misclassify the prose of non-native English writers as AI-generated: across several detectors, over half of TOEFL essays were flagged as "AI-generated," with an average false positive rate of 61.22% (arXiv:2304.02819). The bias tracks surface statistics rather than authorship itself: ICLR 2023 abstract authors based in non-native English-speaking countries wrote significantly lower-perplexity texts than their native-English counterparts (p = 0.035) (arXiv:2304.02819), and that lower-perplexity register is precisely what detectors treat as machine-like.

Two implications follow. First, the bias is treatable through style: rephrasing TOEFL essays toward more native-like word choices cut the average false positive rate by 49.45%, from 61.22% to 11.77% (arXiv:2304.02819). Second, it is exploitable in the opposite direction: a second-round self-edit prompt on ChatGPT-3.5 ("Elevate the provided text by employing literary language") dropped the detection rate of generated essays from 100% to 13% (arXiv:2304.02819). Because these findings come from a single source, there is no cross-study disagreement to reconcile; the open gap is that detectors remain calibrated against native-like English, so their scores conflate form with provenance — leaving unmodeled how both this bias and its bypass shift as detectors, language models, and human writing styles co-evolve.

中文速览：Liang et al. 证明现有 GPT 检测器系统性误判非母语作者的英文——在 TOEFL 作文上平均 61.22% 被误标为 AI 生成（arXiv:2304.02819）。偏差源于表面风格而非真实来源：ICLR 2023 非母语国家作者所写摘要困惑度显著更低（p=0.035）（arXiv:2304.02819）。将作文改写为更接近母语者的措辞可使误判率从 61.22% 降至 11.77%（arXiv:2304.02819）；反之，对 ChatGPT-3.5 施加第二轮"文学化语言"改写提示即可将 AI 文本检出率从 100% 压至 13%（arXiv:2304.02819）。上述证据均出自单一来源，无冲突需要调和；开放缺口在于：检测器以"母语化文本"为校准基准，形式上把文本风格与来源真伪混为一谈，而对这一偏差及其绕过手段随检测器与语言模型共同演进时的漂移，尚无建模。

## Conclusion

This survey synthesized the evidence on bias in AI-text detectors when applied to non-native English writers, anchored primarily in a controlled study of GPT detectors (arXiv:2304.02819). The headline finding is unambiguous: detectors misclassify **over half of non-native (TOEFL) essays** as AI-generated, with an average false positive rate of 61.22% (arXiv:2304.02819). This bias is not a labeling artifact but a linguistic signature — ICLR 2023 authors based in non-native English-speaking countries wrote abstracts with **significantly lower perplexity** than their native-English counterparts (P = 0.035), meaning detectors tend to flag clear, predictable prose as machine-generated (arXiv:2304.02819). Crucially, the bias is reversible at both ends of the pipeline. On the *writer/honest-author* side, enhancing word choices toward native-like language cut the average TOEFL false positive rate from 61.22% to 11.77%; on the *adversarial-author* side, a second-round self-edit prompt on ChatGPT-3.5 reduced detection of AI-generated essays from 100% to 13% (arXiv:2304.02819).

Two practical takeaways follow. First, current detectors are **not reliable as decision tools for authorship** — they systematically penalize non-native writers while simultaneously failing to catch minimally-paraphraseable AI text, making them unfair for assessment and weak for enforcement. Second, the gap between detector capability and both honest and adversary behavior suggests detection accuracy alone is a poor proxy for intent; any deployment must be calibrated against the demographics of the population it screens.

Remaining gaps in the survey's scope: (i) the mitigation (11.77%) and self-edit (13%) results derive from a single study; no replication exists across newer model families or larger datasets; (ii) the residual false-positive floor after such interventions, and its variance across native language backgrounds, remains uncharacterized; (iii) the causal link between the perplexity signal and detection outcomes is established directionally but not quantified as an effect size or decision threshold; and (iv) practical guidance — e.g., recommended probability thresholds, calibration procedures, and disclosure norms — is still absent from the primary literature.

> 中文速览
>
> 本综述以 arXiv:2304.02819 为核心证据，系统梳理了 AI 文本检测器对非英语母语作者的偏见。核心结论：
> 1. **偏见证实**：约六成（61.22%）非母语 TOEFL 作文被误判为 AI 生成（arXiv:2304.02819）；ICLR 2023 非母语作者的摘要困惑度显著更低（P=0.035），说明检测器把"用词简洁、可预测"的写作误当机器产出（arXiv:2304.02819）。
> 2. **偏见可逆**：从诚实作者端，将用词提升至母语水平后误报率从 61.22% 降至 11.77%；从对抗端，对 ChatGPT-3.5 输出的二次自编辑提示使检出率从 100% 降至 13%（arXiv:2304.02819）。
> 3. **实践含义**：现有检测器既不公平（误伤非母语者）又不可靠（漏掉易改写的 AI 文本），不宜单独作为判定工具，须按被筛查人群做校准。
> 4. **剩余空白**：缓解与对抗结果均为单篇小规模证据，缺乏跨新模型（GPT-4、Llama 等）的复现；干预后的误报下限、困惑度信号的效应量与判定阈值、以及实际使用中的阈值/校准/披露规范均未在原始文献中给出。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | GPT detectors misclassify over half of non-native (TOEFL) essays as AI-generated, averaging a 61.22% false positive rate… | arXiv:2304.02819 | high |
| 2 | Enhancing word choices toward native-like language cut the average false positive rate for TOEFL essays from 61.22% to 1… | arXiv:2304.02819 | high |
| 3 | ICLR 2023 authors from non-native English-speaking countries wrote abstracts with significantly lower perplexity than na… | arXiv:2304.02819 | high |
| 4 | A second-round self-edit prompt applied to ChatGPT-3.5 reduced detection rates of AI-generated essays from 100% to 13%. | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819