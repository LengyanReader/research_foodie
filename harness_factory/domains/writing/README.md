# Domain · Writing / essay · 写作域

> Tailored harness for essay / academic writing (esp. for big-pickle): enforce citation-first,
> claim→evidence pairing, a context pack, and a clarity checklist.
> 针对论文/学术写作（尤其面向 big-pickle）：强制**引用优先**、**论点↔证据配对**、上下文包与清晰度清单。

**Updated:** 2026-10-14

## 中文速览
写作的短板通常不在「润色」，而在**证据、结构、原创性**。本域用 harness 补足**系统性流程**：先定 thesis 与
论证结构，再为每条 claim 强制配证据，最后按 rubric 自评并棘轮固化——而不是只做文字打磨。

> **一句话指令词（贴给助手）· One-liner for an agent.**「用 writing 域为我建写作 harness：先定 thesis 与
> outline，每条 claim 强制配**可溯源**证据（semantic-scholar / crossref / openalex），初稿后做
> originality check 与校验，再按 humanities rubric 自评并**棘轮固化**（不回退）。」

## What this domain is for · 用途
Turn "write an essay / a paper section" into a **gated pipeline**: interpretation → outline → evidence →
draft → originality → verification → clarity. Style polish is the **last** step, not the first.
把「写一篇文章」变成**带门禁的流水线**；润色排在**最后**，而非最先。

## Modules · 模块组合
Enabled · 启用：**M1**（规划/综合）· **M3**（校验）· **M4**（溯源）· **M7**（结构/清晰）。
M4 令每条 load-bearing claim 必须可溯源；M3 令「完成」= 通过校验（而非自我感觉良好）。

## Rubric · 评分表（humanities-aligned）
`interpretation 0.25 · context 0.20 · evidence 0.20 · originality 0.15 · clarity 0.10 · rigor 0.10`

> 该表与 `data/rubrics.json` 的 `humanities` 域一致。**当前经 `--domain humanities` 使用**（本域尚未作为
> 独立 rubric 注册，见下「状态」）。

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
# gaps -> harness configuration, scored against the humanities rubric
harness standard --domain humanities plan <objective>
```

## Status · 状态（pending registration）
本域当前为**文档级（L0）harness**：`domains/writing/README.md` 已就绪，但**尚未注册**进
`data/domains.json` 与 `data/rubrics.json`（SSOT），因此 `--domain writing` 暂不可选，需经
`--domain humanities` 使用其 rubric。注册（新增 `domains.json` 条目 + 可选独立 rubric + 分类信号）是
一个**待定决策**——保持 SSOT 单一来源，不静默改动。

## See also
`../humanities/README.md`（学术人文写作的通用流程）· `../deep-research/README.md`（证据获取）·
`../excellence/README.md`（同样用棘轮固化质量）· `../../core/05-provenance-and-integrity.md`（M4）。
