# Four domain harnesses on three criteria · 四个领域 harness 的三判据横向评分

> P14.4, closed. What four published harnesses actually do about schema, identity, evidence and coverage — read in full, scored on criteria fixed before reading.
> P14.4 收尾：四份已发表的 harness 在「模式 · 身份 · 证据 · 覆盖」上到底怎么做的——全文读，判据先于阅读写定。
**Updated:** 2026-10-20

> **中文速览**
> **做法**：四条判据（C1 模式先于抽取 · C2 实体身份 · C3a 证据有界 · C3b 覆盖报告）在**读正文之前**写成可判定问句，四篇全文读完再打分，每格给节/表定位，N/A 与 0 分开记。
> **结果**：C1、C2 只在「建库」体裁上可判（另两例 N/A）；**C3a 在四例上全是 1，作为「有/无」不判别**——改写成**三级阶梯**（提示里要求引用 → 指针解析到原文 → 有机制核验）后才判别，而阶梯正好把四例分开：GraphRAG 一级、PaperQA2 二级、Case 1 二至三级、LongHarness 三级；**C3b 判别**，因为只有 GraphRAG 不报覆盖。
> **结论**：**加 2 条子句、0 个能力、0 个域**。① M3.15「把损失分阶段归因」——单个端到端分数说不清该修检索还是修推理，LongHarness 的 r1·r2·r3 漏斗是范例，PaperQA2 的 precision/accuracy/拒答率是两步版。② M4.16「指针是对支持关系的断言」——悬空（不解析）、过期（解析到已废止证据）、不支撑（解析到但原文不支持）是三种不同缺陷，原库只说了「要带指针」，没说这三种怎么分别检。
> **同时**把 `evidence-bounded-generation` 的触发条件加上 `grounding: required`——此前它只在 `artifact: knowledge_base` 或 KM/DH 域触发，导致 PaperQA2 这类「文献综述型」任务明明最需要它却不触发。
> **预登记被推翻两处**（Case 1 的 C3b、GraphRAG 的 C3a 都预测 0，实测 1）——按规则改的是判据，不是案例。

---

## 0. What this round settles, and what it does not

P14 scored one domain harness (a gazetteer person-graph pipeline, `[R136]`) on three criteria and refused to
grade the comparables, because they had only been resolved at the metadata level. This round opens the PDFs.

| Source | What it is | How it was read |
|---|---|---|
| Case 1 — 关书朋等, *方志人物 KG + RAG* `[R136]` | published Chinese journal case study, 8 entity types, P/R/F1 table | **full PDF read in P14**; this round re-used those notes, no second read |
| GraphRAG `[R148]` (arXiv:2404.16130v2) | LLM-built entity graph + community summaries for global sensemaking | **full text read** 2026-10-20 (26 pp., text extracted) |
| LongHarness `[R128]` (arXiv:2610.13075v1) | model-agnostic harness with an EvidenceBank + conclusion state | **full text read** 2026-10-20 (19 pp.) |
| PaperQA2 `[R238]` (arXiv:2409.13740v2) | literature-search agent, cited answers, LitQA2 benchmark | **full text read** 2026-10-20 (25 pp.) |

**Not done, stated so it is not read into the verdict:** no repository or code inspection (a parameter that exists
only in code is scored as *not published*); Case 1 was not re-read this round (its row rests on P14's full read, and
the corpus of that read is `review/knowledge-and-dh-crosswalk-2026-10.md` §3); one rater, no inter-rater check.
The HTR pair (`[R153]`, `[R154]`) stayed out by design — preprocessing genre, no schema decision, no identity merge,
no evidence/coverage contract; the revisit trigger was "if all four score identically", which did not happen.

---

## 1. How each criterion was scored

The operational questions were frozen in `updates/2026-10-20-p17-criteria.md` before any body was opened. Restated:

- **C1 schema before extraction** — a concrete entity/relation table, ontology file, controlled vocabulary or schema
  URL, referenced *before* the extraction step. A type list that exists only as a prompt placeholder, or the set of
  types the model happened to produce, does not count.
- **C2 entity identity** — one canonical id per entity, aliases recorded against it, and at least one statement about
  what happens on collision. "We merge same-name entities" is not a mechanism.
- **C3a evidence-bounded output** — every named assertion carries a pointer into the evidence, and "the material does
  not support an answer" is an available outcome.
- **C3b coverage** — a denominator that includes abstentions/failures, reported next to whatever precision-like number
  is offered.

**Scoring:** `1` = done and described verifiably · `0` = opposite practice adopted, or described but missing a
necessary element · `N/A` = not reported, which is **not** the same as "not done". Every cell carries a section or
table pointer.

One change was forced by the data and is declared up front: **C3a scored `1` in all four cases**, so as a bit it fails
the C4 meta-criterion. It is therefore reported as a **ladder** (§5), and the bit appears only for continuity.

---

## 2. Case 1 — gazetteer person graph `[R136]`

- **C1 = 1.** Eight entity types, their directions and the four-stage prompting are fixed in the method before
  extraction (表1). The schema is an input, not a summary of the output.
- **C2 = 1.** Same-name persons are *not* merged, authorities are reused, and the decisions are recorded — the
  behaviour M4.12 asks for.
- **C3a = 1 (ladder: 2).** Answers quote the original text as pointers. Whether a mechanism rejects an unresolvable
  pointer is not described.
- **C3b = 1.** Precision **and** recall are reported (表2), so the denominator is visible rather than implied.

This case is why the criteria exist, and it is the only one of the four that satisfies all of them at the bit level.

---

## 3. GraphRAG — the schema that is used but not published `[R148]`

- **C1 = 0.** §3.1.2 has the LLM extract "important entities and relationships" per chunk; the extraction prompt
  (Appendix E.1) constrains `entity type` to "One of the following types: [`{entity types}`]", and §4.1.2 says the prompts
  were built "with entity types and few-shot examples tailored to the domain of the data". So a closed type list
  **exists and is an input** — and the paper never prints it, and relations have no type schema at all. The mechanism is
  schema-constrained; the schema is not a contract anyone can check. That is a `0` under "described but missing a
  necessary element", not an `N/A`.
- **C2 = 0.** §3.1.2 is unusually explicit: "our analysis uses **exact string matching** for entity matching — the task of
  reconciling different extracted names for the same entity", with softer matching deferred to future work, and a
  claim that GraphRAG is "generally resilient to duplicate entities since duplicates are typically clustered together
  for summarization". That is a declared *non*-solution: no alias record, no collision handling, and no measurement of
  how often the exact-match assumption fails.
- **C3a = 1 (ladder: 1).** The answer prompts do ask for per-point references ("Points supported by data should list the
  relevant reports as references", Appendix E.4) and for abstention ("If you don't know the answer, just say so").
  Two limits: the pointer targets a **community report** — a generated summary one hop away from the source text — and
  nothing verifies compliance; it is an instruction to the model, not a gate.
- **C3b = N/A.** Evaluation is LLM-judged pairwise win rates on comprehensiveness / diversity / empowerment /
  directness over C0–C3 vs TS/SS (§3.3 criteria, §5.1 results). There is no abstention class to include in a
  denominator, and no accuracy metric at all. Notably: abstention is *instructed* in the prompt but never
  *counted* — the exact gap the instruction-vs-gate distinction names.

GraphRAG's contribution to this round is therefore a **counter-example with a mechanism**: every one of the three
pointer failures below is possible in it, and the paper's own wording shows the authors knew about the identity one.

---

## 4. LongHarness — evidence with a lifecycle `[R128]`

- **C1 = N/A.** No entity/relation extraction; statements are free text. The nearest analogue *is* declared before the
  loop: the state tuple `S_t = (E_t, C_t, H_t)` and the EvidenceBank record (id, statement, source references,
  lifecycle status) in §2.1/Fig. 2. So the design stance is schema-first about **records**, while the criterion —
  written for ontologies — cannot see it. Recorded as a scope finding, not a score.
- **C2 = N/A** for entities. The analogue is stronger than the criterion expects: **evidence identity** is explicit.
  §2.3: a statement enters as a candidate, becomes *active* on admission, and is revised or retired later; a correction
  is admitted as a new active entry while the previous one is marked *superseded*, and a retraction leaves the active
  set with no replacement. That is `M4.12`'s discipline applied to *evidence records* rather than people.
- **C3a = 1 (ladder: 3).** §2.3: each candidate must cite source references registered by prior `read` actions, the
  **controller checks reference validity**, and final acceptance requires "references resolving to active evidence and
  source passages" (§2.4). This is the only case where the pointer is *enforced by the harness* rather than requested in
  a prompt — and the enforcement is against the **active** set, so a pointer to superseded evidence fails.
- **C3b = 1, with the strongest shape in the pool.** §3.4 decomposes failure into a three-stage funnel,
  `r1 = P(evidence required is present)`, `r2 = P(retained and reconciled | r1)`, `r3 = P(exactly correct | r1, r2)`,
  with retrieval coverage computed over **all** questions and failures scored incorrect. On V2: **r1 87.8%, r2 87.3%,
  r3 79.7%**. Fig. 4 is the worked case: a baseline omits a recognised correction; LongHarness revises `e2`/`e4`, retires
  the old ids, and returns the reference answer instead of the stale one.

**Caveat on the funnel, read from the protocol:** the stage audit runs on *incorrect* episodes only, and "exact-correct
episodes are counted as passing the first two stages by protocol". So `r1`/`r2` are inflated by construction for the
episodes that were already right; the funnel locates loss among failures, it is not an unbiased estimate of pipeline
recall. The paper says this; a reader skimming Table 3 would not.

---

## 5. PaperQA2 — the citation audit `[R238]`

- **C1 = N/A.** No structured extraction; retrieval, contextual summarisation and synthesis.
- **C2 = N/A** for entities; **source identity** is the object that matters: citation keys resolve to one paper, and
  LitQA2's recall metric is "attributed its answer to the correct source DOI". Same pattern as LongHarness — the
  identity discipline exists, on a different object than the criterion names.
- **C3a = 1 (ladder: 2, with a level-3 audit).** The answer prompt requires "for each part of your answer, indicate which
  sources most support it via citation keys at the end of sentences, like (Example2012Example pages 3-4). Only cite from
  the context and only use the valid keys", and offers "I cannot answer" when the context is insufficient. Pointer
  granularity is page-level, i.e. into the source, not into a summary. Enforcement is prompt-level — but the paper then
  *audits* support: citing precision is "the ratio of cited and supported statements over all cited statements", measured
  at **86.1% for WikiCrow vs 71.2% for human-written Wikipedia** (p = 0.0013). The error taxonomy is the useful part:
  "cited and unsupported" bundles true hallucinations with statements that are accurate but **inappropriately cited**.
- **C3b = 1.** LitQA2 (248 questions) is scored three ways with the denominator stated: **precision 85.2 ± 1.1**
  (correct / answered), **accuracy 66.0 ± 1.2** (correct / all), **refusal rate 21.9 ± 0.9** ("insufficient information").
  The arithmetic closes: 85.2% × (1 − 0.219) ≈ 66.5%. The benchmark also *contains* deliberately unanswerable questions
  (the paper says so without giving the count), so refusal is a scored outcome rather than a failure. This is M3.14 in
  the wild, from a team that benefits from the higher number and still reports the lower one.

PaperQA2 is also why `evidence-bounded-generation`'s trigger was too narrow: it is a research-domain, document-artifact
system, and the existing `when` (`artifact: knowledge_base` OR KM/DH domain) would never fire for it.

---

## 6. Cross table

| Case | C1 schema | C2 identity | C3a pointer (ladder) | C3b coverage |
|---|---|---|---|---|
| Case 1 `[R136]` | **1** (8 types, 表1) | **1** (no same-name merge, authorities) | **1** (L2: quotes to original text; enforcement not described) | **1** (P **and** R, 表2) |
| GraphRAG `[R148]` | **0** (type list is a placeholder; relations unschema'd; §3.1.2, App. E.1, §4.1.2) | **0** (exact string matching, duplicates tolerated; §3.1.2) | **1** (L1: prompt asks for per-point refs to community reports; nothing checks; App. E.4) | **N/A** (pairwise LLM-judged win rates; §3.3, §5.1) |
| LongHarness `[R128]` | N/A (record schema only; §2.1/Fig. 2) | N/A (evidence identity: active / superseded / retracted, §2.3) | **1** (L3: controller validates refs against active evidence at submission; §2.3–2.4) | **1** (r1 87.8% / r2 87.3% / r3 79.7% on V2; §3.4, Table 3) |
| PaperQA2 `[R238]` | N/A (no extraction) | N/A (source identity: citation key → DOI) | **1** (L2 + audited: page-level keys, prompt-enforced; cited-and-supported 86.1% vs 71.2%) | **1** (precision 85.2 / accuracy 66.0 / refusal 21.9; §2) |

---

## 7. Which criteria survived, which were rewritten (C4)

The meta-criterion was: a criterion with the same value in every case does not discriminate → retire or reword it,
and say whether the criterion or the pool was at fault.

| Criterion | Values | Verdict |
|---|---|---|
| **C1 schema before extraction** | 1, 0, N/A, N/A | **Keep.** It discriminates within its genre (build a store vs. answer over one) and now carries a useful sub-distinction: *has* a schema vs. *publishes* one. GraphRAG is the "used but unpublished" case. |
| **C2 identity** | 1, 0, N/A, N/A | **Reword.** As written it only fires for KG builders, and it hides that the other two cases both *do* practise identity — on **sources** (PaperQA2: DOI keys) and on **evidence records** (LongHarness: active/superseded/retracted). The general question is "what is this pipeline's unit of reference, and does it have one canonical id with a recorded alias/collision rule?" — entity is only one answer. |
| **C3a evidence-bounded output** | 1, 1, 1, 1 | **Retire as a bit, keep as a ladder.** The pool is not homogeneous — the four differ sharply in *how* the pointer is secured: prompt instruction (GraphRAG), prompt + explicit key discipline at page level (PaperQA2), quotes to original text (Case 1), controller-enforced resolution to active source spans (LongHarness). A bit that reads 1 for a prompt sentence and 1 for a blocking check is measuring the wrong thing. |
| **C3b coverage** | 1, N/A, 1, 1 | **Keep, and enrich.** It separates "reports a denominator including refusals" from "reports only win rates". Within the `1`s there are two shapes worth naming: precision/accuracy/refusal-rate (PaperQA2, two stages) and a conditional stage funnel (LongHarness, three stages, locates where the loss is). |

**The ladder that replaces the C3a bit** (each rung is what the case actually provides, not what it claims):

1. **Requested** — the prompt asks for a pointer, nothing verifies it. GraphRAG.
2. **Resolvable** — pointers are structured, per assertion, at source granularity (page/quotation), with an abstain
   path. PaperQA2, Case 1.
3. **Enforced** — the harness rejects an output whose pointer does not resolve, and resolves against the *currently
   active* evidence, not merely existing evidence. LongHarness.

Rung 3 is not rung 2 plus effort; it is a different mechanism (a gate versus an instruction), and GraphRAG shows the
failure mode of stopping at rung 1 while still reading as "the system cites sources".

---

## 8. What this adds — two clauses, no capabilities

| Addition | The failure it names that nothing named before |
|---|---|
| **M3.15 — attribute the loss, stage by stage** (`core/04`) | A single end-to-end accuracy figure cannot tell a builder whether to fix retrieval, retention or reasoning; a conditional funnel (found → kept → used) locates the loss, and a two-way precision/accuracy/refusal split is the minimum acceptable version. |
| **M4.16 — a pointer is a claim about support** (`core/05`) | The library said "every assertion carries a pointer" (M4.13) and "verify citations mechanically" (M4.9). It did not say that a pointer has **three distinct failure modes** — dangling (does not resolve), stale (resolves to superseded/retracted evidence), unsupported (resolves, but the cited passage does not support the sentence) — nor that resolving is not supporting. |

Both are clauses, not capabilities, and the reason is the M0.5 test rather than taste:

- `verification-gate` is **always-on** and already carries "verify with observed evidence"; a capability for
  stage-decomposed coverage would fire in a strict superset of nothing — it would co-fire with an invariant and add
  annotation, not a decision.
- `evidence-bounded-generation` already fires on the output-side evidence requirement. Its content was missing the
  three failure modes, not its trigger — except for one real gap, which *is* fixed: its `when` was
  `artifact: knowledge_base` OR `domain ∈ {knowledge-management, digital-humanities}`, so a **research-domain,
  document-artifact** system answering over a corpus (PaperQA2's shape, and this repository's own research tasks)
  never fired it. `grounding: required` is now part of the trigger; `preferred` deliberately is not, because a
  preference is not a contract.

Deliberate non-additions, with reasons (M0.5): **no new domain** (none of the four is a faculty); **no
`evidence-lifecycle` capability** — it is the M4.16 / M4.12 content applied to records, and its natural trigger
(corpus answering) is `evidence-bounded-generation`'s; **no `graph-rag` or `agentic-search` capability** — retrieval
architecture is `tool-use` + `context-budget-policy` territory, and naming a product as a capability would make the
catalogue a vendor list. **Revisit trigger for the lifecycle piece**: if a fifth case retracts evidence in a pipeline
that does *not* answer questions (e.g. a dataset build), the record-identity rule is doing independent work and earns
its own clause.

---

## 9. Predictions that were falsified

Pre-registered from abstracts only, with the rule "if the prediction is falsified, the criteria change, not the cases".

| Prediction | Outcome |
|---|---|
| Case 1 C3b = 0? ("P/R/F1 reported, no abstention denominator") | **Falsified → 1.** Recall *is* reported beside precision; no abstention class is needed for a closed extraction task. |
| GraphRAG C3a = 0 ("citations not at claim level") | **Falsified → 1.** The answer prompt requires per-point references and an explicit don't-know. It is rung 1, not rung 0 — which is the more interesting finding. |
| GraphRAG C2 = 0? | **Confirmed**, and stronger than expected: the paper names exact string matching as its policy and calls duplicates tolerable. |
| LongHarness C3b = 0? ("no coverage") | **Falsified → 1.** It has the best coverage accounting in the pool. |
| PaperQA2 C3b = 0 or N/A | **Falsified → 1.** Precision, accuracy and refusal rate are reported together. |
| "C3b is the most discriminating point" | **Half right.** C3b separates GraphRAG from the rest, but C3a *as a ladder* separates all four — the bit was the problem, not the pool. |

Five of six predictions were wrong in the same direction: **the cases are better than the abstracts suggested, and the
binary criteria were flattering no one.** That is the argument for reading bodies instead of abstracts, made by this
round's own error rate.

---

## 10. Open items

- **Case 1 re-read** — its C3a rung (2 or 3) is the one cell resting on P14 notes rather than a fresh read; a
  re-read would settle whether the pipeline rejects an unresolvable pointer or merely renders one.
- **Code-level parameters** — GraphRAG's actual entity-type lists and PaperQA2's citation-key validation live in
  repositories, not papers. Scoring them would change "not published" rows, not the clause content.
- **A fifth, non-QA case** (dataset or archive build) — the recorded trigger for testing whether record identity
  deserves its own clause.
