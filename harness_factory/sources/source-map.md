# Source Map · 提炼溯源

> Which pattern came from which primary artifact. Keeps `core/` honest: every claimed pattern traces back.
> 模式 ← 一手材料 的对照表。用于保证 `core/` 每条模式都可溯源。

**Updated:** 2026-10-23 · All URLs retrieved 2026-10-12 (rows: 2026-10-16, 2026-10-18, 2026-10-19, 2026-10-20, 2026-10-23).

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
| M1.10 The working set is leased, not bought (re-check the loaded set at a phase boundary; evict with a reason + reload trigger; never evict an always-on invariant) | Anthropic context editing + memory tool `[R237]` (auto-clears stale tool results at a token threshold, persists to memory first, vendor-reported 84% fewer tokens and +29%/+39% internal gains); cadence and the `{reason, reload_when}` receipt generalised from M5.10's deferral discipline | practitioner + internal |
| M2 Long-running agents (resets, heartbeat, handoff) | Anthropic [26], [27]; OpenAI per-worktree observability [23] | practitioner |
| M2.10 Loop contract (goal state, budget, per-step ground-truth check, no-progress stop); M2.11 declared control graph | Anthropic *Building effective agents* `[R93]`; ReAct `[R94]`; Reflexion `[R95]`; ADK graph workflows `[R96]` | practitioner |
| M2.12 Declared memory backend + resume protocol | Each memory system declares its own store: MemGPT/Letta, Mem0, Zep/Graphiti (bitemporal graph over Neo4j), A-MEM — `data/harnesses.json` class `memory`, official repos (`github.com/letta-ai/letta`, `github.com/mem0ai/mem0`, `github.com/getzep/graphiti`) | docs + repos |
| M3 Verification gates; verify-the-verifier; separate builder/critic | Anthropic [26], [28]; Fowler guides/sensors [19]; Chollet refinement loop [14] | practitioner |
| M3.10 Match the instrument to the claim | GUM + 2026 amendment `[R107]`; NASA-STD-7009B `[R108]`; SI brochure `[R109]`; Registered Reports `[R110]` | standard |
| M3.11 Declare the inferential frame; M3.12 certify the computation; M3.13 declare the method and its assumptions | Bayesian workflow `[R111]`; rank-normalised R-hat `[R112]`; plus the methodology systems in `[R113]`–`[R119]` | academic + standard |
| M4 Provenance & integrity; injection-safe design | Willison lethal trifecta [15], [16]; design patterns paper [17]; repo citation-verify | practitioner + internal |
| M4.10 Meaning-unit fidelity across languages (align by sense group; corroborate; gloss, never silently substitute) | Translation-quality standards ISO 17100 `[R120]`, ISO 5060 `[R121]`; interchange format XLIFF 2.2 `[R123]`; comparative stylistics Vinay & Darbelnet `[R124]`; dynamic equivalence Nida & Taber `[R125]`; cohesion Halliday & Hasan `[R122]`; MQM `[R126]` | standard + academic |
| M3.15 Attribute the loss stage by stage (found → kept → used; first denominator over all items; scoring conventions stated) | LongHarness `[R128]` §3.4 (r1/r2/r3 funnel on OfficeQA Pro; V2 87.8% / 87.3% / 79.7%; exactly-correct episodes counted as passing r1–r2 by protocol); PaperQA2 `[R238]` (precision 85.2% / accuracy 66.0% / refusal 21.9%) | academic |
| M3.16 A comparison discloses its harness (ETCSOVG seven-layer card per arm + variance statement; locked-harness or factorial protocol; otherwise mark *incomplete*) | Stop Comparing LLM Agents Without Disclosing the Harness `[R243]` (arXiv:2605.23950, read in full 2026-10-23; controlled 3×3 grid HV̄/MV̄ = 7.80×, 6/9 ranking reversals; Appx. A minimum-disclosure fields; authors disclaim universality); mirror-image relation to M5.12 ablation is internal reasoning | academic |
| M4.16 A pointer is a claim about support (dangling / stale / unsupported; resolves against the active set; terminates at the source span) | LongHarness `[R128]` §2.3–2.4 (controller validates references against active evidence at submission; Fig. 4 shows a baseline returning a stale value after a recognised correction); PaperQA2 `[R238]` (page-level citation keys, "I cannot answer", cited-and-supported 86.1% vs 71.2%); GraphRAG `[R148]` App. E.3–E.4 as the prompt-only counter-example | academic |
| M1.11 History you cannot rewrite must be summarized forward (compaction has a rewrite shape and an append shape; where the provider preserves reasoning, the summary is an addition and the original turns stay reachable) | Claude Opus 5.5 `[R239]` (preserved thinking forbids editing prior assistant context for accounts created on/after 2026-08-31); append-only ledger discipline already in M4.8 and M1.10 | vendor docs |
| M2.13 Effort is a budget line, not a quality setting (set per stage against the gate; record it with the model id; cross-effort comparison is a settings comparison; cache pricing is part of the arithmetic) | Claude Opus 5.5 `[R239]` (low/medium/high/xhigh/max ladder; default effort reported to match Opus 5 at max for ~1/5 the cost; a benchmark table comparing one model at xhigh against another at high; $0.20 cache read vs $4 input per 1M) | vendor docs |
| M4.17 The serving model is part of the provenance (requested vs served id/version; effort setting; substitutions recorded and their evals invalidated; alias is not a version) | Claude Opus 5.5 `[R239]` (transparent safety re-routing: most cyber tasks to Opus 4.8, biology/frontier-LLM work to Opus 5); Gemini 4 Argon model card `[R240]` (exact model/version and eval conditions named); model-side twin of M4.16 | vendor docs |
| M3.14 A gate trades precision, not coverage (report recall beside precision); M4.11 ontology as a contract; M4.12 one canonical identity per entity; M4.13 bound the answer by the evidence | Constraint-verification case study `[R136]` (relation precision 88.79% → 97.67% with recall 83.05% → 83.42%); RDF 1.1 `[R137]`; OWL 2 `[R138]`; SKOS `[R139]`; SHACL `[R140]`; PROV-O `[R141]`; CIDOC-CRM `[R142]`; generative KG construction `[R149]`; entity resolution `[R150]`; KG evolution `[R151]`; KG quality `[R152]` | academic + standard + internal |
| M5 Self-evolution engine (signal→audit→mutation→journal) | gruel_cooking `harness/evolution.md` + `audit.py`; `_archive/docs/design/self-evolution-mechanism.md`; Hashimoto [21]; OpenAI garbage collection [23]; `review/harness-catalog.md` §3 (ADAS, Gödel Agent, SICA, DGM, FunSearch/AlphaEvolve, SEAL, Reflexion/Self-Refine, Voyager) | internal + practitioner |
| M5.10 The capability round is a mechanism (registry · definition-of-done · deferral with a revisit trigger) | Repo practice: the P-cycles in `tasks/PLAN.md`, `data/cycles.json`, `review/integration-map-2026-10.md`; staged self-improvement (Promote/Register/Deepen/Fission/Archive/Consolidate) above | internal |
| M2 Externalized memory; M5 skill-library persistence | `review/harness-catalog.md` §4–3e (MemGPT/Letta, Mem0, Zep, A-MEM; Voyager skill library) | practitioner |
| Self-evolution safety (admission/authority/scope/containment) | `review/harness-catalog.md` §8 (SAVER, Misevolution) | practitioner |
| M6 Tools & skills (minimal toolset, progressive skills) | huayan `harness/tools.md`, `skills.md`; Anthropic Agent Skills posts; Openharness skill patterns | internal + practitioner |
| M7 Change governance (SSOT, conventional commits, no unsolicited push) | Repo `AGENTS.md` §4; huayan `rules.md`; Fowler relocating rigor [18] | internal + practitioner |
| M0.8 Human gate on destructive acts; autonomy slider | Karpathy "keep AI on a leash" / Iron Man suit [2]; Willison principle 1 [16]; huayan `compliance.md` | practitioner + internal |
| M0.9 Changes visible and reversible | Repo `AGENTS.md` §4 (conventional commits, no unsolicited push, diff-reviewable); Fowler relocating rigor [18] | internal + practitioner |
| M0.10 The harness evolves | `_archive/docs/design/self-evolution-mechanism.md`; Hashimoto [21]; `review/harness-catalog.md` §3; this repo's own recorded rounds (`data/cycles.json`) | internal + practitioner |
| M8 Collaboration & sessions (contracts, escalation, handoff) | Anthropic generator/evaluator + handoff [26]; Hashimoto six-stage adoption [21] | practitioner |
| M8.10 Declare the topology (who runs when, shared state, ownership) | ADK graph workflows `[R96]`; LangGraph persistence `[R97]` | practitioner |

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
| `domains/digital-humanities/` | witness & rights → transcription (HTR) → entity resolution → standard encoding → publication with the apparatus | TEI P5 `[R147]`; EAD3 `[R146]`; IIIF `[R143]`; DCMI Terms `[R144]`; CIDOC-CRM `[R142]`; Getty TGN `[R145]`; historical-transcription literature `[R153]`, `[R154]` |

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
| `ontology-as-contract` | SHACL `[R140]` (a graph validated against declared shapes); OWL 2 `[R138]`; generative KG construction `[R149]`; case study `[R136]` (the stage prompts pin the ontology *before* extraction) | standard + academic |
| `entity-resolution` | SKOS `[R139]` (preferred/alternate labels); Getty TGN `[R145]`; entity-resolution survey `[R150]`; case study `[R136]` (实体规范化 must not merge same-name persons) | standard + academic + internal |
| `evidence-bounded-generation` | PROV-O `[R141]`; GraphRAG `[R148]`; KG quality dimensions `[R152]`; case study `[R136]` (every accepted triple carries its 原文) | standard + academic + internal |
| `schema-evolution` | KG evolution survey `[R151]`; repo change governance M7 (`core/08-change-governance.md`) | academic + internal |
| `prose-polish` | plain-language guidance `[R192]`; GB/T 15834-2011 `[R193]` (punctuation); readability as drift alarm `[R194]`; text-simplification survey `[R195]`; self-refinement needs an external criterion `[R198]` | standard + practitioner + academic |
| `gap-seeking` | unassisted self-correction fails `[R201]`; calibration `[R202]`; partial self-knowledge `[R203]`, `[R204]`, `[R205]`; quality-diversity `[R208]`, `[R209]`, `[R210]`; Goodhart taxonomy `[R216]` | academic |
| `expression-design` | Diátaxis four needs → four forms `[R219]`; documentation quality as ten dimensions of structure/content/style `[R226]`; WCAG 2.2 text alternatives `[R225]`; diagrams generated from the artefact `[R227]`; animation as a time-encoding channel `[R228]`; MQM error typology `[R224]`; fluency/faithfulness negatively correlated `[R229]`; chapter-to-chapter discourse `[R230]`; 信達雅 primary text `[R233]` | academic + standard + practitioner |
| `component-ablation` | retention ≠ causal contribution ≠ deployed utility; model/artifact/harness effects confounded `[R234]`; single-unit ablation against the per-task median, two one-sided paired tests, protected set, held-out ladder `[R235]`; official implementation `[R236]` | academic + first-party code |
| Evidence instrument map (M3.10) | JCGM 100:2008 GUM `[R107]` (uncertainty budget, coverage factor, 2026 nonlinearity amendment); NASA-STD-7009B `[R108]` (verification / validation / credibility + sensitivity analysis); SI brochure `[R109]` (units); COS Registered Reports `[R110]` (pre-registration); Artstein & Poesio `[R102]` (agreement); first-party project pages of the 27 `instruments` catalog entries | standard + practitioner |
| `reference/requirement-refinement.md` (R0–R5 protocol) | Rieseberg [R80]; M8 escalation/handoff; `domains/deep-research/method.md` L0 "restate + confirm" | practitioner + internal |
| `context-budget-policy` (further source) | LongHarness — stateful evidence management over 100M-token corpora `[R128]` (M0.6 smallest high-signal set; just-in-time retrieval over preloading) | preprint |
| `self-improving-loop` (further source) | Harness² — recursive harness that proposes/probes/composes its own next harness, selecting contrastively **without a ground-truth verifier** `[R130]` (M5.10 round mechanism; M3 gate) | preprint |
| `context-budget-policy` — anti-anchoring | Scaling Discovery Requires Forgetting `[R131]` (deliberate forgetting to escape an anchoring hypothesis; ties to reset-vs-compaction) | preprint |
| `resumable-memory` (further source) | ReHarness — recurrent harness for agentic continual learning `[R132]` (state is revised *backwards* as later evidence arrives) | preprint |
| `graph-orchestration` (further source) | The Agentic Scientist — orchestrating coding agents for discovery `[R133]` (M2.10 loop contract; M2.11/M8.10 declared topology) | preprint |
| `traceable-sources` / `durable-execution` (further source) | GitSwarm — commit-level provenance and compounding inference `[R134]` (M4 claim ledger; M8 reviewable diffs) | preprint |
| `reproducible-experiments` / `eval-driven-development` (further source) | AutoEnvScaling — terminal agents automating the environment/data flywheel `[R135]` (M3.10 match the instrument to the claim) | preprint |

> Full analysis and the integration verdict: [`review/ambition-and-agency.md`](../review/ambition-and-agency.md). Refs R80–R83 live in [`review/references.md`](../review/references.md) (group D).
> The 2026-10-18 frontier pass (context · security · durability · spend · evals) is distilled in [`review/frontier-2026-10.md`](../review/frontier-2026-10.md); refs R84–R92 live in group E.
> The 2026-10-18 workflow pass (loops & graphs) is distilled in [`review/workflow-patterns-2026-10.md`](../review/workflow-patterns-2026-10.md); refs R93–R97 live in group F.
> The 2026-10-18 disciplines pass (formal & empirical sciences) is distilled in [`review/disciplines-crosswalk-2026-10.md`](../review/disciplines-crosswalk-2026-10.md); refs R98-R106 live in group G.
> The 2026-10-18 instruments pass (claim -> instrument -> tool -> gate) is mapped in [`reference/evidence-instruments.md`](../reference/evidence-instruments.md); standards refs R107-R110 live in group H, and the tools themselves are catalog entries (class `instruments`, 27 rows).
> The 2026-10-18 mathematics/statistics + methodology pass (P10) adds `statistics` / `geometry-topology` domains, `statistical-inference` / `certified-computation` capabilities, 23 more `instruments` rows (class `instruments`, now 50), and the field→methodology map [`reference/methodology-map.md`](../reference/methodology-map.md); refs R111-R119 live in groups I-J. Scope/status board: [`review/integration-map-2026-10.md`](../review/integration-map-2026-10.md).
> The 2026-10-19 cross-language pass (P11) adds the invariant **M4.10** in `core/05` and the procedure [`reference/cross-language.md`](../reference/cross-language.md); refs R120-R126 live in group K. It also adds the per-field information-outlet map (`reference/outlet-map.md`, group `outlets` in `sources.json`).
> The 2026-10-19 agent-harness frontier rows above are entered from the *Top AI Papers of the Week* roundup (Oct 12–18, 2026); refs R127-R135 live in group L. The roundup is a **second-hand index — retrieval only, never cited**: all ten items were verified at abstract level through a single arXiv API `id_list` batch (id · title · authors · date agree; no phantom entries), and the roundup-only numbers/affiliations still to clear are enumerated outside version control in `updates/2026-10-19-paper-roundup-proposal.md` §5. One item (LoGRA, `arXiv:2610.06647v2`) is recorded there as **considered and declined**, not listed.
> The 2026-10-20 depth pass (P15) adds invariants **M4.14** (`core/05`, reader gate) and **M5.11** (`core/06`, self-model / gap-seeking), capabilities `prose-polish` and `gap-seeking`, five `instruments` rows (`vale`, `languagetool`, `textstat`, `hermit`, `elk`) and 20 `outlets` rows; refs R155-R218 live in groups N-Q. Four surveys back it: [`review/knowledge-graph-patterns-2026-10.md`](../review/knowledge-graph-patterns-2026-10.md), [`review/training-methodology-coverage-2026-10.md`](../review/training-methodology-coverage-2026-10.md), [`review/language-polish-2026-10.md`](../review/language-polish-2026-10.md), [`review/self-model-and-gap-seeking-2026-10.md`](../review/self-model-and-gap-seeking-2026-10.md); the outlet survey is [`review/scholarly-channels-2026-10.md`](../review/scholarly-channels-2026-10.md). All rows in groups N-Q were resolved in one arXiv `id_list` batch plus direct fetches on 2026-10-20 — **abstract-level** verification for arXiv, full-page for standards and tools; ISO standards and the classic style/metacognition books are deliberately **not entered** (403 + paywall, or no first-party record).
> The 2026-10-20 second depth pass (P16) adds invariant **M4.15** (`core/05`, choose the form before the words) and **M5.12** (`core/06`, a module earns its place by ablation), capabilities `expression-design` and `component-ablation`, two `instruments` rows (`mermaid` diagram-as-code · `vega-lite` visualization grammar) with two new kinds, and deepens **M4.14** with a declared audience/register/channel. Two surveys back it: [`review/expression-design-2026-10.md`](../review/expression-design-2026-10.md) and [`review/harness-ablation-2026-10.md`](../review/harness-ablation-2026-10.md); refs R219-R236 live in groups R-S. Verification this round was **stronger than abstract level**: both §S papers were read **in full** (PDF text extracted), and R233 (the 1898 譯例言) is a **primary text** read end to end. The WeChat explainer that pointed at the SHarP paper is a **second-hand summary — retrieval only, never cited**, with the three findings it omitted recorded in the ablation doc §1.

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
