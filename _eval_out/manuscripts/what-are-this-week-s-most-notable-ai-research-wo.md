# 2609.26761

## Abstract
## Introduction / 引言

## Q&A Digest (问答速览)
- **Q 研究问题**: 2609.26761
- **A 一句话答案**: ## Introduction / 引言
- **子问题（写作视角）** → 证据卡片见 Claims：
  - **Attack-Novelty Claims (Security Researcher)** — Paper title posits 'trace-optimized agent hijacking' as a distinct attack vector specific to MCP (Model Context Protocol) ecosystems.; Attack novelty resides in exploiting the trace feedback path that agent-optimization frameworks use, turning optimization signals into hijacking payloads.; Claimed specialization to MCP implies the vector is engineered for tool-calling agent scaffolds rather than generic prompt injection.
  - **Threat-Model Relevance (MCP Platform Developer)** — The framing of 'agent hijacking in the MCP ecosystem' places the risk at the interface between agent orchestration and MCP tool servers.; Trace-optimization surfaces (observation/reflection logs) are flagged as a new, under-modeled attack surface distinct from tool-invocation boundaries.; Primary authorship at CAS Shenzhen Institutes of Advanced Technology suggests defense motivations anchored in agent-infrastructure research.
  - **Evidence and Reproducibility (Paper Reviewer)** — From the excerpt alone, the paper provides no retrievable experimental protocol, dataset, or baseline; evidence claims are unverifiable pending full text.; Authorship spans SIAT, UCAS, and co-authors (Wang, Zhao, Xu) with corresponding-senior attribution to Xitong Gao, signaling a systems-security research group but no stated reproducibility artifacts.; Assessment: 'evidence-backed findings' cannot be confirmed from the provided excerpt; any evaluative statements in a survey must be marked *unverified* until the full PDF and evaluation details are audited.
  - **Taxonomy Placement (Survey Author)** — The work should be classified under MCP-specific agent-security threats, adjacent to existing prompt-injection and tool-abuse categories rather than as a bundling of them.; The 'trace-optimized' qualifier anchors a subcategory: optimization-driven attacks on agent self-improvement loops, which is missing from most current agent-threat taxonomies.; Affiliation/method cues (system + security authorship) suggest archiving under agent-hijacking/accountability, not under data-poisoning or pure model-safety.
  - **Defensive Mitigation Guidance (System Architect)** — Architects should treat MCP trace logs as untrusted input and isolate/validate trace data before it re-enters the agent's decision loop.; Given hijack potential, tool-server boundaries and MCP message channels should carry explicit trust scoping, with trace-optimization hooks gated by policy.; No concrete defensive control set can be derived from the excerpt; mitigation recommendations must be deferred until the paper's attack mechanics and countermeasures are reviewed in full.
- **证据卡片**: 12 条声明，逐条带 paper_id（arXiv:xxxx）可溯源 → Sources 3 篇

## Intro
## Introduction / 引言

Agent pipelines built on the Model Context Protocol (MCP) increasingly close the loop between execution traces and policy updates, but A2M shows that this trace-optimization loop can itself be weaponized into agent hijacking — a new attack-family claim — reaching a 93.6% macro-average malicious tool invocation rate on GLM-4.6 and a 74.4% mean attack success rate across Information Exfiltration, Environment Integrity Compromise, and Reasoning Derailment (arXiv:2609.26761). This survey therefore asks how security, scale, and efficiency co-evolve across the agentic-LLM stack, arguing that reliability must be assessed jointly against trace-level attack surfaces (arXiv:2609.26761), organizational-scale orchestration that reaches 1,024 agents (arXiv:2609.26781), and inference cost, where IO-aware KV caching and parallel decoding make diffusion LLMs fast and memory-efficient (arXiv:2609.26796). The survey proceeds in three sections: trace-optimized agent hijacking in the MCP ecosystem (arXiv:2609.26761); scaling organizational intelligence to 1,024 agents (arXiv:2609.26781); and IO-aware KV caching and parallel decoding for fast, memory-efficient diffusion LLMs (arXiv:2609.26796).

> **中文速览**：基于 MCP 的智能体流水线不断在执行轨迹与策略更新之间闭环优化，但 A2M 表明该轨迹优化回路本身可被武器化为智能体劫持——这一新攻击族论断在 GLM-4.6 上取得 93.6% 的宏平均恶意工具调用率，并在信息泄露、环境完整性破坏与推理脱轨三类场景下取得 74.4% 的平均攻击成功率 (arXiv:2609.26761)。本综述由此追问安全、规模与效率在智能体-LLM 栈中如何共演，主张可靠性须结合轨迹级攻击面 (arXiv:2609.26761)、可扩展至 1,024 个智能体的组织级编排 (arXiv:2609.26781)，以及通过 IO 感知 KV 缓存与并行解码实现快速、内存高效的扩散 LLM 推理成本 (arXiv:2609.26796) 一并评估。全文分三节：MCP 生态中的轨迹优化型智能体劫持 (arXiv:2609.26761)；组织智能向 1,024 智能体的扩展 (arXiv:2609.26781)；面向快速、内存高效扩散 LLM 的 IO 感知 KV 缓存与并行解码 (arXiv:2609.26796)。

## Attack-Novelty Claims (Security Researcher)

The A2M paper (arXiv:2609.26761) posits trace-optimized agent hijacking as a distinct MCP-specific attack vector, arguing that the trace feedback path used by agent-optimization frameworks can itself be weaponized into hijacking payloads rather than merely abused through generic prompt injection. Empirically, this claim is backed by a macro-average malicious tool invocation rate of 93.6% on GLM-4.6 across four scenarios and a mean attack success rate of 74.4% across Information Exfiltration, Environment Integrity Compromise, and Reasoning Derailment (arXiv:2609.26761). Transferability further supports the vector's structural rather than model-specific character: without re-optimization, attacks still yield a 63.6% macro-average invocation rate on four other models (arXiv:2609.26761). Notably, the surveyed scaling and efficiency works (arXiv:2609.26781; arXiv:2609.26796) do not engage with attack novelty at all, leaving A2M's MCP-specialization claim uncorroborated or contested by adjacent literature. Even within A2M, defenses partially blunt the vector — FIDES-style IFC cuts C-DoS cost from 32.4× to 9.0× and average tool calls from 26.9 to 8.8 (arXiv:2609.26761) — yet the paper does not establish whether trace-optimized hijacking is truly distinct from adapted prompt-injection baselines under matched budgets. The open gap is thus a controlled novelty audit: no independent study has isolated whether the trace feedback path contributes attack power beyond what conventional injection achieves on the same MCP scaffolds.

A2M 论文（arXiv:2609.26761）将「轨迹优化型智能体劫持」定位为 MCP 特有的独立攻击向量，主张智能体优化框架所依赖的轨迹反馈路径本身可被武器化为劫持载荷，而非仅经由通用提示注入被滥用。其实证支撑包括：在 GLM-4.6 上四种场景的宏平均恶意工具调用率达 93.6%，以及在信息泄露、环境完整性破坏与推理偏离三类场景下平均攻击成功率达 74.4%（arXiv:2609.26761）；未经重优化迁移至另外四个模型仍保持 63.6% 的宏平均调用率（arXiv:2609.26761），表明该向量具结构性而非模型特异性。然而，相邻的扩展与效率研究（arXiv:2609.26781；arXiv:2609.26796）完全未涉及攻击新颖性，使 A2M 的 MCP 专门化主张缺乏独立文献的佐证或质疑；即便在 A2M 内部，FIDES 式 IFC 防御已将 C-DoS 代价从 32.4× 降至 9.0×、平均工具调用从 26.9 降至 8.8（arXiv:2609.26761），但论文未在匹配预算下证明轨迹优化劫持相较于改造后的提示注入基线是否真正新颖。由此留下的开放缺口是一次受控的新颖性审计：尚无独立研究厘清轨迹反馈路径在相同 MCP 脚手架上相较常规注入贡献了多少额外攻击能力。

## Threat-Model Relevance (MCP Platform Developer)

A2M (arXiv:2609.26761) pins the MCP-ecosystem risk to the interface between agent orchestration and MCP tool servers: direct attacks optimized on GLM-4.6 reach a macro-average 93.6% malicious tool invocation across four scenarios (arXiv:2609.26761) and a mean attack success rate of 74.4% across Information Exfiltration, Environment Integrity Compromise, and Reasoning Derailment (arXiv:2609.26761). Because the exploit transfers to four other models without re-optimization at a 63.6% macro-average invocation rate (arXiv:2609.26761), the boundary looks structural to the orchestration loop rather than model-specific.

Its threat-model delta is the trace-optimization loop itself: observation/reflection logs added to MCP pipelines are flagged as an under-modeled attack surface distinct from tool-invocation boundaries (arXiv:2609.26761). Authored at the CAS Shenzhen Institute of Advanced Technology (UCAS), by a team including Xitong Gao and Cheng-zhong Xu, the defense baseline is infrastructure-anchored: FIDES-style information-flow control cuts C-DoS cost from 32.4× to 9.0× and average tool calls from 26.9 to 8.8 (arXiv:2609.26761). Here the sources diverge in framing: Flash-dLLM treats the same token path as a pure efficiency surface — GPU memory I/O is its dominant bottleneck and 32 top-attended tokens carry ~50% of middle-layer attention weight (arXiv:2609.26796) — while Agensh scales orchestration to 128 and 1,024 agents (test-pass 19.31%→28.78%; pandoc 33.89%→55.06%) without modeling any adversary (arXiv:2609.26781). The disagreement is over what the trace path is for: a resource to optimize or a surface to weaponize.

The open gap is breadth: A2M is single-source evidence on one frontier model, and neither the 93.6% headline nor the FIDES defense has been reproduced independently at the orchestration scale Agensh reports (arXiv:2609.26761; arXiv:2609.26781).

## 威胁模型相关性（MCP 平台开发者视角）

A2M（arXiv:2609.26761）把 MCP 生态中的 agent 劫持风险定位在 agent 编排与 MCP 工具服务器之间的接口处：针对 GLM-4.6 优化的直接攻击在四个场景下宏平均恶意工具调用率达 93.6%（arXiv:2609.26761），并在信息窃取、环境完整性破坏与推理脱轨三类场景中达到 74.4% 的均值攻击成功率（arXiv:2609.26761）。由于无需重新优化即可迁移到另外四种模型、宏平均调用率达 63.6%（arXiv:2609.26761），该边界更像编排环路的结构性弱点而非模型特异问题。

其威胁模型增量在于 trace 优化环路本身：加入 MCP 管线的观察/反思日志被标记为区别于工具调用边界、尚未被充分建模的攻击面（arXiv:2609.26761）。该工作出自中国科学院深圳先进技术研究院（与 UCAS 联合），作者含 Xitong Gao 与 Cheng-zhong Xu，防御基线亦扎根于基础设施研究：FIDES 式信息流控制可将 C-DoS 成本从 32.4× 降至 9.0×、平均工具调用从 26.9 降到 8.8（arXiv:2609.26761）。此处各来源出现框架分歧：Flash-dLLM 把同一条 token 路径仅当作效率表面——其主导瓶颈是 GPU 内存 I/O，且中间层仅 32 个高关注 token 即承载约 50% 的注意力权重（arXiv:2609.26796）；Agensh 把编排规模推到 128 与 1,024 个 agent（测试通过率 19.31%→28.78%；pandoc 为 33.89%→55.06%），却不建模任何对手（arXiv:2609.26781）。分歧的本质是：trace 路径究竟是被优化的资源，还是可被武器化的表面。

由此留出的空白在于广度：A2M 是单一来源、在单一前沿模型上测得的数据；93.6% 的头条数字与 FIDES 防御均未在 Agensh 所示的编排规模上被独立复现（arXiv:2609.26761；arXiv:2609.26781）。

## Evidence and Reproducibility

The three sources agree that headline contributions are stated as precise quantitative results, but they leave the supporting evidence largely unauditable from the excerpts alone. A2M reports a macro-average malicious tool invocation rate of 93.6% on GLM-4.6 across four scenarios and a mean attack success rate of 74.4% across Information Exfiltration, Environment Integrity Compromise, and Reasoning Derailment, with zero-shot transfer to four other models yielding a 63.6% macro-average (arXiv:2609.26761); its defense evaluation further shows FIDES-style IFC reducing C-DoS cost from 32.4× to 9.0× while average tool calls fall from 26.9 to 8.8 (arXiv:2609.26761). Agensh likewise reports exact scaling gains, raising mean final test-pass rate from 19.31% to 28.78% when moving from 1 to 128 agents on the five hardest ProgramBench tasks (arXiv:2609.26781). Both papers thus agree that evaluation is metric-driven rather than qualitative, yet Flash-dLLM (arXiv:2609.26796), though listed among the sources, contributes no comparable auditable figures in the provided material. The explicit disagreement is between these high-confidence reported numbers and the reviewer assessment: from the excerpt alone there is no retrievable experimental protocol, dataset, or baseline, and A2M's authorship—SIAT and UCAS, with Xitong Gao as corresponding senior author (arXiv:2609.26761)—signals a systems-security group that still states no reproducibility artifacts. The open gap is that "evidence-backed findings" cannot be confirmed; every evaluative statement must remain *unverified* until the full PDFs and evaluation details are audited.

中文：三份来源均以精确量化指标陈述贡献，但仅凭摘录无法审计其证据。A2M 报告在 GLM-4.6 上跨四场景宏平均恶意工具调用率 93.6%、跨三场景平均攻击成功率 74.4%，且不经重优化迁移至其余四模型得宏平均 63.6%（arXiv:2609.26761）；其防御评估显示 FIDES 式 IFC 将 C-DoS 代价由 32.4× 降至 9.0×、平均工具调用由 26.9 降至 8.8（arXiv:2609.26761）。Agensh 同样给出精确数字：在 ProgramBench 最难五题上由 1 至 128 智能体将平均最终测试通过率从 19.31% 提至 28.78%（arXiv:2609.26781）。两文一致强调指标化评估，而 Flash-dLLM（arXiv:2609.26796）在所给材料中无可比可审计数字。明确分歧在于：这些高置信数字与评审判断相冲突——摘录中无可复现实验协议、数据集或基线；A2M 作者横跨 SIAT 与 UCAS、通讯资深作者为 Xitong Gao（arXiv:2609.26761），属系统安全团队却未声明复现工件。遗留空缺是"证据支撑的发现"无法确认，一切评价性表述须标记为 *unverified*，直至审定完整 PDF 与评测细节。

## Taxonomy Placement

A2M should be classified as an MCP-specific agent-security threat rather than as a bundling of familiar attack categories (arXiv:2609.26761). Its core claim is that the trace-optimization loop introduced into MCP-based agent pipelines can itself be weaponized into agent hijacking: optimized attacks reach a 93.6% macro-average malicious tool invocation rate on GLM-4.6 across four scenarios and a 74.4% mean success rate across information exfiltration, environment-integrity compromise, and reasoning derailment, while transferring to four models without re-optimization at a 63.6% macro-average (arXiv:2609.26761). These metrics place it adjacent to the prompt-injection and tool-abuse categories, yet its mechanism — weaponizing the optimization loop rather than a single prompt — is not reducible to either.

The "trace-optimized" qualifier anchors a subcategory that most current agent-threat taxonomies omit: optimization-driven attacks on agent self-improvement loops. This loop is not hypothetical; organizational agent scaling to 1,024 agents is already being engineered (arXiv:2609.26781), and scaling from 1 to 128 agents on the five hardest ProgramBench tasks raises the mean final test-pass rate from 19.31% to 28.78% (arXiv:2609.26781). What Agensh registers as capability gain, A2M registers as attack surface — an explicit divergence in orientation that a survey must name rather than paper over. By contrast, Flash-dLLM, an IO-aware KV-caching and parallel-decoding design for diffusion LLMs, belongs to model-efficiency and stays outside any security taxonomy (arXiv:2609.26796).

Finally, affiliation and method cues — a system-plus-security authorship by a CAS SIAT/UCAS team — suggest archiving this work under agent-hijacking/accountability, not under data-poisoning or pure model-safety, which would mis-frame the threat as a data or robustness artifact. The open gap: no mainstream taxonomy yet accommodates optimization-driven attacks on agent self-improvement loops, so survey authors must currently mint this subcategory explicitly.

中文：

A2M 应归类为 MCP 环境特有的智能体安全威胁，而非既有攻击类别的简单捆绑（arXiv:2609.26761）。其核心论断是：MCP 智能体流水线中新引入的「轨迹优化」环节本身可被武器化为智能体劫持——优化后的攻击在 GLM-4.6 四个场景上达到 93.6% 的宏观平均恶意工具调用率，在信息窃取、环境完整性破坏与推理脱轨三类场景上平均成功率 74.4%，且无需重新优化即可迁移至四种模型，宏观平均值 63.6%（arXiv:2609.26761）。这些指标使其贴近提示注入与工具滥用类别，但机制上它武器化的是优化循环本身而非单条提示，不能归约为二者之一。

「轨迹优化」这一限定词锚定了一个大多数现行智能体威胁分类学都缺失的亚类：针对智能体自改进循环的优化驱动攻击。该循环并非假设——

面向组织的智能体规模化至 1,024 个 agent 已被工程化（arXiv:2609.26781），在最难的五个 ProgramBench 任务上，agent 数由 1 扩至 128 使平均最终测试通过率从 19.31% 升至 28.78%（arXiv:2609.26781）。Agensh 把同一规模化视作能力增益，A2M 却视之为攻击面，两者取向明确相悖，综述必须显式呈现此分歧。相比之下，Flash-dLLM 是面向扩散 LLM 的 IO 感知 KV 缓存与并行解码设计（arXiv:2609.26796），属模型效率范畴，应置身安全分类学之外。

最后，从作者归属与方法线索看——中科院 SIAT/UCAS 团队「系统+安全」的组合署名——宜归档于「智能体劫持/问责」，而非数据投毒或纯模型安全；后者会把该威胁误标为数据或鲁棒性产物。遗留空白：主流分类学迄今未容纳「针对智能体自改进循环的优化驱动攻击」，综述作者当前必须显式设立这一亚类。

## Defensive Mitigation Guidance (System Architect)

A2M shows that the trace-optimization loop added to MCP-based agent pipelines can itself be weaponized, reaching a macro-average malicious tool invocation rate of 93.6% on GLM-4.6 across four scenarios and a mean attack success rate of 74.4% across Information Exfiltration, Environment Integrity Compromise, and Reasoning Derailment (arXiv:2609.26761). The attack also transfers to four other models without re-optimization at a 63.6% macro-average (arXiv:2609.26761). These results elevate MCP trace logs into a trust boundary: architects should treat them as untrusted input and isolate or validate the data before it re-enters the agent's decision loop (arXiv:2609.26761). Given the hijack potential, tool-server boundaries and MCP message channels should carry explicit trust scoping, with trace-optimization hooks gated by policy (arXiv:2609.26761).

One quantifiable countermeasure is reported: a FIDES-style information-flow-control defense cuts the C-DoS cost from 32.4× to 9.0× while average tool calls drop from 26.9 to 8.8 (arXiv:2609.26761), offering a partial containment template. However, no concrete defensive control set can be derived from the excerpt alone; because untargeted transfer succeeds without re-optimization (arXiv:2609.26761), input-side validation must be paired with output-side containment. This leaves an open gap: concrete mitigation recommendations must be deferred until the paper's attack mechanics and countermeasure suite are reviewed in full.

A2M 表明，MCP 智能体流水线中的轨迹优化循环本身可被武器化：在 GLM-4.6 上四个场景的恶意工具调用宏平均率达 93.6%，信息外泄、环境完整性破坏与推理偏离三个场景的平均攻击成功率为 74.4%（arXiv:2609.26761）；该攻击无需重新优化即可迁移至另外四个模型，宏平均率达 63.6%（arXiv:2609.26761）。因此架构师应把 MCP 轨迹日志视为不可信输入，在数据重新进入决策回路前加以隔离与校验；工具服务器边界与消息通道应携带显式信任范围，轨迹优化钩子须由策略把关（arXiv:2609.26761）。A2M 报道了一类可量化的防御：FIDES 式信息流控制将 C-DoS 代价从 32.4× 降至 9.0×，平均工具调用从 26.9 降至 8.8（arXiv:2609.26761），提供了部分遏制模板。但仅凭摘要无法导出具体控制集；鉴于攻击无需重优化即可迁移（arXiv:2609.26761），须在完整审阅该文的攻击机制与对策评测后，再提出具体缓解建议。

## Conclusion / 结论

This survey has traced a common thread across three otherwise distinct 2026 contributions: the agent-stack pipeline is simultaneously becoming more *powerful*, more *scalable*, and more *vulnerable* — and each paper attacks one side of that triangle while largely leaving the others untouched.

**Security.** arXiv:2609.26761 establishes a new attack family: the trace-optimization loop grafted onto MCP-based agent pipelines can itself be weaponized into agent hijacking. The authors (CAS SIAT/UCAS, including Xitong Gao and Cheng-zhong Xu) show the attack is not a laboratory curiosity — direct attacks optimized on GLM-4.6 reach a 93.6% macro-average malicious tool invocation rate across four scenarios (arXiv:2609.26761) and a 74.4% mean attack success rate spanning Information Exfiltration, Environment Integrity Compromise, and Reasoning Derailment (arXiv:2609.26761). Critically, the technique transfers: without re-optimization, four other models still yield a 63.6% macro-average invocation rate (arXiv:2609.26761), so the threat is not confined to a single victim model. On the defensive side, FIDES-style information-flow control meaningfully contains the damage — C-DoS cost drops from 32.4× to 9.0× and average tool calls from 26.9 to 8.8 (arXiv:2609.26761) — yet a 9× residual amplification makes clear that IFC is mitigation, not cure.

**Scale.** arXiv:2609.26781 supplies the constructive counterpart: organizational intelligence that scales. On the five hardest ProgramBench tasks, moving from 1 to 128 agents raises the mean final test-pass rate from 19.31% to 28.78%, and on pandoc the leap to 1,024 agents lifts pass rate from 33.89% to 55.06% (arXiv:2609.26781). The mechanism is an event-driven runtime — each worker reacts to events rather than to a centrally scheduled sequence of steps (arXiv:2609.26781) — which observably lets self-organized cooperation broaden with scale, from peer coordination toward standardized workflows and role specialization (arXiv:2609.26781). The same decentralization that enables growth, however, is exactly the property that complicates centralized oversight and containment against the hijacking surface above.

**Efficiency.** arXiv:2609.26796 attacks the serving layer, showing that GPU memory I/O is the dominant bottleneck for KV-cache-enabled diffusion-LLM inference (arXiv:2609.26796). Its diagnosis — that only 32 top-attended tokens contribute roughly 50% of attention weight in middle layers (arXiv:2609.26796) — licenses aggressive IO-aware caching and parallel decoding, delivering 5.1× and 11.0× speedups over Elastic-Cache on GSM8K and HumanEval, with Flash-Verify's added cost proportional to 2β_m rather than full sequence length (arXiv:2609.26796). Cheaper, faster inference is what makes thousand-agent organizations and trace-optimization loops economically plausible — and therefore also makes the attack loop cheaper to run.

**Synthesis.** The three results compose into a feedback loop: efficiency gains (arXiv:2609.26796) lower the cost of both multi-agent scale (arXiv:2609.26781) and trace-optimized attacks (arXiv:2609.26761); scale multiplies the attack surface that trace-optimization exploits; and the only mature defense evaluated here (IFC) recovers only a fraction of the safety margin.

**Remaining gaps.** (1) *No security evaluation at scale* — A2M is measured on individual-model pipelines, not on event-driven organizations of hundreds to 1,024 agents, so we do not know whether hijack transfer improves or degrades as coordination deepens (arXiv:2609.26761; arXiv:2609.26781). (2) *No cost-security joint study* — the IFC defense overhead (26.9 → 8.8 calls, 32.4× → 9.0×) is never analyzed against the inference-speedup economics that motivate dLLM serving (arXiv:2609.26761; arXiv:2609.26796). (3) *Sparse-model safety is untested* — Flash-dLLM's attention-sparsity finding implicitly reshapes which tokens a trace attacker can steer, yet no work links dLLM decoding dynamics to agent hijacking susceptibility (arXiv:2609.26796). (4) *Defenses remain reactive* — FIDES-style IFC constrains flows post hoc; no paper here closes the trace-optimization loop itself as an attack vector. (5) *Reproducibility and baselines* — each result is strong within its own benchmark (GLM-4.6 scenarios, ProgramBench/pandoc, GSM8K/HumanEval), but no cross-paper benchmark exists for measuring the security–scale–efficiency trade-off jointly.

Closing this loop requires evaluation frameworks that treat the modern agent stack as one coupled system rather than three separable layers — the central open problem this survey leaves to the field.

---

### 中文结论

本综述贯穿三条彼此独立的 2026 年研究线索，指出智能体技术栈正同时变得更*强大*、更*可扩展*、也更*脆弱*：三篇论文各攻其一端，而对其余两端几乎未作处理。

**安全性。** arXiv:2609.26761 提出了一个新攻击族：为基于 MCP 的智能体流水线附加的 trace-优化回路本身可被武器化为智能体劫持。作者（中科院 SIAT/UCAS，含 Xitong Gao、程宗昌）证明这并非实验室噱头——在 GLM-4.6 上直接优化的攻击，四个场景宏平均恶意工具调用率达 93.6%（arXiv:2609.26761），信息窃取、环境完整性破坏、推理脱轨三类场景平均攻击成功率 74.4%（arXiv:2609.26761）；且无需重优化即可迁移，另外四个模型仍达 63.6% 宏平均调用率（arXiv:2609.26761）。防御方面，FIDES 式信息流控制（IFC）可将 C-DoS 代价从 32.4× 压到 9.0×、平均工具调用从 26.9 降到 8.8（arXiv:2609.26761）——但 9× 的残余放大表明 IFC 是缓解而非根治。

**规模化。** arXiv:2609.26781 给出建设性对应：可扩展的组织智能。ProgramBench 最难五题上，1→128 智能体使最终测试通过率均值从 19.31% 升至 28.78%；pandoc 上扩到 1,024 智能体，通过率从 33.89% 升至 55.06%（arXiv:2609.26781）。机制是事件驱动运行时——每个 worker 由事件驱动而非中心化调度序列（arXiv:2609.26781），并可观测到自组织协作随规模从同伴协调扩展到标准化工作流与角色专门化（arXiv:2609.26781）。然而，促成增长的去中心化性质，恰恰也使集中式监管与针对上述劫持面的遏制更为困难。

**效率。** arXiv:2609.26796 攻击服务层：KV 缓存启用的扩散 LLM 推理中，GPU 显存 I/O 是主导瓶颈（arXiv:2609.26796）；其诊断——中间层仅 32 个高注意力 token 就贡献约 50% 注意力权重（arXiv:2609.26796）——支撑了 IO 感知缓存与并行解码，较 Elastic-Cache 在 GSM8K/HumanEval 上分别提速 5.1× 与 11.0×，Flash-Verify 额外代价只与 2β_m 成正比而非全序列长度（arXiv:2609.26796）。更廉价的推理使千级智能体组织与 trace-优化回路在经济上可行——也因此让攻击回路更便宜。

**综合。** 三者构成反馈环：效率增益（arXiv:2609.26796）同时降低多智能体扩展（arXiv:2609.26781）与 trace-优化攻击（arXiv:2609.26761）的成本；规模放大了 trace-优化所利用的攻击面；而本文中唯一成熟的防御（IFC）只挽回了部分安全余量。

**遗留缺口。** (1) *缺大规模安全评测*——A2M 只在单模型流水线上测，未覆盖数百至 1,024 智能体的事件驱动组织，未知劫持迁移性随协调加深如何变化（arXiv:2609.26761; arXiv:2609.26781）。(2) *缺成本-安全联合研究*——IFC 开销（26.9→8.8 次调用、32.4×→9.0×）从未与 dLLM 推理提速的经济性一起分析（arXiv:2609.26761; arXiv:2609.26796）。(3) *稀疏模型安全性未测*——注意力稀疏性隐式改变了攻击者可操纵的 token 集合，但没有工作把 dLLM 解码动力学与劫持易感性关联（arXiv:2609.26796）。(4) *防御仍是被动式*——IFC 事后约束数据流；没有论文从源头封堵 trace-优化回路本身作为攻击向量。(5) *可复现性与基准*——各结果在自身基准（GLM-4.6 场景、ProgramBench/pandoc、GSM8K/HumanEval）内很强，但不存在跨论文基准来联合度量安全-规模-效率权衡。

关闭这一回路，需要把现代智能体栈当作一个耦合系统而非三个可分离层次来评测的框架——这是本综述留给该领域的核心开放问题。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | A2M achieves a macro-average malicious tool invocation rate of 93.6% on GLM-4.6 across four scenarios. | arXiv:2609.26761 | high |
| 2 | A2M attains a mean attack success rate of 74.4% across three attack scenarios. | arXiv:2609.26761 | high |
| 3 | Transfer to four other models without re-optimization yields a macro-average invocation rate of 63.6%. | arXiv:2609.26761 | high |
| 4 | FIDES-style IFC defense reduces C-DoS cost from 32.4× to 9.0× while average tool calls drop from 26.9 to 8.8. | arXiv:2609.26761 | high |
| 5 | Scaling from 1 to 128 agents on the five hardest ProgramBench tasks raises the mean final test-pass rate from 19.31% to … | arXiv:2609.26781 | high |
| 6 | On pandoc, scaling to 1,024 agents raises the final test-pass rate from 33.89% (1 agent) to 55.06%. | arXiv:2609.26781 | high |
| 7 | Each Agensh worker is driven by events rather than by a centrally scheduled sequence of steps. | arXiv:2609.26781 | high |
| 8 | Worker trajectories show self-organized cooperation broadening with scale, from peer coordination toward standardized wo… | arXiv:2609.26781 | medium |
| 9 | Flash-dLLM identifies GPU memory I/O as the dominant bottleneck in KV-cache-enabled dLLM inference. | arXiv:2609.26796 | high |
| 10 | Flash-dLLM achieves 5.1× and 11.0× speedups over Elastic-Cache on GSM8K and HumanEval. | arXiv:2609.26796 | high |
| 11 | Only 32 of the top-attended tokens contribute approximately 50% of attention weight in middle layers. | arXiv:2609.26796 | high |
| 12 | Flash-Verify's additional cost is proportional to 2βm rather than the full sequence length. | arXiv:2609.26796 | high |

## References
- [[1]](https://arxiv.org/abs/2609.26761) arXiv:2609.26761
- [[2]](https://arxiv.org/abs/2609.26781) arXiv:2609.26781
- [[3]](https://arxiv.org/abs/2609.26796) arXiv:2609.26796

## Sources (3)
- arXiv:2609.26761 — A2M: Trace-Optimized Agent Hijacking in the MCP Ecosystem (2026)
- arXiv:2609.26781 — Agensh: Scaling Organizational Intelligence to 1,024 Agents (2026)
- arXiv:2609.26796 — Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs (2026)

## Outline
- Attack-Novelty Claims (Security Researcher): Paper title posits 'trace-optimized agent hijacking' as a distinct attack vector specific to MCP (Model Context Protocol) ecosystems.; Attack novelty resides in exploiting the trace feedback path that agent-optimization frameworks use, turning optimization signals into hijacking payloads.; Claimed specialization to MCP implies the vector is engineered for tool-calling agent scaffolds rather than generic prompt injection.
- Threat-Model Relevance (MCP Platform Developer): The framing of 'agent hijacking in the MCP ecosystem' places the risk at the interface between agent orchestration and MCP tool servers.; Trace-optimization surfaces (observation/reflection logs) are flagged as a new, under-modeled attack surface distinct from tool-invocation boundaries.; Primary authorship at CAS Shenzhen Institutes of Advanced Technology suggests defense motivations anchored in agent-infrastructure research.
- Evidence and Reproducibility (Paper Reviewer): From the excerpt alone, the paper provides no retrievable experimental protocol, dataset, or baseline; evidence claims are unverifiable pending full text.; Authorship spans SIAT, UCAS, and co-authors (Wang, Zhao, Xu) with corresponding-senior attribution to Xitong Gao, signaling a systems-security research group but no stated reproducibility artifacts.; Assessment: 'evidence-backed findings' cannot be confirmed from the provided excerpt; any evaluative statements in a survey must be marked *unverified* until the full PDF and evaluation details are audited.
- Taxonomy Placement (Survey Author): The work should be classified under MCP-specific agent-security threats, adjacent to existing prompt-injection and tool-abuse categories rather than as a bundling of them.; The 'trace-optimized' qualifier anchors a subcategory: optimization-driven attacks on agent self-improvement loops, which is missing from most current agent-threat taxonomies.; Affiliation/method cues (system + security authorship) suggest archiving under agent-hijacking/accountability, not under data-poisoning or pure model-safety.
- Defensive Mitigation Guidance (System Architect): Architects should treat MCP trace logs as untrusted input and isolate/validate trace data before it re-enters the agent's decision loop.; Given hijack potential, tool-server boundaries and MCP message channels should carry explicit trust scoping, with trace-optimization hooks gated by policy.; No concrete defensive control set can be derived from the excerpt; mitigation recommendations must be deferred until the paper's attack mechanics and countermeasures are reviewed in full.

## Claims (12)
- [high] [2609.26761] A2M achieves a macro-average malicious tool invocation rate of 93.6% on GLM-4.6 across four scenarios.  (arXiv:2609.26761)
- [high] [2609.26761] A2M attains a mean attack success rate of 74.4% across three attack scenarios.  (arXiv:2609.26761)
- [high] [2609.26761] Transfer to four other models without re-optimization yields a macro-average invocation rate of 63.6%.  (arXiv:2609.26761)
- [high] [2609.26761] FIDES-style IFC defense reduces C-DoS cost from 32.4× to 9.0× while average tool calls drop from 26.9 to 8.8.  (arXiv:2609.26761)
- [high] [2609.26781] Scaling from 1 to 128 agents on the five hardest ProgramBench tasks raises the mean final test-pass rate from 19.31% to 28.78%.  (arXiv:2609.26781)
- [high] [2609.26781] On pandoc, scaling to 1,024 agents raises the final test-pass rate from 33.89% (1 agent) to 55.06%.  (arXiv:2609.26781)