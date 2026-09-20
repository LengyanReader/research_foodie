# 2503.16581

## Abstract
## Introduction

## Intro
## Introduction

Retrieval-augmented generation (RAG) has emerged as a promising strategy for grounding large language models (LLMs) in authoritative, contextually appropriate sources, reducing the risk of unsubstantiated or irrelevant output in specialized domains (arXiv:2503.16581). This survey investigates whether RAG grounded in authoritative religious texts meaningfully improves model responses in a specialized domain—Quranic studies—by synthesizing results that compare 13 open-source LLMs on subsets of the Quran's 114 surahs, alongside benchmark evidence from earlier retrieval-based approaches (arXiv:2503.16581; arXiv:2411.18583). Our thesis is that retrieval grounding elevates response faithfulness and relevance, though performance remains unevenly distributed across model sizes, with even small models such as Llama3.2:3b scoring strongly on faithfulness (4.619) and relevance (4.857) (arXiv:2503.16581). The remainder of this survey is organized as follows: Section II describes the datasets and evaluation methodology; Section III discusses the comparative performance of the 13 open-source LLMs and baseline retrieval approaches (arXiv:2411.18583); Section IV analyzes RAG's contribution to grounding, faithfulness, and relevance; and Section V closes with limitations and directions for future work.

## 引言

检索增强生成（RAG）正成为将大型语言模型（LLM）锚定于权威且上下文恰当来源的有效策略，从而降低在专业领域输出缺乏依据或无关内容的风险（arXiv:2503.16581）。本综述围绕《古兰经》研究这一专业领域展开，整理比较 13 个开源 LLM 在古兰经 114 章子集上的评测结果，并结合早期基于检索的方法的基准证据，考察以权威宗教文本为基座的 RAG 能否切实改善模型应答（arXiv:2503.16581; arXiv:2411.18583）。我们的论点是：检索锚定能提升应答的忠实度与相关性，但不同规模模型的表现并不均衡——即便像 Llama3.2:3b 这样的小模型也能在忠实度（4.619）与相关性（4.857）上取得佳绩（arXiv:2503.16581）。全文结构如下：第 II 节介绍数据集与评测方法；第 III 节讨论 13 个开源 LLM 与基准检索方法（arXiv:2411.18583）的性能对比；第 IV 节分析 RAG 在锚定、忠实度与相关性方面的贡献；第 V 节总结局限与未来方向。

## Scope of the study

This study positions domain-specific retrieval-augmented generation (RAG) as its central research technique, applied specifically to Quranic studies. The primary investigation compares 13 open-source large language models to determine whether RAG grounded in authoritative religious texts improves response quality in a specialized domain (arXiv:2503.16581). The corpus scope is deliberately restricted in this preliminary phase: 20 of the 114 surahs were selected and tested (arXiv:2503.16581). Within this scope, the RAG method is reported to guarantee that responses derive from authoritative, contextually appropriate sources, thereby reducing unsubstantiated or irrelevant content (arXiv:2503.16581).

The two source studies diverge markedly in model coverage. arXiv:2503.16581 benchmarks open-source models exclusively — finding that large models consistently outperform smaller ones in capturing query semantics and producing grounded responses, yet also noting that the small Llama3.2:3b scores very well on faithfulness (4.619) and relevance (4.857). In contrast, arXiv:2411.18583 compares three retrieval approaches and reports that the proprietary GPT-3.5-turbo achieved the highest ROUGE-1 score (0.364) among them.

本研究将领域特化的检索增强生成（RAG）定位为核心研究技术，并具体应用于《古兰经》研究。主要工作系统比较 13 个开源大语言模型，判断基于权威宗教文本的 RAG 能否在专业领域改善回答质量（arXiv:2503.16581）。语料范围在前期阶段刻意受限：114 个 surah 中仅选取并测试 20 个（arXiv:2503.16581）；在此范围内，RAG 被报告可确保回答源自权威且上下文适当的来源，从而降低生成无依据或无关内容的风险（arXiv:2503.16581）。

两篇文献在模型覆盖面上存在明显分歧：前者只评估开源模型，发现大模型在捕捉查询语义上一致优于小模型，但小模型 Llama3.2:3b 在忠实性（4.619）与相关性（4.857）上表现优异；后者比较三种检索方法，并指出闭源的 GPT-3.5-turbo 取得最高 ROUGE-1 得分（0.364）。由此留下的开放缺口是：尚无研究在固定语料（全部 114 个 surah 而非 20 个的子集）与固定评估协议的前提下，同时横跨开源与闭源模型进行系统比较。

## Model corpus under evaluation

Both studies evaluate language models of differing scales and provenance, making scale the primary axis along which retrieval-augmented performance is expected to vary. The RAG-for-Quranic-studies study reports that large models consistently outperform smaller models in capturing query semantics and producing accurate, contextually grounded responses (arXiv:2503.16581). Its corpus therefore spans open-weight families from compact to large configurations, allowing RAG-grounded behavior to be compared across model sizes (arXiv:2503.16581).

The scale gradient, however, is not strictly monotonic on every quality axis. The small Llama3.2:3b model scores very well on faithfulness (4.619) and relevance (4.857) (arXiv:2503.16581), a result that sits in tension with the same source's blanket claim that large models consistently outperform smaller ones in capturing query semantics (arXiv:2503.16581). The mismatch is explicit within one study rather than across studies. Separately, in a comparative baseline, GPT-3.5-turbo achieved the highest ROUGE-1 score of 0.364 among the three approaches (arXiv:2411.18583).

Together the two sources imply that the "best model" verdict in a grounded-retrieval corpus depends jointly on the evaluation metric and on the model population under test. The leaders differ across sources (the small open-weights Llama3.2:3b on human-rated faithfulness/relevance versus the proprietary GPT-3.5-turbo on lexical overlap), leaving an open gap: no single study systematically compares open-weight and proprietary families across both human-rated and lexical metrics on the same corpus.

---

两项研究都评估了不同规模与来源的语言模型，规模是考察检索增强性能差异的首要维度。用于《古兰经》研究的 RAG 评测指出，大型模型在捕捉查询语义以及生成准确、有上下文依据的回复方面始终优于较小模型（arXiv:2503.16581）。其语料因而覆盖从紧凑到大型的开源权重系列，以便在不同规模上比较 RAG 的接地表现（arXiv:2503.16581）。

但规模梯度并非在每个质量维度上都单调成立。小型 Llama3.2:3b 模型在忠实度（4.619）与相关性（4.857）上表现非常出色（arXiv:2503.16581），这与同一来源中"大型模型始终优于较小模型"的概括形成明显张力（arXiv:2503.16581）——这一矛盾出现在同一项研究内部，而非跨研究冲突。在另一项对比基线中，GPT-3.5-turbo 在三种方法里取得最高 ROUGE-1 分数 0.364（arXiv:2411.18583）。

综合来看，RAG 语料中"哪个模型最优"的结论同时取决于评测指标与被评估的模型群体。各来源给出的领先者并不一致（小型开源模型 Llama3.2:3b 在人工评分的忠实度/相关性上居首，专有模型 GPT-3.5-turbo 则在词法重叠上领先），由此留下一项开放缺口：尚无单项研究在同一语料上系统比较开源权重与专有模型在人工评分与词法两类指标上的表现。

## Institutional and authorship context

The Quranic RAG benchmark anchoring this survey is the product of a seven-author, four-country collaboration (arXiv:2503.16581). The team spans two Indonesian universities — Universitas Islam Riau (Khalila, Nasution, informatics) and Universitas Lancang Kuning (Monika, library information) — together with Izmir Katip Celebi University in Turkey (Onan), Ritsumeikan University in Japan (Murakami), and, in Malaysia, the Faculty of Al-Quran & Sunnah of Universiti Islam Antarabangsa Tuanku Syed Sirajuddin (UniSIRAJ) (Radi) (arXiv:2503.16581). The pairing of engineering and computer-science departments with an Islamic-studies faculty is well matched to the task, since Quranic scholarship is required both to curate the descriptive surah dataset and to adjudicate the human evaluations of faithfulness and relevance (arXiv:2503.16581).

The survey's second source does not share this institutional profile. arXiv:2411.18583 is authored by a different group — Nurshat Fateh Ali and three co-authors — investigating automated literature review via RAG with GPT-3.5-turbo, and its record offers no comparable four-country authorship context. The two papers therefore agree on RAG's value as a grounding mechanism but diverge in provenance: the institutional and authorship weight behind this survey rests almost entirely on the Quranic study, leaving open how verification and domain-expertise requirements scale when RAG meets other specialized corpora.

中文速览：本综述的核心研究（arXiv:2503.16581）由来自四个国家的七位作者完成，横跨印尼的Universitas Islam Riau与Universitas Lancang Kuning、土耳其的Izmir Katip Celebi大学、日本的立命馆大学以及马来西亚的UniSIRAJ大学；工程/计算机院系与伊斯兰研究院系联合作业，既服务于《古兰经》章节描述数据的策划，也支撑faithfulness与relevance的人工评定。另一来源（arXiv:2411.18583）由不同作者群体（Nurshat Fateh Ali等四人）完成，聚焦GPT-3.5-turbo驱动RAG的文献综述自动化，其记录中没有多国作者背景。两篇论文在RAG作为接地机制的共识上一致，但作者与机构背景并不重叠；本综述的机构叙事几乎全部来自前者，留下一个开放问题：当把RAG迁移到其他专门语料时，验证与领域专业要求如何规模化。

## Related work positioning

This study builds directly on recent applications of retrieval-augmented generation (RAG) to text-understanding and literature-review tasks, most notably the automated literature-review system proposed by Nurshat Fateh Ali, which pits an LLM pipeline against transformer and spaCy frequency-based baselines (arXiv:2411.18583). Both lines of work treat RAG as a grounding mechanism: the Quranic-studies study argues that the RAG method guarantees responses derive from authoritative, contextually appropriate sources, thereby reducing unsubstantiated or irrelevant content (arXiv:2503.16581). This shared premise anchors the present work in the broader turn toward RAG as a grounding layer for specialized, reference-heavy domains.

The two studies diverge in object and evaluation. Fateh Ali measures summary quality with ROUGE-1, where GPT-3.5-turbo attains the top score of 0.364, ahead of the transformer model and spaCy, which ranks last (arXiv:2411.18583). The present study instead rates faithfulness and relevance, finding that large models generally outperform smaller ones at capturing query semantics and producing contextually grounded responses (arXiv:2503.16581), even as the small Llama3.2:3b still scores well on faithfulness (4.619) and relevance (4.857) (arXiv:2503.16581) — an internal tension neither paper resolves.

Because the Quranic work is preliminary, testing only 20 of the 114 surahs (arXiv:2503.16581), while the literature-review work relies on a proprietary model and the SciTLDR corpus of 5,400 TLDRs drawn from over 3,200 papers (arXiv:2411.18583), the open gap is whether RAG grounded in authoritative religious texts generalizes across the full corpus and holds up in fully open-source, comparable settings.

---

中文

本研究的定位紧邻将检索增强生成（RAG）用于文本理解与文献综述任务的最新工作，尤其是 Nurshat Fateh Ali 提出的自动文献综述系统——它在 RAG 管线中对比了大语言模型与 transformer、spaCy 频率基线（arXiv:2411.18583）。两条研究线都把 RAG 视为接地的机制：围绕《古兰经》研究的工作主张，RAG 方法能保证回答源自权威且语境恰当的来源，从而减少无根据或不相关的内容（arXiv:2503.16581）。这一共同前提，把本研究置于"以 RAG 为专业且重引用领域提供接地层"的更广泛潮流之中。

两者在研究对象与评测上分道扬镳。Fateh Ali 用 ROUGE-1 衡量摘要质量，GPT-3.5-turbo 以 0.364 拔得头筹，优于 transformer，spaCy 垫底（arXiv:2411.18583）；本研究则以忠实度与相关性为评分维度，发现大模型通常更能捕捉查询语义、给出准确且语境接地的回答（arXiv:2503.16581），但小模型 Llama3.2:3b 在忠实度（4.619）与相关性（4.857）上依旧亮眼（arXiv:2503.16581）——这一内部张力两份文献均未消解。

鉴于《古兰经》研究尚属初步，仅测试了全部 114 章中的 20 章（arXiv:2503.16581），而文献综述工作依赖专有模型，以及由 3,200 余篇论文提炼出 5,400 条 TLDR 的 SciTLDR 语料（arXiv:2411.18583），留下的开放缺口是:依托权威宗教文本的 RAG 能否在整个语料上泛化，并在完全开源、可对等的环境中保持同等表现。

## Conclusion

This survey set out to test a pointed hypothesis: does retrieval-augmented generation (RAG) grounded in authoritative, domain-specific text actually improve language-model responses in a specialized, high-stakes domain? Across the two pools of evidence surveyed — a 13-model open-source comparison on Quranic studies and an automated literature-review construction — the answer is a qualified **yes**, and the evidence converges on three takeaways.

**RAG grounding works, and it earns its keep precisely where hallucination is costliest.** The primary Quranic study concludes that RAG "enhances the models' performance by grounding answers in external domain-specific knowledge, reducing hallucinations, and ensuring more reliable outputs"; responses derive from authoritative, contextually appropriate sources, thereby lowering the probability of unsubstantiated or irrelevant content (arXiv:2503.16581). This is non-trivial in a religious or culturally sensitive setting, where unsupported output is not merely incorrect but trust-destroying (arXiv:2503.16581).

**Scale helps — but the performance frontier is not set by parameters alone.** Large models consistently outperform smaller ones in capturing query semantics and producing accurate, contextually grounded responses, with 70B-class and 27B models leading on context relevance, answer faithfulness, and answer relevance (arXiv:2503.16581); yet their computational demands pose practical-deployment challenges (arXiv:2503.16581). At the opposite extreme, the small Llama3.2:3b scores very well on faithfulness (4.619) and relevance (4.857), performing comparably to far larger models on those two axes (arXiv:2503.16581). The literature-review pool is directionally consistent: the LLM-based RAG approach achieved the highest ROUGE-1 (0.364), ahead of a fine-tuned transformer (second) and a spaCy frequency baseline (last) over the SciTLDR corpus of 5,400 TLDRs derived from 3,200+ papers (arXiv:2411.18583). Given comparable effort, RAG pipelines beat both extractive and transformer baselines.

**Remaining gaps** (all open as of the surveyed evidence, c. 2026):
- **Thin, preliminary coverage** — only 20 of the 114 surahs were selected and tested, against a single descriptive corpus (arXiv:2503.16581); the summarization pool is likewise confined to SciTLDR (arXiv:2411.18583). Neither study spans the full canon, scholarly commentary (tafsir/fiqh), or dialectal and multilingual use.
- **No domain-expert adjudication** — quality rests on human-evaluator rubrics (context relevance, answer faithfulness, answer relevance) (arXiv:2503.16581) and on surface-level ROUGE scores that remain modest (best 0.364) (arXiv:2411.18583); no evaluation by religious scholars is reported, and ROUGE has no demonstrated correlation with theological or hermeneutic accuracy.
- **Accuracy-vs-deployability tension** — high-accuracy large (70B/27B-class) models are computationally impractical, while the small-model result is confined to faithfulness/relevance on a 20-surah slice (arXiv:2503.16581); the optimal size trade-off for production systems is unresolved.
- **Openness asymmetry** — the Quranic comparison is fully open-source by design, yet the best-scoring RAG system in the literature-review pool is the closed GPT-3.5-turbo (arXiv:2411.18583); an open model that reproduces that ceiling has yet to be demonstrated.

The practical reading is clear: RAG grounded in authoritative texts raises both fidelity and trustworthiness in specialized domains, and open-weights architectures can approach that bar without frontier-scale compute — but the evidence base is still too small and too single-corpus to license deployment decisions without expert checkpoints.

> ### 结论
> 本综述检验的假设很直接：在权威化领域文本上做检索增强生成（RAG），是否真的能改善大模型在专业、高风险场景下的回答质量。在两个证据池（13 个开源模型《古兰经》研究对比、自动文献综述构建）上，答案是有保留的**肯定**，证据收敛为三个要点。
> **RAG 接地有效，且恰好在幻觉代价最高的地方最有价值。** 古兰经研究的主要结论是 RAG"将答案锚定在外部领域知识上，减少幻觉并提升输出可靠性"；回答基于权威且语境恰当的来源，降低凭空捏造或无关内容的概率（arXiv:2503.16581）。在宗教或文化敏感场景中，未经证实的输出不只是错误，更会摧毁信任（arXiv:2503.16581）。
> **模型规模重要，但性能上限不由参数量单独决定。** 大模型在捕捉查询语义与生成准确、接地回答上稳定胜过小模型，70B 级与 27B 级模型在语境相关度、回答忠实度与相关度上领先（arXiv:2503.16581），但计算需求制约实际部署（arXiv:2503.16581）；相反，小模型 Llama3.2:3b 在忠实度（4.619）与相关度（4.857）上表现优异（arXiv:2503.16581）。文献综述池方向一致：基于 LLM 的 RAG 取得最高 ROUGE-1（0.364），胜过微调 transformer（第二）与 spaCy 频率基线（最末），语料为 3,200 余篇论文、5,400 条 TLDR 的 SciTLDR（arXiv:2411.18583）。同等投入下，RAG 管线同时击败抽取式与基于 transformer 的基线。
> **剩余缺口**（截至证据调查时，约 2026 年）：① **覆盖仍初步**——仅测试 114 章的 20 章、单一描述性语料（arXiv:2503.16581），综述池亦限于 SciTLDR（arXiv:2411.18583），未覆盖全本经卷、注疏（tafsir/fiqh）或方言与多语言使用；② **缺乏领域专家评审**——质量依赖人工评分表（语境相关度、忠实度、相关度）（arXiv:2503.16581）与仍偏低的表层 ROUGE（最高 0.364）（arXiv:2411.18583），未见宗教学者评审，ROUGE 与神学/诠释准确性无已验证关联；③ **精度与可部署性矛盾未解**——高精度大模型（70B/27B）计算成本过高，小模型优势也仅限 20 章切片上的忠实度/相关度（arXiv:2503.16581）；④ **开放性不对称**——《古兰经》对比全程开源，但综述池中得分最高的却是闭源 GPT-3.5-turbo（arXiv:2411.18583），尚无开源模型证明能达到该上限。
> 实务结论：以权威文本为锚的 RAG 能同时提升专业领域的忠实度与可信度，开源权重架构也有望不靠前沿计算逼近该水平——但现有证据面仍过窄、过于单一语料，不足以为部署决策背书，需保留专家检查点。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Large models consistently outperform smaller models in capturing query semantics and producing accurate, contextually gr… | arXiv:2503.16581 | high |
| 2 | The small Llama3.2:3b model scores very well on faithfulness (4.619) and relevance (4.857). | arXiv:2503.16581 | high |
| 3 | The RAG method guarantees responses derive from authoritative, contextually appropriate sources, reducing unsubstantiate… | arXiv:2503.16581 | high |
| 4 | In this preliminary study, 20 of the 114 surahs were selected and tested. | arXiv:2503.16581 | high |
| 5 | The GPT-3.5-turbo LLM achieved the highest ROUGE-1 score of 0.364 among the three approaches. | arXiv:2411.18583 | high |
| 6 | The transformer model ranked second and spaCy ranked last in the evaluation. | arXiv:2411.18583 | high |
| 7 | The SciTLDR dataset comprises 5,400 TLDRs derived from over 3,200 papers. | arXiv:2411.18583 | high |
| 8 | The spaCy frequency-based approach selects the top 10 percent of sentences as the summary output. | arXiv:2411.18583 | medium |

## References
- [[1]](https://arxiv.org/abs/2503.16581) arXiv:2503.16581
- [[2]](https://arxiv.org/abs/2411.18583) arXiv:2411.18583