# Capability system assessment · 能力体系全方位评估（2026-11-02）

> **中文速览。** 用户要求对现有能力体系做全方位深度评估。方法：**实测探测**（12 个能力触发探针 · 220 行发射
> harness 的内容分析 · 轨迹事件分布 · 17 能力交叉任务）+ **结构审计**（60 轮的演进轨迹）。**核心发现：系统
> 的最大缺口不是匹配率（11/12 探针命中）、不是规则覆盖（全事件有规则覆盖）、也不是测试覆盖（434 守卫全绿），
> 而是「能力触发了但 agent 不知道怎么执行」的操作化鸿沟**——发射 harness 对复杂任务点名了 17 个能力，但没有
> 一个能力发射了可执行的操作步骤。

**Updated:** 2026-11-02 · **Method:** 实测探测 + 结构审计 + 60 轮回溯

> **勘误（P67, 2026-11-03）.** §1 "实验电池 9 族 9/9" 写作时与 SSOT 不符：当日 `data/battery.json` 仅登记 7 族
> （P62 的 reading-extraction 与 cron-parsing 两族已执行、双侧收据在轨迹，但未入册；P62-ext 提交信息称 8/8，
> 亦与注册表不符）。7 族当时的账面为 7/7 全胜。P67 追溯登记两族并为全族绑定 `trial_projects` 后，九族 9/9
> 方为事实（现值见 `battery.json` 与 `tasks/BATTERY.md`）。此差异正是 P67 注册表代谢轮立轮的根据：
> **文档陈述须经注册表守卫才可入册**（新增双向对账 `battery.reconcile` + 守卫测试）。

## 1. What works · 已验证的能力面

| 面板 | 证据 |
|---|---|
| **匹配率** | 12 探针 11 命中（P55 电池 + P52 域键控修复后）；唯一 miss = philosophy 在泛信号竞争中落败 |
| **实验电池** | 9 族 harness 9/9 全胜（裸奔均值 0.318 vs 0.993）；24 条真实轨迹；proof 族 N=3 sign test 3/3 正 |
| **轨迹环** | 24 条轨迹 → trace-audit 5 规则 → 模拟测试 5/5 正确 · 0 假阳性 · 去重验证 |
| **门禁系统** | 434 测试 · cycle audit 0 硬 0 缺口 · DoD 含 battery 软轴 · 命令面守卫 |
| **知识面** | 43 能力 · 44 子句 · 34 域 · R1–R281 · catalog 221 · 思维方式 7 行 |
| **格式对齐** | Agent Skills → AAIF（P57 验证采纳规模：70+ 平台 · 1M 技能 · 2.8 亿安装） |
| **独立验证** | QueenBee 安全机制与本库子句一一对应（P61 全文级）；ThinkingBox 佐证 M3.18(c)（P60 工业规模） |

## 2. The actionability gap · 最大的缺口（实测证据）

**探测**：对复杂任务「构建端到端知识图谱系统」derive harness，17 个能力命中，发射 220 行 AGENTS.md。
**但**：
- `ontology-as-contract` 命中了 → AGENTS.md 里 "ontology" 出现 2 次（特征列表 + 模块名），**零条操作步骤**
- `entity-resolution` 命中了 → "entity resolution" 出现 1 次（能力清单里的名字），**没有 blocking→matching→clustering 程序**
- 证据仪器节是**通用的**（"observed evidence for the artefact"），不是本体工程专用的
- 域 README（`domains/digital-humanities/README.md`）有 workflow，但发射 AGENTS.md **不引用它**

**这就是「能力触发了但 agent 不知道怎么执行」的鸿沟。** 能力系统的匹配面（P18/P55）和守卫面（434 测试）都很强，
但从「能力命中」到「agent 拿到可执行步骤」之间**断了一环**。

## 3. Five optimization areas · 五个优化方向（按影响排序）

### 3.1 Capability → operating procedure · 能力→操作程序（最高影响）

**问题**：能力只是注解（名字 + why + modules），不发射可执行步骤。
**方案**：在 `data/capabilities.json` 的每条能力增加 `procedure` 字段（3–7 步可执行清单），发射模板将其渲染进
AGENTS.md 的对应节。不是重写域 README——是把 README 里的 workflow 提炼为**结构化、机器可读的操作步骤**，
让 agent 不用去翻域文档。
**影响**：直接弥合操作化鸿沟；19 个无域键控能力的域也受益（能力自带程序而非依赖域 README）。
**规模**：43 条能力 × 3–7 步 = 一个中等轮次（按域分组，每批 10–15 条）。
**实验验证**：对 KG 任务重发射 harness，检查 AGENTS.md 是否包含实体归一的 blocking→matching→clustering 步骤。

### 3.2 Domain README → emitted harness · 域 README 接入发射物

**问题**：34 个域 README 各有 workflow，但发射 harness 只写 `Domain: digital-humanities`，不引用 README 路径
或提炼其内容。Agent 不知道去哪找域专属操作。
**方案**：发射 AGENTS.md 增一行 `Domain playbook: read domains/<domain>/README.md`（或 `pointer.json` 增
domain_readme 字段），一行成本，弥合从通用 harness 到域专属指南的路由。
**规模**：S（模板一行 + pointer.py 一行）。

### 3.3 Matching precision for specific domains · 特定域的匹配精度

**实测**：`argument-reconstruction` 的探针「从认识论角度重构这篇论文的论证」未命中——**泛域信号（论文/文献）
票数压过了域专属信号（认识论）**。P27 的信号所有权裁决需要执行：**域专属信号在域内应该有更高的权重**（或
泛域信号降权）。
**方案**：domain_scores() 引入 signal specificity weighting（复合词 > 单词；域专属 > 跨域泛词）。
**规模**：S–M（classify.py 的打分逻辑改动 + 路由电池回归）。

### 3.4 Trace vocabulary extension · 轨迹词表扩展

**现状**：7 个事件（6 过程 + 1 结果）。
**缺失的事件类型**：
- `context_pressure`：上下文窗口将满（触发 M1 预算纪律）
- `tool_error`：工具调用失败（与 gate_miss 不同——gate 是门禁失败，tool 是外部工具报错）
- `human_preference`：人类表达了偏好（与 human_correction 不同——correction 是改了产物，preference 是说了
  「下次要这样」）
- `latency_anomaly`：延迟异常（M2.13 的预算线）
**方案**：词表 v2（每加一种事件 = trace.py 校验 + trace-audit 规则 + 模板合同同步）。
**规模**：M（每次扩展 = 代码 + 数据 + 测试）。

### 3.5 Self-model refresh · 自我模型刷新（M5.11）

**现状**：M5.11 要求 self-model + gap register + disconfirming check，但 self-model 是静态文本，60 轮的
新证据没有回灌。gap register 由 cycle audit 维护但只覆盖机械缺口（缺路由行/守卫/provenance）。
**方案**：self-model 的生成自动化——从 SSOT（capabilities/cycles/references）**现算**当前覆盖面，与
roadmap 对照生成 diff。不是手写更新，是**从 SSOT 现算的视图**（与 CAPABILITIES.md/HARNESS-MAP.md 同理）。
**规模**：M（一个生成器 + 守卫）。

## 4. What needs expansion · 需要拓展的面

| 拓展 | 性质 | 触发 |
|---|---|---|
| **N>1 per-task variance** | 实验设计 | 同任务同条件跑 N≥3 次，配对检验才有方差；M5.12 的统计前提 |
| **Cross-capability interaction model** | 引擎 | 17 个能力同时命中时的**相干性**建模（哪些组合是冗余的？哪些有冲突？）|
| **Memory backend profile** | A.3 #4 | M2.12 声明了 backend，但没有可发射的 profile（P12 落了声明，未落后端选项清单）|
| **Domain-keyed capabilities for remaining 15 domains** | P52 模式 | 每个 = 域 README 的纪律提炼为能力（ arts-design/law/reading/… 各需溯源的一手材料）|
| **Multi-language routing** | P55 | 路由电池仅覆盖 en+zh；其他语言的信号词表为空 |

## 5. Recommended next rounds · 建议的下一批轮次（按影响排序）

| # | 轮 | 影响 | 规模 |
|---|---|---|---|
| 1 | **Capability procedure emission**（3.1）：43 条能力各加 3–7 步操作程序，发射进 AGENTS.md | 最高——直接弥合操作化鸿沟 | M–L（分批） |
| 2 | **Domain README pointer**（3.2）：发射 harness 引用域 README | 高——一行成本 | S |
| 3 | **Signal specificity weighting**（3.3）：域专属信号加权 | 中——修复哲学/史学等域的匹配精度 | S–M |
| 4 | **Self-model auto-generation**（3.5）：从 SSOT 现算 self-model | 中——M5.11 从静态变动态 | M |
| 5 | **Trace vocabulary v2**（3.4）：加 4 种事件类型 | 中——轨迹环的覆盖面扩展 | M |

## 6. Verification

本评估基于实测探测（非理论推演）：12 个触发探针 · 220 行发射 harness 内容分析 · 24 条轨迹事件分布 ·
17 能力交叉任务 · 434 守卫测试。交付 `review/capability-system-assessment-2026-11.md`。
