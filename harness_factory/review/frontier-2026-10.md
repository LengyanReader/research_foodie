# Frontier assimilation · 前沿整合（2026-10）

**Updated:** 2026-10-23 (§6b cue statuses closed by P20; §1–§6 body as of 2026-10-18) · **Status:** applied (data + docs only; human-directed) · **Scope:** agent harness — context, security, durability, spend, evals.

> What the leading labs, security bodies, and practitioners converged on **this cycle**, and
> which of it the capability system did not yet carry. Every claim traces to a primary
> source in [`references.md`](references.md) group **§E** (R84–R92); anything fetched is
> marked, anything only listed is marked *listed*.
> 本轮**顶级实验室 / 安全机构 / 实践者**的收敛点，以及能力系统里**尚未覆盖**的部分。
> 每条声明都可溯源到 `references.md` §E（R84–R92）；已抓取的标注抓取，仅收录的标注 listed。

---

## 中文速览

- **做法。** 先按观察—审计—提案的规矩（M0.4）抓一手材料：Anthropic 上下文工程、Chroma *Context Rot*、OWASP *Top 10 for Agentic Applications 2026*、MCP 安全最佳实践、CaMeL、Temporal *Durable AI*、METR 长任务时间视野、OpenTelemetry GenAI 语义约定、*Agent-as-a-Judge*。逐条核验抓取后，**只把真正缺的能力**写进 `data/capabilities.json`（SSOT），并 regenerate `CAPABILITIES.md`。
- **结论。** 现有 17 项能力**覆盖**了「生成—评估分离」「最小高信号上下文」「来源可溯」等原则，但**没有**独立承载五件前沿共识：**上下文预算**、**不可信内容纪律**、**持久执行**、**成本硬上限**、**评测驱动开发**。新增这 5 项（17 → **22**），均为 **data-only**（改 JSON，不改代码），触发器彼此不重叠。
- **诚实边界。** 这是**能力库**的扩展，不是新协议实现；评测/可观测性（OTel GenAI）**暂未**单列能力，理由见 §5。§E 中 R91（OTel 仓库）抓取超时，仅由一手检索确认 —— 标 *listed*。

---

## 1 · Method · 方法

The self-update loop (`harness refresh` / `evolve`) is **observe-only** (M0.4): it ranks and
proposes, it never authors catalog content. This pass is the *apply* half, human-directed:

```
probe (websearch) → fetch primary → assess coverage vs corpus → extend SSOT (data/*) → regenerate → test
```

- **Primary sources only.** arXiv abstract pages, official docs, standards bodies. Blog
  aggregators were read for orientation but never cited.
- **Coverage check first.** Each candidate idea was diffed against `review/*`,
  `core/*`, and the 17 existing capabilities before anything was added — the goal is a
  smaller, sharper system, not a longer one.
- **Reversible.** Data + generated doc + docs. `git revert` one commit undoes the slice.

## 2 · What the frontier converged on · 本轮收敛点

| Signal · 信号 | What is now settled · 现状 | Mapped capability | Source |
|---|---|---|---|
| Context is **not** uniform — recall degrades as input length grows | "Context rot" measured across 18 frontier models; haystack structure alone changes accuracy | `context-budget-policy` | `[R84]`, `[R52]` |
| Retrieved bytes are **data, not instructions** | Fence untrusted content; a policy layer (CaMeL) can keep untrusted data out of control flow | `untrusted-content-discipline` | `[R88]`, `[R86]`, `[R87]`, `[R42]` |
| Long work must survive **process death** | Journal + deterministic replay; checkpoints are state recovery, *not* exactly-once | `durable-execution` | `[R90]`, `[R89]` |
| Unattended loops **burn budget** | Hard caps ("cut this off and return errors"), not soft warning emails | `cost-budget-caps` | `[R85]` |
| Judge the **trajectory**, not just the output | Agentic evaluators give step-level feedback; agent runs are traced as spans | `eval-driven-development` | `[R92]`, `[R91]` |

## 3 · New capabilities · 新增能力（17 → 22, data-only）

Added to `src/harness_factory/data/capabilities.json`; `CAPABILITIES.md` regenerated.
`when` is the machine-checked trigger; `modules` are what it annotates (never enables — M0.4).

| capability | fires when | modules | grounded in |
|---|---|---|---|
| `context-budget-policy` | `horizon ≥ session` OR `tool_surface ∈ {read, read_write, external}` | M1, M2 | `[R84]` `[R52]` |
| `untrusted-content-discipline` | `tool_surface = external` OR `artifact ∈ {document, knowledge_base}` OR `grounding = required` | M4, M6, M7 | `[R88]` `[R86]` `[R87]` `[R42]` |
| `durable-execution` | `horizon ≥ multi_session` | M2, M3 | `[R90]` `[R89]` |
| `cost-budget-caps` | `tool_surface = external` OR `horizon ≥ multi_session` | M3, M7 | `[R85]` |
| `eval-driven-development` | `verifiability = high` OR `horizon ≥ multi_session` | M3, M5 | `[R92]` `[R91]` |

**Why these five and not others.** They are the only signals that (a) appeared in ≥2
independent leading sources, (b) the corpus did not already carry as a *capability*, and
(c) have a **distinct trigger** — no new row duplicates an existing one (see §5 for the
deliberate non-additions).

## 4 · Per-capability notes · 逐项说明

### `context-budget-policy`
The 2025–26 context-engineering thread (Anthropic `[R52]`) gained an empirical spine: Chroma's
*Context Rot* report `[R84]` shows accuracy falling as **only** input grows, with distractors
and even coherent haystack structure measurably degrading results. The harness implication is
not "bigger windows" but a **policy**: write durable facts outside the window (M2), then
select / compress / isolate per call, and compact **only** against a named, measured
constraint.

### `untrusted-content-discipline`
The lethal trifecta `[R42]` is now joined by institutional guidance and an architectural
defense. OWASP's *Top 10 for Agentic Applications for 2026* (`ASI01`–`ASI10`) `[R86]` routes
goal hijack, tool misuse, memory poisoning and rogue agents through one lens; the **MCP
Security Best Practices** spec `[R87]` makes confused-deputy, token passthrough and local
one-click installs concrete, testable failure modes; **CaMeL** `[R88]` shows a policy layer
can keep untrusted data out of control flow. The capability keeps the discipline minimal:
*one leg of the trifecta must be provably withheld*, with least authority at the call site.

### `durable-execution`
`resumable-memory` externalizes **knowledge**; this capability externalizes **execution
semantics**. Temporal's *Durable AI* `[R90]` is the clearest statement: a worker crash must
replay a journal to the last committed step, not re-run the day — and that is only
crash-*safe* if side effects are idempotent, because a checkpoint is not an exactly-once
guarantee. METR's time-horizon work `[R89]` supplies the reason this is now load-bearing
rather than theoretical: the 50%-completion horizon keeps extending.

### `cost-budget-caps`
Willison's Oct 3 2026 post `[R85]` — hard caps on pay-by-usage services, default-on, with a
prominent "remove the cap" opt-in — is the newest idea in this batch. It is small, sharp, and
actionable. The existing `sandboxed-execution` covers *what may run*; this covers **when it
must stop**, which nothing else did.

### `eval-driven-development`
*Agent-as-a-Judge* `[R92]` formalizes step-level feedback (an agentic evaluator beats
LLM-as-a-judge and matches human baselines). OpenTelemetry's GenAI semantic conventions
`[R91]` standardize how a run is traced (`invoke_agent → chat` → `execute_tool`), so the
evidence exists to grade a **trajectory**. The capability ties `M3` (verified done) to M5:
each recurring failure becomes a frozen golden case, and the judge is never the author.

## 5 · Deliberately not adopted · 暂不纳入（及理由）

| Candidate | Why held | Where it lives today |
|---|---|---|
| Non-human identity / agent credentials | Overlaps `sandboxed-execution` (least privilege) + `untrusted-content-discipline`; better as a *lever*, not a duplicate capability | least-privilege note in `data/levers.json`; OWASP Top 10 `[R86]` |
| Multi-agent / A2A handoff rules | Already covered as *process* | `cross-field-crew`, M8 |
| Provider-side redundancy/drift of the GenAI semantic conventions (OTel) | Spec still **Development**; the harness needs *trace-first* evidence, not a pinned schema | `[R91]`, noted |
| EU AI Act / GPAI-code compliance mapping | Regulatory, environment-specific; not a generic capability | a `domains/` concern, later |
| "Lethal trifecta" as its own capability | Superset already named here | `untrusted-content-discipline` |

> If run traces accumulate in `updates/` and are reused, the honest next step is a
> `run-observability` capability — **only then**, not speculatively.

## 5b · Deliberate non-match · 不匹配说明

`untrusted-content-discipline` fires on `grounding = required` but **not** on the default
`grounding = preferred`; a plain local coding task with `read_write` tools should not pay for
it. This is why it is not `always`: a capability that never discriminates is documentation,
not a mechanism.

## 6 · Verification status · 核验状态

- **Fetched and read (2026-10-18):** R84, R85, R86 (web page; the PDF was not downloaded),
  R87, R90 · R88, R89, R92 (arXiv abstracts).
- **Listed, not deep-read:** R91 (OTel GenAI repo) — the README fetch timed out; the repo,
  its creation date, and *Development* status were confirmed from first-party results.
- **Pre-existing (not this cycle):** `[R42]`, `[R52]` were already in the corpus.
- **`[unverified]`:** nothing in §E is used as an unsourced fact; none is added to the
  reference list unless fetched, listed, or previously verified.

## 6b · Next-cycle cues · 下轮提示

- Watch the **OWASP Agentic Skills Top 10 (AST10)** / *Agent Control Standard (ACS)* — if
  skills carry risk, a `skills` lever should point at them. **Closed in P20 (2026-10-23):**
  AST10 v1.0 shipped and its README was read in full (`[R245]`); the `security` lever in
  `data/levers.json` and the provenance of `portable-skills` / `untrusted-content-discipline`
  now point at it. It is **not** a 1:1 duplicate of the ASI01–ASI10 list already ingested
  (`[R86]`) — it targets the skills execution layer (SKILL.md / skill.json / manifest.json /
  package.json formats, MAESTRO-mapped). ACS remained a watch item until P43 (2026-10-28): the standard was published 2026-09-01 and is entered at landing grade as `[R270]` (deep-read of the standard text is the follow-up).
- Re-probe **context editing / memory tooling** as provider APIs stabilize; a
  `context-budget-policy` *parameter* may beat prose. **Answered as parameters in P20
  (2026-10-23):** `context-budget-policy`'s provenance now binds the delegation mechanism to
  `[R237]` (+ MCP list-cache hints `[R244]`); the `platform.claude.com/docs` pages were still
  region-blocked, so the cue stays open *only* for a first-party docs read — no new mechanism
  claim is made beyond R237.
- Probe **robustness of agent judges** (evaluation integrity) before trusting any golden set.
  **Still open** (P20 surfaced no full-read-grade primary source for it; related instrumentation
  — LHTB's hidden fake-proof verifiers `[R246]` — is *listed* only).

## See also · 参见

- [`references.md`](references.md) §E (R84–R92) · [`references.bib`](references.bib).
- [`CAPABILITIES.md`](../CAPABILITIES.md) — the always-current generated list (22).
- [`reference/capability-router.md`](../reference/capability-router.md) — *situation → capability → file*.
- [`sources/source-map.md`](../sources/source-map.md) — pattern ← primary source.
