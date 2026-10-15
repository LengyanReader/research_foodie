# Harness capabilities · Harness 能力总览

> **Generated** from `src/harness_factory/data/capabilities.json` + `modules.json` — **do not edit by hand**; run `harness capabilities --write` (also refreshed by `harness catalog --write`) to regenerate.
> **生成文档**：由上述 SSOT 生成，**请勿手改**；用 `harness capabilities --write` 重新生成（`harness catalog --write` 亦会同步刷新）。

**13 capabilities · 9 modules (M0–M8)**

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

---

## Evolution · 演化

This document is **generated**, so it evolves with the project: add or tune a capability by editing `data/capabilities.json` and re-running `harness capabilities --write` (the test suite also guards it for drift). The self-evolution loop may *propose* new capabilities from observed projects, but the change is **human-gated and reversible** (M0.4/M0.8). · 本文档自动演化：改 SSOT 后重生成即可；自我演化循环只**提案**新能力，交由人类把关（M0.4/M0.8）。

## See also · 参见

- Rule table + feature vocab: [`reference/derivation-rules.md`](reference/derivation-rules.md).
- Core modules M0–M8: [`core/00-index.md`](core/00-index.md).
- Tool catalog: [`review/harness-index.md`](review/harness-index.md) (`harness catalog`).
