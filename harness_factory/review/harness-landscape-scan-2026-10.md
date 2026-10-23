# Harness landscape scan · 2026-10-23 — what moved since the last assimilation, and what a next round (P18) could carry

**Updated:** 2026-10-23 · **Status:** research findings + **upgrade proposal only** (no SSOT edited; human-gated per M0.4/M0.8) · **Scope:** agent-harness research & practice across the web, diffed against this factory as of R242 / 12 cycles / 37 capabilities (2026-10-20).

> 中文速览：这是 P17 收尾（2026-10-20）之后的一次**全网扫描轮（observe 半环）**。方法：一手来源抓取 → 与本库 R1–R242 语料和 `data/*.json` 做覆盖差集 → 按判别性四判据评估是否值得开一轮 **P18**。
> **三个已被一手核验的新增量**：① **arXiv:2605.23950《Stop Comparing LLM Agents Without Disclosing the Harness》**——把「harness 比模型更能决定长时程表现」形式化为 Binding Constraint Thesis，并给出**披露标准 + 方差分解协议**；这是本库立场的学界表述，现有语料**未收录**。② **MCP 2026-07-28 规范正式版**——无状态核心、MRTR（服务端中途要人确认的回合式请求）、Tasks 扩展（长任务）、缓存化 list、授权加固、12 个月弃用窗口；本库只收过其安全页（R87），**核心变化未消化**。③ **OWASP AST10 v1.0 已发布**——恰是 `frontier-2026-10.md` §6b 挂名的回访触发器，**触发条件已成立**。
> 另有 5 组*listed（未深读）*信号（Claude Code Agent Teams、METR 1.1/105 天翻倍、长时程基准群、A2A 进 Linux Foundation、Anthropic context editing/memory tool）。
> **评估结论：可以升级，且值得** —— 建议 P18 四个切片（见 §4），全部 data-only 或「子句+评审」级，不动引擎代码；其中披露判据与 AST10 两项通过四判据，其余按记录留档。任何落地改动**等用户确认后**再执行。

---

## 1 · Method · 方法

Follows the `frontier-2026-10.md` §1 pipeline (observe → audit coverage → propose; the apply half stays human-directed):

```
probe (websearch, 2026-10-23) → fetch primary → diff vs R1–R242 + data/*.json coverage
    → grade against the discriminating test (integration-map §0) → proposal slices (this doc)
```

- Secondary roundups (winder.ai, cellcog, northflank, stacklok comparisons) were read **for orientation only** and are not cited — the no-laundering rule.
- Every claim below carries its source and status: **fetched** = full text or abstract read on the access date; **listed** = surfaced by search / metadata only, not deep-read.

## 2 · What moved · 本轮观察面

### 2a · Fetched and verified (primary)

| # | Signal | What it says | Access |
|---|---|---|---|
| S1 | **Harness disclosure** — Y. Zhang et al., *"Stop Comparing LLM Agents Without Disclosing the Harness"*, arXiv:2605.23950 (cs.AI/cs.SE), submitted 2026-05-07 ([abs](https://arxiv.org/abs/2605.23950)) | Position paper; **Binding Constraint Thesis**: for long-horizon tasks across frontier-comparable models, the harness (context construction, tool interaction, orchestration, verification) governs performance variance more than the model; supports via (i) control-theoretic formalization (harness = controller, LLM = stochastic policy), (ii) published benchmarks + a controlled variance decomposition showing **model-ranking reversals**, (iii) a proposed **harness-aware evaluation framework** with a disclosure standard and variance-decomposition protocol. Verdict: undisclosed-harness leaderboards are "incomplete and potentially misleading". | abstract read 2026-10-23 |
| S2 | **MCP 2026-07-28 specification** (GA) — official blog ([post](https://blog.modelcontextprotocol.io/posts/2026-07-28/)) | Stateless protocol core (initialize/session retired; per-request self-describing + `server/discover`); **MRTR** replaces held-open streams — server returns `resultType:"input_required"`, client retries with answers (elicitation/sampling); `Mcp-Method`/`Mcp-Name` headers for gateway routing/authorization; list responses gain `ttlMs`/`cacheScope` + deterministic order; **extensions framework** formalized (Tasks — long-running work, contributed by AWS; MCP Apps; Enterprise Managed Authorization); auth hardening (RFC 9207 `iss` validation; DCR → CIMD); Roots/Sampling/Logging + HTTP+SSE deprecated with a **12-month minimum window**. Tier-1 SDKs (TS/Py/Go/C#) ship day-zero. Ecosystem: Bedrock AgentCore, Cloudflare Agents SDK, Microsoft Foundry, Google Cloud quote support. | full post read 2026-10-23 |
| S3 | **OWASP Agentic Skills Top 10 (AST10) v1.0** — project page ([owasp.org](https://owasp.org/projects/agentic-skills-top-10), [repo](https://github.com/OWASP/www-project-agentic-skills-top-10)) | "First comprehensive security framework for AI agent **skills**" — the behavior layer between LLM and MCP tool transport; 10 critical risks across major platforms (SKILL.md / skill.json / cursor rules formats), each **mapped to CSA MAESTRO 7-layer**; evidence-based mitigations. Incubator status; 23 contributors. Mental model quoted: *"MCP = how the model talks to tools; AST10 = what those tools actually do."* | page read 2026-10-23 |

### 2b · Listed, not deep-read (directional; verify before citing as fact)

| # | Signal | Source | Relevance |
|---|---|---|---|
| L1 | **Claude Code Agent Teams** — orchestration of multiple parallel Claude Code sessions (distinct architecture from subagents; shared agent panel; `SubagentStop` hooks; nesting to depth 5 reported by practitioners) | [official docs](https://code.claude.com/docs/en/agent-teams) | M8 / `graph-orchestration` / `cross-field-crew`: vendor convergence on *peer multi-session* coordination, not just parent→child |
| L2 | **METR time horizons 1.1** (Jan 2026, larger task suite) + live dashboard; doubling fit ≈ **105 days** through Feb 2026 data (2024-onward fit; longer-window fit ≈129 d) | [metr.org/time-horizons](https://metr.org/time-horizons/) (page dated 2026-09-08) | refreshes the grounding of `durable-execution` and `long-horizon-autonomy-control` (R89 cites the 2025 paper, not 1.1) |
| L3 | **Long-horizon agent benchmarks cluster**: Long-Horizon Terminal-Bench (46 tasks, hundreds of steps, **hidden fake-proof verifiers**); PolyWorkBench (arXiv:2607.06008, multilingual long-horizon, **same inputs/timeout across harnesses** — an executed controlled harness comparison); AgentIF-OneDay (arXiv:2608.05013, 104 tasks/767 scoring points); a real-world long-horizon benchmark (arXiv:2605.10912, cited 35×) | [LHTB page](https://zli12321.github.io/LHTB/) + arXiv | anti-gaming graders + harness-controlled comparison = instruments for `eval-driven-development`, corroborating S1 |
| L4 | **A2A under Linux Foundation**: 150+ supporting orgs, major cloud platforms, "first production-ready open standard" for agent interoperability (LF press, 2026-04-09) | [LF press](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) | frontier §5 deferred A2A as "covered as process"; production-standard handoff now warrants a re-look at M8 interop clauses |
| L5 | **Provider-side context management formalized**: Anthropic **context editing** + **memory tool** (client-side memory CRUD directory) on the Claude API/platform docs; tool discovery / dynamic execution ("advanced tool use", 2025-11-24) | [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing), [memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) | exactly the `frontier-2026-10` §6b cue "re-probe context editing / memory tooling as provider APIs stabilize"; candidate **parameters** for `context-budget-policy` + the P12 M2.12 memory-backend clause |

## 3 · Coverage diff · 与现有语料的差集

Checked against `review/references.md` (R1–R242), `data/capabilities.json` (37), `data/sources.json`, `data/harnesses.json` (196), `data/levers.json`, and the P7–P17 reviews:

| Item | Already carried | Genuine gap |
|---|---|---|
| S1 disclosure thesis | *adjacent only*: `component-ablation` (review P16), `eval-driven-development` (R92), harness-as-term defined in README | the paper itself is **absent from the corpus** (grep: no 2605.23950 / "disclosing the harness"); the **disclosure-standard / variance-decomposition** protocol is not an executable clause — today the factory *emits* a manifest but nothing requires a *comparison artifact* to disclose both harnesses |
| S2 MCP core changes | R87 = MCP **security best practices** page (2026-07-28 docs line); sources.json tracks MCP as vendor harness | the **spec revision itself** (stateless core, MRTR, Tasks, extensions framework, header routing, deprecation policy) is unassimilated; MRTR natively encodes *mid-call human confirmation* → touches M8 escalation; Tasks → `durable-execution`; cache hints → `context-budget-policy`; 12-month deprecation window → a **change-governance exemplar** (M7) |
| S3 AST10 | `frontier-2026-10` §6b **watch item** (recorded revisit trigger); `portable-skills` capability + M6 emit SKILL.md | the trigger has **fired** — AST10 v1.0 now exists; `data/levers.json` has no skills-security lever pointing at it; `untrusted-content-discipline` does not yet cite the *skills execution layer* |
| L1 agent teams | `graph-orchestration` (M2/M8), harnesses.json role-based multi-agent entries | Claude Code **Agent Teams** as a distinct coordination topology (peer sessions, not parent-child) is not in the vendor catalog |
| L2 METR 1.1 | R89 (2025 paper, 50% horizon trend) | the 1.1 release + 105-day doubling (as of 2026-09) is a **figure refresh**, and the figures are directional → cite the live page + date |
| L3 benchmark cluster | GAIA/BrowseComp/HLE tracked as eval tools; hidden-verifier idea echoes M3 anti-gaming | LHTB / PolyWorkBench / AgentIF-OneDay not registered; PolyWorkBench's fixed-input protocol is a **working instance** of S1's variance decomposition |
| L4 A2A/LF | tracked in sources.json as vendor harness; §5 deferral recorded | status change (LF production standard, 150+ orgs) not reflected; §5's reason ("covered as process") may now under-serve interop handoffs |
| L5 context editing/memory | `context-budget-policy` capability (principle level); M2.12 memory-backend clause (P12) | the **API-level mechanisms** are exactly what §6b said could beat prose — candidate refs/params, not a new capability |

**Already well covered (no action):** durable-execution practice posts (R90 stands), Agent Skills open standard (P1 conformance + `agentskills.io` verified 2026-10-15; ~50 clients noted in P2/B review), lethal trifecta, CaMeL, budget caps, model-ranking-reversal *instances* (P16 ablation read the Distilling/SHarP papers directly — S1 generalizes what P16 practiced).

## 4 · Upgrade evaluation · 升级评估（P18 提案，待确认）

**Verdict: yes — one round is justified, but a bounded one.** The three fetched signals are not "news noise": S1 gives the factory's *own thesis* an external, citable formalization with a protocol the factory can operationalize; S2 changes the substrate two existing capabilities annotate; S3 closes a **recorded** revisit trigger. Applying the four-part discriminating test (`integration-map` §0):

| Slice | Kind | What lands | Passes the test because |
|---|---|---|---|
| **P18.1 · Harness disclosure assimilated** — S1 (+L3 as corroboration) | review + clause + data | new review note absorbing §2a-S1; a proposed clause **M3.16 "a comparison discloses its harness"** (any claim comparing agents across models/harnesses must attach or cite both harness configurations + a variance statement, else mark *incomplete*); crosswalk row vs `component-ablation` / `eval-driven-development`; refs R243–R246 | fires distinctly (only on comparative claims — not every task); maps to a real M3 clause; traceable (fetched); not a duplicate (ablation *removes* components on one harness; disclosure *names* harnesses across comparisons) |
| **P18.2 · AST10 revisit closes** — S3 | data-only | skills lever in `data/levers.json` → AST10; `untrusted-content-discipline` / `portable-skills` provenance rows gain the AST10 citation; frontier §6b cue marked done in `cycles.json` roadmap | the round mechanism *exists for this*: a recorded `revisit_when` fired; a harness that emits `SKILL.md` files must track the security framework *for that format* |
| **P18.3 · MCP 2026-07-28 core digested** — S2 | review + data | sources.json/harnesses.json refresh entries + dated receipts; short § in `review/workflow-patterns-2026-10.md` (or frontier companion): MRTR = protocolized human gate (M8), Tasks extension = vendor convergence on `durable-execution`, cache hints → context budget, **12-month deprecation window = M7 exemplar**; refs R247–R248 | two existing capabilities annotate a substrate that just changed materially; not updating is drift, and each mapping names a *different* face |
| **P18.4 · Figure & status refresh (small)** — L1/L2/L4/L5 | data-only | METR 1.1 + 105 d (marked *directional, as of 2026-09*); Claude Code Agent Teams catalogued as a coordination topology (feeds `graph-orchestration` exemplars); A2A LF status line; context editing + memory tool registered as `context-budget-policy` **reference parameters** (no new capability) | keeps `sources.json` honest ("dates explicit"); the L5 item is a fired §6b cue answered as *parameter*, matching the cue's own wording |

**Deliberate non-additions (pre-recorded):**
- **No `harness-disclosure` capability** — it keys on *claim type* (comparative), not on the feature vector; adding it would fire on nearly nothing or need a new axis → carried by clause M3.16 instead (same logic as `methodology-fit`, integration-map §2).
- **No `memory-api` capability** for L5 — provider-specific mechanism; belongs as refs/params under `context-budget-policy` + M2.12, per the §6b cue itself.
- **No new agent-team capability** — `graph-orchestration` + `cross-field-crew` already annotate M8; L1 is a catalog/exemplar update. If A2A+teams converge further, re-audit *after* full-text reads, not from snippets.
- **P18 ≠ the trace-driven self-evolution round** — that remains the largest recorded gap (ASSESSMENT A.3 #2) and deserves its own round with a design doc first; folding it in would violate one-round-one-`added`-block (M5.10).

**Cost & reversibility:** all four slices are `data/*` + `review/*` + one `core/04` clause + generated-view regeneration (`catalog/capabilities/map --write`) + guard tests; **no engine code changes**; every slice is a separate revertible commit. Tests 242 → est. ~250 (M3.16 checklist + ref-continuity guards).

## 5 · What would change my mind · 推翻条件

- If a full-text read of arXiv:2605.23950 shows the "disclosure standard" is only a reporting checklist already subsumed by `.harness/manifest.json` semantics, P18.1 shrinks to a refs + crosswalk row (still worth it as external validation of the factory's stance). *(Abstract read; full PDF not yet downloaded — deep-read is step 1 of the slice.)*
- If AST10's ten risks all map 1:1 onto existing OWASP ASI01–ASI10 items already ingested (R86), P18.2 shrinks to a single provenance line. *(Project page read; the ten entries themselves not yet read.)*
- If the MCP changelog turns out to be transport-only with no harness-layer semantics, P18.3 is data-only. *(Blog read in full; SEP-level detail not yet.)*

## 6 · Provenance & verification status · 核验状态

- **Fetched (2026-10-23):** arXiv:2605.23950 abstract (full PDF *not* read — marked); MCP 2026-07-28 official blog post (full); OWASP AST10 project page (full; the AST10 list document itself *not* read).
- **Listed (search-surfaced, not deep-read):** code.claude.com agent-teams docs · metr.org/time-horizons page · LHTB project page · arXiv:2607.06008 / 2608.05013 / 2605.10912 · LF A2A press release · platform.claude.com context-editing & memory-tool docs · openai.com AgentKit page. All marked *listed*; none used as a load-bearing fact.
- **Secondary (orientation only, uncited):** winder.ai / cellcog / northflank / stacklok / explainx harness comparisons; totalum/taskade blogs.
- **`[unverified]`:** nothing above is asserted beyond its status; the 105-day doubling figure is attributed to METR's own fit *as reported via secondary post* → treat as directional until read at metr.org directly.
- Proposed new reference ids **R243–R248** continue the existing numbering (R1–R242); actual insertion into `references.md`/`.bib` happens only when a slice is applied.

## See also · 参见

- [`frontier-2026-10.md`](frontier-2026-10.md) — last assimilation + the §6b cues this scan closes/keeps.
- [`integration-map-2026-10.md`](integration-map-2026-10.md) §0 — the discriminating test every slice above is graded against.
- [`harness-ablation-2026-10.md`](harness-ablation-2026-10.md) — P16's internal ablation practice, of which S1 is the external generalization.
- [`../tasks/PLAN.md`](../tasks/PLAN.md) — P17 status; P18 would open here on confirmation, registered in `data/cycles.json` with its own DoD (M5.10).
