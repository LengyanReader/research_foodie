# Variance protocol · 跨会话/跨模型方差协议（P85.2）

> **中文速览。** 本协议把 BATTERY 的方差工作清单变成**可执行的实验设计**（τ-bench 口径 [R282/R279/R285/R288]）：
> 模型 × 条件 × k 次重复 × 任务集，逐格报 pass^k 与 pass@1 的裂口。**本环境能跑的**：跨会话近似
> （P85 零状态携带采样是下界；真实新会话跑同协议是正式格）；**不能跑的**：跨模型格——单模型沙箱，
> 如实登记为 pending，触发条件 = 第二个模型面可执行时。披露按 M3.16 配置卡 + M4.17 模型轴 + M2.13 档位对齐。

**Updated:** 2026-11-21 · **Round:** P85 · **Anchors:** τ-bench/τ²-bench `[R282]`/`[R283]` · ThinkingBox `[R279]` ·
HAL model×scaffold 习语 `[R288]` · passk.py（C(c,k)/C(n,k) 估计器）

## 1. Design · 设计（因子 × 单元 × 估计器）

| 因子 | 取值 | 说明 |
|---|---|---|
| model | ≥2 个模型面 | **跨模型格**：每个模型一个格 |
| condition | A-bare / B-harness | 双条件，判分口径冻结于运行前（M5.13） |
| repeat | k ≥ 3 独立运行/格 | 真实新会话优先；零状态携带采样为下界 |
| task | battery 中有机判判据的族 | 环境终态 / 隐藏重放套件判分（M3.19） |

**估计器**：逐 (model, condition) 格报 `pass^k = C(c,k)/C(n,k)`（n≥k 才计入）与 `pass@1`；
**裂口**（pass@1 − pass^k）是可靠性主张本身——ThinkingBox 的警示即一枪命中与 k/全对的分裂。

## 2. Disclosure · 披露（三件套，缺一不可）

1. **M3.16 配置卡**：每臂 ETCSOVG 七层卡 + 方差说明（跨 harness/跨模型比较的底线）；
2. **M4.17 模型轴**：每条收据带 `{id, version, surface}`（`harvest --model ID@SURFACE`）；
3. **M2.13 档位对齐**：努力档位是设置不是质量档——格间对齐同档位，或披露档位差异（否则比的是设置）。

## 3. Status · 现状（诚实登记）

| 格 | 状态 | 证据/边界 |
|---|---|---|
| 跨会话（模拟下界） | **已跑** | P85：n=3/臂零状态携带采样，pass^3 bare 0.0 / harness 1.0 |
| 跨会话（真实新会话） | pending | 触发：在独立新会话中跑同一 SPEC（用户起新会话执行即可） |
| 跨模型 | **pending — 本环境不可执行** | 单模型沙箱（mimo-v2.6-pro）；触发：第二个模型面可执行（另一模型的会话/CLI 跑同一批 trial projects） |
| 跨环境 | pending | 触发：第二个执行环境（不同 OS/宿主）跑同协议 |

## 4. Execution handoff · 交接（让跨模型格可被别人跑）

1. 把 `updates/dogfood/p85-citation-xsession/`（SPEC + TASK + corpus + judge）整体交付给第二个模型面；
2. 只跑 B 臂与 A 臂各 k=3（判分器 judge.py 原样，不许改）；
3. 收据写 `task_outcome`（带 model 轴）→ `harness passk --k 3`；
4. 与本协议 §1 表格合并成跨模型格——**比的是同一判分器下的分数，不是感受**。
