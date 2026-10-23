# Workflow patterns 2026-10 — loop & graph engineering · 工作流模式（循环 / 图）

**Updated:** 2026-10-23 (§9 P20 addendum; §1–§8 as of 2026-10-18) · Companion to [`frontier-2026-10.md`](frontier-2026-10.md) (context · security · durability · spend · evals).

> **中文速览**
> 问题：本仓库的 22 条能力已覆盖「上下文预算 / 不可信内容 / 持久执行 / 成本上限 / 评测驱动」，但**工作流本身的结构**（agent 循环、图/状态机编排）没有对应能力，模块层也只在 M2 里零散提到「预算」「心跳」。本文按一手资料核验 2025–26 收敛结论后，**新增 2 条通用能力**（`loop-discipline`、`graph-orchestration`），在 M2/M8 补上对应的模块条款，并修正 `langgraph` 的模块映射（M6,M7 → M2,M6,M7,M8）。**未新增**：`routing`/`prompt-chaining`/`reflection-loop` 等（已被模块或既有能力覆盖，另立能力只会变成"文档"）。**使用者侧**：`.harness/capabilities.local.md` 与 `harness learn`/`cases`/`evolve` 是回流通道，但 `updates/` 目前只有 `standard.json`——**尚无案例可整合**，如实记录。

---

## 1 · The question · 问题

Two workflow families were unverified against this library's coverage:

1. **Loop engineering** — an agent is a loop over tools (think → act → observe → re-plan). What turns that loop from a hang into a mechanism: a stated **termination condition**, a **step/turn budget**, a **per-step ground-truth check**, **no-progress/stall detection**, and a readable trace.
2. **Graph engineering** — when work has branches or more than one worker: a **declared topology** (typed shared state, nodes, conditional edges, fan-out/fan-in, per-node checkpoints, resume/cancel) instead of an implicit prompt-driven flow.

Neither had a capability. `core/03` (M2) mentioned budgets, heartbeats and "an externalized state machine" in passing; nothing named the loop contract or the topology.

## 2 · Verified sources · 核验来源

New group **F** in [`references.md`](references.md) (`[R93]`–`[R97]`), all fetched 2026-10-18:

- **`[R93]` Anthropic, *Building effective agents*** — the canonical workflow taxonomy: **prompt chaining, routing, parallelization (sectioning / voting), orchestrator-workers, evaluator-optimizer**; and "agents … are typically just LLMs using tools based on environmental feedback **in a loop**", where "it's crucial … to gain **ground truth** at each step … to assess progress", with "**stopping conditions** (such as a maximum number of iterations) to maintain control".
- **`[R94]` ReAct** (arXiv:2210.03629) — the reason/act interleaving that *is* the agent loop.
- **`[R95]` Reflexion** (arXiv:2303.11366) — self-critique in an **episodic memory buffer** across trials (the evaluator-optimizer loop).
- **`[R96]` Google ADK docs** — template workflows (**sequential / loop / parallel**) are *superseded* in ADK 2.0 by **graph-based workflows** and **dynamic workflows**; the runtime adds **resume**, **cancel** and an **event loop**.
- **`[R97]` LangGraph persistence docs** — **checkpointers** (thread-scoped graph state: continuity, human-in-the-loop, time travel, fault tolerance) vs **stores** (long-term, cross-thread).

Convergence: the two 2024–2026 primary sources that define this space ([R93]) and the two stacks that ship it ([R96], [R97]) agree — declare the loop, declare the graph, and checkpoint both.

## 3 · Coverage matrix · 覆盖矩阵

| pattern | where it already lived | decision |
|---|---|---|
| Prompt chaining | M2.2 incremental + M3.1 define-done (module text) | covered — no capability (would be documentation) |
| Routing | — (implementation choice) | folded into `graph-orchestration` text, not a capability |
| Parallelization — sectioning / voting | M6 model selection, M8 role separation | covered by `graph-orchestration` (fan-out/fan-in) |
| Orchestrator-workers | `cross-field-crew` (M6, M8) | covered |
| Evaluator-optimizer | M3.7 refinement loop; catalog `reflexion`, `self-refine` | covered — no capability |
| ReAct loop | M2 + M6 tool feedback | **`loop-discipline`** (new) |
| Loop contract: termination · budget · per-step ground truth · stall detection · trace | M2.7 heartbeat, M2.8 budget (partial) | **gap → `loop-discipline` + M2.10** |
| Graph / state-machine topology · checkpointed nodes · resume/cancel | — (absent) | **gap → `graph-orchestration` + M2.11 + M8.10** |
| Checkpointing & persistence (thread vs cross-thread) | M2.3, M2.9 | covered (informs `durable-execution`) |
| Human-in-the-loop | `human-review-gate` | covered |
| Guardrails / sandbox | `high-stakes-guardrails`, `sandboxed-execution` | covered |
| Tool design / ACI (poka-yoke, absolute paths) | M6 | covered |
| Memory (short / long term) | `resumable-memory` | covered |
| Handoff / A2A | `cross-field-crew` + M8; A2A protocol deliberately not a capability (see `frontier-2026-10.md` §5) | unchanged |

## 4 · What changed · 本次改动

**Two generic capabilities** (data-only, `data/capabilities.json`; **22 → 24**):

| capability | modules | fires when | why it matters |
|---|---|---|---|
| `loop-discipline` | M2, M3, M6 | `tool_surface ∈ {read_write, external}` **or** `horizon ≥ multi_session` | names the loop contract: goal state, step budget, per-step ground truth, no-progress detection |
| `graph-orchestration` | M2, M8 | `collaboration = multi_agent` **or** `horizon ≥ multi_session` | names the topology: typed state, nodes/edges, fan-out/fan-in, per-node checkpoint, one owner per value |

**Module clauses** so the capabilities annotate real invariants (M0.4 — a capability must not invent substance):

- `core/03-long-running-agents.md` — new **M2.10 (loop contract)** and **M2.11 (declared control graph)** + checklist + two anti-patterns.
- `core/09-collaboration-and-sessions.md` — new **M8.10 (declare the topology)** + checklist line.

**Catalog correction:** `langgraph` `maps_to` was `M6, M7` while its own summary says "graph/state-machine orchestration **with checkpointing**". Fixed to `M2, M6, M7, M8` ([R97]).

## 5 · Deliberately not added · 有意未加

- **`routing`, `prompt-chaining`, `reflection-loop`** — each is already a module item (M2.2, M3.7) or a catalog entry; a capability would duplicate `eval-driven-development` and fire everywhere. The rule from `frontier-2026-10.md` §5 still holds: a capability that never discriminates is documentation, not a mechanism.
- **A graph *execution engine*** (BSP/superstep scheduling, breadth-first vs depth-first) — an implementation detail of a framework, not a harness requirement for its *user* (same reasoning that kept A2A out).
- **`domain`-scoped workflow capabilities** — the audit found none with a *discriminating* feature-vector trigger that M0–M8 plus the 25 domain workflows do not already carry; domain requirements stay in `domains/<id>/README.md` (M0.5).

## 6 · Consumer side · 使用者侧（"is anything integrable from users?"）

Checked the three places a consumer could contribute a capability; **currently empty, reported honestly**:

| channel | what it would produce | status today |
|---|---|---|
| `.harness/capabilities.local.md` (emitted, append-only) | task-local realisation + "distillation candidates" | template exists; a candidate needs **≥2 independent tasks** before it may become a proposal |
| `harness learn` → `updates/cases.jsonl`, `harness evolve` → `missing_capability` proposals | a recurring project capability → human-gated proposal | **no cases recorded yet** (`updates/` holds only `standard.json`) |
| `harness profile` project capabilities (`has-tests`, `has-ci`, `has-docs`, `packaged`, `typed`, `containerized`, `agent-ready`, `has-cli`) | evidence about the *target repo* | **different namespace** — deliberately **not** merged into the harness capability SSOT |

So there is nothing harvested from consumers to integrate at this stage; the channel (profile → learn → cases → evolve, human-gated) is in place and is the correct place for it to arrive.

## 7 · Verification status · 核验状态

- **Verified this session (2026-10-18):** `[R93]` (full page text), `[R94]`, `[R95]` (arXiv abstract pages), `[R96]` (ADK docs page), `[R97]` (LangGraph persistence docs).
- **Derived, not claimed as fact:** the claim that ADK 2.0 *supersedes* template workflows is quoted from the ADK docs page itself, not independently re-tested.
- Regenerate and re-verify: `PYTHONPATH=src python -m harness_factory capabilities --write` (also `map --write`, `catalog --write`).

## 8 · Next-cycle cues · 下轮线索

- Probe **OpenAI, *A practical guide to building agents*** (manager vs decentralized multi-agent, guardrails) and **Strands / Rivet / Vellum** as further topology sources.
- Re-probe **ADK dynamic workflows** and whether a *dynamic* (model-refers-to-refers) topology needs vocabulary beyond `graph-orchestration`.
- Watch **agent-graph observability** (`[R91]` OTel GenAI conventions, still *Development*) — a span tree per node is what makes a declared graph auditable.
- Consider emitting a **loop-contract stanza** in `templates/` (goal state · budget · ground-truth check · stall rule) so `harness init` states it by default.

## 9 · P20 addendum (2026-10-23) · MCP 2026-07-28 core revision digested · MCP 核心修订消化

> 中文：MCP **2026-07-28 规范正式版**（`[R244]`，博客全文已读）改变了本库两条能力所注解的基座，但**不改任何不变量**——协议从传输侧重新确认了它们。四个映射：**MRTR**（服务端返回 `input_required`、客户端带答案重试）= 把「中途要人确认」协议化为记录状态（M8 人类门 + M0.7）；**Tasks 扩展** = `durable-execution` 的厂商收敛（AWS 贡献）；**列表缓存提示** `ttlMs`/`cacheScope` = 上下文预算从环境成本变成显式预算线（`context-budget-policy`）；**12 个月弃用窗口** = M7 变更治理的活样本。无新条款、无新能力；数据面改动：`harnesses.json` `mcp` 补 M2/M8 映射与摘要、`sources.json` 两条 `why` 改写、`capabilities.json` 四条 `why` 补溯源（R244/R245/R249/R237）。溯源与核验状态见 `references.md` §W 与 `data/cycles.json` P20。

- **MRTR is the protocolized human gate (M8).** The server answers `resultType:"input_required"` and the client *retries* with `inputResponses` — held-open streams (elicitation/create, sampling/createMessage, roots/list) are replaced. Approval mid-call becomes recorded state carried by a request, not a connection held open: the durable-execution rule "human approval is recorded state" (M0.3/M0.7), now at the transport layer.
- **Tasks extension = convergence on `durable-execution`.** `io.modelcontextprotocol/tasks` (contributed by AWS): long-running work as an addressable resource — poll `tasks/get`, update `tasks/update`. The capability predates the protocol; the protocol is confirmation, not a new requirement.
- **List-cache hints are a context-budget line.** List responses gain `ttlMs`/`cacheScope` + deterministic ordering: refresh cost of tool lists becomes explicit and policy-able, instead of ambient. Annotated on `context-budget-policy`.
- **A 12-month minimum deprecation window is an M7 exemplar.** Roots/Sampling/Logging and HTTP+SSE are deprecated with a *dated, bounded* migration window — deprecate → announce → window → remove, run by the spec itself. Cite as the change-governance exemplar (M7) next to the repo's own rounds.
- **Stateless core is transport, not harness.** `initialize`/session and `Mcp-Session-Id` retired; per-request self-describing calls + `server/discover`. Effect on a harness: fewer session states to journal and fewer held-open failure modes — recorded for completeness; no clause changes because of it.
- **Not a duplication of M3.16:** R244 changes the *substrate*; the disclosure clause (R243) governs *comparisons*. Both landed the same round via different outlets — see [`harness-disclosure-2026-10.md`](harness-disclosure-2026-10.md).
