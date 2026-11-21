# MLOps · 模型生命周期域

> Wiring `core/` modules into model-lifecycle work: registry records, serving contracts, drift measured
> against named thresholds, retraining gated on evidence.
> 把 `core/` 模块接线成「注册记录、服务契约、漂移实测、证据门禁重训练」的模型生命周期工作流。

**Updated:** 2026-11-21 · **Faculty:** engineering · **Artifact:** mixed · **Grounding:** preferred

---

## 中文速览

MLOps 域让**每一次模型变更都是受治理、可测量的事件**：L0 注册记录先行（id、版本、训练数据血缘）→
L1 服务契约与流量形态声明 → L2 **漂移实测**（指标与阈值先于监控声明，M3.10）→ L3 **重训练按证据门禁**
（不按排期）→ L4 晋升/回滚带 model id + version 记录（M4.17 的生命周期形态）→ L5 生命周期台账复核。
域特有风险：**按日历重训练**（没有测量就没有门禁）、**注册表事后补记**（记录晚于部署即失去归因）、
**悄悄晋级**（A/B 结果不入台账）、**漂移指标事后挑**（看了数据再定阈值=过拟合的警报线）。

## Wiring · 接线

| Level | Move | Modules | Gate |
|---|---|---|---|
| L0 | Registry record before serving | M7 | id/版本/血缘齐 |
| L1 | Declare serving contract | M7 | 流量形态与回滚点声明 |
| L2 | Drift metrics + thresholds named BEFORE monitoring | M3.10 | 指标+阈值+数据窗口写定 |
| L3 | Retrain on measured drift | M3 | 触发条件 = 实测越线，非排期 |
| L4 | Promotion/rollback recorded | M4.17 | model id + version + 理由入账 |
| L5 | Lifecycle ledger review | M7 | 台账可审计 |

## Rubric · 评分

`data/rubrics.json` `mlops`（注册记录完整 0.25 · 漂移实测 0.2 · 重训练门禁 0.2 · 回滚路径 0.15 · 校准 · 清晰）。
`harness standard --domain mlops` 可跑。

## See also · 另见

`../domains/model-selection/README.md`（选型是一次性决策；生命周期是持续运营）·
`../domains/dataops/README.md`（数据侧生命周期）· `../core/04-verification-and-gates.md`（M3.10 仪器匹配）·
`../core/05-provenance-and-integrity.md`（M4.17 模型即来源）。
