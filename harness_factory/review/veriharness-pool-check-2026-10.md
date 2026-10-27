# VeriHarness release pool · 一手核验报告（P37 dogfood）

> **中文速览。** P38 定位的 VeriHarness 发布池（~26,000 rollouts 留出数据）已按预声明判据完成一手核验：
> **7/7 检查通过**——数据集与代码库真实存在、公开、与论文附录 E 的声明逐项相符（五基准 × 双模型 × 轨迹/交付
> 文件/grader 分）。**一项如实记录的差距**：实际 rollout 总数 **23,197**，比论文摘要的「~26,000」**少 10.8%**
> （同数量级、同 10K–100K 档，但差距不抹平）。许可证为 `other / mixed-upstream-see-readme`（非 blanket CC），
> 使用前须逐项看上游许可。本报告是 P37（dogfood 轮）的交付物：机器判决 receipt 已入轨迹，人工确认可随时覆盖。

**Updated:** 2026-10-28 · **Round:** P37 (dogfood) · **Judge:** machine (预声明 7 项判据，M5.13 纪律) · **Effect score:** 1.0 (7/7)

## 1. What was checked · 判据与结果（预声明于工作前）

| # | check | verdict | evidence |
|---|---|---|---|
| E1 | HF 数据集可达且公开 | **PASS** | `caiqizh/veriharness`: `private:false, gated:false, disabled:false`; sha `214c7081…`; lastModified 2026-09-29 |
| E2 | 五个基准 | **PASS** | 卡片表逐名：APEX-Agents · JobBench · SpreadsheetBench-2 · WorkBuddy-Bench · Workspace-Bench Lite —— 与论文 §4.1 五名完全对应 |
| E3 | 两个模型 | **PASS** | `gemini-3.5-flash` · `claude-opus-4-8`（即 Gemini 3.5 Flash / Claude Opus 4.8，与 M3.17 引用的 6.2/6.4 两模型一致） |
| E4 | 规模 ~26,000 | **PASS（带差距）** | 实测 **23,197 rollouts**（2,330 任务 × ~10；README 表逐行求和）= 摘要「~26,000」的 **−10.8%**，同数量级；差距作为发现记录，不抹平 |
| E5 | 载荷字段 | **PASS** | `index.parquet`（每 rollout 一行：`official_id` · `score`(官方 grader, 0–1) · `trajectory_chars` · `artifact_tar`+`tar_sha256`）· `trajectories/<bench>/<model>.parquet`（渲染全文）· `artifacts/<bench>/<model>/<key>.tar`（交付文件）· `mappings/<bench>.json` |
| E6 | GitHub 代码库 | **PASS** | `google-research/veriharness`：存在、Apache-2.0、org 一致、created 2026-09-23 / pushed 2026-10-02 |
| E7 | 与论文无矛盾 | **PASS（一项差距已记）** | 卡片自述「不含上游基准内容（无题面/工作区/评分细则/答案）· 每 rollout 映射官方 task id」与附录 E 一致；唯一差距即 E4 的 23.2k vs ~26k |

## 2. The honest gaps · 如实记录的差距与注意事项

1. **规模差 10.8%**：23,197 实测 vs 摘要「~26,000」。可能解释（未判定）：论文计入了被发布排除的 rollout
   （`dropped_files.jsonl` / `excluded_rollouts.jsonl` 各存在，README 表有 5 条 excluded），或摘要取整口径
   不同。**用法影响**：作为消融/留出数据时以 23,197 为准，不引用「~26,000」。
2. **许可证非 blanket**：`license: other / mixed-upstream-see-readme`。数据集不含上游内容、但 *衍生使用* 受
   上游五基准各自许可约束——接入本库记分/消融工作流前须逐基准过一遍上游许可（R256 的 CC BY-NC-SA 教训同类）。
3. **本环境的访问路径**：huggingface.co 主站当日对本环境整体不可达（对照组 `/papers` 亦超时；2026-10-27 P35
   实测为 200——主机级、按日变化）；核验经公共镜像 **hf-mirror.com** 完成（同一 Hub API 的读通镜像），GitHub
   为直连。镜像中介是一手性折扣，已如实记录；需要时可从任一可达路径复核 sha。
4. **APEX 的 rollout/任务均值 9.74**（4,658/478）而非整 10——个别任务 rollout 不足十条，作留出集时按
   `index.parquet` 实际行数取数。

## 3. What this unblocks · 解锁了什么

- **D1 阶段 C 的候选素材**：带官方 grader 分的 23k 真实 rollout + 可复现 tar（sha256）——若上游许可放行，
  这是本库消融/留出工作迄今能拿到的最接近「真实任务分布」的数据源。
- **P38「已定位」声明的升级**：从「附录 E 点名」升级为「存在性、公开性、内容结构均一手核验」（本报告）。
- **M5.13 的自用示范**：判据先于工作预声明（7 项，见项目 `tasks/PLAN.md`）、机器可判分、判决入轨迹——本报告
  即该条款在自己身上的第一次完整行使。

## 4. Provenance · 溯源

- 判据预声明：`updates/dogfood/p37-veriharness-pool/tasks/PLAN.md`（工作前写入；未入版本控制）
- 证据原件：`updates/dogfood/p37-veriharness-pool/evidence/`（HF API JSON · README 快照；未入版本控制）
- 访问路径与日期：hf-mirror.com（HF Hub API 镜像）+ api.github.com，均 **2026-10-28**；huggingface.co 主站与
  datasets-server 当日超时（HTTP 000 / connect timeout）
- 论文对照基准：`review/self-modifying-harnesses-2026-10.md` §4（R254 全文核验，P38）
- 轨迹：tool home `updates/traces.jsonl`（`task_outcome`, judge=machine, score=1.0, 7 checks in detail）
