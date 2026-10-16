# Capability flow · 双向能力流

> The loop that makes this repo **learn from every task** and every task **get stronger from the
> repo**. Two directions, one contract: **concretize** factory capabilities *into* the task's own
> directory; **distill** the generalizable patterns back into the factory — observe-only, human-gated.
> 本仓库与具体任务之间的**双向闭环**：**下放（concretize）**把通用能力落到任务/项目自己的目录；
> **回流（distill）**把具有通用性的模式提炼回本仓库。回流只**提案**、人类把关（M0.4/M0.8）。

**Updated:** 2026-10-16 · Load via `harness skill capability-flow`.

---

## 中文速览

本仓库和具体任务的关系是**双向**的，这是它区别于普通脚手架模板的核心：

- **方向一｜工厂 → 任务（具体化 / concretize）**：给一个任务推导出 harness 时，**同时**在任务/项目自己的目录下写一份**任务本地能力台账** `.harness/capabilities.local.md`，记录「这次用了哪些能力、在本任务里如何具体落地、还缺什么」。它保存在**任务/项目自己的目录**，随任务走，不回流、不越界。
- **方向二｜任务 → 工厂（提炼 / distill）**：任务结束后，从本地台账与 case 里抽出**具有通用性**的模式（反复出现的痛/招/tool），以**提案**形式回流到 `data/capabilities.json`（或 `core/`、`templates/`）。**只写入 `updates/`（gitignored），绝不自动合并**；由人类审批（M0.4/M0.8）。

一句话：**具体化的留在任务里，通用化的提案给工厂。**

---

## Direction 1 — Concretize (factory → task) · 方向一：具体化

When a harness is derived for a task, the emitter writes a **task-local capability ledger** next to the
harness, in the task/project's own directory:

```
<task-or-project>/.harness/capabilities.local.md
```

It is pre-seeded with the capabilities that fired for *this* task (from `.harness/manifest.json`) and a
schema to **concretize** each one — i.e. record *how this capability is realised here*, not the generic
definition:

| field | meaning |
|---|---|
| capability | the id from `data/capabilities.json` (generic) |
| local realisation | the concrete artefact/step/parameter this task uses (e.g. "gate = `pytest -q` on the 3 CI jobs") |
| evidence | file / command / metric that shows it is actually in place |
| gap | what is still missing for this task, and the cheapest next step |
| generalisable? | `no` (task-specific) / `maybe` (could help others) |

**Boundaries.** The ledger lives *inside the task*; it never edits this repository. It is the *local*
half of the loop. Anything that is task-specific stays here and is never pushed upstream.

An agent maintains it in place: when a capability is concretised, added, or found insufficient, it
appends a row (append-only) and updates the `gap` column. This is the durable, reviewable trace of
"what this task's harness actually is".

## Direction 2 — Distill (task → factory) · 方向二：提炼回流

At session end (M5 self-evolution loop; the `learn`/`evolve` path), scan the local ledger and the
project `case` for patterns that **survive removal of the originating project** (the generalisation
rule). For each `generalisable: maybe` item, emit a **proposal**, never a direct edit:

```
harness learn  --project <task> --goal "<goal>"     # record the case (observe-only)
harness evolve                                      # audit signals -> proposals in updates/
harness evolve --dry-run                            # inspect without writing
```

Proposals land in `updates/` (gitignored) with the dedicated fields the review gate needs:

| field | required |
|---|---|
| impact scope | which capability/module/doc would change |
| evidence | observed in ≥2 independent tasks (file/command/metric) — else mark `needs-evidence` |
| affected files | exact paths |
| verification plan | how the change would be checked |
| reversibility | how to revert |
| risk | what could regress |

A human then moves it `proposed → reviewing → approved/rejected/deferred → applied` (M0.8/M0.9).
**Automation never merges into `data/`, `core/`, `domains/`, or `templates/`** (M0.4).

---

## The loop in one picture · 一图看懂

```
                 derive / init                         learn / evolve
   ┌──────────┐  ───────────────▶  ┌───────────────┐  ───────────────▶  ┌──────────────┐
   │  factory │                    │ task/project  │                    │  updates/    │
   │ (generic │  ◀───────────────  │  .harness/    │  ◀───────────────  │ (proposals)  │
   │  caps)   │   promotion (human-│ capabilities  │   distillation      └──────┬───────┘
   └──────────┘   gated, approved) │  .local.md    │                     human review
         ▲                          └───────────────┘                            │
         └──────────────────── approved proposals enrich caps ──────────────────┘
```

- **Left → right** = concretize (task-specific; stays in the task).
- **Right → left** = distill (general; proposed, reviewed, then merged by a human).

## Why both directions · 为什么必须双向

- **One-way templates rot.** A factory that only emits never learns which emissions failed.
- **One-way harvesting over-generalises.** Without the *local* ledger there is no honest evidence of what actually happened in a task, so distillation becomes guesswork (violates M0.1/M0.2).
- **Separation keeps truth.** Task-specific content never pollutes the generic catalogue; only patterns that survive project removal are proposed (the generalisation rule).

## See also · 参见

- [`reference/capability-router.md`](capability-router.md) — which capability a situation needs.
- [`core/06-self-evolution.md`](../core/06-self-evolution.md) — the signal → audit → mutation → journal engine (M5).
- [`core/08-change-governance.md`](../core/08-change-governance.md) — SSOT, reviewable diffs, human gate (M7).
- [`SKILL.md`](../SKILL.md) §Mutual learning.
