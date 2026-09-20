# 2507.10593

## Abstract
## Intro

## Intro
## Intro

**EN.** As LLM applications grow more dependent on standardized tool-integration protocols, the choice between competing standards—Model Context Protocol (MCP) versus OpenAPI-compatible REST—carries significant performance and engineering consequences that are rarely quantified. This survey asks what the ToolRegistry study (arXiv:2507.10593) establishes on that question, and the benchmark evidence answers pointedly: a FastMCP server in SSE mode reaches only ~33% of the throughput of an OpenAPI-compatible FastAPI server exposing the same service code (arXiv:2507.10593), yet even strong information-retrieval models demonstrably fail at tool selection—the gap ToolRegistry's BM25F-based progressive disclosure is designed to close (arXiv:2507.10593). The paper also establishes a quantifiable integration-code win (60–80% reduction) and observes that all three major providers—Anthropic, OpenAI, Google—now announce MCP support (arXiv:2507.10593). The remainder proceeds as follows: Section 2 frames the motivation (tool-selection failure and the evolution of tool-augmented LLMs), Section 3 contrasts the protocol landscape (MCP vs. OpenAPI), Section 4 analyzes ToolRegistry's design and results, and Section 5 discusses limitations and open questions.

> **中文速览.** 本综述追问 ToolRegistry 研究（arXiv:2507.10593）究竟确立了哪些结论。基准证据给出的答案很明确：用 SSE 模式的 FastMCP 服务器暴露同一份服务代码时，吞吐量仅为 OpenAPI 兼容 FastAPI 的约 33%（arXiv:2507.10593）；与此同时，即使是强信息检索模型在工具选择上仍表现不佳——这正是 ToolRegistry 基于 BM25F 的渐进式披露所针对的缺口（arXiv:2507.10593）。论文还报告集成代码量可削减 60–80%，并观察到 Anthropic、OpenAI、Google 三家主要厂商均已宣布支持 MCP（arXiv:2507.10593）。后文依次展开：动机与工具增强 LLM 的演进（第 2 节）、MCP 与 OpenAPI 的协议格局对比（第 3 节）、ToolRegistry 的设计与结果（第 4 节）、局限与开放问题（第 5 节）。

## Overview

> 中文速览：arXiv:2507.10593 提出 ToolRegistry，一种面向 LLM 工具生态的注册/管理系统，主张在 MCP 与 OpenAPI 两条既有路径之外提供"以吞吐与集成效率优先"的第三解。三个核心实证论断：其一，按其基准，集成代码量可削减 60–80%（arXiv:2507.10593）；其二，SSE 模式下的 FastMCP 服务器吞吐仅为暴露相同服务的 OpenAPI 兼容 FastAPI 服务器的约 33%（arXiv:2507.10593）；其三，工具选择是公认难点——论文援引 Shi 等发现即便强信息检索模型在工具选择上仍表现不佳，从而引出其 BM25F 渐进式披露设计（arXiv:2507.10593）。需注意：性能数字均为单篇自报基准，第三方独立对比尚属空白。

arXiv:2507.10593 introduces **ToolRegistry**, a tool-registry system aimed at the integration bottleneck that has emerged as LLMs increasingly depend on external tools. The paper positions ToolRegistry against two incumbent approaches — Model Context Protocol (MCP) and OpenAPI-compatible servers — and advances three central empirical claims. On engineering effort, ToolRegistry reports that its library cuts integration code by 60–80% per its own benchmarks (arXiv:2507.10593). On routing philosophy, it frames OpenAPI as "a counterpoint to MCP," reporting that a FastMCP server in SSE mode achieves only around 33% of the throughput of an OpenAPI-compatible FastAPI server when exposing the same service code (arXiv:2507.10593) — a striking gap given that all three major providers (Anthropic, OpenAI, Google) now announce MCP support (arXiv:2507.10593).

The design is further motivated by the tool-selection problem: the paper cites Shi et al.'s finding that even strong information-retrieval models perform poorly on tool selection, which motivates ToolRegistry's BM25F-based progressive disclosure (arXiv:2507.10593). Taken together, these claims establish ToolRegistry as a distinct software-engineering answer to the tool-ecosystem problem — one that privileges throughput and reduced integration effort over protocol interoperability. The open gap this leaves is verification: the throughput and 60–80% figures are single-paper, self-reported benchmarks, and independent third-party head-to-head studies across MCP, OpenAPI, and ToolRegistry have not yet been published. (Note: the co-cited sources arXiv:2605.18805 and arXiv:2111.01762 lie outside this section's scope and are not synthesized here.) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (arXiv:2507.10593) (## Overview

> 中文速览：arXiv:2507.10593 提出 ToolRegistry，一款面向 LLM 工具生态的注册系统。按其自有基准，该库能将集成代码削减 60–80%（arXiv:2507.10593）；据其报告，SSE 模式下的 FastMCP 服务器吞吐仅为暴露相同服务的 OpenAPI 兼容 FastAPI 服务器的约 33%（arXiv:2507.10593）。论文援引 Shi 等的发现——即便强信息检索模型在工具选择上仍表现不佳——以此引出其 BM25F 渐进式披露设计（arXiv:2507.10593）。三家主要厂商（Anthropic、OpenAI、Google）均已宣布支持 MCP（arXiv:2507.10593）。但上述性能数字均为单篇自报，第三方独立对比尚属空白。

arXiv:2507.10593 introduces **ToolRegistry**, a registry system aimed at the integration bottleneck that has emerged as LLMs increasingly rely on external tools. The paper advances three central claims. On engineering effort, its library cuts integration code by 60–80% per its own benchmarks (arXiv:2507.10593). On protocol performance, it frames OpenAPI as a counterpoint to MCP, reporting that a FastMCP server in SSE mode achieves only around 33% of the throughput of an OpenAPI-compatible FastAPI server exposing the same service code (arXiv:2507.10593) — a striking gap given that all three major providers (Anthropic, OpenAI, Google) now announce MCP support (arXiv:2507.10593).

This throughput-first stance is motivated by tool selection, which the paper identifies as a known weakness: citing Shi et al.'s finding that even strong information-retrieval models perform poorly on tool selection, it motivates ToolRegistry's BM25F-based progressive disclosure (arXiv:2507.10593). Together these claims position ToolRegistry as a software-engineering answer that privileges throughput and reduced integration effort over protocol interoperability. The open gap is verification: both the ~33% throughput ratio and the 60–80% integration-savings figures are single-paper, self-reported benchmarks, and independent head-to-head studies across MCP, OpenAPI, and ToolRegistry have yet to be published. (Co-listed sources arXiv:2605.18805 and arXiv:2111.01762 fall outside this section's scope.)

> 中文速览
> 本综述的核心结论：工具增强型 AI 生态正从各家私有的工具调用接口转向协议级抽象——MCP 已成为跨厂商标准（arXiv:2507.10593）；但协议胜利并非免费：同为 SSE 传输时，MCP 端点吞吐仅约为 OpenAPI/FastAPI 的三分之一（arXiv:2507.10593）；工具选择仍是检索难题，强 IR 模型表现不佳，催生 BM25F 渐进式披露等检索优先方案（arXiv:2507.10593）；对开发者而言，目录化库可削减 60–80% 集成代码（arXiv:2507.10593）；与之呼应，AIRCC-Clim 以极低计算与技术要求模拟 37 个海气耦合环流模式（arXiv:2111.01762），说明抽象层（协议或仿真器）是让重负载系统变得可用、可负担的共同杠杆。

## Conclusion

This survey paints a convergent picture: as tool-augmented agents move toward production, the center of gravity in the tool layer is shifting from per-vendor proprietary interfaces toward shared, protocol-level abstractions. The clearest signal is standardization — all three major providers now announce support for the Model Context Protocol (MCP) (arXiv:2507.10593), giving tool-calling a common vocabulary across the ecosystem.

That protocol win, however, does not come for free. On identical service code, a FastMCP server in SSE mode reaches only around 33% of the throughput of an OpenAPI-compatible FastAPI server (arXiv:2507.10593) — a transport-level gap that makes serving design a first-class performance decision, not just an interface choice. The search layer faces an analogous bottleneck: even strong information-retrieval models perform poorly at tool selection, which motivates retrieval-first designs such as ToolRegistry's BM25F-based progressive disclosure (arXiv:2507.10593).

Adoption economics are nonetheless favorable on the developer side: cataloging-style libraries are reported to cut integration code by 60–80% (arXiv:2507.10593), lowering the barrier to exposing tools to agents. Complementing the serving side, AIRCC-Clim demonstrates that 37 atmosphere-ocean coupled general circulation models can be emulated with low computational and technical requirements for the user (arXiv:2111.01762) — reinforcing the meta-observation that abstraction layers (protocols, catalogs, or emulators) are what make heavy agent-facing systems tractable in practice.

## Remaining gaps

- The 33% throughput figure covers MCP over SSE only; no standardized comparison across streaming-HTTP, WebSocket, or gRPC transports was reviewed (own observation, *unverified*).
- Efficiency numbers are library-specific and directional; a common, cross-implementation benchmark suite for MCP server throughput does not yet exist (own observation, *unverified*).
- Claims from arXiv:2605.18805 were not available in the working context, so that strand of the survey could not be synthesized and remains an open thread.
- The link between tool-protocol design and surrogate-model emulation is currently suggestive rather than proven; a deeper comparative analysis is outside this survey's scope.

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | ToolRegistry reports that a FastMCP server in SSE mode achieves only around 33% of the throughput of an OpenAPI-compatib… | arXiv:2507.10593 | high |
| 2 | Per the paper's benchmarks, ToolRegistry cuts integration code by 60–80%. | arXiv:2507.10593 | high |
| 3 | The paper cites Shi et al. finding that even strong information-retrieval models perform poorly on tool selection, motiv… | arXiv:2507.10593 | high |
| 4 | All three major providers (Anthropic, OpenAI, Google) now announce support for the Model Context Protocol (MCP). | arXiv:2507.10593 | high |
| 5 | AIRCC-Clim emulates 37 atmosphere-ocean coupled general circulation models with low computational and technical requirem… | arXiv:2111.01762 | high |
| 6 | AIRCC-Clim is a standalone, easy-to-use program for Windows and Linux systems | arXiv:2111.01762 | high |
| 7 | Probabilistic projections are built through stochastic simulation to represent uncertainty in the climate sensitivity pa… | arXiv:2111.01762 | high |
| 8 | Four RCP emissions trajectories are included by default and editable by the user | arXiv:2111.01762 | high |

## References
- [[1]](https://arxiv.org/abs/2507.10593) arXiv:2507.10593
- [[2]](https://arxiv.org/abs/2111.01762) arXiv:2111.01762
- [[3]](https://arxiv.org/abs/2605.18805) arXiv:2605.18805