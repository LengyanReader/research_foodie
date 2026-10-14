# Domain · Frontier standard / excellence · 最高标准域
> A capability that continuously measures work against the **best-known bar** and ratchets toward it.
> 一种能力：让产出**持续对标最高标准**并**只升不降**地逼近它。
**Updated:** 2026-10-14

---

## 中文速览
最高标准域回答一个问题：**「这件事的最高水平是什么样？我们现在差多少？怎么一步步逼近，且永不倒退？」** 它不生产领域内容，而是给任何任务加一层**标杆回路**：**L0 定标**（指名当前公认的最高标——SOTA 榜、顶级专家/产品范例、头名结果，并给出可核验依据）→ **L1 对标**（用同一把尺子给当前产出自评）→ **L2 差距审计**（逐维度：我们在哪、标杆在哪、差因何在）→ **L3 提升计划**（一次只拉最大的那块短板）→ **L4 提升并复测** → **L5 棘轮**（把已达到的分数固化为新下限，**绝不接受回退**）→ **L6 跟踪移动前沿**（标杆会前进，定期重新定标）→ **L7 记录**。**铁律：标杆必须可溯源、可核验（M4）；「是否达到最高标准」由人工确认（M0.8）；不得自我宣称优秀。**

> **一句话指令词（贴给助手）· One-liner for an agent.**「用 excellence 域的最高标准棘轮处理 <产出物>：先指名一个**可溯源**的最高标杆（R4+，给出来源），按本域 rubric 打分 → 审计最大差距 → 逐项提升 → 把达标分固化为**新下限**（未获人工豁免不得回退），并定期复核标杆是否前移。」

> 机制细节见 [`standard-ladder.md`](standard-ladder.md)。能力以数据驱动方式接入：`data/capabilities.json` 的 `frontier-standard`（触发模块 M3 校验 · M5 自演化 · M8 人工门）。
>
> **可执行 · Executable.** 棘轮已落为 CLI：`harness standard --domain <D> bar|score|audit|raise|frontier <objective>`，读写一份 bar ledger（默认 `updates/standard.json`）。每个域在 `data/rubrics.json` 有各自加权评分表（未知域回退 `default`），因此**同一棘轮适用于所有 24 个域**；`raise` 拒绝回退（除非 `--force`）。· The ratchet is a CLI over a per-domain weighted rubric (`data/rubrics.json`, `default` fallback); it applies to **all 24 domains** and refuses regressions unless `--force`.

---

## What this domain is for · 用途
Give **any** task an explicit, source-anchored **target of excellence** and a **monotone improvement loop** toward it. "Excellence" is never asserted — it is *defined* (a named bar), *measured* (a rubric against that bar), and *raised* (a ratchet), with the bar itself tracked as a moving frontier.

## Why a separate capability · 为什么单列
- **Verification (M3)** asks "is it *correct/complete*?" — a floor.
- **Excellence** asks "is it *as good as the best in the world*?" — a **ceiling that moves**. A floor-gate passes work that is merely acceptable; the apex-bar loop keeps pushing toward the top and never backslides.
- It is **domain-agnostic**: research, code, design, writing, a report, a model — all can be pointed at their best-known reference and ratcheted.

## Pipeline layers · 分层（L0–L7）
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Fix the apex bar | M4, M8 | name the current best-known standard + a checkable source; human confirms |
| L1 | Baseline the output | M3 | score today's artifact on the **same** rubric/benchmark as the bar |
| L2 | Dimension gap audit | M3, M4 | per dimension: ours vs bar vs why; locate the binding constraint |
| L3 | Improvement plan | M1, M7 | pick the **largest** gap; one lever at a time; state the target delta |
| L4 | Raise & re-verify | M6, M3 | apply the lever; re-measure on the same rubric; keep evidence |
| L5 | Ratchet | M2, M5 | record achieved score as the **new floor**; regressions are rejected |
| L6 | Track the frontier | M5, M6 | periodically re-check whether the bar moved (new SOTA); re-baseline |
| L7 | Record | M2, M4 | bar ledger: bar · rubric · scores over time · provenance |

## The apex-bar ladder · 标杆阶梯
Each rung is a named, sourced standard — climb in order, never skip the definition. · 每一级都是**有名有源的标杆**，逐级攀爬。

| rung · 级 | what it is · 内涵 | example · 例子 |
|---|---|---|
| R1 Floor · 底线 | correctness / completeness gate | tests pass, claims sourced (M3) |
| R2 Peer · 同级 | typical competent output | "an average good report" |
| R3 Strong · 优秀 | the recognized strong practice | top-venue paper, senior practitioner work |
| R4 Leader · 领先 | current best available | SOTA on a benchmark/leaderboard |
| R5 Frontier · 前沿 | best-in-class human/expert exemplar | the canonical exemplar others copy |
| R6 Moving · 移动前沿 | the bar as it advances over time | refreshed R4/R5 as SOTA moves |

## Module combination · 模块组合
- **M0** — constitution: never self-declare excellence; an unverifiable bar is `unverified` (M0.1/M0.4).
- **M1** — compare like-for-like: hold the artifact + rubric + exemplar, not the whole corpus.
- **M2** — the bar ledger persists; the ratchet's floor survives across sessions.
- **M3** — the measuring instrument: same rubric on artifact and bar; evidence, not opinion.
- **M4** — the bar's provenance: where the standard comes from, and when it was checked.
- **M5** — the frontier loop: signal (bar moved) → audit (gap) → mutation (improve) → journal (ratchet).
- **M6** — tools to fetch the bar (leaderboards, benchmarks, exemplars) and to measure.
- **M7** — raising the bar is a reviewable change; no auto-publish of a claimed new high.
- **M8** — a human confirms the bar and accepts a new floor (M0.8).

## Anti-patterns · 反模式
- **Self-declared excellence** — calling it "world-class" with no named, sourced bar.
- **Unfalsifiable bar** — a standard no one can measure against.
- **Skipping the definition** — "improve" without saying improve *to what*.
- **Regression tolerance** — accepting a lower score than the ratchet floor.
- **Frozen bar** — never re-checking when SOTA moves; "best" is a moving target.
- **Averaging the gap** — hiding a large deficit behind an overall good score.

## See also
`self-standard.md` (this project held to Claude's engineering bar) · `security-model.md` (least privilege, human gate, reversibility) · `standard-ladder.md` (the ratchet mechanism, in detail) · `../deep-research/README.md` (the output this can point at) · `../model-selection/README.md` (fit-for-task eval) · `../core/04-verification-and-gates.md` · `../core/06-self-evolution.md` · `../review/harness-index.md`.

> **Keeping the frontier alive · 保持前沿鲜活.** `harness evolve` audits the bar ledger (`updates/standard.json`) and raises a `stale_frontier` proposal for any apex bar (R4+) whose moving frontier has not been re-checked within `FRONTIER_MAX_AGE_DAYS` (90) — or that has a floor but no named bar. · `harness evolve` 审计标杆台账，对超过 90 天未复核（或只有下限、无标杆）的 R4+ 标杆发出 `stale_frontier` 提案。
