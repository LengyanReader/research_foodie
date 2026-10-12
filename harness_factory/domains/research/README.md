# Domain · Research · 科研域
> Wiring `core/` modules into a local-first research pipeline.
> 把 `core/` 模块接线成一条「本地优先」的科研流水线。
**Updated:** 2026-10-12

---

## 中文速览
科研域的目标是**可溯源、可复现、成本敏感**地把「问题 → 综述/结论」跑通。它以 L0–L6 分层编排 `core/`：L0 建档（M7）、L1 取文（M6）、L2 解析（M6）、L3 归证（M4）、L4 综合（M1/M3）、L5 评分（M3）、L6 出稿（M4/M7）。工具默认开源免费（opencode CLI、arXiv API、MinerU、pandoc+xelatex、pypdf），付费仅用于质量关键步。**引用即生命线**（M0.2/M4）。

---

## What this domain is for · 用途
Turn a research question into a cited, reproducible deliverable — a survey, a report, a manuscript — on a **local-first, near-zero-cost** stack, without outsourcing judgment. Derived from the archived `research_foodie` pipeline (`_archive/docs/PROJECT.md`, `DATAFLOW-AND-REUSE.md`, `TOOL-COMPARISON.md`, `CAPABILITY-STATUS.md`).

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Scaffold & plan | M7, M0 | project dir, plan-first, run ledger |
| L1 | Acquire sources | M6, M0.2 | arXiv/API fetch; record IDs + access dates |
| L2 | Parse & normalize | M6, M2 | PDF → markdown (MinerU/pypdf); idempotent hashing |
| L3 | Ground claims | M4, M3 | claim ↔ source ledger; `verified`/`unverified` |
| L4 | Synthesize | M1, M3 | minimal high-signal context; draft from evidence |
| L5 | Judge & score | M3 | separate evaluator; three-state; default-FAIL |
| L6 | Publish | M4, M7 | references (IEEE), render (pandoc+xelatex), no auto-push |

## Module combination · 模块组合
- **M0** is the constitution: truth before throughput; every claim sourced.
- **M1** keeps each synthesis step's context to the evidence at hand, not the whole corpus.
- **M2** makes long runs resumable (large PDF batches, multi-hour synthesis).
- **M3** separates the writer from the evaluator; "done" requires evidence.
- **M4** is the domain's spine: claim→source→access-date ledger; injection-safe fetch.
- **M6** supplies the tool set: fetch, parse, render — minimal, fail-loud.
- **M7** governs the deliverable: reviewable diffs, no unsolicited publish.

## Anti-patterns
- Fabricated citations (violates M0.2/M4 — the cardinal sin).
- Summarizing away uncertainty (M0.1/M0.4).
- Dumping the whole corpus into one window (M1).
- Publishing results with no rollback or review (M7/M0.8).

## See also
`../core/00-index.md` · `../sources/source-map.md` (research row) · `../review/harness-catalog.md` · `_archive/docs/` (source project).
