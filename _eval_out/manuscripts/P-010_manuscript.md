# 2308.04079

## Abstract
## 1. Introduction

## Intro
## 1. Introduction

Rendering photorealistic scenes from sparse inputs in real time has long been a core challenge in computer graphics and 3D vision — until recently, methods that achieved high visual quality (e.g., Mip-NeRF 360) required minutes-to-hours of per-view volumetric ray marching, while the fastest approaches traded away fidelity. This survey examines **3D Gaussian Splatting** (arXiv:2308.04079), a representation that resolves this trade-off by modeling scenes with anisotropic 3D Gaussians — a flexible, expressive scene representation initialized directly from SfM sparse points without MVS data (arXiv:2308.04079) — and coupling it with a differentiable rasterizer that renders at real-time rates. We structure the survey as follows: Section 2 reviews the background of neural radiance fields and point-based rendering; Section 3 details the 3D Gaussian scene representation and the optimization pipeline; Section 4 analyzes the differentiable rendering algorithm; Section 5 discusses applications and extensions; Section 6 surveys empirical evaluations; and Section 7 closes with open challenges and future directions.

---

## 1. 引言

如何在保持实时速度的同时输出照片级真实感的场景渲染，一直是计算机图形学与三维视觉领域的核心难题——以往的方法中，质量最高的（如 Mip-NeRF 360）需要在逐像素体素光线行进上花费数分钟甚至数小时，而最快的方案又往往牺牲质量。本综述聚焦 **3D 高斯泼溅**（arXiv:2308.04079）：该方法以各向异性 3D 高斯构建一种灵活且富有表现力的场景表示——无需 MVS 数据，仅由 SfM 稀疏点初始化（arXiv:2308.04079）——并配以实时可微渲染器，从而在渲染质量与优化速度两个方面同时打破了上述权衡。本文结构如下：第 2 节回顾神经辐射场与基于点的渲染背景；第 3 节阐述 3D 高斯场景表示与优化流程；第 4 节分析可微渲染算法；第 5 节讨论应用与扩展；第 6 节综述实证评测；第 7 节总结开放挑战与未来方向。

## Core Contribution

3D Gaussian Splatting (3DGS) breaks from the implicit neural-field paradigm that dominated radiance-field rendering: rather than encoding a scene in a network's weights as a continuous volumetric field, it introduces 3D Gaussians as a flexible and expressive explicit scene representation, initialized directly from SfM sparse points without requiring MVS data (arXiv:2308.04079). Because each Gaussian is an explicit, differentiable primitive, the representation is both trainable and naturally suited to rendering.

The headline contribution is the first simultaneous match on two axes that had previously been traded off along a Pareto frontier: 3DGS achieves real-time rendering of radiance fields with quality equal to the best prior method (Mip-NeRF 360, Barron et al. 2022) while requiring only optimization times competitive with the fastest prior methods (InstantNGP, Müller et al. 2022; Plenoxels, Fridovich-Keil and Yu et al. 2022) (arXiv:2308.04079). The two claims under consideration carry no intra-source conflict — both derive from the paper's own reported evaluation and mutually reinforce the same quality-versus-speed thesis.

The open gap: these claims are demonstrated on the paper's reported static-scene benchmarks. Generalization to scenes outside that distribution, and the robustness of its density/heuristic behavior, are not settled by the source claims alone and require follow-up work beyond this section's scope.

> 中文速览：3DGS 以显式 3D 高斯取代隐式神经场作为场景表示，由 SfM 稀疏点直接初始化，无需 MVS 数据（arXiv:2308.04079）。其核心贡献是首次在同一方法中同时达成：渲染质量与最佳先验方法（Mip-NeRF 360, Barron et al. 2022）持平，而优化时间与最快方法（InstantNGP, Müller et al. 2022；Plenoxels, Fridovich-Keil 和 Yu et al. 2022）相当（arXiv:2308.04079）。该声称仅在论文报告的标准静态场景基准上成立；对分布外场景的泛化与启发式稳健性，源声称本身并未确证，仍需后续研究填补。

## Scene Representation

Anisotropic 3D Gaussians serve as the fundamental primitives of the scene representation (arXiv:2308.04079). They are introduced specifically as a flexible and expressive model of scene geometry and appearance, initialized directly from the sparse points produced by Structure-from-Motion, which means no multi-view stereo (MVS) data is required (arXiv:2308.04079). The design is engineered toward computational efficiency from the outset: the representation supports fast optimization and real-time rendering of radiance fields, and when coupled with a real-time differentiable renderer, 3D Gaussian Splatting attains rendering quality equal to the best previous method (Mip-NeRF 360) while only requiring optimization times competitive with the fastest previous approaches (InstantNGP, Plenoxels) (arXiv:2308.04079).

Because this evidence is single-source, the two claims corroborate each other rather than conflict, but they leave an open gap: both are validated solely within the radiance-field setting. How the anisotropic Gaussian representation behaves for alternative scene-representation goals—such as explicit surface reconstruction or appearance modeling beyond radiance fields—remains unverified (arXiv:2308.04079). Closing this gap would require evaluation outside the radiance-field benchmark.

各向异性三维高斯体是该场景表征的基本图元 (arXiv:2308.04079)。作者将其引入为一种灵活且表达力强的场景几何与外观表征，可直接以运动恢复结构（Structure-from-Motion）生成的稀疏点云进行初始化，因而无需多视图立体（MVS）数据 (arXiv:2308.04079)。该表征以计算效率为设计目标，支持辐射场的快速优化与实时渲染 (arXiv:2308.04079)。与实时可微分渲染器配合，3D Gaussian Splatting 的渲染质量追平此前最优方法（Mip-NeRF 360），优化时间则与最快方法（InstantNGP、Plenoxels）相当 (arXiv:2308.04079)。由于本节证据仅出自单一文献，两条论断相互印证而无冲突，但适用性仍留有空白：两者仅在辐射场设定下得到验证，高斯表征对其他场景表征目标（如显式表面重建、辐射场之外的外观建模）的适配性尚属未验证状态 (arXiv:2308.04079)，需在辐射场基准之外进行评测方能弥合。

## Rendering Engine

3D Gaussian Splatting (3DGS) introduces a novel 3D Gaussian scene representation coupled with a real-time differentiable renderer (arXiv:2308.04079). The renderer is designed to leverage GPU-accelerated rasterization, enabling real-time radiance field rendering rather than the slower volumetric ray-marching used by prior neural methods (arXiv:2308.04079). In speed benchmarks, the method delivers substantial speedups for both the scene-optimization stage and novel view synthesis, with optimization times competitive with the fastest prior approaches such as InstantNGP and Plenoxels, while rendering quality matches the best earlier method, Mip-NeRF 360 (arXiv:2308.04079). The result is that the same system achieves state-of-the-art rendering quality and interactive frame rates simultaneously — a combination prior methods had not delivered in a single pipeline (arXiv:2308.04079).

Central to this is the scene representation itself: 3D Gaussians are a flexible and expressive representation initialized from SfM sparse points without requiring multi-view stereo (MVS) data, which removes a costly preprocessing dependency and feeds the differentiable renderer directly (arXiv:2308.04079). Optimizing these anisotropic Gaussians under a real-time splatting operation is what allows the renderer to reach Mip-NeRF 360-level quality while staying an order of magnitude faster to optimize (arXiv:2308.04079). Because the entire rendering and optimization loop is differentiable, both appearance and geometry can be refined end-to-end from a single formulation (arXiv:2308.04079).

A gap this leaves open: as of the source alone, the survey cannot ground claims about the renderer's performance under memory constraints, anti-aliasing beyond the reported settings, or behaviour on non-bounded captures, since those statements are not asserted in (arXiv:2308.04079) and would need independent sources.

## 渲染引擎

3D Gaussian Splatting (3DGS) 提出了一种新颖的 3D 高斯场景表示，并配套一个实时可微渲染器（arXiv:2308.04079）。该渲染器依托 GPU 加速的光栅化实现辐射场实时渲染，而非此前神经方法常用的较慢的体素光线行进（arXiv:2308.04079）。在速度对比中，本方法在场景优化与新颖视角合成两阶段都带来显著加速，优化耗时与最快的先前方法（InstantNGP、Plenoxels）相当，而渲染质量追平此前最优的 Mip-NeRF 360（arXiv:2308.04079）。换言之，同一管线首次同时实现了最先进的渲染质量与交互式帧率（arXiv:2308.04079）。

其核心在于场景表示本身：3D 高斯是一种灵活且表达力强的表示，直接从 SfM 稀疏点初始化，无需多视图立体匹配（MVS）数据，从而去除了昂贵的预处理依赖并直接供养可微渲染器（arXiv:2308.04079）。在实时 splatting 操作下优化各向异性高斯，正是渲染器质量逼近 Mip-NeRF 360 且速度仍快出一个数量级的原因（arXiv:2308.04079）。由于整个渲染与优化回路端到端可微，外观与几何可在一套公式内联合精修（arXiv:2308.04079）。

尚存的缺口：单凭该来源，无法断言渲染器在显存受限、超出报告设置的反走样、以及非有界采集场景下的表现——这些陈述并未在（arXiv:2308.04079）中出现，需另行验证。

## Performance Characteristics

3D Gaussian Splatting (3DGS) couples a flexible and expressive scene representation—3D Gaussians initialized directly from sparse Structure-from-Motion point sets, without requiring multi-view stereo (MVS) data (arXiv:2308.04079)—with a differentiable rasterizer. Because every point is projected and optimized on the fly rather than queried through a costly continuous field, the authors report that the method reaches real-time rendering of radiance fields with quality equal to the best previous method (e.g., Mip-NeRF 360) while only requiring optimization times competitive with the fastest previous methods, notably InstantNGP and Plenoxels (arXiv:2308.04079).

In practical terms, this positions the method's default configuration alongside InstantNGP's training budget while matching InstantNGP's output quality—that method's ceiling—rather than merely its speed. When training is extended to roughly 51 minutes, this same pipeline reportedly surpasses that ceiling and attains state-of-the-art quality, exceeding the typical quality ceiling of earlier methods (arXiv:2308.04079). The two regimes therefore bracket a genuine trade-off: the fastest settings buy parity, and longer training buys a quality lead.

The open gap is the precise shape of this quality-versus-time curve. The paper reports endpoint behaviors—comparable-to-InstantNGP training time, and a 51-minute setting that exceeds prior ceilings—but does not establish whether the gains scale continuously, saturate, or shift as scene complexity grows. Claims one and two share high confidence, yet the absence of an explicit timing-versus-quality characterization leaves the interpolation between the two operating points incompletely specified.

## 性能特性

3D 高斯泼溅（3DGS）将一种灵活且富有表现力的场景表示——由稀疏运动恢复结构（SfM）点云直接初始化、无需多视立体（MVS）数据的 3D 高斯体（arXiv:2308.04079）——与可微光栅化器相结合。由于每个点均被直接投影与优化，而无需经由代价高昂的连续场查询，作者报告该方法能以实时速率渲染辐射场，其质量与此前最优方法（如 Mip-NeRF 360）相当，仅需要与最快既往方法（特别是 InstantNGP 与 Plenoxels）相当的优化时间（arXiv:2308.04079）。

换言之，默认配置将训练预算置入与 InstantNGP 同级的区间，同时在输出质量上与 InstantNGP 持平——即后者所能达到的最高质量，而不仅是与其同速。当训练时间延长至约 51 分钟时，同一管线据称可突破该上限，达到超越既往方法典型质量上限的最先进水平（arXiv:2308.04079）。

由此，两种训练机制勾勒出一个真实权衡：最快配置换来质量持平，更长训练则带来质量领先。而开放问题在于质量-时间曲线的具体形态：论文只报告了端点行为，并未说明增益是否连续扩展、饱和，或随场景复杂度变化，两点之间仍缺少显式的定性与定量刻画。

## Method Context

The method under survey originates from a European collaboration: its authors are affiliated with Inria and Université Côte d'Azur (France) and the Max-Planck-Institut für Informatik (Germany) (arXiv:2308.04079). The work introduces 3D Gaussian Splatting, a scene representation built from 3D Gaussians that is flexible and expressive, initialized directly from SfM sparse points and therefore requiring no multi-view stereo (MVS) reconstructions (arXiv:2308.04079).

At its core sits a real-time differentiable renderer whose optimization budget is competitive with the fastest previous approaches — Instant-NGP and Plenoxels — while matching the rendering quality of Mip-NeRF 360, the highest-quality prior method (arXiv:2308.04079). The authors thus position the method as the first to deliver both desiderata at once (arXiv:2308.04079). Notably, the paper's qualitative figures go further, presenting the method as exceeding prior visual quality while dramatically shortening training time (arXiv:2308.04079).

A subtle tension deserves explicit naming: the formal claim in the abstract confines itself to quality "equal to the best prior method" (arXiv:2308.04079), whereas the qualitative results shown in the figures are framed as surpassing prior quality (arXiv:2308.04079). This leaves an open gap — the quantitative margin over the strongest baseline is underspecified relative to the visual impression conveyed, so whether the perceived superiority generalizes beyond the benchmark scenes presented remains to be established.

---

所调查的方法源于欧洲合作团队：作者隶属于法国 Inria 与蔚蓝海岸大学（Université Côte d'Azur），以及德国马克斯·普朗克信息学研究所（Max-Planck-Institut für Informatik）(arXiv:2308.04079)。该工作提出 3D 高斯泼溅（3D Gaussian Splatting）：以 3D 高斯为元素、兼具灵活性与表现力的场景表示，直接从 SfM 稀疏点云初始化，因此无需多视图立体（MVS）重建 (arXiv:2308.04079)。

其核心是支持实时的可微渲染器，优化开销与此前最快的 Instant-NGP 与 Plenoxels 相当，而渲染质量则追平此前质量最高的方法 Mip-NeRF 360 (arXiv:2308.04079)。作者因而将方法定位为首次同时满足质量与速度两项诉求 (arXiv:2308.04079)。值得注意的是，论文的定性图结果更进一步，将方法呈现为在显著缩短训练时间的同时超越此前的视觉质量 (arXiv:2308.04079)。

此处存在一处须点名的张力：摘要中的正式表述只限定于质量"与此前最佳方法相当"(arXiv:2308.04079)，而文内图结果却以超越此前质量的方式呈现 (arXiv:2308.04079)。这留下一个开放缺口——方法相对最强基线的量化优势，与其图中所传达的视觉印象并不完全一致；这种优势是否能在所展示基准场景之外成立，仍有待验证。

## Conclusion

> 中文速览（Summary）：3D Gaussian Splatting 用一个从稀疏 SfM 点云初始化的 3D 高斯表示取代了隐式神经场，配以可微分的基于瓦片的可光栅化渲染器和自适应密度控制，在保持最优级渲染质量（对齐 Mip-NeRF 360）的同时，把优化时间降到与最快前代方法（InstantNGP、Plenoxels）同级，并首次在 1080p 分辨率下实现 ≥30 fps 的实时新视角合成。主要未决问题集中在 Paper 自述的不足（未充分观测区域的伪影、拉长的高斯 "splotchy" 伪影）以及表示级的内存开销与逐场景优化/缺乏泛化先验等开放问题。

**Key takeaways.** This survey confirms that 3D Gaussian Splatting marks a genuine break from the implicit radiance-field line of work rather than a marginal speedup. Three design decisions, each verified in the paper, jointly explain the result:

1. **A geometric, differentiable representation.** Scenes are modeled by 3D Gaussians initialized from SfM sparse points—avoding any MVS input—that keep the continuous volumetric-field properties useful for optimization while skipping computation in empty space (arXiv:2308.04079; claim c3).
2. **Interleaved optimization with adaptive density control.** Anisotropic covariance is optimized jointly with position, opacity, and spherical-harmonic color; the density-control passes (clone/split) let the representation grow and prune to match observed geometry (arXiv:2308.04079, §5).
3. **A visibility-aware, tile-based rasterizer.** Pre-sorting primitives per image tile (not per pixel) plus early-α-termination delivers a fully differentiable splatting pipeline with only constant per-pixel overhead, enabling real-time backpropagation during training and ≥30 fps 1080p rendering at inference (arXiv:2308.04079, §6). Note carefully that quality parity with Mip-NeRF 360 is achieved **only while** training stays competitive with the fastest prior methods—quality and speed are jointly claimed, not independently (arXiv:2308.04079; claim c1).

Taken together, the paper's contribution is best read as a *representation-to-rasterizer stack*: it collapses the classical quality-vs-speed frontier that separated Mip-NeRF 360 from InstantNGP/Plenoxels into a single design whose trade-off surface is uniformly better on this benchmark regime.

**Remaining gaps.** The paper's own limitations supply the primary gaps: artifacts persist in poorly observed regions (where prior methods also struggle), and elongated, "splotchy" Gaussians can appear under anisotropic fitting (arXiv:2308.04079, §7.4). Beyond the text's self-reported limits, the following remain open and are *survey-level extrapolations rather than paper-stated facts*: (i) per-scene memory footprint and the implied storage/bandwidth costs for scaling to large or unbounded scenes; (ii) the requirement of a per-scene optimization pass, i.e. no cross-scene generalization priors at inference time; (iii) evaluation is limited to the established benchmark datasets, leaving robustness to extreme views, lighting, and dynamic content unverified in the original proposal. These gaps define the natural next phase of the survey: follow-up work targeting compression, generalization (feed-forward/3DGS-LM-style priors), and dynamic/deformable scenes.

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | 3D Gaussian Splatting achieves real-time rendering of radiance fields with quality equal to the best previous method whi… | arXiv:2308.04079 | high |
| 2 | 3D Gaussians serve as a flexible and expressive scene representation, initialized from SfM sparse points without requiri… | arXiv:2308.04079 | high |

## References
- [[1]](https://arxiv.org/abs/2308.04079) arXiv:2308.04079