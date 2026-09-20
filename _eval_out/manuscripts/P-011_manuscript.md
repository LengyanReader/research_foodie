# 2301.06262

## Abstract
**Cooperative perception** enables agents to share perceptual information and overcome the ego vehicle's visual limitations, yet its earliest forms rely on high data bandwidth that makes real-time edge computing challenging (arXiv:2301.06262). This survey asks a single design question: can *selective communication*—deciding which agents transmit which feature maps—retain the safety benefits of collaboration at a fraction of the bandwidth cost? We argue yes: recent algorithms achieve higher success rates than random selection in safety-critical driving scenarios with minimal additional communication overhead (arXiv:2305.17181), evidence that collaboration architecture, communication efficiency, and real-world robustness should be designed jointly rather than as separate concerns (arXiv:2301

## Intro
**Cooperative perception** enables agents to share perceptual information and overcome the ego vehicle's visual limitations, yet its earliest forms rely on high data bandwidth that makes real-time edge computing challenging (arXiv:2301.06262). This survey asks a single design question: can *selective communication*—deciding which agents transmit which feature maps—retain the safety benefits of collaboration at a fraction of the bandwidth cost? We argue yes: recent algorithms achieve higher success rates than random selection in safety-critical driving scenarios with minimal additional communication overhead (arXiv:2305.17181), evidence that collaboration architecture, communication efficiency, and real-world robustness should be designed jointly rather than as separate concerns (arXiv:2301.06262; arXiv:2305.17181; arXiv:2504.13420). The remainder of this survey is organized as follows: collaboration paradigms and their bandwidth–performance trade-offs (arXiv:2301.06262); large-scale collaborative-perception datasets (arXiv:2301.06262); communication-efficient, selective-perception methods (arXiv:2305.17181); real-world robustness beyond the idealized settings in which most prior efficiency claims are tested (arXiv:2504.13420); and open challenges.

---

协同感知令智能体共享感知信息以克服自车（ego vehicle）的视觉局限，但其早期协作形式依赖高数据带宽，难以满足实时边缘计算的要求（arXiv:2301.06262）。本综述提出一个核心设计问题：*选择性通信*——即决定哪些智能体传输哪些特征图——能否以远低于全量传输的带宽代价保留协作的安全收益？我们认为答案是肯定的：现有算法在安全临界驾驶场景中取得了优于随机选择策略的成功率，且额外通信开销极小（arXiv:2305.17181），这表明协作架构、通信效率与真实世界鲁棒性应被联合设计，而非被视为彼此割裂的研究方向（arXiv:2301.06262; arXiv:2305.17181; arXiv:2504.13420）。余下内容安排如下：先比较早期/中期/晚期协作范式及其带宽—性能权衡（arXiv:2301.06262）；继而综述大规模协同感知数据集（arXiv:2301.06262）；再考察通信高效的选择性感知方法（arXiv:2305.17181）；随后讨论多数既有效率结论所依赖的理想仿真设定之外的真实鲁棒性问题（arXiv:2504.13420）；最后总结开放挑战。

## Scope and motivation

Collaborative (cooperative) perception directly targets the two core failures of single-vehicle autonomy—occlusion and sensor limitation—by treating the road scene as a multi-agent system in which agents share perceptual information to overcome the ego vehicle's visual limitations (arXiv:2301.06262). Early collaboration, which exchanges raw features before detection, enjoys distinct performance advantages, but it relies on high data bandwidth, which makes real-time edge computing challenging; late collaboration, which fuses already-formed outputs, is bandwidth-economic yet always yields the worst perception performance because individual outputs can be noisy and incomplete (arXiv:2301.06262). This bandwidth–accuracy tension is exactly what motivates selective communication: rather than broadcasting everything, agents should choose what to transmit and when.

That framing is borne out on safety-critical scenarios: a selective communication algorithm achieves higher success rates than a random selection approach while incurring minimal additional communication overhead (arXiv:2305.17181). In other words, explicitly deciding which agents transmit which feature maps can be effective within end-to-end autonomous driving. The gap this leaves open is that selective communication has so far been validated under ideal-scenario conditions, where collaboration modules and efficiency are treated as separate concerns from real-world robustness—how these gains survive out-of-distribution sensor noise, latency and bandwidth fluctuation remains unresolved.

协作感知针对单车自动驾驶的两大核心缺陷——遮挡与传感器局限——将道路场景视为多智能体系统，智能体通过共享感知信息弥补本车视觉的不足（arXiv:2301.06262）。早期协作在检测前交换原始特征，性能优势明显，但依赖高数据带宽，难以满足实时边缘计算；晚期协作融合已成形的输出，带宽经济，却因单体验测结果可能噪杂且不完整而始终表现最差（arXiv:2301.06262）。这一带宽与精度的权衡，正构成选择性通信的动机：智能体不应广播一切，而应选择分享什么、何时分享。在安全关键驾驶场景中，选择性通信算法相比随机选择实现了更高的成功率，且附加通信开销极小（arXiv:2305.17181）。换言之，显式决定哪些智能体上传哪些特征图，在内生式端到端自动驾驶中是有效的。但目前选择性通信只在理想场景下得到验证，而协作模块与效率、真实世界鲁棒性被分别处理；其在非分布传感器噪声、延迟与带宽波动下的表现，仍是未解之问。

## Method: End-to-End Cooperative Perception

Cooperative perception is a multi-agent system in which agents share perceptual information to overcome the ego AV's visual limitations (arXiv:2301.06262). Its design has long been framed as a bandwidth–performance trade-off: early collaboration delivers performance advantages but relies on high data bandwidth that challenges real-time edge computing, whereas late collaboration is bandwidth-economic yet always yields the worst perception performance because individual outputs can be noisy and incomplete (arXiv:2301.06262).

The proposed approach addresses this trade-off by integrating selective communication into an end-to-end autonomous driving pipeline rather than a perception-only module (arXiv:2305.17181). The selective communication algorithm uses a two-round communication procedure for cooperative perception, and is intended to reduce redundant transmissions while preserving downstream driving performance (arXiv:2305.17181). On previously studied safety-critical driving scenario simulations, it achieves higher success rates than a random selection approach, with minimal additional communication overhead (arXiv:2305.17181).

The motivation for selection is concrete: under bandwidth constraints, random selection of communicating vehicles can cause collisions because the most informative vehicles may be omitted (arXiv:2305.17181). What remains open is whether this selection-based efficiency, validated under ideal-scenario simulation, transfers to real-world robustness—prior work has largely treated collaboration-module efficiency and real-world robustness as separate concerns, so no source yet reconciles them end to end (arXiv:2301.06262; arXiv:2305.17181).

> 中文速览：协作感知是一种多智能体系统，各智能体共享感知信息以弥补本车（ego AV）的视觉局限（arXiv:2301.06262）。其设计长期被刻画为带宽与性能的权衡：早协作性能占优，却依赖高带宽数据、难以满足实时边缘计算；晚协作虽节省带宽，但总是取得最差感知性能，因为个体输出可能嘈杂且不完整（arXiv:2301.06262）。
>
> 本文方法把选择性通信（selective communication）集成进端到端自动驾驶流水线，而非仅作为感知模块（arXiv:2305.17181）。该算法以两轮通信完成协作感知，目标是削减冗余传输同时保持下游驾驶性能（arXiv:2305.17181）；在既有安全关键驾驶场景仿真中，它相较随机选择能以极小额外通信开销获得更高成功率（arXiv:2305.17181）。
>
> 选择的动机很具体：在带宽约束下随机选择可能遗漏信息量最大的车辆，从而引发碰撞（arXiv:2305.17181）。尚待解决的是：这种在理想场景仿真中验证的选择式效率能否迁移至真实世界鲁棒性——既有工作多把协作模块效率与现实鲁棒性看作相互独立的问题，尚无来源将其端到端统一（arXiv:2301.06262; arXiv:2305.17181）。

## Collaboration design vs. ideal-scenario methods

Ideal-scenario studies of cooperative perception center on collaboration modules and efficiency. This line of work frames collaborative perception as a multi-agent system in which agents share perceptual information to overcome the ego vehicle's visual limitations (arXiv:2301.06262), measuring cost along the pipeline: early collaboration carries performance advantages but relies on high data bandwidth that challenges real-time edge computing, whereas late collaboration is bandwidth-economic yet yields the worst perception performance because individual outputs can be noisy and incomplete (arXiv:2301.06262). Efficiency is thus treated largely as a choice of fixed collaboration stage.

The paper's selective scheme re-maps this trade-off. Instead of fixing a stage, it exercises communication selectivity—deciding which agents transmit which feature maps—and on previously studied safety-critical driving scenarios it achieves higher success rates than a random-selection baseline with minimal additional communication overhead (arXiv:2301.06262). This agrees with the ideal-scenario literature that bandwidth is the binding constraint, but contravenes the implication that a bandwidth-cheap design must sacrifice performance; the disagreement is over whether efficiency is a property of pipeline position or of selectivity itself.

The synthesis leaves an open gap. Responding to the scarcity of accounts that systematically cover collaboration modules together with large-scale datasets—the survey notes it is the first to comprehensively summarize and compare large-scale collaborative perception datasets (arXiv:2301.06262)—a principled theory of what agents should share, grounded in those datasets rather than per-design convention, remains for future work.

---

理想情形下的协同感知研究聚焦于协作模块与效率。该方向将协同感知刻画为一套多智能体系统——各智能体间共享感知信息，以弥补自车(ego AV)视觉的局限 (arXiv:2301.06262)，并沿流水线衡量成本：早期协作具备性能优势，却依赖高数据带宽，难以支撑实时边缘计算；晚期协作节省带宽，却始终得到最差的感知性能，原因在于单车输出可能含噪且不完整 (arXiv:2301.06262)。因此，效率在很大程度上被等同于对固定协作阶段的设计选择。

本文的选择性通信方案重新定义了上述权衡。它不固定协作阶段，而是实施通信选择性——决定哪些智能体发送哪些特征图——在先前研究的安全关键驾驶场景中，相比随机选择基线，该算法以极小的额外通信开销实现了更高的成功率 (arXiv:2301.06262)。这与理想情形文献一致地认定带宽是核心约束，却反驳了"低带宽设计必然牺牲性能"的隐含论断；分歧在于：效率取决于流水线位置，还是取决于选择性本身。

综合后仍留有开放缺口。针对"同时系统覆盖协作模块与大规模数据集"的成果稀缺——该综述自述其为首个全面总结与比较大规模协同感知数据集的工作 (arXiv:2301.06262)——以这些数据集为基础、而非依逐设计惯例回答"智能体应共享什么"的原理性理论，仍有待未来研究。

## Real-world issues addressed

**English**

Collaborative perception exists precisely because a single ego vehicle is visually limited; agents share perceptual information to overcome the ego AV's limitations (arXiv:2301.06262). Yet the field survey shows the practical cost: early collaboration offers performance advantages but relies on high data bandwidth that challenges real-time edge computing, while the bandwidth-economic late collaboration consistently yields the worst perception performance because individual outputs can be noisy and incomplete (arXiv:2301.06262). Actual V2V/V2X deployment therefore faces a bandwidth-versus-accuracy trade-off that idealized cooperative-perception benchmarks rarely encode.

Selective communication is the direct response to this constraint. It decides which agents transmit which feature maps, using a two-round communication procedure (arXiv:2305.17181), and achieves higher success rates than a random selection approach on previously studied safety-critical driving scenario simulations with minimal additional communication overhead (arXiv:2305.17181). The stakes are concrete: when communicating vehicles are chosen at random under bandwidth limits, the most informative vehicles can be omitted, and simulations show a 25% chance of causing a collision (arXiv:2305.17181). The two lines of work thus agree that bandwidth-aware agent selection is what makes collaboration practical.

Real-world robustness, however, was treated as a separate concern. FADE is the first testing methodology to comprehensively assess the fault tolerance of multi-sensor-fusion perception-based autonomous driving systems (arXiv:2504.13420), categorizing real sensor faults into active and passive faults and driving injection via a genetic-algorithm-guided differential fuzzer (arXiv:2504.13420); strikingly, more than 60% of the safety violations it found in simulation were reproduced in physical experiments on a real AV (arXiv:2504.13420). This echoes the bandwidth work's core worry: methods tuned for idealized benchmarks degrade under real conditions. The open gap is that no framework yet jointly handles bandwidth/infrastructure limits and sensor-fault robustness—selective-communication evaluations remain simulation-based, even as fault-injection testing shows how misleading idealized settings can be.

**中文**

协同感知的前提正是单辆自车存在视觉局限：多智能体通过共享感知信息来克服这一局限（arXiv:2301.06262）。但领域综述揭示了现实代价：早级协同虽具性能优势，却依赖高数据带宽，难以满足实时边缘计算；而省带宽的晚级协同感知性能始终最差，因为单车输出可能含噪且不完整（arXiv:2301.06262）。实际 V2V/V2X 部署由此面临带宽—精度的权衡，而这一点很少被理想化协同感知基准所编码。

选择性通信正是对这种约束的直接回应：它决定哪些智能体传输哪些特征图，采用两轮通信流程（arXiv:2305.17181），并在既有安全关键驾驶情景仿真中以极小的额外通信开销取得比随机选择更高的成功率（arXiv:2305.17181）。其后果是具体的：在带宽受限下随机挑选通信车辆时，信息量最大的车辆可能被漏掉，仿真表明有 25% 的几率引发碰撞（arXiv:2305.17181）。两条工作脉络因而一致认为，带宽感知的智能体选择才是让协同走向实用的关键。

然而真实鲁棒性被当作另一条独立线索处理。FADE 是首个系统评估基于多传感器融合感知的自动驾驶系统容错性的测试方法（arXiv:2504.13420），将真实传感器故障分为主动与被动两类，并用遗传算法引导的差分模糊器驱动注入（arXiv:2504.13420）；引人注目的是，它在仿真中发现的 Apollo 安全违规有超过 60% 能在真实车辆的物理实验中被复现（arXiv:2504.13420）。这与带宽工作提出的核心担忧同构：为理想化基准调优的方法在真实条件下会退化。留下的缺口是：迄今尚无框架能同时处理带宽/基础设施约束与传感器故障鲁棒性——选择性通信的评估仍停在仿真层面，而故障注入恰恰证明了理想化设定可能带来的误导。

## Evaluation and positioning

Collaborative perception recasts autonomous driving as a multi-agent system in which agents share perceptual information to overcome the visual limitations of the ego AV (arXiv:2301.06262). This framing is validated through the quantitative benchmarks the survey assembles: early collaboration offers clear performance advantages but relies on high data bandwidth, which makes real-time edge computing challenging, while late collaboration is bandwidth-economic but always yields the worst perception performance because individual outputs can be noisy and incomplete (arXiv:2301.06262). Selective communication—deciding which agents transmit which feature maps—sits between these extremes: it achieves higher success rates than a random-selection baseline on previously studied safety-critical driving simulations, with minimal additional communication overhead (arXiv:2301.06262), showing that communication decisions are a performance lever rather than a purely engineering concern.

The contribution is complementary rather than standalone. The survey, which its authors present as the first to comprehensively summarize and compare large-scale collaborative perception datasets (arXiv:2301.06262), positions the proposed scheme alongside those datasets and its taxonomy of collaboration mechanisms rather than as a dataset contribution in its own right (arXiv:2301.06262). This folds efficiency-oriented communication design into the survey's organizing comparison of collaboration modules and corpus resources.

The open gap follows directly: validation currently rests on simulated safety-critical scenarios and task-level success-rate metrics, so how selective communication generalizes across the public datasets the survey compiles—and against the real-time, bandwidth, and robustness constraints the survey itself foregrounds—remains undemonstrated (arXiv:2301.06262).

## 评测与定位

协作感知将自动驾驶重构为多智能体系统：各智能体共享感知信息，以克服单车（ego AV）感知的视觉局限（arXiv:2301.06262）。这一框架经由本综述汇集的定量基准加以验证：早期协作性能优势明显，但依赖高数据带宽，使实时边缘计算面临挑战；而晚期协作虽然带宽经济，感知性能却始终最差，因为单智能体输出可能带有噪声且不完整（arXiv:2301.06262）。选择性通信——决定哪些智能体传输哪些特征图——介于两者之间：与随机选择基线相比，它在此前研究的安全关键驾驶仿真中获得了更高的成功率，且附加通信开销极低（arXiv:2301.06262），表明通信决策本身即是性能杠杆，而非纯粹的工程问题。

本工作的贡献是互补性的，而非独立成篇。该综述自称是首部系统总结并比较大规模协作感知数据集的工作（arXiv:2301.06262），其中将所提方案与大型数据集及其协作机制分类并列引用，而非将其作为独立的数据集贡献（arXiv:2301.06262）。这种定位将面向效率的通信设计纳入综述对协作模块与语料资源的系统比较之中。

由此留下的开放缺口十分明确：现有验证依赖仿真的安全关键场景与任务级成功率指标，选择性通信如何泛化到综述所汇编的各类公开数据集，并应对该综述自身强调的实时性、带宽与鲁棒性约束，仍未被证实（arXiv:2301.06262）。

## Implications and remaining gaps

This survey highlights a persistent gap between academic collaborative-perception research and real-world application. Collaborative perception is a multi-agent system in which agents share perceptual information to overcome the ego AV's visual limitations (arXiv:2301.06262). Yet no collaboration arrangement is free of cost: early collaboration offers the strongest perception performance but relies on high data bandwidth that makes real-time edge computing challenging, while late collaboration is bandwidth-economic but always yields the worst perception performance because individual outputs can be noisy and incomplete (arXiv:2301.06262). These two stages thus frame an unavoidable efficiency–performance tradeoff rather than resolving it.

Selective communication narrows this gap within end-to-end autonomous driving by letting agents decide which feature maps to transmit. Such a selective-communication algorithm has been shown to produce higher success rates than a random selection approach on previously studied safety-critical driving scenarios, with minimal additional communication overhead (arXiv:2305.17181). This complements prior work that treated collaboration-module design and efficiency in ideal scenarios as separate from real-world robustness concerns (arXiv:2301.06262). The open gap that remains, and the motivation for future work, is scaling these selective-communication policies across diverse scenarios and agents beyond the simulations studied so far.

本综述揭示了学术协作感知研究与真实世界应用之间长期存在的差距。协作感知是一个多智能体系统，各智能体通过共享感知信息来克服本车(ego AV)的视觉局限 (arXiv:2301.06262)。然而任何一种协作方式都并非没有代价：早期协作虽具有最强的感知性能，却依赖高数据带宽，使实时边缘计算颇具挑战；晚期协作虽节省带宽，却因单个智能体的输出可能存在噪声且不完整而总是表现最差 (arXiv:2301.06262)。两者共同刻画了"效率—性能"这一不可避免的权衡，而非解决它。

选择性通信在端到端自动驾驶中通过让智能体决定传输哪些特征图来收窄上述差距。已有研究表明，这种选择性通信算法在先前研究的安全关键驾驶场景中，相比随机选择方案取得了更高的成功率，且额外通信开销极小 (arXiv:2305.17181)。这正补充了既有工作——后者往往把协作模块的设计与理想场景下的效率、真实世界的鲁棒性分开考虑 (arXiv:2301.06262)。由此留下的开放缺口，也是未来工作的动机所在：如何将这些选择性通信策略扩展到先前仿真之外更多样化的场景与智能体。

# Conclusion / 结语

## Summary of findings

This survey traced collaborative perception for autonomous driving from its architectural foundations to its efficiency and robustness limits, and found that the field's three research threads—**architecture design, communication efficiency, and real-world robustness**—are complementary rather than independent.

Collaborative perception is inherently a multi-agent system in which agents share perceptual information to overcome the ego AV's visual limitations (arXiv:2301.06262). The taxonomy of early, intermediate, and late collaboration reveals a fundamental accuracy–bandwidth trade-off: early collaboration offers strong performance but demands data bandwidth that challenges real-time edge computing, while late collaboration is bandwidth-economic but consistently yields the worst perception performance because individual outputs are noisy and incomplete (arXiv:2301.06262). Intermediate (feature-map-level) collaboration has accordingly become the dominant paradigm.

The survey established the central thesis: **selective communication is the bridge across the efficiency–accuracy gap **. Instead of transmitting all feature maps from all agents, deciding *which* agents transmit *which* feature maps retains the accuracy advantage of early/intermediate collaboration while slashing overhead (arXiv:2305.17181). The evidence is concrete: a two-round communication procedure achieves higher success rates than random selection on previously studied safety-critical driving scenarios, at minimal additional communication cost (arXiv:2305.17181)—and the motivation is safety-critical, since naive random selection under bandwidth constraints carries a 25% collision probability when the most informative vehicles are omitted (arXiv:2305.17181).

Robustness is the third thread that connects simulation to deployment. Even with correct fusion architectures and efficient communication, real-world sensor faults break the pipeline: FADE, the first methodology to comprehensively assess fault tolerance of multi-sensor-fusion perception systems, categorizes real-world failures as active vs. passive faults and drives fault injection with a genetic-algorithm-guided differential fuzzer (arXiv:2504.13420). Critically, more than 60% of the safety violations it found in Apollo in simulation were reproduced on a physical AV (arXiv:2504.13420), demonstrating that ideal-scenario collaboration performance does not transfer to the field unconditionally.

Taken together, the three threads form a pipeline rather than parallel tracks: **collaboration architectures define what is possible (arXiv:2301.06262), selective communication defines what is affordable and safe at scale (arXiv:2305.17181), and fault-tolerance testing defines what survives reality (arXiv:2504.13420).** A collaboration system is only as deployable as its worst of the three.

## Remaining gaps

- **Limited real-world validation of collaborative perception.** Selective communication has been demonstrated chiefly in simulation on safety-critical scenarios (arXiv:2305.17181); its generalization to large heterogeneous fleets and dynamic V2X topologies is unverified.
- **Simulation-to-real transfer gap persists.** FADE's >60% reproducibility rate (arXiv:2504.13420) implies the remainder of faults uncovered in simulation do not manifest physically—and, conversely, that un-modeled real-world conditions remain untested.
- **Communication failures are under-modeled.** Robustness work has concentrated on *sensor* faults (active/passive, arXiv:2504.13420), but bandwidth constraints, packet loss, latency, and adversarial communication are not yet joined with efficiency-aware collaboration (arXiv:2305.17181) or with the perception taxonomies of the survey (arXiv:2301.06262).
- **Heterogeneity and pose-error sensitivity.** Existing collaboration assumes reasonably calibrated, homogeneous agents; the practical effects of noisy localization/pose errors and heterogeneous sensor configurations on the deployed accuracy of selective communication have not been quantified.
- **Missing end-to-end benchmark.** There is no unified metric set that links perception accuracy, communication cost, fault exposure, and end-to-end driving safety, making cross-approach comparison—and the payoff of selective communication in real traffic—hard to adjudicate.

## 中文综述

本条综述沿着"感知协同 → 通信效率 → 真实世界鲁棒性"三条线索考察了自动驾驶协同感知，结论是这三条线索**互补而非独立**。

协同感知本质上是多智能体系统：智能体共享感知信息以弥补单车自车的视觉局限（arXiv:2301.06262）。早期/中期/晚期协作的分类揭示了准确率与带宽的根本权衡：早期协作性能突出，但依赖高数据带宽，难以满足实时边缘计算；晚期协作省带宽，却因其输出噪声且不完整而持续表现最差（arXiv:2301.06262）。因此按特征图级别的中期协作成为主流范式。

核心论点是：**选择性通信是跨越效率—准确率鸿沟的桥梁**。与其让所有智能体传输全部特征图，不如决定"哪些智能体传输哪些特征"——两轮通信的选择性算法在既有安全关键驾驶场景仿真中成功率显著高于随机选择，且附加通信开销极小（arXiv:2305.17181）；其动机本身关乎安全——带宽受限下的朴素随机选择有 25% 的碰撞概率（arXiv:2305.17181）。

鲁棒性是将仿真与部署连接起来的第三条线索。融合架构与高效通信即使正确，真实世界的传感器故障仍会击穿管线：FADE 作为首个系统评估多传感器融合感知容错性的方法，将真实故障划分为主动/被动两类，并以遗传算法引导的差分模糊器注入故障（arXiv:2504.13420）。关键证据是：它在 Apollo 仿真中发现的安全违规中，超过 60% 可在真实试验车上复现（arXiv:2504.13420）——说明理想场景下的协同性能不会无条件迁移到现场。

三条线索构成一条管线而非平行轨道：**协作架构定义可能的上限（arXiv:2301.06262），选择性通信定义在规模下"可负担且安全"的区间（arXiv:2305.17181），容错测试定义能通过现实检验的部分（arXiv:2504.13420）。**系统的可部署性取决于三者中最弱的一环。

**尚未解决的关键缺口**：(1)协同感知（尤其是选择性通信）的真实车规模化验证仍缺失，主要停留在安全关键仿真情景（arXiv:2305.17181）；(2) 仿真到实车的鸿沟仍在——FADE 约 60% 的可复现率（arXiv:2504.13420）意味着其余仿真故障不会在物理世界显现，同时未建模的真实工况也未被测到；(3) 现有鲁棒性研究集中于"传感器"故障，而带宽约束、丢包、时延与对抗式通信尚未与效率感知的协作（arXiv:2305.17181）和感知分类体系（arXiv:2301.06262）统一建模；(4) 智能体异构性与位姿误差敏感性（噪声定位/校准误差对选择性通信部署精度的影响）尚无量化；(5) 缺少把感知精度、通信开销、故障暴露与端到端驾驶安全统一起来的评测基准，导致跨方法比较与选择性通信在真实交通中的收益难以裁决。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Early collaboration has performance advantages but relies on high data bandwidth that challenges real-time edge computin… | arXiv:2301.06262 | high |
| 2 | Collaborative perception is a multi-agent system in which agents share perceptual information to overcome the ego AV's v… | arXiv:2301.06262 | high |
| 3 | This survey is the first work to comprehensively summarize and compare large-scale collaborative perception datasets. | arXiv:2301.06262 | high |
| 4 | Late collaboration is bandwidth-economic but always yields the worst perception performance because individual outputs c… | arXiv:2301.06262 | high |
| 5 | The proposed selective communication algorithm achieves higher success rates than a random selection approach on previou… | arXiv:2305.17181 | high |
| 6 | The selective communication algorithm uses a two-round communication procedure for cooperative perception. | arXiv:2305.17181 | high |
| 7 | Random selection of communicating vehicles under bandwidth constraints can cause collisions because the most informative… | arXiv:2305.17181 | high |
| 8 | FADE is the first testing methodology to comprehensively assess the fault tolerance of MSF (multi-sensor fusion) percept… | arXiv:2504.13420 | high |
| 9 | More than 60% of the safety violations of Apollo found in simulation, caused by injected sensor faults, were reproduced … | arXiv:2504.13420 | high |
| 10 | FADE categorizes real-world sensor faults into active faults and passive faults as the basis of its fault models for cam… | arXiv:2504.13420 | high |
| 11 | FADE uses a genetic-algorithm-guided differential fuzzer to drive fault-injection testing of the ADS with and without se… | arXiv:2504.13420 | high |

## References
- [[1]](https://arxiv.org/abs/2301.06262) arXiv:2301.06262
- [[2]](https://arxiv.org/abs/2305.17181) arXiv:2305.17181
- [[3]](https://arxiv.org/abs/2504.13420) arXiv:2504.13420