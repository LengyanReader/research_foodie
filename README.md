# research_foodie

A **local-first, cost-sensitive proactive academic research pipeline** that turns a research question into a *citation-grounded* draft — every sentence traceable to a parsed paper, every gate mechanical before it is human.

> 中文版见 [`README.zh-CN.md`](README.zh-CN.md). Complete overview (goals · components · workflow · measured status): [`docs/PROJECT.md`](docs/PROJECT.md).

Updated: 2026-09-16 · License: MIT

## What this project does

- Takes a research question (or a field watch) and produces an outline-driven, **bilingual (EN + 中文)** draft.
- Grounds every factual claim in a **verbatim quote** from a locally parsed paper (arXiv) — a deterministic 5-gram gate blocks hallucinated quotes mechanically, before any LLM review.
- Runs as a LangGraph state machine: `S_lit → S_org → S_write → S_final → L6 gate → P3 judge → human`.
- Is **cost-sensitive**: the core loop runs on open-source tooling and free/open LLM access (core cost ≈ $0).

It is **not** a black-box "deep research" product: it never auto-ships a manuscript. Mechanical validation runs before AI review; AI revises, humans approve (blueprint §0).

## Pipeline at a glance

```
[L0] Question / field watch
  ▼
[L1] S_lit   discovery rails (seed manifest · arXiv API · orx CLI) → candidates
  ▼
[L2] Evidence  MinerU PDF→Markdown → multi-paper evidence pool (per-paper grounding)
  ▼
[L3] S_org   taxonomy + STORM-style outline (sections + key_points)
  ▼
[L4] S_write   per-paper evidence-backed claims (verbatim quotes) → cross-paper draft
  ▼
[L5] S_final   assembled output (Sources + per-claim attribution)
  ▼
[L6] Gates    deterministic validation → DAS-Bench-style AI judge → HUMAN checkout
  ▼
Manuscript  (Zotero + Pandoc + LaTeX)  ·  Track B: OCR + translation with expert gate
```

Current implementation delivers the **P2 minimal vertical** end-to-end (question → grounded draft → validated artifact); the proactive *stale → re-discovery* loop and full DAS-2M/live sweeps are roadmap items.

## Quickstart

Environment is a conda env `ds0509` (Python 3.12, Windows). Use that interpreter explicitly:

```powershell
$PY='C:\Users\data\miniconda3\envs\ds0509\python.exe'
```

**Run the integration test** (mock = deterministic regression in seconds; real = full opencode-LLM loop):

```powershell
& $PY -m tools.pipeline.test_pipeline mock      # 25/25 PASS
& $PY -m tools.pipeline.test_pipeline real      # default model opencode/big-pickle (~8 min, 10 LLM calls)
```

**Demo questions:** *"GPT detectors bias against non-native English writers"* (Liang et al. 2023) and *"How reliable are automatic detection tools for AI-generated text?"* (multi-paper pool: Liang + Weber-Wulff + GLTR).

**LLM backends** (`tools/llm/client.py`): `opencode` by default (hosted free model via `opencode run --format json`); `openai` for any OpenAI-compatible endpoint (DeepSeek / DashScope / OpenRouter / Moonshot / OpenAI). Set via `LLM_BACKEND` / `OPENCODE_MODEL` / `OPENAI_BASE_URL` / `OPENAI_MODEL` / `OPENAI_API_KEY`.

**Discovery rail** (manifest default): `$env:S_LIT_BACKEND='seed'|'arxiv'|'orx'`.

**Parse a paper** (MinerU; use page windows ≤6 pp for long/OCR-heavy PDFs, see runbook K12):

```powershell
& 'C:\Users\data\miniconda3\envs\ds0509\Scripts\mineru.exe' -p paper.pdf -o mineru_out_ds0509 -b pipeline -m txt -s 0 -e 5
```

**Benchmark-style evaluation** (16 DAS-Bench criteria re-implemented verbatim):

```powershell
& $PY -m tools.eval.bench_eval --backend opencode --scenarios P-A,P-B,P-C,001,019 --out _eval_out/bench_pilot_das.md
```

## Status

- **Phase 0/1 (docs)**: complete. **P1 tooling**: MinerU PDF→Markdown PASS; PaddleOCR Chinese OCR PASS (K7 closed).
- **P2 minimal vertical + framework integration (GREEN)**: LangGraph pipeline with pluggable S_lit rails (seed / arXiv API — verified reachable 2026-09-16 / orx CLI), multi-paper evidence pool (`resolved_evidence`, 3 local parses), per-paper grounded claims (`paper_id` attribution), STORM-style outline (4-6 sections), **survey-depth per-section drafting** (intro + `## <heading>` section paragraphs + conclusion, inline arXiv attribution, disagreement/gap handling), **manuscript output** (Abstract / Evidence Table / References) + **local PDF rendering** (`tools/eval/render_manuscript.py`, pandoc+xelatex CJK), L6 deterministic gate (+ informational `multi_paper` metric), DAS-Bench-style AI judge (strict matrix v1).
- **Tests**: mock **34/34** · real `opencode/big-pickle` **34/34** (real ~4–8 min; strict judge verdict=pass).
- **Evaluation pilot** (`tools/eval/bench_eval.py`, Sessions 11–16): canonical (sidecar-cached, `--out` no longer overwrite-trap) — **P-A 3.94 / P-B 3.06 / P-C 4.00**, family means **BSC 3.67 / MAR 3.33 / TSQ 3.42 / HDQ 4.25 / Total 3.67** (n=3; run-to-run variance ±0.3 documented). MAR lifted by the manuscript fix (Evidence Table now within the judge's 40K view); rendered PDFs under `_eval_out/manuscripts/`; Layout axis remains a text-judge limitation (needs a ≥300B page-aware judge, blocked). P-A/P-C questions dedup'd. 001/019 correctly no-evidence. Report: `_eval_out/bench_pilot_das.md`.
- **Track C · evidence-grounded QA** (`qa` scenario family in bench_eval, Sessions 17–19): corpus-anchored + **Qasper external-author gold QAs** + **SciQ provided-context MCQs** + **PubMedQA yes/no abstracts** + **news-suggestion anchors** (`ctx`/`seed_id` routing, zero manual parses). Learnable-loop: survey graph answers *about* a paper → `seed_id`/`ctx` scenarios route to a grounded **extractive-answer node** (`tools/pipeline/answer.py`; ~15–20 s/answer). **QA panel n=31: correctness 4.23 · groundedness 4.45 · 24/31 correct** — extract/context paths **12/13** (the one miss is a taxonomy/synthesis question); residuals are PubMedQA yes/no conclusion convergence (8/14 — a measured model boundary, `yesno` mode); 6 new corpus papers added incl. `add_paper.py` (one-command corpus adder).
- **Case-grounded battery (Session 19b)** — `tools/eval/pools_30.py`: all 30 DAS-Bench topics through discovery → windowed parse → incremental pool manifest (`_eval_out/pools_30.json`; **22/30 topics with parsed evidence, 12 full pools**). **10 topics judged end-to-end → Total 3.13** (BSC 3.08 · MAR 2.67 · TSQ 3.05 · HDQ 3.73). Judge variance measured via `tools/eval/variance_run.py`: proxy trio **P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13**. Full capability statement in `docs/CAPABILITY-STATUS.md`.
- **Defaults**: `opencode` backend throughout (Ollama backend removed 2026-09-16); seed manifest stays the deterministic offline discovery default.

## Repository map

| Path | What it is |
|---|---|
| `docs/refs/ai-research-tools-workflow-guide.md` | Verified tool survey (2026-09-15) with Verification Ledger |
| `docs/design/research-foodie-blueprint.md` | Bilingual architecture blueprint: purpose/non-goals, L0–L6, state machine, cost matrix, roadmap |
| `docs/design/self-evolution-mechanism.md` | Bilingual self-evolution design: 4-phase cycle, evidence, failure modes (2026-09-20) |
| `docs/PROJECT.md` | **Project overview (master entry):** goals · components (code-mapped) · workflow · measured status · roadmap |
| `docs/DATAFLOW-AND-REUSE.md` | **Implementation truth:** exact inputs/outputs per mode, per-node stage I/O, honest stitch ledger (executed vs borrowed vs reference) |
| `docs/TOOL-COMPARISON.md` | **Stage-by-stage comparison vs line-research tools** + reusable-asset inventory (verified 2026-09-20) |
| `docs/CAPABILITY-STATUS.md` | Measured capability statement: numbers, GREEN/BLOCKED list, reproduce commands |
| `docs/setup-runbook.md` | Bilingual ops runbook: env, commands, **usage cheat-sheet + demos (§3.1)**, smoke tests, known issues K1–K12 |
| `docs/PLAN.md` · `docs/PROGRESS.md` | Execution plan + progress log (plan-first, track-as-you-go) |
| `tools/llm/` | Unified LLM client (`opencode` + `openai`) + mock server |
| `tools/pipeline/` | LangGraph pipeline: `corpus.py` (discovery + evidence pool) · `graph.py` (S_lit…S_final) · `validate.py` (L6) · `judge.py` (P3) · `test_pipeline.py` |
| `tools/eval/bench_eval.py` | DAS-Bench 16-criterion evaluation harness |
| `tools/citation-verify/` | Vendored citation-verification harness (CrossRef/arXiv/Semantic Scholar) |
| `external/` | Downloaded framework repos (gitignored): STORM, DAS(+DAS-Bench), paper-qa, MinerU, DeepResearch, orx, OpenResearch… |

## Governance principles

- **Citations are the lifeline**: every factual claim routes back to a primary source (parsed paper, arXiv ID) with access dates; unverifiable claims are marked *unverified*, never presented as fact.
- **Dates are explicit**: current-state statements carry `as of <date>`.
- **Cost-sensitive**: open-source/free tooling default; paid APIs only at quality-critical steps.
- **No unsolicited commits**; docs stay bilingual where a single language would lose precision.

## Roadmap (next)

1. ≥300B frozen, page-aware judge on the rendered PDFs (MAR Layout axis + full DAS-Bench compliance; needs API keys / GPU / network).
2. Track B (humanities): PaddleOCR Chinese evidence layer into the proactive loop.
3. Track C (external benchmarks): Qasper end-to-end done (2/2 gold-perfect); panel at n=31 (PubMedQA/SciQ MCQs wired, `yesno` mode shipped); GAIA level-1 if HF gating allows. Full inventory & numbers: [`docs/CAPABILITY-STATUS.md`](docs/CAPABILITY-STATUS.md).
4. Stage comparison & reuse lane: L4 relevance re-rank + L2-style perspective outline + judge median (local, ≈$0) then official DAS-Eval/DAS-2M/knowledge-storm when a ≥300B judge endpoint exists — see [`docs/TOOL-COMPARISON.md`](docs/TOOL-COMPARISON.md).
5. Self-evolution loop (baseline freeze + health check + weekly cadence) — `docs/PLAN.md §8 Phase X` & [`docs/design/self-evolution-mechanism.md`](docs/design/self-evolution-mechanism.md).
6. Local web frontend (FastAPI + HTMX/SSE, `127.0.0.1`) as the observation surface for runs/health/feedback — `docs/PLAN.md §8 Phase F`; hand-run all commands from runbook §3.1 demos.
7. Model routing (Phase D): zero-key `opencode` default; register any OpenAI-compatible API key (DeepSeek/Qwen/Kimi/OpenRouter) as a **strong judge lane** — variance P-A sd <0.40 target. Works with no key today.

See `docs/PLAN.md §8` for measurable acceptance checks.