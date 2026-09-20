# Research Foodie — Data Flow & Framework-Stitching Details (数据流与缝合细则)

> **中文速览**
> 本文档回答三个问题：(1) **输入输出**是什么、落在哪些文件；(2) **中间运行阶段**每一步的具体进出（状态键、LLM 调用次数、失败路径）；(3) **到底缝合/使用/借用了哪些框架与工具、各到什么程度**。
> 核心结论（诚实版）：真正在运行时被**执行**的外部依赖只有 6 个——**LangGraph**（唯一 Python 框架，纯粹编排）、**opencode CLI**（主力免费模型）、**arXiv 官方 API**（发现/下载）、**MinerU**（PDF→Markdown）、**pandoc+xelatex**（Markdown→PDF）、**pypdf**（页数工具）。其余全部是**"模式借鉴、代码自研"**：DAS（状态机 S_lit…S_final + 16 维判题剧本，官方 harness 未运行）、STORM（大纲式样）、PaperQA2（claim+quote 证据式样）、orx（发现 rails 的**可选用例**，本机无该二进制）。HuggingFace `qiaojin/PubMedQA` 仅在**出题时**取数，场景上下文静态内嵌，无运行时依赖。

- `Updated`: 2026-09-20
- `Status`: Peers with `docs/PROJECT.md` (overview) + `docs/design/research-foodie-blueprint.md` (intent). This file is the **implementation truth**: exact I/O + stitch degree, verified against source 2026-09-20.
- `Language`: English master with 中文速览; code identifiers verbatim.

---

## 1. Inputs & outputs / 输入与输出

### Mode 1 — survey pipeline (`tools/pipeline/graph.py::Pipeline.run`)

**Inputs** (two entry patterns):

| Pattern | Arguments | Meaning |
|---|---|---|
| discovery-led | `question: str`, optional `discovery_backend: "seed"\|"arxiv"\|"orx"` (env `S_LIT_BACKEND`, default `seed`) | question → live candidates → resolved evidence pool |
| pre-parsed | `paper_id`, `parsed_md` | single-paper 1-pool mode (unit-test / demo path) |

**Output** — the final graph state (dict), trimmed and cached per scenario:

| Key | Type | Content |
|---|---|---|
| `papers` | `list[dict]` | **evidence pool**: `{arxiv_id, label, path, md}` (md ≤ 300 000 chars of MinerU markdown) |
| `taxonomy` | `dict` | `{topics: [str]}` |
| `outline` | `dict` | `{thesis: str, sections: [{heading, key_points: [str]}]}` (4–6 sections) |
| `claims` / `dropped_claims` | `list[dict]` | `{id, claim, quote, section, cite, confidence, paper_id, source}`; dropped = failed the 5-gram verbatim gate |
| `draft` | `str` | bilingual (EN+中文) survey draft, intro + ≥1 section + conclusion |
| `output` / `manuscript` | `str` | full Markdown manuscript (Title/Abstract/Intro/Evidence Table/References/Sources/Claims) |
| `validation` | `dict` | L6 `{passed, score, checks…, n_papers_cited}` **plus** `judge` verdict (4-axis) |
| `iteration` · `_elapsed` | `int` · `float` | revision counter (accumulator channel) · wall time |

### Mode 2 — evidence-grounded QA (`tools/pipeline/answer.py::answer_question`)

- **Input**: `question`, `paper_id`, `md` (≤ 40 000 chars), `mode=""|"yesno"`.
- **Output**: answer artifact (`## Answer (EN)` / `## 中文速览` / `## Source evidence`), then **deterministic gate** `check_answer(require_cite=True)` (min length, inline `(arXiv:id)`, source-evidence). Scored by `bench_eval.score_qa` (one judge call → `correctness` + `groundedness`).

### Mode 3 — battery (`tools/eval/pools_30.py`)

- **Input**: a DAS-Bench topic name (e.g. "RAG").
- **Output**: evidence pool (`_eval_out/pools_30.json`, incremental manifest) + judged row per topic in `pools_30_report.md` + manuscript PDFs.

### Where things land

| Artifact | Path |
|---|---|
| parsed paper markdown | `_demo_downloads/mineru_out_ds0509/{arxiv_id}/…/**.md` |
| evidence pools (30 topics) | `_eval_out/pools_30.json` |
| per-scenario cache (incl. QA rows) | `_eval_out/bench_cache/{id}.json` |
| benchmark report | `_eval_out/bench_pilot_das.md` |
| battery report + per-topic judge cache | `_eval_out/pools_30_report.md` · `_eval_out/pools_cache/` |
| variance records | `_eval_out/variance_runs.json` |
| rendered manuscripts (Markdown + PDF) | `_eval_out/manuscripts/{topic}_manuscript.{md,pdf}` |

## 2. Intermediate stages / 中间运行阶段（逐节点进出）

`lit → org → write → (review → revise_para → write) → finalize → gate → judge`. LLM calls all go through `tools/llm/client.py::LLMClient` (opencode or openai backend). Budgets below are what the code passes.

| Stage | Function | LLM calls | Input → output | Fail path |
|---|---|---|---|---|
| **lit** | `_lit` | 0 | parsed_md → `evidence_chunks` (blank-line split) | n/a |
| **org** | `_org` | 2 | cross-paper window (primary 5 chunks + 2nd paper 2 chunks, ≤2000 chars) + question → `taxonomy` (JSON `topics`), `outline` (JSON thesis/sections); fallback outline if parse fails | template default outline |
| **write** | `_write` | 1 + (sections+2) | per paper (≤3) 1 call each over ≤20 000 chars → claims, run `grounded_claims` (5-gram gate, drops ungrounded); then draft = intro + per-section body (≤6 sections) + conclusion, each its own call (`body` 520 tok, others 320) → `draft`, `claims`, `dropped_claims`, `iteration+1` | claims empty → review sends to revise |
| **review** | `_review` (conditional edge) | 0 | if `iteration > 3` → `stale` (converges to finalize); elif claims ≥1 and draft >30 chars → `pass`; else `revise` | max_revisions bounds |
| **revise_para** | `_revise_para` | 1 | draft + top-3 claims → improved draft (whole-draft rewrite; scoped-in-DAS design, wholesale here as skeleton) | → write again |
| **finalize** | `_finalize` | 0 | claims/outline/draft → assembled Markdown manuscript (title=question[:90]; abstract=intro[:800]; Evidence Table ≤12 claims; References dedup) | n/a |
| **gate** | `_gate` | **0 (zero-LLM)** | state + concatenated paper md → `validate()`: structure / cites (well-formed arXiv·DOI) / **grounding 5-gram** (fuzzy) + verbatim metric / bilingual / multi_paper | `fails` non-empty → `passed=False` (verbatim) |
| **judge** | `_judge` | 1 | manuscript + outline + claims[:4] over 4-axis rubric → `{label, score, checks{groundedness,structure,bilingual,clarity}, feedback}` (never raises) | parse failure → deterministic `fail` with reason |

Total ≈ **5–10 LLM calls / survey run** (papers + sections vary). QA mode = 1 call + 1 scorer call. Grounding claim drop is *mechanical* (5 contiguous content tokens must co-occur in source), so hallucinated quotes cannot reach the draft.

## 3. Framework & tool stitch ledger / 缝合与借用清单

Columns: **executed** (our code really calls it today) · **optional** (wired but binary/data absent here) · **borrowed** (spec/pattern re-implemented, code is ours) · **vendored** (copied in) · **reference** (downloaded/mentioned, not wired). Honest, verified 2026-09-20.

| Tool / framework | Role in this pipeline | Degree | Evidence (code) |
|---|---|---|---|
| **LangGraph** | Orchestrator: `StateGraph(PipelineState)` typed state, `iteration` reducer channel, 7 nodes, conditional edges `write→review`, compile+invoke | **executed — the only Python framework dependency of the core loop** | `graph.py:76-102` |
| **opencode CLI** (`opencode run --format json --pure -m opencode/big-pickle --auto -f tmpfile`) | Free hosted model = primary LLM backend; NDJSON event parse (text / text.delta / step_finish→tokens+cost); 3× flat retry | **executed — default backend** | `client.py:142-234` |
| **arXiv export API** (`export.arxiv.org/api/query`, Atom, relevance sort; `export.arxiv.org/pdf/{id}`) | Live discovery rail + corpus PDF download; stdlib `urllib`, no library; `_ID_RE` handles `vN` suffixes | **executed — `S_LIT_BACKEND=arxiv`, add_paper, pools** | `corpus.py:149-176,33` · `add_paper.py:34-38` |
| **MinerU CLI** (`mineru.exe -p … -o … -b pipeline -m txt -s -e`) | PDF→Markdown workhorse. Windowed ≤6 pp, **distinct `-o` dirs** (overwrite bug), sub-split recovery, 420 s timeout | **executed — the parse engine** | `add_paper.py:41-93` · runbook K7 |
| **pandoc + xelatex (MiKTeX) + Microsoft YaHei** | MD→PDF for MAR axis (CJK font so bilingual drafts render) | **executed — rendering step** | `render_manuscript.py:25-52` |
| **pypdf** (`PdfReader`) | Page count (parse windows; PDF page count after render) | **executed — micro-utility** | `add_paper.py:64` · `render_manuscript.py:49` |
| **DAS / DAS-Bench** (arXiv:2608.18034, repo `ZhikaiXu24/DAS`) | (a) **Borrowed architecture**: state model `S_lit/S_org/S_write/S_final`, scoped `revise_para`, "deterministic before semantic". (b) **16 criteria copied verbatim** into `DAS_16` (`# verbatim from benchmark/evaluation_protocol.md`). (c) **The official harness is NOT executed** — scoring is our own judge prompt applying the 16 criteria (1–5) over a ≤40K-char artifact view; family means are ours | **borrowed (architecture) + copied (rubric) + self-scores** | `bench_eval.py:44-72` · `graph.py:1-37` · `judge.py` |
| **STORM** (Stanford OVAL) | Outline pattern: "question-driven thesis + sections + key_points" — **knowledge-storm NOT imported**; our own JSON prompts | **borrowed (pattern only)** | `graph.py:145-167` |
| **PaperQA2 / ai2-scholar-qa** | Evidence-backed-claim pattern (claim + verbatim quote + section + cite) — **lib NOT imported**; `external/paper-qa` present but unused | **borrowed (pattern only)** | `graph.py:186-215` |
| **OpenResearch / orx CLI** | Discovery rail shell-out `orx discover keyword <q>` **only if the binary is on PATH** (absent here — Rust source only in `external/orx`); else falls back to the arXiv-API family it mimicks | **optional — not active in this env** | `corpus.py:183-197,93-97` |
| **HuggingFace `qiaojin/PubMedQA`** (pqa_labeled train) | **Authoring-time data source only**: 14 yes/no questions + abstract contexts + labels were pulled in Sessions 19 and embedded **statically** into `PubMedQA_SCENARIOS` (`context`, `gold_tokens`). No runtime import | **external data at design time; zero runtime dep** | `bench_eval.py:249-362` |
| **citation-verify** (vendored) | CrossRef / arXiv / S2 batch citation checker, vendored from the local citation-verification skill | **vendored — standalone, not yet wired into the loop** | `tools/citation-verify/*.py` |
| **mock_openai_server** | Deterministic fake OpenAI endpoint for mock tests | **ours (test fixture)** | `tools/llm/mock_openai_server.py` |
| Ollama | was a backend; **removed 2026-09-16** by user decision | removed | `client.py:96-100` |
| DAS-2M pool, PaddleOCR (Track B), GAIA, embedding index, Zotero+LaTeX assembly, Tongyi DeepResearch, ≥300B judge, proactive change-feed | blueprint roadmap; downloaded (`external/`) or planned, **not wired** | reference / future | blueprint §3–§6 |
| **OpenAI-compatible APIs** (DeepSeek/DashScope/OpenRouter/Moonshot/OpenAI) | `backend="openai"` — same client, `POST /v1/chat/completions`, JSON-mode via `response_format` | executed-if-configured (key-gated, not default) | `client.py:90-95,236-262` |

**Honest caveats on the stitch:**
1. **"STORM/PaperQA2 integration" in the docs means *pattern*, not dependency.** Both `external/` repos are downloaded but never imported; the outline/claims shape is ours. This is by design (`AGENTS.md`: reuse what's released, reimplement what's thin) — but say it plainly: **zero third-party LLM-agent frameworks besides LangGraph execute here.**
2. **The 16-dim DAS-Bench score is a self-scored approximation**, not the official harness output (which would need the OpenAlex judge + ≥300B model + rendered pages). The criteria text is verbatim; the scoring run is not the harness.
3. **`opencode/big-pickle` is a free hosted black-box** — we read its NDJSON for tokens/cost but can't pin weights; temperature >0 → judged-variance documented (`variance_run.py`).
4. Reasoning stacks are LLM-native (claims, outline, draft come from prompts with JSON schemas, not from a framework's planner).

## 4. Deliberately not stitched / 刻意不缝合

| Not used | Why (evidence) |
|---|---|
| Embedding/semantic index | Blueprint planned it; current discovery is seeded lexical scoring + arXiv relevance sort — small corpus, no precision gain measured yet (`corpus.py`) |
| DAS-2M dump | Only topic *names* drive `pools_30`; 2M-paper dump not pulled (`pools_30` fetches live arXiv) |
| Zotero + LaTeX | Replaced by pandoc+xelatex (lighter, CJK OK) for the MAR Part-1 stage (`render_manuscript.py`) |
| Proactive change-feed → re-discovery | Deliberately gated off to keep the graph convergent; blueprint §6 P4 |
| GAIA / Track B / ≥300B judge | External key/GPU/gating/input blockers (see `CAPABILITY-STATUS.md` §3) |

## 5. How to verify this file yourself / 自证路径

1. `rg "from langgraph" tools/` → only `graph.py:77`.
2. `rg "knowledge-storm|import paper_qa|import storm" tools/` → nothing.
3. `rg "mineru|pandoc|xelatex|opencode run|export.arxiv.org" tools/` → the six executed integrations above.
4. `_eval_out/bench_cache/PQ-*.json` → `context` is static (no HF call in run trace).