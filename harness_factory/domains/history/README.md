# History · 史学域

> Wiring `core/` modules into primary-source historical work: source criticism first, periodization declared, silences weighed.
> 把 `core/` 模块接线成「史源批判先行、断代显式、沉默入账」的史学工作流。

**Updated:** 2026-10-23 · **Faculty:** humanities · **Artifact:** document · **Grounding:** required

---

## 中文速览

史学域让**每一个历史断言都挂在一手史料上、带着日期、并声明诠释视角**。以 L0–L5 编排 `core/`：L0 问题与时段（M7）、L1 史源定位与溯源（M4）、L2 史源批判——真伪·偏见·阙漏（M3/M4）、L3 重建并**显式断代与分期**（M3）、L4 权衡反叙事与沉默（M3/M5）、L5 带日期与视角写作（M7/M4.10）。域特有风险：**以论带史**、**去语境化引用**、**时代错置**、**把沉默当不存在**、**版本/译本混淆**。

## Wiring · 接线

| Level | Move | Modules | Gate |
|---|---|---|---|
| L0 | Frame the question in time and place | M7 | scope + period named |
| L1 | Locate and provenance the sources | M4 | every source carries origin + access date |
| L2 | Criticize the sources (authenticity, bias, lacunae) | M3, M4 | 史源批判三问作答：真伪 · 偏见 · 阙漏 |
| L3 | Reconstruct with periodization declared | M3 | 断代/分期是声明，不是默认 |
| L4 | Weigh counter-narratives and silences | M3, M5 | 反叙事与沉默入账（M3.15 分阶段归因） |
| L5 | Write with dated claims and an explicit lens | M7, M4.10 | 每个断言带日期；视角显式 |

## Risks · 域特有风险

- **以论带史** — the thesis selects the sources instead of the sources bounding the thesis.
- **Anachronism · 时代错置** — a concept from one period applied to another without declaring the jump.
- **Silence as absence** — a gap in the archive reported as "nothing happened" instead of a gap in the evidence (M4.13's "the material is silent" is the honest form).
- **Version/edition confusion** — citing a later redaction as the period's voice.

## Rubric · 评分

`data/rubrics.json` `history`（史源批判 0.25 · 断代与分期 0.2 · 语境保真 0.2 · 反叙事与沉默 0.15 · 校准 0.1 · 清晰 0.1）。`harness standard --domain history` 可跑。

## Outlets · 信息源

史学一手源（档案 · 期刊 · 数据库）见 `reference/outlet-map.md`；中文史籍先看 CNKI / Wanfang（outlets 已核验）；一手档案以档案馆/图书馆登记处（LOC / NARA 类）为起点，检索前读各条的 `not_for`。

## See also · 另见

`../core/04-verification-and-gates.md`（M3.15 分阶段归因）· `../core/05-provenance-and-integrity.md`（M4.13 证据有界）· `../domains/digital-humanities/README.md`（史料数字化与编码）· `../reference/methodology-map.md`（考据与史学方法行）。
