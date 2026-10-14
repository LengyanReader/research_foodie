# Domain · Reading & distillation · 读物阅读域
> Wiring `core/` modules into **type-aware, provenance-grounded, near-lossless** reading of texts and books.
> 把 `core/` 模块接线成一条「**按类型识别、来源可溯、近乎无损**」的文本/书籍阅读流水线。
**Updated:** 2026-10-13

---

## 中文速览
读物阅读域的目标是：**先判定读物类型，再按类型穷尽提炼维度，尽可能信息无损，并在拿不到原文时明确通知人工**。以 L0–L6 分层编排 `core/`：L0 判型（体裁/语言/版本/目的）、L1 获取原文（公版库/借阅库/开放获取/API，记录来源+访问日期+许可）、L2 解析归一（PDF/EPUB/DOCX/HTML → 带章节结构的纯文本，哈希固定版本）、L3 按类型提炼（见 `extraction-dimensions.md` 的全维度清单）、L4 无损蒸馏（引文带定位锚点，区分「原文陈述」与「提炼/推断」，覆盖式抽取）、L5 保真校验（回指原文、缺口/歧义标注、三态判定）、L6 记录与通知（溯源台账 + 未获取/未决项 → 人工）。**核心铁律：原文在手之前，绝不编造原文内容（M0.1/M0.2/M4）。**

---

## What this domain is for · 用途
Turn a text — a book, paper, report, essay, novel, statute, scripture, manual, transcript — into a **structured, source-anchored, near-lossless distillation** (key points, highlights, author intent, argument, evidence, themes, terminology, quotes, unresolved questions), while **acquiring the original** and **escalating to a human** whenever it cannot be obtained or the fidelity is uncertain.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Identify & classify material | M0, M7 | genre, language, edition, medium, reader purpose; sets the extraction profile |
| L1 | Locate & acquire original | M6, M4 | public-domain / borrowable / open-access / purchase; record source + access date + license |
| L2 | Ingest & normalize | M6, M2 | PDF/EPUB/DOCX/HTML/OCR → text + chapter structure; content hash pins the version |
| L3 | Type-aware extraction | M1, M4 | pick the dimension set by genre (see `extraction-dimensions.md`) |
| L4 | Lossless distillation | M1, M3 | coverage ledger; anchored verbatim quotes; quote vs inference kept apart |
| L5 | Fidelity verification | M3, M4 | every distilled claim points back to an anchor; gaps/ambiguity flagged; three-state |
| L6 | Record & notify | M4, M7, M8 | provenance ledger; **fail-loud to a human** on unobtainable/ambiguous items |

## Type taxonomy · 读物类型（L0 判定）
The genre decides **which dimensions matter and how lossless is defined**. · 体裁决定**提炼哪些维度、如何定义无损**。

| type · 类型 | signal cues · 线索 | extraction emphasis · 提炼侧重 |
|---|---|---|
| Academic paper · 学术论文 | abstract, DOI, arXiv, methods, results | thesis, method, data, results, limitations, citations |
| Monograph / book · 专著 | chapters, preface, index | argument arc, chapter theses, key claims, terminology |
| Textbook · 教材 | exercises, chapter summaries | concepts, definitions, worked examples, learning objectives |
| Essay / op-ed · 散文/评论 | thesis, rhetoric, stance | central claim, argument, rhetoric, assumptions, counter-points |
| Fiction / novel · 小说 | characters, plot, narrative | characters, plot, themes, motifs, POV, symbolism, tone |
| Poetry · 诗歌 | verse, lineation | imagery, form, meter, themes, ambiguity (preserve, don't resolve) |
| Scripture / classic · 经典/经文 | canon, verse, commentary | structure, pericopes, key verses, interpretive traditions, ambiguities |
| Report / whitepaper · 报告/白皮书 | exec summary, findings | findings, recommendations, data, caveats, actionables |
| Legal / statute / contract · 法律文本 | clauses, sections, parties | obligations, rights, definitions, conditions, exceptions, cross-refs |
| Technical / manual · 技术文档 | steps, API, version | procedures, prerequisites, parameters, warnings, version |
| History / biography · 史传 | chronology, sources | timeline, actors, causes, evidence quality, bias, contested claims |
| Transcript / interview · 访谈/记录 | speakers, timestamps | speakers, claims, positions, commitments, actionables |
| Dataset / table · 数据集 | schema, columns | schema, provenance, definitions, caveats, license |

## Module combination · 模块组合
- **M0** — the constitution: **never fabricate source content**; truth and traceability outrank coverage.
- **M1** — hold only the passage under distillation plus its anchors, not the whole book, in context.
- **M2** — long books / multi-volume runs persist a reading ledger and resume across sessions.
- **M3** — separates the distiller from the verifier; "done" requires every claim to point back to an anchor.
- **M4** — the spine: quote ↔ source(edition, chapter/page, offset) ledger; distinguish quote from inference.
- **M6** — the acquisition + parsing toolset (libraries, `pandoc`/`calibre`/`MinerU`/`GROBID`/OCR), minimal and fail-loud.
- **M7** — the deliverable is reviewable; no auto-publish; downloads recorded with license.
- **M8** — **escalate to a human** when the original is unobtainable, editions conflict, or fidelity is uncertain.

## Acquisition · 原文获取
Locate and, where lawful, fetch the original; **record source + access date + license**. · 定位并（在合法前提下）获取原文，记录来源、访问日期与许可。

1. **Public domain · 公版** — Project Gutenberg, Standard Ebooks, HathiTrust (full-view only).
2. **Borrow / lend · 借阅** — Internet Archive, Open Library (controlled digital lending).
3. **Open access · 开放获取** — DOAB, Unpaywall, CORE, arXiv, publisher OA.
4. **Metadata / preview · 元数据** — Open Library, Google Books, WorldCat (locate, not full text).
5. **Purchase / library · 购买/馆藏** — purchase links or interlibrary loan; **never** scrape paywalled/DRM text.
6. **Fallback · 兜底** — if none succeed: **STOP and notify a human** with what was tried and what is missing.
   **找不到或无法合法获取时：停止，并通知人工**（列出已尝试渠道与缺口；不得编造原文）。

## Lossless doctrine · 无损准则
- **Anchored quotes · 带锚引文** — every highlight is verbatim with a locator (edition/page/chapter/paragraph/offset).
- **Quote ≠ inference · 引文≠推断** — the source's words and your reading are visually separate (M4).
- **Coverage ledger · 覆盖台账** — every chapter/section is accounted for; omissions are logged, never silent.
- **Preserve uncertainty · 保留不确定** — ambiguity is marked, not resolved away; unused/uncertain items surfaced.
- **Retain the original · 留存原文** — the normalized text is kept alongside the distillation for re-checking.
- **Profile-driven depth · 按型定深** — the genre sets which of the full dimension set applies.

## Human-notification triggers · 人工通知触发条件
| trigger · 触发 | action · 动作 |
|---|---|
| Original not found / not licensed · 原文未找到/未授权 | stop; report attempted channels + gap |
| Paywall / DRM / copyright · 付费墙/版权限制 | request human decision; do not circumvent |
| Conflicting editions / versions · 版本冲突 | present candidates; await choice |
| OCR/extraction fidelity below threshold · 提取保真度不足 | flag sections; request human or better scan |
| Genre ambiguous / mixed · 体裁不明/混合 | present classification + confidence; await confirmation |
| Provenance incomplete · 溯源不完整 | mark `unverified`; do not present as fact |

## Discipline-specific risks · 领域特有风险
- **Fabricated quotations or page numbers** — the cardinal sin (M0.2/M4).
- **Summary that erases uncertainty** — flattening what the text leaves open (M0.1).
- **Paraphrase-as-quote** — presenting your reading as the author's words.
- **Edition / translation confusion** — conflating versions or losing the original language.
- **Coverage illusion** — a tidy summary that silently dropped whole regions of the text.
- **Copyright violation** — downloading beyond lawful access.

## See also
`extraction-dimensions.md` (the exhaustive dimension checklist) · `../core/00-index.md` · `../core/05-provenance-and-integrity.md` · `../humanities/README.md` · `../review/harness-index.md`.
