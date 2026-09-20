# Capability Status — research_foodie (as of 2026-09-20)

> 中文速览：本工作区已具备一条**本地可跑通的研究管线**（证据发现→大纲→多论文接地综述→手稿→DAS-Bench 风格 16 维 AI 判题），外加**证据接地 QA 面板**（n=31）与**30 话题任意域证据池电池**（建池 22/30、判题 10 篇）。**2026-09-20 新增**：一条**可定时、可度量、人工在环的自我演化机制**（E-3 演化冲刺/E-4 依赖台账/E-5 反馈累积+晋升规则），L-6 单命令自检 `self_check.ps1`，以及 Phase L 检索/判题强化（L-1 BM25 重排、L-2 多视角、L-3 判题中位数）与 D-3 跨模型判题矩阵。**2026-09-20 续（Session 23）**：一条**定时能力/基准快照** `capability_report`（把“各工具在 benchmark 上的表现 + 当前配置”汇成一屏带日期的报告，随演化周期刷新），基座模型**三选项可切换**（`free-opencode` / `openai-compat`（可跨到 DashScope Qwen）/ `judge-strong`，qwen3.8-flash 可用 `OPENCODE_MODEL` 直接重定向），以及**论文初稿 v1** `docs/paper/research-foodie-paper.md`。所有数字在下方给出，全部来自本地免费模型实测（opencode/big-pickle），无 API key。硬阻塞仅剩：DAS-Bench 全量合规需 ≥300B 冻结 judge + DAS-2M 池 + PDF 渲染判 MAR（需 key/GPU）、GAIA 需 HF gating、中文证据层需人工提供中文语料 PDF。

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

### 2.7 Self-evolution loop (WS-C Phase X) + Phase L/D strengthening — GREEN (Session 22, 2026-09-20)

The "self-evolution" capability is a **scheduled-measurement + regression-detection + human-gated-repair** loop (never autonomous code/weight change), per `docs/design/self-evolution-mechanism.md`. All zero-LLM paths verified:

| item | tool | status (this session) |
|---|---|---|
| E-3 evolution cadence | `tools/eval/evolution_sprint.py` + `evolution.py` (tickets) | ✅ 2 consecutive `--quick` sprints GREEN; ticket open/feed/close + streak logic unit-tested |
| E-4 dependency/version ledger | `evolution.verify_deps` → `deps_ledger.json` | ✅ 9 pins live-verified; drift/missing classification feeds the board |
| E-5 feedback corpus + promotion rule | `evolution.py` (gold quota, `promotion_check`, `bump_revision`) | ✅ real-gold quota (≥50%/≥10 rows), N≥3∧Δ≥2σ∧no-regression gate — unit-tested |
| L-6 one-command self-check | `tools/eval/self_check.py` + `self_check.ps1` | ✅ offline GREEN in ~13 s (unit → mock integration → cadence) |
| L-1 BM25 relevance re-rank | `tools/pipeline/rerank.py` (wired into `graph._write`) | ✅ unit + mock 34/34 with `source_windows` provenance; gate never weakened |
| L-2 reader-perspective decomposition | `graph._org` perspective rail | ✅ mock deterministic (perspectives=3) |
| L-3 judge median-of-N | `bench_eval.median_bench` / `variance_run` | ✅ unit-tested aggregation; single-call baseline kept separate |
| D-3 cross-model judge matrix | `tools/eval/judge_matrix.py` | ✅ harness mock-verified (2 vantages); compression measure gated on ≥300B key |
| D-4 provenance in every report | `bench_eval`/`health_check`/`evolution_sprint`/`judge_matrix` | ✅ model+judge_model+temperature+profile footers |
| Scheduled capability snapshot | `tools/eval/capability_report.py` | ✅ reads cached artifacts → dated `_eval_out/capability_report.md` (config × benchmark × evolution-state); wired into every cadence step 8 |
| Multi-option base model | `tools/llm/profiles.py` (`free-opencode`/`openai-compat`/`judge-strong`) | ✅ 3 selectable options + `OPENCODE_MODEL` qwen3.8-flash redirect; loud-fail on missing key/unknown profile; `test_capability.py` **33 guards** |
| Paper draft | `docs/paper/research-foodie-paper.md` | ✅ Draft v1 + Mermaid figures (`fig:architecture`, `fig:loop`) + deterministic §4.6 (living doc — §4 tied to `capability_report`/`ablations`) |
| Deterministic §4.6 ablations (Session 24) | `tools/eval/ablations.py` → `_eval_out/ablations.md` | ✅ **model-free (no LLM/key)**: gate ON/OFF leakage 8→0 · 0 false drops; pool coverage 73% (14/8/8); median-of-N spread ≈0.31 — feeds paper §4.6; auto-refreshed at cadence step 8 |
| Daily-cadence scheduler (Session 24) | `tools/web/schedule_task.ps1` | ✅ idempotent Windows Task registration of the **offline** `evolution_sprint --quick` (`-At`/`-Unregister`); delivered, not auto-run; live loop intentionally unscheduled (see §3) |
| Client fail-fast on model errors (Session 24) | `tools/llm/client.py` (`OpencodeError`, `_first_opencode_error`) | ✅ parses opencode `{"type":"error"}` billing/401 events into a clear **non-retryable** error (no ~600 s hang on a credit-blocked account) |

Deterministic guard tests: `tools/eval/test_evolution.py` (31 assertions, temp-isolated, zero-network). **Honest boundary:** the loop writes only ledger JSONs under `_eval_out/`; live re-measures (L-1/L-2 acceptance on real P-A..C/QA, L-3 sd<0.40) still need a real judge cadence, and D-3/R-1 need a registered strong key.

## 3. Not working / blocked (honest)

| item | blocker |
|---|---|
| DAS-Bench **full compliance** (≥300B frozen judge, DAS-2M pools, gold PDFs, rendered-page MAR) | API keys / GPU — deferred by user until local work done |
| GAIA batch (ICLR 2024, 466 Qs) | HF dataset gating per run; probed reachable, not run |
| Track B **Chinese evidence layer** | needs a Chinese-corpus PDF from the user |
| PubMedQA yes/no convergence (4/7 on the hard subset) | mall live model limitation — next prompt/loop candidate |
| 8/30 empty evidence pools | arXiv relevance + parse caps; candidate quality is a measured property, not silent |
| **Live model cadence / fresh §4 judge numbers** (Session 24) | free hosted judge is **credit-blocked** — `opencode` CLI → opencode.ai "zen" gateway returns **HTTP 401 "No payment method"** (hence `big-pickle` hangs, `qwen3.8-flash` rc=1). Qoder's in-IDE Qwen is **not** exposed as a callable/key-free endpoint (`qoder` CLI = IDE launcher; `:56510` = private WebSocket, `:9420` = Chromium debug) — model-call work deferred; deterministic/mock paths unaffected |

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
# self-checks (E-1/E-2; health_check also has --freeze baseline freeze and --quick fast cycle)
& $PY -X utf8 -m tools.eval.health_check              # mock + pools + arxiv_probe + gate_coverage + judge sanity
# L-6 one-command self-check (unit + mock integration + evolution cadence, ~15s offline)
& ./self_check.ps1                                     # or: -m tools.eval.self_check ; -Full adds live judge
# WS-C self-evolution cadence + deterministic guards
& $PY -X utf8 -m tools.eval.evolution_sprint --quick   # health→deps→tickets→feedback→promotion→report (+refresh capability_report & ablations)
& $PY -X utf8 -m tools.eval.ablations                   # deterministic §4.6 (model-free) → _eval_out\ablations.md
& $PY -X utf8 -m tools.eval.test_capability             # 33 zero-LLM guards (profiles + report + ablations + client 401-parse)
pwsh -File tools/web/schedule_task.ps1 -At 09:00        # register the offline daily cadence (no LLM/no key); -Unregister to remove
& $PY -X utf8 -m tools.eval.test_evolution             # 31 zero-LLM guard tests (temp-isolated)
# D-3 cross-model judge matrix
& $PY -X utf8 -m tools.eval.judge_matrix --judges free-opencode --rounds 3
# Scheduled capability × benchmark snapshot (offline; --live refreshes first)
& $PY -X utf8 -m tools.eval.capability_report            # -> _eval_out/capability_report.md
# Base-model options (env only, no keys in repo): free-opencode | openai-compat | judge-strong
& $PY -X utf8 -m tools.eval.test_capability              # 22 config+report guards (zero-network)
# tests (script-style runners, not unittest.TestCase — invoke as modules)
& $PY -X utf8 -m tools.pipeline.test_pipeline mock     # 34/34 integration (in-proc mock)
& $PY -X utf8 -m tools.eval.test_evolution             # 31 self-evolution guards
& $PY -X utf8 -m tools.eval.test_capability             # 22 config + capability-report guards
& $PY -X utf8 -m tools.pipeline.test_pipeline real     # full real-model integration (~2 min)
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
| pipeline (graph / claims / judge) | `tools/pipeline/{graph,answer,corpus,judge,validate,rerank}.py` |
| benchmark + QA + pools + variance | `tools/eval/{bench_eval,add_paper,pools_30,variance_run}.py` |
| health check / baselines / ledgers | `tools/eval/{health_check,run_ledger}.py` · `_eval_out/{baselines.json, health_check.md, ledgers/}` |
| self-evolution loop (E-3/E-4/E-5) | `tools/eval/{evolution,evolution_sprint,test_evolution}.py` · `_eval_out/{tickets.json, deps_ledger.json, feedback/, revisions.json, evolution_sprint.md}` |
| one-command self-check (L-6) · judge matrix (D-3) | `self_check.ps1` · `tools/eval/{self_check,judge_matrix}.py` |
| profiles / routing | `tools/llm/profiles.py` |
| scheduled capability snapshot | `tools/eval/capability_report.py` · `_eval_out/capability_report.md` |
| paper draft / outline | `docs/paper/research-foodie-paper.md` · `docs/design/tool-paper-outline.md` |
| real results | `_eval_out/{bench_pilot_das.md, pools_30_report.md, variance_runs.json, pools_cache/}` |
| design / progress | `docs/{PLAN.md, PROGRESS.md, design/research-foodie-blueprint.md}` |