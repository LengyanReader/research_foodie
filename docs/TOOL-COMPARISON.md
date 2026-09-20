# Research Foodie — Tool Positioning & Stage-by-Stage Comparison (工具定位与逐阶段对比)

> **中文速览**
> 本文档把 research_foodie 的每个实现阶段与国内外该阶段的**对标工具**并排比较：我们做了什么、对标工具做什么、真实差在哪、以及 2026-09 此刻有哪些**可下载/可引用/可整合**的资产与缝合法。结论先行：(a) 我们强在**接地性**（5-gram 逐字验证 + 全局零 LLM 校验）与**本地零成本**；(b) 真正的功能缺口集中在 **L1 发现（DAS-2M 元数据湖）、L3 结构（STORM 式多视角/逆向路由）、L4 检索（PaperQA2 式 RCS 重排）、L6 判题（官方 DAS-Eval 工具包）**；(c) 2026-08 DAS 方法代码仍未发布，但 **DAS-Bench+DAS-Eval 评测工具包、DAS-2M、220 篇样例综述已全部公开**，是现阶段最该借用的资产。

- `Updated`: 2026-09-20
- `Status`: verified against source + 一手网页 2026-09-20 (arXiv repo/HF release pages)
- `Master`: English w/ 中文速览; companion: `docs/DATAFLOW-AND-REUSE.md` (our I/O truth) · `docs/design/research-foodie-blueprint.md` (intent)

---

## 1. Comparison by pipeline stage / 逐阶段对比

Legend — 🟢 our implementation ✓ · 🔵 gap vs the head-to-head tool

### L1 — Discovery (发现)

| | research_foodie (ours) | Head-to-head tool | Gap / insight |
|---|---|---|---|
| What | `seed` manifest (deterministic keyword scoring) · live **arXiv API** (urllib) · optional `orx discover` shell-out (binary absent) · `pools_30` fetch | **orx** `discover keyword` + `paper` (alphaXiv full-text search) · **DAS-2M** metadata lake (2M papers, HF, 2026-08) · STORM search backends (You/Bing/…RM) | 🔵 We have no **metadata lake**: discovery is breadth-limited to arXiv relevance top-K. **DAS-2M** gives a reusable survey-oriented 2M-paper index — biggest L1 asset to borrow |
| Evidence truth | ✅ every ID verified to primary source (PROGRESS ledger) | orx discovery is unverified → we'd still run our verification | keep ours |

### L2 — Evidence parsing (证据解析)

| | ours | Head-to-head | Gap |
|---|---|---|---|
| Parse | **MinerU** `-m txt` windowed ≤6pp, sub-split recovery, 420 s timeout (`add_paper.py`) | MinerU (same engine) · PaperQA2 uses **Grobid** parsing + chunking · DAS-2M pre-parsed metadata | 🔵 No **chunked-index / retrieval store** — we slice raw markdown, we don't index. MinerU parity, but we skip the index PaperQA2/DAS both build |
| Metadata | manual `_LOCAL_MD` registry + verified labels | PaperQA2 auto-fetches Crossref/S2 metadata **+ retraction check** (`pqa`) | 🔵 auto metadata + retraction = our vendored `citation-verify` step is manual |

### L3 — Structure / outline (结构)

| | ours | Head-to-head | Gap |
|---|---|---|---|
| Taxonomy | prompt over a 2 000-char cross-paper window → `topics` + outline (`_org`) | **STORM**: Perspective-Guided Question Asking (discover perspectives → simulated multi-turn convos → outline); **DAS**: candidate-grounded Taxonomy Planning + **reverse PaperRouter** (section→papers) | 🔵 No **perspective decomposition** (STORM's core, strongest measured effect on coverage/organization); **no reverse routing** (DAS's, unreleased code) |
| Note | STORM's core = "good questions"; direct outline prompts underperform (NAACL 2024) | — | our `_org` is closer to STORM's "Direct Gen" baseline than to STORM proper |

### L4 — Claim-led writing (写作)

| | ours | Head-to-head | Gap |
|---|---|---|---|
| Evidence→claims | per paper 1 LLM call over **raw first ≤20 000 chars** → grounded claims (verbatim 5-gram gate) | **PaperQA2**: Gather-Evidence = top-k dense retrieval → **LLM re-rank + contextual summarization (RCS)** → agent may traverse citations | 🔵 The critical L4 gap: **no relevance selection** — we take a raw window. PaperQA2's RCS (meta-described as decisive for RAG) is exactly what a cheap re-rank would add |
| Draft | intro + per-section grounded bilingual paragraphs | STORM deep-write w/ citations · DAS hierarchical paragraph planning | ~parity in shape; DAS adds cross-paper comparison subsections (unreleased) |

### L5 — Orchestration

| | ours | Head-to-head | Gap |
|---|---|---|---|
| Loop | LangGraph, 7 nodes, scoped-ish `revise_para` (whole-draft) | DAS stateful closed-loop w/ **scoped semantic review-and-repair** (their ablation: post-review variance 32%→1.9%) · orx parallel agent workspace | 🔵 our revise is whole-draft; DAS's scoped-loop benefit is a real but low-frequency win here (we rarely trigger revise) |

### L6 — Validation / judge (校验与判题)

| | ours | Head-to-head | Gap |
|---|---|---|---|
| Deterministic | ✅ zero-LLM L6 (structure/cites/5-gram grounding/bilingual/multi-paper) | DAS "deterministic before semantic" (same doctrine) | parity in doctrine; ours is genuinely zero-cost |
| Judge | 4-axis internal judge + **self-scored** 16-dim DAS-Eval (criteria verbatim) | **Official DAS-Eval toolkit now released (2026-08-20, GitHub+HF)** incl. evaluation code | 🔵 we re-implemented scoring; the **official runner exists and is ours-to-run** once a ≥300B OpenAI-compatible judge/GPU is wired |
| Human gate | manual checklist (blueprint §L6) | 220 DAS surveys (HF, 2026-08) usable as **few-shot calibration corpus** | borrow as rubric/quality anchors |

## 2. Reusable asset inventory (verified 2026-09-20) / 可复用资产清单

| Asset | Type | From | License / note | Reuse decision (Feas × Value) |
|---|---|---|---|---|
| **knowledge-storm** v1.1.1 | pip pkg (MIT) | Stanford OVAL | MIT (verified); litellm LMs+embeddings; **Co-STORM** in pkg; retrieval = You/Bing/**VectorRM**(user doc grounding)/Serper/Brave/SearXNG/DuckDuckGo/Tavily/Google | 🔵 **VectorRM + Outline module** = our L3 upgrade path; needs an OpenAI-compatible LM endpoint (we only have opencode CLI today → keep prompt version until then). Feas 3 · Val 3 |
| **DAS-Bench + DAS-Eval** evaluation toolkit | repo + HF | ZhikaiXu24 (2026-08-20) | released on HF; lic per repo/HF (unverified) | 🔵 **official 16-dim runner** to replace our self-score; needs ≥300B judge endpoint + rendered PDFs. Feas 2 · Val 5 |
| **DAS-2M** metadata lake | HF dataset | ZhikaiXu24 (2026-08-08) | released | 🔵 L1 discovery rail option (stream on demand). Feas 3 · Val 3 |
| **220 surveys by DAS** | HF (PDFs) | ZhikaiXu24 (2026-08-14) | released | few-shot + rubric calibration anchors. Feas 4 · Val 3 |
| **orx CLI / OpenResearch** | binary (Windows beta) | alphaXiv (MIT, verified) | MIT; needs Git for Windows; `orx install-skills` drops **SKILL.md into OpenCode**; `orx discover` / `orx paper` (alphaXiv full-text, no login) | 🔵 finally *enable* our dormant `S_LIT_BACKEND=orx` + adopt its agent-skills for the coding-agent lane. Feas 4 · Val 2 (it orchestrates agents, not our LangGraph) |
| **paper-qa** 2026.8.12 | pip pkg | Future-House | open-source; **RCS re-rank** = the L4 technique we'll **mirror cheaply** (BM25-style, zero dep); full agentic RAG optional later | Feas 5 (mirror) / 3 (adopt) · Val 4 |
| **opencode-academic-research** | OpenCode skill suite | timpara (2026-05) | CC BY-NC 4.0 (verified); 4 skills · 13 slash cmds · 38 agents: research/write/**peer-review**/revision prompts | 🔵 reuse the **review-stage prompts** for our human L6 lane; adjacent, no core-loop risk. Feas 4 · Val 3 |
| Local skills already installed | skills | `~/.agents/skills/` | academic-research-writer · citation-verification · research · (find/skill-creator) | wire `citation-verification` into assembly; keep `academic-research-writer` for human polish |
| STORM prompts/method | paper Appendix B (DSPy pseudo-code+prompts) | NAACL 2024, arXiv:2402.14207 | CC per arXiv | perspective-asking (max_turn×(max_perspective+1) budget) replicable with our client now. Feas 5 · Val 4 |

## 3. Bottom line / 结论

1. **借 DAS 生态**（现已全公开：评测工具、元数据湖、220 样例）是"按最近基准对齐"的最短路径；唯一等待项是 ≥300B 判题端点。
2. **补 L4 检索重排**是本阶段性价比最高的自研缺口（PaperQA2 RCS 的轻量复刻，零依赖）。
3. **L3 多视角**（STORM 思想）与 **L6 官方 DAS-Eval** 分别代表"现在可做"与"等资源可做"。
4. **方法代码仍未公开**（DAS ⏳ to be released）→ 状态机/路由继续按论文复现是我们的既定路径，未被下游变化推翻。