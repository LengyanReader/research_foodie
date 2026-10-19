# Knowledge-graph, ontology & knowledge-feature patterns · 知识图谱·本体·知识特征模式

> A classic / frontier / management-and-evolution survey, with the gates a harness must enforce.
> 经典·前沿·管理与演化：给 harness 的落地清单。
**Updated:** 2026-10-20

## 0. Scope and relation to the earlier round

This is the **canon survey** that the previous round lacked. That round (2026-10-19) read one real domain harness in full
and derived four clauses from it — `ontology-as-contract` (M4.11), `entity-resolution` (M4.12),
`evidence-bounded-generation` (M4.13) and `schema-evolution` (via M7). The **standards** behind them live in
`review/references.md` §M (R137–R154); this doc adds the field's *own* canon in §N (R155–R170) — the survey, the
engineering method, the representation family, and the reasoners that can refute a graph claim.

**Method.** Normative W3C texts, standards-body records and tool pages were fetched on 2026-10-20 (HTTP 200, Firefox UA);
arXiv rows come from one `id_list` batch. Classic **books and book chapters** (METHONTOLOGY, NeOn, OntoClean) were **not
re-read** and are named, not cited as evidence.

---

## 1. The stack, as layers

A knowledge graph is not one artifact. Confusing the layers is the most common design error, and each layer has its own
failure mode and its own gate.

| Layer | What it fixes | Normative anchor | Failure if skipped |
|---|---|---|---|
| **Data model** | nodes, edges, literals, named graphs | RDF 1.1 (R137), JSON-LD 1.1 (R157) | Every extractor invents its own record shape. |
| **Schema / ontology** | classes, properties, axioms, cardinalities | RDFS + OWL 2 (R138); profiles EL/QL/RL (R159) | "Entity" means whatever the last script meant. |
| **Vocabulary / alignment** | controlled terms, mappings to external schemes | SKOS (R139), LOV (R169), OLS4 (R170) | The same concept appears under five labels and never joins. |
| **Constraints** | what a valid instance looks like | SHACL (R140) | Invalid data is indistinguishable from valid. |
| **Query / access** | how questions become answers | SPARQL 1.1 (R156); OBDA via Ontop (R168) | Answers depend on who wrote the script, not on the graph. |
| **Provenance** | which source, which extraction, which version | PROV-O (R141); named graphs; RDF-star **draft** (R158) | A wrong statement cannot be traced, so it cannot be removed. |
| **Reasoning** | what follows from what is stated | HermiT (R166), ELK (R167) | "Derived" and "extracted" are conflated. |

**The one-line rule.** *Declare the layer you are operating on.* Most "the graph is wrong" bugs are a layer confusion: a
schema problem fixed with a data patch, or a provenance problem fixed by re-extraction.

---

## 2. Classic: ontology engineering as a method, not an artifact

An ontology is a **contract**, so the interesting question is not "which editor" but "which method produced it".

| Method | What it contributes | Status |
|---|---|---|
| **Ontology Development 101** (R160) | The **competency-question** method: write the questions the ontology must answer *before* modelling; iterate. | fetched (PDF 200) |
| **METHONTOLOGY** | Lifecycle: specification → conceptualisation → formalisation → implementation → maintenance. | **not re-read** (book chapter) |
| **NeOn** | Scenario-based, reuse-first engineering across networked ontologies; explicit **glossary of activities**. | **not re-read** (book) |
| **OntoClean** | Meta-properties (rigidity, identity, unity) to catch taxonomies that *look* right and are not. | **not re-read** (paper) |
| **Ontology Design Patterns (ODP)** | Reusable modelling fragments (n-ary relation, part-whole, time-indexed situation). | community catalogue, **not fetched** |
| **Modularisation** | Split by *competency*, not by convenience; each module has its own import boundary. | practice, no single canonical source |

**Why this matters for a harness.** "We used OWL" says nothing. The checkable claim is: **were the competency questions
written first, and does the schema answer them?** That is the operational meaning of M4.11 (ontology-as-contract), and it is
a gate, not a style preference.

---

## 3. Knowledge features: representations, completion, reasoning

"Knowledge features" is where the field's vocabulary is muddiest. Four different things get called the same word:

| Family | Examples | What it is good for | What it is **not** |
|---|---|---|---|
| **Embeddings** | TransE (2013, not on arXiv) → RotatE (R161), ComplEx (R162), ConvE (R163) | Link prediction, similarity, candidate generation | **Not evidence.** A high score is a model's guess; it cannot ground a claim. |
| **Graph neural nets** | R-GCN (R164), CompGCN (R165) | Node/relation classification with structure | Not a substitute for a schema; they learn what the data already encodes. |
| **Symbolic reasoners** | HermiT (R166) for OWL 2 DL; ELK (R167) for OWL 2 EL | **Deciding** entailment; finding inconsistency | Only as good as the axioms; they will happily derive nonsense from a wrong axiom. |
| **OBDA / virtual graphs** | Ontop (R168) | Query relational data *as* a graph without materialising it | The mapping is the contract — an unmapped column does not exist. |

**The harness distinction.** Embeddings *rank*; reasoners *decide*. A pipeline that uses a reasoner's output as a candidate
and then a reasoner/SHACL check as a gate is sound. A pipeline that reports an embedding score as a fact is the exact
failure M3.10 names (instrument ≠ claim), and M4.13 (evidence-bounded output).

---

## 4. Frontier: construction, retrieval, and the LLM turn

| Line of work | Source | What changed | What did **not** change |
|---|---|---|---|
| **Generative KG construction** | R149 (`arXiv:2210.12714`) | Extraction became a generation task over schema + text, with LLMs as the extractor. | You still need a **declared schema** and an **identity rule** — otherwise the output is a pile of plausible triples. |
| **GraphRAG** | R148 (`arXiv:2404.16130`) | Retrieval moved from chunks to a *community summary* graph for query-focused summarisation. | Provenance still has to point back to the source text; a summary is not a citation. |
| **KGQA (multi-hop)** | — | Multi-hop questions are answered by traversal + LLM synthesis. | The answer must be **evidence-bounded**: "the graph does not say" is a valid output. |
| **KG + LLM fusion** | — | The graph as a *tool*/memory for an agent, not only as a query target. | Retrieval provenance (which subgraph, which version) must travel with the answer. |
| **Agentic / self-evolving KG** | R151 (`arXiv:2310.04835`) | The graph is maintained by agents that add, merge and retire statements. | Then **schema evolution** and **identity** become routine operations, not one-off migrations (M7). |

**The honest summary.** The 2022–2026 turn changed *who extracts* and *how retrieval is shaped*. It did not repeal the two
hard constraints: **identity** (one entity, one canonical id) and **evidence** (every statement points at a source span).

---

## 5. Management, evolution and quality

This is the part practitioners under-invest in and the part a harness can enforce most cheaply.

| Concern | Source | Practice |
|---|---|---|
| **Evolution** | R151 | Treat schema change as a **versioned migration** with a compatibility statement; never an in-place rename. |
| **Quality assessment** | R152 (`arXiv:2208.07779`) | Score dimensions separately (completeness, accuracy, consistency, timeliness); a single "quality" number hides the trade-off. |
| **Entity resolution** | R150 (`arXiv:1905.06397`) | Blocking → pairwise matching → clustering → **human adjudication** for the ambiguous band. Aliases are kept, not overwritten. |
| **Curation workflow** | — | Every statement has a state (proposed / accepted / disputed / retired) and an owner. |
| **Statement-level provenance** | R141, R158 (draft), Wikidata model | Prefer reified/named-graph statements over "the graph says so"; a triple without a source cannot be challenged. |
| **Retirement** | — | Deprecate, do not delete: a removed statement is usually a *disagreement* that should stay visible. |

**The quality trap.** Quality metrics are proxies and get gamed (see `review/self-model-and-gap-seeking-2026-10.md` §3).
"99% of statements have a source" is compatible with a graph that is *wrong in the same way everywhere*. Pair every
completeness metric with an **accuracy check against held-out sources**.

---

## 6. Canonical systems (first-party, one line each)

| System | What it is | Why it is on this list |
|---|---|---|
| **Wikidata** | Crowd-edited item/property/statement graph | The reference implementation of **per-statement provenance** (qualifiers, references, ranks). |
| **DBpedia** | Structured extraction from Wikipedia | The canonical *extraction-at-scale* pipeline and its error profile. |
| **YAGO** | Entity/relation KB with temporal and spatial facts | Shows how far rule-based cleaning + a taxonomy can go. |
| **ConceptNet** | Commonsense assertions with weights | A model of **disagreement as data** (assertions carry sources and scores). |
| **UMLS** | Biomedical terminology integration | The canonical **vocabulary alignment** problem (many sources, one concept). |
| **SNOMED CT** | Clinical terminology with a description logic core | Ontology + reasoner in production, under regulation. |
| **Gene Ontology** | Controlled vocabulary + annotations across species | The model for **evidence codes** on every assertion. |
| **ChEBI** | Chemical entities ontology | Identity across naming systems. |
| **CIDOC-CRM** | Event-centric cultural-heritage ontology | The reference for **events over things** (R142). |
| **Europeana** | Aggregation of heritage records | Shows the aggregator-vs-holder provenance split. |
| **GeoNames / Pleiades** | Gazetteers (modern / ancient) | Stable place ids; the identity backbone for spatial joins. |
| **BabelNet** | Multilingual encyclopaedic graph | Multilingual identity via synsets; the cross-language case. |

---

## 7. What a harness must enforce

Mapping the five layers to the clauses that already exist — this is the point of the survey: the canon should change the
*gate list*, not just the reading list.

| Gate | Clause | The failure it prevents |
|---|---|---|
| **Declared schema before extraction** | M4.11 | "We will model it later" → every extractor invents its own shape. |
| **One identity per entity, aliases retained** | M4.12 | Two people averaged into one row; or one person split into five. |
| **Every assertion carries a pointer** | M4.13 | A fluent answer the sources do not support. |
| **Schema change is a versioned migration** | M7 | An in-place rename that silently breaks every downstream query. |
| **The instrument matches the claim** | M3.10 | An embedding score reported as a fact; a reasoner's entailment reported as an extraction. |
| **Retrieval provenance travels with the answer** | M4.13 | A GraphRAG summary with no path back to the text. |

---

## 8. Deliberate non-additions

- **No new clause for "knowledge features".** Embeddings/completion/reasoning are *instrument choices* (M3.10), already
  covered; adding a clause would restate M3.10 with new nouns.
- **No `encoding-standard` instrument kind.** TEI/CIDOC/Dublin Core/EAD3/IIIF are **norms**, not instruments; they live in
  §M and in `domains/digital-humanities/README.md`. (Recorded in the previous round as well.)
- **No mandated graph database.** Neo4j/RDFLib/Jena/Protégé are catalogued as instruments; the choice is a task decision.
- **No claim that the classic method books were re-read.** They were not (§0, §2).
- **No "KG quality score".** §5 explains why a single number is the wrong instrument.

---

## 中文

**分层，是本文的主线。** 知识图谱不是一个东西：数据模型（RDF/JSON-LD）→ 模式/本体（RDFS/OWL 2，含 EL/QL/RL 剖面）→ 词表与对齐（SKOS/LOV/OLS4）→
约束（SHACL）→ 查询（SPARQL；OBDA 用 Ontop）→ 溯源（PROV-O、命名图、RDF-star 草案）→ 推理（HermiT/ELK）。**最常见的 bug 是层级混淆**：
用补数据去修模式问题，或用重新抽取去修溯源问题。

**经典方法是"先写能力问题"。** Ontology Development 101 的能力问题法（R160）是唯一可操作、可检查的起点：先把本体要回答的问题写下来，再建模。
METHONTOLOGY/NeOn/OntoClean 是书/论文，本轮**未重读**，只作谱系列名，不作证据。

**"知识特征"要分清四件事。** 嵌入（RotatE/ComplEx/ConvE）**排序**；GNN（R-GCN/CompGCN）学结构；符号推理器（HermiT/ELK）**判定**蕴含；
OBDA（Ontop）把关系库当图查。**嵌入分数不是证据**——这是 M3.10 与 M4.13 的原话。

**前沿变了什么、没变什么。** 生成式图谱构建（R149）与 GraphRAG（R148）改变了"谁来抽取"与"检索的形状"；但**身份**（一实体一规范 ID）与
**证据**（每条断言指回原文片段）没有被取消。

**管理与演化是回报率最高的一段。** 演化=带版本的迁移（R151）；质量=分维度打分（R152，不要单一"质量分"）；实体消解=分块→配对→聚类→**歧义带交人裁决**（R150）；
每条断言有状态与责任人；**弃用而非删除**。质量指标是代理，会被告姆哈特定律玩弄（见 `self-model-and-gap-seeking` §3），每项完整性指标都要配一个留出源的准确性检查。

**给 harness 的六道门。** 先声明模式（M4.11）· 一实体一 ID 且留别名（M4.12）· 每条断言带指针（M4.13）· 模式变更是版本化迁移（M7）·
仪器匹配主张（M3.10）· 检索溯源随答案同行（M4.13）。

**有意不新增。** 不为"知识特征"新开子句（那是仪器选择，M3.10 已覆盖）；不设 `encoding-standard` 仪器类（TEI/CIDOC/DC/EAD3/IIIF 是**规范**不是仪器）；
不规定图数据库；不声称重读过经典方法论著作；不设单一"图谱质量分"。
