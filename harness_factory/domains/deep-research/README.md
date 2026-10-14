# Domain · Deep research · 深度调研域
> Wiring `core/` modules into an **Anthropic-grade** deep-research loop: plan → parallel search → screen → extract → synthesize → verify → iterate.
> 把 `core/` 模块接线成一条 **Anthropic 级**深度调研闭环：规划 → 并行检索 → 筛选 → 抽取 → 综合 → 校验 → 迭代。
**Updated:** 2026-10-13

---

## 中文速览
深度调研域的目标：**给一个课题，做出一份可溯源、能自评、敢标注不确定的调研报告——达到 Anthropic「多智能体研究系统」的水准**。核心不是「搜一次、总结一下」，而是：**先规划再执行**（把课题拆成子问题与检索计划）、**多路并行检索**（web + 学术）、**筛选去重**、**抽取证据**、**带矛盾的综合**、**逐条引文审计**、**按缺口迭代**、最后**自评**。以 L0–L9 编排 `core/`。**铁律：没有来源就不下断言（M0.1/M0.2/M4）；来源冲突必须呈现而非抹平；覆盖与置信度必须显式。**

> 本域 = 编排方法论（本文件 + `method.md`）+ 工具目录（`deep-research` class）+ 质量评测（`research-eval`）。方法论对齐 Anthropic《How we built our multi-agent research system》，工具可替换。

---

## What this domain is for · 用途
Produce a **decision-grade research brief** on a topic: what is known, who disagrees, how strong the evidence is, what is still open, and where each claim comes from — plus an honest statement of coverage and confidence. On a **local-first, near-zero-cost** stack where possible; paid search/LLM only at quality-critical steps.

## Why "deep" ≠ "one search" · 为什么「深」不等于「搜一次」
Anthropic's multi-agent research system beats a single agent mainly through **token-budgeted breadth**: an orchestrator **decomposes** the question, spawns **parallel subagents** that each search a slice, and a synthesizer **merges + verifies**. The gains come from *coverage*, *parallelism*, and *verification* — not from a longer single prompt. This domain encodes exactly that.

## Pipeline layers · 分层流水线（L0–L9）
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Scope the question | M0, M7 | restate the ask; define deliverable, audience, decision, time box |
| L1 | Plan & decompose | M0, M1 | sub-questions, search plan, source-type mix (web/academic/primary), stop criteria |
| L2 | Parallel search | M6, M1 | multi-query, multi-engine; **breadth first**; record every query + hit |
| L3 | Retrieve & parse | M6, M2 | fetch full text / endpoints; normalize (see `../reading/`) ; hash + cache |
| L4 | Screen & dedup | M3, M4 | relevance, inclusion/exclusion, near-duplicate collapse, source credibility |
| L5 | Extract evidence | M1, M4 | evidence table: claim · quote/paraphrase · source · strength · stance |
| L6 | Synthesize | M1, M3 | themes, agreements, **contradictions kept**, gaps; minimal high-signal context |
| L7 | Verify & citation-audit | M3, M4 | every claim → source resolves; quote accuracy; default-FAIL on unresolved |
| L8 | Iterate / gap-fill | M2, M5 | detect uncovered sub-questions → new queries; run to stop criteria |
| L9 | Report & self-eval | M4, M7, M3 | brief + coverage & confidence + limitations; separate evaluator rubric |

> L0–L9 are a **loop**, not a line: L7/L8 send you back to L1/L2 until stop criteria (coverage, budget, or diminishing returns) are met.

## Orchestration pattern · 编排模式（Anthropic-style）
```
                 ┌───────────────┐
   question ───▶ │  Orchestrator  │  (plan, decompose, allocate budget)
                 └──────┬────────┘
        ┌───────────────┼───────────────┐        parallel subagents
        ▼               ▼               ▼
   [subagent A]    [subagent B]    [subagent C]   each: search slice -> extract
   web-primary     academic         primary/domain  with its own citations
        └───────────────┼───────────────┘
                        ▼
                 ┌───────────────┐
                 │  Synthesizer   │  merge, dedup, keep contradictions
                 └──────┬────────┘
                        ▼
                 ┌───────────────┐
                 │    Verifier    │  claim↔source audit (separate pass, M3)
                 └───────────────┘
```
- **One orchestrator, many workers.** The orchestrator plans and owns the stop criteria; workers never self-publish.
- **Subagents are narrow.** Each gets one sub-question + a source-type mandate + a budget → higher recall, less context bleed (M1).
- **Synthesisers and verifiers are separate from searchers** (M3) — the agent that wrote a claim must not be the one that clears it.
- **Everything is logged** (queries, hits, fetches, decisions) so the brief is reproducible and auditable (M4/M0.9).

## Quality bar · 质量标准（"Anthropic 级" 的判据）
A brief is **decision-grade** only if all hold:
1. **Scope fidelity** — answers the actual question, not an adjacent one.
2. **Breadth** — multiple independent source types; no single-source conclusions on contested points.
3. **Citation integrity** — every non-trivial claim resolves to a checkable source; quotes are verbatim (M0.2/M4).
4. **Contradiction honesty** — disagreements and weak evidence are shown, not averaged away (M0.1).
5. **Provenance** — source + access date + (for papers) ID; `unverified` where it can't be traced.
6. **Coverage accounting** — says what was *not* found and which sub-questions stayed open.
7. **Calibration** — confidence is stated and matches the evidence.
8. **Self-evaluation** — a separate rubric pass scores the brief before delivery (M3).

See `method.md` for the full operating playbook (query decomposition, screening, evidence table, contradiction handling, stopping criteria, evaluation rubric).

## Module combination · 模块组合
- **M0** — constitution: no source → no claim; present uncertainty; never fabricate a reference.
- **M1** — isolation: each worker/synthesizer sees only its slice; protects context from corpus-dump.
- **M2** — long runs persist a research ledger (queries, hits, evidence table) and resume across sessions.
- **M3** — separation: independent verifier + rubric evaluator; default-FAIL until claims resolve.
- **M4** — the spine: claim ↔ source(URL/ID, access date) ledger; quotes verbatim; `unverified` fenced.
- **M5** — the loop: coverage/recency signals drive new queries; stop on criteria, not on fatigue.
- **M6** — tools: search, fetch, parse (see the `deep-research` and `reading` catalog classes), minimal & fail-loud.
- **M7** — deliverable: reviewable, no auto-publish; scope + budget declared up front.
- **M8** — escalate to a human on scope ambiguity, contested/high-stakes claims, or unobtainable sources.

## Tooling · 工具目录
`harness catalog --class deep-research` lists: research agents (OpenAI/Gemini Deep Research, Claude Research, Perplexity, `gpt-researcher`, `open-deep-research`, STORM), web search (Exa, Tavily, Brave, SearXNG, SerpAPI), academic search (Semantic Scholar, Crossref, OpenAlex, Europe PMC, CORE, Scite, Litmaps), retrieval/RAG (LlamaIndex, LangChain, FAISS, Qdrant, Chroma, BM25, sentence-transformers), crawlers/content extraction (Trafilatura, readability, Jina Reader, Firecrawl, Crawl4AI), screening (Rayyan, Covidence, ASReview), and research evaluation (GAIA, BrowseComp, HLE, FRAMES, DeepResearch Bench).

## Human-notification triggers · 人工通知触发
| trigger · 触发 | action · 动作 |
|---|---|
| Scope ambiguous / no decision named · 课题含糊 | restate + confirm before searching |
| Contested high-stakes claim · 高利害争议 | present both sides + evidence; escalate |
| Key source unobtainable / paywalled · 关键来源不可得 | report + request access; do not fabricate |
| Coverage stop-criteria unmet with budget exhausted · 预算内未达覆盖 | deliver partial + explicit gaps; ask |
| Verifier cannot resolve a claim · 无法归证 | mark `unverified`; do not present as fact |

## Anti-patterns · 反模式
- Single-query "search then summarize" (the cardinal deep-research failure).
- Averaging away contradictions; hiding weak evidence (M0.1).
- Fabricated or stale citations (M0.2/M4 — the cardinal sin).
- Corpus-dump into one window, losing provenance (M1).
- No coverage/confidence statement; overconfident tone.
- Publishing without the separate verifier/evaluator pass (M3/M7).

## See also
`method.md` (operating playbook) · `../research/README.md` (local-first academic pipeline) · `../reading/README.md` (acquire/parse/distill) · `../model-selection/README.md` · `../core/05-provenance-and-integrity.md` · `../review/harness-index.md`.
