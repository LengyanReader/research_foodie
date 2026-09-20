# Capability Status — research_foodie (as of 2026-09-19)

> 中文速览：本工作区已具备一条**本地可跑通的研究管线**（证据发现→大纲→多论文接地综述→手稿→DAS-Bench 风格 16 维 AI 判题），外加**证据接地 QA 面板**（n=31）与**30 话题任意域证据池电池**（建池 22/30、判题 10 篇）。所有数字在下方给出，全部来自本地免费模型实测（opencode/big-pickle），无 API key。硬阻塞仅剩：DAS-Bench 全量合规需 ≥300B 冻结 judge + DAS-2M 池 + PDF 渲染判 MAR（需 key/GPU）、GAIA 需 HF gating、中文证据层需人工提供中文语料 PDF。

---

## 1. What this project is

`research_foodie` is a **cost-sensitive, local-first academic research pipeline**: it takes a research question, discovers evidence (local MinerU-parsed corpus + live arXiv rail), builds a taxonomy/outline, drafts a bilingual multi-paper survey with per-claim verbatim grounding, assembles a manuscript, runs a deterministic L6 gate, and scores itself with a DAS-Bench-style 16-criterion AI judge. Track C adds a second mode — **evidence-grounded QA** — where a benchmark question is answered directly from one source paper or a provided context (Qasper / SciQ / PubMedQA contract).

Everything below was measured with the local free judge model (`opencode/big-pickle`, temperature >0, so numbers are noisy — §5).

## 2. Verified capabilities (measured)

### 2.1 Full research pipeline (P2 vertical) — GREEN

- Deterministic L6 gate + multi-paper claim grounding: **mock 34/34 · real 34/34** tests pass (one transient 33/34 variance witness, rerun green).
- Proven on **arbitrary third-party DAS topics** (not just the seed corpus): the 30-topic battery runs the *full* pipeline — discovery → outline → per-paper claims → survey → judge — on 22 topics with parsed evidence.

### 2.2 Track C — evidence-grounded QA panel (n=31)

| subset | n | correctness | groundedness | correct (>=4) |
|---|---|---|---|---|
| Corpus-anchored survey QAs (QA-1..5) | 5 | 4.20 | 4.40 | 4/5 |
| Qasper external-author gold QAs (QA-6..10) | 5 | 5.00 | 5.00 | 5/5 |
| SciQ provided-context MCQs (SQ-1..5) | 5 | 5.00 | 3.80 | 5/5 |
| News-suggestion anchors (QA-11,12 · 1703.10344) | 2 | 5.00 | 5.00 | 2/2 |
| **Extract/context path incl. QA-3 seed route** | **13** | **4.85** | **4.38** | **12/13** |
| PubMedQA yes/no abstracts (PQ-1..14) | 14 | 3.57 | 4.43 | 8/14 |
| **Full QA panel** | **31** | **4.23** | **4.45** | **24/31** |

*Figures from `_eval_out/bench_pilot_das.md` (real runs, Sessions 17–19, regenerated 2026-09-19). `gold_tokens` hits are soft; the LLM correctness/groundedness judge is primary. Directional only.*

Strong point: **extractive/context factoid answering is essentially solved at 12/13** (proper nouns, metrics, counts — one 15-20 s LLM call over ≤40 KB of paper text). The single imperfect cell inside it is QA-3 (taxonomy/synthesis — needs multi-paper S_write). The other 1 imperfect area is PubMedQA **yes/no conclusion convergence** (8/14): the model answers factually but often does not land the exact yes/no/maybe decision the gold expects.

### 2.3 DAS-Bench-style evaluation gate — canonical trio + variance

Canonical trio (proxy topics, local corpus, full pipeline), 2 fresh runs each:

| topic | Total | BSC | MAR | TSQ | HDQ |
|---|---|---|---|---|---|
| P-A · AI-text detection reliability | **3.88 ± 0.53** | 4.00 | 3.25 | 3.75 | 4.50 |
| P-B · detector bias vs non-native | **3.31 ± 0.00** | 3.12 | 2.88 | 3.12 | 4.12 |
| P-C · detection taxonomy | **3.53 ± 0.13** | 4.00 | 3.12 | 2.88 | 4.12 |
| **Mean** | **3.57** | 3.70 | 3.08 | 3.25 | 4.25 |

*Judge is a non-deterministic free model; the variance table above shows the honest spread (P-A's ±0.53). The regenerated report's family row for the trio (n=3, latest runs) reads **Total 3.75** (BSC 3.75 · MAR 3.50 · TSQ 3.58 · HDQ 4.17).*

### 2.4 30-topic arbitrary-domain evidence pool battery

- **Pool build**: 30/30 DAS-Bench topics processed; **22 have ≥1 locally parsed source paper** (12 full 3-paper pools). 8 topics yielded empty pools (network/relevance caps).
- **End-to-end judged sample (n=10)**: Total **3.13** (BSC 3.08 · MAR 2.67 · TSQ 3.05 · HDQ 3.73). Best HDQ 3.73 confirms the pipeline synthesizes; MAR 2.67 is dragged by 1-paper pools and the text-only artifact (no rendered-page scoring).
- Pool battery report: `_eval_out/pools_30_report.md`.

### 2.5 Manuscript rendering (MAR axis Part 1)

Each judged topic produces a full Markdown manuscript (Title/Abstract/body/Evidence Table/References/Sources/Claims) *and* a **local PDF** via `_render_manuscript` — see `_eval_out/manuscripts/`.

### 2.6 Corpus & tooling

- 12 papers parsed locally (MinerU windowed, ≤6 pp/window, flake self-healing), registered in `tools/pipeline/corpus._LOCAL_MD`.
- `tools/eval/add_paper.py` — **one command** to add an arXiv paper to the corpus (download → windowed parse → merge).
- `tools/eval/pools_30.py` — 30-topic pool builder + crash-resilient (per-topic cache) judge.
- `tools/eval/variance_run.py` — judge variance harness.

## 3. Not working / blocked (honest)

| item | blocker |
|---|---|
| DAS-Bench **full compliance** (≥300B frozen judge, DAS-2M pools, gold PDFs, rendered-page MAR) | API keys / GPU — deferred by user until local work done |
| GAIA batch (ICLR 2024, 466 Qs) | HF dataset gating per run; probed reachable, not run |
| Track B **Chinese evidence layer** | needs a Chinese-corpus PDF from the user |
| PubMedQA yes/no convergence (4/7 on the hard subset) | mall live model limitation — next prompt/loop candidate |
| 8/30 empty evidence pools | arXiv relevance + parse caps; candidate quality is a measured property, not silent |

## 4. Reproduce (all local, free)

```powershell
$PY = 'C:\Users\data\miniconda3\envs\ds0509\python.exe'
# full benchmark report (scenarios + QA panel + variance-merged rows)
& $PY -X utf8 -m tools.eval.bench_eval --out _eval_out\bench_pilot_das.md
# 30-topic battery: build pools, then judge (resumable)
& $PY -X utf8 -m tools.eval.pools_30 --step build
& $PY -X utf8 -m tools.eval.pools_30 --step judge --judge 10
# variance re-runs
& $PY -X utf8 -m tools.eval.variance_run --rounds 2
# tests
& $PY -X utf8 -m unittest discover -s tools -p "test_*.py"
```

## 5. Limitations & directionality

- All judge numbers come from a **local non-deterministic free model**; treat every figure as ±0.3-0.5 and, per the DAS-Bench protocol, never as a head-to-head vs the published table (frozen 300B judge, DAS-2M pools, rendered pages).
- QA "gold_tokens" hits are a **soft deterministic signal**; the LLM correctness/groundedness judge is primary.
- PubMedQA figures hover near the yes/no judgment limit of the current model — the honest test-force reveals the boundary rather than hiding it.
- Pools include off-topic relevance hits (arXiv search bias); judged scores therefore reflect *end-to-end quality including discovery noise*, which is the realistic deployment condition.
- Exact-path shrinking of repo state: numbers 'as of 2026-09-19'; evidence pools live in the gitignored domain (`_demo_downloads/`, `_eval_out/`).

## 6. Where to look

| what | path |
|---|---|
| pipeline (graph / claims / judge) | `tools/pipeline/{graph,answer,corpus,judge,validate}.py` |
| benchmark + QA + pools + variance | `tools/eval/{bench_eval,add_paper,pools_30,variance_run}.py` |
| real results | `_eval_out/{bench_pilot_das.md, pools_30_report.md, variance_runs.json, pools_cache/}` |
| design / progress | `docs/{PLAN.md, PROGRESS.md, design/research-foodie-blueprint.md}` |