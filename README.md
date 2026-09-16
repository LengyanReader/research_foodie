# research_foodie

A **local-first, cost-sensitive proactive academic research pipeline** that turns a research question into a *citation-grounded* draft — every sentence traceable to a parsed paper, every gate mechanical before it is human.

> 中文版见 [`README.zh-CN.md`](README.zh-CN.md).

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
- **P2 minimal vertical + framework integration (GREEN)**: LangGraph pipeline with pluggable S_lit rails (seed / arXiv API — verified reachable 2026-09-16 / orx CLI), multi-paper evidence pool (`resolved_evidence`, 3 local parses), per-paper grounded claims (`paper_id` attribution), STORM-style outline (4-6 sections), **survey-depth per-section drafting** (intro + `## <heading>` section paragraphs + conclusion, inline arXiv attribution, disagreement/gap handling), L6 deterministic gate (+ informational `multi_paper` metric), DAS-Bench-style AI judge.
- **Tests**: mock **33/33** · real `opencode/big-pickle` **33/33** (real ~4–8 min draft + strict judge verdict=pass; judge gate = deterministic threshold matrix v1 — pass requires score≥4 and all four rubric checks, groundedness failure or score<2 is a hard fail).
- **Evaluation pilot** (`tools/eval/bench_eval.py`, Session 11-13): DAS-16 family means **BSC 3.25 / MAR 2.50 / TSQ 3.17 / HDQ 3.75 / Total 3.17** — **TSQ lifted 2.42→3.17** by per-section drafting; artifacts 23-26K chars; proxies 2.94–3.38; DAS topic 001 correctly no-evidence after the seed-precision fix. Report: `_eval_out/bench_pilot_das.md`.
- **Defaults**: `opencode` backend throughout (Ollama backend removed 2026-09-16); seed manifest stays the deterministic offline discovery default.

## Repository map

| Path | What it is |
|---|---|
| `docs/refs/ai-research-tools-workflow-guide.md` | Verified tool survey (2026-09-15) with Verification Ledger |
| `docs/design/research-foodie-blueprint.md` | Bilingual architecture blueprint: purpose/non-goals, L0–L6, state machine, cost matrix, roadmap |
| `docs/setup-runbook.md` | Bilingual ops runbook: env, commands, smoke tests, known issues K1–K12 |
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

1. MAR render axes — page-rendered artifact / figure-table extraction (plain-markdown cannot score Figure/Table quality; the residual low axis).
2. DAS-Bench full compliance — DAS-2M topic pools + a ≥300B frozen judge (needs API keys / GPU / network).
3. Track B (humanities): PaddleOCR Chinese evidence layer into the proactive loop.

See `docs/PLAN.md §7` for measurable acceptance checks.