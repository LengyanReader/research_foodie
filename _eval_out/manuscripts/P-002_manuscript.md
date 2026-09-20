# 2606.24322

## Abstract
Memory is the substrate on which capable LLM agents persist knowledge across turns, yet it is precisely here that two independent research threads converge: how memory should be structured, and how far any of it can be trusted. We survey two recent proposals — MM-Mem (arXiv:2603.01455), a pyramidal multimodal memory anchored in Fuzzy-Trace Theory, and the non-malleable memory construction TMA-NM (arXiv:2606.24322), which establishes that LLM-agent adversaries can launder untrusted memory origins through self-summarization, trusted-tool echo, and manufactured corroboration — and argue that sound agent memory must be simultaneously hierarchical in structure and bound to origin at write time, never to derivable content. The survey proceeds as follows: §II derives the write-time separation the

## Intro
Memory is the substrate on which capable LLM agents persist knowledge across turns, yet it is precisely here that two independent research threads converge: how memory should be structured, and how far any of it can be trusted. We survey two recent proposals — MM-Mem (arXiv:2603.01455), a pyramidal multimodal memory anchored in Fuzzy-Trace Theory, and the non-malleable memory construction TMA-NM (arXiv:2606.24322), which establishes that LLM-agent adversaries can launder untrusted memory origins through self-summarization, trusted-tool echo, and manufactured corroboration — and argue that sound agent memory must be simultaneously hierarchical in structure and bound to origin at write time, never to derivable content. The survey proceeds as follows: §II derives the write-time separation theorem for memory authority; §III dissects the three laundering channels and TMA-NM's non-malleable construction with its 0% attack-success results; §IV maps MM-Mem's sensory→episodic→symbolic hierarchy; §V closes with open problems.

> 中文速览：记忆是可行动 LLM 智能体跨轮次持久化知识的底座，但这里恰好汇聚了两条相互独立的链路：记忆该如何组织，以及其中多少可以被信任。本综述考察两项近期工作——基于模糊痕迹理论（Fuzzy-Trace Theory）构建金字塔式多模态记忆的 MM-Mem（arXiv:2603.01455），以及不可延展记忆构造 TMA-NM（arXiv:2606.24322，证明 LLM 智能体对手可通过自我摘要、可信工具回显与人为佐证三通道漂白不受信任的记忆来源）——并主张健全的智能体记忆必须在结构上分层、在写时绑定来源而非可推演内容。余下安排：§II 推导写时内存分离定理；§III 剖析三种来源漂白通道与 TMA-NM 的不可延展构造及 0% 攻击成功结果；§IV 梳理 MM-Mem 感觉→情景→符号的层级架构；§V 讨论开放问题。

## Overview

arXiv:2606.24322 establishes that memory authority in LLM agents cannot be inferred from content alone: an adversary can launder untrusted memory origins through three channels—self-summarization, trusted-tool echo, and manufactured corroboration (arXiv:2606.24322). Its central formal result is a separation theorem: with write-time origin binding disabled, the security invariant is violated in a reachable state, so binding authority to origin at write time is necessary to sound memory authority (arXiv:2606.24322). The accompanying construction, TMA-NM, binds authority irrevocably to a memory item's origin—never to content or derivation edges—making authority non-malleable (arXiv:2606.24322), and reaches 0% attack success on both direct and laundering attacks across all models and channels while preserving full legitimate utility (arXiv:2606.24322).

Taken together, the two papers approach agent memory from opposite directions. 2606.24322 anchors trust in provenance, explicitly rejecting content or derivation edges as grounds for authority, while 2603.01455 structures memory by content, proposing a pyramidal multimodal architecture with sensory, episodic, and symbolic layers grounded in Fuzzy-Trace Theory (arXiv:2603.01455). Neither design subsumes the other; the open gap is whether origin-bound, non-malleable authority can be reconciled with a content-structured hierarchical memory without sacrificing either full utility or the write-time security invariant—a question the two frameworks jointly raise but neither alone answers.

arXiv:2606.24322 确立：LLM 智能体的记忆权威不能仅凭内容推断——对手可经三条通道洗白不可信来源，即自我摘要、可信工具回显与制造佐证（arXiv:2606.24322）。其核心形式结果是分离定理：若禁用写入时来源绑定，安全不变量会在可达状态中被破坏，故写入时来源绑定对健全的记忆权威是必要的（arXiv:2606.24322）。配套构造 TMA-NM 将权威不可撤销地绑定于条目写入时的来源，而非内容或派生边，使权威不可篡改（arXiv:2606.24322）；在全部模型与通道上，对直接与洗白两种攻击均达 0% 攻击成功率，同时保住完整合法效用（arXiv:2606.24322）。

两篇论文从相反方向处理智能体记忆：2606.24322 把信任锚定在来源，明确拒斥以内容或派生边作为权威依据；2603.01455 则按内容组织记忆，提出基于模糊痕迹理论的分层多模态架构，分为感觉、情景与符号三层（arXiv:2603.01455）。两种设计互不包含；开放缺口在于：来源绑定且不可篡改的权威，能否与按内容组织的分层记忆相调和，而不牺牲完整效用或写入时安全不变量——这正是二者共同提出、却又各自无法单独回答的问题。

## Conclusion

This survey asks what arXiv:2606.24322 establishes — and the answer is a two-part result: poisoning of LLM-agent long-term memory is a systematizable attack class with at least three demonstrated laundering channels, and the countermeasure is structural, not patchwork.

**Key takeaways.** First, adversaries need no direct write access to a trusted memory to corrupt an agent's authority: they can launder untrusted origins through self-summarization (paraphrasing poison into the agent's own note while the derivation edge is dropped), trusted-tool echo, and manufactured corroboration (arXiv:2606.24322). Second, the security invariant is inseparable from *when* origin information is bound: disabling write-time origin binding violates the invariant in a reachable state of the formal model, making write-time binding a necessary — not optional — condition for sound memory authority (arXiv:2606.24322). Third, the construction TMA-NM makes authority non-malleable, bound irrevocably to a memory item's origin at write time and never to content or derivation edges, and reports **0% attack success on both direct and laundering attacks across all models and channels at full legitimate utility** (arXiv:2606.24322). The complementary source extends the canvas to *what* gets stored: MM-Mem organizes multimodal memory pyramidally into sensory, episodic, and symbolic layers, grounding the verbatim-to-gist distillation that long-horizon video agents require (arXiv:2603.01455).

**Remaining gaps.** (1) The 0%-attack-success and full-utility figures are single-paper, self-reported evaluations on a defined channel set; independent replication and adversarial variation beyond the three laundering channels remain missing. (2) The separation theorem holds within the paper's model *M*; how the invariant transfers to real, continuously consolidated agent memories — where gist distillation (e.g., MM-Mem-style abstraction) itself rewrites content and could become a new laundering surface — is unsettled. (3) The security and representation literatures are disjoint: neither source evaluates the other (origin-bound authority applied to verbatim-to-gist compression, or distillation robustness under poisoned inputs). (4) Only partial evidence for arXiv:2603.01455 was available in this survey's evidence pool, so its quantitative video-agent results remain *unverified* here.

**Bottom line.** arXiv:2606.24322 establishes that memory authority must be bound at write time to *origin*, never to content or derivation edges (arXiv:2606.24322); arXiv:2603.01455 establishes that what gets written into long-horizon memory is increasingly a *gist-level abstraction* rather than raw experience (arXiv:2603.01455). The question that unites them: can origin-bound authority survive the encoding itself?

---

## 结论（中文摘要）

本调研追问：arXiv:2606.24322 究竟确立了什么。答案是两件事——面向 LLM 智能体长期记忆的中毒是可系统化的攻击类别（至少三条洗白通道），而对应的防御是结构性而非修补性的。

**核心要点。** 其一，攻击者无需对可信记忆拥有直接写权限即可污染智能体的权威：通过自我摘要（把毒化内容改写进智能体自己的笔记、并丢弃推导边）、可信工具回显、以及制造交叉佐证三种通道，即可洗白不可信来源 (arXiv:2606.24322)。其二，安全不变式与"何时绑定来源"密不可分：在形式化模型中关闭写入时来源绑定，会在可达状态下违反安全不变式——因此写入时绑定是"可靠的记忆权威"的必要条件，而非可选项 (arXiv:2606.24322)。其三，构造 TMA-NM 使权威不可篡改——权威在写入时被不可逆地绑定到记忆条目的来源、而非内容或推导边——并在所有模型、所有通道上报告直接攻击与洗白攻击**成功率为 0%、合法效用无损** (arXiv:2606.24322)。互补来源把视野扩展到"存什么"：MM-Mem 按感觉、情景、符号三层将多模态记忆金字塔化组织，为长时间跨度视频智能体所需的"逐字→要旨"蒸馏提供结构基础 (arXiv:2603.01455)。

**尚存空白。** (1) "0% 攻击成功、全效用"是限定通道集的单篇自报评测，缺少独立复现及三条通道之外的对抗变体。(2) 分离定理仅在论文模型 *M* 内成立；该不变式如何迁移到现实中被持续整合与蒸馏（如 MM-Mem 式要旨抽象本身即在重写内容）的智能体记忆——蒸馏可能成为新的洗白面——仍无定论。(3) 安全线 (arXiv:2606.24322) 与表征线 (arXiv:2603.01455) 互不交叉：既无"来源绑定作用于逐字→要旨压缩"的研究，也无"毒化感知输入下蒸馏是否鲁棒"的检验。(4) 本场证据池对 arXiv:2603.01455 仅取到部分声称，其视频智能体定量结果在本综述中标记为 *unverified*。

**一句话总结。** arXiv:2606.24322 确立：记忆权威必须在写入时绑定来源，而非内容或推导边 (arXiv:2606.24322)；arXiv:2603.01455 确立：写入长期记忆的内容正越来越多地是要旨级抽象而非原始经验 (arXiv:2603.01455)。连接两者的开放问题由此浮现：**来源绑定的权威，能否在编码与蒸馏本身之中幸存？**

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | LLM-agent adversaries can launder untrusted memory origins via three channels: self-summarization, trusted-tool echo, an… | arXiv:2606.24322 | high |
| 2 | Disabling write-time origin binding violates the security invariant, so write-time origin binding is necessary to sound … | arXiv:2606.24322 | high |
| 3 | Authority is bound irrevocably to a memory item's origin at write time, never to content or derivation edges, making it … | arXiv:2606.24322 | high |
| 4 | TMA-NM achieves zero attack success across all models and channels on both direct and laundering attacks while preservin… | arXiv:2606.24322 | high |
| 5 | MM-Mem is a pyramidal multimodal memory architecture grounded in Fuzzy-Trace Theory that structures memory hierarchicall… | arXiv:2603.01455 | high |
| 6 | The authors introduce SIB-GRPO, an optimization objective derived from Information Bottleneck theory that balances seman… | arXiv:2603.01455 | high |

## References
- [[1]](https://arxiv.org/abs/2606.24322) arXiv:2606.24322
- [[2]](https://arxiv.org/abs/2603.01455) arXiv:2603.01455