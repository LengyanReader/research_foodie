# Cross-language fidelity · 跨语言保真（意群对齐）

> **What this is.** `core/05` (**M4.10**) says: when a claim moves into another language, align by
> **meaning unit** and **corroborate** — never assume word-match means meaning-match. This is the concrete
> procedure: how to cut a text into meaning units, how to carry each unit, how to *prove* the carried
> claim still says the same thing, and how to handle terms and bilingual deliverables. Load it whenever
> work crosses languages — translating sources, writing a bilingual report, or corroborating a claim
> across an English and a Chinese source. · 本文把 **M4.10** 落地：如何按**意群（语义单元）**切分与搬运、
> 如何用**回译/复核互证**证明「意思没变」、如何处理术语与双语交付。凡跨语言翻译来源、写双语报告、
> 或在中英两份来源间互证主张时，都按本文执行。
> Same paths as every factory doc — these are **the harness-factory's** files, not your project's.

**Updated:** 2026-10-19 · Load via `harness skill cross-language`. Sources: `review/references.md` §K. Companions: `reference/methodology-map.md` (what procedure licenses the inference, M3.13) and `reference/evidence-instruments.md` (what observes it, M3.10).

---

## 中文速览

**译的不是词，是意群。** 逐字对译（word-for-word）在结构、情态、范围、语用上必然走样：`may/shall` 之分、否定辖域、量词范围、专名与标识符，逐字处理就会变形。本文给出的规程是：**(1) 按意群切分**（语义单元 = 最小的「整体搬运才不走样」的一段，通常不是词，也不总是句子）；**(2) 整段搬运**并显式记录合并/拆分；**(3) 互证**——回译、目标语读者复述、跨语言来源互校，而不是「词都对上就算对」；**(4) 术语处理**——不可译词**音译 + 加注**，绝不悄悄替换近义词，必要时建双语术语表；**(5) 双语交付**——一份意思、两种协调的表达，英文为主体、中文为**执行性意译**，可以压缩、不可失真，引用与标识符不翻译。**反模式**：逐字对译、假朋友（false friend）、悄悄换词、把译文当一手来源。规则本身是 **M4.10**（不变量层，不做成能力——特征向量没有语言轴，无法判别）。

---

## How to use · 用法

1. **Name the unit first.** Cut the source into meaning units (not words, not always sentences) and state where each boundary is. See §1.
2. **Carry each unit whole**, then re-split if the target needs it — recording any merge or split. See §2.
3. **Prove the carry.** Round-trip, a target-language reader, or a second-language source — pick at least one and run it. See §3.
4. **Handle terms explicitly**, with a gloss and a term table. See §4.
5. **For a bilingual deliverable**, produce two coordinated renderings of one meaning (master + executive rendering). See §5.

> Rule of thumb: **translation is a claim about meaning, so it is governed by M4, not by M2.** The question is never "do the words line up?" but "does the carried claim still say what the source said, in the source's own scope?"

---

## 1. The unit of meaning · 意群

A **meaning unit** (意群 / sense group / thought group; in translation studies the *translation unit*) is the smallest stretch of text that can only be carried **as a whole**. It is *not* the word and *not* always the sentence:

- a **negation scope** (`not all X are Y` ≠ `all X are not Y`),
- a **modality** (`may` vs `shall` vs `should`),
- a **quantifier** (`most` vs `many`),
- a **hedged claim** (`suggests` vs `shows`),
- a **fixed phrase or idiom** whose parts are meaningless alone,
- a **named entity / identifier** (a DOI, gene symbol, API name — these are carried verbatim, never translated).

**The test:** translate each candidate piece independently; if any piece changes what the sentence *claims*, the boundary is wrong — widen the unit until the claim is stable. Cohesion markers (reference, substitution, ellipsis, conjunction) bind units together and must be carried across too — the resources for text construction, not just sentences, are what makes a passage mean what it means (`[R122]`).

---

## 2. The alignment procedure · 对齐规程

1. **Segment by meaning**, not by comma or period. Mark the units (usually one per proposition / rhetorical move / table row).
2. **Render each unit whole** in the target; re-segment afterwards if the target's grammar prefers a different cut.
3. **Map units 1:1 where possible.** A unit may legitimately become two (or two merge into one), but every merge/split is **recorded** — silently fusing two claims into one is a provenance defect, not a style choice (M4.3).
4. **Preserve the unit's invariants:** modality, polarity (negation), quantification, tense/aspect, stance (assert / hedge / report), and named entities.
5. **Align structure too:** heading↔heading, list↔list, table↔table, code↔code. If word order must differ, keep the unit mapping explicit so a reader can follow it.

---

## 3. Mutual corroboration · 互证

This is the step word-for-word translation eliminates. Corroboration is **independent**, not a re-read of your own work:

1. **Round-trip (back-translation).** Render the target back into the source language *without looking at the original*, then diff **unit by unit**. Any difference that touches a claimed fact, scope, or modality is a defect to fix.
2. **Target-language reader.** A reader treats the target as a native document; ask *"what do you understand?"*, not *"is this a correct translation?"* The comprehension is the evidence.
3. **Cross-source corroboration.** When the same claim exists in two languages (an English abstract and a Chinese paper, a translated standard and its source), treat them as **two sources**, not master + copy: check they agree, and where they disagree go back to the original — do not let one language's rendering launder an error into the other.
4. **Corroborate ≠ repeat.** Repeating your own rendering, or running the same machine translator twice, is not corroboration. An *independent* rendering or reader is.

> Two-source rule: a fact asserted only in a translation is *one* source, not two. Cite the original; cite its translation only alongside it.

---

## 4. Term handling · 术语处理

- **Untranslatable / culture-bound term:** transliterate **and** gloss (成对给出原文 + 直译/释义) on first use, then reuse consistently. A gloss is not a substitute — it is an annotation.
- **Established target-language equivalent:** use it, but keep the source term in a small glossary so a later reader can recover it.
- **Never silently substitute** a near-synonym that narrows or widens the term (`shall` → `may` is a meaning change, not word choice).
- **Keep a bilingual term table** (source term → target term → note) for any document longer than a page — this is the M4 claim-ledger applied to vocabulary.
- **Identifiers stay verbatim:** DOIs, arXiv IDs, gene/protein symbols, API and code identifiers are never translated.

---

## 5. Bilingual deliverables · 双语交付

- **One meaning, two coordinated renderings** — not a master plus a word map. In this factory: the English *master body* is authoritative; the Chinese `> 中文速览` / `## 中文` section is an **executive rendering** (意译/要点化). It may compress; it may not change a claim or add one the master lacks.
- **Compress by omission, never by distortion.** A summary is allowed to be selective; it is not allowed to be wrong. If a nuance cannot survive compression, add a one-line note — do not drop it silently.
- **Carry the same citations and identifiers in both versions** — a citation is not translated.
- **Register may differ; the claim may not.** The Chinese may read more formally or more tersely; the proposition, scope and stance must match.

---

## 6. What this is NOT · 边界

- **Not a machine-translation metric.** BLEU / COMET-type scores measure surface overlap against a reference, not the preservation of a claim's meaning; a high score is *not* a gate. They may rank candidates; they may not certify fidelity.
- **Not "translation memory as authority".** A memory/tool match is a *candidate* rendering, not a verified one. It still passes §3.
- **Not a demand for stylistic identity.** The two languages need not read alike; they must *claim* alike.
- **Not the same as the field of linguistics.** `domains/linguistics/` studies language data with annotation schemes and measured agreement; this doc is a *transmission* discipline that any domain can hit (M0.5 — one home per concept).

---

## Deliberate non-additions · 有意不新增

- **No `cross-language` capability.** The 8-axis feature vector (`data/capabilities.json`) has no language axis, so the capability could not fire on some realistic tasks and not others — it would not discriminate. The requirement is carried as the invariant **M4.10** plus this procedure (same logic as `methodology-fit` in P10; recorded in `review/integration-map-2026-10.md`).
- **No catalog entry for CAT/TM/MT tools as *evidence*.** A tool that proposes a rendering is not evidence that the rendering is faithful; fidelity's evidence is the §3 corroboration, not a product.
- **No duplicated translation-theory textbook.** This is a working procedure, not a survey; the canon is cited (`[R120]`–`[R126]`), not reproduced.

---

## See also · 另见

- `core/05-provenance-and-integrity.md` — **M4.10** (meaning-unit fidelity) and the M4 checklist/anti-patterns.
- `reference/methodology-map.md` — the method layer (M3.13); a bilingual study still declares its protocol, assumptions and reporting standard.
- `reference/evidence-instruments.md` — the instrument layer (M3.10); what *observes* a claim.
- `domains/linguistics/README.md` — language data, annotation and inter-annotator agreement.
- `review/integration-map-2026-10.md` — why this is an invariant, not a capability (deliberate non-addition).
- `review/references.md` §K — sources `[R120]`–`[R126]`.
