# Harness Index · Harness 索引

> Generated from `src/harness_factory/data/harnesses.json` — **do not edit by hand**; run `harness catalog --write` to regenerate.
> 由 `data/harnesses.json` 生成，**请勿手改**；用 `harness catalog --write` 重新生成。

**Updated:** 2026-10-12 · 64 entries · 9 classes · companion to `harness-catalog.md` (the prose taxonomy).

---

## How to use · 用法

```bash
harness catalog                       # list everything
harness catalog --class self-evolution
harness catalog --kind memory-system
harness catalog --module M5           # harnesses that exercise a core module
harness catalog --search voyager
harness catalog --tracked             # only entities also tracked in sources.json
harness catalog claude-code           # detail one entry
```

---

## Coding / software harnesses · 编码 harness  (11)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `opencode` | opencode · opencode | 终端编码 agent | M1, M6, M7 | https://github.com/sst/opencode |
| `claude-code` | Claude Code · Claude Code | 终端编码 agent | M1, M6, M7 | https://docs.anthropic.com/en/docs/claude-code · tracked:anthropic-claude-code |
| `codex-cli` | Codex CLI · Codex CLI | 终端编码 agent | M1, M6, M7 | https://github.com/openai/codex · tracked:openai-codex-cli |
| `gemini-cli` | Gemini CLI · Gemini CLI | 终端编码 agent | M1, M6, M7 | https://github.com/google-gemini/gemini-cli · tracked:google-gemini-cli |
| `openhands` | OpenHands · OpenHands | 终端编码 agent | M1, M6, M7, M8 | https://github.com/All-Hands-AI/OpenHands |
| `swe-agent` | SWE-agent · SWE-agent | 终端编码 agent | M1, M6, M7 | https://github.com/SWE-agent/SWE-agent · tracked:swe-agent |
| `aider` | Aider · Aider | 终端编码 agent | M1, M6, M7 | https://github.com/Aider-AI/aider |
| `cline` | Cline · Cline | IDE 侧 agent | M1, M6, M7, M8 | https://github.com/cline/cline |
| `roo-code` | Roo Code · Roo Code | IDE 侧 agent | M1, M6, M7 | https://github.com/RooCodeInc/Roo-Code |
| `goose` | goose · goose | 终端编码 agent | M1, M6, M7 | https://github.com/block/goose |
| `crush` | crush · crush | 终端编码 agent | M1, M6, M7 | https://github.com/charmbracelet/crush |

## Orchestration frameworks / agent SDKs · 编排框架与 SDK  (11)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `claude-agent-sdk` | Claude Agent SDK · Claude Agent SDK | agent SDK / 框架 | M6, M7, M8 | https://docs.anthropic.com/en/api/agent-sdk/overview · tracked:anthropic-agent-sdk |
| `openai-agents-sdk` | OpenAI Agents SDK · OpenAI Agents SDK | agent SDK / 框架 | M6, M7, M8 | https://github.com/openai/openai-agents-python · tracked:openai-agents-sdk |
| `openai-swarm` | Swarm · Swarm | agent SDK / 框架 | M6, M8 | https://github.com/openai/swarm · tracked:openai-swarm |
| `google-adk` | Agent Development Kit (ADK) · Agent Development Kit (ADK) | agent SDK / 框架 | M6, M7, M8 | https://github.com/google/adk-python · tracked:google-adk |
| `smolagents` | smolagents · smolagents | agent SDK / 框架 | M6 | https://github.com/huggingface/smolagents |
| `langgraph` | LangGraph · LangGraph | agent SDK / 框架 | M6, M7 | https://github.com/langchain-ai/langgraph · tracked:langchain |
| `autogen` | AutoGen · AutoGen | agent SDK / 框架 | M6, M8 | https://github.com/microsoft/autogen · tracked:autogen |
| `crewai` | CrewAI · CrewAI | agent SDK / 框架 | M6, M8 | https://github.com/crewAIInc/crewAI · tracked:crewai |
| `llama-stack` | Llama Stack · Llama Stack | agent SDK / 框架 | M6, M7 | https://github.com/meta-llama/llama-stack · tracked:meta-llama-stack |
| `a2a` | Agent2Agent (A2A) · Agent2Agent (A2A) | 协议 | M7, M8 | https://github.com/a2aproject/A2A · tracked:google-a2a |
| `dspy` | DSPy · DSPy | agent SDK / 框架 | M6 | https://github.com/stanfordnlp/dspy · tracked:dspy |

## Self-evolution methods · 自我演化方法  (13)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `adas` | ADAS / Meta Agent Search · ADAS / Meta Agent Search | 改自身脚手架 | M5, M7 | arXiv:2408.08435 (ICLR 2025) |
| `godel-agent` | Gödel Agent · Gödel Agent | 改自身脚手架 | M5, M7 | arXiv:2410.04444 / ACL 2025 |
| `sica` | Self-Improving Coding Agent (SICA) · 自改进编码 agent (SICA) | 改自身脚手架 | M5, M7 | arXiv:2504.15228 |
| `dgm` | Darwin Gödel Machine (DGM) · 达尔文哥德尔机 (DGM) | 改自身脚手架 | M5, M7 | arXiv:2505.22954 |
| `funsearch` | FunSearch · FunSearch | 进化式代码搜索 | M5 | Nature 624:545-552 (2023) |
| `alphaevolve` | AlphaEvolve · AlphaEvolve | 进化式代码搜索 | M5 | arXiv:2506.13131 |
| `openevolve` | OpenEvolve · OpenEvolve | 进化式代码搜索 | M5 | https://github.com/algorithmicsuperintelligence/openevolve |
| `codeevolve` | CodeEvolve · CodeEvolve | 进化式代码搜索 | M5 | arXiv:2510.14150 |
| `seal` | SEAL (Self-Adapting Language Models) · SEAL（自适配语言模型） | 改自身权重 | M5 | arXiv:2506.10943 (NeurIPS 2025) |
| `self-rewarding-lm` | Self-Rewarding Language Models · 自奖励语言模型 | 改自身权重 | M5 | arXiv:2401.10020 |
| `reflexion` | Reflexion · Reflexion | 推理期自我修正 | M3, M5 | arXiv:2303.11366 (NeurIPS 2023) |
| `self-refine` | Self-Refine · Self-Refine | 推理期自我修正 | M3 | arXiv:2303.17651 (NeurIPS 2023) |
| `voyager` | Voyager · Voyager | 技能沉淀 | M5, M6 | arXiv:2305.16291 |

## Memory & persistence · 记忆与持久化  (4)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `memgpt-letta` | MemGPT / Letta · MemGPT / Letta | 记忆系统 | M2 | arXiv:2310.08560 |
| `mem0` | Mem0 · Mem0 | 记忆系统 | M2, M4 | arXiv:2504.19413 |
| `zep-graphiti` | Zep / Graphiti · Zep / Graphiti | 记忆系统 | M2, M4 | arXiv:2501.13956 |
| `a-mem` | A-MEM · A-MEM | 记忆系统 | M2 | Xu et al. 2025 |

## Skills ecosystems & protocols · 技能生态与协议  (2)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `anthropic-agent-skills` | Anthropic Agent Skills · Anthropic Agent Skills | 技能生态 | M1, M6 | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview |
| `mcp` | Model Context Protocol (MCP) · 模型上下文协议 (MCP) | 协议 | M1, M6 | https://modelcontextprotocol.io · tracked:anthropic-mcp |

## Evaluation harnesses · 评测 harness  (11)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `swe-bench` | SWE-bench · SWE-bench | 基准/评测器 | M3 | arXiv:2310.06770 |
| `terminal-bench` | Terminal-Bench · Terminal-Bench | 基准/评测器 | M3 | https://github.com/laude-institute/terminal-bench |
| `arc-agi` | ARC-AGI · ARC-AGI | 基准/评测器 | M3 | https://arcprize.org |
| `livecodebench` | LiveCodeBench · LiveCodeBench | 基准/评测器 | M3 | https://github.com/LiveCodeBench/LiveCodeBench |
| `polyglot` | SWE-bench Polyglot · SWE-bench Polyglot | 基准/评测器 | M3 | https://github.com/swe-bench/swe-bench.github.io |
| `locomo` | LoCoMo · LoCoMo | 基准/评测器 | M2, M3 | https://github.com/snap-research/locomo |
| `longmemeval` | LongMemEval · LongMemEval | 基准/评测器 | M2, M3 | https://github.com/xiaowu0162/LongMemEval |
| `lm-eval-harness` | LM Evaluation Harness · LM Evaluation Harness | eval-framework | M3 | https://github.com/EleutherAI/lm-evaluation-harness |
| `helm` | HELM · HELM | eval-framework | M3, M4 | https://github.com/stanford-crfm/helm |
| `simple-evals` | simple-evals · simple-evals | eval-framework | M3 | https://github.com/openai/simple-evals |
| `lighteval` | LightEval · LightEval | eval-framework | M3 | https://github.com/huggingface/lighteval |

## Surveys (orientation) · 综述导航  (5)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `survey-self-evolving-agents` | Self-Evolving Agents: What/When/How/Where · 自演化 agent 综述（What/When/How/Where） | 综述 | M0, M5 | arXiv:2507.21046 (TMLR 2026) |
| `survey-co-evolution` | Co-Evolution in Agentic Systems · agent 系统中的共同演化 | 综述 | M5, M8 | arXiv:2608.10299 |
| `survey-self-improvements` | Self-Improvements in Modern Agentic Systems · 现代 agent 系统的自我改进综述 | 综述 | M5 | arXiv:2607.13104 |
| `survey-agentic-rl` | Agentic RL for LLMs · LLM 的 agentic 强化学习综述 | 综述 | M5 | arXiv:2509.02547 |
| `survey-memory` | Memory in the Age of AI Agents · AI agent 时代的记忆综述 | 综述 | M2 | arXiv:2512.13564 |

## Safety of self-evolution · 自我演化安全  (2)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `saver` | SAVER (Safety in Self-Evolving Agents) · SAVER（自演化 agent 的安全） | 安全框架 | M0, M5, M8 | arXiv:2610.00093 |
| `misevolution` | Misevolution (Emergent Risks in Self-evolving LLM Agents) · Misevolution（自演化 agent 的涌现风险） | 安全框架 | M0, M5, M8 | arXiv:2509.26354 |

## Discovery / evidence & model search · 发现·证据与模型搜索  (5)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `elicit` | Elicit · Elicit | evidence-extractor | M1, M4 | https://elicit.com/ |
| `consensus` | Consensus · Consensus | evidence-synthesizer | M1, M4 | https://consensus.app/ |
| `connected-papers` | Connected Papers · Connected Papers | graph-explorer | M1, M4 | https://www.connectedpapers.com/ |
| `researchrabbit` | ResearchRabbit · ResearchRabbit | graph-explorer | M1, M4 | https://www.researchrabbit.ai/ |
| `paperswithcode` | PapersWithCode · PapersWithCode | index | M1, M4 | https://paperswithcode.com/ |

---

## Cross-links · 交叉链接

- Prose taxonomy & design lessons: [`harness-catalog.md`](harness-catalog.md).
- Tracked feeds for these entities: `data/sources.json` (`harness sources`).
- Core modules M0–M8: [`../core/00-index.md`](../core/00-index.md).
