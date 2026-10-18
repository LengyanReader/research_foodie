# Domain · Writing / essay · 写作域

> Tailored harness for essay / academic writing (esp. for big-pickle): enforce citation-first,
> claim→evidence pairing, a context pack, and a clarity checklist.
> 针对论文/学术写作（尤其面向 big-pickle）：强制**引用优先**、**论点↔证据配对**、上下文包与清晰度清单。

**Updated:** 2026-10-15

## 中文速览
写作的短板通常不在「润色」，而在**证据、结构、原创性**。本域用 harness 补足**系统性流程**：先定 thesis 与
论证结构，再为每条 claim 强制配证据，最后按 rubric 自评并棘轮固化——而不是只做文字打磨。

> **任务句（接在「配置」之后贴给助手）· Task line (paste after the config).**「用 writing 域为我建写作 harness：先定 thesis 与
> outline，每条 claim 强制配**可溯源**证据（semantic-scholar / crossref / openalex），初稿后做
> originality check 与校验，再按 `writing` rubric 自评并**棘轮固化**（不回退）。」

## What this domain is for · 用途
Turn "write an essay / a paper section" into a **gated pipeline**: interpretation → outline → evidence →
draft → originality → verification → clarity. Style polish is the **last** step, not the first.
把「写一篇文章」变成**带门禁的流水线**；润色排在**最后**，而非最先。

## Modules · 模块组合
Enabled · 启用：**M1**（规划/综合）· **M3**（校验）· **M4**（溯源）· **M7**（结构/清晰）。
M4 令每条 load-bearing claim 必须可溯源；M3 令「完成」= 通过校验（而非自我感觉良好）。

## Rubric · 评分表（humanities-aligned）
`interpretation 0.25 · context 0.20 · evidence 0.20 · originality 0.15 · clarity 0.10 · rigor 0.10`

> 本域已在 `data/rubrics.json` 注册独立 rubric（`writing`），数值与 `humanities` 一致；可经
> `--domain writing` 直接使用（不再需要借道 `humanities`）。

## Pipeline · 流水线
| layer · 层 | step · 步骤 | guarantee · 保证 | module |
|---|---|---|---|
| L0 | 题目解析 · parse | 复述真实问题（thesis + 受众 + 体裁），歧义则先确认 | M0,M7 |
| L1 | Outline · 结构 | thesis + 分论点 + 论证顺序（先骨架后血肉） | M1,M7 |
| L2 | Context pack · 上下文包 | 关键来源入包（academic-search / crossref / openalex） | M1,M6 |
| L3 | Claim→Evidence · 配对 | **每条 claim 强制挂证据**；无源则标 `unverified` | M4 |
| L4 | Draft · 草稿 | 按 outline 成文；引文逐条锚定 | M1,M4 |
| L5 | Originality · 原创性 | 区分「复述」与「己见」；标注借鉴来源 | M3,M4 |
| L6 | Verify · 校验 | claim 全部可解析到来源；缺口/矛盾如实标注 | M3,M4 |
| L7 | Clarity · 清晰 | 结构/行文润色（最后一步） | M7 |

## Tools · 工具
`academic-search` · `evidence-extractor` · `survey`（见 `harness catalog --class deep-research`）。

## Quick check · 快速自检
```bash
# gaps -> harness configuration, scored against the writing rubric
harness standard --domain writing plan <objective>
```

## Status · 状态（registered）
本域已注册进 SSOT：`data/domains.json` 有 `writing` 条目（faculty `humanities`、artifact `document`、
grounding `required`、20 条分类信号），`data/rubrics.json` 有独立 `writing` rubric。因此
**`--domain writing` 可直接选择**，`standard --domain writing …` 可直接评分，分类器也能凭信号命中本域。

## Cross-language writing · 跨语言写作
When the same deliverable is written in two languages (English master + Chinese executive summary, or vice versa), the discipline is **M4.10**: produce **two coordinated renderings of one meaning**, compress by omission and never by distortion, carry the same citations/identifiers, and handle untranslatable terms by gloss rather than substitution. Procedure: `../../reference/cross-language.md`.

## See also
`../humanities/README.md`（学术人文写作的通用流程）· `../deep-research/README.md`（证据获取）·
`../excellence/README.md`（同样用棘轮固化质量）· `../../core/05-provenance-and-integrity.md`（M4）。
