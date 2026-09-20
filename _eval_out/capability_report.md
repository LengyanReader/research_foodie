# Capability & Benchmark Report — research_foodie

> Generated `2026-09-20T17:51:35` by `tools.eval.capability_report`. Reads cached `_eval_out/` artifacts; every figure keeps its own `as of` date below.

## 1. Configuration (what ran)

- **Active base-model profile:** `[profile free-opencode] draft=opencode/big-pickle, qa=opencode/big-pickle, judge=opencode/big-pickle`
- **Baseline measured on:** `opencode/big-pickle (free, directional)`
- **Selectable options** (`LLM_PROFILE`):
  - `free-opencode (opencode hosted free; redirect via OPENCODE_MODEL, e.g. opencode/qwen3.8-flash)`
  - `openai-compat (all lanes -> OpenAI-compatible provider via OPENAI_*; e.g. DashScope Qwen, needs key)`
  - `judge-strong (draft|qa free-opencode, judge -> strong OpenAI-compatible, needs key)`
- **Tool ledger** (`as of 2026-09-20T17:51:35`):

  | tool | version | status | severity |
  |---|---|---|---|
  | python | 3.12.13 | ok | required |
  | langgraph | 1.1.10 | ok | required |
  | mineru | 3.4.5 | ok | required |
  | opencode_cli | 1.18.31 | ok | required |
  | default_model | opencode/big-pickle | ok | info |
  | pandoc | pandoc 3.8.2.1 | ok | optional |
  | xelatex | MiKTeX-XeTeX 4.11 (MiKTeX 24.4) | ok | optional |
  | paddleocr | 3.7.0 | ok | optional |
  | arxiv_api | reachable | ok | optional |

## 2. Capability × benchmark performance

_Frozen baseline `as of 2026-09-20`; judge is a non-deterministic free model — treat figures as directional (§4)._

| capability | benchmark / test | measured | source |
|---|---|---|---|
| Deterministic L6 gate + grounding | pipeline test (mock) | **34/34 PASS** (0 failures) | `test_pipeline mock` |
| Evidence-grounded QA (Track C) | QA panel | n=31 · correctness **4.23** · groundedness **4.45** · 24/31 | `bench_pilot_das.md` |
| Arbitrary-domain discovery | 30-topic pool battery | 22/30 covered · 8 empty | `pools_30_report.md` |
| DAS-Bench 16-criterion judge | canonical trio (P-A/B/C) | see below | `variance_runs.json` / `baselines.json` |

| topic | mean Total | sd | n |
|---|---|---|---|
| P-A | 3.88 | 0.38 | 2 |
| P-B | 3.31 | 0.0 | 2 |
| P-C | 3.53 | 0.09 | 2 |
_(raw judge runs in `variance_runs.json`: 6)_

- **Regression thresholds (E-2):** FAIL ≥ 2.0σ · WARN ≥ 1.0σ — on judge Total (proxy manuscripts×1 round)

## 3. Self-evolution state (WS-C)

- **Open tickets:** 0 (board clear)
- **Feedback corpus:** 8 rows · gold share 0.0 (quota_ok=True, enforced=False)
- **Last cadence** `2026-09-20` (quick): exit=0 · PASS=13 · SKIP=3
  - provenance: `judge skipped (--quick)`
- **Recent cadence exits:** [0, 0, 0, 0, 0]

## 4. Honest boundaries

- Judge numbers come from a **non-deterministic free model** (±0.3–0.5); never head-to-head vs the published DAS table (needs a frozen ≥300B judge + DAS-2M pools + rendered pages).
- 8/30 evidence pools empty = arXiv relevance + parse caps, a **measured** property, not silent failure.
- This report **reads** artifacts only — it changes no code, no prompts, opens no PRs. Promotion stays human-gated.

---
*Provenance: generated `2026-09-20T17:51:35` · profile `[profile free-opencode] draft=opencode/big-pickle, qa=opencode/big-pickle, judge=opencode/big-pickle` · reproduce: `python -m tools.eval.capability_report`*
