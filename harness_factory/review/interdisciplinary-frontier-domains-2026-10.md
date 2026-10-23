# Interdisciplinary & frontier domains · 跨学科与前沿域检视（P29）

> **中文速览。** 用户问：跨学科/超学科与前沿域能否整合？检视结论按 M0.5 判据（域 = 能改变路由/门禁内容才入）
> 分四类：**组合即覆盖**（多数跨学科任务按「工作性质」分类已覆盖，不新开域）· **信号修复**（2 处实测误路由，
> data-only 修掉）· **落 1 个真前沿域** `ai-safety`（判别力足：安全论证有独特的门禁结构）· **推迟 3 个**
> （interpretability / embodied / systems-science，各带重访触发）。**同时装上自动发现机制** `harness probe-domains`：
> 已采集的情报中匹配不到任何域信号的条目自动聚类成候选域提案（提案制，M0.4）——未提到的域从此会**自己浮出来**。

**Updated:** 2026-10-23 · **Round:** P29 · **Method:** 12 个跨学科/前沿任务实测 classify+derive（2026-10-23），
判据先行。

## 1. Empirical table · 实测表（12 任务）

| task | classified | verdict |
|---|---|---|
| urban heat islands + satellite | general（10 能力） | **信号修复**：earth-environment 补 `satellite`/`urban climate`/`遥感` |
| complex networks / power grids | data-science | **组合即覆盖**（方法=建模，域=数据工作；无需新域） |
| system dynamics city food | data-science | **组合即覆盖**（systems-science 是方法不是工作性质；推迟，见 §3） |
| single-cell RNA-seq pipeline | **devops** ✗ | **信号修复**：biology 补 `rna-seq`/`single-cell`/`transcriptomic`（"pipeline" 误命中是 P18 类缺陷） |
| agent alignment eval | data-science | **落域**：`ai-safety`——安全论证的门禁结构（L0–L5 + rubric）判别力足 |
| HCI voice interfaces for elderly | arts-design | **组合即覆盖**（设计+心理学方法；不新开域） |
| transformer circuit interpretability | **devops** ✗ | **推迟**：interpretability 是前沿工作性质（机理定位、可证伪性）——见 §3 |
| neuro-symbolic legal reasoner | law（17 能力） | **组合即覆盖**（法律工作用形式方法；features 组合已表达） |
| STS analysis of LLM adoption | general | **组合即覆盖**（人文+社科方法；STS 是研究纲领不是工作性质） |
| futures scenario planning AGI policy | social-science | **组合即覆盖** |
| embodied household manipulation | general（10） | **推迟**：embodied 触底 general——见 §3 |
| climate attribution heatwave | earth-environment ✓ | **已覆盖** |

## 2. Landed · 落地

- **`ai-safety` 域**（faculty meta）：workflow L0–L5（安全属性/威胁模型 → 能力实测 M3.10 → 红队留痕 M3.15 →
  逐条安全论证 M4.13/M4.16 → 按 M3.16 披露卡自审 → 残余风险显式）；rubric 六维（安全论证结构 0.25 · 红队覆盖
  0.2 · 能力实测 0.2 · 残余风险坦诚 0.15 · 校准 · 清晰）；README 点名域特有风险（把「没测出」写成「没有」·
  单向论证 · M4.17 静默换模型 · M3.16 披露不完整）。
- **信号修复（data-only）**：biology +3（rna-seq/single-cell/transcriptomic）、earth-environment +3
  （satellite/urban climate/遥感）——修掉 2 处实测误路由。

## 3. Deferred with triggers · 推迟并记重访触发

| 候选 | 理由 | 重访触发 |
|---|---|---|
| `interpretability` | 前沿工作性质（机理定位、可证伪的机制主张）判别力足，但信号面太窄（"circuit" 已被 engineering 占用，需专属信号集 + rubric 设计） | probe-domains 连续两轮浮出 interpretability 簇，或出现第二例误路由 |
| `embodied` | 触底 general；工作性质 = 工程+物理+实时控制，信号（manipulation/locomotion）尚未验证判别力 | probe-domains 浮出 embodied 簇时 |
| `systems-science` | 是方法不是工作性质（系统动力学是 statistics/engineering 的建模工具），M0.5 不判别 | 出现「系统动力学建模」任务族落错域 |

## 4. The automated finder · 自动发现机制（本轮的机制性答案）

`harness probe-domains [--root DIR] [--no-write] [--json]`：
1. 读 `updates/intel.jsonl`（`harness intel` 的产出，人跑拉取、离线分析）；
2. 对每条做 classify+derive，落在 `general` 或能力底线（≤10）的判为 **unmapped**；
3. unmapped 条目按**共享关键词**聚类（排除停用词与已有域信号），每簇附最近的既有域（= 最便宜的信号修复方案）；
4. 产出提案到 `updates/DOMAIN-PROBES.md`——**只提案**（M0.4/M0.8）：簇是否够格开域由人按 M0.5 判据裁决。

与既有机制的分工：`refresh`/`intel` 拉**已知主题**，`probe-domains` 找**未知簇**，`evolve` 审**目录健康**——
三个半环合起来就是「自动发现 → 提案 → 人裁决」的完整回路。守卫：`tests/test_domain_probe.py` 4 用例
（空情报静默 · unmapped 簇浮现且不带 mapped 项 · 全映射零提案 · emit 只写报告不碰 SSOT）。

## 5. Verification

`python -m unittest discover -s tests` → **334 OK**（+4）；`cycle audit` → **25 轮 · 0 硬 · 0 缺口**；
`catalog --write` 重生成（34 域同步）；P18 32 族回归全过（新信号未扰动既有族）。
