# Harness capabilities · Harness 能力总览

> **Generated** from `src/harness_factory/data/capabilities.json` + `modules.json` — **do not edit by hand**; run `harness capabilities --write` (also refreshed by `harness catalog --write`) to regenerate.
> **生成文档**：由上述 SSOT 生成，**请勿手改**；用 `harness capabilities --write` 重新生成（`harness catalog --write` 亦会同步刷新）。

**43 capabilities · 9 modules (M0–M8)**

---

## Purpose · 目的

A harness is the durable scaffolding around an agent: the invariants it must hold, the context it may load, the memory it externalises, the gates that define "done", the provenance it records, the tools/skills it may use, the governance over its changes, and how it collaborates with humans. This repository compiles a *task-specific* harness instead of shipping one fixed scaffold.

**Capabilities are the middle layer** between a task's features and the modules that get enabled. Each capability is one reusable *requirement* (e.g. "verification gate", "resumable memory", "sandboxed execution") that fires when the task's feature vector matches its `when` clause, and then **annotates** the already-enabled modules with *why* they matter (M0.4: it augments explainability, it never overrides the rule engine).

> 中文速览：harness 是围绕 agent 的耐久脚手架。**能力（capability）**是「任务特征 → 启用模块」之间的**数据驱动中间层**：每条能力是一个可复用的**要求**，由任务特征向量匹配 `when` 触发，给已启用模块**标注理由**——只增可解释性，绝不改变规则引擎的决定（M0.4）。

## How it works · 工作机制

```
task text ──▶ feature vector ──▶ capability.match(when) ──▶ annotate enabled modules
            (classify)           (data/capabilities.json)      → .harness/manifest.json
```

1. **Classify** the goal into the 8-axis feature vector (`horizon`, `verifiability`, `stakes`, `grounding`, `artifact`, `tool_surface`, `collaboration`, `domain`).
2. **Match** every capability whose `when` clause holds for that vector.
3. **Annotate** the enabled modules with the matching capability ids + reasons; record all of it in `.harness/manifest.json` for review.

## Modules · 模块 (M0–M8)

| id | module | one-line rule | doc |
|---|---|---|---|
| M0 | Meta-principles · 元原则 | Truth and traceability outrank speed; automate only observe/record/rank | `core/01-meta-principles.md` |
| M1 | Context engineering · 上下文工程 | Context is a finite, scarce resource - curate, don't dump | `core/02-context-engineering.md` |
| M2 | Long-running agents · 长时程 agent | Externalize memory; advance incrementally; make every run resumable | `core/03-long-running-agents.md` |
| M3 | Verification & gates · 验证与门禁 | Define done before work; verify the verifier; hard vs soft gates | `core/04-verification-and-gates.md` |
| M4 | Provenance & integrity · 来源与完整性 | Every fact traceable to a primary source; uncertain means uncertain | `core/05-provenance-and-integrity.md` |
| M5 | Self-evolution · 自演化 | signal -> audit -> mutation -> journal, human-gated | `core/06-self-evolution.md` |
| M6 | Tools & skills · 工具与技能 | Minimal toolset; biased errors; skills load progressively | `core/07-tools-and-skills.md` |
| M7 | Change governance · 变更治理 | Single source of truth; reviewable diffs; no unsolicited destructive acts | `core/08-change-governance.md` |
| M8 | Collaboration & sessions · 协作与会话 | Explicit contracts; escalate decisions; hand off with state | `core/09-collaboration-and-sessions.md` |

## Capabilities · 能力清单

### `baseline-discipline` — Baseline discipline · 基线纪律

- **Fires when · 触发条件:** always · 总是
- **Modules · 关联模块:** M0, M1, M7
- **Why · 理由:** Every task needs load-bearing invariants, curated context, and change governance.

### `verification-gate` — Verification gate · 验证门禁

- **Fires when · 触发条件:** always · 总是
- **Modules · 关联模块:** M3
- **Why · 理由:** Define done before work and verify with observed evidence (M0.3). Agreement is not verification: when selecting or revising among sampled rollouts, disagreements are adjudicated against environmental evidence and consensus is audited for jointly omitted requirements - verification is an evidence-bearing act, not a vote (M3.17).

### `resumable-memory` — Resumable memory · 可续接记忆

- **Fires when · 触发条件:** horizon ≥ session
- **Modules · 关联模块:** M2
- **Why · 理由:** Work that spans a session must externalize state and resume from it.

### `traceable-sources` — Traceable sources · 来源可溯

- **Fires when · 触发条件:** grounding ∈ {preferred, required} (来源要求) OR artifact ∈ {document, dataset, knowledge_base} (产物)
- **Modules · 关联模块:** M4
- **Why · 理由:** Cited material demands every claim trace to a primary source (M0.1).

### `self-improving-loop` — Self-improving loop · 自改进循环

- **Fires when · 触发条件:** horizon ≥ multi_session
- **Modules · 关联模块:** M5
- **Why · 理由:** Multi-session work benefits from an explicit signal→audit→mutation→journal loop (M0.10). Each proposed self-edit or checkpoint swap is gated by acceptance criteria named before application, patches the cause rather than the triggering example, attributes which axis moved (harness/model/environment), and carries a declared rejection bound - and gains are not assumed to compound across rounds (M5.13).

### `tool-use` — Tool use · 工具使用

- **Fires when · 触发条件:** tool_surface ∈ {read, read_write, external} (工具面)
- **Modules · 关联模块:** M6
- **Why · 理由:** A task that touches the world needs a minimal, progressive toolset.

### `human-review-gate` — Human review gate · 人工复核门

- **Fires when · 触发条件:** collaboration ∈ {human_review, multi_agent} (协作) OR stakes ∈ {high} (风险)
- **Modules · 关联模块:** M8
- **Why · 理由:** Others are involved or stakes are high: escalate irreversible decisions (M0.8).

### `high-stakes-guardrails` — High-stakes guardrails · 高风险护栏

- **Fires when · 触发条件:** stakes ∈ {high} (风险)
- **Modules · 关联模块:** M3, M8
- **Why · 理由:** When stakes are high, strengthen gates and lower autonomy.

### `reproducible-experiments` — Reproducible experiments · 可复现实验

- **Fires when · 触发条件:** domain ∈ {data-science, research} (领域) and verifiability ∈ {high} (可验证性)
- **Modules · 关联模块:** M3, M4, M5
- **Why · 理由:** Data/research with measurable outcomes must be reproducible and traceable.

### `long-horizon-autonomy-control` — Long-horizon autonomy control · 长时程自主控制

- **Fires when · 触发条件:** horizon ≥ multi_session and stakes ∈ {high} (风险)
- **Modules · 关联模块:** M2, M3, M8
- **Why · 理由:** A long, high-stakes run needs durable memory, hard gates, and low autonomy. The autonomy frontier moves on a months-scale: METR's 50%-success time horizon is reported at ~1.1 h with a ~105-day doubling fit (R249, *listed, directional, as of 2026-09*; refreshes R89) -- gate and escalation designs are time-boxed assumptions, so record the as-of date and revisit on schedule.

### `frontier-standard` — Frontier standard / apex bar · 最高标准 / 标杆

- **Fires when · 触发条件:** domain ∈ {excellence} (领域) OR (verifiability ∈ {high} (可验证性) and horizon ≥ multi_session)
- **Modules · 关联模块:** M3, M5, M8
- **Why · 理由:** Measure output against the best-known standard, ratchet up monotonically, and track the moving frontier (M0.3/M0.5/M0.10); never self-declare excellence.

### `sandboxed-execution` — Sandboxed / least-privilege execution · 沙箱 / 最小权限执行

- **Fires when · 触发条件:** tool_surface ∈ {external} (工具面) OR stakes ∈ {high} (风险)
- **Modules · 关联模块:** M3, M6, M7
- **Why · 理由:** Anything that executes code or reaches the world declares an execution backend and a least-privilege posture (isolation, approval for irreversible acts) rather than running unconstrained (M0.4/M0.8).

### `portable-skills` — Portable skills (Agent Skills format) · 可移植技能（Agent Skills 格式）

- **Fires when · 触发条件:** tool_surface ∈ {read, read_write, external} (工具面)
- **Modules · 关联模块:** M6
- **Why · 理由:** Skills are emitted in the Agent Skills (SKILL.md) open format so the same skill loads in any compatible harness (agentskills.io), not just the one that generated it. Portability is also the attack surface: OWASP AST10 (R245) catalogues this format's execution-layer risks -- malicious skills, over-privilege, insecure metadata, update drift, cross-platform reuse -- so an emitted skill carries provenance and least-privilege obligations, not just a description.

### `ambition-elevation` — Ambition elevation (raise, then converge) · 野心提升（先拔高，再收敛）

- **Fires when · 触发条件:** horizon ≥ session
- **Modules · 关联模块:** M0, M3, M8
- **Why · 理由:** Restate the ask at a higher altitude before executing: offer an Elevated (stretch) and a Moonshot reading of the goal, classify constraints as hard / soft / assumed, then converge to the smallest verifiable increment with explicit human confirmation (M0.3/M0.4/M0.8). See reference/requirement-refinement.md.

### `expert-instruments` — Expert instruments (depth) · 专家级工具（深度）

- **Fires when · 触发条件:** verifiability ∈ {high} (可验证性) OR horizon ≥ multi_session
- **Modules · 关联模块:** M3, M4, M6
- **Why · 理由:** Depth comes from insisting on the instruments the best practitioners in the field actually use (the real solver/DB/eval harness and the rawest data, not toy substitutes) and from an outside judge that can be run -- not the model grading itself (M0.2/M0.3).

### `cross-field-crew` — Cross-field crew (range) · 跨领域班底（广度）

- **Fires when · 触发条件:** collaboration ∈ {multi_agent} (协作) OR horizon ∈ {long_running} (时间跨度)
- **Modules · 关联模块:** M6, M8
- **Why · 理由:** Range comes from reframing nouns as verbs and convening a cognitively diverse crew (analyst / editor / red-team) to *do* the work the discipline does -- not to role-play a persona (M0.4/M8).

### `bidirectional-capability-flow` — Bidirectional capability flow · 双向能力流

- **Fires when · 触发条件:** always · 总是
- **Modules · 关联模块:** M0, M5, M7
- **Why · 理由:** Each harness also writes a task-local capability ledger (`.harness/capabilities.local.md`) and, at the end, proposes the generalizable patterns it found back to the factory catalog -- observe-only and human-gated (M0.4/M0.5/M0.10). See reference/capability-flow.md.

### `context-budget-policy` — Context budget policy · 上下文预算纪律

- **Fires when · 触发条件:** horizon ≥ session OR tool_surface ∈ {read, read_write, external} (工具面)
- **Modules · 关联模块:** M1, M2
- **Why · 理由:** Attention is a fixed, non-uniform budget: recall degrades as the window fills even on trivial tasks ("context rot"). The window is working memory -- write durable facts outside it (M2), then select / compress / isolate what enters, and compact only against a measured constraint (M0.6). The loaded set is leased, not bought: at each phase boundary re-check it, put back what no longer changes a decision (with a reason and a reload trigger), and never evict an always-on invariant (M1.10). Reference parameters now exist at the API level: threshold-triggered clearing of stale tool results and a client-side memory tool (R237) show the policy can be delegated to the provider; MCP 2026-07-28 list-cache hints ttlMs/cacheScope (R244) make the refresh cost of tool lists explicit -- a budget line, not an ambient cost.

### `untrusted-content-discipline` — Untrusted-content discipline · 不可信内容纪律

- **Fires when · 触发条件:** tool_surface ∈ {external} (工具面) OR artifact ∈ {document, knowledge_base} (产物) OR grounding ∈ {required} (来源要求)
- **Modules · 关联模块:** M4, M6, M7
- **Why · 理由:** Retrieved bytes -- web pages, files, tool output, even tool descriptions -- are untrusted data, never instructions (M0.1/M0.4). Keep trusted instructions and untrusted data in separate regions, break at least one leg of the lethal trifecta (private data + untrusted content + egress channel), and enforce least authority at the call site. Skill bodies and skill metadata are themselves an untrusted-instruction channel at run time -- the AST01/AST05 classes of OWASP AST10 (R245) target exactly this layer, external instructions included.

### `durable-execution` — Durable execution · 持久执行

- **Fires when · 触发条件:** horizon ≥ multi_session
- **Modules · 关联模块:** M2, M3
- **Why · 理由:** Work that outlives a process must journal each step and replay, not re-run: record the durable log, make every side effect idempotent, and treat human approval as recorded state -- a checkpoint alone is not exactly-once (M0.3/M0.7). The MCP 2026-07-28 Tasks extension (io.modelcontextprotocol/tasks, poll via tasks/get, update via tasks/update; R244) is protocol-level convergence on exactly this shape: long-running work as a durable, addressable task resource.

### `cost-budget-caps` — Cost budget caps · 成本预算上限

- **Fires when · 触发条件:** tool_surface ∈ {external} (工具面) OR horizon ≥ multi_session
- **Modules · 关联模块:** M3, M7
- **Why · 理由:** An unattended loop can incinerate a budget, so set a HARD cap on calls/tokens/spend and halt rather than warn (M0.3/M0.8): choose the number up front, and make uncapped operation an explicit opt-in.

### `eval-driven-development` — Eval-driven development · 评测驱动开发

- **Fires when · 触发条件:** verifiability ∈ {high} (可验证性) OR horizon ≥ multi_session
- **Modules · 关联模块:** M3, M5
- **Why · 理由:** Grade the trajectory, not only the final artifact (M0.3): each recurring failure becomes a frozen golden case, so every harness change is re-scored against an evaluator that is not the author (M0.4). Report the stage funnel (found / kept / used) rather than one end-to-end score, so the loss is locatable and the repair is chosen rather than guessed (M3.15).

### `loop-discipline` — Loop discipline (termination · budget · no-progress) · 循环纪律（终止 · 预算 · 无进展）

- **Fires when · 触发条件:** tool_surface ∈ {read_write, external} (工具面) OR horizon ≥ multi_session
- **Modules · 关联模块:** M2, M3, M6
- **Why · 理由:** An agent is a loop over tools (ReAct): write the goal state that ends it, the step/turn budget, and the per-step ground-truth check BEFORE it runs -- and detect a repeating state/action so a stalled run stops instead of retrying blindly (M0.3/M0.7).

### `graph-orchestration` — Graph orchestration (declared topology · typed state) · 图编排（显式拓扑 · 类型化状态）

- **Fires when · 触发条件:** collaboration ∈ {multi_agent} (协作) OR horizon ≥ multi_session
- **Modules · 关联模块:** M2, M8
- **Why · 理由:** Multi-step or multi-worker work gets a DECLARED control graph -- typed shared state, explicit nodes and (conditional) edges, fan-out on a frozen input, explicit fan-in merge, one owner per shared value, a checkpoint per node -- instead of hoping an implicit prompt-driven flow stays on track (M0.5/M0.7).

### `formal-verification` — Formal verification (machine-checked claims) · 形式验证（机器可核验）

- **Fires when · 触发条件:** domain ∈ {mathematics, logic} (领域) OR (verifiability ∈ {high} (可验证性) and artifact ∈ {code} (产物))
- **Modules · 关联模块:** M3, M4, M6
- **Why · 理由:** For a formal claim, prose agreement is not evidence: state the language and axioms, push the derivation through a proof assistant or a checked model, keep the axiom base and every imported lemma as provenance, and treat an unclosed goal as UNFINISHED (M0.3) -- not as 'morally true'.

### `dimensional-analysis` — Dimensional & numerical discipline · 量纲与数值纪律

- **Fires when · 触发条件:** domain ∈ {physics, engineering, chemistry, earth-environment} (领域)
- **Modules · 关联模块:** M3, M6
- **Why · 理由:** A physical quantity carries units and error: check dimensional consistency before any arithmetic, carry units and uncertainty through every step, state the tolerance/convergence criterion up front, and pin the toolchain for numeric work (M0.3) -- a number without units or error bars is not a result.

### `empirical-measurement` — Empirical measurement & inference · 实证测量与推断

- **Fires when · 触发条件:** domain ∈ {psychology, cognitive-science, medicine, economics-finance, social-science, education} (领域)
- **Modules · 关联模块:** M3, M4
- **Why · 理由:** When the claim is empirical, pre-specify the design and the analysis before seeing the data, report effect sizes with intervals (not only p), control multiplicity, and show the measurement itself is reliable (inter-rater agreement / alpha / test-retest): pre-registered confirmation is a different claim from exploration, and 'significant' is not 'large'.

### `statistical-inference` — Statistical inference (frame, convergence, interval) · 统计推断（框架·收敛·区间）

- **Fires when · 触发条件:** domain ∈ {statistics} (领域)
- **Modules · 关联模块:** M3, M4
- **Why · 理由:** A statistical claim is a claim about a model, not about the data: name the inferential frame (frequentist or Bayesian), state the likelihood/priors and the assumptions they encode, check the computation converged (R-hat and effective sample size for MCMC, not eyeballed traces), and report the estimate as an interval -- a p-value or a point estimate alone is not the result (M3.11).

### `certified-computation` — Certified computation (exact or independently re-derived) · 可核验计算（精确或独立重算）

- **Fires when · 触发条件:** domain ∈ {geometry-topology} (领域)
- **Modules · 关联模块:** M3, M6
- **Why · 理由:** A computed invariant (a Groebner basis, a homology group, a knot polynomial, a triangulation's property) is a claim resting on an algorithm: run it under exact or certified arithmetic (or a recorded precision), handle degeneracies rather than inheriting floating-point noise, and re-derive the result independently or on a perturbed input -- an unchecked CAS/solver output is a conjecture (M3.12).

### `ontology-as-contract` — Ontology as contract · 本体即契约

- **Fires when · 触发条件:** domain ∈ {knowledge-management, digital-humanities} (领域) OR artifact ∈ {knowledge_base} (产物)
- **Modules · 关联模块:** M3, M4
- **Why · 理由:** A knowledge base is only as trustworthy as the schema it was built against. Declare the entity types, relation directions and allowed values *before* extraction, then let every acceptance check decide against that schema: a candidate that cannot be typed is a defect to record, not a finding to keep. The schema is the gate (M3); its version is part of the artifact (M4.11).

### `entity-resolution` — Entity resolution with recorded aliases · 实体归一（别名留痕）

- **Fires when · 触发条件:** domain ∈ {knowledge-management, digital-humanities, humanities} (领域) OR artifact ∈ {knowledge_base} (产物)
- **Modules · 关联模块:** M4
- **Why · 理由:** One canonical id per entity, aliases recorded as aliases against that id, and never a merge that invents a claim the source did not make (M0.4). Same name / different entity is the normal case in historical and biographical material: when the evidence cannot decide a merge, the pair goes to a human gate rather than being averaged into one record (M4.12). The same resolution done offline pays twice: an entity-level corpus map built once by resolving recurring mentions across documents is shared across queries instead of rediscovered per query, and outperforms per-query navigation alternatives while using fewer tokens.

### `evidence-bounded-generation` — Evidence-bounded generation · 输出侧证据约束

- **Fires when · 触发条件:** artifact ∈ {knowledge_base} (产物) OR domain ∈ {knowledge-management, digital-humanities} (领域) OR grounding ∈ {required} (来源要求)
- **Modules · 关联模块:** M3, M4
- **Why · 理由:** Reading material is untrusted input (M4.5); writing it down is a provenance claim (M4.4). When a system answers *about* a corpus or a knowledge base, every named assertion (person, place, date, number, relation) carries a pointer into the evidence, and "the sources do not support an answer" is a complete, acceptable output. External-knowledge completion is the failure this bars: an answer that is fluent, plausible and nowhere in the material (M4.13). The pointer itself must be checked for three distinct failures -- dangling, stale (resolving to a superseded or retracted entry) and unsupported -- and must terminate at the source span, not at a generated summary (M4.16).

### `schema-evolution` — Versioned schema evolution · 模式演化（版本化迁移）

- **Fires when · 触发条件:** domain ∈ {knowledge-management, digital-humanities} (领域) OR artifact ∈ {knowledge_base} (产物)
- **Modules · 关联模块:** M4, M7
- **Why · 理由:** A knowledge base outlives the ontology it was born with. Treat a schema change as a migration: a declared version, a re-validation of the affected slice, and a record of which schema version each assertion was extracted under; deprecate terms by redirect rather than deletion so old ids stay resolvable. Change governance (M7) applied to meaning, not only to code; evolution is where a knowledge base silently becomes two.

### `gap-seeking` — Self-model and gap-seeking · 自我模型与缺口探测

- **Fires when · 触发条件:** horizon ∈ {multi_session} (时间跨度)
- **Modules · 关联模块:** M5
- **Why · 理由:** A system that cannot name what it does not cover rediscovers the same gap every round; self-attributed strength is testimony, not evidence, so a claimed capability needs an external check and an uncovered direction needs a bounded, budgeted probe.

### `prose-polish` — Prose polish: write for the reader · 文字润色：为读者而写

- **Fires when · 触发条件:** artifact ∈ {document} (产物)
- **Modules · 关联模块:** M4
- **Why · 理由:** Model prose fails readers while staying factually true (hedge stacking, stock phrases, list-ification, wrong register, translationese), so readability and register need a gate separate from truth: mechanical checks may reject, never approve, and a reader decides whether it sounds human.

### `expression-design` — Expression design: choose the form before the words · 表达设计：先定形式，再定措辞

- **Fires when · 触发条件:** artifact ∈ {document, dataset} (产物)
- **Modules · 关联模块:** M4
- **Why · 理由:** Correct content can still fail because it was given the wrong form: a manual organised around the author's outline, a table that hides the decisive comparison, a diagram that silently drops a qualifier. The content unit (claim, relation, procedure, quantity, change over time) and the reader's task (learn, do, look up, understand) select the form - tutorial, how-to, reference, explanation, then prose/table/diagram/chart/notation/animation/sound - and a form change may change what the reader can check but never what is claimed (M4.10). Prose polish repairs sentences; this decides whether the information should be a sentence at all.

### `component-ablation` — Component ablation: a module earns its place · 组件消融：组件须自证其位

- **Fires when · 触发条件:** horizon ∈ {multi_session} (时间跨度) and verifiability ∈ {high} (可验证性)
- **Modules · 关联模块:** M3, M5
- **Why · 理由:** A harness grows by accretion and never shrinks, so module count starts reading as capability. Retention is not contribution: presence during success does not show causation, and model, artifact and harness effects are confounded. The place of a module is decided by a single-unit ablation against the per-task median over ablations, reported on two axes (performance and token cost) and evaluated on a held-out ladder; removing a unit can raise cost, and an all-pruned baseline that still scores is a statement about task coverage.

### `model-portfolio-discipline` — Model portfolio: choose per stage, measure on your own task · 模型组合：按阶段选型，在自己的任务上测量

- **Fires when · 触发条件:** domain ∈ {model-selection} (领域)
- **Modules · 关联模块:** M3, M4, M7
- **Why · 理由:** A model choice is a measurement, not a rank. Vendor tables compare different models at different effort levels, an alias silently moves to a new snapshot, and a safety policy can re-route the request to another model, so a leaderboard position does not transfer to your task. Declare the requirements matrix (quality, latency, cost, licence, privacy), pick a portfolio per stage rather than one model for the whole job, run a minimal fit-for-task evaluation on your own hold-out at a declared effort, and pass a hard decision gate with requested/served model ids, versions and effort settings recorded (M4.17). A tie goes to the cheaper tier; a change of tier or effort re-opens the evaluation. Compare on both sampling axes: post-training can sharpen single-shot accuracy (pass@1) while shrinking solution coverage (pass@K), so a base model with a light inference harness may be the better portfolio member when test-time budget is available.

### `research-question-generation` — Research-question generation (ideation with calibrated taste) · 研究问题生成（带校准品味的构思）

- **Fires when · 触发条件:** artifact ∈ {plan} (产物)
- **Modules · 关联模块:** M2, M3, M4, M5
- **Why · 理由:** Fills the P18 hole (plan-artifact tasks had no dedicated capability); the taste-calibration duty binds where a human-expert consensus is available. The ideation discipline, from three first-party studies: (a) oversample-then-filter with DECLARED criteria (After42: 3% -> 33% interesting share); (b) solve-refine-critique -- 'solving is essential to asking good questions', and per M5.14 the failed solve attempts are the signal; (c) novelty and feasibility are scored SEPARATELY (Stanford: novelty up, feasibility flat; overall score barely correlates with feasibility, r=0.097); (d) model-judge taste must be CALIBRATED against expert consensus where available (agreement below human-human baseline without criteria; 65-80% recall with criteria + ensembles; 'cannot yet replace human research taste') and personalization comes from behavioral feedback, not stated preferences; (e) diversity is tracked -- generation plateaus (4000 seeds -> 200 unique) and inference-time scaling bottleneck on duplicates; homogenization is a named risk. Humans gate the final selection (M0.4/M0.8).

### `source-criticism` — Source criticism (historical method) · 史源批判（史学方法）

- **Fires when · 触发条件:** domain ∈ {history} (领域)
- **Modules · 关联模块:** M3, M4
- **Why · 理由:** P27's judged discriminator for the history domain (史源批判·断代显式·沉默入账): every historical claim carries its source's position in the primary/secondary/report hierarchy; independent witnesses are corroborated before a claim is asserted; dating is explicit (a claim without its period is unanchored); silence in the sources is recorded as an evidence state, not skipped — 'the material is silent' is a valid result (M4.13's historical form). Content sourced in review/basic-disciplines-schools-2026-10.md.

### `argument-reconstruction` — Argument reconstruction (philosophical method) · 论证重构（哲学方法）

- **Fires when · 触发条件:** domain ∈ {philosophy} (领域)
- **Modules · 关联模块:** M3, M4
- **Why · 理由:** P27's judged discriminator for the philosophy domain (论证重构·立场声明·反例坦诚): arguments are reconstructed in explicit premise-conclusion form before evaluation; the author's own stance is declared rather than smuggled; counterexamples are engaged honestly (the strongest version of the opponent's argument is stated before it is answered). Content sourced in review/basic-disciplines-schools-2026-10.md.

### `concept-definition` — Concept-first case discipline (political-science method) · 概念先行的案例纪律（政治学方法）

- **Fires when · 触发条件:** domain ∈ {political-science} (领域)
- **Modules · 关联模块:** M3, M4
- **Why · 理由:** P27's judged discriminator for the political-science domain (概念界定·方法声明·案例选择留痕): concepts are defined before cases are selected (concept stretching is the failure mode); the method is declared with its assumptions (M3.13's political-science form); case selection is logged with its rules so the selection itself is auditable. Content sourced in review/basic-disciplines-schools-2026-10.md.

### `safety-argumentation` — Safety argumentation (AI-safety gate structure) · 安全论证（AI 安全门禁结构）

- **Fires when · 触发条件:** domain ∈ {ai-safety} (领域)
- **Modules · 关联模块:** M3, M6
- **Why · 理由:** P29's judged discriminator for the ai-safety domain (L0-L5 安全论证门禁结构): the safety property and threat model are stated before capability claims are tested (M3.10 instruments), red-team attempts are logged with their coverage (M3.15's precision/recall form), and 'the model refused' is distinguished from 'the capability is absent'. Content sourced in review/interdisciplinary-frontier-domains-2026-10.md.

---

## Evolution · 演化

This document is **generated**, so it evolves with the project: add or tune a capability by editing `data/capabilities.json` and re-running `harness capabilities --write` (the test suite also guards it for drift). The self-evolution loop may *propose* new capabilities from observed projects, but the change is **human-gated and reversible** (M0.4/M0.8). · 本文档自动演化：改 SSOT 后重生成即可；自我演化循环只**提案**新能力，交由人类把关（M0.4/M0.8）。

## See also · 参见

- Rule table + feature vocab: [`reference/derivation-rules.md`](reference/derivation-rules.md).
- Core modules M0–M8: [`core/00-index.md`](core/00-index.md).
- Whole-factory map (modules · capabilities · domains · CLI): [`HARNESS-MAP.md`](HARNESS-MAP.md).
- Tool catalog: [`review/harness-index.md`](review/harness-index.md) (`harness catalog`).
