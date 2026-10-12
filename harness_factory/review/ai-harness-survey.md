# A Survey of AI Agent Harnesses and Self-Evolution Methods · AI agent harness 与自我演化方法综述

> A narrative review of how agent harnesses are built, classified, and made to improve themselves — with a focus on self-evolution and its safety.
> 对 agent harness 的构建、分类与自我改进的叙述性综述——侧重自我演化及其安全。
> Companion to `harness-catalog.md` (exhaustive listing). **Updated:** 2026-10-12.

---

## 中文速览

**这份综述做什么。** 定义「harness」这一层，给出七族分类法，重点分析**自我演化**：它改什么（脚手架 vs 权重）、动力信号从哪来、是否自指、是否开放结局；讨论记忆作为演化的基底、技能生态与协议、评测 harness，以及自我演化的**安全**（SAVER、误演化）；最后列出开放问题。**全量清单与逐条引用见 `harness-catalog.md`；合并参考文献见 `references.md`。**

**一句话结论。** 模型的智能是给定的；**harness 决定它能否可靠工作并持续变好**。而「持续变好」的难点不在能力，而在**治理**：准入、溯源、权限、范围、遏制、人类门——否则系统会**误演化**，把目标漂移与安全退化当作进步。

---

## 1. Introduction & scope · 引言与范围

The last decade moved from *models* to *systems*: an LLM alone produces text, but an **agent** acts — it plans, calls tools, reads files, and iterates. The layer that turns a model into a reliable worker is the **harness**. This survey organizes the field along two axes: (i) the **families** of harnesses that exist today, and (ii) the **self-evolution** methods that let a harness or agent improve over time. Section 2 defines the term; §3–§5 survey static harnesses; §6–§10 analyze self-evolution, memory, skills, evaluation, and safety; §11 lists open problems.

## 2. What is a harness? · 什么是 harness

A useful decomposition (Mollick; Böckeler/Fowler):

> **model** (capability) → **app** (interface) → **harness** (tools + workflow + context management) → **agent** (the harness running in a loop)

The adopting formulation is **"Agent = Model + Harness."** The harness supplies *feedforward* guides (specs, schemas, examples) and *feedback* sensors (tests, linters, gates) [P19, P20]. Empirically the harness often matters *more* than the model for real productivity — a claim echoed across the practitioner literature [P29, P30]. Karpathy's "Software 3.0" frames the context window itself as the programming substrate [P1–P4].

## 3. Classification · 分类总览

Seven families (detailed in the catalog):

1. **Coding / software harnesses** — turn an LLM into a repo agent (e.g. Claude Code, Codex-style agents, `Aider`, `OpenHands`, `SWE-agent`).
2. **Orchestration frameworks / agent SDKs** — LangGraph, AutoGen, CrewAI, OpenAI Agents SDK, and peers.
3. **Self-evolution methods** — scaffold search, evolutionary code search, weight self-adaptation, inference-time self-correction, skill-library growth (§6).
4. **Memory & persistence** — MemGPT/Letta, Mem0, Zep; the substrate that lets experience *persist* (§7).
5. **Skills ecosystems & protocols** — `AGENTS.md`, Anthropic **Agent Skills**, MCP (§8).
6. **Evaluation harnesses** — SWE-bench (Verified/Polyglot), Terminal-Bench, ARC-AGI, LiveCodeBench, LoCoMo/LongMemEval (§9).
7. **Surveys** — orientation maps of the field (§11; catalog §7).

## 4. Coding harnesses · 编码 harness

Coding is the field's proving ground because its outputs are **cheap to verify** (tests pass/fail), which the "verifiability spectrum" identifies as the precondition for fast agent improvement [P1]. Coding harnesses share a shape: a **loop** over (read → plan → edit → run → observe), a **minimal toolset** (shell, editor, test runner), and **context management** (search, maps, compaction). Two design tensions recur: *autonomy level* (autocomplete → single edit → whole repo) and *context strategy* (reset vs compaction vs subagents) [P2, P26].

## 5. Orchestration frameworks · 编排框架

Orchestration frameworks supply graph/state-machine execution, role abstraction (planner/worker/critic), and tool plumbing. They are mostly **static**: the graph is authored by humans. The self-evolution literature (§6) is largely a reaction to this — asking whether the *orchestration itself* can be discovered rather than hand-written.

## 6. Self-evolution: a four-axis analysis · 自我演化的四个轴

We can place every self-evolution method on four axes.

**(a) What is updated — scaffold vs. weights.** Scaffold/prompt/tool updates are cheap, interpretable, and reversible; weight updates are powerful but costly and harder to govern. Most 2023–2025 work operates on the scaffold; **SEAL** is the notable weight-level case, having the model generate its own finetuning data and update directives (*self-edits*) reinforced by downstream task success [S5].

**(b) Where the driving signal comes from.** Self-feedback (Self-Refine, Reflexion) [S7, S8], self-judging reward (Self-Rewarding LMs) [S6], an archive of past agents (ADAS, SICA, DGM) [S1–S4], or external evaluators (FunSearch, AlphaEvolve) [S10, S11].

**(c) Is it self-referential?** Meta-agent edits *other* agents (ADAS) [S2] versus the agent edits *itself*, including the update logic (Gödel Agent, SICA, DGM) [S1, S3, S4]. The latter is more general and more dangerous.

**(d) Is it open-ended?** Single best-so-far vs. an **archive of stepping stones** (DGM, AlphaEvolve's island/MAP-Elites populations) [S4, S11]. Open-ended evolution trades a single optimum for continuous discovery.

Concrete families: **scaffold/code self-modification** (ADAS, Gödel Agent, SICA, DGM); **evolutionary code search** (FunSearch, AlphaEvolve, OpenEvolve, CodeEvolve) [S10–S13]; **weight self-adaptation** (SEAL) [S5]; **inference-time self-correction** (Self-Refine, Reflexion) [S7, S8]; **skill-library growth** (Voyager) [S9].

## 7. Memory as the substrate of evolution · 记忆是演化的基底

Evolution requires somewhere for experience to *live*. Memory systems differ along extraction / management / storage / retrieval [M27]. Representative designs: **MemGPT/Letta** (OS-style tiered paging) [M28], **Mem0** (extraction + conflict detection + hybrid vector/graph store) [M19], **Zep/Graphiti** (bitemporal knowledge graph) [M20]. The survey field distinguishes **forms × functions × dynamics**, and stresses the shift *from storage to experience* [M18, M26]. In harness terms, memory is M2 (externalized state) + M4 (provenance) — without it, nothing can compound.

## 8. Skills ecosystems & protocols · 技能生态与协议

The emerging consensus is **progressive disclosure**: keep a small **index** in context (name, trigger, one-liner) and load a skill's **body** only when its trigger fires. Anthropic's **Agent Skills** — folders of `SKILL.md` plus scripts — instantiate this: metadata is the map, instructions are procedural knowledge, scripts are *executed, not read* [K24, K25]. `AGENTS.md` is the same idea for repo conventions. **MCP** standardizes tool access. This is M1 + M6, generalized.

## 9. Evaluation harnesses · 评测 harness

You cannot evolve without a scorer. Common benches: **SWE-bench Verified/Polyglot** (coding) [E29], **Terminal-Bench**, **ARC-AGI / ARC-AGI-3** (skill-acquisition **efficiency**, not just skill) [P12–P14], **LiveCodeBench**, and **LoCoMo/LongMemEval/MemoryArena** (memory). The design lesson from Chollet: measure *efficiency of skill acquisition*, or you optimize the wrong thing.

## 10. Safety of self-evolution · 自我演化的安全

When "experience becomes reusable state, past events become future causes," new risks appear. **SAVER** offers a transition-centered framework `Substrate × Adaptation → Violation → Exposure → Response`, with the key insight that failures need **not** start from harmful information: legitimate state becomes unsafe when adaptation widens its **persistence, authority, or scope** beyond the conditions under which it was valid. Governance must therefore be **longitudinal** — trace to the originating transition, contain at the exposure surface, prevent re-emergence [SA21]. Empirically, **misevolution** shows memory evolution decaying refusal (−45% on a Qwen3-Coder agent) and tool evolution creating/reusing vulnerable tools (unsafe rate ~65.5%) while failing to reject malicious external tools (~93%) [SA22].

> **Design rule.** Every self-evolution loop needs (i) an **admission gate** on what may become durable state, (ii) **provenance + authority + scope** on each such state, (iii) a **containment/revocation** path, and (iv) **human-gated** promotion for the highest-authority carriers (workflow rules, tool definitions, weights). This is `core/06-self-evolution.md` M5 + M0 + M8.

## 11. Surveys & open problems · 综述与开放问题

Orientation surveys organize the field along complementary cuts: **self-evolving agents** (components × timing) [SV14], **co-evolution** (agent–agent, agent–environment, meta) [SV15], **self-improvements** (update target × signal) [SV16], **agentic RL** [SV17], **memory** [SV18, M26], and **self-play** [SV23].

**Open problems.** (1) *Value attribution*: which scaffold change actually caused the gain? (2) *Generalization*: does an improvement transfer off the tuning distribution? (3) *Stable identity*: how do you evolve capability without drifting goals? (4) *Governance at scale*: longitudinal traceability of durable state. (5) *Evaluation of open-ended discovery*: how to score a system whose target moves. (6) *Cost governance*: when self-improvement is worth its compute.

## 12. Conclusion · 结论

The model is given; the **harness** determines whether capability becomes reliable work. Self-evolution is the frontier — and its hard problem is not capability but **governance**: admission, provenance, authority, scope, containment, and human gates. A harness that can learn from its failures *and* bound the blast radius of learning is the durable design.

---

## References · 参考文献

Full, per-item IEEE citations live in **`references.md`**; the exhaustive classified listing (with 29 references) is in **`harness-catalog.md` §References**. Bracketed labels above map as follows: `[P*]` → practitioner-playbook; `[S*]`/`[M*]`/`[E*]`/`[SA*]`/`[SV*]`/`[K*]` → catalog references 1–29. All access dates 2026-10-12.
