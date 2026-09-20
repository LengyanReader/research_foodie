# Research Foodie — Project Overview (项目总览)

> **中文速览**
> research_foodie 是一条**本地优先、成本敏感（核心 ≈$0）、证据必可溯源**的主动式学术研究流水线。本文档是主入口：说明项目目标、架构分层、已实现组件（逐一对应到代码文件）、端到端工作流、实测能力数字与剩余阻塞项。三个并行产品形态——(1) 研究管线：提问→证据→大纲→多论文接地综述→手稿→16 维判题；(2) Track C：**证据接地 QA**（从单篇论文/给定上下文直接作答，n=31 面板）；(3) 判题电池：对任意 30 个 DAS 话题建证据池并批量判题。所有数字来自本地免费模型实测（`opencode/big-pickle`），无 API key。与本文档配套：`README.md`（入口）· `docs/design/research-foodie-blueprint.md`（架构蓝图，设计意图）· `docs/CAPABILITY-STATUS.md`（能力盘点与复现命令）。

- `Updated`: 2026-09-20
- `Status`: Implementation (P2+ GREEN) — local core done; ≥300B judge / GAIA / Chinese corpus blocked on keys|gating|input (see §8)
- `Language`: English master with 中文速览; identifiers/code English

---

## 1. Goal / 目标

Turn a research question (or a monitored field) into a **citation-grounded, publication-oriented manuscript**, and measure honestly whether that manuscript survives both a mechanical gate and an AI review gate. **Every factual claim must trace to a specific paper + passage** (`AGENTS.md`: citations are the lifeline); no bare LLM guest-citations.

| The project does | The project does NOT |
|---|---|
| Produce structured, per-claim-grounded bilingual (EN + 中文) drafts | Ship unattributed "deep research" narratives |
| Gate every artifact through deterministic validation → AI judge → human review | Auto-publish without a human gate — never |
| Run the core loop on free/local tooling (≈$0) | Require paid subscriptions for the core loop |
| Measure its own quality and noise honestly (variance, coverage, boundaries) | Hide failure cells behind averages |
| Reuse released components (DAS-Bench rubric, STORM-style outline, MinerU parsing) | Re-implement what is already released and benchmarked |

## 2. Architecture at a glance / 架构一览

Layered L0–L6 (design intent in `docs/design/research-foodie-blueprint.md`; the implemented graph is below):

```text
[L0] Question / field watch
  ▼
[L1] S_lit    discovery rails: seed manifest · live arXiv API · orx CLI → candidates
  ▼
[L2] Evidence MinerU PDF→Markdown (windowed ≤6 pp) → per-paper evidence pool
  ▼
[L3] S_org    taxonomy + STORM-style outline (sections + key_points)
  ▼
[L4] S_write  per-paper grounded claims (verbatim quotes) → cross-paper draft
  ▼
[L5] S_final  assembled artifact (Sources + per-claim arXiv attribution) + local PDF
  ▼
[L6] Gate     deterministic validation (zero-LLM) → DAS-Bench-style 16-dim AI judge → HUMAN
```

**Implemented LangGraph nodes** (`tools/pipeline/graph.py`): `lit → org → write → revise_para → finalize → gate → judge`. Scoped review (DAS's key finding): `revise_para` re-enters **only** the offending paragraph, never regenerates wholesale; deterministic-gate failure loops back scoped.

**Two routing modes** (learnable loop): survey path answers *about* a paper via the graph; `seed_id`/`ctx` scenarios route to a **grounded extractive-answer node** (`tools/pipeline/answer.py`, ~15–20 s/answer) for benchmark QA.

## 3. Components / 组件清单

| Module | File | Function |
|---|---|---|
| LLM client | `tools/llm/client.py` | Unified `LLMClient`: `opencode` backend (free hosted model, JSON mode) + `openai` backend (any OpenAI-compatible endpoint). Flat 3× retry on empty sessions |
| Mock server | `tools/llm/mock_openai_server.py` | Deterministic fake for mock tests |
| Claim planning | `tools/llm/claim_plan.py` | Per-section claim + citation-group planner |
| Discovery & corpus | `tools/pipeline/corpus.py` | Rails: deterministic seed manifest / live arXiv API (regex `_ID_RE` incl. version suffix) / orx; `_LOCAL_MD` registry of locally parsed papers |
| Graph | `tools/pipeline/graph.py` | LangGraph state machine `S_lit→S_org→S_write→S_final` with scoped `revise_para` loop, L6 gate, judge node |
| State | `tools/pipeline/state.py` | Graph state schema |
| Extractive QA | `tools/pipeline/answer.py` | Grounded answer node for QA scenarios (fact / multi / boolean `/ yesno`) |
| L6 validation | `tools/pipeline/validate.py` | **Zero-LLM deterministic gate**: structure, well-formed cites (arXiv/DOI), 5-gram verbatim-grounding check blocks hallucinated quotes, JSON recovery parsers |
| AI judge | `tools/pipeline/judge.py` | DAS-Bench-style 4-axis rubric (groundedness/structure/bilingual/clarity), deterministic threshold matrix mostly `fail/` `pass/` `revise`, never raises |
| Pipeline tests | `tools/pipeline/test_pipeline.py` | `mock` + `real` integration runs (34/34) |
| Benchmark harness | `tools/eval/bench_eval.py` | DAS-Bench 16-criterion scores (BSC · MAR · TSQ · HDQ + Total); scenario families: proxy `P-A/B/C`, DAS `001/019`, `qa` corpus `QA-1..5`, `seed_id` `QA-3,6..12`, SciQ `SQ-1..5`, PubMedQA `PQ-1..14`; family means + report writer |
| QA scorer | `tools/eval/bench_eval.py::score_qa` | correctness + groundedness LLM judge (+ token-stability soft check), truncated-JSON recovery (max_tokens 1000 + regex fallback) |
| Pool battery | `tools/eval/pools_30.py` | All 30 DAS topics: discovery→download→windowed MinerU parse→incremental manifest (`pools_30.json`)→per-topic cached judge (crash-resumable) |
| Variance harness | `tools/eval/variance_run.py` | Re-runs proxy trio to measure judge run-to-run spread |
| Corpus adder | `tools/eval/add_paper.py` | One-command add an arXiv paper: download→pypdf page count→windowed `-m txt` parse (420 s subprocess timeout)→merge→print registration line |
| Renderer | `tools/eval/render_manuscript.py` | Markdown → local PDF (pandoc + xelatex CJK) |
| Citation verification | `tools/citation-verify/` | Vendored CrossRef / arXiv / Semantic Scholar batch check (canonical-authority workflow) |
| Externals | `external/` (gitignored) | STORM · DAS(+DAS-Bench) · paper-qa · MinerU · DeepResearch · orx · OpenResearch |

## 4. Workflow / 端到端工作流

**Mode 1 — research survey (on demand).** `L0` question → discovery rail fetches candidates → MinerU parses top papers → taxonomy + outline → per-paper grounded claims → cross-paper bilingual draft → L6 deterministic gate (cites/grounding) → AI judge (4-axis) → human review → manuscript + PDF.

**Mode 2 — evidence-grounded QA (Track C).** A benchmark question + source (`seed_id` paper or `ctx` context) → extractive answer node grounded in that paper's passages → `score_qa` correctness/groundedness → reported in the panel.

**Mode 3 — battery (any 30 DAS topics).** Topic → live arXiv discovery → parse → evidence pool; if pool non-empty → full Mode-1 pipeline → judge → per-topic report `pools_30_report.md`.

**Validation duty split:** mechanical (L6, zero cost) guards *factual integrity*; the LLM judge rates *subjective quality*; the human gate curates release. Judge is non-deterministic (free model) — see variance below.

## 5. Measured status / 实测能力

| Area | Number (as of 2026-09-19) | Meaning |
|---|---|---|
| Pipeline tests | **mock 34/34 · real 34/34** | Deterministic + full LLM loop green |
| QA panel n=31 | correctness **4.23** · groundedness **4.45** · 24/31 | See breakdown below |
| Extract/context QA path (n=13) | **12/13** | Factoid answering ≈ solved (proper nouns/metrics/counts) |
| PubMedQA yes/no (PQ-1..14) | **8/14** | Yes/no *conclusion* = measured model boundary |
| Canonical trio | **P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13** | Judge run-to-run noise | 
| Battery judged (n=10) | **Total 3.13** (BSC 3.08 · MAR 2.67 · TSQ 3.05 · HDQ 3.73) | End-to-end incl. discovery noise; HDQ=strength, MAR=pool-size drag |
| Pool coverage | **22/30 topics with evidence** (12 full pools) | 8 empty = relevance/network caps (measured, not silent) |

QA panel subset detail: corpus-anchored 5 (4.20/4.40, 4/5) · Qasper external gold 5 (**5.00/5.00, 5/5**) · SciQ provided-context 5 (**5.00/3.80, 5/5**) · news anchors 2 (**5.00/5.00, 2/2**) · PubMedQA 14 (3.57/4.43, 8/14). Ground-truth in `_eval_out/bench_pilot_das.md`.

**Honesty rules** (every number here already enforces them): directional, never head-to-head vs the published DAS table (that needs a ≥300B frozen judge); `gold_tokens` hits are soft; judge model recorded in verdicts; limitations listed in §8 and `docs/CAPABILITY-STATUS.md`.

## 6. Repository map / 仓库地图

| Path | Contents |
|---|---|
| `README.md` (`README.zh-CN.md`) | Entry + pipeline diagram + quickstart |
| `docs/PROJECT.md` | **this overview** |
| `docs/design/research-foodie-blueprint.md` | Architecture intent: L0–L6, state model, reuse map, cost matrix, roadmap P1–P5 |
| `docs/CAPABILITY-STATUS.md` | Measured capability statement + how to reproduce |
| `docs/PLAN.md` · `docs/PROGRESS.md` | Plan-first / track-as-you-go (rows + dated sessions) |
| `docs/setup-runbook.md` | Ops runbook: env, commands, smoke tests, known issues K1–K12 |
| `docs/refs/ai-research-tools-workflow-guide.md` | Verified tool survey + Verification Ledger |
| `tools/` | `llm/` · `pipeline/` · `eval/` · `citation-verify/` (see §3) |
| `_eval_out/` | Real results: `bench_pilot_das.md`, `pools_30_report.md`, `variance_runs.json`, `pools_cache/`, `manuscripts/`, per-scenario caches |
| `_demo_downloads/` | Parsed-paper Markdown artifacts (MinerU windows) |
| `external/` (gitignored) | Framework repos referenced by the blueprint |

## 7. Reproduce / 复现

```powershell
$PY='C:\Users\data\miniconda3\envs\ds0509\python.exe'
& $PY -X utf8 -m tools.pipeline.test_pipeline mock
& $PY -X utf8 -m tools.eval.bench_eval --scenarios "P-A,P-B,P-C,001,019" --out _eval_out/bench_pilot_das.md
& $PY -X utf8 -m tools.eval.pools_30 --step build      # 30-topic pools (resumable)
& $PY -X utf8 -m tools.eval.pools_30 --step judge --judge 10
& $PY -X utf8 -m tools.eval.variance_run --rounds 2
```

## 8. Roadmap / 路线图

**Done (local core):** P1 tooling · P2 minimal vertical + framework integration · P3-style judge gate (local) · MAR render Part 1 (MD+PDF) · Track C QA (panel n=31) · 30-topic battery · variance.

**Blocked / requires keys · GPU · input** (user decision points):

| item | blocker |
|---|---|
| DAS-Bench **full compliance** — ≥300B frozen, page-aware judge on rendered PDFs, DAS-2M pools, Layout/MAR parity | API keys / remote GPU |
| **GAIA** batch (466 Qs) | HF per-run gating |
| **Track B** — Chinese evidence layer (PaddleOCR + translation w/ expert gate) into the proactive loop | needs a Chinese corpus PDF from the user |
| PubMedQA yes/no conclusion convergence (8/14) | model boundary; next prompt/loop-layout candidates |
| Proactive change-feed (stale → scoped re-synthesis) | design ready (blueprint §6); scheduled on key-free rails |

## 9. Governance / 质量护栏

- Citations are the lifeline: every claim traces to a parsed paper + passage; unverifiable → *unverified*, never asserted (AGENTS.md).
- Dates explicit (`as of …`); prices/leaderboard numbers directional with source.
- Cost-sensitive: open/free default; paid APIs only at quality-critical escalation lanes.
- No unsolicited commits; docs reviewed with `rg` for TODO/TBD/dead links.