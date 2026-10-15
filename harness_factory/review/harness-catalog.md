# AI Harness Catalog · AI Harness 全谱系

> A taxonomy of agent harnesses and, in depth, **self-evolution methods** — the machinery by which a harness improves itself.
> 一份 agent harness 的分类学，并重点罗列**自我演化方法**——harness 借以自我改进的机制。
> **Updated:** 2026-10-12 · All URLs retrieved 2026-10-12. Companion to `practitioner-playbook.md`.

---

## 中文速览

**这份文档做什么。** 把当前（as of 2026-10）可观察到的 agent **harness** 系统性地归类，重点放在用户最关心的**自适应 / 自我演化方法**上：哪些方法在改**代码/脚手架**，哪些在改**权重**，哪些只在**推理期**自我修正，哪些在**积累记忆/技能**。每条给出「机制一句话 + 一手来源」。

**一句话结论。** 目前能自我改进的系统可沿两个轴切分：**改什么**（scaffold 代码 / 模型权重 / 上下文与记忆 / 技能库）和**靠什么信号**（基准分数 / 环境反馈 / 自我评判 / 进化档案）。真正的**递归自我改进**（agent 改「自己改自己的那部分代码」）目前由 **Gödel Agent、DGM、SICA** 这一类代表；**进化式代码搜索**由 **FunSearch / AlphaEvolve / OpenEvolve / CodeEvolve** 代表；**权重自适应**由 **SEAL / Self-Rewarding LMs** 代表；**推理期自我修正**由 **Reflexion / Self-Refine** 代表；**技能沉淀**由 **Voyager** 代表。安全上，**SAVER** 与 **Misevolution** 说明：一旦「经验变成可复用状态」，过去的事件会成为未来的因，安全属性必须跨「积累/复用」存活。

**怎么用。** 用 §Taxonomy 定位类别；若你造的是自我演化 harness，直接读 §3 与 §7；每条目的 **Maps to** 指向 `core/` 模块。

> **诚实性声明 / Integrity note.** 所有条目均给一手来源（论文 / 官方仓库 / 官方文档）。*Early-pass IDs pending re-verification* are flagged inline. Pricing/leaderboard-style numbers are **directional**.

---

## Taxonomy · 分类总览

| # | Class · 类别 | What it is · 是什么 | Representative systems · 代表 | Maps to |
|---|-------------|--------------------|------------------------------|---------|
| 1 | Coding / software harnesses | Interactive coding agents; the "harness" is the scaffold around a model | opencode, Claude Code, Codex CLI, Gemini CLI, OpenHands, SWE-agent, Aider, Cline, Roo Code, goose, crush | M1,M6,M7 |
| 2 | Orchestration frameworks / agent SDKs | Libraries to compose agents, tools, workflows | Claude Agent SDK, OpenAI Agents SDK, Google ADK, smolagents, LangGraph, AutoGen, CrewAI | M6,M7,M8 |
| 3 | **Self-evolution methods** | Systems that improve themselves | see §3 | M5 |
| 3a | — Scaffold / code self-modification | Agent edits its own codebase | ADAS, Gödel Agent, SICA, Darwin Gödel Machine | M5,M7 |
| 3b | — Evolutionary code search | LLM-as-mutation over programs | FunSearch, AlphaEvolve, OpenEvolve, CodeEvolve | M5 |
| 3c | — Weight self-adaptation | Agent updates its own weights | SEAL, Self-Rewarding LMs, STaR (see note) | M5 |
| 3d | — Inference-time self-correction | No weight change; verbal feedback loop | Reflexion, Self-Refine | M3,M5 |
| 3e | — Skill-library growth | Commit verified skills for reuse | Voyager | M5,M6 |
| 4 | Memory & persistence | External, evolving state | MemGPT/Letta, Mem0, Zep/Graphiti, A-MEM | M2 |
| 5 | Skills ecosystems & protocols | Progressive-disclosure skills; tool protocols | Anthropic Agent Skills, MCP | M1,M6 |
| 6 | Evaluation harnesses | Benchmarks that grade agents | SWE-bench, Terminal-Bench, ARC-AGI, LiveCodeBench, Polyglot, LoCoMo/LongMemEval | M3 |
| 7 | Surveys (orientation) | Frameworks to read the field | Gao et al. 2026; co-evolution; self-improvements; agentic RL; memory; self-play | M0,M5 |
| 8 | Safety of self-evolution | How evolution breaks | SAVER; Misevolution | M0,M5,M8 |

---

## 1. Coding / software harnesses · 编码 harness

The clearest "harness" exemplars: a model plus a scaffold (tools, context management, permissions, verification). Representative, **not exhaustive** (names and repos as of 2026-10-12).

| Harness | Distinguishing scaffold idea | Source |
|---|---|---|
| **opencode** | Open-source terminal coding agent; provider-agnostic; plugin/skill system | GitHub `sst/opencode` |
| **Claude Code** | Terminal agent with a skills/subagent model and permission gates | Anthropic |
| **Codex CLI** | OpenAI's local coding agent; repo-legible, agent-first workflow | GitHub `openai/codex` |
| **Gemini CLI** | Google's open-source terminal agent; MCP support | GitHub `google-gemini/gemini-cli` |
| **OpenHands** | Open platform for software agents; sandboxed runtime | GitHub `All-Hands-AI/OpenHands` |
| **SWE-agent** | Agent-computer interface for issue resolution | GitHub `SWE-agent/SWE-agent` |
| **Aider** | Git-native pair programmer; repo map | GitHub `Aider-AI/aider` |
| **Cline / Roo Code** | IDE-side agents (VS Code lineage) with human-in-the-loop approvals | GitHub `cline/cline`; Roo Code |
| **goose** | Block's extensible open-source agent | GitHub `block/goose` |
| **crush** | Terminal agent from Charm | Charm |

> **Pattern (M6).** All converge on the same scaffold concerns: a minimal toolset with **biased errors**, context compaction, explicit permission gates, and a way to verify "done". The differentiator is *how* they let you engineer the harness (plugins, skills, rules files).

---

## 2. Orchestration frameworks / agent SDKs · 编排框架

Libraries for building harnesses rather than turnkey agents.

- **Claude Agent SDK** — build agents on the same loop/skills primitives as Claude Code (Anthropic).
- **OpenAI Agents SDK** — lightweight agent loop, handoffs, guardrails (OpenAI).
- **Google Agent Development Kit (ADK)** — multi-agent orchestration (Google).
- **smolagents** — minimal code-writing agents (Hugging Face).
- **LangGraph** — graph/state-machine orchestration with checkpointing (LangChain).
- **AutoGen / CrewAI** — multi-agent conversation and role teams.

> **Pattern (M7,M8).** The framework choice mostly decides your **state model** (graph vs. loop vs. conversation) and your **handoff/contract** mechanism. See `core/09-collaboration-and-sessions.md`.

---

## 3. Self-evolution methods · 自我演化方法

**The core of this catalog.** Two axes: *what is updated* (scaffold code / model weights / context & memory / skill library) and *what signal drives the update* (benchmark score / environment feedback / self-judgment / evolutionary archive).

### 3a. Scaffold / code self-modification · 改自身脚手架

The agent edits the code that defines it. Degrees of self-reference matter: a **separate meta-agent** vs. a **truly self-referential** loop where the agent edits the part that edits itself.

| Method | Mechanism in one line | Self-reference | Source |
|---|---|---|---|
| **ADAS / Meta Agent Search** | A meta-agent programs new agents in code, keeps an archive of discoveries, iterates | Meta-agent edits *target* agents (not itself) | arXiv:2408.08435 (ICLR 2025) [2] |
| **Gödel Agent** | Agent reads and monkey-patches its own runtime code, including the update logic, guided only by a high-level objective | **Fully self-referential** (recursive) | arXiv:2410.04444 / ACL 2025 [3] |
| **SICA** | Best archived agent becomes meta-agent; edits its own Python to improve cost/speed/benchmark | Self-referential (no meta/target split) | arXiv:2504.15228 [1] |
| **Darwin Gödel Machine (DGM)** | Self-modifying coding agent + open-ended archive of stepping stones (Darwinian) | Self-referential + open-ended archive | arXiv:2505.22954 [4] |

**Design lesson (M5,M7).** *Keep an archive, not just hill-climb.* DGM showed that less-performing ancestors can be the stepping stones to later breakthroughs; pure hill-climbing converges prematurely. Pair every self-modification with **empirical validation** (SICA: utility = 0.5·score + 0.25·cost + 0.25·time) and with **traceability** of the change.

### 3b. Evolutionary code search · 进化式代码搜索

LLM as a smart mutation operator over a program database; an automated evaluator scores candidates.

| Method | Mechanism | Source |
|---|---|---|
| **FunSearch** | LLM proposes functions; evaluator scores; best returned to a diverse program database | *Nature* 2023 [10] |
| **AlphaEvolve** | Evolves whole codebases; prompt-sampler + LLM ensemble + evaluator pool + island/MAP-Elites DB | arXiv:2506.13131 [11] |
| **OpenEvolve** | Open re-implementation of AlphaEvolve (prompt sampler / LLM ensemble / evaluator pool / program DB) | GitHub `algorithmicsuperintelligence/openevolve` [12] |
| **CodeEvolve** | Island-based GA + inspiration crossover + meta-prompting; open source | arXiv:2510.14150 [13] |

**Design lesson (M5).** The evaluator is the lynchpin: "LLM creativity guarded by an objective evaluator" is what turns hallucination-prone generation into *verifiable discovery*. This is the same **refinement loop** as Chollet's (see `practitioner-playbook.md`).

### 3c. Weight self-adaptation · 改自身权重

The model changes its own parameters (persistent, costly, highest authority — and highest risk).

| Method | Mechanism | Source |
|---|---|---|
| **SEAL** | Model generates its own finetuning data + update directives ("self-edits"); RL rewards self-edits whose applied update improves the task | arXiv:2506.10943 (NeurIPS 2025) [5] |
| **Self-Rewarding LMs** | Model is its own reward model via LLM-as-a-Judge; Iterative DPO improves both instruction-following and rewarding | arXiv:2401.10020 [6] |
| *(STaR / Constitutional AI / Meta-Rewarding)* | Rationale-based self-training / principle-based self-critique / judge-the-judge | **To verify before formal citation** — see note |

### 3d. Inference-time self-correction · 推理期自我修正

No weight change; convert feedback into language and retry.

| Method | Mechanism | Source |
|---|---|---|
| **Reflexion** | Actor + Evaluator + Self-Reflection; verbal reflections stored in episodic memory drive later trials | arXiv:2303.11366 (NeurIPS 2023) [8] |
| **Self-Refine** | Same model produces → critiques → refines iteratively; no training | arXiv:2303.17651 (NeurIPS 2023) [7] |

**Design lesson (M3).** These are the lightest self-improvement loop and the easiest to gate: bounded memory (1–3 reflections), explicit feasibility limits (Reflexion fails on tasks needing high exploration diversity).

### 3e. Skill-library growth · 技能沉淀

| Method | Mechanism | Source |
|---|---|---|
| **Voyager** | Automatic curriculum + ever-growing **skill library** of verified executable code + iterative prompting with self-verification | arXiv:2305.16291 [9] |

**Design lesson (M5,M6).** A **verified, retrievable skill library** compounds capability and mitigates catastrophic forgetting — the procedural-memory counterpart to episodic memory (§4).

---

## 4. Memory & persistence · 记忆与持久化

Evolution needs somewhere for experience to *live*. Memory systems differ along extraction / management / storage / retrieval (see arXiv:2604.01707 [27]).

| System | Distinguishing idea | Source |
|---|---|---|
| **MemGPT / Letta** | OS-style tiered memory (core/archival/recall) paged by the LLM via function calls | arXiv:2310.08560 [28] |
| **Mem0** | Extraction + conflict detection + hybrid vector/graph store; 3-scope hierarchy | arXiv:2504.19413 [19] |
| **Zep / Graphiti** | Bitemporal knowledge graph (event time + ingestion time) over Neo4j | arXiv:2501.13956 [20] |
| **A-MEM** | Agentic memory objects with associative links; schema-aware routing | (Xu et al. 2025) [18] |

> **Pattern (M2,M4).** Persist knowledge **outside** the context window; keep provenance and time on every memory (bitemporal flags let you supersede without losing the audit trail); and treat **stale/poisoned memory** as a first-class threat (§8).

---

## 5. Skills ecosystems & protocols · 技能生态与协议

| Thing | Idea | Source |
|---|---|---|
| **Anthropic Agent Skills** | A skill = directory with `SKILL.md` (YAML `name`+`description`); **progressive disclosure**: metadata always loaded, body on trigger, bundled files/scripts on demand | Anthropic docs + engineering post [24],[25] |
| **Agent Skills (open standard)** | The vendor-neutral generalization: a folder with `SKILL.md` (`name` ≤64 chars, lowercase-hyphen; `description` ≤1024 chars), Discovery → Activation → Execution; shared by ~50 client harnesses | `agentskills.io/specification` [30] |
| **Model Context Protocol (MCP)** | Standard protocol for exposing tools/resources to agents | (widely adopted; see `core/07-tools-and-skills.md`) |

> **Pattern (M1,M6).** Metadata is the *index*; instructions are *procedural knowledge*; scripts are *executed, not read* (only output costs tokens). This is exactly OpenAI's `AGENTS.md`-as-map principle, generalized.

### 5a. Self-improving agent runtimes · 自我改进 agent 运行时

Turnkey runtimes that make "skills + memory as durable, **portable** state" concrete — the closest peers to Hermes, and the integration surface for this repo (see `tasks/ASSESSMENT.md` §B).

| Runtime | Mechanism in one line | Portable skills | Source |
|---|---|---|---|
| **Hermes Agent** (Nous Research, MIT) | Self-improving personal agent: agent-curated memory, autonomous skill creation, multi-platform gateway | ✅ `SKILL.md` | [31] |
| **OpenClaw** | Local, open-source personal assistant; messaging-channel gateway + skills | ✅ | [32] |
| **Goose** (Block) | Extensible local agent (code + research/writing/automation); MCP client | ✅ | [33] |
| **OpenHands** | Open platform for cloud coding agents; sandboxed runtime | ✅ | [34] |
| **Letta / Letta Code** | Stateful agents: git-backed memory that learns and self-improves | ✅ | [35] |
| **hermit** (benschrauwen) | File-first runtime for self-improving autonomous apps: heartbeat daemon, telemetry, strategic review, git checkpoints, sandbox | — | [36] |
| **hermit** (cashapp) | Hermetic per-project toolchains; ships an AI-coding-agent skill | ✅ | [37] |

> **Integration (M5,M6,M7).** Two capabilities were added to absorb these patterns: **`portable-skills`** (emit every harness skill in the Agent Skills `SKILL.md` format, so it loads in any of the ~50 client harnesses) and **`sandboxed-execution`** (declare an execution backend + least-privilege posture for anything that executes code or touches the world). Hermit's *file-first + heartbeat + sandbox* pattern informs the M2/M5 runtime hooks (`gate`/`harvest`).

---

## 6. Evaluation harnesses · 评测 harness

You cannot evolve without a scorer. Common benches referenced across §3: **SWE-bench Verified / Polyglot** (coding agents: SICA, DGM), **Terminal-Bench**, **ARC-AGI / ARC-AGI-3** (skill-acquisition efficiency), **LiveCodeBench** (competitive coding), **LoCoMo / LongMemEval / MemoryArena** (memory). Chollet: measure **efficiency**, not just success.

---

## 7. Surveys (orientation) · 综述导航

| Survey | Question it organizes | Source |
|---|---|---|
| **Self-Evolving Agents: What/When/How/Where** | Components (model/memory/tools/architecture) × timing × signal | arXiv:2507.21046 (TMLR 2026) [14] |
| **Co-Evolution in Agentic Systems** | Agent–agent, agent–environment, and meta co-evolution | arXiv:2608.10299 [15] |
| **Self-Improvements in Modern Agentic Systems** | Update target (θ vs scaffold) × driving signal | arXiv:2607.13104 [16] |
| **Agentic RL for LLMs** | POMDP framing; planning/tool/memory/reasoning/self-improvement | arXiv:2509.02547 [17] |
| **Memory in the Age of AI Agents** | Forms × functions × dynamics | arXiv:2512.13564 [18] |
| **From Storage to Experience** | Storage → reflection → experience evolution | ACL Findings 2026 [26] |
| **Self-play in RL** | Iterated policies vs. historical/current selves | arXiv:2408.01072 [23] |

---

## 8. Safety of self-evolution · 自我演化的安全

When "experience becomes reusable state, past events become future causes."

- **SAVER** (arXiv:2610.00093 [21]) — transition-centered framework `Substrate × Adaptation → Violation → Exposure → Response`. Key claim: failures need **not** start from harmful info; legitimate state becomes unsafe when adaptation widens its **persistence, authority, or scope** beyond the conditions under which it was valid. Governance must be **longitudinal** (trace to the originating transition, contain at the exposure surface, prevent re-emergence).
- **Misevolution** (arXiv:2509.26354 [22]) — empirical: memory evolution decays refusal (−45% on a Qwen3-Coder agent); tool evolution creates/reuses vulnerable tools (unsafe rate ~65.5%) and fails to reject malicious external tools (~93%).

> **Pattern (M0,M5,M8).** Every self-evolution loop needs: an **admission gate** on what may become durable state, **provenance + authority + scope** on each state, a **containment/revocation** path, and **human-gated** promotion for the highest-authority carriers (workflow rules, tool defs, weights).

---

## Cross-cutting map to `core/` · 与核心模块的映射

| Harness class | Primary core modules |
|---|---|
| Coding harnesses (§1) | M1 context, M6 tools, M7 governance |
| Orchestration (§2) | M6, M7, M8 |
| Self-evolution (§3) | **M5** (engine), M3 (verification), M7 (governance) |
| Memory (§4) | M2 (externalized memory), M4 (provenance) |
| Skills/protocols (§5) | M1, M6 |
| Evaluation (§6) | M3 |
| Safety (§8) | M0, M5, M8 |

---

## References · 参考文献（IEEE，访问日期 2026-10-12）

[1] M. Robeyns, M. Szummer, and L. Aitchison, "A Self-Improving Coding Agent," arXiv:2504.15228, May 2025. Code: https://github.com/MaximeRobeyns/self_improving_coding_agent
[2] S. Hu, C. Lu, and J. Clune, "Automated Design of Agentic Systems," arXiv:2408.08435, Aug. 2024 (ICLR 2025). Code: https://github.com/ShengranHu/ADAS
[3] X. Yin, X. Wang, L. Pan, L. Lin, X. Wan, and W. Y. Wang, "Gödel Agent: A Self-Referential Agent Framework for Recursively Self-Improvement," in *Proc. ACL*, 2025, pp. 27890–27913. DOI: 10.18653/v1/2025.acl-long.1354. arXiv:2410.04444
[4] J. Zhang, S. Hu, C. Lu, R. Lange, and J. Clune, "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents," arXiv:2505.22954, May 2025. Code: https://github.com/jennyzzt/dgm
[5] A. Zweiger, J. Pari, H. Guo, E. Akyürek, Y. Kim, and P. Agrawal, "Self-Adapting Language Models," arXiv:2506.10943, Jun. 2025 (NeurIPS 2025).
[6] W. Yuan, R. Y. Pang, K. Cho, X. Li, S. Sukhbaatar, J. Xu, and J. Weston, "Self-Rewarding Language Models," arXiv:2401.10020, Jan. 2024.
[7] A. Madaan *et al.*, "Self-Refine: Iterative Refinement with Self-Feedback," arXiv:2303.17651, Mar. 2023 (NeurIPS 2023).
[8] N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and S. Yao, "Reflexion: Language Agents with Verbal Reinforcement Learning," arXiv:2303.11366, Mar. 2023 (NeurIPS 2023).
[9] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar, "Voyager: An Open-Ended Embodied Agent with Large Language Models," arXiv:2305.16291, May 2023.
[10] B. Romera-Paredes *et al.*, "Mathematical discoveries from program search with large language models," *Nature*, vol. 624, no. 7992, pp. 545–552, 2023. Code: https://github.com/google-deepmind/funsearch
[11] A. Novikov *et al.*, "AlphaEvolve: A coding agent for scientific and algorithmic discovery," arXiv:2506.13131, Jun. 2025.
[12] A. Sharma, "OpenEvolve: an open-source evolutionary coding agent," 2025. https://github.com/algorithmicsuperintelligence/openevolve
[13] Inter-Co, "CodeEvolve: An open source evolutionary coding agent," arXiv:2510.14150, Oct. 2025. Code: https://github.com/inter-co/science-codeevolve
[14] H. Gao *et al.*, "A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to ASI," arXiv:2507.21046, Jul. 2025 (TMLR 2026).
[15] Q. Zong *et al.*, "Co-Evolution in Agentic Systems: Toward Self-Directed Evolution Beyond Human Design," arXiv:2608.10299, Aug. 2026.
[16] "Self-Improvements in Modern Agentic Systems: A Survey," arXiv:2607.13104, Jul. 2026.
[17] G. Zhang *et al.*, "The Landscape of Agentic Reinforcement Learning for LLMs: A Survey," arXiv:2509.02547, Sep. 2025.
[18] "Memory in the Age of AI Agents," arXiv:2512.13564, Dec. 2025.
[19] P. Chhikara *et al.*, "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory," arXiv:2504.19413, Apr. 2025.
[20] P. Rasmussen *et al.*, "Zep: A Temporal Knowledge Graph Architecture for Agent Memory," arXiv:2501.13956, Jan. 2025.
[21] J. Chen *et al.*, "Safety in Self-Evolving Agents: A Survey," arXiv:2610.00093, Sep./Oct. 2026.
[22] "Emergent Risks in Self-evolving LLM Agents" (Misevolution), arXiv:2509.26354, Sep. 2025.
[23] R. Zhang, Z. Xu, C. Ma, C. Yu, and W.-W. Tu, "A Survey on Self-play Methods in Reinforcement Learning," arXiv:2408.01072, Aug. 2024.
[24] Anthropic, "Agent Skills — Overview," Claude Platform Docs. https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview
[25] Anthropic, "Equipping agents for the real world with Agent Skills," Oct. 16, 2025. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
[26] "From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms," in *Findings of ACL*, 2026. https://aclanthology.org/2026.findings-acl.2069.pdf
[27] "Memory in the LLM Era: Modular Architectures and Strategies in a Unified Framework," arXiv:2604.01707, 2026.
[28] C. Packer *et al.*, "MemGPT: Towards LLMs as Operating Systems," arXiv:2310.08560, Oct. 2023.
[29] A. Jimenez *et al.*, "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?," arXiv:2310.06770, 2023.
[30] Agent Skills, "Specification," agentskills.io, accessed 2026-10-15. https://agentskills.io/specification
[31] Nous Research, "Hermes Agent," GitHub, accessed 2026-10-15. https://github.com/NousResearch/hermes-agent (MIT): https://hermes-agent.org
[32] OpenClaw, "OpenClaw," GitHub, accessed 2026-10-15. https://github.com/openclaw/openclaw
[33] Block, "goose — an open source, extensible AI agent," GitHub, accessed 2026-10-15. https://github.com/block/goose
[34] All Hands AI, "OpenHands," GitHub, accessed 2026-10-15. https://github.com/OpenHands/OpenHands
[35] Letta, "Letta — Platform for stateful agents," GitHub, accessed 2026-10-15. https://github.com/letta-ai/letta
[36] B. Schrauwen, "hermit — file-first runtime for self-improving autonomous apps," GitHub, accessed 2026-10-15. https://github.com/benschrauwen/hermit
[37] Cash App, "hermit — hermetic toolchains," GitHub, accessed 2026-10-15. https://github.com/cashapp/hermit

> **Pending-verification note.** The following were reported by an earlier research pass but were **not** independently re-verified here; do not cite as fact until checked: **Self-Harness** (reported arXiv:2606.09498), **STaR** (Zelikman et al.), **Constitutional AI** (Bai et al.), **Meta-Rewarding** (Wu et al.), **ARC-AGI-3 / ARC Prize 2025 IDs** (see `practitioner-playbook.md` note). MemGPT/Letta and SWE-bench IDs are well-established but were not re-fetched this session.
