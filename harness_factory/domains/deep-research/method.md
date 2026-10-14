# Deep research · Operating playbook · 深度调研操作手册

> The step-by-step method behind the `deep-research` domain. Deterministic, checkable, model-agnostic.
> `deep-research` 域背后的分步方法。确定性、可核查、与模型无关。
**Updated:** 2026-10-13 · Companion to `domains/deep-research/README.md`.

---

## 0. Research ledger · 调研台账（贯穿全流程）
Persist one append-only ledger so any run is reproducible and auditable (M2/M4). · 全程维护一份只追加的台账，保证可复现、可审计。

```yaml
question: <verbatim ask>
decision: <what this informs>        audience: <who reads it>
sub_questions: [ {id: q1, text, status: open|answered|dead, sources: [...]}, ... ]
queries:   [ {id, text, engine, ts, hits: N, used: N, by: subagent} ]
sources:   [ {id, url|doi|isbn, title, author, year, type, retrieved_at, credibility: high|med|low} ]
evidence:  [ {claim_id, text, source_id, locator, stance: supports|refutes|mixed|context, strength} ]
claims:    [ {id, text, evidence: [...], status: verified|unverified|contested} ]
coverage:  { q1: 0.7, q2: 1.0, ... }   gaps: [...]   confidence: low|med|high
stop:      { reason: coverage|budget|diminishing, at: ts }
```

## 1. L0 Scope · 界定
Restate the ask; name the **decision** it supports, the **audience**, the **deliverable** (memo/brief/report), the **time/budget box**, and any **must-use / excluded** sources. If the ask is ambiguous, **stop and confirm** (M8).

## 2. L1 Plan & decompose · 规划与分解
Turn the question into **3–7 sub-questions** that are independently searchable, then define the **search plan**: which source types per sub-question, which engines, and the **stop criteria**.

Decomposition patterns · 分解模板:
- **Stakeholder / actor** — split by who: regulators, vendors, researchers, users.
- **Dimension** — split by facet: definition, evidence, cost, risks, alternatives.
- **Temporal** — split by era: origins, current state, outlook.
- **Contrastive** — split by claim: arguments *for* vs *against*.
- **Method/level** — split by scale: individual, org, market, society.
- **Open-vs-closed** — split by what is settled vs contested.

For each sub-question, pre-write **2–4 query variants** (synonyms, jargon↔lay, site: filters, date bounds). · 每个子问题预写 2–4 个查询变体。

## 3. L2 Parallel search · 并行检索
Breadth-first, multi-engine, multi-type. Run subagents in parallel, one sub-question each. · 广度优先、多引擎、多来源类型；子代理并行。

| source type · 类型 | engines/tools · 工具 | use for · 用途 |
|---|---|---|
| Web (open) | Exa, Tavily, Brave, SearXNG, Perplexity | current state, news, primary pages |
| Academic | Semantic Scholar, Crossref, OpenAlex, Europe PMC, CORE, Scite, Litmaps | peer-reviewed evidence, citation trails |
| Primary/domain | gov/statistics, filings, standards, docs | authoritative facts, numbers |
| Reference/books | see `../reading/` libraries | definitions, background |

Rules · 规则: record **every** query + counts; note when you **switch** a query that returned little; prefer **2+ independent sources** for any contested point; capture source **dates** (recency matters and must be visible).

## 4. L3 Retrieve & parse · 取文与解析
Fetch full text (not just snippets) where possible; normalize to text + structure; record `retrieved_at`; cache by content hash. Reuse `../reading/` (parsers, OCR). No paywall circumvention (M4).

## 5. L4 Screen & dedup · 筛选与去重
Title/abstract screen → full-text screen with explicit **inclusion/exclusion** criteria (PRISMA-style when systematic). Collapse near-duplicates (same study via multiple outlets). Grade **credibility**: primary vs secondary; methodology; recency; conflicts of interest. Tools: Rayyan, Covidence, ASReview (for systematic reviews).

## 6. L5 Extract evidence · 证据抽取
One row per evidence item — this table *is* the brief's skeleton (M4):

| claim_id | claim · 主张 | quote or paraphrase · 原文/转述 | source_id | locator | stance | strength |
|---|---|---|---|---|---|---|
| c3 | X reduces cost ~20% | “…” (verbatim) | s12 | §4.2 p.9 | supports | strong (RCT, n=…) |

- Quotes **verbatim + located**; paraphrase labeled; keep the original language.
- `stance ∈ {supports, refutes, mixed, context}`; `strength` grounded in method, not vibes.
- **Absence of evidence is evidence**: record “not found” explicitly.

## 7. L6 Synthesize · 综合
Write the narrative from the evidence table only (M1). Structure: answer → key findings (ranked) → evidence & strength → **what disagrees and why** → what's still open. **Keep contradictions visible**; never average them into mush (M0.1). Separate **fact** (sourced) from **inference** (yours, labeled).

## 8. L7 Verify & citation-audit · 校验与引文审计
A **separate** pass (M3) checks, per claim: does the source actually say this? is the quote exact? is it current? is it primary? Default-FAIL: any claim without a resolving source is downgraded to `unverified` (M4). Re-open the source — do not trust the snippet.

## 9. L8 Iterate / gap-fill · 迭代补缺
Compute coverage per sub-question; for gaps, **generate new queries** and loop L2–L7. Stop when stop-criteria hit:

| stop criterion · 停止条件 | definition · 定义 |
|---|---|
| Coverage | every sub-question ≥ target coverage (e.g. ≥2 independent sources, or "answered") |
| Diminishing returns | new queries add no new claims/evidence across K rounds |
| Budget | time/token/cost box exhausted → deliver partial + explicit gaps |
| Saturation | same facts recur across new sources (theoretical saturation) |

## 10. L9 Report & self-eval · 成稿与自评
Deliverable = **brief + coverage & confidence + limitations + reference list** (IEEE). Then a **rubric self-eval** (separate evaluator, M3):

| criterion · 维度 | 0–3 | check · 核查 |
|---|---|---|
| Scope fidelity | | answers the actual question |
| Breadth | | ≥2 independent source types; no single-source contested claims |
| Citation integrity | | every claim resolves; quotes exact (spot-check ≥3) |
| Contradiction honesty | | disagreements shown, not smoothed |
| Provenance | | source + access date + ID present; `unverified` fenced |
| Coverage accounting | | states gaps & open sub-questions |
| Calibration | | confidence matches evidence |
| Actionability | | a reader can decide/act |

Any criterion ≤1 → **do not ship**; loop back (M3/M7). Publish only with review (no auto-push).

---

## Reference: brief skeleton · 报告骨架
```markdown
# <Topic> — research brief (<date>)
## Bottom line            # answer first, ≤5 bullets, each cited
## Key findings           # ranked, with strength + citation
## Evidence & analysis    # per finding: source, method, numbers
## Disagreements & limits # what's contested, weak, or missing
## Open questions         # sub-questions left unanswered
## Coverage & confidence  # coverage % by sub-question; overall confidence + why
## Sources                # IEEE list, with retrieved_at
```

> Method alignment: the orchestration pattern (orchestrator + parallel workers + separate synthesizer/verifier) and the emphasis on token-budgeted breadth follow Anthropic's published multi-agent research system design. Tooling here is substitutable and mostly open/local.
