# Research Foodie — Execution Plan (执行计划)

> 中文速览：本计划分三部分——(A) 校对 `docs/refs/ai-research-tools-workflow-guide.md` 并建立"验证台账"；(B) 修订该指南（补参考文献、修正已确认的错误、增补开源工具）；(C) 编写 `docs/design/research-foodie-blueprint.md` 架构蓝图（复用 OpenResearch / STORM / DAS / PaperQA2 / MinerU，本地优先 + 廉价 API）。纯文档交付，不写代码。所有事实声明一律回到一手资料。

- `Updated`: 2026-09-16
- `Status`: **Tasks A–D complete. P1 tooling complete; P2 minimal vertical GREEN + framework integration + generalization; benchmark-style evaluation pilot done (Session 11)** — MinerU ✓, PaddleOCR ✓ (K7 closed), LLM client ✓ (default `opencode` backend, `opencode/big-pickle`; OpenAI-compat; **Ollama backend removed 2026-09-16**); `langgraph` 1.1.10 installed; `tools/pipeline/` P2 live: **S_lit pluggable discovery rails (seed | arXiv API | orx CLI; arXiv verified reachable 2026-09-16)** + full graph + L6 deterministic gate + write-time grounded-claim filter + full-text claim extraction; **STORM-style outline + DAS-Bench-style AI judge gate integrated (Session 9)**; **mock 19/19 + real `opencode/big-pickle` 18/18 (121.7 s, score 1.0, judge=pass); 2nd real paper (Weber-Wulff `2306.15666`) PASS in 149.8 s — generalization proven; DAS-Bench 16-criterion pilot (`tools/eval/bench_eval.py`) — preview totals 2.44–3.19 vs published 3.2–4.3, report `_eval_out/bench_pilot_das.md`**. Next: multi-paper evidence in S_lit (MAR/multi-ref drag) + P3 judge calibration against DAS-16 + DAS-2M/≥300B judge for a compliant submission.
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

**Known issues resolved:** iteration-accumulator bug (plain dict channel → `Annotated[operator.add]`); mock routing now inspects system+user messages; JSON extraction hardened (parse helpers moved to `validate.py`); opencode Windows cmdline gotchas (prompt via `-f` temp file; message before greedy `-f` flag); Ollama backend removed cleanly (2026-09-16); network correction — export.arxiv.org now reachable (was measured blocked 2026-09-15) → live `arxiv` discovery rail exercised.

## 7. Follow-up plan (recorded 2026-09-16, Session 11) / 后续计划

Priorities are ordered by impact-to-cost; each has a measurable acceptance check.

- **P0. Multi-paper evidence in S_lit** — extend `S_lit` to fetch + parse top-k full texts (arXiv live rail + MinerU `-m txt` windows, reusing the K12 workaround) so the graph can synthesize *across* papers. *Why:* the DAS-Bench pilot shows MAR / Multi-Reference Synthesis dominate the drag (preview Total 2.75 vs published 3.2–4.3); single-paper artifacts cannot reach survey-level. *Accept:* ≥3 papers per topic in evidence; Multi-Reference + Balance criteria ≥3 on the pilot topics.
- **P1. P3 judge threshold calibration** — calibrate the internal 4-axis judge against the DAS-16 preview scores (internal pass@4–5 vs preview totals ~2.4–3.2 → gate is too lenient). *Accept:* a documented pass/revise threshold matrix (score + axes) + regression in `test_pipeline`.
- **P2. Seed-rail discovery precision** — the fuzzy `tool` match wrongly pulled `2306.15666` for DAS topic 001; add a minimum-score threshold + id tie-break. *Accept:* topic 001 no longer resolves to the detection paper.
- **P3. DAS-Bench full compliance (blocked on keys/GPU/network)** — DAS-2M topic pools + gold PDFs (Hugging Face), rendered-page MAR scoring, and a ≥300B frozen judge (or the config's local OpenAI-compatible endpoint); then run the vendored `evaluation/run_eval_all.sh` and report honestly per `evaluation_protocol.md`.
- **P4. Cooldown items** — Track B (PaddleOCR) wiring into the proactive loop; robustness ablations + cost report (P5).

Kept in sync with the "Next:" lines at the top of each PROGRESS session entry.