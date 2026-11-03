Updated: 2026-11-03 · P69 worked instance of the standing routine work

# Trend Review & Literature Synthesis · 趋势综述与文献辩证

> **中文速览** — 本文件是「例行工作」每次更新后应产出的**分析正文**（脚手架由 `harness trend` 生成，见 `updates/TREND.md`；可视化见 `docs/index.html`）。分三部分：①AI 全行业与相邻领域趋势，②harness 方向文献综述，③其他有趣且有潜力方向的梳理。三节各附**前沿辩证**（区分「趋势」与「声量」）。凡事实性声明一律回一手源，标注访问日期与核验强度（全文读 / 仅著录 / 厂商自报 / 未核）。数据面截至快照 2026-11-03（intel 3336 条，行业簇 2851、harness 簇 3336、有趣方向簇 0、学科簇 10；近三十日动量见括注）。

> **EN summary** — This is the *authored body* the P69 routine produces after every full-update (the scaffold is `updates/TREND.md`; the visual face is `docs/index.html`). Three parts: (1) AI-industry & adjacent-field trends, (2) a harness-direction literature review, (3) other promising directions — each with a dialectical reading that separates signal from noise. Every factual claim resolves to a primary source with an access date and a verification strength (*full-read* / *listed* / *vendor-reported* / *unverified*). Corpus as of the 2026-11-03 snapshot: 3336 intel items, industry 2851 / harness 3336 / trajectories 0 / domains 10.

---

## 0. 方法与溯源 · Method and provenance

**中文.** 分析建立在三处一手材料之上：本仓库 `review/references.md` 的编号文献（R1–R281，其中近三条 R279–R281 于 2026-11-02 **全文读**）、P68 的 `review/ai-tool-stack-scan-2026-11.md`（每条经 GitHub API + 官方 README/规范核，访问 2026-11-03），以及本轮 `harness trend` 的确定性聚合。本文不新增未经核验的数字；引用即生命线，无法回源者标 *unverified* 且不作为论据。数据分布本身是证据：**某簇读空，是侦察盲区，不是渲染问题**（见 §3 末、§4）。

**EN.** The reading rests on three primary grounds: this repo's numbered literature (`review/references.md`, R1–R281, the latest three *full-read* on 2026-11-02), the P68 tool scan (`review/ai-tool-stack-scan-2026-11.md`, each row resolved to GitHub API metadata + official README/spec, accessed 2026-11-03), and the deterministic aggregate from `harness trend`. No unverified figure is introduced; a claim that cannot be traced is marked *unverified* and carries no argument. The distribution itself is evidence: **an empty cluster is a discovery blind spot, not a rendering bug** (§3 end, §4).

---

## 1. 行业与相邻领域趋势 · AI industry & adjacent fields

**中文.** 行业簇 2851 条、近三十日 648 条，来源宽度 13 家——它是当前**声量最大**的一簇，几乎全部由厂商发布、生态集成与「企业落地」叙事构成。三点判断：

1. **骨架趋同，护城河上移。** 计划—工具—验证—记忆的四件套已成公共知识，差异化不再发生在「有没有 harness」，而在**验证门禁与溯源层**有多硬。这与 R279 ThinkingBox「A trajectory is a claim. Database state is the evidence. Repetition is the trust test.」的立场同构（全文读，访问 2026-11-02）。
2. **可观测性正成为底座。** OpenTelemetry 的 GenAI 语义约定 + Langfuse 一类工具，把「trace 一等公民」从工程习惯推成标准位（P68 核：otel-genai、langfuse 均 feed 可达，访问 2026-11-03）。趋势与声量之别在于：约定一旦被多语言 SDK 采纳即为趋势，单点厂商博客只是声量。
3. **数字须分「平台值」与「开源值」。** 记忆层最响的基准多为**托管平台**产出而非 OSS SDK——Mem0 的 LoCoMo/LongMemEval 高分即被其 README 明确限定在平台侧（P68 核，访问 2026-11-03）。引用时不分辨范围，就是把厂商叙事误当趋势。

**EN.** The industry cluster (2851 items, 648 in 30 days, 13 sources) is the loudest and is almost entirely vendor launches, ecosystem integrations, and "enterprise adoption" narrative. Three readings:

1. **The skeleton has converged; the moat moved up.** Plan–tool–verify–memory is now common knowledge, so differentiation is no longer *whether* a harness exists but *how hard* its verification gates and provenance layer are — isomorphic to R279 ThinkingBox's "a trajectory is a claim, database state is the evidence, repetition is the trust test" (*full-read*, 2026-11-02).
2. **Observability is becoming the substrate.** OTel's GenAI semantic conventions plus tools like Langfuse push "trace as a first-class citizen" from habit toward standard (P68: `otel-genai`, `langfuse` both feed-reachable, 2026-11-03). Signal vs noise: a convention adopted across language SDKs is a trend; one vendor blog post is noise.
3. **Separate platform numbers from OSS numbers.** The loudest memory benchmarks are managed-platform figures, not the open-source SDK — Mem0's own README scopes its headline scores to the platform (P68, 2026-11-03). Citing without that distinction mistakes vendor narrative for trend.

---

## 2. harness 方向文献综述 · Harness literature review

**中文.** harness 簇 3336 条（近三十日 888）——因每条受跟踪情报都带 `agent-harness` 主题，此簇即**全库**，是广度而非细分。真正的文献密度在三条 2026-11 全文读：

- **R279 ThinkingBox（Microsoft + Hugging Face，HF blog，全文读）。** 智能体沙箱与**按数据库终态打分**的基准：507 个有状态业务流程、5 领域、跨 18 个 LLM 各跑 20 次；判分器比较副作用增量与目标终态，经 OpenEnv 适配输出二值奖励。核心警示：**121,680 次试验的 79,853 次失败中，67.24% 干净终止、无报错，但可执行检查发现其中 77.61% 字段值错误**——约四分之三的失败是**工具处理**而非推理。这为本库 M5.13（验收门）、M5.12（带最小证据量的方差感知记分）提供了外部实现与实证注脚。
- **R280 QueenBee（arXiv:2606.27492，全文读）。** **递归自改进的 harness**：模型权重冻结，进化发生在编排层——把 workflow 视作「生成时序通信 DAG 的可执行程序」，以 **SFT-Bank**（执行诊断 / 设计假说 / 验证结论的结构化持久记忆）前馈。自进化拓扑较最强固定拓扑降 RMSE ~37.2%、消息 ~74.2%、token ~59.6%。作者诚实限定：「递归自改进」仅指 planner 生成策略，workers/prompts/scorer 冻结。其保护清单与本库条款**一一对应**（留出验收→M5.13；方差感知记分→M5.12；洞察证伪→M5.11；同构去重→M4.12）。
- **R281 LegoSR（arXiv:2610.33465，仅著录）。** 自改进智能体引导的科学发现：选择求解器、以历史任务教训自适应搜索，在同模型/工具/预算下最高超通用智能体 29 个百分点。*listed*，正文未逐读。

**综述判断.** 2026 的 harness 研究**重心已从「能力」转向「可信闭环」**：状态级判分、结构化验证记忆、留出证伪、保守信用分配。这与本库 D1（自演化）形态互为表里——外部独立实现印证了模式库的方向，而非推翻它。

**EN.** The harness cluster (3336, 888 in 30d) equals the *whole* corpus because every tracked item carries the `agent-harness` topic — breadth, not a niche. The real literature density sits in the three 2026-11 full-reads: **R279 ThinkingBox** (state-graded sandbox; its failure taxonomy — most failures are tool-handling, not reasoning, and 77.61% of "clean" terminations still carry wrong field values — is the empirical footnote to M5.13/M5.12); **R280 QueenBee** (a recursively self-improving *harness*: weights frozen, the orchestration layer evolves via a structural SFT-Bank of diagnoses/hypotheses/validation, and its safeguard list maps one-to-one onto this library's clauses); **R281 LegoSR** (self-improving agent-guided scientific discovery; *listed*). Synthesis: 2026 harness research has shifted from *capability* to *trustworthy closure* — state grading, structural validation memory, held-out falsification, conservative credit — corroborating, not contradicting, the library's D1 self-evolution shape.

---

## 3. 其他有趣且有潜力的方向 · Other promising directions

**中文.** **先说数据事实：有趣方向簇读空（0 条）。** 本簇覆盖 deep-research / retrieval-grounding / ambition-and-agency / research-evaluation / citation-integrity 等主题，而当前 feed 流几乎只吐 `agent-harness / mcp / eval / memory`——**这是侦察面的洞，不是没有前沿**，已登记为 P69.R1（拓宽 watchlist 查询）。故本节以 P68 已核实的工具生态为据，标为「组件趋势」而非「文献」：

- **约束解码 / 结构化输出（F4）**：Outlines、Instructor（P68 核：Outlines Apache-2.0，feed 可达，访问 2026-11-03）——把「让模型只在合法语法里说话」工程化，是 schema-valid 步骤契约的低成本路径。
- **时序知识图谱记忆（F1）**：Graphiti（Apache-2.0）——相对静态向量库，强调随时间演化的实体关系。
- **沙箱执行（F3）**：E2B、OpenEnv（与 R279 同源）——把「有状态副作用可判分」变成通用底座。
- **本地推理（F6）**：vLLM（Apache-2.0，活跃）——自托管、成本敏感场景的现实选择。
- **护栏（F7）与网关**：NeMo Guardrails、LiteLLM——**但二者许可证在 GitHub API 上显示 `NOASSERTION`**，未过入表门（P68 核，访问 2026-11-03），登记为 P68.R2 待核。

**辩证.** **重型检索增强退潮**是一个反向信号：Microsoft GraphRAG 已**自述进入维护模式**（P68 据 README，访问 2026-11-03，标 `defunct-track`，勿即采用）。当一度最重的 RAG 方案让位于轻量结构化输出与可观测性，「检索越强越好」的默认叙事需要被质疑。

**EN.** **The data first: this cluster reads zero.** It spans deep-research / retrieval-grounding / ambition-and-agency / research-evaluation / citation-integrity, yet the feed currently emits almost only agent-harness/mcp/eval/memory topics — a *discovery hole, not an absent frontier*, logged as P68→P69.R1. So this section draws on the P68-verified tool ecosystem, labelled component-trends rather than literature: constrained decoding (Outlines/Instructor), temporal knowledge-graph memory (Graphiti), sandboxed execution (E2B/OpenEnv), local inference (vLLM), guardrails/gateway (NeMo/LiteLLM — both `NOASSERTION`, intake gate not passed). Dialectically, **heavy-RAG fatigue** is the counter-signal: Microsoft GraphRAG self-declares maintenance mode (P68, marked `defunct-track`, do-not-adopt) — when the once-heaviest RAG regime yields to lightweight structured output and observability, the "more retrieval is always better" default deserves questioning.

---

## 4. 前沿辩证 · Frontier dialectics（趋势 vs 声量）

**中文.** 四条贯穿判断：

1. **趋同即护城河上移。** harness 骨架公共化后，价值集中在验证与溯源（§1.1、§2 综述）。
2. **读数即立场。** 同一模型 pass@1 高不等于 20/20 一致（R279：Kimi-K3 至少一次 93.89% 但一致仅 13.41%）；选指标就是选结论——本库 M5.12 的最小证据量与方差感知记分正是此虑。
3. **数据分布是元证据。** 行业簇 2851 对有趣方向簇 0，既说明**行业声量压倒前沿论文**，也说明**侦察面偏窄**；诚实的做法是把读空当作待办（P69.R1），而非粉饰成「该方向不存在」。
4. **许可即治理。** `NOASSERTION` 与 `defunct-track` 不是脚注，是入表门（M0.8）；把法律状态与维护状态当作能力评估的一等维度。

**EN.** Four through-lines: (1) convergence moves the moat to verification and provenance; (2) the metric is the stance — R279's pass@1 vs 20/20-consistency divergence (93.89% vs 13.41% for one model) shows choosing a metric is choosing a conclusion, the very worry M5.12's minimum-evidence/variance-aware credit answers; (3) the distribution is meta-evidence — industry 2851 against trajectories 0 says both that *industry volume drowns frontier papers* and that *our discovery net is narrow*, and the honest move is to treat the empty cluster as a work item (P69.R1), not as proof the direction is absent; (4) license is governance — `NOASSERTION`/`defunct-track` are first-class dimensions of capability assessment, gating intake at M0.8.

---

## 5. 溯源表 · Source register

| # | claim anchor | primary source | accessed | strength |
|---|---|---|---|---|
| R279 | ThinkingBox 状态判分与失败分类（67.24% 干净终止 / 77.61% 字段错 / 四分之三为工具处理） | Microsoft & Hugging Face, HF blog `microsoft/thinkingbox` | 2026-11-02 | **full-read** |
| R280 | QueenBee 递归自改进 harness（SFT-Bank、拓扑 RMSE −37.2%） | arXiv:2606.27492 [cs.MA] | 2026-11-02 | **full-read** |
| R281 | LegoSR 自改进科学发现（最高 +29 pp） | arXiv:2610.33465 | 2026-11-02 | *listed* |
| P68 | Mem0 平台限定基准 / Graphiti / E2B / Outlines / vLLM（Apache-2.0，feed 可达） | 各官方仓库 + GitHub API | 2026-11-03 | **verified** |
| P68 | LiteLLM、NeMo Guardrails 许可证 `NOASSERTION` | GitHub API license.spdx_id | 2026-11-03 | **verified** |
| P68 | Microsoft GraphRAG 进入维护模式（`defunct-track`） | 官方 README 自述 | 2026-11-03 | **verified** |
| snapshot | 行业 2851 / harness 3336 / 有趣方向 0 / 学科 10（近三十日 648 / 888 / 0 / 10） | `data/trend-snapshot.json`（`harness trend` 聚合） | 2026-11-03 | deterministic |

> 未纳入本文者：一切仅有二手转述、无一手可达的条目——按「引用即生命线」留作 *unverified*，不入论据。

---

*Mechanism · 机制*：本轮由 `harness full-update` 第八相（trend-review）自动生成 `updates/TREND.md` 脚手架 + 刷新 `data/trend-snapshot.json` + 重建 `docs/index.html`；分析正文（本文件）由人/agent 撰写。引擎只聚合与引用，从不下判断（M4/M0.4）。GitHub Pages 经 `.github/workflows/pages.yml` 从 SSOT 构建发布。
