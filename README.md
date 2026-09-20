# research_foodie

**Local-first, cost-sensitive active academic research pipeline.** Turn a research question (or a watched field) into a *citation-grounded*, bilingual survey manuscript — every factual sentence traces to a parsed paper, and every gate is mechanical before it is human.

> 中文版见 [`README.zh-CN.md`](README.zh-CN.md) · Master overview (goals / components / workflow / measured status): [`docs/PROJECT.md`](docs/PROJECT.md) · Blueprint: [`docs/design/research-foodie-blueprint.md`](docs/design/research-foodie-blueprint.md)

`Updated: 2026-09-20` · `License: MIT`

---

## Why this exists / 为什么做这个

General "deep research" tools produce fluent surveys that look right but **fabricate citations** — a measured GPT-4o hallucination rate around 78–90% (*OpenScholar*, Nature 650:857, 2025). They are also black boxes, cost real money, and hide failure cells behind averages.

research_foodie takes the opposite posture:

- **Citations are the lifeline.** Every claim must anchor to a *verbatim quote* from a locally parsed paper (arXiv); a deterministic 5-gram grounding gate blocks hallucinations mechanically — before any LLM review.
- **≈$0 core loop.** Runs on MinerU (local parse) + the free hosted model `opencode/big-pickle` + the free arXiv API. No API keys required for the core loop.
- **Honest self-measurement.** Judge noise, pool coverage, and model boundaries are reported, not averaged away.

## What it does / 做什么

- **Mode 1 — research survey:** question → live discovery → MinerU parse → taxonomy + STORM-style outline → per-paper grounded claims → **survey-depth bilingual (EN + 中文) draft** with inline `(arXiv:…)` attribution, disagreement/gap handling → manuscript (Abstract / Evidence Table / References) → local **PDF** (pandoc + xelatex + CJK).
- **Mode 2 — evidence-grounded QA (Track C):** answer a benchmark question *directly from a paper/context* via a grounded extractive-answer node (Qasper / SciQ / PubMedQA / corpus-anchored).
- **Mode 3 — battery:** run any of the 30 DAS-Bench topics end-to-end (discovery → evidence pool → judge).
- **Evaluation:** DAS-Bench's 16-criterion rubric re-implemented verbatim; judge-variance harness; 30-topic pools; citation-verify harness (CrossRef / arXiv / Semantic Scholar).

## Architecture / 架构

```text
[L0] Question / field watch
  ▼
[L1] S_lit   discovery rails: seed manifest · live arXiv API · orx CLI
  ▼
[L2] Evidence  MinerU PDF→Markdown → multi-paper evidence pool (per-paper grounding)
  ▼
[L3] S_org   taxonomy + STORM-style outline (sections + key_points)
  ▼
[L4] S_write per-paper grounded claims (verbatim quotes) → cross-paper draft
  ▼
[L5] S_final assembled manuscript (Sources + per-claim arXiv attribution) → local PDF
  ▼
[L6] Gates  deterministic zero-LLM validation → DAS-Bench-style AI judge → HUMAN
```

Implemented as a LangGraph state machine (`tools/pipeline/graph.py`): `lit → org → write → revise_para → finalize → gate → judge`. Scoped review re-enters only the offending paragraph; a failing mechanical gate loops back scoped. `seed_id`/`ctx` questions route to the extractive-answer node instead. Discovery rails are pluggable (`S_LIT_BACKEND=seed|arxiv|orx`; arXiv API verified reachable ~1.1 s, 2026-09-16).

## Quickstart / 快速上手

Environment: conda env `ds0509` (Python 3.12, Windows). Use it explicitly:

```powershell
$PY = 'C:\Users\data\miniconda3\envs\ds0509\python.exe'
$UTF8 = '-X','utf8'                 # avoids cp1252 decode noise in the opencode subprocess
```

**Integration test** (mock = deterministic, seconds; real = full free-model loop, 2–4 min):

```powershell
& $PY -m tools.pipeline.test_pipeline mock      # 34/34 PASS
& $PY $UTF8 -m tools.pipeline.test_pipeline real  # opencode/big-pickle, verdict PASS
```

**Demo questions:** *"GPT detectors bias against non-native English writers"* (Liang `2304.02819`) · *"How reliable are automatic detection tools for AI-generated text?"* (multi-paper pool: Liang + Weber-Wulff `2306.15666` + GLTR `1906.04043`).

**DAS-Bench 16-axis benchmark** (report → `_eval_out/bench_pilot_das.md`; `--out` overwrites, always run the full set in one call):

```powershell
& $PY $UTF8 -m tools.eval.bench_eval --scenarios P-A,P-B,P-C,001,019
```

**Evidence-grounded QA panel subset:**

```powershell
& $PY $UTF8 -m tools.eval.bench_eval --scenarios QA-6,QA-7,SQ-1,PQ-1
```

**30-topic battery + judge variance:**

```powershell
& $PY $UTF8 -m tools.eval.pools_30          # → _eval_out/pools_30.json + pools_30_report.md
& $PY $UTF8 -m tools.eval.variance_run      # → _eval_out/variance_runs.json
```

**Local web dashboard (WS-B):** trigger runs, live SSE progress, cancel, manuscripts, feedback — all in a browser:

```powershell
& $PY -X utf8 -m uvicorn tools.web.app:app --host 127.0.0.1 --port 8787
# → http://127.0.0.1:8787/
```

It binds **127.0.0.1 only** and is a *local observation surface*: GitHub Pages is static-host-only (no server-side execution — Python/Node/PHP runtimes are not supported on Pages), so the live dashboard stays local; read-only static export is the deployable fallback (F-3).

**LLM backends** (`tools/llm/client.py`): `opencode` default (free hosted model, zero key) · `openai` for any OpenAI-compatible endpoint (DeepSeek / DashScope·Qwen / Moonshot·Kimi / OpenRouter / OpenAI) via `OPENAI_BASE_URL` / `OPENAI_MODEL` / `OPENAI_API_KEY`. Phase D adds per-role profiles (cheap draft lane / strong judge lane). **Parse a paper** with MinerU (`-m txt`, page windows ≤6 pp for long PDFs — see runbook K12).

> Full per-tool cheat-sheet + 4 end-to-end demos: [`docs/setup-runbook.md §3.1`](docs/setup-runbook.md) · End-to-end usage flow (question-first → dense-output settings → spec/format conformance): [`§3.0`](docs/setup-runbook.md).

## Measured status / 实测能力 (as of 2026-09-19)

> Directional, never head-to-head vs the published DAS table (that needs a ≥300B frozen judge). Judge model is recorded in every verdict. Full statement: [`docs/CAPABILITY-STATUS.md`](docs/CAPABILITY-STATUS.md).

| Area | Number | Meaning |
|---|---|---|
| Pipeline tests | **mock 34/34 · real 34/34** | Deterministic + full LLM loop green (2 real papers: Liang, Weber-Wulff) |
| QA panel n=31 | correctness **4.23** · groundedness **4.45** · 24/31 | Track C, incl. Qasper gold 5/5 · SciQ context 5/5 · PubMedQA 8/14 |
| Extract/context path (n=13) | **12/13** | Factoid from single paper/context ≈ solved |
| PubMedQA yes/no (PQ-1..14) | **8/14** | Yes/no *conclusion* = measured model boundary |
| Canonical trio (variance) | **P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13** | Judge run-to-run noise (free model) |
| Battery judged (n=10) | **Total 3.13** (BSC 3.08 · MAR 2.67 · TSQ 3.05 · HDQ 3.73) | End-to-end incl. discovery noise; HDQ = strength, MAR = pool-size drag |
| Pool coverage | **22/30 DAS topics** with parsed evidence (12 full pools) | 8 empty = relevance/network caps, measured not silent |

**Honesty contract:** judge noise is reported (P-A σ≈0.53), 001/019 are correctly *no-evidence*, PubMedQA's 8/14 boundary is owned, and hidden failure cells are listed — not averaged away. Chains go through three gates: deterministic L6 (factual integrity, zero cost) → AI judge (quality) → **human** (release; nothing auto-publishes).

## Repository map / 仓库地图

| Path | What it is |
|---|---|
| `README.zh-CN.md` | 中文入口 (this project's Chinese entry) |
| `docs/PROJECT.md` | **Master overview:** goals / components / workflow / measured status / roadmap |
| `docs/design/research-foodie-blueprint.md` | Architecture blueprint: L0–L6, state model, cost matrix, roadmap |
| `docs/design/self-evolution-mechanism.md` | Self-evolution design (WS-C): 4-phase cycle, evidence, failure modes |
| `docs/design/tool-paper-outline.md` | arXiv systems-paper outline (bilingual) for this tool |
| `docs/DATAFLOW-AND-REUSE.md` | Inputs/outputs per mode, stage I/O, honest framework-stitch ledger |
| `docs/TOOL-COMPARISON.md` | Stage-by-stage compare vs STORM / orx / PaperQA2 / DAS / MinerU |
| `docs/CAPABILITY-STATUS.md` | Measured numbers, GREEN/BLOCKED list, reproduce commands |
| `docs/setup-runbook.md` | Ops runbook: env, commands, usage flow §3.0, demos §3.1, issues K1–K12 |
| `docs/PLAN.md` · `docs/PROGRESS.md` | Plan-first / track-as-you-go (§8 = parallel workstreams WS-A/B/C/D/R) |
| `tools/llm/` | Unified LLM client (`opencode` + `openai`) · mock server · smoke test |
| `tools/pipeline/` | LangGraph: `corpus.py` · `graph.py` · `validate.py` (L6) · `judge.py` · `answer.py` · `test_pipeline.py` |
| `tools/eval/` | `bench_eval.py` (DAS-16) · `pools_30.py` · `variance_run.py` · `add_paper.py` · `render_manuscript.py` |
| `tools/web/` | Local FastAPI dashboard (runs / SSE / cancel / manuscripts / feedback) — WS-B |
| `tools/citation-verify/` | CrossRef / arXiv / Semantic Scholar batch citation verification |
| `_eval_out/` | Real results: bench reports, pools, variance, manuscripts, web run logs (gitignored) |

## Governance / 质量护栏

- **Citations are the lifeline** — every factual claim traces to a primary source (parsed paper, arXiv ID) with access dates; unverifiable → *unverified*, never asserted as fact.
- **Dates are explicit** — current-state statements carry `as of <date>`; pricing/leaderboard numbers are directional with sources.
- **Cost-sensitive** — open/free by default; paid APIs only at quality-critical escalation lanes.
- **No unsolicited commits; plan-first, track-as-you-go** (`docs/PLAN.md` → `docs/PROGRESS.md`).

## Roadmap & open workstreams / 路线图

Progress is organized as **parallel workstreams** (see `docs/PLAN.md §8`):

- **WS-A** core pipeline (Phase L): L-1 relevance re-rank · L-3 judge median-of-3 (attack P-A σ 0.53) · L-4 citation-verify wiring.
- **WS-B** web dashboard (Phase F): ✅ F-1/F-2 delivered (runs/SSE/cancel) · F-3 read-only static export (GH Pages deployable) · F-4 cadence wiring (E-2/E-3/E-4/E-5 on one URL).
- **WS-C** self-evolution (Phase X): baseline freeze → variance-aware health check → gate-coverage mutation test → weekly cadence with provenance floor (E-1…E-7).
- **WS-D** model routing (Phase D): per-role profiles; strong judge lane on an OpenAI-compatible API key (no key required today) — target P-A sd < 0.40.
- **WS-R** resource-gated (Phase R): official DAS-Eval harness · DAS-2M metadata lake · knowledge-storm · ≥300B page-aware judge (needs keys / GPU / network).

**Blocked (needs keys · GPU · input):** ≥300B page-aware judge on rendered PDFs (MAR Layout axis + full DAS-Bench compliance) · GAIA batch · Chinese evidence layer (Track B) — merge decision in [`docs/CAPABILITY-STATUS.md §3`](docs/CAPABILITY-STATUS.md).

---
*MIT License · bilingual docs enforced by [`AGENTS.md`](AGENTS.md) · built Windows 11, CPU-only, conda `ds0509`.*