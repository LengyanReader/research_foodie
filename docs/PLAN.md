# Research Foodie — Execution Plan (执行计划)

> 中文速览：本计划分三部分——(A) 校对 `docs/refs/ai-research-tools-workflow-guide.md` 并建立"验证台账"；(B) 修订该指南（补参考文献、修正已确认的错误、增补开源工具）；(C) 编写 `docs/design/research-foodie-blueprint.md` 架构蓝图（复用 OpenResearch / STORM / DAS / PaperQA2 / MinerU，本地优先 + 廉价 API）。纯文档交付，不写代码。所有事实声明一律回到一手资料。

- `Updated`: 2026-09-16
- `Status`: **Tasks A–D complete. P1 tooling complete; P2 minimal vertical GREEN + framework integration + generalization; benchmark-style evaluation pilot done (Session 11); multi-paper evidence synthesis P0 GREEN (Session 12); survey-depth S_write GREEN — per-section drafting (Session 13); P1 judge calibration GREEN (Session 14); MAR render axes part 1 GREEN — manuscript + PDF (Session 15)** — MinerU ✓, PaddleOCR ✓ (K7 closed), LLM client ✓ (default `opencode` backend, `opencode/big-pickle`, `--auto` for headless robustness; OpenAI-compat; **Ollama backend removed 2026-09-16**); `langgraph` 1.1.10 installed; `tools/pipeline/` P2 live: **S_lit pluggable discovery rails (seed | arXiv API | orx CLI; arXiv verified reachable 2026-09-16)** + **multi-paper evidence pool `resolved_evidence()` (3 local papers) + per-paper grounded claims (`paper_id`) + survey-depth per-section drafting (intro + `## <heading>` sections + conclusion, inline arXiv attribution) + manuscript `_finalize` (Abstract/Evidence Table/References) + local PDF render (`tools/eval/render_manuscript.py`)** + full graph + L6 deterministic gate (+ informational `multi_paper` check) + code-fence-tolerant JSON parsing; **STORM-style outline + DAS-Bench-style AI judge gate integrated (Session 9)**; **mock 34/34 + real `opencode/big-pickle` 34/34; DAS-16 canonical family means BSC 2.92 / MAR 2.67 / TSQ 2.83 / HDQ 3.75 / Total 3.04 (Session 15 combined run; MAR fix verified: Figure/Table 1→3, MAR 1.75→2.50 on P-A), PDFs 5-8 pp**. Next: ≥300B page-aware judge on rendered PDFs (MAR Layout axis + compliance), DAS-2M pools, Track B.
- `Language`: English (master) with 中文速览 blocks

---

## 1. Background / 背景

The repo contains a single reference guide (`docs/refs/ai-research-tools-workflow-guide.md`, ~317 lines) surveying AI research tools. The user asked to:
1. Audit, repair, supplement, and optimize that document (accuracy, completeness, depth, primary-source citations);
2. Plan a complete **intelligent proactive research workflow** based on — but not limited to — that guide, favoring open-source/free tools with high cost-effectiveness;
3. Reference / reuse / re-develop named frameworks: **alphaXiv/OpenResearch**, **Deep Academic Survey (DAS)**, **Stanford OVAL STORM**, etc.

Environment: local Win11 CPU-only host + a remotely accessible GPU platform (dual-track). Locale: bilingual (EN/ZH).

## 2. Deliverables / 交付物

| # | Artifact | Action |
|---|----------|--------|
| D1 | `AGENTS.md` | Workspace principles (bilingual) — created |
| D2 | `docs/PLAN.md` | This plan (bilingual) — created |
| D3 | `docs/PROGRESS.md` | Bilingual progress log — created |
| D4 | `docs/refs/ai-research-tools-workflow-guide.md` | Revised (fixes + references + verification ledger) |
| D5 | `docs/design/research-foodie-blueprint.md` | Bilingual architecture blueprint (L0–L6 workflow) |

Implementation began after Task D (this section reflects the docs-only phase). Code delivered to date: `tools/llm/` (LLM client + mock server + claim-plan module), `tools/pipeline/` (P2 LangGraph skeleton).

## 3. Verified findings so far (Task A input) / 已核实的发现

> Sources verified 2026-09-15 via primary GitHub/arXiv/Nature/官方 pages.

**Correct as written** (numbers match primary sources):
- DAS total avg 4.34 = Human 4.34; Naive-RAG 4.03, Gemini DR 3.92, GPT DR 3.68, SurveyForge 3.78, AutoSurvey 3.73 (github.com/ZhikaiXu24/DAS table).
- DAS preference over Naive RAG 27/30 topics (majority voting).
- DAS-2M ≈2M arXiv papers (2020-01 → 2026-06), 8 field groups, on HuggingFace; DAS-Bench 30 topics / 16 criteria (BSC/TSQ/HDQ/MAR); generation code explicitly "To be released"; eval harness released incl. `evaluation/run_eval_all.sh`, `PDF_EXTRACT_KIT_ROOT`, OpenAI-compatible judge.
- OpenScholar in Nature 2026 (650:857–863, DOI 10.1038/s41586-025-10072-4), beats PaperQA2 by ~6% on correctness; GPT-4o hallucinates citations 78–90%.
- Tongyi DeepResearch: 30.5B total / 3.3B active (arXiv 2510.24701); open (Apache-2.0), GitHub Alibaba-NLP/DeepResearch.
- GitHub Copilot usage-based billing live June 1, 2026 (1 credit = $0.01; Pro $10/mo incl. ~$15 credits).
- `open_deep_research` ranked #6 on FutureSearch Deep Research Bench (0.4344) — confirmed in repo README (2025-08-02).
- PaperQA2: retraction check + superhuman claims (arXiv 2409.13740); Apache-2.0.

**Errors / stale facts to fix**:
- E1. `orx lit` is not a command → actual: `orx discover keyword|embedding|openalex|biorxiv`, `orx paper <id> [--source] [--full]`. (`orx lit` ≈ internal skill module `orx-lit-review`.) New info missing: Windows-beta support, `orx install-skills` (Claude Code/Codex/OpenCode/Cursor), `orx up` local dashboard, local-model support (Ollama/LM Studio), new OpenAlex/bioRxiv backends.
- E2. MinerU license: since 2026-04-18 (v3.1.0) it is the custom **MinerU Open Source License** (Apache-2.0-based + attribution for online services + commercial thresholds MAU>100M / revenue>$20M), not plain Apache 2.0. Also "from the same lab" misleading: MinerU = OpenDataLab; DAS = Zhejiang Univ + SJTU.
- E3. Semantic Scholar index count ≈ 223M on official site as of Sep 2026 (214M was API/product-page figure).
- E4. Copilot Free "2,000 completions/mo" is stale under usage-based billing (completions unbilled/unlimited on paid plans; Free = limited chat+agent).

**Open / spot-check claims** (each verifies against a source, or is demoted to *unverified*):
- U1. DAS judge models "Kimi K2.6 alongside Qwen3.5" → check DAS-Bench README/HF page.
- U2. DAS-2M built by parsing with MinerU → check DAS paper §DAS-2M.
- U3. "STORM ~3–4 min/topic" hosted UI → soft claim, no hard source.
- U4. Research Rabbit free-tier "50 seed papers / search" post-Litmaps → check.
- U5. Elicit "~90% extraction accuracy" self-report → check Elicit page.
- U6. scite "1B citation statements / 180M+ papers" → check scite page.
- U7. Curtin University dropped Turnitin AI-detection in 2026 → check news.
- U8. Judge-switch anecdote ("Gemini 2.5 Pro → GPT-5.5, May 2026"), "#1 leaderboard" marketing pattern → likely mark unverified/anecdotal.
- U9. NotebookLM → Gemini Notebook rename (July 2026) → check Google.
- U10. Claude Science beta June 30, 2026; GPT-Rosalind Apr 2026; Gemini for Science May 2026 → spot-check.
- U11. Weber-Wulff et al. detector study; Liang et al. (Stanford) non-native bias → confirm exact citations.
- U12. PaddleOCR "109 languages"; DeepL pricing $8.74/mo → spot-check.

## 4. Execution steps / 执行步骤

### Task A — Residual verification (`docs/PROGRESS.md` → ledger appendix)
- [x] A1. Verify U1–U12 against primary sources (web). Recorded in PROGRESS.md and the guide's Verification Ledger. (U1,U2,U4,U7–U12 VERIFIED; U3 demoted to unverified; U5/U6 corrected; U13 Ai2 ScholarQA discovered & added.)
- [x] A2. Where a claim cannot be verified: keep in doc but mark *unverified* + note; drop assertions phrased as fact. (Done for U3.)

### Task B — Revise the guide (`docs/refs/ai-research-tools-workflow-guide.md`)
- [x] B1. Apply E1–E4 corrections with per-correction source + access date.
- [x] B2. Add a **References** section: arXiv IDs / DOIs / GitHub URLs for every named system & study.
- [x] B3. Add "Verified as of 2026-09-15" banner + **Verification Ledger** appendix.
- [x] B4. Supplement open-source stack: Ai2 ScholarQA, OpenResearch new backends, Windows/remote-GPU notes; tighten unverifiable anecdotes.
- [x] B5. Preserve existing strengths: human checkpoints, pricing caveats, citation-fabrication warnings, Chinese-source caveats.

### Task C — Architecture blueprint (`docs/design/research-foodie-blueprint.md`, bilingual)
- [x] C1. Dual-track scope: Track A CS/ML; Track B multilingual humanities.
- [x] C2. L0–L6 layered architecture with state model mirroring DAS.
- [x] C3. Reuse map: reuse-as-is vs re-implement vs build custom.
- [x] C4. Cost/environment matrix: local Win11 CPU + remote GPU + cheap APIs (core ≈$0).
- [x] C5. Proactive loop design: change feed → drift/confidence flags → re-synthesis policy.
- [x] C6. Phased roadmap P1–P5 with exit criteria.

### Task D — Wrap-up
- [x] D1. Update `README.md` pointer to the two docs.
- [x] D2. grep for `TODO`/`TBD`/broken links; update PROGRESS.md.
- [x] D3. Report; no commit unless requested.

## 5. Principles in force (from other sessions) / 适用原则
- `cookbooks/AGENTS.md` → single master doc, faithful translation (adapted: EN+ZH both primary here).
- `m_flow/AGENTS.md` → structured layout, quality gates, Conventional Commits.
- This repo's `AGENTS.md` → 计划先行 / track-as-you-go / primary sources first / cost-sensitive.

## 6. Implementation log (post-Task D) / 实现日志

| # | What | Status | Test result |
|---|------|--------|-------------|
| 1 | `tools/llm/client.py` — unified LLM backend (**opencode default** + OpenAI-compat) | done | mock 3/3 · **opencode/big-pickle 3/3** |
| 2 | `tools/llm/smoke_test.py` + `mock_openai_server.py` | done | see above |
| 3 | `tools/llm/claim_plan.py` — reusable L4 claim-plan (CLI) | done | opencode/big-pickle ✔ |
| 4 | `tools/pipeline/` — P2 LangGraph minimal vertical (S_lit→S_org→S_write→S_final→L6 gate) | done | **mock 14/14 · real opencode/big-pickle 14/14 (58.1 s, claims=4, score 1.0)** |
| 5 | `langgraph` 1.1.10 installed in `ds0509` | done | compile + invoke verified |
| 6 | K8 env-split decision: single `ds0509`, no split | done | — |
| 7 | Vision-OCR fallback (`qwen3.5:4b think=false` on `ocr_test.png`) | done | 3/3 lines 20.4 s (Ollama-era; archived) |
| 8 | S_lit seed-corpus discovery + L6 deterministic validator | done | fabrication caught; filter runs at write time |
| 9 | Robustness fixes (single-obj wrap, bare cite ID, hallucination filter) | done | archived — qwen2.5:3b-era, removed with Ollama backend |
| 10 | **Default LLM → opencode CLI free model** (`opencode/big-pickle`); Ollama backend **removed** from code (Session 7–8) | done | smoke 3/3 · pipeline 14/14 |
| 11 | **Full-text claim extraction** (S_write reads whole md; `section` attribution) | done | real 14/14 (58.1 s); spot-check: all claims `[high]`, verbatim quotes, correct headings |
| 12 | **Framework integration (Session 9):** STORM-style outline (S_org `outline` → outline-driven S_write) · OpenResearch/orx + arXiv **live discovery rails** (`S_LIT_BACKEND=seed|arxiv|orx`) · **P3 DAS-Bench-style AI judge gate** (`judge.py`, `finalize→gate→judge→END`, `validation.judge`) | done | **mock 19/19 · real opencode/big-pickle 18/18 (121.7 s, outline 3 sections, draft 3357 chars, score 1.0, judge=pass)**; arXiv rail verified reachable (~1 s, 2026-09-16); orx binary absent → wired fallback |
| 13 | **Second real paper — generalization (Session 10):** Weber-Wulff `2306.15666` parsed (MinerU `-m txt` + page windows, K12 workaround; merged md 124,408 chars) + full-loop real run | done | discovery-led → candidates `['2306.15666','2304.02819','1706.03762']` → 4 grounded claims, outline 3 sections, draft 1725 chars, **L6 score 1.0, judge=pass in 149.8 s** |
| 14 | **Benchmark-style evaluation vs DAS-Bench assets (Session 11):** `tools/eval/bench_eval.py` re-implements the 16 criteria verbatim (BSC·MAR·TSQ·HDQ); real pilot on 2 proxy + 2 verbatim DAS topics | done | preview totals **P-A 2.62 / P-B 3.19 / 001 2.44 / 019 no-evidence**; family means BSC 2.83 / MAR 2.25 / TSQ 2.42 / HDQ 3.50 / Total 2.75 vs published 3.2–4.3 → signals: internal P3 judge too lenient, seed-rail precision issue, MAR/multi-ref dominate drag; report `_eval_out/bench_pilot_das.md` |
| 15 | **Multi-paper evidence synthesis P0 (Session 12):** 3rd corpus paper GLTR `1906.04043` parsed (MinerU `-m txt`, 2 windows, distinct-`-o` merge); `resolved_evidence()` multi-paper evidence pool; per-paper grounded claims with `paper_id`; multi-paper S_org/S_write/S_final; seed precision guard + stopwords; fence-tolerant JSON parse; `--auto` headless fix | done | mock 23/23 · real 23/23 (110.8 s); P-A **Total 3.06** papers=3/cited=3 (BSC multi-ref+balance ≥3 met); 001 correctly no-evidence; judge/parser flakiness (fenced JSON) fixed at shared layer |
| 16 | **Survey-depth S_write (Session 13):** per-section drafting (intro + `## <heading>` per outline section + conclusion, inline arXiv attribution, disagreement/gap instructions); S_org outline 4-6 sections; mock INTRO/SECTION/CONCLUSION routes + new asserts | done | mock 25/25 · real 25/25 (498.6 s, draft 16,281 chars, 5 sections, L6 1.0, judge=pass); DAS-16 family means **BSC 3.25 / MAR 2.50 / TSQ 3.17 / HDQ 3.75 / Total 3.17** (up from 2.42 TSQ / 2.75 total, Session 11); artifacts 23-26K chars; residual low axis MAR=figure/table/layout (plain-markdown render limit, honest); report `_eval_out/bench_pilot_das.md` |
| 17 | **P1. P3 judge threshold calibration (Session 14):** 1-5 score anchors in rubric (reserve 5); strict deterministic threshold matrix in `judge.py` — pass requires score≥4 AND all four checks (clarity now mandatory), groundedness=False or score<2 → hard fail; matrix calibrated against DAS-16 preview (score 5 ≈ family Total ~3.2, directional n=1); deterministic `_pick_label` regression added | done | **mock 33/33 · real 33/33** (276.3 s, verdict still pass — strict gate only rejects genuinely weak artifacts); matrix documented in `judge.py` docstring + this row; labelled `matrix v1`, re-baseline flagged when ≥300B frozen judge available |
| 18 | **MAR render axes part 1 (Session 15):** manuscript `_finalize` (Abstract + Evidence Table + References + annex); `tools/eval/render_manuscript.py` pandoc+xelatex CJK PDF render (pypdf pages); bench artifact = manuscript (annex stripped) + judge context 12K→40K (**fix: table/refs were past truncation — judge never saw them**); `pdf pg` report column | done | **mock 34/34 · real 34/34** (243.6 s); PDFs render (P-A 8 pp / P-B 5 pp / P-C 7 pp); MAR fix validated solo P-A Figure/Table **1→3**, MAR 1.75→2.50; canonical combined run **P-A 3.25 / P-B 2.75 / P-C 3.12**, family means BSC 2.92 / **MAR 2.67** / TSQ 2.83 / HDQ 3.75 / **Total 3.04**; Layout axis still 2 (text judge can't see layout; PDFs now substrate for ≥300B judge) |
| 19 | **Data hygiene (Session 16):** bench sidecar cache (`_eval_out/bench_cache/`, vintage-flagged merge when `--scenarios` is a subset — kills the `--out` overwrite trap); P-A/P-C near-duplicate question dedup (P-C → methods-taxonomy multi-paper question) | done | **P-A 3.62 / P-B 3.06 / P-C 4.00** → family means **BSC 3.42 / MAR 3.42 / TSQ 3.42 / HDQ 4.00 / Total 3.56** (best so far); cache helpers unit-probed; 001/019 no-evidence hold |
| 20 | **Track C part 1 — evidence-grounded QA (Session 17):** `qa` scenario family in bench_eval (5 corpus-anchored questions with `gold_tokens` fact-hit flags + `score_qa` correctness/groundedness rubric); qa excluded from DAS family means; mock route; report QA-pilot table | done | 5-Q real pilot **≈25.5 min**: QA mean **correctness 3.80 / groundedness 4.20**, **4/5 correct**; QA-3 cold-miss = "answers the paper, not the question" taxonomy failure (learnable); P-A fresh rerun **3.94** → family means **BSC 3.67 / MAR 3.33 / TSQ 3.42 / HDQ 4.25 / Total 3.67** (n=3) |
| 21 | **Track C part 2 — Qasper end-to-end (Session 18):** dev v0.3 from HF/S3 (paper keys = arXiv ids); 2 new external papers parsed (`1908.10084` SBERT, `1611.03599` UTCNN); fixes — `resolved_evidence` routes on any arXiv id in the question (seed routing), new `tools/pipeline/answer.py` grounded **extractive-answer node** (`seed_id` qa scenarios bypass the survey graph); deterministic `check_answer` L6 gate | done | **QA-6 c 2→5 / g 0→2 gold 2/2** · **QA-7 c 1→5 / g 0→2 gold 2/2** (~16 s/answer); QA-3 (taxonomy) c 1→3 under extractive — synthesis-type questions need multi-paper S_write (documented boundary); **QA pilot n=7: correctness 4.43 · groundedness 4.57 · 6/7 correct**; extractive path 3/3 gold-perfect |
| 22 | **Track C part 3 — QA panel expansion (Session 19):** Qasper +3 papers (`1910.09982`, `1910.06036`, `1908.06267`); **SciQ provided-context `ctx` routing** (`require_cite=False`, `SQ-1..5`); PubMedQA yes/no abstracts + **`yesno` answer mode** (PQ-1..14); one-command corpus adder `add_paper.py` (verified on 12-pp `1703.10344`); QA-scorer truncated-json recovery | done | extract/context path **12/13**; PubMedQA 8/14 (yes/no conclusion = model boundary); **panel n=31 regeneration: correctness 4.23 · groundedness 4.45 · 24/31** |
| 23 | **30-topic evidence-pool battery + judge variance (Session 19b):** `tools/eval/pools_30.py` (all 30 DAS topics, live discovery → windowed parse → incremental manifest, crash-resumable), `tools/eval/variance_run.py`; robustness fixes (`_ID_RE` v-suffix, MinerU subprocess timeout, judge per-topic cache, LLMClient flat retry) | done | **pools 22/30 with ≥1 parsed paper (12 full)**; **10 judged end-to-end → Total 3.13** (BSC 3.08 · MAR 2.67 · TSQ 3.05 · HDQ 3.73); **variance P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13** |

**Known issues resolved:** iteration-accumulator bug (plain dict channel → `Annotated[operator.add]`); mock routing now inspects system+user messages; JSON extraction hardened (parse helpers moved to `validate.py`); opencode Windows cmdline gotchas (prompt via `-f` temp file; message before greedy `-f` flag); Ollama backend removed cleanly (2026-09-16); network correction — export.arxiv.org now reachable (was measured blocked 2026-09-15) → live `arxiv` discovery rail exercised.

## 7. Follow-up plan (recorded 2026-09-16, Session 11; P0/P2 done Session 12) / 后续计划

Priorities are ordered by impact-to-cost; each has a measurable acceptance check.

- ~~**P0. Multi-paper evidence in S_lit** — extend `S_lit` to fetch + parse top-k full texts (arXiv live rail + MinerU `-m txt` windows, reusing the K12 workaround) so the graph can synthesize *across* papers.~~ **DONE Session 12** (evidence pool + per-paper grounding, pilot P-A papers=3/cited=3) + **DONE Session 13** (the *draft-depth* lever: per-section survey drafting lifted family means to **BSC 3.25 / MAR 2.50 / TSQ 3.17 / HDQ 3.75 / Total 3.17**, TSQ 2.42→3.17). Rows 15-16.
- ~~**P1. P3 judge threshold calibration** — calibrate the internal 4-axis judge against the DAS-16 preview scores (internal pass@4–5 vs preview totals ~2.4–3.2 → gate is too lenient). *Accept:* a documented pass/revise threshold matrix (score + axes) + regression in `test_pipeline`.~~ **DONE Session 14**: rubric 1-5 anchors (reserve 5), strict deterministic matrix in `judge.py` (pass = score≥4 ∧ all-four-checks incl. clarity; groundedness=False or score<2 → hard fail), parity map (score 5 ≈ family Total ~3.2, directional), `_pick_label` regression in `test_pipeline`; **mock 33/33 · real 33/33** (verdict still pass — matrix rejects only genuinely weak artifacts). Row 17.
- ~~**P2. Seed-rail discovery precision** — the fuzzy `tool` match wrongly pulled `2306.15666` for DAS topic 001; add a minimum-score threshold + id tie-break.~~ **DONE Session 12**: `SEED_MIN_SCORE=2` + stopword-filtered tokens; topic 001 now resolves to `2409.13740` only → honest no-evidence (no more wrong-evidence scoring of a detection paper).
- **P3. DAS-Bench full compliance (blocked on keys/GPU/network)** — DAS-2M topic pools + gold PDFs (Hugging Face), rendered-page MAR scoring, and a ≥300B frozen judge (or the config's local OpenAI-compatible endpoint); then run the vendored `evaluation/run_eval_all.sh` and report honestly per `evaluation_protocol.md`. **Pipeline substrate for MAR is in place since Session 15 (manuscript markdown + rendered PDFs under `_eval_out/manuscripts/`); the remaining gap is the page-aware judge + pools.**
- **P4. Cooldown items** — Track B (PaddleOCR) wiring into the proactive loop; robustness ablations + cost report (P5).

Kept in sync with the "Next:" lines at the top of each PROGRESS session entry.

## 8. Next-implementation plan (recorded 2026-09-20) / 后续实现规划

> 中文速览：本计划按**四条并行工作流（workstream）+ 各自的评估门**组织，而不是线性阶段——后端、前端、自演化可以同周开工，各自的验收各自可测（见下 Workstream map）：
> - **WS-A 核心管道（Phase L）**：本地 ≈$0，现在可做——(L-1) S_write 检索重排（PaperQA2 RCS 轻量复刻）、(L-2) S_org 多视角分解（STORM 思想）、(L-3) 判题 median-of-3（压 judge 噪声，P-A ±0.53）、(L-4) 引用校验接线。评估门 = bench/variance 回归数字。
> - **WS-B 前端与后端壳（Phase F）**：单机观测台 FastAPI + HTMX/SSE + 模型路由（WS-D 依赖的唯一接口是**稳定 CLI 入口 + `_eval_out/*.json`**，可与 WS-A 并行开工）。评估门 = F 项验收（SSE 实时进度 / 可取消 / 只读降级）。
> - **WS-C 自演化（Phase X）**：基线冻结 + 健康检查 + 变异加固 + 周更节奏，**数据已存在**（E-1 基线数字当前全可测），与 L 项解耦可先行。评估门 = E 项验收（GREEN/WARN/FAIL、gate_coverage、次数/阈值规则）。
> - **WS-D 模型接入与路由（Phase D，新增，2026-09-20）**：回答"前端靠什么模型跑"——**两者皆可**：`opencode` 注册免费托管模型（零 key、默认）+ 主流模型 API key（DeepSeek / DashScope(Qwen) / Kimi(Moonshot) / OpenRouter 等，全部走既有 `openai` backend）。设计为**按角色的 backend 配置文件（profiles）**：草稿/QA 走廉价 lane、判题走强模型 lane（D-3 解耦 judge），前端只读 profile、永不存 key。评估门 = 每 profile 过 mock 回归 + 跨模型判题矩阵。
> - **WS-R 资源门控（Phase R）**：官方 DAS-Eval / DAS-2M / knowledge-storm / orx，需 ≥300B judge 端点/GPU/key——WS-D 的强模型 lane 先铺路。
>
> 每项带可度量验收；WS-A/B/D 的合入必须过 WS-C 的健康检查（基线回归），WS-C 的"演化"主张必须经 WS-D 跨模型验证。

**Workstream map (parallel + evaluated) / 并行工作流与依赖**

| WS | Lane | Ships (items) | Blocking dep | Evaluation gate | Can start |
|---|---|---|---|---|---|
| A | core pipeline | L-1..L-6 (Phase L) | none (code exists) | bench_eval + variance vs 2026-09-20 baselines | now |
| B | web frontend/backend shell | F-1..F-4 (Phase F) | stable CLI + `_eval_out` I/O only | F acceptances (SSE/ cancel/ fallback) | now, parallel to A |
| C | self-evolution cadence | E-1..E-7 (Phase X) | baselines (measured) | health verdicts + gate_coverage + promotion rules | now, parallel to A |
| D | model access & routing | D-1..D-5 (Phase D) | LLMClient (exists) | per-profile mock 34/34 + cross-model judge matrix | now (keys optional) |
| R | resource-gated | R-1..R-6 (Phase R) | strong judge lane (D-3) / GPU / keys | official vs self delta table | after D-3 or keys |

Systemization rule (AGENTS.md-aligned, recorded so it can't drift): **no BD (frontend) commit may regress the C (baseline) verdicts; no C "improvement" claim is valid without a D (cross-model) check.** Each workstream logs into PROGRESS under its own heading so sessions can interleave.

Sorted by impact-to-cost; each item carries a measurable acceptance check.

### Phase L — Local, ≈$0, do now (dependency-free)
- **L-1. S_write relevance re-rank (mirror PaperQA2 RCS)** — before per-paper claim extraction, score sentence/paragraph windows against the question(s) with a cheap lexical (BM25-style / overlap + section-prior) ranker; inject only top-k windows into the extraction LLM call. *Rationale:* our worst retrieval gap — we feed the raw first ≤20 000 chars of each paper instead of the *relevant* passages. *Accept:* on P-A/P-B/P-C + QA-1..5, extract/context QA keeps 12/13; groundedness 4.45 not regressed; claims-wall-sheet verbatim 5-gram gate 34/34; and on a topic where the answer is mid-paper (e.g. QA-3 counterpart), measured pass shifts from cold-miss to hit without taxonomy surgery. *Fallback:* keep raw window + section log, so worst case = no harm.
- **L-2. S_org perspective decomposition (STORM-inspired, prompt-only)** — `_org` first asks for 3–5 reader perspectives (with the user-provided question as anchor), then answers each per-paper-window, then produces the outline (STORM's max_turn×(max_perspective+1) QA budget, re-implemented at low scale). *Accept:* outline `key_points` coverage judged ≥2 on 2 previously-thin topics, family Total not lowered; no new determinism/lint regressions.
- **L-3. Judge median-of-3 aggregation** — run each bench judge call 3× (3 flat retries exist in LLMClient) and take the **median** of the 4-axis verdict; keep single-call in pipeline runtime. *Accept:* P-A judge sd < 0.40 across 3 rounds (from 0.53), P-B stays 0.00, reported family means restated with medians.
- **L-4. (Easy) wire `citation-verification` locally installed skill** into the assembly guidance (agent-side checklist), no code change; and expose the 220-survey rubric anchors as judge few-shot calibrators (skip — needs PDF parse, park in Phase R).
- **L-5. Tool-usage documentation (工具使用方法入档)** — maintain a **per-tool usage cheat-sheet** in `docs/setup-runbook.md` §3 (expand the one-command inventory): for each tool actually used (MinerU `-m txt` windowed · arXiv API rails · `pandoc`+`xelatex` CJK render · opencode CLI backends · `langgraph` · `bench_eval`/`pools_30`/`variance_run`/`add_paper`/`answer`), record *purpose · verified command · version pin · worked example output · known issue K#*. Cross-link from `docs/TOOL-COMPARISON.md` §2 and `docs/DATAFLOW-AND-REUSE.md`; keep it in the "executed" (not "borrowed") set.

  *Accept:* a fresh agent can reproduce every pipeline stage (parse → pool → draft → render → bench → variance) from the runbook alone, and `rg` a stale-command sweep against the verified-command list returns zero docs hits (commands the LLM client no longer supports, e.g. old Ollama/env vars, are removed or flagged `superseded`).
- **L-6. (optional) Evaluation-one-command** — bundle `bench_eval --scenarios` + `variance_run` + `health_check` (below) behind a single `tools/eval/self_check.ps1` runner so the cadence is one command. *Accept:* one command reproduces the health report; exit code reflects GREEN/WARN/FAIL.

### Phase D — Model access & routing (backend profiles) / 模型接入与路由 (2026-09-20)

> 中文速览：**结论——前端/后端跑什么模型，`opencode` 注册与主流 API key 两条路都支持，设计成"按角色路由、key 永不入库"**：
> - `tools/llm/client.py` 已实现两种 backend：`opencode`（CLI 调 opencode 免费托管模型，默认 `opencode/big-pickle`，零 key）与 `openai`（任何 OpenAI 兼容端点：DeepSeek / DashScope(Qwen) / Moonshot(Kimi) / OpenRouter / OpenAI / 本地服务）。**注册 options**：`LLM_BACKEND`、`OPENCODE_MODEL`、`OPENAI_BASE_URL`、`OPENAI_MODEL`、`OPENAI_API_KEY`（client.py:22-27）。
> - **现状判题与草稿共用一个 client/judge 模型**（judge.py:9-10,71）→ 噪声源之一（P-A ±0.53 有一部分是免费小模型判题导致的）。因此新增 **角色级路由**：`draft`(S_org/S_write/answer) 走廉价 lane，`judge`(判题/健康检查) 走强模型 lane。
> - **仅 Java/无 key 约束不变**：默认 `opencode` 免费；入 D-3 后可把 judge 切到已注册的强模型，同时草稿仍走免费 lane——对标 DAS 惯例（judge 用 ≥300B 级）且不破坏"本地零成本"属性。key 只从环境变量读取，前端进程只读 profile 名，**不代理、不存储任何 key**。

**D-1. Profile registry (`tools/llm/profiles.py`)** — named, immutable backend profiles read from env at startup (no keys in code/repo, `AGENTS.md` secret policy):
- `free-opencode` (default): all lanes → opencode `opencode/big-pickle`, via `OPENCODE_MODEL`.
- `judge-strong` (user-configured): `draft|qa` → opencode (or `OPENCODE_MODEL`), `judge` → `OPENAI_BASE_URL`/`OPENAI_MODEL`/`OPENAI_API_KEY` (any OpenAI-compatible provider the user registered).
- `swap-opencode` build: `opencode --version` reachable (no key) | `openai` needs `OPENAI_API_KEY`.
- The profile is a plain dict `{lane: {backend, model, base_url}}`; unknown env value → loud failure (recorded in PROGRESS), never silent fallback. *Accept:* running `bench_eval`/`health_check` with a profile emits a header line showing per-lane model; switching `OPENAI_MODEL` re-routes only the judge lane. — 2026-09-20 **implemented** (`dataclass(frozen=True)` + `ProfileError` loud failure; `free-opencode` default + `judge-strong` with `OPENAI_*`; `load_profile()`/`clients_for()`/`profile_header()`).
- **D-2. Per-role routing in callers** — `bench_eval.py`, `variance_run.py`, `health_check.py`, and the web runner (F-1) construct **two** LLMClients from the profile: `draft_client` (pipe/QA) and `judge_client` (scoring). `judge.py:71` gains a `client=` param (already threaded in pipeline default); `score_*` functions in `bench_eval.py` accept the judge client explicitly. *Accept:* a run + judge can use different models; every artifact still records `judge_model` (provenance preserved). — 2026-09-20 **implemented** (draft/judge clients built from `clients_for(profile)` via `--profile`; `Pipeline(client, judge_client=...)` routes P3 judge; mock regression 34/34 PASS with routing active).
- **D-3. Strong-judge lane (unlocks R-1/R-6/E-7)** — when the user registers a ≥300B-class OpenAI-compatible model (e.g. DeepSeek/Qwen/Kimi/OpenRouter frontier), run the **judge lane** through it and measure judge-variance compression on P-A/P-B/P-C (target P-A sd < 0.40 vs 0.53 with median-of-3, L-3). This is the cheapest *model-side* lever on credibility; requires only env vars, no code migration. *Accept:* variance table before/after; then R-1 official DAS-Eval uses the strong lane with the vendored harness.
- **D-4. Cross-model awareness** — treat any registered model as a **replaceable judging vantage** (E-7 adjudicator swap, and already-measured cross-judge disagreement: internal Qwen-vs-Kimi ?=0.507/MAE=0.630, PROGRESS). Record `model`+`judge_model`+`temperature`+profile name in every report footer so a score claim is always attributable to a specific model behind it.
- **D-5. Cost & key hygiene** — report per-run token/cost when the backend exposes usage (opencode returns cost in step_finish; openai returns usage). Keys exist only as env vars, never in git or the web bundle; the frontend (Phase F) never sends/reads key material — the server process owns the env. *Accept:* `rg` finds zero key/literal in repo; a fresh agent reproduces a run with profile via env only.
- **Explicit not-planned:** local-model lanes are removed (Ollama gone 2026-09-16); no multi-key load-balancing or auto-retry across providers (keep the failure model simple); no paid-API gateway dependency.

### Phase R — Resource-gated (≥300B judge endpoint / GPU / API key / FB bandwidth)
- **R-1. Official DAS-Eval run (highest-value, blocked on judge)** — run the vendored `external/DAS` evaluation code (`evaluation/run_eval_all.sh` per `evaluation_protocol.md`) against our rendered manuscripts (substrate ready since Session 15) once an OpenAI-compatible ≥300B / page-aware judge endpoint is available. *Accept:* honest official-vs-self-scored delta table.
- **R-2. DAS-2M metadata-lake discovery rail** — optional `S_LIT_BACKEND=das2m` reading the HF 2M-paper lake (streamed) to widen Track A discovery beyond arXiv relevance top-K. *Accept:* pools coverage 22/30 → ≥26/30 on Drive A with same evidence truth.
- **R-3. knowledge-storm module swap for S_org (Co-STORM / VectorRM)** — `pip install knowledge-storm` (MIT) and use its OutlineModule + VectorRM (grounding on user docs) via a litellm OpenAI-compatible endpoint; compare vs L-2 prompt version on the same 2 topics. *Accept:* outline + 3-axis judge at parity or better than L-2, with dependency/lightweight trade-offs documented.
- **R-4. orx enablement** — install orx (Windows beta; Git for Windows dep), enable dormant `S_LIT_BACKEND=orx`, adopt `orx install-skills` into OpenCode for the *agent* lane (its workspace orchestrates agents, not our LangGraph — keep our loop). *Accept:* `orx discover/paper` returns ≥3 verified candidates on 1 topic that the arXiv rail missed.
- **R-5. paper-qa backend adoption (optional heavy)** — full agentic RAG (RCS + citation traversal) as an *alternative* `answer.py` backend for Track C; baseline vs our extractive path on QA-1..14. *Accept:* ≥12/14 correct with groundedness ≥4.5 before switching.
- **R-6. Judge calibration corpus** — parse a subset of the 220 published DAS surveys as few-shot rubric anchors (needs MinerU parse + storage).

**Explicitly not planned:** deeper STORM/PaperQA2/agent-rollups *inside* the core loop (destroys the "zero external framework at runtime" property), whole-draft revise_para rescope (low measured value), and any paid-API dependence before Phase R keys exist.

### Phase X — Tool self-evolution (maintenance cadence) / 工具自我演化机制

> 中文速览：把"自我演化"落地为一个**可定时、可度量、人工在环**的维护机制——不是自动改代码，而是四件事：(1) **基线冻结**（把已测数字固化为基线文件）；(2) **健康检查脚本**定期重跑子集并对照基线，漂移即 FAIL/WARN；(3) **演化冲刺节奏**（每周：跑 checks → 开/关调试图 → 只写 PROGRESS，改动需显式放行）；(4) **版本与依赖台账 + 反馈累积**（每次判题/纠错入账，见回落差才升 judge 矩阵或 prompt 版本）。配套工具使用方法入档（L-5）与单命令自检（L-6）。**设计依据与证据见 `docs/design/self-evolution-mechanism.md`（2026-09-20 一手调研）**；两条设计规则在此强制：(a) **演化触发只能来自外部测量**（判题/接地门/变异注入），从不"让模型自觉变好"（Huang et al. 2023：内在自校正对推理无效甚至有害；GPT-4 定位逻辑错误仅 52.9%）；(b) **任何演化信号必须先过方差感知阈值**（判题噪声实测 ±0.53 → 依赖 L-3 judge 中位数）。诚实边界：本轨道的"自我演化"= 调度测量 + 回归检测 + 人工在环修复 + 版本化反馈，**不包含**任何自动 commit、权重更新或无人值守 prompt 演化。

The goal is a *measurable, scheduled, human-in-the-loop* evolution loop — the opposite of autonomous code-rewriting (which violates the repo's "no unsolicited commits" rule). It maps the canonical four-phase self-evolution cycle (**experience acquisition → refinement → updating → evaluation**, Tao et al. 2404.14387) onto our measured environment, and markets the two strongest evidence-backed mechanisms: (i) **token-space "skill library" memory** (Reflexion 2303.11366 · Voyager 2305.16291) = versioned runbook + tickets + feedback corpus; (ii) **metric-gated programmatic prompt evolution** (DSPy 2310.03714 · GEPA 2507.19457) = manual mini-version to start, automated only when a strong reflection LM exists (Phase R).

- **E-1. Baseline freeze (基线冻结)** — write current measured values as a machine-readable baseline (`_eval_out/baselines.json`): mock regression 34/34 · panel n=31 (correctness 4.23 / groundedness 4.45 / 24/31, extract 12/13) · pools 22/30 (14 full) · judged sample Total 3.13 (BSC/MAR/TSQ/HDQ) · variance P-A±0.53 / P-B±0.00 / P-C±0.13 · per-topic judged scores. *Accept:* baseline loaded by health check; extended with `gate_coverage` once E-2b lands. — 2026-09-20 **implemented** (built into `health_check --freeze`, zero-LLM; `baselines.json` committed).
- **E-2. Health-check script (`tools/eval/health_check.py`)** — each cycle re-runs a **frozen subset** (fixed scenarios, never curated retroactively to pass — the DriftBench/Evidently reference-vs-current rule): mock regression (deterministic, ~2 min) + 1 proxy variance round + pool-coverage re-scan (arXiv reachability probe) + judge sanity on one cached topic. Emits GREEN/WARN/FAIL vs baselines with **variance-aware thresholds**: mock 34/34 = hard gate; Total Δ ≥ 2σ (≈±0.50) = FAIL, ≥ 1σ (≈±0.26) = WARN (σ = recorded judge noise per proxy; P-A 0.53 → its own 2σ); pool coverage −10% of recorded = WARN. *Accept:* <10 min/cycle, exit code reflects verdict, failures link to the PROGRESS row that last touched the affected component. — 2026-09-20 **implemented**; first full cycle measured: mock PASS · pools PASS (22/30, full 14) · arxiv_probe PASS · gate PASS · judge P-A 0.4σ PASS / P-B 1.3σ WARN / P-C 1.7σ WARN → **exit 1 (WARN)**; σ floor 0.10 for recorded zero variance; `--quick` skips the <10 min judge sanity; `--freeze` regenerates `baselines.json`.
- **E-2b. Gate-coverage mutation check (`gate_coverage`)** — each cadence, synthesize mutated claim/quote/citation strings (swapped verb, broken 5-gram, reordered cite ID, dropped bilingual sentence) and assert the **deterministic L6 gate rejects every mutant**; kill-rate recorded as `gate_coverage` in baselines. *Accept:* gate_coverage = 100% on ≥20 mutants per cadence; any surviving mutant → debug ticket (fix the gate, not the prompt). Zero-LLM, minutes — the highest-value/lowest-cost "evolutionary" act available (rationale: LLMs cannot reliably find their own errors, Tyen et al. 2311.08516). — 2026-09-20 **implemented** in `health_check.gate_coverage`; 23 mutants (token-level gap-1 interleave × 8 source sentences + 4 synthetic negatives + 3 structure breaks + 4 bad cites + 4 keep-controls) → **kill rate 100%**; mutation debugging caught two real L6 leak paths (token-level vs word-level interleave on `<sup>…</sup>` markup; structure-break mutants re-seeding dropped keys) — gate fixes, not prompt fixes.
- **E-3. Evolution cadence (演化冲刺)** — standing weekly item (logged in PROGRESS like any session): run E-2 + E-2b → diff vs baselines → open/close **debug tickets** (one line each: symptom → measured delta → hypothesis → fix class) → version-bump baselines on any confirmed shift. Code/prompt changes **only** after explicit user green-light; the loop itself writes only to PROGRESS/baselines/JSONL. *Accept:* each cadence run produces a dated health line + ticket list, reviewable in one screen.
- **E-4. Version & dependency ledger (台账)** — pin every runtime guardrail in the runbook (MinerU · langgraph · pandoc · xelatex · opencode CLI/model availability · arXiv API endpoint) and re-verify per cadence (export.arxiv.org was a false-block; the free backend can change silently). Any pin change → run E-2 before and after; log both numbers; attribute score deltas to *backend/model* as well as prompts. *Accept:* ledger shows version + last-verified date per tool; no dangling expectations about removed backends.
- **E-5. Feedback accumulation → versioned prompts/judges (manual mini-GEPA)** — every judged run and every user correction is logged (JSONL under `_eval_out/feedback/`), **provenance-tagged and anchored to real primary sources** (parsed papers, gold tokens) with a floor quota of real ground truth per cadence — the anti-model-collapse rule after Seddik et al. 2404.05090 (mixing real data within a bound avoids collapse). When evidence shows a consistent, *non-noise* delta, bump a **numbered revision** of the affected prompt/judge (judge matrix v1 → v2). **Promotion rule:** requires N≥3 rounds, Δ ≥ 2σ, no mock/gold regression, and (Phase R) survival against an adjudicator swap. Prompts/judges are versioned, revertable, never ad-hoc. *Accept:* full bump history in PROGRESS; each revision re-baselined before/after.
- **E-6. (R-phase) Schedule & alerting** — promote E-2 to a scheduled job (Windows Task Scheduler / pre-commit hook) with a one-line alert channel, keeping the frozen subset fixed. *Accept:* health degrades → human notified within one cadence without manual invocation.
- **E-7. (R-phase) Automated prompt evolution + adjudicator swap** — when a strong OpenAI-compatible reflection LM exists, optionally compile the loop via **DSPy/GEPA** (GEPA: beats GRPO up to 35× cheaper on text feedback, arXiv:2507.19457) and add a second, independent judge so promotions must survive a different vantage. *Accept:* measured ≥1σ gain on frozen subset vs manual versioning, with mock/gold non-regression; otherwise revert to manual.

**Honest boundary** (recorded so it can't be overstated): "self-evolution" here = *scheduled measurement + regression detection + mutation-hardened gates + human-gated repair + versioned feedback* — deliberately **not** autonomous code mutation, weight updates, auto-commit, or unattended prompt evolution; those would contradict `AGENTS.md` (no unsolicited commits) and the human-checkpoint doctrine in the blueprint (§0, §L6). Evidence and failure-mode analysis: `docs/design/self-evolution-mechanism.md`.

### Phase F — Local web frontend / 本地 Web 前端 (2026-09-20 analysis)

> 中文速览：给这条 CLI 管道加一个**本地读观测台**（localhost 单机，≈$0）——不必做成产品 UI，目的：(1) 把 `_eval_out/` 的曲线、报告、判题 feedback 变成人可读的页面；(2) 照 demo（runbook §3.1）一键触发 `bench_eval`/`pools_30`/`variance_run`/QA，浏览器里看实时进度（SSE），长跑可取消；(3) 是 Phase X 自演化节奏（E-2 健康检查、E-3 ticket）与 L6 人工评审的自然落点。**结论：需要 FastAPI（不用 Flask，也暂不做无后端纯静态页）**，理由见下"是否需要的评估"。前端=服务端渲染 Jinja2 + vanilla JS `EventSource`（SSE；零外部 JS、零 Node 链，网络不稳 K1/K2 下零外部依赖优先于 htmx —— 2026-09-20 落地时实测如此），Pydantic 模型直接映射现有 `tools/pipeline` 状态与 `_eval_out/*.json` 结构。

**Is a web backend needed at all? / 是否需要后端——评估**
- **纯静态无后端（直接读 `_eval_out/*.json`+`.md`）**：能展示既有报告（只读），但无法触发展评/判题、无法流式进度、无法取消长跑，也拿不到 live 的 judge checks 的一手 JSON。只满足"看上次的结果"，不满足"点一下开跑并看进度"→ **不满足需求**，仅可作降级方案（F-3 可顺带提供）。
- **Flask（WSGI 同步）**：内建 Jinja2，极轻量、SSE/长任务要靠线程 + 手动 stream，无类型校验（需 marshmallow），无自动 OpenAPI。对本场景的致命点：一次真实 bench 跑 2–8 min，同步 worker 会阻塞同线程其他请求；做"实时进度 + 并发多任务"要额外手工线程/队列 ≥ FastAPI 原生 async 的复杂度，却不给类型与文档收益 → **不选**。
- **FastAPI（ASGI + Uvicorn）**：原生 async → SSE/WebSocket 进度流、长任务不阻塞、支持并发触发；Pydantic v2 把 `_eval_out` 与 pipeline state 自动校验/序列化；自动 OpenAPI/Swagger。本地单用户对性能无压力，但 async + 类型 + 文档是"零额外成本"的结构性收益。Flask 15 年扩展生态与 68k-78k stars 对本单机工具无价值（对比方向性数字见下）。→ **选 FastAPI。**
- **Gradio / Streamlit（demo 优先）**：秒级起步、自动组件，但弱类型、页面结构与"观测台+SSE"控制力不足，且把我们锁在库自己的渲染模型 → 仅适合一次性 demo，不留作正式落地；可在 F-1 评估期顺手跑一次对比再弃。
- *方向性来源（二手、仅供决策）*：Flask WSGI 同步 / FastAPI ASGI async，Flask 无内建校验、FastAPI 内建 Pydantic+OpenAPI（dev.to 2025-02-05 · PlainEnglish 2023-08-24）；吞吐对比 FastAPI 约 3–7×（tech-insider 2026-04-02 · ByteIota 2025-12，量级方向性）；FastAPI 星数 ~78–82k vs Flask ~68k（2026-04）。一手核证原则记 AGENTS.md：本决策依赖框架常识，不依赖具体榜单数字。

**F-1. Backend scaffold (`tools/web/app.py`)** — FastAPI app (uvicorn), **bind `127.0.0.1` only**, no new deps beyond `fastapi`+`uvicorn` in `ds0509`. Routes: `GET /` (dashboard: baselines from E-1, last health verdict, `_eval_out` index) · `GET /runs` (list of recorded scenarios + verdicts) · `POST /runs` (trigger one scenario set → returns `run_id`) · `GET /runs/{id}/events` (SSE progress stream; reuses `LLMClient` backend, exposes live judge checks) · `DELETE /runs/{id}` (cancel — cooperative flag checked between nodes, like the pipeline's existing retry loop) · `GET /manuscripts/{id}.pdf` (L6 human review) · `POST /feedback` (append JSONL → `_eval_out/feedback/`, E-5 ingestion). Jinja2 templates + vanilla JS `EventSource` for SSE (no htmx dependency; inline CSS, zero external JS — network flakiness K1/K2 makes a vendored-CDN copy worse than no external asset) — **no Node toolchain**. *Accept:* `python -m uvicorn tools.web.app:app --port 8787` serves the dashboard; a fresh agent can read run PROGRESS/verdict/feedback for any scenario without touching the terminal. — 2026-09-20 **implemented** (`tools/web/app.py` + `run_manager.py`); TestClient smoke: 4 pages 200, `test_pipeline mock` streamed 38 SSE lines → done rc=0, real-run cancel tree-killed with no orphan python.
- **F-2. Progress + cancel on a real run (the one thing Flask wouldn't give cheaply)** — SSE pushes node transitions (S_lit→S_org→S_write→S_final→gate→judge) of a **live** `bench_eval`/`test_pipeline real` (2–4 min) plus E-2 health verdict. *Accept:* browser shows live stage map + 5-gram gate pass per claim + final judge checks; a started real run can be cancelled from the page and the terminal process exits (no orphaned subprocesses).
- **F-3. Passive fallback** — offer a **read-only** mode that serves just the rendered `_eval_out` index + latest reports (no POST) as the no-backend equivalent, so the dashboard degrades gracefully if uvicorn/deps are missing. *Accept:* README/runbook entry documents fallback; page loads without POST routes enabled. — 2026-09-20 **implemented** (`tools/web/export_static.py`); regenerates `gh-pages/` (3 pages + candidate `manuscripts/*.pdf` copies wrapped in HTML + `.nojekyll`), stdlib-only (no uvicorn/fastapi) so it also serves as the GH Pages deployable; verified: 44 pdfs exported, `python -m http.server` serves all 4 paths 200. Deploy = GH Pages `branch: main / folder: /gh-pages`.
- **F-4. Wiring into cadence** — the dashboard is the visible surface of Phase X: E-2 health verdict, E-3 debug tickets, E-4 ledger snapshots, E-5 feedback log are all readable on one local URL. *Accept:* running the weekly cadence end-to-end (checks → tickets → next-row) can be done from the dashboard once F-1/F-2 land; it never pushes to any remote, keeps `127.0.0.1` binding (auth added only if exposed beyond localhost — explicit scope boundary).

Kept in sync with the "Next:" lines at the top of each PROGRESS session entry.