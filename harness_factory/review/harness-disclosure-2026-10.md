# Harness disclosure · 2026-10 — reading arXiv:2605.23950 in full, and what it changes in M3

**Updated:** 2026-10-23 · **Round:** P20.1 (+ P20.3 corroboration) · Companion to [`harness-landscape-scan-2026-10.md`](harness-landscape-scan-2026-10.md) (the observe half; this doc is the assimilate half).

> **中文速览**
> 本轮把《Stop Comparing LLM Agents Without Disclosing the Harness》（arXiv:2605.23950，`[R243]`）**全文读完**（不止摘要）：它提出的 Binding Constraint Thesis 与本库立场同构——长时程任务上 **harness 引发的方差可以压过模型引发的方差**（受控 3×3 网格：HV̄/MV̄ = **7.80×**，两次独立 run 分别 8.72×/6.76×；9 组模型对/harness 对比较中 **6 组排名翻转**）。它给出两件本库此前没有的可执行物：**ETCSOVG 七层披露卡**（Execution/Tool/Context/Scheduling/Observability/Verification/Governance，逐层最低披露字段）与**两种合法比较协议**（锁定 harness，或双因子分解方差）。据此在 M3 落新条款 **M3.16「比较必须披露其 harness」**——不做能力（它按*主张类型*触发而非特征向量，与 `methodology-fit` 同理），只做条款 + 清单 + 反模式。与 `component-ablation`（M5.12）互为镜像：剪枝在*一个* harness 内部拆部件，披露在*多个* harness 之间点名配置。公开佐证（HAL 跨脚手架 34–48 分差距、Epoch AI 报告 11–15 分纯 scaffold 波动）与 PolyWorkBench 的固定输入协议（*listed*，未深读）都指向同一方向。论文的**可伪证条款**（若受控网格发现 MV > HV 则推翻）与「H3 反而放大模型间方差」的反直觉细节一并记录，不粉饰。

---

## 1 · Why this paper, why now · 动机

The factory's premise is that the harness is the object of study ("same model, different harness, different agent"). Until this round that premise was **asserted internally** (README, `component-ablation` practice in P16) but **not externally citable**: the corpus (R1–R242) contained no disclosure standard and no variance-decomposition protocol. `[R243]` supplies both, and it keys on exactly the artifact the factory already emits — a disclosed harness configuration (`AGENTS.md` + `.harness/manifest.json`).

Scan-round note: the signal was surfaced in [`harness-landscape-scan-2026-10.md`](harness-landscape-scan-2026-10.md) §2a-S1; the shrink condition ("if the disclosure standard is only a checklist already subsumed by the manifest, this slice shrinks to refs + crosswalk") was checked by a **full read** and **did not fire** — the card is a field taxonomy for *comparisons*, not a manifest for *one run*, and the variance protocol has no counterpart in the library.

## 2 · What the paper actually says · 论文内容（全文读）

**Y. Zhang, J. Wang, Y. Ge, W. Xu, J. Hamm, C. K. Reddy** (Tulane / Rutgers / ind. / Virginia Tech), arXiv:2605.23950, submitted 2026-05-07, cs.AI/cs.SE. Position paper + one controlled experiment.

1. **Binding Constraint Thesis.** For long-horizon tasks across frontier-comparable models, harness-induced variance (HV) governs performance at least as much as model-induced variance (MV). Explicitly *empirical and falsifiable*: a factorial grid finding MV̄ > HV̄ under matched conditions would refute it (§3.3).
2. **Harness as controller.** The harness is the controller of a stochastic policy; three quantities locate its failure modes — **stability** (self-verification/feedback), **context drift**, and **control lag τ** (steps between anomaly detection and corrective observation reaching the policy; high τ enables failure cascades). The asymmetry that grounds the thesis: upgrading the model lowers the anomaly *base rate*, but the *response* to anomalies is a controller property that no model upgrade supplies.
3. **The four common responses all fail to solve attribution** (§3): standardizing on one harness (HAL, SWE-bench Pro scaffold, Epoch's mini-SWE-agent) — endorsed as *one of two* valid regimes, but it embeds design choices and forecloses harness-side gains; "scale dissolves it" — contradicted by Claude Code redesigning (not removing) harness components as models improved; disclosure is the structural answer.
4. **ETCSOVG disclosure card** (Appx. A, Table 3) — seven layers with **minimum fields** per layer:
   | Layer | Minimum disclosure |
   |---|---|
   | **E**xecution | runtime substrate, sandboxing, filesystem/network access, task timeout, step timeout, max steps, evaluation entry point |
   | **T**ool | tool list, schema style, tool-selection policy, error format, retryable error classes, model-visible vs hidden middleware |
   | **C**ontext | context cap, ordering, summarization/compression policy, retrieval method, persistent memory, cache policy |
   | **S**cheduling | agent loop, stopping rule, retry policy, escalation, delegation, rollback behavior |
   | **O**bservability | logged artifacts, trajectory format, checkpoints, traces, validation logs, post-run auditability |
   | **V**erification | output parser, schema validation, self-checking, test execution, anomaly detection, final patch validation |
   | **G**overnance | permission model, allow/deny rules, side-effect boundaries, secret handling, human approval points |
5. **Controlled 3×3 grid** (§4.2). Models chosen *before* the run for tight leaderboard clustering (Kimi K2.6 45.4, GLM-5.1 45.3, GPT-5.4 44.6 on the 2026-04-23 LLM Stats coding snapshot); harnesses H1 Minimal (no compression, verbose schema, no retry/verification/recovery) / H2 Improved / H3 Full (per-step self-check, drift checks every 5 steps, anomaly middleware, output validation, rollback depth 10); 100 difficulty-stratified SWE-bench Verified tasks, 2 runs, shared Docker env, 50 steps, 120 s/step.
   Results (mean pass@1, two runs): GLM-5.1 52.5→56.5→65.5; GPT-5.4 55.0→58.5→63.5; Kimi K2.6 52.0→59.0→60.5. **HV̄ 18.48 pp² vs MV̄ 2.37 pp² = 7.80×** (run 1: 8.72×; run 2: 6.76× — the pattern is not an averaging artifact); **6 of 9** model-pair/harness-pair comparisons flip ranking. The authors explicitly disclaim universality of the 7.80× ratio.
6. **Reporting practice.** η²_p from fixed-effects two-way ANOVA, but *must* be paired with ω² or a bootstrap interval (η²_p is positively biased on small grids) **and with explicit reversal counts** — a large η²_p neither implies nor requires ranking flips.
7. **A subtlety worth keeping** (Appx. E): cross-model variance is *smallest* under H2 (1.17 pp²) and *largest* under H3 (4.22 pp²) — better control can **absorb** model differences, while verification/recovery mechanisms can **expose** them. "Better harness ⇒ model choice irrelevant" is false in both directions; this is itself an argument for disclosure over standardization.

## 3 · Crosswalk vs this library · 与本库对照

| existing | relation to `[R243]` |
|---|---|
| `component-ablation` (M5.12, R234/R235) | **mirror image**: ablation removes parts *within* one disclosed harness to measure causal contribution; disclosure names the harness *across* comparisons so contributions are separable at all. Neither subsumes the other. |
| `eval-driven-development` (R92) | upstream: it says define the eval gate; M3.16 says the *comparison of gated runs* is incomplete without harness cards on both sides. |
| M3.10 instrument-matching | same claim-type logic: a comparative claim gets its instrument (ETCSOVG card + variance decomposition), just as a formal claim gets a checker. |
| M3.14 / M3.15 (precision-recall, staged funnel) | siblings on reporting integrity: M3.14 says don't read a filter as a discovery, M3.15 says locate the lost stage, **M3.16 says name the condition the scores came from**. |
| `.harness/manifest.json` (M5.10 emission) | the manifest describes **one emitted harness**; the ETCSOVG card is what a **comparison** must attach per arm — the shrink-condition from the scan doc fails because the purposes differ (task execution vs experimental condition). |
| `model-portfolio-discipline` (P19, R239–R242) | P19 concluded "the model is a variable"; M3.16 is its measurement-side complement: if the model is a variable, every comparison must state the *other* variable. |
| M8 human-gate / M2.12 | ETCSOVG **Governance** ("human approval points") and **Context** ("summarization/compression, persistent memory") are external validation that the library's layer split is load-bearing. |

**Why a clause, not a capability:** it fires on *claim type* (a comparative benchmark statement), not on the 8-axis feature vector — the same reasoning recorded in `integration-map-2026-10.md` §2 for `methodology-fit`. Landing: **M3.16** in [`../core/04-verification-and-gates.md`](../core/04-verification-and-gates.md) (pattern item + checklist line + anti-pattern "Unnamed-harness comparison").

## 4 · Public corroboration (and its limits) · 公开佐证

All from `[R243]` §4.1's observational survey, read in context; the paper is the citation, the numbers are its reports:

- **HAL** — cross-scaffold gaps on SWE-bench Verified Mini under the *same model*: 34 pp (Claude Sonnet 4.5, 68%→34%), 34 pp (GPT-5 Medium, 46%→12%), ≈48 pp (o4-mini), between SWE-Agent and HAL Generalist.
- **Epoch AI** — up to 11–15 pp of scaffold-only variation on SWE-bench Verified; its recommendation (mini-SWE-agent for cross-model comparison) is a locked-harness protocol in practice.
- **SWE-bench Pro** — top six frontier models span only 4.9 pp under one scaffold; adding a single subagent (WarpGrep) flips MiniMax 2.5 vs Claude Opus 4.6 — interaction effects are not ignorable.
- **PolyWorkBench** (arXiv:2607.06008, *listed — abstract-level only*) — an executed instance of the controlled comparison discipline: same inputs and timeout across harnesses.
- **LHTB** (Long-Horizon Terminal-Bench, *listed*) — hidden fake-proof verifiers; corroborates M3's anti-gaming lineage rather than disclosure per se.

## 5 · MCP 2026-07-28 addendum pointer · 另见

The same round digested the MCP core revision (`[R244]`, P20.3). Because MRTR, Tasks, cache hints and the deprecation window map onto M8/M2/M1/M7 respectively, that material is recorded in [`workflow-patterns-2026-10.md`](workflow-patterns-2026-10.md) §9 (protocol-side mechanics) rather than here; AST10 closure (P20.2) lands in `data/levers.json` + capability provenance and is recorded in [`cycles.json`](../src/harness_factory/data/cycles.json).

## 6 · Verification status · 核验状态

- **Full read 2026-10-23:** `[R243]` HTML full text (main body §1–§5 + Appendices A/B/E read; all figures above quoted from the paper itself). Not independently replicated; the 7.80× ratio is the authors' single-grid estimate on one task distribution — carry as *directional*, never as a law.
- **Full read 2026-10-23:** `[R244]` (MCP GA blog), `[R245]` (OWASP AST10 README, all ten risks + evidence table).
- **Listed only, marked per the no-laundering rule:** PolyWorkBench / LHTB / AgentIF-OneDay / METR dashboard / agent-teams docs / LF A2A press (see [`references.md`](references.md) §W verification note).
- **Deliberately not entered:** `platform.claude.com/docs` pages (region-blocked this session, same as P19) — the context-editing/memory mechanism claims rest on `[R237]` alone.

## See also · 参见

[`harness-landscape-scan-2026-10.md`](harness-landscape-scan-2026-10.md) (the scan that proposed P20) · [`../core/04-verification-and-gates.md`](../core/04-verification-and-gates.md) (M3.16) · [`harness-ablation-2026-10.md`](harness-ablation-2026-10.md) (M5.12, the mirror) · [`model-families-2026-10.md`](model-families-2026-10.md) (P19) · [`../sources/source-map.md`](../sources/source-map.md) (provenance row) · [`workflow-patterns-2026-10.md`](workflow-patterns-2026-10.md) §9 (MCP addendum)
