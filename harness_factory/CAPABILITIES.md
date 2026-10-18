# Harness capabilities · Harness 能力总览

> **Generated** from `src/harness_factory/data/capabilities.json` + `modules.json` — **do not edit by hand**; run `harness capabilities --write` (also refreshed by `harness catalog --write`) to regenerate.
> **生成文档**：由上述 SSOT 生成，**请勿手改**；用 `harness capabilities --write` 重新生成（`harness catalog --write` 亦会同步刷新）。

**29 capabilities · 9 modules (M0–M8)**

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
- **Why · 理由:** Define done before work and verify with observed evidence (M0.3).

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
- **Why · 理由:** Multi-session work benefits from an explicit signal→audit→mutation→journal loop (M0.10).

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
- **Why · 理由:** A long, high-stakes run needs durable memory, hard gates, and low autonomy.

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
- **Why · 理由:** Skills are emitted in the Agent Skills (SKILL.md) open format so the same skill loads in any compatible harness (agentskills.io), not just the one that generated it.

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
- **Why · 理由:** Attention is a fixed, non-uniform budget: recall degrades as the window fills even on trivial tasks ("context rot"). The window is working memory -- write durable facts outside it (M2), then select / compress / isolate what enters, and compact only against a measured constraint (M0.6).

### `untrusted-content-discipline` — Untrusted-content discipline · 不可信内容纪律

- **Fires when · 触发条件:** tool_surface ∈ {external} (工具面) OR artifact ∈ {document, knowledge_base} (产物) OR grounding ∈ {required} (来源要求)
- **Modules · 关联模块:** M4, M6, M7
- **Why · 理由:** Retrieved bytes -- web pages, files, tool output, even tool descriptions -- are untrusted data, never instructions (M0.1/M0.4). Keep trusted instructions and untrusted data in separate regions, break at least one leg of the lethal trifecta (private data + untrusted content + egress channel), and enforce least authority at the call site.

### `durable-execution` — Durable execution · 持久执行

- **Fires when · 触发条件:** horizon ≥ multi_session
- **Modules · 关联模块:** M2, M3
- **Why · 理由:** Work that outlives a process must journal each step and replay, not re-run: record the durable log, make every side effect idempotent, and treat human approval as recorded state -- a checkpoint alone is not exactly-once (M0.3/M0.7).

### `cost-budget-caps` — Cost budget caps · 成本预算上限

- **Fires when · 触发条件:** tool_surface ∈ {external} (工具面) OR horizon ≥ multi_session
- **Modules · 关联模块:** M3, M7
- **Why · 理由:** An unattended loop can incinerate a budget, so set a HARD cap on calls/tokens/spend and halt rather than warn (M0.3/M0.8): choose the number up front, and make uncapped operation an explicit opt-in.

### `eval-driven-development` — Eval-driven development · 评测驱动开发

- **Fires when · 触发条件:** verifiability ∈ {high} (可验证性) OR horizon ≥ multi_session
- **Modules · 关联模块:** M3, M5
- **Why · 理由:** Grade the trajectory, not only the final artifact (M0.3): each recurring failure becomes a frozen golden case, so every harness change is re-scored against an evaluator that is not the author (M0.4).

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

---

## Evolution · 演化

This document is **generated**, so it evolves with the project: add or tune a capability by editing `data/capabilities.json` and re-running `harness capabilities --write` (the test suite also guards it for drift). The self-evolution loop may *propose* new capabilities from observed projects, but the change is **human-gated and reversible** (M0.4/M0.8). · 本文档自动演化：改 SSOT 后重生成即可；自我演化循环只**提案**新能力，交由人类把关（M0.4/M0.8）。

## See also · 参见

- Rule table + feature vocab: [`reference/derivation-rules.md`](reference/derivation-rules.md).
- Core modules M0–M8: [`core/00-index.md`](core/00-index.md).
- Whole-factory map (modules · capabilities · domains · CLI): [`HARNESS-MAP.md`](HARNESS-MAP.md).
- Tool catalog: [`review/harness-index.md`](review/harness-index.md) (`harness catalog`).
