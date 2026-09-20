# 2510.15253

## Abstract
## 1. Introduction

## Intro
## 1. Introduction

As organizations ingest documents that fuse text, tables, charts, and layout into a single artifact, a fundamental scaling question arises: when text-centric retrieval pipelines discard the very cross-modal cues and structural semantics such visually rich documents encode (arXiv:2510.15253), how can Retrieval-Augmented Generation (RAG) retrieve and reason across modalities? This survey is anchored by what arXiv:2510.15253 establishes — the first systematic treatment that explicitly connects multimodal RAG and document understanding: it shows that current multimodal RAG benchmarks require 20–200M visual tokens, far exceeding the typical 128K–1M context limits of existing MLLMs, and argues that documents' intrinsic multimodality therefore "demands a more advanced paradigm: Multimodal RAG," moving beyond static, single-modality retrieval. Complementary primary sources show retrieval augmentation spreading across the generation and retrieval stack — autoregressive patch-level retrieval for image generation (arXiv:2506.06962) and co-evolving queries and knowledge bases for code generation (arXiv:2402.12317). The remainder unfolds as follows: Section 2 grounds the problem domain and the token/context bottleneck; Section 3 presents a taxonomy of Multimodal RAG for document understanding across domain, retrieval modality, and granularity; Section 4 synthesizes the primary-source evidence base, including AR-RAG (arXiv:2506.06962) and EVOR (arXiv:2402.12317); Section 5 reviews benchmarks, applications, and open challenges; Section 6 concludes with a research roadmap.

> 中文速览：当组织摄入融合文字、表格、图表与布局的文档时，一个根本性的扩展问题随之浮现——以文本为中心的检索管道恰恰丢弃了这类文档所承载的跨模态线索与结构语义（arXiv:2510.15253），检索增强生成（RAG）究竟如何跨模态完成检索与推理？本综述围绕 arXiv:2510.15253 确立的结论展开——这是首个明确将多模态 RAG 与文档理解联系在一起的系统性调研：它表明当前多模态 RAG 基准所需 2000万–2亿 个视觉 token 远超现有 MLLM 12.8万–100万 的上下文上限，并论证文档内在的多模态特性决定了必须转向"多模态 RAG"这一更高级范式，而非静态、单模态的检索。互补的一手来源显示，检索增强正在向生成与检索全栈扩散：面向图像生成的补丁级自回归检索（arXiv:2506.06962），以及面向代码生成、查询与知识库协同进化的检索（arXiv:2402.12317）。本文结构如下：第2节界定问题域与 token/上下文瓶颈；第3节给出面向文档理解的多模态 RAG 分类体系（领域、检索模态、粒度）；第4节综合一手证据基，涵盖 AR-RAG（arXiv:2506.06962）与 EVOR（arXiv:2402.12317）；第5节回顾基准、应用与开放挑战；第6节总结并提出研究路线图。

## Overview

arXiv:2510.15253 establishes multimodal document understanding as a pressing, unresolved problem. The authors ground the need for Multimodal RAG in a scale gap: current multimodal RAG benchmarks require 20–200M visual tokens, far exceeding the typical 128K–1M context limits of existing MLLMs (arXiv:2510.15253). They further argue that text-based retrieval approaches exhibit fundamental limitations on visually rich documents, because such approaches fail to adequately capture cross-modal cues and structural semantics (arXiv:2510.15253).

Because documents combine text, tables, charts, and layout, their multimodal nature demands a more advanced paradigm — Multimodal RAG (arXiv:2510.15253). On this diagnosis, the authors present the first comprehensive survey that explicitly connects multimodal RAG and document understanding, structuring the field around this link (arXiv:2510.15253).

The gap this leaves is twofold: the "first" framing is an unverified positioning claim, and—more decisively—the token-scale mismatch the survey identifies remains an open problem rather than a solved method, leaving benchmark-scale retrieval within tractable context budgets unaddressed.

---

arXiv:2510.15253 将多模态文档理解确立为一个紧迫且尚未解决的问题。作者以规模差距为论据指出多模态 RAG 的必要性：当前多模态 RAG 基准需消耗 20–200M 视觉 token，远超现有 MLLM 通常的 128K–1M 上下文上限（arXiv:2510.15253）。他们进一步指出，基于文本的检索方法在处理视觉丰富文档时存在根本局限，因其无法充分捕捉跨模态线索与结构语义（arXiv:2510.15253）。

由于文档是文本、表格、图表与版式的组合，其多模态本质要求更高级的范式——多模态 RAG（arXiv:2510.15253）。在此诊断之上，作者呈现了首篇将多模态 RAG 与文档理解显式贯通的全景综述，并据此组织领域版图（arXiv:2510.15253）。

综述留下的开放空缺有二：其一，"首篇"地位属尚待验证的角色声明；其二，也是更关键的——其所识别的 token 规模失衡仍是未解决的工程难题，如何在可负担的上下文预算内完成文档级检索，尚未得到解答。

## 7 Conclusion

> 中文速览：本综述以"超越上下文窗口"为线索，回答了 arXiv:2510.15253 所确立的核心命题——视觉丰富的文档理解已超出 MLLM 的上下文极限（现有基准需 20–200M 视觉 token，而典型上下文仅 128K–1M），因此必须从"塞进上下文"转向"检索式扩展"的多模态 RAG 范式。主体贡献有三：(1) 方法论分类（开放/封闭域、检索模态、检索粒度、图/智能体混合增强）；(2) 数据集、基准与评测指标的整合；(3) 应用画像（金融、科研、社会调查）。两个佐证把前沿推得更细：AR-RAG (arXiv:2506.06962) 将检索从"整页静态"推进到 patch 级、逐布(step-wise)自回归的 k-最近邻检索，经训练无关的解码期分布增强（DAiD）融合，Janus-Pro+FAiD 在 Midjourney-30K 达 6.67 FID、GenEval 0.78；EVOR (arXiv:2402.12317) 证明查询与知识库须"同步演化"，执行准确率较 Reflexion 高 2–4 倍、较 DocPrompting 高 18.6%。剩余缺口集中在效率（token 预算、检索循环延迟与能耗）、细粒度跨模态表征，以及真实部署中的鲁棒性、失控与隐私安全。

This survey set out to answer one question — what does the multimodal-RAG–document-understanding literature actually establish — and the synthesis of arXiv:2510.15253 with its two complementary case studies yields a three-part answer.

**First, the motivating crisis is one of context, not of quality.** Current multimodal RAG benchmarks require 20–200M visual tokens while existing MLLMs hold only 128K–1M context windows (arXiv:2510.15253). Long-context scaling alone cannot close that gap, so retrieval becomes the only way to *scale beyond context*; and because documents interleave text, tables, charts, and layout, text-only OCR-centric pipelines miss exactly the cross-modal cues and structural semantics that make them hard to read (arXiv:2510.15253). Multimodal RAG is thus established not as an optional convenience but as the defining paradigm for visually rich document AI.

**Second, the design space is mapped but unsettled.** The survey (arXiv:2510.15253) organizes the field along four axes — open vs. closed domain, retrieval modality, retrieval granularity, and graph-/agent-based hybrid enhancements — and consolidates the datasets, benchmarks, and retrieval/generation metrics the community uses to measure itself. The two exemplars expose the live seams. AR-RAG (arXiv:2506.06962) shows granularity is the frontier: replacing static whole-image retrieval with patch-level, per-step k-NN retrieval merged at decode time through a training-free distribution augmentation (DAiD) improves object and spatial-relation coherence across GenEval, DPG-Bench, and Midjourney-30K, with Janus-Pro + FAiD reaching 6.67 FID and 0.78 on GenEval. EVOR (arXiv:2402.12317) shows the knowledge base is not static either: synchronously evolving both queries and diverse knowledge bases delivers two to four times the execution accuracy of Reflexion and +18.6% over DocPrompting (CodeLlama), reframing retrieval from "searching a fixed corpus" to "co-evolving the corpus with the query."

**Third, the remaining gaps are consistent and concrete.** (i) *Efficiency* dominates: the token mismatch at the field's core persists (arXiv:2510.15253), and the iterative retriever–generator–executor loops of AR-RAG and EVOR carry latency and energy costs that both works explicitly flag for real-time, energy-constrained deployment (arXiv:2506.06962; arXiv:2402.12317). (ii) *Fine-grained multimodal representation* remains immature in both directions — behind, from pages to patches; ahead, from pages to elements/tables/charts — and graph/agent hybrids trade coverage for coordination overhead (arXiv:2510.15253). (iii) *Robustness and security* in deployment are only preliminarily handled: hallucination and misinformation, plus the privacy and integrity of retrieved snippets and code (arXiv:2402.12317; ethics discussion in arXiv:2510.15253). (iv) *Evaluation is fragmented*: numerous recent one-off benchmarks leave open questions about annotation consistency, inter-domain transferability, and alignment across modalities (arXiv:2510.15253).

Taken together, arXiv:2510.15253 establishes that multimodal RAG is the necessary and now-systematized backbone for document understanding, and that the next bottleneck is no longer "which components exist," but how to make retrieval fine-grained, cheap, and safe at scale.

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Current multimodal RAG benchmarks require visual token counts that far exceed the context limits of existing MLLMs. | arXiv:2510.15253 | high |
| 2 | Text-based retrieval approaches fail to capture cross-modal cues and structural semantics in visually rich documents. | arXiv:2510.15253 | high |
| 3 | This paper presents the first comprehensive survey that explicitly connects multimodal RAG and document understanding. | arXiv:2510.15253 | high |
| 4 | Documents' multimodal nature combining text, tables, charts, and layout demands a more advanced paradigm: Multimodal RAG… | arXiv:2510.15253 | high |
| 5 | AR-RAG enhances image generation by autoregressively incorporating patch-level k-nearest neighbor retrievals at each gen… | arXiv:2506.06962 | high |
| 6 | Unlike static retrievals of entire reference images, AR-RAG performs fine-grained, step-wise retrieval at the image patc… | arXiv:2506.06962 | high |
| 7 | DAiD is a training-free decoding strategy that merges the distribution of model-predicted patches with the distribution … | arXiv:2506.06962 | high |
| 8 | Janus-Pro with FAiD achieves 6.67 FID on Midjourney-30K and 0.78 overall score on GenEval. | arXiv:2506.06962 | high |
| 9 | EVOR employs synchronous evolution of both queries and diverse knowledge bases in RACG | arXiv:2402.12317 | high |
| 10 | EVOR achieves two to four times the execution accuracy of methods like Reflexion and DocPrompting | arXiv:2402.12317 | high |
| 11 | EVOR beats DocPrompting by 18.6% on average with CodeLlama | arXiv:2402.12317 | high |
| 12 | EVOR-BENCH's Scipy/Tensorflow datasets are adapted from DS-1000 to modified library versions | arXiv:2402.12317 | high |

## References
- [[1]](https://arxiv.org/abs/2510.15253) arXiv:2510.15253
- [[2]](https://arxiv.org/abs/2506.06962) arXiv:2506.06962
- [[3]](https://arxiv.org/abs/2402.12317) arXiv:2402.12317