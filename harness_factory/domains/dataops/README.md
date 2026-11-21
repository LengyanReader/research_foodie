# DataOps · 数据生命周期域

> Wiring `core/` modules into data-lifecycle work: contracts before pipelines, lineage for every value,
> backfills that restate rather than rewrite.
> 把 `core/` 模块接线成「契约先行、血缘可溯、回填重述不重写」的数据生命周期工作流。

**Updated:** 2026-11-21 · **Faculty:** engineering · **Artifact:** dataset · **Grounding:** preferred

---

## 中文速览

DataOps 域让**每一次数据变更是声明过、可检查的事件**：L0 **契约先于管道**（schema、取值范围、时效 SLA）→
L1 血缘图谱（源 → 变换 → 消费方）→ L2 质量检查钉在契约边界（违例即响，M3）→ L3 **回填带日期重述台账**
（绝不静默重写，M0.9）→ L4 时效 SLA 用实测时间戳核验 → L5 质量/血缘作为证据报告，不作保证话术。
域特有风险：**契约后补**（先跑管道再补契约=契约不承重）、**血缘断链**（中间变换不可追溯）、
**静默回填**（改了历史数据不留痕）、**时效口头化**（SLA 没有测量时间戳）。

## Wiring · 接线

| Level | Move | Modules | Gate |
|---|---|---|---|
| L0 | Contract before ingestion | M7 | schema/范围/时效写定 |
| L1 | Map lineage | M4 | 每个值可溯到源 |
| L2 | Quality checks at contract boundaries | M3 | 违例响亮失败 |
| L3 | Backfill = dated restate | M0.9, M7 | 更正条目带日期，非静默 |
| L4 | Freshness SLA verified | M3 | 实测时间戳，非口头 |
| L5 | Report as evidence | M4 | 质量数字带出处 |

## Rubric · 评分

`data/rubrics.json` `dataops`（契约声明 0.25 · 血缘可溯 0.2 · 质量门禁 0.2 · 回填与重述 0.15 · 校准 · 清晰）。
`harness standard --domain dataops` 可跑。

## See also · 另见

`../domains/mlops/README.md`（模型侧生命周期）· `../domains/data-science/README.md`（分析 vs 运营）·
`../core/05-provenance-and-integrity.md`（M4 血缘形态）· `../core/08-change-governance.md`（M0.9 追加式重述）。
