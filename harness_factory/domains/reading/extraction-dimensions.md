# Reading · Extraction dimensions · 阅读提炼维度全清单

> The exhaustive dimension set for **near-lossless** reading. Pick the subset by genre (L3); never silently drop
> a dimension the genre needs. Every extracted item carries an anchor `(edition, locator)` and a status.
> 阅读「近乎无损」的**全维度清单**。按体裁选子集（L3），体裁需要的维度不得静默丢弃。每条产出都带定位锚点与状态。
**Updated:** 2026-10-13 · Companion to `domains/reading/README.md`.

---

## How to use · 用法
1. **Classify** the material (L0) → gives a genre.
2. **Select** dimensions via the genre map (bottom).
3. **Extract** each dimension into the distillation, each item anchored and status-tagged.
4. **Verify** (L5) that every section is covered (coverage ledger) and every claim resolves to an anchor.

**Status vocabulary · 状态词表（M4）:** `quote` (verbatim, anchored) · `paraphrase` (your words, anchored) ·
`inference` (your reading, no source claim) · `unverified` (cannot be traced) · `ambiguous` (text is genuinely open).

---

## A. Bibliographic & identity · 书目与身份
| # | dimension · 维度 | what to capture · 抓取内容 |
|---|---|---|
| A1 | title / subtitle · 标题/副标题 | title, subtitle, series · 标题、副标题、丛书 |
| A2 | author / editor / translator · 作者/编者/译者 | names, roles, dates · 姓名、角色、年代 |
| A3 | edition / version · 版本 | edition, printing, revision, ISBN/DOI · 版次、印次、修订、ISBN/DOI |
| A4 | publisher / date / place · 出版信息 | publisher, year, place · 出版方、年份、地点 |
| A5 | original language / translation · 语言/译本 | source language; translator; translation notes · 原语、译者、译注 |
| A6 | medium / format · 载体 | print/ebook/scan/HTML; file hash · 纸质/电子/扫描；文件哈希 |
| A7 | license / rights · 许可/权利 | public domain / CC / copyright status · 公版/CC/版权状态 |
| A8 | source & access date · 来源与访问日期 | where obtained; when (M4) · 获取处与访问日期 |
| A9 | genre / discipline · 体裁/学科 | the L0 classification + confidence · L0 分类与置信度 |
| A10 | intended audience · 目标读者 | who the text addresses · 文本面向谁 |
| A11 | reader purpose · 阅读目的 | why we read it (drives depth) · 阅读目的（决定深度） |

## B. Structural · 结构
| # | dimension · 维度 | what to capture · 抓取内容 |
|---|---|---|
| B1 | outline / TOC · 目录大纲 | parts, chapters, sections, headings · 部、章、节、标题 |
| B2 | hierarchy / nesting · 层级 | depth, cross-references · 层级、交叉引用 |
| B3 | front/back matter · 前后附 | preface, intro, appendix, index, notes · 序、导言、附录、索引、注释 |
| B4 | coverage ledger · 覆盖台账 | every unit accounted for; omissions logged · 每单元有交代，遗漏入账 |
| B5 | section summaries · 分段摘要 | one line per unit (skeleton) · 每单元一行骨架 |

## C. Propositional — key points & highlights · 命题层：要点与重点
| # | dimension · 维度 | what to capture · 抓取内容 |
|---|---|---|
| C1 | thesis / central claim · 中心论点 | the main proposition · 主要主张 |
| C2 | key points · 要点 | ranked list of the load-bearing points · 承重要点（排序） |
| C3 | highlights · 重点 | passages marked most important · 最重要段落 |
| C4 | sub-claims · 次级主张 | supporting propositions · 支撑性命题 |
| C5 | definitions · 定义 | key terms as defined by the text · 文本自定义的关键术语 |
| C6 | enumerations · 列举 | lists, steps, taxonomies · 清单、步骤、分类 |
| C7 | data / figures · 数据/图表 | numbers, tables, figure captions · 数字、表格、图注 |
| C8 | examples / cases · 例证 | illustrative cases · 示例与案例 |
| C9 | counterpoints · 反例 | acknowledged objections · 已承认的反驳 |

## D. Intent & rhetoric · 意图与修辞
| # | dimension · 维度 | what to capture · 抓取内容 |
|---|---|---|
| D1 | author intent · 作者意图 | stated aim / purpose · 声明的目的 |
| D2 | audience address · 面向对象 | who is being persuaded · 劝说对象 |
| D3 | rhetorical strategy · 修辞策略 | ethos/pathos/logos, framing · 修辞与框定 |
| D4 | tone / register · 语气/语域 | formal/informal, ironic, polemical · 语气 |
| D5 | stance / bias · 立场/偏见 | what the author is committed to · 作者的立场 |
| D6 | implied assumptions · 隐含前提 | unstated premises · 未言明的前提 |
| D7 | omissions / silences · 沉默/回避 | what is conspicuously not said · 明显未说之处 |

## E. Argument & evidence · 论证与证据
| # | dimension · 维度 | what to capture · 抓取内容 |
|---|---|---|
| E1 | argument map · 论证图 | premises → inference → conclusion · 前提→推理→结论 |
| E2 | evidence type · 证据类型 | empirical, textual, anecdotal, formal · 证据种类 |
| E3 | evidence quality · 证据质量 | strength, sample, method · 强度、样本、方法 |
| E4 | warrant · 论证担保 | why the inference holds · 推理成立的理由 |
| E5 | logical form · 逻辑形式 | deductive/inductive/abductive · 演绎/归纳/溯因 |
| E6 | fallacies · 谬误 | detected gaps (flag, don't silently fix) · 检测到的逻辑缺口 |
| E7 | contradictions · 矛盾 | internal tensions · 内部矛盾 |
| E8 | open questions · 未解问题 | what the text leaves open · 文本悬置的问题 |

## F. Content-specific · 内容物（按体裁展开）
| # | dimension · 维度 | applies to · 适用 |
|---|---|---|
| F1 | characters · 人物 | fiction, biography, drama |
| F2 | plot / narrative arc · 情节 | fiction |
| F3 | setting · 场景 | fiction, history |
| F4 | themes / motifs · 主题/母题 | fiction, essay, poetry |
| F5 | symbols / imagery · 象征/意象 | poetry, fiction |
| F6 | point of view · 视角 | fiction |
| F7 | timeline / chronology · 时间线 | history, biography, report |
| F8 | actors / agents · 行动者 | history, social science |
| F9 | causes / consequences · 因果 | history, science |
| F10 | method / procedure · 方法/流程 | paper, technical, textbook |
| F11 | results / findings · 结果/结论 | paper, report |
| F12 | limitations · 局限 | paper, report |
| F13 | obligations / rights · 义务/权利 | law, contract |
| F14 | conditions / exceptions · 条件/例外 | law, contract |
| F15 | prescriptions / recommendations · 建议 | report, whitepaper |
| F16 | actionables · 可执行项 | report, transcript, manual |

## G. Language & reference · 语言与指涉
| # | dimension · 维度 | what to capture · 抓取内容 |
|---|---|---|
| G1 | key quotations · 关键引文 | verbatim + anchor (M4) · 原文+锚点 |
| G2 | terminology / glossary · 术语表 | term → definition → locator · 术语→定义→位置 |
| G3 | allusions / citations · 用典/引用 | works referenced by the text · 文本引用之作 |
| G4 | cross-references · 交叉引用 | internal pointers · 内部指向 |
| G5 | translation notes · 译注 | decisions that change meaning · 影响语义的译法 |
| G6 | ambiguous passages · 歧义段落 | keep open, mark `ambiguous` · 保留开放，标 `ambiguous` |

## H. Meta / synthesis · 元与综合
| # | dimension · 维度 | what to capture · 抓取内容 |
|---|---|---|
| H1 | layered summary · 分层摘要 | one-line / paragraph / full brief · 一行/一段/全文简报 |
| H2 | significance · 意义 | why it matters to the reader's goal · 对读者目标的意义 |
| H3 | relation to other works · 与他作关系 | agreements, contradictions, lineage · 一致/矛盾/脉络 |
| H4 | unresolved / follow-ups · 待办/后续 | open threads, next readings · 未决线索、后续阅读 |
| H5 | fidelity report · 保真报告 | coverage %, anchors resolved, flagged items · 覆盖率、锚点、标记项 |

---

## Genre → dimension map · 体裁→维度映射
Select at least the listed dimensions; add others as the text warrants. · 至少选取所列维度，可按需增补。

| genre · 体裁 | must-include dimensions · 必含维度 |
|---|---|
| Academic paper · 学术论文 | A, B, C1–C8, D1,D6, E1–E8, F10–F12, G1–G3, H1–H5 |
| Monograph / book · 专著 | A, B, C, D, E, G, H |
| Textbook · 教材 | A, B, C1–C7, E1, F10, G1–G2, H1–H2,H5 |
| Essay / op-ed · 散文/评论 | A, B, C1–C4, D1–D7, E1–E6, G1, H1–H3,H5 |
| Fiction / novel · 小说 | A, B, C1,C5, D1–D4, F1–F6, G1,G6, H1–H3,H5 |
| Poetry · 诗歌 | A, B, C1, D3–D4, F4–F5, G1,G5–G6, H1,H3,H5 |
| Scripture / classic · 经典 | A, B, C1–C5, D1,D6, E1–E4, F7, G1,G3,G5–G6, H1–H3,H5 |
| Report / whitepaper · 报告 | A, B, C1–C8, E2–E3, F7,F11–F15, G1, H1–H2,H4–H5 |
| Legal / statute · 法律 | A, B, C1,C5,C6, F13–F14, G2,G4, H5 |
| Technical / manual · 技术文档 | A, B, C1,C5–C8, F10, G1–G2, H1,H4–H5 |
| History / biography · 史传 | A, B, C1–C4, D1,D5–D7, E2,E6–E8, F7–F9, G1–G3, H1–H3,H5 |
| Transcript / interview · 访谈 | A, B, C1,C4, D1,D5, F8,F16, G1, H1,H4–H5 |
| Dataset / table · 数据集 | A, C5,C7, E2, G2, H5 |

---

## Lossless checklist · 无损核对清单
- [ ] Every structural unit appears in the **coverage ledger** (no silent omission).
- [ ] Every highlight is **verbatim + anchored**; paraphrase and inference are labeled.
- [ ] Each dimension item carries a **status** (`quote`/`paraphrase`/`inference`/`unverified`/`ambiguous`).
- [ ] The **original normalized text is retained** for re-checking.
- [ ] Genuinely open passages are marked `ambiguous`, not resolved.
- [ ] The **fidelity report** states coverage %, resolved anchors, and flagged items.
