# Philosophy · 哲学域

> Wiring `core/` modules into philosophical work across schools: argument reconstruction, declared positions, counterexample honesty.
> 把 `core/` 模块接线成「论证重构、立场声明、反例坦诚」的哲学工作流——不限流派。

**Updated:** 2026-10-23 · **Faculty:** humanities · **Artifact:** document · **Grounding:** preferred

---

## 中文速览

哲学域覆盖**从诠释学到分析哲学再到批判理论**的论证类工作：一手文本细读（M4）→ 论证逐前提重构 → **声明诠释立场与视域**（M4.15）→ 找最强反例 → 区分「文本怎么说」与「我主张什么」。域特有风险：**把诠释当论证**、**立场隐身**（未声明的立场 = 以写作者为默认受众）、**稻草人化对手**、**用术语堆砌代替论证**。思想/学术流派的梳理见 `reference/methodology-map.md`（诠释学 · 现象学 · 分析哲学 · 实用主义 · 批判理论 · 结构主义各行）。

## Wiring · 接线

| Level | Move | Modules | Gate |
|---|---|---|---|
| L0 | State the question and its tradition | M7 | 传统/流派点名（methodology-map 行） |
| L1 | Reconstruct the arguments from primary texts | M4 | 逐前提重构；引用落原文片段（M4.16） |
| L2 | Declare the interpreter's position and horizon | M4.15 | 立场、视域、受众先声明 |
| L3 | Search for the strongest counterexample | M3 | 最强反例，不是最弱反例 |
| L4 | Separate exegesis from systematic claim | M3, M4 | 「文本说 X」与「我主张 Y」分行 |
| L5 | Write with the position and its rivals named | M7, M4.10 | 对手立场以其最强形态入文 |

## Risks · 域特有风险

- **Interpretation as argument** — 诠释结论当作论证结论汇报（humanities 域的同族风险）。
- **Hidden position** — an undeclared stance silently becomes "whoever is writing" (M4.14).
- **Strawmanning** — the rival view stated in its weakest form (L3's gate exists to stop this).
- **Term-dropping** — 术语堆砌代替论证；每个承重术语须首现即定义（M4.15 四缺陷检索）。

## Rubric · 评分

`data/rubrics.json` `philosophy`（论证重构 0.25 · 立场声明 0.2 · 反例坦诚 0.2 · 文本忠实 0.15 · 校准 0.1 · 清晰 0.1）。`harness standard --domain philosophy` 可跑。

## Outlets · 信息源

一手哲学文献：**PhilPapers**（索引）· **Stanford Encyclopedia of Philosophy**（peer-reviewed 综述）——两者均已在 outlets 组核验；经典文本语料（Perseus / Past Masters）尚未入 instruments（P27 登记的候选）。检索前读 `outlet-map.md` 各条 `not_for`。

## See also · 另见

`../domains/humanities/README.md`（诠释的相邻域）· `../reference/methodology-map.md`（流派行）· `../core/05-provenance-and-integrity.md`（M4.16 指针三失效）· `../review/language-polish-2026-10.md`（M4.14 受众声明）。
