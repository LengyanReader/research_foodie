# Domain · Data Science · 数据科学域
> Wiring `core/` modules into a reproducible, leakage-free experiment pipeline.
> 把 `core/` 模块接线成「可复现、无泄漏」的实验流水线。
**Updated:** 2026-10-12

---

## 中文速览
数据科学域的核心风险是**泄漏**与**不可复现**。它把 `core/` 组合成：**数据集登记表**（M0.5/M4，带哈希与来源）、**不重叠切分**（train/val/test 严格隔离，M0.3）、**三态判定**（pass/fail/uncertain，M3）、**默认失败 + 证据门**（M3）、**实验台账**（M2/M7 可复现）。评测协议与报告模板固定化，让「变好」是可测量的、而不是感觉的（M5 用留出集衡量）。来源：`Sport_Coach/sportscoach/tennis_play/harness/`（`PRINCIPLES.md`、`TESTING.md`、`metrics/METRICS.md`、`reports/{EVAL_PROTOCOL,REPORT_TEMPLATE}.md`、`datasets/build_registry.py`）。

---

## What this domain is for · 用途
Run models/experiments you can *trust and reproduce*: no train/test leakage, every dataset versioned, every result measured against a fixed protocol, every failure surfaced honestly.

## Module combination · 模块组合
- **M4 + M0.5.** Dataset registry: name, version, source, hash, splits. One canonical record; content hashes detect drift.
- **M3 (verification).** Fixed **eval protocol** before experimentation; **default-FAIL** metric gates; **three-state** judging; separate evaluator context.
- **M2 (long-running).** Experiment ledger: config → data hash → seed → metrics → artifact. Resumable, idempotent.
- **M0.1/M0.4.** Never report a metric computed on data the model saw in training; automation scores, humans interpret.
- **M5 (evolution).** Improvements measured on a **holdout**; promote only if the gain generalizes.
- **M7.** Config changes as reviewable diffs; artifacts versioned.

## Patterns · 模式
1. **Dataset registry.** Each dataset: id, source + access date, hash, split definition, license. Non-overlapping splits are enforced, not assumed.
2. **Leakage checks.** Explicit tests for overlap between train/val/test (by row, by entity, by time).
3. **Fixed eval protocol.** Same metrics, same splits, same seeds policy across runs; documented in `EVAL_PROTOCOL`.
4. **Report template.** Every run reports metric ± variance, dataset hash, config, and known limitations.
5. **Three-state judging.** A result may be `pass`/`fail`/`uncertain`; `uncertain` is a legitimate, recorded outcome.

## Anti-patterns
- Train/test leakage (silently inflates metrics).
- Metrics on data the model has seen (M0.1).
- Undocumented splits/config → irreproducible results.
- Cherry-picked seeds or best-of-N reported as the result.
- Promoting "improvements" measured on the tuning set (M5).

## See also
`../core/04-verification-and-gates.md` (M3) · `../core/06-self-evolution.md` (M5, holdout) · `../sources/source-map.md` (data-science row) · `C:\DA_Practice\Sport_Coach\sportscoach\tennis_play\harness\`.
