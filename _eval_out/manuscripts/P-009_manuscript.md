# 2403.04279

## Abstract
**EN**

## Intro
**EN**

Controllable text-to-image (T2I) generation remains an open question: although modern diffusion models produce photorealistic images from text, relying solely on text conditioning does not fully satisfy the varied and complex requirements of different applications and scenarios (arXiv:2403.04279). This survey answers the question by establishing a systematic, condition-perspective taxonomy of controllable generation, organizing methods by the type of condition faithfully injected into a pre-trained T2I model—from global conditions such as style and subject affinity to local, spatially grounded conditions—thereby unifying the theoretical foundations of diffusion, flow matching, latent diffusion, and diffusion transformers with practical advances for steering models beyond pure text input (arXiv:2403.04279). The rest of this paper is organized as follows: Section 2 reviews the theoretical foundations of T2I diffusion models; Section 3 introduces our condition-based taxonomy of controllable generation; Section 4 surveys representative methods and applications under each condition type; Section 5 discusses open challenges and future directions; Section 6 concludes.

**中文**

可控文生图（T2I）仍是核心问题：现代扩散模型虽能以文本生成逼真图像，但仅依赖文本条件并不能完全满足不同应用与场景的多样复杂需求（arXiv:2403.04279）。本综述从「条件」的统一视角出发，提出系统的可控生成分类法——按注入预训练 T2I 模型的条件类型（从风格、主体等全局条件到空间约束的局部条件）组织方法，并把扩散、流匹配、潜空间扩散、扩散 Transformer 等理论基础与实际的可控生成进展贯通起来（arXiv:2403.04279）。全文结构如下：第2节回顾 T2I 扩散模型的理论基础；第3节给出面向条件的可控生成分类法；第4节分条件类型综述代表性方法与实际应用；第5节讨论开放挑战与未来方向；第6节总结。

## Scope and intended contribution of the survey

This survey consolidates both theoretical foundations and practical advancements in controllable generation with text-to-image (T2I) diffusion models, organizing the field through a systematic, condition-perspective taxonomy (arXiv:2403.04279). Its motivation rests on a documented shortfall: relying solely on text for conditioning pre-trained T2I models does not fully cater to the varied and complex requirements of different applications and scenarios, so the work reviews literature that steers pre-trained T2I models to support novel conditions beyond pure text (arXiv:2403.04279). From this premise the survey builds outward: among denoising formulations it focuses on flow matching because it underpins many state-of-the-art T2I systems such as Stable Diffusion 3 and Flux, while tracing complementary efficiency and architectural lineages — Latent Diffusion Models, which broke a major efficiency barrier by performing diffusion in a compressed latent space, and Diffusion Transformers, which treat image latents as patch tokens and denoise entirely through self-attention (arXiv:2403.04279).

The review's contribution is therefore twofold: it bridges theoretical machinery and practical systems, and it frames condition-based control — rather than text alone — as the organizing lens for the field. Because all four supporting claims issue from a single source, no internal conflict arises; the open gap this leaves is external validity. The taxonomy, and its ranking of techniques (notably the prominence granted to flow matching), are single-paper judgments that later, independently authored surveys have yet to corroborate.

> 中文速览
> 本综述以"条件控制视角"为组织主轴，系统整合可控文本到图像（T2I）扩散模型的理论基础与实践进展，并给出文献分类体系（arXiv:2403.04279）。其出发点是一个公认缺口：仅靠文本提示调节预训练 T2I 模型，无法充分满足不同应用与场景的多样化复杂需求，故该综述聚焦于引导预训练模型支持文本之外的新型条件（arXiv:2403.04279）。在此基础上，它在去噪框架中重点讨论流匹配（flow matching），因其支撑了 Stable Diffusion 3、Flux 等主流系统；同时梳理了两条互补的技术脉络——在压缩潜空间执行扩散以取得效率突破的潜扩散模型，以及将图像潜变量视为 patch token、完全以自注意力完成去噪的扩散 Transformer（arXiv:2403.04279）。该综述的贡献有二：其一，在理论机制与实践系统之间架起桥梁；其二，把"基于条件的控制"（而非仅有文本）确立为组织该领域的核心视角。由于上述四点均出自同一篇文献，来源内部并无分歧；留下的开放缺口在于外部效度——其分类体系与技术优先级排序仍属单篇论文的判断，尚待后续独立撰写的综述加以印证。

## Theoretical foundations covered

The survey grounds its condition-perspective taxonomy in a compact review of theoretical foundations (arXiv:2403.04279). It begins from the observation that relying solely on text for conditioning does not fully cater to the varied and complex requirements of different applications and scenarios, which motivates control beyond pure text prompts (arXiv:2403.04279). Within the basics of denoising diffusion probabilistic models (DDPMs), the survey deliberately focuses on the flow-matching technique, since it underpins many state-of-the-art text-to-image systems such as Stable Diffusion 3 and Flux (arXiv:2403.04279). This single-source framing yields a coherent baseline for the survey rather than a pluralistic comparison of rival theories.

The foundation review then turns to widely used text-to-image (T2I) diffusion models, which serve as the substrate for the control methods surveyed (arXiv:2403.04279). Two architectural advances are highlighted: Latent Diffusion Models achieved a major efficiency breakthrough by performing diffusion in a compressed latent space, and Diffusion Transformers treat image latents as patch tokens while denoising entirely through self-attention (arXiv:2403.04279). Because every claim in this section traces to a single source, the findings agree by construction and no explicit disagreements surface — but this leaves an open gap: the theoretical coverage is bounded by the survey's own focus on flow matching and recent architectures, so alternative diffusion-theoretic foundations are not independently cross-checked here.

该综述以"条件（condition）视角"的分类学为框架，从扩散模型的基础入手梳理理论基础（arXiv:2403.04279）。其出发点是：仅依赖文本进行条件化并不能完全满足不同应用与场景的复杂需求，因此需要超越纯文本提示的引导控制（arXiv:2403.04279）。在去噪扩散概率模型（DDPM）基础部分，综述着重介绍 flow matching 技术，因为它支撑了诸如 Stable Diffusion 3 与 Flux 等众多最先进的文生图（T2I）系统（arXiv:2403.04279）。随后转向广泛使用的 T2I 扩散模型，将其作为各类控制方法的基座（arXiv:2403.04279）。其中重点介绍了两项架构进展：潜在扩散模型通过在压缩潜在空间中执行扩散带来显著的效率突破；扩散 Transformer 则将图像潜变量视为 patch 令牌，并完全通过自注意力完成去噪（arXiv:2403.04279）。由于本部分的全部论断均出自 arXiv:2403.04279 这一单一来源，各处说法彼此一致、不存在显式冲突，但也因此留下空白：对扩散理论基础（尤其是非 flow-matching 路径）的覆盖受限于该综述自身的取舍，未在本节中得到独立的交叉验证。

## Core organizing taxonomy: the condition perspective

The survey's organizing taxonomy is the "condition perspective": rather than treating text prompts as the sole control signal, it argues that relying solely on text for conditioning does not fully cater to the varied and complex requirements of different applications and scenarios (arXiv:2403.04279). From this premise, prior work on controllable generation is grouped into three directions: generation with specific conditions, generation with multiple conditions, and universal controllable generation (arXiv:2403.04279). This decomposition positions conditioning itself — rather than the model architecture — as the axis along which controllability is understood.

Underlying these directions, the survey focuses on the flow-matching technique because it underpins many state-of-the-art text-to-image systems such as Stable Diffusion 3 and Flux (arXiv:2403.04279). Two further techniques support conditioning in practice: latent diffusion models introduced a major efficiency breakthrough by performing diffusion in a compressed latent space (arXiv:2403.04279), and Diffusion Transformers treat image latents as patch tokens and perform denoising entirely through self-attention (arXiv:2403.04279).

All claims in this section trace to a single survey, so their evidence agrees rather than conflicts; there is no genuine cross-source disagreement to reconcile (arXiv:2403.04279). The open gap the condition perspective leaves is therefore external: the three-way split into specific, multiple, and universal conditioning stands as a framework assertion, but balanced validation of each direction demands reference to the primary works this survey compiles, beyond its own synthesizing view (arXiv:2403.04279).

该综述以"条件视角"（condition perspective）作为核心组织框架：与其把文本提示词当作唯一控制信号，它认为单靠文本进行条件控制并不能完全满足不同应用与场景的多样而复杂的需求（arXiv:2403.04279）。由此出发，可控生成的研究被归纳为三个方向：特定条件下的生成、多条件生成，以及通用可控生成（arXiv:2403.04279）。这种划分把"条件"本身——而非模型架构——作为理解可控性的主轴。

支撑这些方向的底层技术上，该综述聚焦于流匹配（flow matching），因为它支撑着 Stable Diffusion 3、Flux 等众多最先进的文生图系统（arXiv:2403.04279）。另外两项技术在实际条件控制中很关键：潜在扩散模型通过在压缩的潜在空间中执行扩散过程实现了重大的效率突破（arXiv:2403.04279）；扩散 Transformer 则将图像潜在表示视为补丁令牌（patch tokens），完全通过自注意力完成去噪（arXiv:2403.04279）。

本节所有主张均出自同一篇综述，其证据相互一致而非冲突，并没有真正需要调和的跨来源分歧（arXiv:2403.04279）。条件视角由此留下的开放空白是外部的：将研究划分为特定、多重与通用条件控制三个方向属于框架层面的论断，要对每一方向做出均衡验证，仍需回溯该综述所汇编的原始文献，而非仅依赖其自身的综合视角（arXiv:2403.04279）。

## Analysis approach per category

The survey organizes controllable T2I generation through a condition-perspective taxonomy, and for each category it analyzes the underlying control mechanism that steers a pre-trained model beyond pure text conditioning (arXiv:2403.04279). The motivation is explicit: relying solely on text for conditioning does not fully cater to the varied and complex requirements of different applications and scenarios (arXiv:2403.04279). Each category is therefore examined in terms of how its specific conditioning signal enters and flows through the generation process, rather than treated as an isolated trick.

Within each category, the survey reviews representative methods based on their core techniques. Those techniques are anchored to the backbone they build upon: Latent Diffusion Models introduced a major efficiency breakthrough by performing diffusion in a compressed latent space (arXiv:2403.04279), while Diffusion Transformers treat image latents as patch tokens and perform denoising entirely through self-attention (arXiv:2403.04279). The survey further focuses on the flow-matching technique, as it underpins many state-of-the-art text-to-image systems such as Stable Diffusion 3 and Flux (arXiv:2403.04279).

Synthesizing across these choices, the per-category analysis reveals that the control mechanism is deeply coupled to the generative backbone — the same conditioning signal is realized differently in latent-space diffusion, self-attention DiT, and flow-matching pipelines. Because only one source underpins this section, no disagreements emerge; the open gap is that a condition-centric taxonomy, while systematic, leaves cross-category combinations of control signals — and how they interact inside a single backbone — largely unexplored (arXiv:2403.04279).

---

## 各分类的分析方法 / Analysis per category

该综述以条件视角（condition-perspective）构建可控 T2I 生成的分类框架，对每一类都深入分析其底层的控制机制——即如何在纯文本条件之外对预训练模型进行引导（arXiv:2403.04279）。其动机十分明确：仅依赖文本进行条件控制，并不能完全满足不同应用与场景中多样而复杂的需求（arXiv:2403.04279）。因此，每个类别都被置于"特定条件信号如何进入并流经生成过程"的视角下考察，而非当作孤立技巧处理。

在每个类别内部，综述依据各方法的**核心技术**进行代表性综述。这些技术锚定于它们所依赖的骨干模型：Latent Diffusion Models 通过在压缩潜空间中执行扩散，实现了重大的效率突破（arXiv:2403.04279）；Diffusion Transformers 则将图像潜变量视为 patch token，完全通过自注意力完成去噪（arXiv:2403.04279）。综述还特别聚焦于 flow-matching 技术，因为它支撑了 Stable Diffusion 3 与 Flux 等众多先进文生图系统（arXiv:2403.04279）。

综合而言，逐类分析表明控制机制与生成骨干深度耦联——同一条件信号在潜空间扩散、自注意力 DiT 与 flow-matching 管线中的实现方式各不相同。由于本节仅基于单一来源，不存在观点冲突；遗留的开放缺口在于：这种以条件为核心的分类虽然系统化，却较少探索跨类别的控制信号组合，以及它们在单一骨干内部如何相互作用（arXiv:2403.04279）。

## Companion resources and framing

Beyond its technical chapters, arXiv:2403.04279 ships a companion resource: the survey maintains an exhaustive, curated list of controllable text-to-image (T2I) diffusion literature in a public GitHub repository (https://github.com/PRIV-Creation/Awesome-Controllable-T2I-Diffusion-Models), an index that follows the field as it grows (arXiv:2403.04279). The survey positions controllable generation within the broader AI-generated content (AIGC) context, as reflected in its index terms (arXiv:2403.04279).

Framing and resource reinforce each other. The survey's motivating claim is that relying solely on text to condition T2I diffusion models does not fully cater to the varied and complex requirements of different applications and scenarios (arXiv:2403.04279). Text-only prompting is thus treated as the baseline, and the survey's whole subject — steering pre-trained T2I models beyond pure text conditioning, from theoretical foundations to practical advances — is organized around that gap (arXiv:2403.04279). The curated repository makes the taxonomy's scope concrete, while the framing gives its entries their purpose (arXiv:2403.04279).

What remains open is the step from cataloguing to choosing: a curated list and a condition-perspective taxonomy describe what controllers exist, but neither quantifies how far text-only prompting falls short nor offers selection criteria for a given workflow. The companion repository likewise inherits a maintenance hazard — its exhaustiveness is only as current as its latest update — a constraint any living survey must continuously manage (arXiv:2403.04279).

## 配套资源与定位

除技术章节外，arXiv:2403.04279 附带一项配套资源：该综述在公开的 GitHub 仓库中维护着可控文生图（T2I）扩散文献的详尽精选清单（https://github.com/PRIV-Creation/Awesome-Controllable-T2I-Diffusion-Models），随领域发展持续更新（arXiv:2403.04279）。综述将可控生成置于更广泛的 AI 生成内容（AIGC）语境中，这一定位反映在其索引词上（arXiv:2403.04279）。

定位与资源相互印证。综述的核心动因是：仅依靠文本对 T2I 扩散模型进行条件控制，无法完全满足不同应用场景中多样而复杂的需求（arXiv:2403.04279）。因此纯文本提示被视作基线，而综述的全部主题——从理论基础到实践进展，引导预训练 T2I 模型超越纯文本条件——都围绕这一缺口展开（arXiv:2403.04279）。精选仓库使分类体系的覆盖面具体化，定位则为各条目赋予了意义（arXiv:2403.04279）。

仍待弥合的缺口在于从"编目"走向"选型"：精选清单与条件视角的分类体系回答了存在哪些控制手段，却既未量化纯文本提示的不足程度，也未给出在具体工作流中挑选控制器的准则。配套仓库同样面临维护风险——其详尽程度仅溯及最近一次更新——这是任何常青综述都须持续应对的限制（arXiv:2403.04279）。

## Conclusion / 结论

**Taking stock.** This survey (arXiv:2403.04279) argues that relying solely on text prompts does not fully cater to the varied and complex requirements of different applications and scenarios in T2I generation (arXiv:2403.04279, §Abstract). Text conditioning alone struggles to convey conditions — an unseen person, a distinct art style, a precise spatial layout — that are not faithfully expressible in language, which motivates a systematic rethinking of *what* conditions steer a diffusion model and *how* they are injected.

**Architecture of the field.** The survey's condition-perspective taxonomy organizes controllable generation into three sub-tasks: introducing novel conditions, integrating multiple conditions, and universal (condition-agnostic) control. Across these, the technical foundations rest on a compact lineage: denoising diffusion probabilistic models; flow matching, which underpins state-of-the-art systems such as Stable Diffusion 3 and Flux (arXiv:2403.04279, §2.1); Latent Diffusion Models, whose compressed-latent formulation delivered a major efficiency breakthrough (arXiv:2403.04279, §2.3); and Diffusion Transformers, which treat image latents as patch tokens and denoise them entirely through self-attention (arXiv:2403.04279, §2.3). The survey's recurring technical challenges — flexibly injecting new conditions without quality loss, faithfully fusing multiple signals, disentangling target concepts from background confounders, and preserving prior knowledge during fine-tuning — are shared across all three sub-tasks and give the taxonomy its explanatory power.

**Remaining gaps.** Two open directions stand out (arXiv:2403.04279, §…):
1. *A universal, cross-modal control paradigm.* Existing controllable models remain task-specific; unified frameworks that flexibly handle spatial, semantic, and multimodal inputs — and extend beyond images to audio, video, and 3D — are still open problems.
2. *World models built on controllability.* The condition-injection principles of diffusion models could ground video-based world models with camera-controllable, temporally/spatially consistent simulated environments, connecting generative modeling to embodied AI.

**Bottom line.** Controllable T2I generation has matured from text-only prompts into a condition-centric science with clear theoretical foundations, but its frontier has shifted from "more conditions" to "fewer constraints": unified, cross-modal, and task-agnostic control remains the field's central open problem.

---

> **中文速览：** 本综述（arXiv:2403.04279）指出，仅靠文本提示无法满足多样化应用的全部需求（§Abstract）。它从条件视角建立分类：新条件引入、多条件融合、通用（条件无关）可控生成，理论基础则沿一条清晰脉络铺陈——DDPM 与支撑 SD3/Flux 的 flow matching（§2.1）、在压缩潜空间扩散而带来效率突破的 LDM（§2.3），以及以自注意力对 patch 化图像潜变量去噪的 DiT（§2.3）。核心挑战跨越三大子任务：不损失质量地注入新条件、忠实融合多条件、将目标概念与背景干扰解耦并在微调中保住先验知识。剩余空白集中在两点：一是迈向统一的多模态控制范式（图像之外拓展至音视频、3D），二是基于可控性构建可交互、时空一致的「世界模型」视频生成系统。总体判断：可控 T2I 的战场已从「增加条件」转向「消除约束」，通用、跨模态、任务无关的控制仍是待解的核心命题。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Relying solely on text prompts does not fully satisfy varied and complex application requirements in T2I diffusion gener… | arXiv:2403.04279 | high |
| 2 | The survey focuses on flow matching because it underpins state-of-the-art T2I systems such as Stable Diffusion 3 and Flu… | arXiv:2403.04279 | high |
| 3 | Latent Diffusion Models introduced a major efficiency gain by performing diffusion in a compressed latent space. | arXiv:2403.04279 | high |
| 4 | Diffusion Transformers treat image latents as patch tokens and perform denoising entirely through self-attention. | arXiv:2403.04279 | high |

## References
- [[1]](https://arxiv.org/abs/2403.04279) arXiv:2403.04279