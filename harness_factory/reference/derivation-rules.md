# Derivation rules · 推导规则（agent-readable mirror）

**Updated:** 2026-10-15 · Mirrors `src/harness_factory/derive.py` + `data/capabilities.json`.
**Purpose:** let a vibe-coding assistant (L0, no Python) derive a harness by reading rules, and let
the CLI (L1) stay explainable. 若可用 CLI，优先 `PYTHONPATH=src python -m harness_factory derive --task "…" --json`。

> 中文速览：本文件是 `derive.py` 规则表的 Markdown 镜像。给定**任务特征向量**，按下表选出**启用模块**，
> 再按 `data/capabilities.json` 标注**能力**。只做「分类/选择/标注」，绝不编造任务实质（M0.4）。

## 1. Feature vector · 任务特征向量

Classify the task into these closed vocabularies (rules; optional LLM may fill gaps):

| feature | values | meaning |
|---|---|---|
| `horizon` | `one_shot` · `session` · `multi_session` · `long_running` | time span of the work |
| `verifiability` | `high` · `medium` · `low` | can "done" be checked objectively? |
| `stakes` | `low` · `medium` · `high` | cost of error / irreversibility |
| `grounding` | `off` · `preferred` · `required` | need for primary sources |
| `artifact` | `code` · `document` · `dataset` · `knowledge_base` · `plan` · `mixed` | deliverable kind |
| `tool_surface` | `none` · `read` · `read_write` · `external` | what the task touches |
| `collaboration` | `solo` · `human_review` · `multi_agent` | who is involved |
| `domain` | full list in `data/domains.json` (e.g. `general` · `research` · `reading` · `knowledge-management` · `data-science` · `devops` · `model-selection` · …) | scenario |

## 2. Module rules · 模块规则

| Module | Enabled when | Key params |
|---|---|---|
| **M0** Meta-principles | always | — |
| **M1** Context | always | context policy |
| **M2** Long-running/memory | `horizon ≥ session` | `memory_depth` = session / durable (≥ multi_session) |
| **M3** Verification/gates | always | `gate_strictness` |
| **M4** Provenance | `grounding ∈ {preferred, required}` OR `artifact ∈ {document, dataset, knowledge_base}` | `provenance` |
| **M5** Self-evolution | `horizon ≥ multi_session` | `evolution_cadence` = per_session / periodic |
| **M6** Tools/skills | `tool_surface ≠ none` | `tool_surface` |
| **M7** Governance | always | commit policy |
| **M8** Collaboration | `collaboration ≠ solo` OR `stakes = high` | `collaboration`, `autonomy` |

**Derived parameters:**

- `gate_strictness`: `strict` if `verifiability = low` OR `stakes = high`; `relaxed` if `verifiability = high` AND `stakes = low`; else `standard`.
- `autonomy`: `low` if `stakes = high` OR `verifiability = low`; `high` if `stakes = low` AND `verifiability = high`; else `medium`.
- `memory_depth`: `session` if `horizon = session`; `durable` if `≥ multi_session`.
- `evolution_cadence`: `per_session` if `multi_session`; `periodic` if `long_running`.

Precedence: **explicit flags > LLM suggestion > rules > domain defaults**. Record `source` = `rules|llm|flags|mixed`.

## 3. Capability map · 能力映射

Capabilities are the data-driven requirement layer (`data/capabilities.json`); each entry is
`{id, when, modules, why}`. Matching capabilities **annotate enabled modules** and appear in the manifest —
they never enable a module the rule table did not. Current set:

| capability | fires when | modules |
|---|---|---|
| `baseline-discipline` | always | M0, M1, M7 |
| `verification-gate` | always | M3 |
| `resumable-memory` | `horizon ≥ session` | M2 |
| `traceable-sources` | `grounding ∈ {preferred, required}` OR `artifact ∈ {document, dataset, knowledge_base}` | M4 |
| `self-improving-loop` | `horizon ≥ multi_session` | M5 |
| `tool-use` | `tool_surface ∈ {read, read_write, external}` | M6 |
| `human-review-gate` | `collaboration ∈ {human_review, multi_agent}` OR `stakes = high` | M8 |
| `high-stakes-guardrails` | `stakes = high` | M3, M8 |
| `reproducible-experiments` | `domain ∈ {data-science, research}` AND `verifiability = high` | M3, M4, M5 |
| `long-horizon-autonomy-control` | `horizon ≥ multi_session` AND `stakes = high` | M2, M3, M8 |
| `frontier-standard` | `domain = excellence` OR (`verifiability = high` AND `horizon ≥ multi_session`) | M3, M5, M8 |
| `sandboxed-execution` | `tool_surface = external` OR `stakes = high` | M3, M6, M7 |
| `portable-skills` | `tool_surface ∈ {read, read_write, external}` | M6 |

Add a requirement by editing the JSON, not code. (`frontier-standard` = the highest-standard ratchet: measure against the best-known bar, raise monotonically, track the moving frontier — `domains/excellence/`.) A generated, always-current rendering of this table lives in [`../CAPABILITIES.md`](../CAPABILITIES.md) (`harness capabilities`).

## 4. Output contract · 输出契约

When emitting a harness (by CLI or by an L0 agent), produce at least:

```
AGENTS.md                     operating manual (task, features, modules, capabilities, hard rules, gates)
tasks/PLAN.md                 plan-first
tasks/PROGRESS.md             track-as-you-go
.harness/manifest.json        the HarnessPlan (task, features, capabilities, modules+reasons, files)
.harness/gates.md             hard/soft gates
.harness/PROVENANCE.md        derivation record (which rule/capability fired; mark unverified)
.harness/check.py             self-check gate
```

plus, conditionally: `.harness/ledger.md` (M2), `.harness/skills/README.md` + `.harness/skills/<name>/SKILL.md` (M6),
`.harness/decisions.md` (M8), `.harness/PROFILE.md` (when a project was profiled).

The M6 skill (`<name>` = `harness-<domain>`) is emitted in the [Agent Skills](https://agentskills.io/specification)
open format (`name` + `description` frontmatter, progressive disclosure) so it loads in any compatible harness.

**Gate:** no unrendered placeholders; every file listed in the manifest exists; every load-bearing
claim is sourced or marked `unverified`.

## 5. Mutual learning · 相互学习

A profiled project yields a **case** (`updates/cases.jsonl`): features + capabilities + modules.
`evolution` audits cases; a capability recurring across projects but absent from the registry becomes a
`missing_capability` proposal (human-gated). Projects teach the factory; capabilities from one project
become reusable options for others.
