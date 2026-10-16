# Requirement refinement · 需求精炼

> The protocol an agent runs **before executing**: restate the ask more clearly / more completely /
> more deeply, actively strengthen · correct / adjust / expand / deepen it, surface the uncertainties,
> talk to the human, accept interruption and correction at any time, and only proceed after explicit
> confirmation. Nothing here writes task substance (M0.4) — it only sharpens, proposes, and converges.
> 需求精炼协议：**先澄清、再拔高、后收敛**。把一句话需求改写得更清楚/更完备/更深入、主动纠偏与扩充、
> 暴露不确定点、与人互动确认，**得到明确确认后才执行**；只做精炼与提案，绝不编造任务实质（M0.4）。

**Updated:** 2026-10-16 · Part of the L0 (read-and-reason) surface. Load via `harness skill requirement-refinement`.

---

## 中文速览

一次性复述需求是不够的。真正的「读懂任务」是一个**六步协议**：**R0 复述 → R1 提升野心 → R2 约束分类 → R3 提候选版本 → R4 交互确认 → R5 收敛执行**。每一步都产出**可被用户当场纠正**的东西；在用户**明确确认**之前，只提案、不落盘、不动手。协议默认给模型一个**专家人格**（本领域顶尖/一线/导师），但人格只改变「怎么做」，绝不编造事实（M0.4）。这套协议与 `core/01`–`core/09` 一致：它服务 M0.3（先定义完成）、M0.4（只观察/提案）、M0.8（人类门禁）。

---

## The six steps · 六步协议

| step | name | what the agent produces | gate |
|---|---|---|---|
| **R0** | Restate · 复述与澄清 | One-sentence plain restatement + an explicit list of what is **known / assumed / unknown**; the decision it serves and the audience | If two readings are both plausible, **stop and ask** (M8) |
| **R1** | Elevate · 提升野心 | An **Elevated (stretch)** and a **Moonshot** reading of the goal, each with *why it is worth more* — "what would matter if the mechanical steps were handled?" | Never silently substitute a grander goal for the user's; propose, label clearly |
| **R2** | Classify constraints · 约束分类 | Every constraint labelled **Hard** (non-negotiable) / **Soft** (preference) / **Assumed** (self-imposed, unverified). Assumed constraints are converted to *pending questions*, not treated as facts | Do not drop a Hard constraint; do not obey an Assumed one without flagging it |
| **R3** | Offer candidates · 候选版本 | **3 named readings** of the same ask: `MVP` (smallest verifiable increment) · `Elevated` (stretch) · `Exploratory` (moonshot/learning goal). Each with scope, cost, and what it would prove | The user may pick one, mix, or reject; the agent must be able to state each in one line |
| **R4** | Confirm · 交互确认 | Ask the user to choose / amend; accept interruption and correction at any time; re-run from R0 on a material change | **No work begins until the user explicitly confirms** (M0.8) |
| **R5** | Converge · 收敛执行 | Lock the confirmed reading into `tasks/PLAN.md` (goal + DoD + first move), then execute | "Done" is a verified state (M0.3) |

> **Why this order.** Clarifying alone produces a *clearer small goal*; clarifying then elevating produces a *clearer goal that is worth more*. Elevating before converging is what stops a harness from tooling an under-aimed task (see `review/ambition-and-agency.md`).

---

## Elevation prompt (R1) · 提升野心的问法

Ask these four questions about the *task*, then rewrite the ask — do **not** role-play a persona:

1. What would a **top practitioner in this field** do that the user is *not* asking for?
2. What **rawest material** would they start from (raw data, primary sources, the real instrument) rather than a summary or a toy substitute?
3. Which specific **methods / instruments / tools** do they actually use, and can we run one of them to get feedback immediately?
4. What, **other than the agent or the user**, would show the result is right (an outside check, a benchmark, a replication)?

The rewritten ask becomes the `Elevated` candidate in R3. Keep the original as the `MVP` candidate — the user may still prefer it.

---

## Constraint classification (R2) · 约束分类

| label | meaning | default action |
|---|---|---|
| **Hard** | physically/logically non-negotiable, or explicitly so stated (budget cap, regulation, platform) | design around it; never remove silently |
| **Soft** | a preference or habit; could be traded for value | surface the trade-off; let the user decide |
| **Assumed** | the agent (or the brief) *inferred* it; never verified | **question it**; convert to a pending clarification |

> An **Assumed** constraint treated as Hard is the most common cause of an under-ambitious solution.

---

## Persona by domain (auto) · 自动代入人格

When the user does not name an expert persona, **assume one from the task's domain** — a top-tier / leading / world-class practitioner *and* a mentor for it — and say which one you assumed. The persona changes *method and standards*, never *facts*: it must still obey M0.1 (truth), M0.2 (sources), M0.4 (no fabrication). The domain → persona pairing comes from `domains/<name>/README.md`.

---

## Interaction contract · 交互契约

- **Propose, don't presume.** Every step before R5 is a proposal the user can reject or redirect.
- **Interruptible.** A correction at any step restarts the protocol from the step it invalidates (usually R0).
- **One question batch.** Collect clarifications (R0/R2) into a single, prioritised batch rather than a drip (M8).
- **Explicit confirmation, not implied.** Silence is not consent for R5; the user's "go" is.
- **Budget-aware.** If no human is reachable, proceed with the labelled `MVP` reading and record the assumption in `tasks/PROGRESS.md` — never invent scope (M0.4).

---

## Where it is wired · 落点

- Emitted `AGENTS.md` carries a **Requirement refinement** section referencing this file.
- Emitted `tasks/PLAN.md` records the confirmed **reading** (`MVP` / `Elevated` / `Exploratory`), the **constraint classification**, and the **first move**.
- Capability `ambition-elevation` (`data/capabilities.json`) fires for non-`one_shot` work and annotates the plan.
- Source: F. Rieseberg, *How to be more ambitious* (2026) — see `review/ambition-and-agency.md` and `review/references.md` R80.

## See also · 参见

- [`reference/capability-router.md`](capability-router.md) — locate the capability a situation needs.
- [`reference/capability-flow.md`](capability-flow.md) — the local ⇄ factory capability loop.
- [`core/09-collaboration-and-sessions.md`](../core/09-collaboration-and-sessions.md) — escalation & handoff (M8).
