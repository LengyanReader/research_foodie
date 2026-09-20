# Research Foodie: A Local-First, Cost-Sensitive, Citation-Mandatory Survey Pipeline with Evidence-Grounded Drafting and Honest Self-Evaluation

> **中文速览** — 本文是 research_foodie 的论文**初稿（draft v1, 2026-09-20）**，由 `docs/design/tool-paper-outline.md` 大纲展开成文。所有实验数字均来自本仓库 `_eval_out/` 的本地免费模型实测（判题为非确定性模型，方向性）。本文件是**活文档**：§7 的每个数字都由 `python -m tools.eval.capability_report` 生成/复核（`_eval_out/capability_report.md`），随自演化周期更新。诚实性规则沿用 AGENTS.md：数字带 `as of` 日期、方向性结论标注、未一手复核的引用标 *unverified*。`[TODO]` = 待补实验/配图。

- **Status:** Draft v1 — full spine written from the outline; ablations (§7.6), figures (`fig:architecture`, `fig:loop`), and one-hand citation re-verification pending
- **Target:** arXiv (cs.CL / cs.AI), applied-NLP / systems track
- **Reproducibility:** every quantitative claim maps to a `docs/setup-runbook.md §3` command; regenerate the whole number set with the runbook + `capability_report`
- **Data & code:** local-first; no API keys required for the ≈$0 core loop (hosted free model + free arXiv API + local MinerU parsing)

---

## Abstract

LLM-assisted "deep research" tools now draft literature surveys at scale, but they remain
opaque on two axes that matter most for scholarship: **factual grounding** (whether every
factual claim can be traced to a specific source) and **reproducible evaluation** (whether
the system knows, and honestly reports, when it gets worse). Reported citation-fabrication
rates for frontier models are high — e.g. 78–90% for GPT-4o in the OpenScholar
setting [12] — and quality is usually judged by a single non-deterministic call with no
variance record, on paid cloud models that exclude low-resource users. We present
**Research Foodie**, a local-first, cost-sensitive academic-survey pipeline that treats
*per-claim verbatim grounding as a hard structural constraint* rather than a prompt
request. Three mechanisms enforce it: a write-time anti-hallucination filter that drops
un-grounded claims (5-gram overlap against the parsed source), a **deterministic L6 gate**
that checks structure, citation form, grounding, and bilingual integrity with zero LLM
calls, and a DAS-Bench-style 16-criterion AI judge layered on top. On top of generation we
add a **self-evolution measurement loop** in which every "did this change help?" signal
comes only from *external measurement* (mock regression, pool coverage, a mutation-tested
gate, dependency-version drift) filtered through *variance-aware* thresholds, with
human-gated promotion — the loop writes ledgers, never code. In ≈$0 CPU-only runs
(hosted free model, temperature > 0) the pipeline passes **34/34 mock and 34/34 real**
end-to-end tests on two third-party papers, answers an evidence-grounded QA panel
(n = 31) at **correctness 4.23 / groundedness 4.45** — extractive factoid answering is
essentially solved at **12/13**, while PubMedQA yes/no convergence sits at **8/14**, an
explicitly reported model limit. On a 30-topic arbitrary-domain battery it covers
**22/30** evidence pools and judges an end-to-end sample (n = 10) at Total **3.13**.
We report judge noise (canonical trio P-A **3.88 ± 0.53**), coverage failures, and the
boundary that a ≥ 300 B frozen judge would move but that we do not have keys for. The
contribution is a demonstration that *auditable, ≈ $0, self-measuring* survey generation
is constructible — and that its limits should be surfaced, not hidden.

**Keywords:** survey generation · evidence grounding · hallucination prevention ·
LLM evaluation · local-first · citation verification · DAS-Bench · self-evolution

---

## 1. Introduction

The production of literature surveys has moved from a purely human craft to an
agent-orchestrated pipeline. Systems such as OpenResearch/orx [1], STORM [2], PaperQA2 [3],
Tongyi DeepResearch [13], and OpenScholar [12] automate retrieval, outline construction, and
drafting. As capability has grown, two gaps have become the binding constraint on trust:

1. **Citation hallucination.** Models attach plausible-but-fake or unsupported references;
   the OpenScholar evaluation reports GPT-4o fabricating on the order of 78–90% of
   generated citations in its setting [12]. A survey whose facts cannot be traced is not
   usable for scholarship regardless of fluency.
2. **Non-reproducible evaluation.** Quality is typically a single judge call, reported as a
   scalar with no variance, no frozen baseline, and no record of when a change made the
   system *worse*. Meanwhile the barrier to entry (cloud models, GPUs) excludes the
   low-resource users who would most benefit from open tooling.

**Our approach.** Research Foodie makes grounding a *structural* property. A factual claim
that cannot be shown verbatim inside the source it cites never reaches the manuscript. On
top of that floor we add honest self-measurement: a scheduled loop that detects regressions
from external signals only and never lets the system quietly edit itself.

**Contributions.**

- **C1 — Grounding as a first-class constraint.** A write-time 5-gram filter plus a
  zero-LLM deterministic L6 gate plus a 16-criterion judge make "every claim is traceable"
  an architectural invariant, not an aspiration (§6.5–6.6).
- **C2 — A near-zero-cost, reproducible implementation.** The full vertical runs on a
  hosted *free* model, the free arXiv API, and local MinerU parsing on a CPU-only machine;
  every stage has a one-line reproduction command (§7, `docs/setup-runbook.md`).
- **C3 — A self-evolution measurement mechanism.** External-measurement-only triggers,
  variance-aware thresholds, a frozen baseline, a mutation-tested gate, and human-gated
  promotion turn "is the system better?" into a data question (§6.7).
- **C4 — An honest evaluation protocol.** Judge noise, empty-pool failures, and the model's
  decision limits are all reported explicitly; we never head-to-head against the published
  DAS leaderboard we cannot reproduce (§7, §8).

*Paper organization.* §2 positions the work; §3 describes the system; §4 reports evaluation;
§5 discusses limitations; §6 concludes. *(Section numbering in this draft follows the
outline's spine; final arXiv formatting TBD.)*

---

## 2. Related Work

We organize comparison along the evaluation axes the system itself uses.

- **STORM [2]** (NAACL 2024) introduced multi-perspective outline generation and
  retrieval-based section writing, but offers no mandatory grounding gate and no mechanical
  judge. We adopt the perspective-decomposition idea (our L-2 reader-perspective rail) and
  add a hard grounding constraint.
- **OpenResearch / orx [1]** emphasize agentic orchestration and full-text retrieval
  (alphaXiv); they do not commit to per-claim traceability. We borrow the discovery-rail
  pattern while keeping a deterministic LangGraph path.
- **PaperQA2 [3]** pairs retrieval re-ranking with citation verification and a retraction
  check, and reports superhuman LitQA2 accuracy — but is not tied to a zero-budget model
  route. We borrow its claim+verbatim-quote evidence style.
- **DAS / DAS-Bench [4]** (arXiv:2608.18034; 30 topics, 16 criteria) is the rubric we adopt
  *verbatim* for the judge (BSC/MAR/TSQ/HDQ families). We implement the judge ourselves and
  therefore report directionally; the official harness (frozen ≥ 300 B judge, DAS-2M pools,
  rendered-page MAR) is **not** run — an explicit limitation, not a silent one.
- **Tongyi DeepResearch [13]** (Apache-2.0 open baseline) and **OpenScholar [12]**
  (Nature 650:857) anchor the "understandable but hallucination-prone" frontier we target.
- **Parsing / data / benchmarks:** MinerU [5], DAS-2M [7], Qasper [8], PubMedQA [9],
  SciQ [10], GAIA [11].
- **Self-evolution methodology:** GEPA/DSPy [15] (text-feedback optimization, up to ~35×
  cheaper than RL), Seddik [16] (anti-collapse / provenance floors), Huang [17]
  (measurement-driven optimization), Tyen [18] (LLM-as-judge noise). These motivate our
  two design rules in §6.7.

**Research gap.** Existing systems are either *capable but expensive/ungrounded* or
*grounded but not self-measuring*. To our knowledge no public implementation delivers
auditable, mandatory-provenance survey generation at ≈ $0 on CPU-only hardware *and*
honestly self-evaluates with variance. That niche is ours.

---

## 3. System Design

> `[TODO fig:architecture]` — L0–L6 layering + the `S_lit→S_org→S_write→S_revise→S_final→gate→judge` state machine. `[TODO fig:loop]` — the self-evolution cycle.

### 3.1 Overview
Six layers (L0 orchestration → L6 deterministic gate) over a LangGraph state machine. Two
routing modes share the graph: a *survey* path and a `seed_id`-anchored *evidence-grounded
QA* node (Track C). Model access is pluggable across three selectable base-model options
(§3.7).

### 3.2 Discovery (L1)
Three interchangeable rails — `seed | arxiv | orx` (`S_LIT_BACKEND`). The free arXiv API
responds in ~1.1 s (measured 2026-09-16); the failure chain is `orx → arxiv → seed` so a
run never dead-ends. Without a DAS-2M metadata lake (absent locally), pool precision is
capped by arXiv relevance top-K — a measured property (§4.4).

### 3.3 Evidence & parsing (L2)
MinerU converts PDF→Markdown in windowed mode (≤ 6 pages/window) to dodge a known
long-document flake; `resolved_evidence()` assembles a multi-paper evidence pool.

### 3.4 Orchestration (L3–L5)
Per-paper grounded claims (each tagged with its `paper_id`), STORM-style outline, per-section
grounded writing, and a `_finalize` step emitting Abstract / Evidence Table / References /
audit annex.

### 3.5 Deterministic gate (L6, zero-LLM)
`validate.py` checks structure, citation form (arXiv/DOI), **5-gram verbatim grounding**,
bilingual integrity, and multi-paper presence. Claims failing grounding are dropped at write
time. We harden the gate with a **mutation test** (23 hand-built mutants, 100 % kill) so a
regression in the gate — not just in the draft — is caught (§4.5, E-2b).

### 3.6 AI judge gate
A DAS-Bench 16-criterion rubric (BSC · MAR · TSQ · HDQ, verbatim from the protocol).
Every score is provenance-stamped with the actual `judge_model` and temperature (§3.8).

### 3.7 Model access & routing (WS-D, Phase D)
Role-level *profiles* resolve which model runs which lane (draft | qa | judge). Three
selectable options, chosen by env var — no keys ever in code or the repo:

- `free-opencode` (default) — all lanes on a hosted free model; redirect the hosted model
  with `OPENCODE_MODEL` (e.g. `opencode/qwen3.8-flash`).
- `openai-compat` — all lanes on any OpenAI-compatible provider via `OPENAI_*` (e.g. Qwen
  through DashScope); needs a key.
- `judge-strong` — draft/qa stay free, judge escalates to a registered strong model — the
  DAS convention that drafting stays free even under a paid judge.

An unknown profile or missing key fails loudly (never a silent fallback). This is verified by
`tools/eval/test_capability.py`.

### 3.8 Provenance (D-4)
Every report (bench, health, sprint, judge matrix, capability snapshot) carries model,
`judge_model`, temperature, profile, and an `as of` timestamp, so a number can always be
traced to the run that produced it.

### 3.9 Self-evolution (WS-C, Phase X)
A four-phase acquisition→refinement→updating→evaluation cycle (Tao [need ref id]; cf. the
blueprint) built on **two enforced rules**: (i) a trigger may come *only* from external
measurement — never model self-assessment (Huang [17], Tyen [18]); (ii) every signal passes a
variance-aware threshold before opening a ticket or nominating promotion. Primitives
(`tools/eval/evolution.py`): a one-open-per-component debug-ticket board (E-3), a
dependency/version ledger (E-4), and a feedback corpus with an anti-model-collapse
real-gold quota plus a promotion rule requiring **N ≥ 3 sustained rounds ∧ Δ ≥ 2σ ∧ no
regression** (E-5). The loop writes only ledger JSONs under `_eval_out/`; it never edits
code or prompts and never commits — promotion is an eligibility flag a human acts on.
`[TODO fig:loop]`

---

## 4. Evaluation

> All figures `as of 2026-09-19/20`, from `_eval_out/`, produced by a non-deterministic
> free judge (temperature > 0 → noisy; treat as directional). Regenerate/refresh the whole
> table with `python -m tools.eval.capability_report` (writes
> `_eval_out/capability_report.md`).

### 4.1 Vertical correctness (pipeline tests)
Deterministic L6 gate + multi-paper grounding: **mock 34/34 · real 34/34** (real = two
third-party papers, Liang 2304.02819 and Weber-Wulff 2306.15666, full loop), with verbatim
quotes, normalized `arXiv:` citations, and validation score 1.0 regardless of which model
drafts. Full P-A loop latency 121.7 s on the free hosted model.

### 4.2 Evidence-grounded QA (Track C)

| subset | n | correctness | groundedness | pass |
|---|---|---|---|---|
| Extractive / provided-context path | 13 | 4.85 | 4.38 | **12/13** |
| Qasper external gold QAs | 5 | 5.00 | 5.00 | 5/5 |
| SciQ MCQs (provided context) | 5 | 5.00 | 3.80 | 5/5 |
| PubMedQA yes/no | 14 | 3.57 | 4.43 | **8/14** |
| **Full panel** | **31** | **4.23** | **4.45** | **24/31** |

Extractive factoid answering is essentially solved; PubMedQA **yes/no conclusion
convergence (8/14)** is an honestly-reported model limit, not a harness bug.

### 4.3 16-criterion judge — canonical trio & variance
P-A **3.88 ± 0.53** · P-B **3.31 ± 0.00** · P-C **3.53 ± 0.13** (2 fresh runs each). The ± is
the point: we report the spread, and the self-evolution loop's FAIL threshold is defined in
σ units of exactly this spread (§4.5).

### 4.4 30-topic arbitrary-domain battery
Pool build **22/30** covered (14 full 3-paper pools; **8 empty** = arXiv relevance + parse
caps). End-to-end judged sample (n = 10) Total **3.13** (BSC 3.08 · MAR 2.67 · TSQ 3.05 ·
HDQ 3.73). HDQ confirms synthesis; MAR 2.67 is dragged by 1-paper pools and the text-only
artifact (no rendered-page scoring — a ≥ 300 B page-aware judge is the known blocker).

### 4.5 Self-evolution measurement (Phase X, design verified)
The mutation-tested gate kills **23/23** mutants (100 %), so gate regressions are detected
independently of draft quality. `tools/eval/test_evolution.py` (31 assertions) and
`tools/eval/test_capability.py` (22 assertions) prove ticket open/feed/close, promotion
verdicts, gold-quota floor, dep-drift classification, and the config layer — all deterministically,
zero-network, temp-isolated. Two consecutive `--quick` cadences render GREEN with a clear
board; the L-6 `self_check.ps1` runs the whole offline net in ~15 s.

### 4.6 Ablations `[TODO]`
Planned: (a) grounding gate on/off → judge-score delta; (b) discovery-rail swap → pool
coverage; (c) judge swap (free vs ≥ 300 B) → score compression (D-3 `judge_matrix` harness is
implemented and mock-verified; live run gated on a registered key); (d) post-change re-measure
(mutation/kill rate).

### 4.7 Cost & latency
Core loop ≈ $0. `[TODO]` a formal token / API-call / wall-clock table.

---

## 5. Discussion & Limitations

The three gates complement rather than replace human review: the positioning is
anti-fabrication and noise reduction, **not** auto-publication (stated in README/AGENTS).

Honest limitation list:
1. Judge is a free non-deterministic model; MAR/Layout needs a ≥ 300 B page-aware judge (blocked on keys/GPU).
2. 8/30 topics yield empty evidence pools — a measured cap of arXiv relevance + parsing, surfaced not hidden.
3. PubMedQA yes/no 8/14 is a model boundary.
4. Single CPU-only machine; no metadata lake, no GAIA batch (HF gating).
5. Self-evolution Phase-X E-7 (automated DSPy/GEPA prompt evolution + judge-vantage swap) remains a planning item gated on a strong reflection LM.

**Takeaway for the community:** cost, grounding, and auditability can be satisfied together,
at least in part — by making mandatory provenance a *structural* constraint (write-time
filter + deterministic gate) instead of a prompt instruction.

---

## 6. Conclusion

We presented Research Foodie: an auditable, ≈ $0, self-measuring survey pipeline that makes
per-claim verbatim grounding an architectural invariant and reports its own variance and
failures. Its limits — the judge model, evidence-pool coverage — are surfaced explicitly.
Future work: a ≥ 300 B frozen judge, the DAS-2M pool, GAIA, a Chinese evidence layer, and
R-phase automated prompt evolution feeding the (still human-gated) promotion rule.

---

## References (IEEE-style, draft)

> From this repo's verified sources (PROGRESS U/LEDGER lines, TOOL-COMPARISON). Accessed
> 2026-09-20. *unverified* marks entries needing one-hand re-check before publication; run
> `tools/citation-verify` on [4][14][17][18][19][20] and drop anything unverifiable.

1. OpenResearch / orx (2025), official mirror; CLI `orx discover`.
2. Y. Shao et al., "Assisting in Writing Wikipedia-like Articles from Scratch with LLMs," NAACL 2024, arXiv:2402.14207.
3. PaperQA2, arXiv:2409.13740.
4. J. Xu et al., DAS: Efficient and Scalable Collaboration between Agents, arXiv:2608.18034; DAS-Bench 30 topics / 16 criteria, repo ZhikaiXu24/DAS. — *re-verify arXiv ID before publication*.
5. MinerU: precise document extraction, arXiv:2410.17381. — *version unverified*.
6. LangGraph (LangChain), docs.langchain.com.
7. DAS-2M ≈ 2 M arXiv papers (2020-01→2026-06), HuggingFace (2026-08).
8. Qasper qasper-train-dev-v0.3, allenai.
9. PubMedQA: qiaojin/PubMedQA (HF).
10. SciQ, AllenAI (provided-context mode).
11. GAIA benchmark (466 Qs).
12. H. Chen et al. (OpenScholar), *Nature* 650, 857–863, 2025, DOI 10.1038/s41586-025-10072-4.
13. Tongyi DeepResearch, 30.5 B total / 3.3 B active, arXiv:2510.24701 (Apache-2.0).
14. Jiang et al., "STORM ...", arXiv — *cross-check vs [2]*.
15. GEPA, arXiv:2507.19457.
16. Seddik et al., arXiv:2404.05090.
17. Huang et al., "Efficient Optimization ...", arXiv:2310.01798. — *title unverified*.
18. Tyen et al., arXiv:2311.08516. — *unverified*.
19. PaddleOCR / PaddleOCR-VL, arXiv:2510.14528.
20. Lloyd et al., LRM-judging measurement, 2025. — *unverified*.

---

*Lineage: draft v1 authored 2026-09-20 from `docs/design/tool-paper-outline.md` +
`docs/CAPABILITY-STATUS.md` + `_eval_out/` measured artifacts. Living document: §4 numbers
are refreshed/verified by `python -m tools.eval.capability_report`; keep the outline
(`docs/design/tool-paper-outline.md`) and this draft in step as the self-evolution cadence
records new measurements.*
