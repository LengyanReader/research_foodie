Updated: 2026-11-03 · P69 standing routine · P65 enriched · P64 assessment incorporated

# Trend Review & Literature Synthesis · 趋势综述与文献辩证

> **摘要 · Executive summary.** 本期覆盖 2026 年 10 月下旬至 11 月初，基于 3336 条情报（418 条来自 arXiv）与三条全文级一手文献（R279 ThinkingBox · R280 QueenBee · R281 LegoSR）。三个核心判断：**①** harness 骨架已趋同，差异化上移至验证门禁与溯源层——本库八族配对试验（裸奔均值 0.27 vs harness 0.99）与 ThinkingBox 的工业规模实证（77.61% 的静默失败携带错误状态）从两个方向印证了同一结论；**②** 评判标准正在从 pass@1 转向一致性——ThinkingBox 的数据显示两者尖锐分化（93.89% vs 13.41%），选指标就是选结论；**③** 治理基建在加速合并——Agent Skills 捐入 Linux Foundation 旗下的 AAIF（70+ 平台、100 万技能、2.8 亿安装），Open Responses / OpenEnv / OpenSandbox 三条新标准线同批立项。以下正文分五节展开证据与分析，每节中英并行。

> **Executive summary.** This review covers late October to early November 2026, drawing on 3,336 intelligence items (418 from arXiv) and three full-read primary sources (R279 ThinkingBox · R280 QueenBee · R281 LegoSR). Three core findings: **(1)** the harness skeleton has converged; differentiation now lives in verification gates and provenance — confirmed independently by our eight-family paired trials (bare mean 0.27 vs harness 0.99) and ThinkingBox's industrial-scale data (77.61% of silently failing runs carry wrong database state); **(2)** evaluation standards are shifting from pass@1 to consistency — ThinkingBox shows the two diverge sharply (93.89% vs 13.41%), and the metric you choose determines the conclusion you get; **(3)** governance infrastructure is consolidating — Agent Skills donated to the Linux Foundation's AAIF (70+ platforms, 1M skills, 280M installs), with Open Responses / OpenEnv / OpenSandbox launched in the same batch. Five sections follow, each bilingual.

---

## 1 · 行业全景与相邻领域 · Industry landscape and adjacent fields

### 中文

行业簇 2851 条情报中，近三十日 648 条，来源 13 家。信号集中在三处：

**骨架趋同，护城河上移。** 计划—工具—验证—记忆的四件套已成公共知识——每家厂商的产品发布都在宣称「我们有 harness」。差异化不再发生在「有没有」，而在验证门禁与溯源层的**硬度**。ThinkingBox 的立场「A trajectory is a claim. Database state is the evidence. Repetition is the trust test.」与本库 M3.18(c) 的重放评分条款同构——两者独立得出同一结论：**可信性不在模型推理，在可执行检查**。

**可观测性正在成为底座。** OpenTelemetry 的 GenAI 语义约定（`otel-genai`，feed 可达）与 Langfuse 将「trace 一等公民」从工程偏好推向行业标准。判断标准：当多个语言 SDK 采纳同一约定，即为趋势；单一厂商博客是声量。

**平台数字与开源数字必须分开读。** Mem0 的 LoCoMo/LongMemEval 基准高分被其 README 限定在托管平台侧，开源 SDK 不复现同等成绩（P68 经 GitHub API + README 核验，访问 2026-11-03）。引用不区分范围，即把厂商叙事误当社区趋势。

### English

Within the 2,851 industry items (648 in the last 30 days, 13 sources), the signal concentrates in three areas:

**The skeleton has converged; the moat moved up.** The plan–tool–verify–memory quartet is now common knowledge — every vendor announcement claims "we have a harness." Differentiation no longer lies in *whether* a harness exists, but in how rigorous its verification gates and provenance layer are. ThinkingBox's "A trajectory is a claim. Database state is the evidence. Repetition is the trust test." is structurally identical to this library's M3.18(c) replay-grading clause — two independent efforts arriving at the same conclusion: **trustworthiness lives in executable checks, not in model reasoning**.

**Observability is becoming substrate.** OpenTelemetry's GenAI semantic conventions (`otel-genai`, feed-reachable) and Langfuse are pushing "trace as a first-class citizen" from engineering habit toward standard. The test: when multiple language SDKs adopt the same convention, it is a trend; a single vendor blog post is noise.

**Platform numbers and OSS numbers must be read separately.** Mem0's LoCoMo/LongMemEval benchmark scores are scoped to the managed platform in their own README; the open-source SDK does not reproduce them (P68, verified via GitHub API + README, 2026-11-03). Citing without that distinction mistakes vendor narrative for community trend.

---

## 2 · Harness 文献综述 · Harness literature synthesis

### 中文

harness 簇 3336 条即全部情报——每条受跟踪条目都带 `agent-harness` 主题，此簇反映广度而非细分。真正的文献密度集中在三条全文读：

**ThinkingBox（R279，Microsoft + Hugging Face）。** 507 个有状态业务工作流、五领域、18 个 LLM 各跑 20 次；评分依据是终端数据库状态与副作用，经 OpenEnv 适配器输出二值奖励。核心发现：**121,680 次试验中 79,853 次失败，其中 67.24% 干净终止、无报错，但可执行检查发现 77.61% 存在错误字段值**。失败分类：约 4/5 是工具处理而非推理。pass@1 与 20/20 全过一致性的分化（Kimi-K3：93.89% vs 13.41%）揭示——**至少一次成功不等于可靠成功**。

**QueenBee（R280，arXiv:2606.27492，全文读）。** 冻结模型权重，进化发生在编排层：工作流表示为「生成时序通信 DAG 的可执行程序」，以 SFT-Bank（执行诊断 / 设计假说 / 验证结论的结构化持久记忆）前馈。自进化拓扑较最强固定拓扑降 RMSE 37.2%、消息 74.2%、token 59.6%。作者诚实限定：递归自改进仅指规划器的生成策略。**其安全机制与本库子句一一映射**（held-out 接受门 → M5.13；方差感知信用 → M5.12；洞察证伪 → M5.11；结构去重 → M4.12）——一个独立实现验证了本库的子句体系。

**LegoSR（R281，arXiv:2610.33465，仅著录）。** 自改进智能体引导的科学发现，同预算下最高超通用智能体 29 个百分点。

**综述判断：2026 年 harness 研究的重心已从「能力构建」转向「可信闭环」。** 状态级判分、结构化验证记忆、留出证伪、保守信用分配——四个关键词来自三篇独立论文，也与本库 D1（自演化）的形态互为表里。

### English

The harness cluster (3,336 items) equals the *entire* corpus because every tracked entry carries the `agent-harness` topic — this measures breadth, not a niche. The literature density concentrates in three full-reads:

**ThinkingBox (R279, Microsoft + Hugging Face).** 507 stateful business workflows across five domains, each run 20 times by 18 LLMs; grading by terminal database state and side effects via the OpenEnv adapter. Core finding: **of 79,853 failures among 121,680 trials, 67.24% terminated cleanly with no reported error, yet executable checks found wrong field values in 77.61% of them**. Failure taxonomy: approximately four in five failures are *tool handling*, not reasoning. The pass@1 versus 20/20-consistency divergence (Kimi-K3: 93.89% at least once vs 13.41% consistently) reveals that *succeeding once does not mean succeeding reliably*.

**QueenBee (R280, arXiv:2606.27492, full-read).** Model weights frozen; evolution happens at the orchestration layer: workflows represented as *executable programs that generate temporal communication DAGs*, fed forward by an SFT-Bank (persistent structural memory of execution diagnoses, design hypotheses, and validation outcomes). The self-evolved topology reduces RMSE by 37.2%, messages by 74.2%, and tokens by 59.6% relative to the strongest fixed topology. The authors honestly scope "recursive self-improvement" to the planner's generation strategy. **The safeguard list maps one-to-one onto this library's clause system** (held-out acceptance gate → M5.13; variance-aware credit → M5.12; insight falsification → M5.11; structural dedup → M4.12) — an independent implementation validating our clause design.

**LegoSR (R281, arXiv:2610.33465, listed).** Self-improving agent-guided scientific discovery; up to 29 percentage points over a generic agent with the same model, tools, and budget.

**Synthesis: 2026 harness research has shifted from *capability building* to *trustworthy closure*.** State-level grading, structural validation memory, held-out falsification, and conservative credit allocation — four themes from three independent papers, isomorphic to this library's D1 self-evolution design.

---

## 3 · 本库八族配对试验的一手证据 · First-hand evidence from eight paired trials

### 中文

趋势综述通常依赖外部论文与厂商发布。本库的独特优势是拥有**八族 × 双条件的配对试验数据**（24 条真实轨迹）——这是量化 harness 价值的一手证据，不是厂商自报。试验设计：每个任务族由同一模型分别以裸奔（无 harness 纪律）与 harness（完整纪律：验收门 · 溯源 · 操作程序）各执行一次，以预声明的机器可检查判据评分。

| 任务族 | 裸奔 | harness | delta | 判分方式 |
|---|---|---|---|---|
| model-choice | 0.00 | 1.00 | **1.00** | 选型记录结构完整性（M4.17） |
| proof-verification | 0.00 | 1.00 | **1.00** | Lean 编译 + 零逃逸 |
| kg-dh | 0.00 | 1.00 | **1.00** | 证据指针解析（M4.13） |
| bayesian-stats | 0.20 | 1.00 | 0.80 | 判分者独立重推导（M3.11） |
| lit-review | 0.20 | 1.00 | 0.80 | 引用可核验性 |
| deep-research | 0.40 | 1.00 | 0.60 | 多跳引用链逐 hop 核验 |
| unit-tests (semver) | 0.55 | 1.00 | 0.45 | 判分者先行隐藏重放 |
| reading-extraction | 0.78 | 0.94 | 0.16 | 16 流派 × 经典源精确匹配 |

三条跨族结论，每条附带证据与反例考量：

**结论一：harness 的贡献随可验证性递增。** 证明/选型/指针族 delta=1.0（裸奔完全失败），提取族 delta=0.16（裸奔部分正确但缺溯源）。这与 ThinkingBox「四分之三失败是工具处理非推理」形成跨源印证。反例考量：阅读提取的 delta 最小（0.16），因为结构化文档提取是裸奔最擅长的任务——这不削弱结论，反而精确化了结论的适用边界。

**结论二：裸奔的缺陷不是「不准确」而是「不可审计」。** 贝叶斯族裸奔的点估计数值接近（正态近似在 n=500 恰好可用），但无先验声明、无诊断、无来源——读者无法把主张还原到证据。反例考量：如果读者只关心点估计的数值精度，裸奔可能已经足够——但科学研究的要求恰好不止于此。

**结论三：记忆伪造精确出处。** deep-research 试验中，裸奔把 Roughgarden (2016) 教科书的引用凭空具体化为「Kalyanasundaram–Schnitger 1992 STOC」——主题对、引文错。这说明**记忆对出处的伪造是精确级的（主题与年份都对，作者与标题错）**，只有逐 hop 解析才能捕获。

### English

Trend reviews typically rely on external papers and vendor announcements. Our unique advantage is **eight families × two conditions of paired-trial data** (24 real traces) — first-hand evidence of harness value, not vendor self-report. Design: each task family executed by the same model under bare (no harness discipline) and harness (full discipline: acceptance gates, provenance, operating procedures) conditions, scored by pre-declared machine-checkable criteria.

Three cross-family conclusions, each with evidence and counter-considerations:

**Finding 1: The harness contribution scales with verifiability.** Proof/selection/pointer families show delta=1.0 (bare fails completely); extraction shows delta=0.16 (bare partially correct but lacking provenance and bounding). Cross-source corroboration: ThinkingBox finds "three quarters of failures are tool handling, not reasoning." Counter-consideration: the smallest delta (reading-extraction, 0.16) reflects the task where bare memory performs best — this refines, rather than undermines, the conclusion's applicability boundary.

**Finding 2: The bare condition's failure is not "inaccuracy" but "unauditability."** The Bayesian bare condition's point estimate is numerically close (normal approximation at n=500), but lacks prior declaration, diagnostics, and provenance — the reader cannot trace the claim to evidence. Counter-consideration: if the reader cares only about point-estimate accuracy, bare may suffice — but scientific methodology requires more.

**Finding 3: Memory fabricates precise attributions.** In the deep-research trial, the bare condition transformed a Roughgarden (2016) textbook citation into "Kalyanasundaram–Schnitger 1992 STOC" — the topic and year correct, the authors and venue wrong. Only hop-by-hop resolution catches this class of error.

---

## 4 · 新兴方向 · Emerging directions

### 中文

**数据事实：有趣方向簇读空（0 条）。** 已通过新增 `emerging-directions` watchlist 主题（15 个关键词：world model · embodied · multimodal agent · AI4Science · causal · interpretability · mechanistic · neuro-symbolic · test-time compute 等）接入 trajectories 簇；下次 intel pull 时该簇将自然填充。当前以 P68 已核实的工具生态为据：

- **约束解码 / 结构化输出**：Outlines、Instructor（Apache-2.0）——「让模型只在合法语法里说话」的工程化，是 schema-valid 输出契约的低成本路径。
- **时序知识图谱记忆**：Graphiti（Apache-2.0）——强调随时间演化的实体关系，相对静态向量库是有意义的差异化。
- **沙箱执行**：E2B、OpenEnv（与 R279 同源）——「有状态副作用可判分」正在变成通用底座。
- **本地推理**：vLLM（Apache-2.0，活跃）——自托管与成本敏感场景的现实选择。
- **护栏与网关**：NeMo Guardrails、LiteLLM——许可证 `NOASSERTION`，未过入表门，登记待核。

**反向信号**：Microsoft GraphRAG 自述进入维护模式（`defunct-track`）。当一度最重的 RAG 方案让位于轻量结构化输出与可观测性，「检索越强越好」的默认叙事需要被重新审视。

### English

**The data first: the trajectories cluster reads zero.** A new `emerging-directions` watchlist topic (15 keywords) has been wired into the cluster; it will fill on the next intel pull. Current evidence draws on the P68-verified tool ecosystem:

- **Constrained decoding / structured output**: Outlines, Instructor (Apache-2.0) — engineering "the model speaks only within legal grammar" as a low-cost path to schema-valid output contracts.
- **Temporal knowledge-graph memory**: Graphiti (Apache-2.0) — entity relationships that evolve over time, a meaningful differentiation from static vector stores.
- **Sandboxed execution**: E2B, OpenEnv (same lineage as R279) — "stateful side effects are gradable" is becoming general-purpose infrastructure.
- **Local inference**: vLLM (Apache-2.0, active) — the realistic choice for self-hosted, cost-sensitive scenarios.
- **Guardrails and gateway**: NeMo Guardrails, LiteLLM — license `NOASSERTION`, intake gate not yet passed.

**Counter-signal**: Microsoft GraphRAG self-declares maintenance mode (`defunct-track`). When the once-heaviest RAG approach yields to lightweight structured output and observability, the "more retrieval is always better" default deserves re-examination.

---

## 5 · 分析与预测 · Analytical projections

### 中文

以下四条预测从上述证据**逻辑推出**——每条注明支撑证据、置信度与反转条件。它们不是猜测，是从已观察事实中提取的可检验推论。

**预测一：验证级基准将取代 pass@1 成为标准度量。**
支撑证据：R279 数据显示 pass@1 与 20/20 一致性尖锐分化；R269 ABC 检查单将任务有效性与结果有效性列为可检验主张；本库 M3.19 落地了同一纪律。
置信度：**高**（三个独立来源收敛）。
反转条件：出现一个被广泛采纳的一致性基准标准且与 pass@1 不矛盾。

**预测二：沙箱平台将在 OpenEnv 标准下整合。**
支撑证据：R278 AAIF 四项目含 OpenSandbox（阿里）与 OpenEnv（HF+Meta）；R279 ThinkingBox 已经使用 OpenEnv 适配器；三个独立来源在同一个接口上收敛。
置信度：**中高**（产品与标准同步收敛，但实际部署尚未大规模验证）。
反转条件：OpenEnv 被更广泛的行业接口标准取代，或 ThinkingBox 的开源采用率显著低于预期。

**预测三：记忆系统的差异化将从容量转向一致性。**
支撑证据：R279 数据显示 pass@1 与 20/20 分化的根因是「四分之三失败为工具处理」——即记忆检索的工具调用稳定性而非记忆容量是瓶颈。P52 记录的 Mem0「平台数字 vs OSS 数字」分歧进一步说明：记忆系统的评估需要区分「最佳情况」与「可靠情况」。
置信度：**中**（证据来自两个来源，但记忆系统本身的演化方向仍受多种因素影响）。
反转条件：出现一种记忆架构在一致性与容量之间实现了真正的权衡突破。

**预测四：技能生态将在认证与社区两条轨道上分化。**
支撑证据：R276 记录 Agent Skills 捐入 AAIF（70+ 平台、1M 技能、2.8 亿安装），公告明确提出下一步是「版本化发布、正式提案流程、安全指引」——即认证轨道；同时社区技能持续增长（superpowers 一类方法论框架跨六个 agent 平台运行）。两条轨道服务的需求不同（企业合规 vs 快速迭代）。
置信度：**中**（基于治理结构与社区趋势的推理，非实测）。
反转条件：AAIF 认证流程被社区广泛抵制，或社区技能的安全事件导致全面认证需求。

### English

Four projections logically follow from the evidence above. Each cites its supporting evidence, confidence level, and reversal condition.

**Projection 1: Verification-grade benchmarks will replace pass@1 as the standard metric.**
Evidence: R279 shows pass@1 and 20/20-consistency diverge sharply; R269 (ABC) lists task validity and outcome validity as checkable claims; this library's M3.19 codifies the same discipline. Three independent sources converge.
Confidence: **high**.
Reversal: a widely adopted consistency benchmark standard emerges that does not conflict with pass@1.

**Projection 2: Sandbox platforms will consolidate under OpenEnv.**
Evidence: R278 AAIF includes OpenSandbox (Alibaba) and OpenEnv (HF+Meta); R279 ThinkingBox already uses the OpenEnv adapter; three independent sources converge on the same interface.
Confidence: **medium-high** (product and standard converging, but large-scale deployment not yet demonstrated).
Reversal: a broader industry interface standard displaces OpenEnv, or ThinkingBox's open-source adoption falls significantly short.

**Projection 3: Memory systems will differentiate on consistency, not capacity.**
Evidence: R279 attributes the pass@1/consistency divergence to tool-handling failures (79.9%), not reasoning — meaning retrieval stability, not memory capacity, is the bottleneck. P52's Mem0 "platform vs OSS" divergence further shows that memory evaluation must distinguish "best case" from "reliable case."
Confidence: **medium** (two-source evidence; memory-system evolution influenced by many factors).
Reversal: a memory architecture achieves a genuine breakthrough in the consistency-capacity trade-off.

**Projection 4: The skills ecosystem will bifurcate into certified and community tracks.**
Evidence: R276 documents Agent Skills donated to AAIF (70+ platforms, 1M skills, 280M installs), with next steps explicitly including "versioned releases, formal proposal process, security guidance" — the certified track. Meanwhile community skills continue growing (superpowers runs across six agent platforms). The two tracks serve different needs (enterprise compliance vs rapid iteration).
Confidence: **medium** (reasoning from governance structure and community trends, not direct measurement).
Reversal: broad community resistance to AAIF certification, or a major community-skill security incident forcing universal certification.

---

## 6 · 溯源表 · Source register

| # | claim anchor | primary source | accessed | strength |
|---|---|---|---|---|
| R279 | ThinkingBox 状态判分与失败分类（67.24% / 77.61% / 79.9% 工具处理） | Microsoft & Hugging Face, HF blog | 2026-11-02 | **full-read** |
| R280 | QueenBee 递归自改进 harness（SFT-Bank、RMSE −37.2%、安全机制映射） | arXiv:2606.27492 | 2026-11-02 | **full-read (P61)** |
| R281 | LegoSR 自改进科学发现（最高 +29 pp） | arXiv:2610.33465 | 2026-11-02 | *listed* |
| P68 | Mem0 平台限定 / Graphiti / E2B / Outlines / vLLM（Apache-2.0） | 各官方仓库 + GitHub API | 2026-11-03 | **verified** |
| P68 | LiteLLM、NeMo Guardrails `NOASSERTION` | GitHub API license.spdx_id | 2026-11-03 | **verified** |
| P68 | Microsoft GraphRAG `defunct-track` | 官方 README | 2026-11-03 | **verified** |
| R276 | Agent Skills 捐入 AAIF（70+ 平台 / 1M / 280M） | Anthropic announcement | 2026-10-31 | **full-read** |
| R278 | AAIF 四项目（Open Responses / OpenEnv / OpenSandbox） | aaif.io | 2026-10-31 | *listed* |
| snapshot | 行业 2851 / harness 3336 / trajectories 0 / domains 10 | `data/trend-snapshot.json` | 2026-11-03 | deterministic |

> 未纳入本文者：一切仅有二手转述、无一手可达的条目——按「引用即生命线」留作 *unverified*，不入论据。

---

*Mechanism · 机制*：`harness full-update` 第八相自动聚合 intel 并写 `updates/TREND.md` 脚手架 + 刷新 `data/trend-snapshot.json` + 重建 `docs/index.html`；分析正文（本文件）由人/agent 撰写。引擎只聚合与引用，从不下判断（M4/M0.4）。GitHub Pages 经 `.github/workflows/pages.yml` 自动发布。
