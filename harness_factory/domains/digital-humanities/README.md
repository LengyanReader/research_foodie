# Domain · Digital Humanities · 数字人文域
> Wiring `core/` modules into machine-readable cultural heritage: encode, canonicalise, publish with provenance.
> 把 `core/` 模块接线成「可机器读取的文化遗产」：转写 → 规范 → 按标准编码 → 带证据出版。
**Updated:** 2026-10-19

---

## 中文速览

数字人文域回答：**怎么把一批史料/文物变成可检索、可引用、可被他人复用的结构化知识。** 它与 `humanities`（文本细读与诠释）的分工是：`humanities` 产出**判断**，本域产出**编码**。用 **M4** 保证每条断言带出处指针（M4.13）；用 **M4.11** 把「先定本体再做抽取」变成硬约束；用 **M4.12** 处理人与地的同名/异名（可权威则复用，不可判者交人）；用 **M4.8/M2.12** 让转写与标注可续接；用 **M3** 设「何时可发布」的门。产物是**带校勘记与模式版本**的数据集，而不是一次性演示。一手来源：TEI P5 `[R147]`、EAD3 `[R146]`、IIIF `[R143]`、DCMI Terms `[R144]`、CIDOC-CRM `[R142]`、Getty TGN `[R145]`。

---

## What this domain is for · 用途

Turn a body of historical or cultural-heritage material into a **machine-readable, citable, reusable** artifact: a transcription, an annotated corpus, a prosopography, a place gazetteer, or a knowledge graph — published to a standard, with the schema version and the evidence for each assertion recorded.

It is deliberately *not* the `humanities` domain. `humanities` is interpretive close reading whose artifact is a **document**; `digital-humanities` is computational encoding whose artifact is a **dataset**. A close reading of 雍正《畿辅通志》 is `humanities`; building a person-relation graph out of it with a declared ontology is this domain. (Case study: `../review/knowledge-and-dh-crosswalk-2026-10.md`.)

## Module combination · 模块组合

- **M4.11 (ontology as a contract).** Declare entity types, relation directions, allowed values and the identity rule *before* transcribing/extracting. A candidate that cannot be typed is a defect to record — not quietly kept.
- **M4.12 (one canonical id per entity).** Aliases recorded against the canonical id; undecidable merges escalate to a human gate (M8.3). Same-name persons and transliterated place names are the normal case, not the exception.
- **M4.13 (evidence-bounded output).** Every named assertion in a generated answer or a published record carries a pointer into the transcription/facsimile. "The witness is silent here" is a complete answer.
- **The transcription is an instrument (M3.10).** HTR output travels with the model id/version used and a stated or measured character-error rate; a transcription with no model record is an unidentified instrument (`../reference/evidence-instruments.md`).
- **M4.8 / M2.12 (resumable, append-only).** A transcription or annotation run is long: checkpoints per increment, append-only corrections, a declared backend and resume protocol (`../core/03-long-running-agents.md`).
- **M3.14 (a gate trades precision, not coverage).** A constraint/verification pass over extracted triples raises precision; it cannot raise recall. Report both, or the coverage claim is unsupported.
- **M1 (context).** Retrieval returns the entry, not the whole corpus; the store is indexed by `entry_id`.
- **M7 (governance).** The ontology has a version; a schema change is a migration, not a silent redefinition.

## Workflow · 流程

1. **Frame the corpus question & the edition.** What is being encoded, from which witness, to whose benefit; which licence/rights attach.
2. **Secure the witness.** Facsimile (IIIF), transcription where one exists, rights recorded.
3. **Transcribe & annotate to a declared scheme.** HTR (`transkribus`, `escriptorium`) with the model recorded and an error rate stated; annotation guidelines named.
4. **Resolve entities.** Persons, places, dates → canonical ids via an authority (Getty TGN, Pleiades, GeoNames); aliases kept, undecidable merges escalated.
5. **Encode to a standard.** TEI P5 for text/apparatus, EAD3 for finding aids, CIDOC-CRM for heritage events, IIIF for images, DCMI Terms for the record; the ontology version is part of the artifact.
6. **Publish with the apparatus & the schema version.** Every assertion traceable; the schema version named; the code that derived it recorded.

## Patterns · 模式

1. **Declared ontology before extraction.** The stage prompts/schemas pin entity types and relation directions first; the extraction is measured against them (M4.11).
2. **Alias-not-merge.** Same-name records stay separate until evidence (or a human) links them; the link is a logged decision (M4.12).
3. **原文 as a first-class entity.** The source passage itself is a node the assertions point at, so provenance is structural rather than prose (M4.13; the case study makes 原文 an entity type).
4. **Authority-first identifiers.** Reuse an existing authority id rather than minting a local one; local ids are a last resort, recorded as such.
5. **Two-number reporting.** Any verification pass reports precision **and** recall against a labelled sample (M3.14).
6. **Versioned schema + migration.** Deprecate by redirect, never delete; the schema version travels with every record (M7, M4.11).

## Anti-patterns

- **Schema-after-the-fact.** Extracting first and describing the types from the output; the "ontology" becomes a description of the extraction errors.
- **Merge by label.** Collapsing two people with one name, or splitting one place across transliterations, so the graph invents and divides entities.
- **The confident paraphrase.** A published summary that is fluent and nowhere in the witness (M4.13).
- **Precision sold as coverage.** Reporting a verification stage's precision jump while recall is flat, and calling the result complete (M3.14).
- **Unversioned schema.** A graph whose meaning changed silently between runs.

## See also

`../core/05-provenance-and-integrity.md` (M4.11–M4.13) · `../core/04-verification-and-gates.md` (M3.14) · `../core/03-long-running-agents.md` (M2.12) · `../reference/evidence-instruments.md` (HTR / gazetteer / ontology rows) · `../reference/outlet-map.md` (standards & authorities) · `../review/knowledge-and-dh-crosswalk-2026-10.md` (the round that added this domain) · `README.md` (`humanities` — the interpretive sibling).
