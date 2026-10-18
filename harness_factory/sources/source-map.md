# Source Map · 提炼溯源

> Which pattern came from which primary artifact. Keeps `core/` honest: every claimed pattern traces back.
> 模式 ← 一手材料 的对照表。用于保证 `core/` 每条模式都可溯源。

**Updated:** 2026-10-18 · All URLs retrieved 2026-10-12 (rows: 2026-10-16, 2026-10-18).

---

## 中文速览

这张表把 `core/` 的通用模式与 `domains/` 的域内编排，映射到它们各自的**一手来源**（官方仓库 / 论文 / 官方文档 / 一手访谈）。它在提炼过程中被用来做「泛化检验」：如果一个模式只能从单一项目的内部细节得到，它就不进 `core/`，只作为出处示例。Karpathy 及同行的技能提炼另见 `review/practitioner-playbook.md`；跨行业顶级人物的能力支架见 `review/masters-playbook.md`；全部 agent/自演化 harness 的分类见 `review/harness-catalog.md`。

---

## Core modules ← sources · 核心模块 ← 一手来源

| Pattern (module) | Distilled from | Kind |
|---|---|---|
| M0.1 Truth-before-throughput; M0.4 observe-only automation | Self-evolution mechanism design (`_archive/docs/design/self-evolution-mechanism.md`); huayan `harness/compliance.md` | internal + practitioner |
| M0.2 Source-grounding; M4 provenance & `unverified` tagging | Repo `AGENTS.md` §3 (citations are the lifeline); `tools/citation-verify/` | internal |
| M0.3 / M3 verify-before-done; default-FAIL contract | huayan `workflows/*` gates; Anthropic "Harness design for long-running apps" [26]; Anthropic `cwc-long-running-agents` [27] | practitioner |
| M0.5 SSOT | OpenAI "Harness engineering" (repo as system of record) [23]; repo docs conventions | practitioner + internal |
| M0.6 Minimal high-signal context | Anthropic "Effective context engineering" [25]; Karpathy "context engineering" [4] | practitioner |
| M0.7 Resumable / idempotent | March-of-nines reliability engineering (Karpathy) [5]; Anthropic handoff [26] | practitioner |
| M1 Context engineering (compaction, notes, subagents) | Anthropic [25]; OpenAI progressive disclosure / AGENTS.md-as-map [23] | practitioner |
| M2 Long-running agents (resets, heartbeat, handoff) | Anthropic [26], [27]; OpenAI per-worktree observability [23] | practitioner |
| M3 Verification gates; verify-the-verifier; separate builder/critic | Anthropic [26], [28]; Fowler guides/sensors [19]; Chollet refinement loop [14] | practitioner |
| M4 Provenance & integrity; injection-safe design | Willison lethal trifecta [15], [16]; design patterns paper [17]; repo citation-verify | practitioner + internal |
| M5 Self-evolution engine (signal→audit→mutation→journal) | gruel_cooking `harness/evolution.md` + `audit.py`; `_archive/docs/design/self-evolution-mechanism.md`; Hashimoto [21]; OpenAI garbage collection [23]; `review/harness-catalog.md` §3 (ADAS, Gödel Agent, SICA, DGM, FunSearch/AlphaEvolve, SEAL, Reflexion/Self-Refine, Voyager) | internal + practitioner |
| M2 Externalized memory; M5 skill-library persistence | `review/harness-catalog.md` §4–3e (MemGPT/Letta, Mem0, Zep, A-MEM; Voyager skill library) | practitioner |
| Self-evolution safety (admission/authority/scope/containment) | `review/harness-catalog.md` §8 (SAVER, Misevolution) | practitioner |
| M6 Tools & skills (minimal toolset, progressive skills) | huayan `harness/tools.md`, `skills.md`; Anthropic Agent Skills posts; Openharness skill patterns | internal + practitioner |
| M7 Change governance (SSOT, conventional commits, no unsolicited push) | Repo `AGENTS.md` §4; huayan `rules.md`; Fowler relocating rigor [18] | internal + practitioner |
| M0.8 Human gate on destructive acts; autonomy slider | Karpathy "keep AI on a leash" / Iron Man suit [2]; Willison principle 1 [16]; huayan `compliance.md` | practitioner + internal |
| M8 Collaboration & sessions (contracts, escalation, handoff) | Anthropic generator/evaluator + handoff [26]; Hashimoto six-stage adoption [21] | practitioner |

---

## Domain assemblies ← sources · 域内编排 ← 一手来源

| Domain | Composed from | Primary sources |
|---|---|---|
| `domains/research/` | L0–L6 pipeline, free-first tooling, citation verification | `_archive/docs/PROJECT.md`, `DATAFLOW-AND-REUSE.md`, `TOOL-COMPARISON.md`, `CAPABILITY-STATUS.md` |
| `domains/knowledge-management/` | coverage maps, source ledgers, gates | huayan `harness/{coverage-map,sources,compliance,rules}.md`, `workflows/*` |
| `domains/data-science/` | dataset registry, 3-state judging, non-overlapping splits | Sport_Coach `harness/{PRINCIPLES,TESTING,EVAL_PROTOCOL,datasets}` [see repo paths below] |
| `domains/devops/` | evolution signals, audit, change governance | gruel_cooking `harness/{principles,skills,workflows,evolution,audit.py}` |
| `domains/statistics/` | declared frame → model/priors → convergence-checked computation → interval → robustness | Bayesian workflow `[R111]`; rank-normalised R-hat `[R112]`; Stan `[R113]` |
| `domains/geometry-topology/` | object/representation → invariant → certified computation → independent re-derivation | IEEE 1788-2015 `[R114]`; CAS / geometry-topology instrument catalog |

---

## Capability additions ← sources · 能力新增 ← 一手来源

| Capability | Distilled from | Kind |
|---|---|---|
| `ambition-elevation` (Altitude axis) | Rieseberg "How to be more ambitious" (2026) `[R80]`; Locke & Latham goal-setting (`specific+challenging > do-your-best`) [R81], [R82] | practitioner + academic |
| `expert-instruments` (Depth) | Rieseberg [R80] (real instruments, outside judge, raw data); Anthropic builder/critic + default-FAIL [26], [28]; Chollet refinement loop [14] | practitioner |
| `cross-field-crew` (Range) | Rieseberg [R80]; Anthropic generator/evaluator [26]; Hashimoto six-stage adoption [21] | practitioner |
| `bidirectional-capability-flow` | repo `AGENTS.md` §5 workflow principles; `reference/capability-flow.md`; M5 self-evolution engine | internal |
| `context-budget-policy` | Chroma "Context Rot" `[R84]` (recall degrades with input length); Anthropic "Effective context engineering" `[R52]` (compaction/notes/subagents) | empirical + practitioner |
| `untrusted-content-discipline` | Willison lethal trifecta `[R42]`; OWASP Top 10 for Agentic Applications 2026 `[R86]` (ASI01–ASI10); MCP Security Best Practices `[R87]`; CaMeL `[R88]` | practitioner + standard + academic |
| `durable-execution` | Temporal "Durable AI" `[R90]` (journal/replay, idempotent side effects); METR time-horizon `[R89]` | practitioner + empirical |
| `cost-budget-caps` | Willison "default hard budget caps" `[R85]` (hard, not soft) | practitioner |
| `eval-driven-development` | Agent-as-a-Judge `[R92]` (step-level feedback); OpenTelemetry GenAI conventions `[R91]` (traced runs) | academic + standard |
| `loop-discipline` | Anthropic "Building effective agents" `[R93]` (ground truth per step, stopping conditions); ReAct `[R94]`; Reflexion `[R95]`; ADK loop workflow `[R96]` | practitioner + academic |
| `graph-orchestration` | Anthropic `[R93]` (orchestrator-workers, parallelization); ADK graph-based workflows `[R96]`; LangGraph checkpointers/stores `[R97]` | practitioner |
| `formal-verification` | Mathlib `[R98]`; Lean 4 `[R99]`; Open Logic Project `[R100]` (proof theory / model theory / countermodels); Woodcock *et al.* `[R106]` (formal methods in practice) | academic + practitioner |
| `dimensional-analysis` | Buckingham 1914 `[R104]` (dimensional equations / physically similar systems) | academic (foundational) |
| `empirical-measurement` | Munafò *et al.* `[R103]` (pre-registration, effect sizes, power, analytic flexibility); Artstein & Poesio `[R102]` (inter-coder agreement); Anderson *et al.* `[R105]` (falsifiable cognitive model) | academic + practitioner |
| `statistical-inference` | Gelman *et al.* *Bayesian Workflow* `[R111]` (declared frame, priors, convergence, iterative validation); Vehtari *et al.* `[R112]` (rank-normalised R-hat / ESS); Stan `[R113]` | academic |
| `certified-computation` | IEEE 1788-2015 interval arithmetic `[R114]` (certified-precision arithmetic); the CAS / geometry-topology instrument catalog (`sagemath`…`polymake`) | standard + practitioner |
| Evidence instrument map (M3.10) | JCGM 100:2008 GUM `[R107]` (uncertainty budget, coverage factor, 2026 nonlinearity amendment); NASA-STD-7009B `[R108]` (verification / validation / credibility + sensitivity analysis); SI brochure `[R109]` (units); COS Registered Reports `[R110]` (pre-registration); Artstein & Poesio `[R102]` (agreement); first-party project pages of the 27 `instruments` catalog entries | standard + practitioner |
| `reference/requirement-refinement.md` (R0–R5 protocol) | Rieseberg [R80]; M8 escalation/handoff; `domains/deep-research/method.md` L0 "restate + confirm" | practitioner + internal |

> Full analysis and the integration verdict: [`review/ambition-and-agency.md`](../review/ambition-and-agency.md). Refs R80–R83 live in [`review/references.md`](../review/references.md) (group D).
> The 2026-10-18 frontier pass (context · security · durability · spend · evals) is distilled in [`review/frontier-2026-10.md`](../review/frontier-2026-10.md); refs R84–R92 live in group E.
> The 2026-10-18 workflow pass (loops & graphs) is distilled in [`review/workflow-patterns-2026-10.md`](../review/workflow-patterns-2026-10.md); refs R93–R97 live in group F.
> The 2026-10-18 disciplines pass (formal & empirical sciences) is distilled in [`review/disciplines-crosswalk-2026-10.md`](../review/disciplines-crosswalk-2026-10.md); refs R98-R106 live in group G.
> The 2026-10-18 instruments pass (claim -> instrument -> tool -> gate) is mapped in [`reference/evidence-instruments.md`](../reference/evidence-instruments.md); standards refs R107-R110 live in group H, and the tools themselves are catalog entries (class `instruments`, 27 rows).
> The 2026-10-18 mathematics/statistics + methodology pass (P10) adds `statistics` / `geometry-topology` domains, `statistical-inference` / `certified-computation` capabilities, 23 more `instruments` rows (class `instruments`, now 50), and the field→methodology map [`reference/methodology-map.md`](../reference/methodology-map.md); refs R111-R119 live in groups I-J. Scope/status board: [`review/integration-map-2026-10.md`](../review/integration-map-2026-10.md).

---

## Practitioner skills ← sources · 实践者技能 ← 一手来源


- A. Karpathy — Software 2.0/3.0, march of nines, keep-AI-on-a-leash, context engineering, auto-research [1]–[4].
- I. Sutskever — age of research, generalization, value functions, research taste [5], [6].
- R. Sutton — Bitter Lesson (two parts), OaK, Era of Experience [7]–[9].
- J. Carmack — learn-from-experience, reality-not-turn-based [10], [11].
- F. Chollet — measure of intelligence, refinement loop, ARC-AGI-3 [12]–[14].
- S. Willison — agents-as-loop, lethal trifecta, injection-safe patterns [15]–[17].
- C. Fowler — Relocating Rigor [18]; B. Böckeler / M. Fowler — Agent = Model + Harness, guides vs sensors [19], [20].
- M. Hashimoto — harness engineering, AGENTS.md from failures [21], [22].
- OpenAI Codex team — agent legibility, AGENTS.md-as-map, garbage collection [23], [24].
- Anthropic — context engineering, generator/evaluator split, default-FAIL [25]–[28].
- E. Mollick — models/apps/harnesses [29], [30]; D. Hassabis — scientific method for AI [31], [32].

**Cross-industry ability harnesses** ← `review/masters-playbook.md` §References. Non-AI figures (investing, startups, product, hardware, science, risk, content, growth, education): Munger [1], [2]; Naval [3], [4]; Paul Graham [5], [6]; Jobs [7], [8]; Musk [9], [10]; Zhang Yiming [11]; Feynman [12]; Taleb [13]; MrBeast [14]; X-Mentor [15]; Sun Yuchen [16] (understanding-only); Trump [17] (understanding-only); Zhang Xuefeng [18]. Immediate source = the local perspective skill files under `C:\Users\data\.agents\skills\huashu-nuwa\examples\`.

---

## Local source paths (for re-extraction) · 本地来源路径

- `C:\DA_Practice\cookbooks\gruel_cooking\harness\` — `README.md`, `principles.md`, `skills.md`, `workflows.md`, `evolution.md`, `audit.py`
- `C:\DA_Practice\huayan_collection\harness\` — `README.md`, `principles.md`, `rules.md`, `skills.md`, `tools.md`, `sources.md`, `coverage-map.md`, `concerns.md`, `compliance.md`, `workflows\*.md`
- `C:\DA_Practice\Sport_Coach\sportscoach\tennis_play\harness\` — `README.md`, `PRINCIPLES.md`, `TESTING.md`, `DEBUG.md`, `RESEARCH.md`, `ERROR_PREVENTION.md`, `metrics/METRICS.md`, `reports/{EVAL_PROTOCOL,REPORT_TEMPLATE}.md`, `datasets/build_registry.py`
- `harness_factory\_archive\docs\` — `PROJECT.md`, `DATAFLOW-AND-REUSE.md`, `CAPABILITY-STATUS.md`, `TOOL-COMPARISON.md`, `PLAN.md`, `PROGRESS.md`, `design\*.md`, `paper\*.md`, `refs\*.md`

> Extracted as *patterns* only. Concrete project content is intentionally **not** carried into `core/`; it stays in `_archive/` and appears here as provenance.
