# research_foodie

A local-first, cost-sensitive **proactive academic research pipeline** — from question to citation-grounded, publication-oriented draft, with human gates.

> 中文速览：research_foodie 是一套本地优先、成本敏感（核心成本≈$0）的主动式学术研究流水线，双轨覆盖 CS/ML 技术综述与多语言人文研究。输入一个问题（或一个受监控的领域），输出一份逐句可溯源到具体论文的综述草稿，并在文献变化时自动标记待更新的章节。已交付 `tools/llm/` 统一 LLM 接口（**默认后端 = opencode CLI 免费模型 `opencode/big-pickle`**；Ollama 后端已于 2026-09-16 移除）与 `tools/pipeline/` LangGraph P2 最小纵切（**可插拔 S_lit 发现 rail (`seed|arxiv|orx`) + STORM-style 大纲 + 全文 claim 抽取 + L6 确定性校验门 + 写时反幻觉过滤 + DAS-Bench-style AI 评审门**；mock **19/19** + real `opencode/big-pickle` **18/18**，judge=pass；**已在第二篇真实论文（Weber-Wulff `2306.15666`）上验证泛化**）；并复用 DAS-Bench 数据集资产做了 **16 轴基准评测试点**（`tools/eval/bench_eval.py`，预览总分 2.44–3.19，报告 `_eval_out/bench_pilot_das.md`）；`langgraph` 1.1.10 安装于 `ds0509`。下一阶段：S_lit 多论文证据（攻 MAR/多引用短板）+ P3 评审门槛校准 + DAS-2M/≥300B 评审。

## Purpose & pipeline at a glance / 目的与流水线总览

**What it does:** turns a research question (or a monitored field) into a citation-grounded, publication-oriented draft, then keeps that draft current as the literature moves.
**What it does NOT:** it is not a black-box "deep research" product; it never auto-ships a manuscript without a human gate. Mechanical validation runs before any AI judge; AI revises, humans accept (see blueprint §0).

```
[L0] Question / field watch
  │
  ▼
[L1] Discovery   queries + change feed → candidate pool (DAS-2M · OpenAlex · S2 · orx · Ai2 ScholarQA)
  │
  ▼
[L2] Evidence    parse PDFs (MinerU / PaddleOCR) → 8-field records → dual index (lexical + embedding)
  │
  ▼
[L3] Structure   taxonomy outline (STORM) → paper→section routing
  │
  ▼
[L4] Writing     per-section claim plans → grounded drafting (PaperQA2 / ScholarQA)
  │
  ▼
[L5] Orchestrate  LangGraph state machine  S_lit → S_org → S_write → S_final
  │                    ▲                         │
  │   proactive loop:  └── flagged stale → scoped re-discovery ─┘
  ▼
[L6] Gates        deterministic checks → DAS-Bench judge → HUMAN checkpoint
  │
  ▼
Manuscript  (Zotero + Pandoc + LaTeX)   ·   Track B adds OCR+translation with expert gate
```

Workflow step-by-step and state details: `docs/design/research-foodie-blueprint.md` §3.
How to operate the environment (commands, smoke tests, known issues): `docs/setup-runbook.md`.

## Documents

| Doc | What it is |
|---|---|
| `docs/refs/ai-research-tools-workflow-guide.md` | Verified (2026-09-15) tool survey: full workflow arc, updates, Verification Ledger, References |
| `docs/design/research-foodie-blueprint.md` | Bilingual architecture blueprint: purpose/non-goals, L0–L6 workflow, state machine, reuse map, cost matrix, phased roadmap P1–P5 |
| `docs/setup-runbook.md` | Bilingual operations runbook: conda env, verified commands, smoke-test results, known issues (K1–K12), local-model candidates, next steps |
| `docs/PLAN.md` · `docs/PROGRESS.md` | Execution plan + progress log (track-as-you-go) |
| `tools/citation-verify/` | Vendored citation-verification harness (CrossRef/arXiv/Semantic Scholar clients) |
| `tools/llm/` | Unified LLM client — **`opencode` (default, hosted free model via CLI)** + `openai` (DeepSeek/DashScope/OpenRouter/Moonshot) — one interface; keyless mock smoke test. Ollama backend removed 2026-09-16 |
| `tools/pipeline/` | P2 LangGraph minimal vertical — S_lit(discovery rails: seed / arXiv API / orx CLI) → S_org(taxonomy + STORM outline) → S_write(grounded claims + outline-driven draft) → S_final → **L6 gate** → **P3 judge**; write-time grounded-claim filter; mock + real integration tests (`judge.py`, `corpus.py`, `validate.py`, `graph.py`); en route: DAS-2M/live sweeps |
| `external/` | Downloaded harness repos for later phases (gitignored): STORM, DAS(+DAS-Bench), paper-qa, MinerU, PDF-Extract-Kit, DeepResearch, open_deep_research, orx, OpenResearch |

## Status

- **Phase 0/1 (docs)**: complete. **P1 tooling**: MinerU PDF→Markdown PASS in `ds0509`; PaddleOCR Chinese OCR PASS (K7 closed); remote GPU deferred. **P2 minimal vertical + framework integration + generalization + benchmark-style eval**: `tools/pipeline/` LangGraph pipeline + pluggable S_lit rails (`corpus.py`: seed | **arXiv API — verified reachable 2026-09-16** | orx CLI adapter) + STORM-style outline (`S_org`) + `validate.py` L6 gate + `judge.py` **P3 DAS-Bench-style AI judge** — **mock 19/19 + real `opencode/big-pickle` 18/18 (121.7 s, STORM outline 3 sections, full-text claims, draft 3357 chars, score 1.0, judge=pass)**; **generalization proven: 2nd real paper (Weber-Wulff `2306.15666`) full loop PASS in 149.8 s (4 claims, score 1.0, judge=pass)**; **DAS-Bench 16-criterion evaluation pilot (`tools/eval/bench_eval.py`, Session 11): preview totals P-A 2.62 / P-B 3.19 / 001 2.44 / 019 no-evidence, report `_eval_out/bench_pilot_das.md`**; `langgraph` 1.1.10 installed. Write-time grounded-claim filter mechanically blocks fabrication; seed rail stays the deterministic offline default (orx binary not installed in this env → wired arxiv→seed fallback).
- **Default LLM / models**: `tools/llm/client.py` defaults to the **`opencode` backend** (`opencode/big-pickle`, hosted free model via `opencode run --format json`) — smoke 3/3 · pipeline 18/18 (121.7 s, claims=4, outline 3 sections, score 1.0, judge=pass). **Ollama backend removed 2026-09-16** (user decision); local-model evaluation from Session 6 is archived in PROGRESS as history.