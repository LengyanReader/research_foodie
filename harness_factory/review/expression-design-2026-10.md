# Expression design: choosing the form before the words · 表达设计：先定形式，再定措辞

> Structure, medium and modality as decisions with a cost — documentation architecture, the diagram/table/prose ladder,
> and translation as expression rather than substitution.
> 谋篇·选型·择模态：文档架构、图表/表格/文字的阶梯，以及把翻译当作表达而非替换。
**Updated:** 2026-10-20

## 0. Why this is its own concern

`prose-polish` fixes sentences. This document is about the decision made **before** the first sentence: given this
content and this reader, what *form* should carry it — a paragraph, a table, a diagram, a chart, a formula, a
storyboard, a recording? Getting the form wrong produces a failure no amount of editing repairs: a correct manual
organised around the author's outline, a table that hides the one comparison that mattered, a diagram that silently
drops a qualifier, or three pages of prose describing a structure that a five-line diagram would have settled.

The claim being defended here: **form is a design decision with a measurable cost to the reader** (time, working
memory, ambiguity), so it belongs under a gate, not under taste. This doc grounds clause **M4.15** and the capability
`expression-design`. It also carries the translation slice (requirement: 信达雅, not word-for-word) because translation
is the same problem with a fixed source — the content is given, the form is not.

**Method.** Pages were fetched **2026-10-20** with `python` + `urllib` and a Firefox UA. **Depth is graded, and stated:**
R219 (Diátaxis), R224 (MQM) and R233 (譯例言) were **read as text**, and every claim resting on them is quoted or
paraphrased from that text; R220-R223, R225, R231 and R232 answered **200** and are cited as first-party style or tool
references, but their individual clauses were not read line by line; the five arXiv rows are **abstract-level** (one
`id_list` batch), which covers every claim made here because each one appears in the abstract. The classic works a
reader will expect (Mayer on multimedia learning; Sweller on cognitive load; Paivio on dual coding; Tufte on
quantitative display; Rosenfeld & Morville on information architecture; Nida on dynamic equivalence) are **named and
not entered**: all are books behind a paywall, and no first-party record was reachable this session. They inform the
framing; no rule below rests on them.

---

## 1. Three questions, asked in this order

1. **What is the content unit?** A claim, a relation, a procedure, a quantity, a decision, a definition, or a
   *change over time*. Content units are not sentences — a procedure is a graph, a comparison is a matrix, a
   taxonomy is a tree. Writing prose first forces the unit into sentence shape and the shape then dictates the
   structure.
2. **What is the reader's task?** Learning it, doing it, looking something up in it, or understanding why it is so.
   These are four different documents (Diátaxis, §2). One document may contain all four; it must not blend them
   *within* a section.
3. **What does each candidate form cost the reader?** Every form trades something: prose carries causality and
   judgement but is slow to scan; a table is fast to compare but cannot say "because"; a diagram shows topology but
   loses precision; animation shows change but cannot be searched, quoted, or diffed.

**Rule.** Choose the cheapest form that still carries the relation *and* its qualifiers. When two forms tie, choose
the one with the **reviewable source** (§5).

---

## 2. Four reader needs, four forms

**Verified.** Diátaxis (R219, `diataxis.fr`, fetched 200) prescribes a mapping from four distinct user needs to four
document forms — **tutorials** (learning), **how-to guides** (doing), **reference** (looking up), **explanation**
(understanding) — and states that it addresses content (*what to write*), style (*how to write it*) and architecture
(*how to organise it*). The diagnostic value is in the **mismatch**: a page that teaches and also tries to be a
reference does neither, because the same sentence cannot be both "try this and see" and "this is the exhaustive
list".

| Reader need | Form | Carries | Fails when |
|---|---|---|---|
| Learn by doing | Tutorial | A guaranteed-success path, one at a time | It explains instead of leading |
| Do a task now | How-to guide | Goal → steps → result | It teaches background first |
| Look up a fact | Reference | Complete, uniform, scannable | It narrates or omits cases |
| Understand why | Explanation | Trade-offs, history, constraints | It becomes a procedure |

The practitioner style authorities make the same point at the sentence level: Google's developer documentation guide
(R220, fetched 200) and the Microsoft Writing Style Guide (R221, fetched 200) both fix voice, terminology, code
formatting and link text, and both assume the *architecture* is decided elsewhere. The Good Docs Project (R222, 200)
supplies templates per document type; Write the Docs (R223, 200) is the practitioner community where the genre
conventions are argued. Template without architecture reproduces the author's outline faster.

**Documentation quality has dimensions, and "good" is not one of them.** Treude, Middleton & Atapattu (R226,
arXiv:2007.10744v3) decompose documentation quality into **ten dimensions across structure, content and style**, and
had technical editors apply the framework to several genres; their finding that reference documentation and READMEs
score well while blog-article-style pages score poorly is exactly the four-forms argument measured. Structure is a
quality dimension, not decoration.

---

## 3. Locating what needs explanation

"Find the parts the reader will not follow" is a searchable operation, not an intuition. Four defects account for
most comprehension failures:

| Defect | Test | Fix |
|---|---|---|
| **Undefined term at first use** | Does every term appear after its definition *in reading order*? | Define at first use, or link to the definition |
| **Unstated precondition** | Can a reader start the procedure from a cold state? | Name the required state, version, permission, input |
| **Unexplained jump** | Does a conclusion introduce information not in the preceding two sentences? | Insert the missing middle step, or cut the conclusion |
| **Missing worked example** | Is there one concrete instance of each abstract rule? | One example per rule, not one per document |

A definition that first appears after the term's third use is a defect, not a stylistic choice: the reader has
already built a wrong model and must now rebuild it. The same for a reference table with no unit column — the unit
is a precondition, and its absence is the defect.

---

## 4. Form is a claim: fidelity survives the change of medium

A change of form is a change of **what the reader can check**. It may not change what is claimed (M4.10). Three
failure modes, all common:

- **Qualifier loss.** Prose says "measured on 38 of 50 tasks (12 had no full text)"; the diagram's box says
  "LitQA2". The diagram is now false.
- **Axis/unit loss.** A chart without units is a shape, not a quantity — the reader can rank but not act.
- **Category collapse.** A table whose column header merges two distinct categories ("status" covering both
  *unverified* and *disputed*) destroys the distinction the prose was careful to keep (M4.2).

So each non-text form needs a **text spine**: a caption that states the claim, the data, the unit and the caveat, and
alt text for the reader who cannot see it. **Verified.** WCAG 2.2 (R225, `w3.org/TR/WCAG22/`, fetched 200) carries
the normative text-alternatives requirement for non-text content; it is an accessibility floor and, conveniently, the
same discipline that makes a figure reviewable in a diff.

---

## 5. The modality ladder, ordered by cost to the reader

Cheapest first. Climb only when the cheaper rung cannot carry the relation.

| Rung | Use when the content is… | Cost | Evidence / status |
|---|---|---|---|
| **Prose** | Causal, judgemental, sequential-with-reasons | Slow to scan; the reader must hold the thread | — |
| **List** | Enumerable, unordered, same shape | Cannot carry "because"; ordering is lost | — |
| **Table** | Comparison across fixed attributes | Needs a stable schema; cells cannot argue | — |
| **Diagram (node-link)** | Topology: structure, flow, dependency, state | Precision; layout is editorial, not data | R227 (interactive codebase diagrams) |
| **Chart** | Distribution, trend, magnitude | Axis/aggregation choices change the reading | R232 (Vega-Lite grammar), R228 (animation) |
| **Formal notation** | Exactness: types, invariants, equations | Requires training; excludes readers | M3 formal-verification |
| **Animation / video** | The *change itself* is the content | Not searchable, not quotable, not diffable, expensive to revise | R228 |
| **Sound** | The signal is auditory (prosody, alert, music) | Not scannable; inaccessible without a transcript | — |

Two findings from the retrieved work are worth stating because they cut against the obvious reading:

- **Diagrams are cheap to generate and expensive to keep true.** Štěpánek et al. (R227, arXiv:2407.21621v1) observe in
  their abstract that software documentation "is usually textual and accompanied only by simple static diagrams", that
  maintaining it by hand is time-consuming, and that they therefore build the node-link diagram from the codebase by
  static analysis as a **viable alternative to missing or outdated documentation**. The lesson is not "draw more"; it is
  **derive the diagram from a machine-checkable source or expect it to lie within a release**.
- **Animation is an encoding channel, not a decoration.** Zong et al. (R228, arXiv:2208.03869v2) model animation in
  Vega-Lite as *time as an encoding channel*, so that static, interactive and animated views come from one
  specification and an author can move between them. That is the correct test for choosing video: **is time the
  variable being encoded?** If not, animation adds production cost and removes searchability for nothing.

**The reviewable-source rule.** A form whose source of truth is text or code (Mermaid R231, Vega-Lite R232, diagrams
generated from the artefact) can be reviewed, diffed and rebuilt. A rendered video cannot. So when the deliverable is
video, storyboard or comic, the **script/storyboard is the artefact of record** and the render is a build product; a
video with no text spine is an unreviewable claim. This is the same multi-format-from-one-source logic that makes
Pandoc (`document-parser`, already registered) useful: one source, many renderings, one place to correct.

---

## 6. Translation is expression under a constraint

The source is fixed; the form is not. The Chinese tradition states the trade-off better than any checklist, and the
**primary text is reachable**: Yan Fu's 譯例言 to 《天演論》 (R233, Wikisource, fetched 200; dated 光緒二十四年, 1898).

> 「譯事三難：信、達、雅。求其信已大難矣，顧信矣不達，雖譯猶不譯也，則達尚焉。」
> — Three difficulties: *xin* (faithful), *da* (intelligible/reaching), *ya* (refined). Faithfulness is already hard;
> but a faithful text that is not *da* "is translated yet as if untranslated" — so *da* comes next.

Three further points from the same page, each of which is an operational rule:

- **Not word-for-word, and this is stated as method, not licence.** 「不斤斤於字比句次，而意義則不倍本文」 — do not
  haggle over word order and sentence sequence, *but the meaning must not betray the original*. The licence and its
  limit are in one sentence.
- **Hold the whole text before writing.** 「將全文神理，融會於心，則下筆抒詞，自然互備」 — the unit of fidelity is the
  whole text, which is why sentence-by-sentence translation fails on discourse.
- **Naming is the expensive part.** 「一名之立，旬月踟躕」 — a single term may take months. And where no term exists,
  「即義定名」: coin it from the meaning, and record the choice. That is the ancestor of M4.10's "an untranslatable
  term gets a note, never a silent substitution" — with the addition that the coined term is a **decision to log**.

**Modern evidence agrees that the trade-off is real and measurable.** Griebel & Underwood (R229, arXiv:2605.15282v1)
measure fluency (original-likeness via a translationese classifier) and faithfulness (COMET-KIWI) on 130,486 translated
paragraphs from 106 novels in 16 source languages, across human, Google Translate and TranslateGemma translations, and
find a **consistent negative correlation** between the two — weaker and often non-significant for one system, but
present for human and MT alike. Two consequences: "fluent" is not evidence of "faithful" (the polish gate cannot
certify translation), and the correlation is **length-sensitive**, so segment length must be held fixed before
comparing systems.

Jin, An & Ma (R230, arXiv:2407.08978v1) supply the discourse argument: their Chinese–English literary corpus of 160
books shows that sentence-aligned evaluation assumes an alignment that literary text does not provide, and that
chapter-to-chapter context is itself a hard setting. So: **translate at the size of the meaning unit, not the
sentence** — which is what M4.10 already requires, now with a corpus.

**For quality claims, use a shared typology rather than adjectives.** MQM (R224, `themqm.org`, fetched 200) is an
analytic translation-quality framework — human and automatic — built on an open hierarchical error typology
(Accuracy, Fluency, Terminology, Style and more) with scoring models, and states alignment with ISO 5060. Its value
here is that it converts "信达雅" into countable error categories, so a translation claim can be **audited** rather
than admired. (The ISO text itself is paywalled and not entered; the alignment claim is the MQM Council's own.)

**Deliberate non-entry.** Nida's *dynamic equivalence* is the Western counterpart of 信达雅 and is named in the
capability rationale; the 1964 book is not reachable first-party, so no rule cites it. The Chinese primary text does
the same work with a citation that can be checked.

---

## 7. What a harness must do

1. **Ask the three questions before drafting** (§1) and write the answers down — one line each. A form chosen before
   the content unit is known is a template.
2. **Assign each section a reader need** (§2) and refuse a section that tries to serve two.
3. **Run the four comprehension-defect checks** (§3) as a list, not a feeling.
4. **Carry every qualifier across the form change** (§4), and give every non-text form a caption plus alt text.
5. **Climb the ladder only as far as the relation requires** (§5), and keep the source of truth reviewable.
6. **For translation, fix the unit at the meaning unit, log coined terms, and report quality as error categories**
   (§6) — never as "fluent".
7. **Declare the audience, register and channel before polishing** (M4.14) — the reader is not a constant.

## Anti-patterns

- **Type-first drafting.** "It's a README" → template → content squeezed into the template.
- **One document, four needs.** A tutorial that is also the reference and also the rationale; each reader is slowed.
- **Prose describing a structure.** Three paragraphs narrating a five-node graph.
- **Decorative diagram.** A figure that restates the caption and carries no relation.
- **Chart without units, caption without caveat, diagram without the excluded cases.**
- **Video for a static relation.** Production cost, no search, no diff, no quote.
- **Translation as substitution.** Word-for-word where the unit is the paragraph; coined terms unlogged.
- **"Fluent, therefore faithful."** R229 measures them as negatively correlated.

## See also

`../core/05-provenance-and-integrity.md` (M4.10 cross-language, M4.14 reader gate, M4.15 this clause) ·
`language-polish-2026-10.md` (sentence-level failure taxonomy) · `../reference/cross-language.md` (meaning-unit
alignment, round-trip) · `../reference/outlet-map.md` (where documentation and translation research is published) ·
R219–R233 in `references.md` §R.
