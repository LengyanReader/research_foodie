# Language polish: making generated prose readable · 语言润色：让生成的文字适合人读

> Readability, register, idiomaticity — what is mechanically checkable, what needs a reader, and the tools.
> 可读·语域·地道：哪些可机检，哪些需人读，工具在哪。
**Updated:** 2026-10-20

## 0. Why this is its own concern

A deliverable can be **true, sourced, and still fail**. The claim survives; the reader does not. Model prose fails in a
characteristic way: it hedges until the sentence says nothing, pads with stock phrasing, turns an argument into a bullet
list, and adopts a register that belongs to no actual audience. None of that is a factual error, so no verification gate
catches it — which is why polish needs its own gate (this doc grounds **M4.14** and the capability `prose-polish`).

**Method.** Web sources were fetched on **2026-10-20** with `python` + `urllib` and a Firefox UA; the status is recorded
per row. arXiv rows come from one `id_list` batch (`review/references.md` §P). Works that could not be fetched are marked
**not fetched** and are *not* used as evidence — they are named because a reader will expect them, and pretending a book
was verified would be worse than saying it was not.

---

## 1. The failure, named

Naming the defect is most of the fix. These are the recurring shapes in generated prose (editorial observation, not a
cited taxonomy):

| Failure | What it looks like | Why it hurts |
|---|---|---|
| **Hedge stacking** | "may potentially somewhat help in some cases" | The modality collapses; the reader cannot tell what is claimed. |
| **Stock-phrase saturation** | "in today's fast-paced world", "delve into", "it's not just X, it's Y", "a testament to" | Signals a template, not a thought; the reader discounts everything after it. |
| **List-ification** | Three bullets where one causal sentence was needed | Destroys argument structure; bullets cannot carry "because". |
| **False balance** | "While X, it is also important to note Y" with no weighing | Sounds fair, decides nothing. |
| **Summary-of-summary** | "In conclusion, as we have seen…" restating the section | Adds length, not information. |
| **Register mismatch** | Chatty for a regulator; bureaucratic for a tutorial | The content is right and the audience is wrong. |
| **Translationese** | Long pre-modifiers, stacked possessives, passive where the language prefers active | Grammatical, but no native writer would produce it. |
| **Em-dash / colon saturation** | Every paragraph performing "insight" with punctuation | Rhythm becomes monotone; emphasis stops meaning anything. |

---

## 2. Plain language & readability

**Verified.** The US federal plain-language guidance (R192, `plainlanguage.gov/guidelines/`, fetched 200) is the most
usable operational checklist: write for the reader, use short familiar words, prefer active voice, keep subject–verb–object
close, and organise for the reader's task rather than the writer's outline. It is guidance, not a metric.

**Readability formulas are advisory, never gates.** Flesch–Kincaid, SMOG and Dale–Chall (as implemented by R194
`textstat`) reduce a text to syllable and sentence-length proxies. They are useful for **catching drift** (a paragraph that
became twice as dense) and useless for **certifying quality**: a short, clear sentence can be false, and a long, dense one
can be exactly right for its audience. Treat a score as a *smoke detector*, not a verdict — the same discipline as M3.14
(a gate must not trade precision for coverage).

**Paywalled, therefore not relied on.** The ISO plain-language standard family exists, but its catalogue page returned
**403** from this host and the text is paywalled, so no rule in this doc rests on it. Same for the ISO post-editing and
MT-evaluation standards: named, not entered.

---

## 3. Register & style authorities

| Authority | Use it for | Status 2026-10-20 |
|---|---|---|
| Chicago Manual of Style | Books, humanities, citation form | **not fetched** (subscription) |
| APA 7 / MLA 9 | Social science / humanities citation and prose norms | **not fetched** |
| Oxford *New Hart's Rules* | British English house style | **not fetched** |
| Strunk & White, *The Elements of Style* | Terse prescriptive rules; good for triage, dated on grammar | **not fetched** |
| Gopen & Swan, "The Science of Scientific Writing" | **Information order**: put old before new, stress at the end — the single most useful idea here | **not fetched** (page returned 503) |
| Pinker, *The Sense of Style* | Why prose is hard; the "curse of knowledge" | **not fetched** |
| Williams, *Style: Lessons in Clarity and Grace* | Subject–verb–object discipline; nominalisation as the main enemy | **not fetched** |
| R199 Vale | **Mechanical enforcement** of a declared house style | fetched 200 |
| R200 LanguageTool | Grammar/style checking, including Chinese | fetched 200 |

The point of listing the unfetched four is not decoration: they disagree with each other. Strunk & White say "omit needless
words"; Gopen & Swan say the *position* of information matters more than its length. A harness that reduces "polish" to a
word-count rule has picked one authority and mistaken it for the field.

---

## 4. Chinese-specific failure modes

Chinese generated text fails differently from English, and the fixes are not translations of each other.

- **Punctuation is normative, not decorative.** R193 (GB/T 15834-2011《标点符号用法》) is the national standard; the
  portal answered 200, the full text was not downloaded. Full-width vs half-width, the correct use of 「」/“”/《》, and the
  ellipsis (……, six dots) are checkable. Mixed-width punctuation inside one sentence is the most common visible defect.
- **欧化句式 / 翻译腔 (Europeanised syntax).** Long attributive pre-modifiers ("一个在……背景下……的……的……"), stacked 的,
  and bare 被-passives where Chinese prefers a topic-comment or active form. Grammatical, unidiomatic. **This is editorial
  practice, not a cited finding** — name it, do not pretend it is a rule.
- **四字格堆砌.** Four-character phrases are a resource; three in a row is a slogan, not an argument.
- **的的不休.** Chains of 的 that could be recast as a topic-comment sentence.
- **Register drift between 简繁 / 书面口语.** Simplified/traditional conversion is not 1:1 (词汇与量词差异), so a mechanical
  conversion silently changes wording; treat conversion as translation, not encoding (cf. `reference/cross-language.md`).
- **Term consistency.** A term glossed once must be reused verbatim (M4.10 §4); paraphrasing a technical term reads as a
  different concept.

**Chinese readability metrics are weaker than English ones.** Syllable-count proxies do not transfer cleanly. Do not
pretend a translated Flesch score means anything; for Chinese, prefer a **checklist + a reader**.

---

## 5. Research base: simplification, style control, and self-editing

- **Text simplification** is a mature subfield with its own survey (R195) and evaluation resources (R196 ASSET, with
  multiple rewrite operations; R197 GEM, which scores several quality dimensions rather than one). The transferable
  lesson: **"simpler" is multi-dimensional** (lexical, syntactic, structural) and evaluated by humans, not by one number.
- **Self-refinement** (R198) improves output only when the feedback carries **new information** — an external check, a
  rubric, a reader. A model asked to "make it better" with no criterion mostly re-rolls its own prior. This is the same
  asymmetry as M5.11 (self-report is cheap; an external check is decisive).
- **Style steering / preference optimisation** can shift register, but the same machinery that makes text agreeable also
  makes it sycophantic (R191, §O) — optimizing for "sounds good to a rater" is not optimizing for "is good".

---

## 6. The gate: what a machine checks vs what a reader decides

| Mechanically checkable (hard gate is defensible) | Needs a reader (advisory only) |
|---|---|
| Declared house style runs clean (R199 Vale rules) | Does it sound like a person wrote it for *this* audience? |
| Term consistency against the bilingual term table | Is the register right (regulator / tutorial / paper)? |
| Punctuation per the standard (R193 for Chinese; publisher guide for English) | Is the argument's *order* right (Gopen & Swan)? |
| Banned-phrase / stock-phrase list per publication | Is a bullet list hiding a causal claim? |
| Numbers, units, identifiers verbatim (M4.10) | Is the emphasis in the right place? |
| Readability **band** (drift alarm, not a pass mark) | Does a native reader stumble anywhere? |

**Rule.** Never let a mechanical score *approve* prose. It may only **reject** (a banned phrase, a broken punctuation
rule, a term inconsistency) — the asymmetric form of a M3.14 gate.

---

## 7. A concrete polish pass

1. **Freeze the claim.** Snapshot the propositions (M4.4 ledger). Polish may not change scope, stance or modality (M4.10).
2. **Lint mechanically.** Run the declared style (Vale), the language checker (LanguageTool), and the punctuation rule.
   Fix only what the rule actually names; ignore taste.
3. **Cut the template.** Delete stock phrases, false balance, summary-of-summary, and hedging that carries no information.
4. **Restore argument.** Turn bullet lists back into causal sentences wherever the relation is "because", "therefore",
   "unless". Keep bullets for genuine enumerations.
5. **Re-order for the reader.** Old information first, new information stressed at the end; one idea per paragraph.
6. **Read it aloud (or have a fresh reader do it).** This is the only step that detects "grammatical but nobody would say
   this". Record the verdict; it is a judgement, not a measurement.

---

## 8. Deliberate non-additions & honest limits

- **No "AI-detector" as a quality gate.** Detection scores are unreliable and adversarial; using one to *approve* prose is
  a gate that trades precision for coverage (M3.14).
- **No single readability threshold.** A universal "grade 8" rule would fail exactly the texts that need density (legal,
  mathematical, clinical). Band + drift, not a pass mark.
- **No claim that ISO standards were read.** They were not (403 + paywall).
- **No claim that the classic style books were re-read.** They were not; they are named as authorities, not as evidence.
- **English and Chinese are not symmetric.** The Chinese section names failure modes that have no English equivalent
  (四字格, 的的不休) and omits English ones that do not transfer (article usage).

---

## 中文

**为什么单列。** 一段文字可以**真实、有出处，却仍然失败**：主张成立，读者读不下去。模型文本有固定病灶——对冲堆叠到什么也没说、
套话填充、把论证拆成项目符号、语域不属于任何真实受众。这些都不是事实错误，所以验证门禁抓不到，必须单设一道**润色门**（M4.14，能力 `prose-polish`）。

**可读性公式只作参考，绝不作判据。** textstat 一类工具把文本压成音节/句长代理；它能发现**漂移**（某段突然变密），不能**认证质量**——
短句也可能假，长句也可能正是该受众需要的。故只允许"机械项**否决**"，不允许"机械项**通过**"（M3.14 的非对称用法）。

**中外不对称。** 英文靠 Gopen & Swan 的**信息顺序**（旧信息在前、重点在句尾）与 Williams 的主谓宾纪律；中文的病灶是**欧化句式/翻译腔**
（长定语、叠"的"、滥用"被"）、**四字格堆砌**、**标点混用**（GB/T 15834-2011 有规定，全半角与「」“”《》可机检）、**繁简转换不等价**
（按翻译处理，不按编码处理）。中文可读性指标弱于英文，别拿翻译过来的 Flesch 分数当回事——用清单 + 一位读者。

**六步。** ① 冻结主张（M4.4）→ ② 机械 lint（Vale / LanguageTool / 标点）→ ③ 删模板（套话、假平衡、总结的总结、空对冲）→
④ 还原论证（该用"因为/因此/除非"的地方不许用项目符号）→ ⑤ 按读者重排（旧信息在前、重点在后、一段一意）→ ⑥ **读出声**或换一位新鲜读者
——只有这一步能发现"语法正确但没人会这么说"。第 ⑥ 步是判断，不是测量。

**有意不新增。** 不用"AI 检测器"当质量门（不可靠且对抗性强）；不设统一可读性阈值（法律/数学/临床正需要密度）；不声称读过 ISO 标准
（403 + 付费墙）；不声称重读过经典文体书（只作权威列名，不作证据）。
