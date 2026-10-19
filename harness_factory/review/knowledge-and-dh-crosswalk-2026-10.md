# Knowledge engineering & digital humanities — crosswalk and round record (2026-10)
> What a published real-world domain harness actually does, how it maps onto this library's clauses, and what (if anything) the library was missing.
> 一个已发表的真实领域 harness 做了什么、如何对应本仓库的条款、以及本仓库此前缺了什么。
**Updated:** 2026-10-19

---

## 中文速览

本文件是 **P14 轮的交付物**：用户要求「把数字人文，以及涉及知识库/知识图谱/知识本体的开发维护管理演化 的 harness 能力做深入检索、调研、梳理并整合」。做法不是收编某一篇论文，而是**以一个已发表、可核验的领域 harness 为案例**（关书朋等《智能体驱动的方志人物知识图谱构建与检索增强生成问答研究》，`[R136]`，一手 PDF 全文已读），把它的 11 个机制逐条对照本仓库的 `core/` 条款与能力，给出「已覆盖 / 部分覆盖 / 缺口」判词；再按**三条固定判据**与可比对象对照。结论是：11 个机制里 9 个已被既有条款覆盖，**真正的缺口只有两条** —— ①「输出侧证据约束」（生成的答案里每个具名断言必须带证据指针，无据即声明不足）；②「门禁只买精确率、不买覆盖率」这条读法。落地为 **4 条条款（M3.14、M4.11–M4.13）+ 4 个能力 + 1 个域 + 13 件仪器 + §M 参考文献组**，并**明确记录不新增什么**（M0.5）。知识库的**演化**（模式版本迁移）单列为 `schema-evolution`。

---

## 1. Why this round · 为什么有这一轮

The ask was a *class*: how to develop, maintain, manage and evolve a knowledge base / graph / ontology, and what digital-humanities work needs on top. A single paper cannot ground a class claim, so `[R136]` is used as **Case 1** — an unusually complete published record (corpus scale, stage prompts, a P/R/F1 table, a three-mechanism QA comparison) — and the generalisations are grounded in the **normative standards** the field actually works to: RDF 1.1 `[R137]`, OWL 2 `[R138]`, SKOS `[R139]`, SHACL `[R140]`, PROV-O `[R141]`, CIDOC-CRM `[R142]`, IIIF `[R143]`, DCMI Terms `[R144]`, Getty TGN `[R145]`, EAD3 `[R146]`, TEI P5 `[R147]`, plus the KG-engineering literature `[R148]`–`[R152]` and the historical-transcription literature `[R153]`–`[R154]`.

The library's answer to "what does this class need" is not a new topic list: it is **four clauses**, each naming a failure mode that no existing clause named.

## 2. Case 1 · the gazetteer person-graph (`[R136]`)

**Source status.** Primary source verified in full — the publisher's open PDF (`wxysjxb.ajcass.com`), no paywall. Citation: 文献与数据学报 **8**(3): 56–72, Sep. 2026. The printed DOI (`10.31193/SSAP.J.ISSN.2096-6695.2026.03.05`) does **not** resolve; treat it as printed-only. Everything below comes from the article, not from a web rendering.

**What it builds.** From the "人物" section of 雍正《畿辅通志》 (≈49.47 万字, chunked at ~2,500 字 into 445 blocks), a four-stage agent pipeline produces a person-centric knowledge graph: 6,488 source entries → 64,050 candidate triples → constraint verification leaves 58,876 accepted / 591 corrected / 4,583 rejected → **39,440 canonical entity nodes / 59,465 relations**. Retrieval is hybrid (semantic + graph + keyword) over three stores (FAISS 1024-d `bge-m3` embeddings, SQLite for 原文, Neo4j for the graph), joined by `entry_id` / `entity_id`.

**Mechanism inventory → verdict.** (Verdicts are per *mechanism*, against this library's clauses as they stood before this round.)

| # | Mechanism (as the case does it) | Mapped clause / capability | Verdict |
|---|---|---|---|
| M-1 | Ontology fixed **before** extraction: 8 entity types (人物·时间·地点·事件·官职·著述·所属类别·**原文**) + declared relation directions | M4.11, `ontology-as-contract` | **gap → added** |
| M-2 | Staged pipeline with **typed intermediate artifacts** (`entry_id`, candidates with their 原文) | M2.x, M2.11 | covered |
| M-3 | A **constraint-verification** stage: entity type, relation direction, evidence support; explicitly bars 外部知识补全与过度推断 | M3.10, M4.5 | partially covered — the *stage* was covered; its **statistics reading** was not |
| M-4 | **Entity normalization** that must 不合并同名人物 and keep 古地名/复合官职 | — | **gap → added** (M4.12, `entity-resolution`) |
| M-5 | **原文 as a first-class entity type** — provenance is structural, not prose | M4.4 (claim ledger) | partially covered |
| M-6 | Hybrid retrieval with declared weights (α=0.25 semantic, β=0.08 graph, γ=0.10 keyword) | M1.x, retrieval instruments | covered |
| M-7 | **Output-side** bounding: answers carry the evidence; a gap in the material is a valid answer | M4.5 (input side only) | **gap → added** (M4.13, `evidence-bounded-generation`) |
| M-8 | Evaluation on a **226-item labelled sample** with P/R/F1 | M3.9, `eval-driven-development` | covered |
| M-9 | Three QA mechanisms compared head-to-head (KG query vs RAG vs agent) | M3.9 | covered |
| M-10 | **Declared multi-store backend** (SQLite + FAISS + Neo4j) with a join key | M2.12 (added in P12.3 this same day) | covered |
| M-11 | Reuse of **reference ontologies/authorities** (FOAF, CBDB; CHGIS/TGAZ for toponyms) | M4.11 (reuse an authority) | covered |

**The one number worth reading twice.** 表2 reports, for 关系抽取: precision **88.79% → 97.67%** after the constraint stage, while recall moves **83.05% → 83.42%**. That is nearly a *ten-point precision gain with a flat recall* — the signature of a filter. The paper says as much in prose ("尤其是关系抽取从 88.79% 提升至 97.67%") and does not claim coverage improved. The generalised rule is now **M3.14**: a gate removes candidates; it cannot add them, so report recall beside precision or the completeness claim is unsupported. (Entity recognition for comparison: P 92.55% → 98.05%, R 88.25% → 88.03%.)

## 3. Three fixed criteria, and the comparables · 三条判据与可比对象

Every read of a domain harness is scored on the same three questions:

1. **Is the schema declared before extraction** (and versioned), or inferred from the output? (M4.11)
2. **Is entity identity handled** — aliases recorded, merges evidenced or escalated, authorities reused? (M4.12)
3. **Is the output evidence-bounded, and is coverage reported** alongside precision? (M4.13 + M3.14)

| Comparable | Read this round | (1) schema first | (2) identity | (3) output bound + coverage |
|---|---|---|---|---|
| Case 1 — gazetteer person graph `[R136]` | **full PDF** | yes (8 types + directions fixed pre-extraction) | yes (no same-name merges; authorities reused) | yes on both (原文 pointers; P **and** R reported) |
| Microsoft GraphRAG — pipeline overview `[R148]`, project README | **README + landing page fetched** | no fixed ontology: LLM-derives entities/relationships from unstructured text (its own description: "extract meaningful, structured data from unstructured text using the power of LLMs") | not a stated concern of the pipeline overview | citations to source chunks; precision/recall of graph *coverage* not the reported headline |
| LongHarness `[R128]`, HTR pipelines `[R153]`/`[R154]` | **metadata only** (arXiv API) | — | — | — |

> **Honest limit, recorded as work rather than glossed.** Only Case 1 was read in full this round. The comparables at row 3 were resolved at the *metadata* level only, so no verdict is asserted for them; a harness-vs-harness survey means opening five PDFs and scoring them on the three criteria above. That is deferred as **P14.4** (`data/cycles.json`), not claimed here. GraphRAG's row rests on its own project README/overview, which is part of its released artifact.

## 4. What was added, and why each one discriminates · 新增了什么

| Addition | Kind | The failure it names that nothing named before |
|---|---|---|
| `M3.14` — a gate trades precision, not coverage | clause (`core/04`) | reporting a verification pass's precision as though the result set became *complete* |
| `M4.11` — ontology as a contract | clause (`core/05`) | extracting first and letting the "ontology" describe the extraction errors |
| `M4.12` — one canonical identity per entity | clause (`core/05`) | merging two people who share a name, or splitting one place across transliterations |
| `M4.13` — bound the answer by the evidence | clause (`core/05`) | the fluent answer that is nowhere in the material |
| `ontology-as-contract` | capability | as above, as a trigger the engine can fire on (`artifact: knowledge_base`, or the KM/DH domains) |
| `entity-resolution` | capability | as above |
| `evidence-bounded-generation` | capability | as above (output-side twin of `untrusted-content-discipline`) |
| `schema-evolution` | capability | a schema change that silently redefines archived assertions (M7 applied to *meaning*) |
| `domains/digital-humanities/` | domain (31st) | DH *encoding* work as distinct from `humanities` *interpretation*; artifact is a dataset, not a document |
| 13 `instruments`, 6 kinds | catalog | HTR, gazetteer, ontology-toolkit, graph-database, kg-construction, entity-resolution had no first-party tool entries |
| `§M` (R136–R154) | references | the normative KG/DH standards were cited nowhere in this repo |
| 7 outlets | `data/sources.json` | W3C, IIIF, CIDOC, LOC standards, Getty, TEI-C, Wikidata as *where to look* |

## 5. Deliberate non-additions (M0.5) · 有意不新增

- **A new capability for KG-*query* / hybrid retrieval.** Retrieval is already covered by `context-budget-policy` + `tool-use` and the retrieval instruments (M-6 above scored *covered*). A `graph-retrieval` capability would restate them.
- **A `knowledge-engineering` domain.** `domains/knowledge-management/` already owns coverage-mapping, canonicalisation and source ledgers; the *graph* specifics are now **clauses** (M4.11–M4.13), which is the right layer — a domain says *where you are*, a clause says *what must be true*.
- **A second domain for "prosopography".** It is a `digital-humanities` workflow (step 4: resolve entities), not a separate faculty.
- **An `encoding-standard` instrument kind for TEI/CIDOC/Dublin Core/EAD/IIIF.** Standards are norms, not instruments (`reference/evidence-instruments.md` §Deliberate non-entries); they live as references `[R142]`–`[R147]` and as domain gate text. Gazetteers *are* instrumented, because an authority table is queryable the way `uniprot` is.
- **CBDB and ISAD(G) as sources.** Both were probed and are **not reliably reachable** from this environment (403 on repeat); recording them would mean citing what was not read. SNAC/EAD3 cover the need for now.
- **The 17 roundup-only numbers from §L** are no longer `unverified`: 16 were **confirmed verbatim in the papers' own HTML full text** this round (12 numbers + 4 of 5 affiliations); one paper (`2610.20563`) has no reachable HTML full text, so its VLIW cycle figures stay **unverified**. Two readings were *corrected* in kind: the 4.1×–39× range is the **TQ-cost gain column** (not "composition cost"), and 41.1 → 53.3 is the **avg@5** metric.

## 6. Open items · 未决

- **P14.4** — score 3–5 published domain harnesses on the three fixed criteria (bodies not read this round).
- **P12.4** — the 22 `verified: false` outlets remain unconfirmed (blocked hosts).
- **`[R136]`'s DOI does not resolve.** The article is citable from the publisher landing page + page range; do not cite the DOI as live.
- **Two mechanisms came out `partially covered`** (M-3's statistics reading, M-5's structural provenance). M-3 is now M3.14; M-5 is addressed by M4.13 but a dedicated *"the source passage is a node"* clause was judged not to discriminate beyond M4.4 + M4.13 and was **not** added.

## See also

`core/04-verification-and-gates.md` (M3.14) · `core/05-provenance-and-integrity.md` (M4.11–M4.13) · `domains/digital-humanities/README.md` · `reference/evidence-instruments.md` · `reference/capability-router.md` · `sources/source-map.md` (M3.14/M4.11–M4.13 row) · `review/references.md` §M · `reference/outlet-map.md`.
