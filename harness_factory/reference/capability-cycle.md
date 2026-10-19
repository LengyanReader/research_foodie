# The capability cycle · 能力演化循环

> **What this is.** `core/06` (**M5.10**) says a capability round is a *mechanism*, not a habit: a round
> is recorded, audited against a definition-of-done, and its non-additions are logged with a reason and a
> revisit trigger. This is the procedure — where a round's inputs come from, how to rank candidates, what
> "done" means *mechanically*, how to record the round, and how to close it. Load it whenever you are
> about to grow, deepen or refresh this factory's capability set (a "P-cycle"), or when you need to know
> *why* something was deliberately not added. · 本文把 **M5.10** 落地：一轮能力拓展/深化/更新/演化
> 从哪取输入、如何排序候选、何谓**可核验的完成**、如何登记、如何收口。凡要扩展本仓库的能力集，
> 或要查「某事为何被有意不做」时，读本文。
> Same paths as every factory doc — these are **the harness-factory's** files, not your project's.

**Updated:** 2026-10-19 · Load via `harness skill capability-cycle`. SSOT: `data/cycles.json`.
Commands: `harness cycle` · `harness cycle audit` · `harness cycle roadmap` · `harness cycle dod` ·
`harness cycle show <id>`. Companions: `reference/capability-flow.md` (the *per-task* flow),
`reference/capability-router.md` (find a capability from a situation), `../tasks/PLAN.md` (the naming
authority for cycle ids).

---

## 中文速览

**能力增长是轮次，不是手感。** 一轮（一个 cycle）做三件事：**(1) 读缺口面**——`harness cycle audit` 列出缺
路由行 / 缺溯源行 / 缺门禁 / 子句未锚定的能力；**(2) 排序并切片刻**——一次只做 2–4 个可核验的切片，优先级
按「能否判别」而非「听起来重要」；**(3) 过完成定义并登记**——`data/cycles.json` 记录本轮新增（能力/学科/
子句/文献/目录条数），并按**七轴完成定义**逐项过关；**有意不做**的事写进 `roadmap`，必须带**理由**与
**重访触发条件**。**关键区分**：`refresh` 管的是*情报实体*，`evolve` 管的是*对实体的变异提议*，
`capability-flow` 管的是*单次任务的双向流动*，本文管的是**能力集自身的轮次**——四者不重叠。
**反模式**：只写文档不接 SSOT、开了轮次永不收口、把「有意不做」悄悄丢掉、为新而新（重复登记 = 应合并，非新增）。

---

## How to use · 用法

1. **Read the surface, not your mood.** Run `harness cycle audit`. The *gaps* section is the input list; the *problems* section must be empty (it is hard).
2. **Rank by discrimination.** A candidate earns a slot only if it fires on something no existing capability fires on, or closes a recorded gap. Volume is not a virtue (M0.5).
3. **Cut 2–4 slices.** One slice = one checkable change (a clause, a doc, a catalog block, a guard). Anything that cannot be checked this round is a `roadmap` entry, not a slice.
4. **Implement the wiring, not just the prose**: clause → SSOT → router row → provenance row → load index → guard.
5. **Run the definition-of-done**: `harness cycle audit` must be green, `python -m unittest discover -s tests` must pass.
6. **Record the round** in `data/cycles.json` (`status: done`), regenerate generated views, commit.
7. **Defer honestly**: every "not now" goes to `roadmap` with `reason` + `revisit_when` + `source`.
8. **Close it.** `active` is a state you pass through, not a place to live.

---

## 1. What a round is — and what it is not

The factory already has three adjacent mechanisms. A round is the fourth, and the boundary matters (M0.5):

| mechanism | unit | input | output | gate |
|---|---|---|---|---|
| `harness refresh` | one *entity* scan | feeds / watchlist | new or changed entities in `updates/` | human review, `refresh-apply` |
| `harness evolve` | one *mutation proposal* over tracked entities | `snapshot` + `audit` | `updates/evolution/*` proposals | accept list, `evolve-apply` |
| `reference/capability-flow.md` | one *task* | what the task taught | a distill proposal back into the factory | human confirmation |
| **a capability cycle** (`M5.10`) | **one *round* of the capability set** | the gap surface + recorded cues | new capabilities / domains / clauses / docs, **and** an audited record | `harness cycle audit` + tests |

So: `refresh`/`evolve` ask *"what changed in the world?"*; a round asks *"what should this factory be able to do that it cannot do yet — and is the addition actually complete?"* A round usually *consumes* `evolve` output; it does not replace it.

A round is **not** a prose milestone. If the only artifact is a paragraph in `PLAN.md`, the round did not happen — `data/cycles.json` is the record, and `PLAN.md` remains the narrative plan of record.

---

## 2. The definition-of-done (seven axes)

The bar is **data**, in `data/cycles.json` → `definition_of_done` (read it with `harness cycle dod`). `harness cycle audit` checks the hard axes and *reports* the soft ones.

| axis | severity | means | how it is checked |
|---|---|---|---|
| **registered** | hard | every id the round claims exists in the live SSOT; a claimed clause is anchored | `added.capabilities ⊆ capabilities.json`, `added.domains ⊆ domains.json`, `added.references ⊆ references.md`, clause anchored in its own `core/` doc |
| **discriminator** | hard | the trigger is one the engine can actually evaluate | mirrors `capabilities._cond_matches`: `any` · `min_horizon` · feature axes · `domain`; an undeclared predicate silently never fires |
| **clause** | hard | a label lives in *its* module (`M2` → `core/03`, …) | heading `## M0.4 …` or a bold clause title `**… (M3.11).**` anchors it |
| **guard** | soft | a test fails if the wiring is removed | the capability id is named under `tests/` |
| **provenance** | soft | a first-party source backs the clause | the clause appears in `sources/source-map.md` |
| **router** | soft | findable from a *situation* | the capability appears in `reference/capability-router.md` |
| **reachable** | soft | one instruction reaches the doc | the doc is listed by `harness skill` |

Two notes on honesty:

- **Provenance is per clause, not per capability.** A capability is a *composition* of module clauses; requiring a separate primary source for each one would invite citation padding. The clause carries the source.
- **`discriminator` does not mean "unique `when`".** Capabilities are *lenses* and are designed to co-fire (`capabilities.match` returns every match). The failure it guards against is a trigger the engine cannot evaluate, or a duplicate registration that adds nothing (same `when`, `modules` **and** title = consolidate, don't add).

---

## 3. Inputs — where the next round comes from

| input | what it tells you | where |
|---|---|---|
| **gap surface** | missing router rows / guards / provenance; unanchored clauses | `harness cycle audit` (soft section) |
| **recorded cues** | gaps the last round already named | `review/integration-map-*.md` §3 |
| **assessment** | structural gaps (self-evolution without evidence, memory spec-only, CI claims) | `../tasks/ASSESSMENT.md` §A.3 |
| **signals + cases** | what real runs actually stumbled on | `<kb>/updates/signals.jsonl`, `updates/cases.jsonl` |
| **frontier staleness** | what the world moved past | `harness standard audit`, `harness evolve` audit |
| **a standing ask** | what the operator keeps needing | `AGENTS.md`, the current `PLAN.md` milestone |

A round must be able to say *which* input it answered. "It seemed like a good idea" is not an input.

---

## 4. Rank and slice

Rank with three questions, in order:

1. **Does it discriminate?** Would a new capability fire on a task vector that no existing one fires on? If not, it is either a *deepening* of an existing capability (edit it) or a **non-addition** (record it). The 8-axis feature vector is the constraint: a capability the vector cannot distinguish is prose, not mechanism.
2. **Does it close a recorded gap?** Named in the audit, the assessment, or the integration map. A gap with a source beats a gap without one.
3. **Is it cheap to verify?** A slice whose result can be checked this round beats a slice that needs a future round to prove itself.

Then cut **2–4 slices**, each one checkable change:

- a **clause** (an invariant the round answers to),
- an **SSOT block** (data, not prose),
- a **doc** (the procedure a reader needs),
- a **guard** (the test that fails if it drifts),
- optionally a **generated view** (map / index) and a **wiring row**.

Anything larger is two rounds. Anything unverifiable is a roadmap entry.

---

## 5. Implement — the wiring checklist

```
[ ] clause        core/06 or the owning module: the invariant, with its label
[ ] SSOT          data/*.json: the capability / domain / outlet / cycle entry
[ ] provenance    sources/source-map.md: clause -> first-party source
[ ] router        reference/capability-router.md: situation -> capability
[ ] load index    skill.py + SKILL.md: so `harness skill` reaches the doc
[ ] guard         tests/: fails if the wiring is removed
[ ] views         harness map --write / harness catalog --write
[ ] record        data/cycles.json: the round, status, added ids
[ ] close         harness cycle audit green; tests green; commit
```

The order is not ceremonial: each line is one of the seven axes. Doing them in this order means the audit passes on the first run instead of after a scavenger hunt.

---

## 6. Record — the `cycles.json` shape

```jsonc
{
  "id": "P11",
  "date": "2026-10-19",
  "status": "done",                 // done | active | planned
  "title_en": "...", "title_zh": "...",
  "sources_groups": ["K"],
  "slices": ["..."],                 // what shipped, one line each
  "added": {
    "capabilities": ["..."],         // ids, re-checked against the SSOT
    "domains": ["..."],
    "clauses": ["M4.10"],            // labels, re-checked against core/
    "references": ["R120", "..."],   // ids, re-checked against references.md
    "catalog_delta": 0,
    "instruments_delta": 0,
    "outlets_delta": 68
  }
}
```

Counts (`catalog_delta`, `outlets_delta`, …) are for scale; ids are for verification. A round that only moved counts can say so — a round that claims ids must be able to prove them.

---

## 7. Defer — don't drop

A deferral is a **decision**, and it has three fields:

| field | question it answers | example (D3) |
|---|---|---|
| `reason` | why not now? | the feature vector has no qualitative axis, so it could not discriminate |
| `revisit_when` | what would change the answer? | the vector gains an affordance that distinguishes qualitative designs |
| `source` | who recorded the gap? | `review/integration-map-2026-10.md` §3 #1–2 |

`harness cycle roadmap` prints them. The audit fails a deferral that is missing `reason` or `revisit_when` — a deferral with no trigger is indistinguishable from a thing that was forgotten.

**Closing one.** When a roadmap item ships, its `status` becomes `done` and it records `done_in`
(e.g. `"P12 (reference/cross-language.md §7)"`); the trigger is then no longer required — a closed item
is not a deferral. The audit enforces that shape: open work must say *why* and *when*, closed work must
say *where* (P12 made this distinction when P12.5 shipped).

---

## 8. Close the round

A round closes when all three hold:

1. `harness cycle audit` → **OK** (no hard problems);
2. `python -m unittest discover -s tests` → green;
3. `data/cycles.json` says `done`, the added ids are real, and the non-additions are in `roadmap`.

Then regenerate the views and commit. If a slice could not be finished, it moves to `roadmap` with a trigger — the round still closes.

**Worked example.** P13 (this round) opened by asking whether a mechanism for rounds existed; the answer was no, so the round built one, then *used* it: the first `audit` found that `M2.10`, `M2.11`, `M3.10` and `M8.10` were cited in review docs but never anchored in `core/`, and the round anchored them. That is the intended shape — the mechanism's first act is to find something real.

---

## Deliberate non-entries · 有意不收录

- **No second plan of record.** `data/cycles.json` records what happened and what was deferred; `tasks/PLAN.md` remains the narrative plan. The audit checks the former, not the latter — keeping one authority for each (M0.5).
- **No automatic mutation.** The round ranks and drafts; humans accept (M0.4, M0.8). There is no `cycle --apply`.
- **No per-capability provenance requirement.** Provenance stays at the clause level (§2).
- **No "capability count" target.** A round that adds zero capabilities and closes a gap (P11, P9) is a success; a round that adds five without wiring is not.

---

## Anti-patterns

- **Prose-only round.** A milestone is written, nothing enters the SSOT, no guard exists — the next round rediscovers the same gap.
- **Round without closure.** `active` forever, never audited.
- **Silent deferral.** "Not now" with no reason and no trigger; the decision evaporates.
- **Novelty addition.** A capability that duplicates an existing trigger, module and title: that is a consolidation (M0.5), not a new capability.
- **Wiring after the fact.** Shipping the doc first and promising "tests later" — the audit will (correctly) keep failing.
- **Counting capabilities as progress.** The metric is *checked wiring*, not rows.

---

## See also

`../core/06-self-evolution.md` (M5.10, and the mutation vocabulary it builds on) · `capability-flow.md` (the per-task flow this round consumes) · `capability-router.md` (routing by situation) · `requirement-refinement.md` (R0–R5, when the ask itself is vague) · `../tasks/PLAN.md` (cycle ids and narrative milestones) · `../tasks/ASSESSMENT.md` §A.3 (structural gaps) · `../review/integration-map-2026-10.md` §3 (recorded cues).
