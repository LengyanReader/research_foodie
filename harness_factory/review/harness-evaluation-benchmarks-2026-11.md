# Agent-capability evaluation · benchmarks, test-banks & harnesses — a landscape scan for P70

**Updated:** 2026-11-04 · **Status:** research findings — **applied as round P70 on 2026-11-04** (registry: `data/cycles.json` P70). · **Scope:** the external ecosystem that *tests* agent/harness capability — public **benchmarks / test-banks**, the **evaluation harnesses** that run them, and the **grading semantics** — read against this factory's own capability demonstration (`data/battery.json` 9 families · `data/scoreboard.json` 7 tasks × 5 axes · watchlist `evaluation-gates`), as of R29 / R185 / R243 / R279 and 43 catalogued tools (2026-11-04).

> 中文速览：这是 **P70 全网扫描轮**（observe 半环）。目标不是再攒一个榜单，而是回答两个问题：**外部拿什么考 agent 的能力**（题库/benchmark），以及**这套考法反过来对本库「能力体现」提出什么新要求**。三分对象：**① 题库/benchmark**（SWE-bench R29、τ-bench/τ²-bench、GAIA、OSWorld、WebArena、AgentBench、HELM R185、HAL、Terminal-Bench 2.0、RE-Bench、FORCE-Bench）；**② 评测框架/runner**（Inspect AI·UK AISI、OpenAI Evals、promptfoo/deepeval、HAL orchestrator）；**③ 判分语义**（**pass^k 可靠性**、**数据库状态判分** ThinkingBox R279、**harness 不披露即不可比** R243、**基准污染/HF 泄漏**）。一手来源逐条核验、带访问日期，未深读标 *listed*。
> **对本库的落点（提升能力体现）**：单次通过率（pass@1）不足以证「能力」——同一任务连跑 k 次的 **pass^k**、以**终态/断言**而非模型自述判分、以及**防污染**检查，才与本库既有的 M5.11 证伪、M5.12 方差敏感、M5.13 留出与「judge_checks 先于执行声明」同构。于是本轮：新基准登记入 `sources.json`/`references.md`（R282–R290），加宽 `evaluation-gates` 侦察主题使常转 `full-update` 能摄取新榜单，并在证据仪器表落一行 **agent 能力评测** 仪器 + 一个 **PENDING 试验族**（spec 就绪、`results` 留空＝不臆造）+ 纯标准库 `passk.py`（从既有 `task_outcome` 轨迹算 pass^k）。

---

## 1 · Method · 方法

Follows the standing scan pipeline (`frontier-2026-10.md` §1 / `harness-landscape-scan-2026-10.md` §1; the apply half stays human-directed):

```
probe (websearch, 2026-11-04) → fetch primary (arXiv abs / GitHub / official page)
    → dedup vs references.md (R1–R281) → grade against the discriminating test
    → register the verified subset → wire into the standing loop (watchlist / battery / instrument)
```

- Secondary roundups (prefactor.tech, morphllm, benchclaw, kosmoy, hamel.dev) were read **for orientation only** and are **not cited** — the no-laundering rule.
- Every entry below carries its source and status: **fetched** = primary page/abstract read on 2026-11-04; **listed** = surfaced by search / repo metadata only, not deep-read.
- **Dedup already done:** SWE-bench is **R29** and HELM is **R185** in the consolidated list — they are *cross-referenced*, not re-added; the numbered additions are the **benchmark/eval papers not yet in the corpus** (R282–R290).

## 2 · The map · 三分对象

### 2a · Benchmarks / test-banks · 题库（what they grade）

| Benchmark · 名称 | Grades · 判什么 | Reliability idiom · 可靠性口径 | Verifiable verdict · 判据形态 | Access | Ref |
|---|---|---|---|---|---|
| **SWE-bench** — real GitHub issues, 2 294 inst. / Verified 500 | resolve-a-task (repo patch) | pass@1 headline; harness-controlled "Bash Only" 500 | **test-suite run** (fail→pass) | leaderboard fetched 2026-11-04 | R29 (existing) |
| **τ-bench / τ²-bench** — tool-agent-user, simulated user | multi-turn tool use + policy compliance | **pass^k** (k repeated runs must all succeed) | **DB state** after the conversation | abs + repo fetched 2026-11-04 | **R282/R283** |
| **GAIA** — general-assistant, 466 q. | tool+reason+browse, unambiguous final answer | exact-match single score | **golden answer** match | abs fetched 2026-11-04 | **R284** |
| **OSWorld** — real-OS GUI tasks | computer use (GUI, apps) | pass rate over 369 tasks | **scripted env-state checks** | abs fetched 2026-11-04 | **R285** |
| **WebArena** — self-hostable web env | long-horizon web navigation | functional-correctness reward | **reward function** on DB/page state | abs fetched 2026-11-04 | **R286** |
| **AgentBench** — 8 interactive envs | LLM-as-agent breadth | per-env success | env-specific success metrics | abs fetched 2026-11-04 | **R287** |
| **HELM** — holistic multi-metric | accuracy + calibration/robustness/fairness/efficiency | multi-metric, not one number | per-scenario metrics | repo fetched 2026-11-04 (**maintenance mode 2026-06-01**) | R185 (existing) |
| **HAL** (Holistic Agent Leaderboard) — 21 730 rollouts / 9 models / 9 benchmarks / 8 partners | *meta*: standardized orchestration | **3-D model×scaffold×benchmark** | re-runs each benchmark under one harness | abs fetched 2026-11-04 | **R288** |
| **Terminal-Bench 2.0** — harbor-framework, 89 hard terminal tasks | agent work in a shell | harness + model reported **together** | **pytest** per task | repo fetched 2026-11-04 | **R289** |
| **RE-Bench** — frontier AI R&D (MLE-style) | autonomous research/engineering | vs **human expert** baseline | metric per task + submission validity | abs fetched 2026-11-04 | **R290** |
| **FORCE-Bench** — enterprise-finance agentic, 251 expert q. | domain agentic responses | **rubric-based**, calibrated | rubric scoring | abs listed 2026-11-04 | *listed* |

### 2b · Evaluation frameworks / runners · 评测框架

- **Inspect AI** — UK AI Security Institute, `github.com/UKGovernmentBEIS/inspect_ai` (**MIT**, PyPI `inspect-ai`), a framework for LLM evals with **over 200 pre-built evaluations** ready to run on any model; built-in prompt engineering, tool usage, multi-turn dialog, and **model-graded** evaluation; solvers/scorers/datasets are composable. Docs publish a coding-agent index (`llms.txt`). *fetched* 2026-11-04. → nearest external instrument to this factory's **paired-trial** idea (a controlled harness that runs the same task across conditions).
- **OpenAI Evals** — `github.com/openai/evals` (**MIT**), a registry of evals + a runner; simple template-based and model-graded evals. *fetched* (license + releases feed) 2026-11-04.
- **promptfoo** — already registered (`sources.json` tools, `eval`+`red-teaming`, feed-pullable): declarative prompt/agent/RAG tests + red-team scans with CLI/CI. This factory's *existing* nearest instrument to an external eval runner (`harness-landscape` F5).
- **HAL orchestrator** — the paper's contribution is the **harness**, not a new task set: parallel evaluation across hundreds of VMs, cutting eval time from weeks to hours and removing implementation bugs. *listed*.

### 2c · Grading semantics worth stealing · 判分语义

1. **pass^k, not pass@1** (τ-bench/τ²-bench; echoed by ThinkingBox R279's "repetition is the trust test"): report the fraction of runs in which the agent succeeds **every** time over k trials — a reliability quantity. τ-bench's own leaderboard shows Pass^1 0.46 → Pass^4 0.22 on airline (Claude-3.5-Sonnet), i.e. **one-shot ≠ dependable**.
2. **Grade terminal state, not the model's say-so** (τ-bench DB state; OSWorld/WebArena scripted checks; ThinkingBox R279 side-effect-diff vs required end state): the agent's *claim* that it finished is treated as exactly that — a claim. The check is the environment's post-state.
3. **Disclose the harness or the number is meaningless** (this is the library's own thesis, stated in the literature at **R243** "Stop Comparing LLM Agents Without Disclosing the Harness"): HAL makes this operational by re-running benchmarks under a *named* scaffold; Terminal-Bench reports harness+model jointly. An undisclosed scaffold hides the confound between "better model" and "better scaffolding".
4. **Contamination is a live threat** (HAL, *reported from abstract*): LLM-aided log inspection surfaced agents **searching HuggingFace for the benchmark** instead of doing the task, and *higher reasoning effort reducing accuracy in the majority of runs* — both are reasons to hold a benchmark **out of training/derivation** (M5.13) and to keep a fixed grader (M5.13(a)/(d)).

> 中文：四条可直接借用的判分口径——**多次一致（pass^k）**而非单次；**判终态**而非听模型自报；**披露 harness** 否则数字不可比（本库 R243 立场，HAL/Terminal-Bench 已在操作层落实）；**防污染**（agent 会去 HF 搜榜单；「更多推理反而更差」也已被记为观察，故基准须留出一轮不入推导，M5.13）。

## 3 · Diff against this factory · 覆盖差集

What we already had vs what P70 adds:

| Surface · 面 | Before P70 | Gap found by the scan | Action |
|---|---|---|---|
| Paired bare-vs-harness trials | `battery.json` 9 families, all `done`, single-shot `A-bare`/`B-harness` ratios | no **reliability** dimension — a family can read 1.0 on one rollout yet be undependable | add a **PENDING** family `agent-eval-reliability` with declared `judge_checks` + `results` left empty |
| Grading idiom | `judge_checks` (E1–E5 claim/source/provenance), `scoreboard` effect axis | nothing computes **pass^k** from repeated outcome traces | add `passk.py` (pure stdlib, reads `updates/traces.jsonl` `task_outcome` events) |
| External benchmark registry | promptfoo / deepeval / nemo-guardrails (tool-level) | no **test-banks / leaderboard harnesses** catalogued | register the verified subset in `sources.json` tools + `references.md` §AE |
| Standing discovery | `evaluation-gates` queries are generic ("LLM agent evaluation") | new named benchmarks never surface into the harness cluster | widen `evaluation-gates` queries/keywords (SWE-bench, tau-bench, OSWorld, pass^k, leaderboard, …) |

## 4 · Discriminating test — does any of this open a *new capability*, or only new *data*? · 判别性

Applying `reference/integration-map` §0: P70 is **data + one instrument hook**, not a new engine.
- Registered entities are *inputs to observe*, each feeding the standing `full-update` via `sources.json`/watchlist — no code surface of its own (M0.4).
- `passk.py` is the single new *consumer-facing* function: it turns the existing `task_outcome` trace stream into the reliability quantity the benchmarks demand, so the capability bar (pass^k + state-graded + contamination-held-out) becomes **measurable on our own dogfood** — the honest way to "raise the capability demonstration" without inventing scores.

## 5 · What this round did NOT claim · 明确不做

- **No benchmark result is quoted as this factory's own capability.** The pass rates above belong to the cited papers' *models under *their* harnesses*; we register them as instruments and leads.
- **HAL's headline numbers (21 730 rollouts, ~$40 000, "higher reasoning reduces accuracy", HF-search contamination) are *reported from the abstract*, not replicated** — labelled *reported*.
- **The PENDING battery family ships with `results` empty on purpose** — a declared-but-unrun trial (M5.13 "judge_checks before execution"); running it is the next compute-bearing round, gated on real repeated rollouts.
- **τ-bench / HELM repo licenses not re-verified this session** (their *papers* are the cited object; `sources.json` tool entries record the feed and the arXiv id, and license is marked where confirmed: SWE-bench MIT, HELM Apache-2.0, OpenAI Evals MIT, Inspect MIT).

---

## 6 · Source register · 出处

Full IEEE entries in `review/references.md` **§AE (R282–R290)**; BibTeX in `references.bib`. Access date for all: **2026-11-04**. Cross-references into existing numbers: SWE-bench **R29**, HELM **R185**, harness-disclosure thesis **R243**, ThinkingBox state-grading **R279**.
