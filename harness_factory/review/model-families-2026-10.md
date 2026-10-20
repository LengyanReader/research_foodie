# The model is a variable · 模型是变量

> What the three frontier families (OpenAI · Anthropic · Google) now expose, as of 2026-10-20 — and which of it changes how a harness must be built.
> 御三家截至 2026-10-20 暴露出的机制中，哪些真正改变了 harness 的建法。

**Updated:** 2026-10-20 · Sources: §V of [`references.md`](references.md) (R239–R242) · Access date 2026-10-20

---

## 中文速览

**结论：三家的差异在模型，收敛在 harness。** 2026 年 10 月的三个旗舰（Claude Opus 5.5 / Gemini 4 Argon / OpenAI 的 5.6–6 代）在榜单上互有胜负，但对外暴露的**机制**已经趋同，而且这五个机制里有三个会**推翻**本仓库此前的默认做法：

1. **努力档位成了计价商品**（low→max，或思考 token 预算）。同一份发布里的对比表就用了**不同档位**（xhigh 对 high），所以「模型 A 胜模型 B」可能只是「设置 A 胜设置 B」。默认档在 Opus 5.5 上被报为以约 1/5 成本追平上一代 max 档 `[R239]`——**默认拉满不是质量设置，是把预算花在门禁看不见的地方**。→ 新条款 **M2.13**。
2. **服务你的模型未必是你请求的模型**。Opus 5.5 的安全策略把多数网络安全任务改路由到 Opus 4.8、生物与前沿 LLM 研发任务改路由到 Opus 5，且是**透明**的 `[R239]`；别名也会悄悄指向新快照。**模型 id 不属于稳定身份**。→ 新条款 **M4.17**（与 M4.16 的指针纪律同构：指针要指到真正支撑断言的东西，模型 id 要指到真正产出它的东西）。
3. **历史可能不再可改写**。Anthropic 的 *preserved thinking* 禁止 2026-08-31 之后创建的 API 账号编辑既有 assistant 上下文 `[R239]`；只会「就地改写」的压缩策略在这类历史上**直接失效**。→ 新条款 **M1.11**：不可改写的历史只能向前摘要。
4. **沙箱与工作区成了产品级概念**（OpenAI Agents SDK：Manifest / 快照 / 能力）。但文档自己承认：会话**不保证 OS 级隔离**、快照只存工作区根目录、能力开关只控制「看得见」而**不授权**模型自拟的实参 `[R241]` `[R242]`。→ 不新增条款，只加深 **M6**（暴露≠授权；「沙箱」须点名机制）。
5. **长上下文要实测，不能假设**。Gemini 4 Argon 的 1M 窗口在厂商自己的长上下文评测里，从 ≤128k 的 99.7% 掉到 256k–1M 的 84.2% `[R240]`——窗口长度不等于可用注意力。→ 已由 **M1.5 / M1.10** 覆盖，不重复立条款。

**为什么只加一个能力**：`model-selection` 域一直有 L0–L5 的方法说明，却**没有任何能力在 `derive` 时触发**——这是 P18 审计里「域有文档、路由无入口」的同型空洞。新增 `model-portfolio-discipline`（仅 `domain=model-selection` 触发）填的正是这个分离集：选型任务的判据是「在自己的留出集上、在声明的档位上测过」，而现有能力没有任何一条要求这件事。**只加能力还不够**：通用邻域（`model`/`模型`/`评测`）按计数会把「选一个模型」判成数据科学，所以同时补了显式选型线索（命中即定向该域，且刻意排除「模型对比」）——否则等于交付一条没人能触发的规则。**未采纳**的项（三家各自的引用 API、computer-use 细节、fast mode、CCL 案例）逐条记了理由与重开条件，见 §5。

---

## 0. Ask, scope, and what this read is not

The ask was to check, analyse and evaluate the current flagship models of OpenAI / Anthropic / Google and identify harness capabilities worth integrating. That framing has a trap: a **model comparison** produces a ranking, while a **harness** needs mechanisms that stay true when the ranking changes next quarter. So the unit of analysis here is not "which model is best" but **"which exposed behaviour changes what a harness must declare, record, or test"**.

Three boundaries, stated up front:

- **No benchmark adjudication.** Vendor numbers are quoted only as *vendor-reported*, and only where a clause leans on the mechanism behind them (e.g. an effort ladder exists and is priced). Nothing here re-ran a benchmark, and no leaderboard ordering is asserted.
- **No pricing advice.** Prices appear as evidence that cost is now a function of *effort × cache × tier*, not as a recommendation.
- **No OpenAI model claim beyond what was reachable.** `openai.com/index/*`, `platform.openai.com/docs` and `help.openai.com` returned **403**; `ai.google.dev` and `cloud.google.com` failed at transport; `platform.claude.com/docs` is region-blocked. The OpenAI row therefore rests on the vendor's own **Agents SDK documentation** `[R241]` `[R242]`, and the model names in the comparison column are those *named by the other two vendors' pages* `[R239]` `[R240]` — recorded as such, not as verified product facts.

## 1. The three families as of 2026-10-20

| Vendor | Frontier tier | First-party evidence read | Harness-relevant surface |
|---|---|---|---|
| **Anthropic** | Claude **Opus 5.5** (22 Sep 2026), below **Fable 5.1**; Opus 5 is the model the release is priced against | announcement `[R239]` | effort ladder + prices + cache tiers; fast mode; **transparent safety re-routing**; **preserved thinking** (prior context immutable); thinking cannot be disabled; per-action classifier; open-source sandbox |
| **Google** | Gemini **4 Argon** (13 Oct 2026) | model card `[R240]` | 1M-token in/out; native text/image/audio/video; long-context degradation measured; computer use; CCLs not ruled out → deployment safeguards |
| **OpenAI** | frontier tier named in the other two vendors' comparison tables `[R239]` `[R240]`; `gpt-5.6-sol` appears in OpenAI's own SDK example `[R242]` | Agents SDK docs `[R241]` `[R242]` (**model pages 403**) | sandbox **Manifest / capabilities / snapshot**; compaction as a capability; **exposure vs authorization**; MCP servers authorize themselves; session lifecycle; concurrency/archive limits |

What is **not** in this table, deliberately: parameter counts, training data, context-window races as a scoreboard, and any "X is better than Y". They are not harness inputs.

## 2. Five mechanisms that converged

Convergence is the finding, not any single feature. Three vendors with different architectures now expose the same five levers — which means a harness can be written against the **lever**, not the vendor.

| # | Mechanism | Evidence | What it does to a harness |
|---|---|---|---|
| 1 | **Reasoning effort as a priced dial** (low→max, or thinking budget) | `[R239]` (ladder, prices, default-vs-max cost ratio) | Effort becomes a per-stage budget decision that must be *recorded*; leaving it at the maximum is a cost bug, and comparing models across efforts is a measurement bug |
| 2 | **Provider-side routing and fallback** (safety re-route; alias drift) | `[R239]` (cyber → Opus 4.8; bio/frontier-LLM → Opus 5) | The served model is part of provenance; a silent substitution invalidates an eval and a claim's attribution |
| 3 | **Immutable prior context** (preserved thinking) | `[R239]` (accounts on/after 2026-08-31) | Compaction must have an **append** shape, not only a rewrite shape; the original turns stay reachable |
| 4 | **Workspace contract + isolation claim** (Manifest / snapshot / backend) | `[R241]` (fresh-session contract; no OS-level guarantee; snapshot = workspace root) | "Declared workspace", "live workspace" and "snapshot" are three objects; "sandbox" is a claim about a backend that must name its mechanism |
| 5 | **Capability exposure ≠ authorization** | `[R242]` (callbacks cannot authorize arguments; MCP authorizes its own operations) | Authorization lives inside the tool, on the concrete argument — the visible-tool list is not a security boundary |

Two more that did **not** need new machinery, because the library already states them: **long context is not free attention** (`[R240]`: 99.7% at ≤128k → 84.2% at 256k–1M; M1.5 compaction, M1.10 eviction) and **computer use is sandboxed execution** (M6; `[R240]` OSWorld-2.0 69.2% is a capability number, not a new requirement).

## 3. Mapping onto the 37 capabilities

Test applied to each mechanism: *does an existing capability already require this, or would a competent harness that follows the library still get it wrong?* "Partial" means the floor mentions the object but not the new failure mode.

| Mechanism | Existing coverage | Verdict |
|---|---|---|
| Effort/thinking as a priced per-stage dial | `cost-budget-caps` (ceilings), `eval-driven-development` (gates) — neither decides **where** effort goes, and neither records it | **Gap** → M2.13 |
| Served model differs from requested (re-route, alias, fallback) | `traceable-sources` (sources), `durable-execution` (run state) — nothing records the producer | **Gap** → M4.17 |
| Prior context immutable (preserved thinking) | M1.5 compaction (summarise state), M4.8 append-only ledger — but compaction was implicitly a rewrite | **Gap** → M1.11 |
| Workspace contract: declared vs live vs snapshot | `durable-execution`, `resumable-memory` — durability is required, the *three objects* are not distinguished | **Partial** → M6 checklist + anti-patterns (no clause) |
| Exposure is not authorization | `tool-use` (least privilege), `untrusted-content-discipline` (M4.5) — neither says the model's *argument* is untrusted input to the tool | **Partial** → M6 checklist + anti-patterns |
| Sandbox is a backend claim | `sandboxed-execution` — requires a sandbox, not a named mechanism and its limits | **Partial** → M6 checklist + anti-patterns |
| 1M context with measured degradation | `context-budget-policy` (M1.5, M1.10) | **Covered** |
| Computer use / GUI agents | `sandboxed-execution`, `tool-use` | **Covered** |
| Fast mode (2.5× at 2× price) | `cost-budget-caps` | **Covered** — a latency/cost trade inside the same cap |
| Native citations / grounding tools | `traceable-sources`, `evidence-bounded-generation`, M4.16 | **Covered** — vendor mechanism, same obligation |
| Model choice itself (portfolio, per-stage tier, re-eval on change) | `model-selection` domain documents L0–L5, but **no capability fires** | **Gap** → `model-portfolio-discipline` |

The last row is the P18-shaped hole: a domain with a written method and no router entry. It is not "another model capability"; it is the requirement that a model choice be a **measurement on your own task at a declared effort**, which none of the existing 37 asks for.

## 4. What was integrated

**Clause M1.11 — history you cannot rewrite must be summarized forward** (`core/02-context-engineering.md`). Compaction has two shapes, rewrite and append; the provider can remove the choice. Where reasoning is preserved, the summary is an **addition** — decisions, open questions, evidence pointers, next action — and the original turns remain reachable. Test: can the next stage resume from the summary *and* can a reader still reach the turn it summarises?

**Clause M2.13 — effort is a budget line, not a quality setting** (`core/03-long-running-agents.md`). Set effort per stage against the gate; keep it low where the work is mechanical; record it beside the model id. Two named failures: max-effort-by-default, and cross-effort comparison (a difference that belongs to the settings). Cache pricing is part of the same arithmetic, so context layout is a budget decision.

**Clause M4.17 — the serving model is part of the provenance** (`core/05-provenance-and-integrity.md`). Record requested id, served id/version, effort setting, and any substitution with its reason. An eval whose model changed silently is not a measurement; an invisible fallback is a provenance defect even when the output is good. Twin of M4.16: the pointer must resolve to what supports the claim, the model id to what produced it.

**Capability `model-portfolio-discipline`** (`domain=model-selection`, modules M3/M4/M7). Requirements matrix → per-stage portfolio → minimal fit-for-task eval on your own hold-out **at a declared effort** → hard decision gate with ids, versions and effort recorded. A tie goes to the cheaper tier; a change of tier or effort re-opens the evaluation. Registered in `data/capabilities.json` and routed from `reference/capability-router.md` (the row that previously said "—").

Reachability was half the work. The capability fires only on `domain=model-selection`, and the domain was practically unreachable from text: a real ask — *在 GPT 和 Claude 之间选一个模型，做一个可复现的适配性评测* — classified as `data-science`, because that domain's generic signals (`model`, `模型`, `eval`, `评测`) outvote the selection domain's exact phrases by count. Adding the capability without fixing this would have shipped a rule no one can trigger. The fix reuses P18's rule rather than inventing a new mechanism: **explicit cues outrank the domain default**. `_SELECTION_CUES` names a *choice* (`which model`, `choose a model`, `选一个模型`, `哪个模型`, `选型` …) and points the domain at `model-selection`; `模型对比` / `model comparison` is deliberately excluded, because an ablation or a literature review is phrased the same way. Three guards pin it: a Chinese and an English selection ask must land on the domain, and a comparison-only ask must not.

**M6 deepening (no new clause, M0.5 discipline).** Two checklist rows and two anti-patterns: *exposure as authorization* (the visible-tool list is not the boundary; the tool authorizes its arguments — `[R242]`) and *sandbox as a word* (name the mechanism, its limits, and durable-vs-runtime paths — `[R241]`). These are sharpening an existing module, not a new obligation, so they do not inflate the clause count.

## 5. Deliberately not integrated

Recorded with the trigger that would reopen each, per M0.5.

| Not added | Why | Revisit when |
|---|---|---|
| **Vendor citation / grounding APIs** as a capability | The obligation is already stated output-side (M4.13, M4.16, `evidence-bounded-generation`); a vendor's citation object is one way to satisfy it, and a harness that depends on it loses portability | A vendor's citations become non-portable in a way that changes the *check* (e.g. spans that cannot be verified locally) |
| **Computer-use / GUI specifics** | `sandboxed-execution` + `tool-use` already require isolation and typed arguments; the OSWorld figure is a model property, not a harness rule | GUI actions become a primary artifact class (screenshots as evidence) rather than a tool surface |
| **Fast mode / latency tiers** | A cost-latency trade inside `cost-budget-caps`; no new declaration is needed | Latency becomes an explicit acceptance criterion in the requirements matrix for most tasks |
| **CCL / deployment-safeguard cases** | Product and policy decisions, not harness mechanisms; the harness obligation (don't claim a model did what it didn't) is covered by M4.17 | A task's legality or admissibility depends on a CCL determination |
| **A `provider-routing` capability** | The *requirement* is recording and invalidation (M4.17), not choosing a route; a capability keyed on "provider reroutes" is not expressible in the task vector | A second independent mechanism appears (e.g. per-request model selection by the harness across vendors at scale) |
| **1M-context guidance** | Already covered by M1.5/M1.10; the new number confirms the existing rule rather than changing it | A model sustains attention flat across the full window, measured independently |

## 6. Limits of this read

- **Blocked hosts:** `openai.com` / `platform.openai.com` / `help.openai.com` (403), `ai.google.dev` (timeout), `cloud.google.com` (transport), `platform.claude.com/docs` (region block), `raw.githubusercontent.com` (transport). No claim rests on them.
- **Vendor-reported numbers** (prices, effort-cost ratios, GraphWalks, OSWorld-2.0) are **not** peer-reviewed and are labelled wherever used; no clause depends on their exact value, only on the mechanism they evidence.
- **OpenAI's model line is under-verified here by construction.** The row in §1 is a documentation row, not a model row. A later round with access to OpenAI's model pages should fill it — and, per M4.17, should record the access date with the model snapshot it describes.
- **One session.** The mechanisms were read once, from announcement-level and docs-level text. Any clause that turns out to be vendor-specific (preserved thinking is the obvious candidate) already carries its scope in the text rather than being generalised silently.
