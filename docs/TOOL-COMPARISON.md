# Research Foodie — 全方位工具对比与深度评估（Deep Tool Landscape Comparison & Evaluation）

> **中文速览**
> 本文档对 research_foodie 与 **2026 年 9 月现实中可对照的约 30 个系统/组件**做**逐阶段深度对比**：五类竞品（①学术综述管线 ②商用深度研究产品 ③检索/证据基础件 ④agent 编排框架 ⑤判题与评测工具），按 L1–L6 + 交付/评测逐段并排"谁赢在哪、为什么、差多少"，并附**单工具评估卡**、**横向结论**（引用幻觉率、判题方差、成本姿态、CPU/离线现实）、**复用决策矩阵**与**诚实边界**。
>
> **一句话定位结论**：我们的独特性不在任何单一阶段最强，而在**把"强制溯源"做成结构约束（write-time 5-gram 过滤 + L6 零-LLM 门 + DAS-Bench 16 轴判题）并塞进 ≈$0、CPU-only、免费模型预算**——这个组合在商用产品与学术管线两端都是空白；但单项差距明显：发现层（无元数据湖/语义召回）、结构层（无 STORM 式多视角）、写作层（无 PaperQA2 式 RCS 检索重排）、判题层（自实现、方向性）。
>
> **2026-09-23 关键校验更新**（相比 2026-09-20 版）：Co-STORM 正确 arXiv=`2408.15232`；MinerU=`2409.18839`；Tyen 判题元评测=`2311.08516`（2311.16502 实为 MMMU）；OpenResearch(Stanford OVAL) **无 arXiv 论文**（2504.01874 是代数几何数学稿）；OpenScholar 见刊 **Nature 2026-02-04**（650:857）；DAS 方法代码**仍未公开**（arXiv:2608.18034 已核实，Bench/Eval/2M/220 样例全公开）；商用深度研究"引用幻觉"实测区间 **3–13% URL 幻造 / 5–18% 不可解析**（DRBench，arXiv:2604.03173）；**《Science》并无 Deep Research 人类评测论文**（评测活在 arXiv）。

- `Updated`: 2026-09-23
- `Status`: verified against primary sources（arXiv / official repos / official product pages / Nature；全部访问日期 2026-09-23）；`*unverified*` 标未直接核实项
- `Master`: English w/ 中文速览；companion: `docs/DATAFLOW-AND-REUSE.md`（我们 I/O truth）· `docs/design/research-foodie-blueprint.md`（intent）· outline §5 / paper §2（论文版浓缩对比）

---

## 1. Landscape / 格局总览

| 桶 | 代表系统（2026-09 现实） | 共同特征 | 我们的对应 |
|---|---|---|---|
| ① 学术综述管线 | **STORM/Co-STORM**（arXiv:2402.14207/2408.15232）、**OpenResearch(orx)**、**DAS/DAS-Bench**（arXiv:2608.18034）、**PaperQA2**（arXiv:2409.13740）、**OpenScholar**（Nature 650:857, 2026-02）、**Tongyi DeepResearch**（arXiv:2510.24701）、OpenResearcher(2603.20278)、Ragnarök(2406.16828) | 有论文/代码/评测锚点；目标产出综述或长文 | 同场竞技，生态位 ≈$0+强制溯源 |
| ② 商用深度研究产品 | OpenAI Deep Research、Gemini Deep Research（app+API agent）、NotebookLM/Gemini Notebook、Perplexity Deep Research、Grok DeepSearch、DeepSeek（agentic 姿态）、Microsoft Copilot（消费版 2026-08-18 退役；企业版 Researcher/Analyst） | 云 Agent 多步浏览→带引用报告；**全部 cloud-only** | 无——我们是本地清单/可审计路径 |
| ③ 检索/证据基础件 | arXiv API、**Semantic Scholar S2AG API**（免费）、Elicit、Consensus、Undermind、Scite、AlphaXiv、Grobid、**MinerU**、PaddleOCR-VL | 单品解决发现/解析/证据评级 | 已接 arXiv+MinerU；S2AG/Grobid 待接 |
| ④ agent 编排框架 | **LangGraph**（我们已用）、AutoGen(维护模式)、CrewAI、MetaGPT、OpenAI Agents SDK、opencode | 状态图/多 agent/SOP | LangGraph 7 节点状态机 + 门 |
| ⑤ 判题与评测工具 | **DAS-Eval 16 轴**、JudgeLM/MT-Bench、LLM-judge 可靠性研究、GEPA、DRBench/DRACO/ReportEval、urlhealth | 怎么"打分/判题/查伪"才有意义 | DAS rubric verbatim + median-of-N harness |

> 判别"是真综述工具还是聊天包装"的**三层试金石**：① 事实声明是否在**写时**就绑定来源；② 质量是否按**可复现协议**判定（而非单次不确定调用）；③ 整个环路对低资源用户是否**买得起**。（论文 §2.1 同口径）

---

## 2. Stage-by-stage / 逐阶段深度对比

> 图例：🟢 我们的实现 · 🔵 对标竞品领先处 · ⚠️ 需要资源等待/方向性数字

### L1 — Discovery & Retrieval（发现与检索）

| 维度 | research_foodie（我们） | 对标 | 谁赢在哪 / 差距 |
|---|---|---|---|
| 入口 | `seed` 清单（确定性关键词打分）· **免费 arXiv API**（urllib，~1.1s 实测）· orx rails（S_LIT_BACKEND 可切） | **DAS-2M**（HF ≈2M 篇 arXiv 元数据湖，2020-01→2026-06，8 组领域）· **S2AG API**（免费，relevance search ≤1000 结果，batch 500 IDs/9999 cites，SPECTER2 嵌入可下载建本地向量库）· STORM 的 VectorRM/You/Bing；OpenScholar 45M OA 论文 datastore | 🔵 我们**无元数据湖、无语义召回、无引用图**——广度被 arXiv 相关性 top-K 限制（实测属性，非静默）。**S2AG = 零成本同层替代**（免费 API + Datasets 下载嵌入） |
| 失败链 | orx→arxiv→seed 保底 | — | 🟢 已具备 |
| 评测/真实性 | 每 ID 回证到一手来源（PROGRESS ledger） | orx 的 discover 不受校验 | 🟢 保留我方 |

### L2 — Evidence Parsing（证据解析）

| 维度 | 我们 | 对标 | 差距 |
|---|---|---|---|
| PDF→文本 | **MinerU** `-m txt` 窗口 ≤6pp、子分块、420s 超时（`add_paper.py`） | 同引擎 Green；**Grobid**（Apache-2.0，**纯 CPU 官方镜像**，TEI 结构化含 PDF 坐标）· PaperQA2 实际用 Grobid · MinerU 论文 arXiv:**2409.18839**；PaddleOCR-VL（0.9B，109 语种，专为资源受限设计） | 🔵 解析引擎同源；但我们**不建 chunk 索引**（PaperQA2/DAS 都建检索 store）；**Grobid CPU 镜像 + S2AG 元数据/撤稿检查**是本层该补的 |
| 元数据 | manual `_LOCAL_MD` 注册表 + 人工核对标签 | PaperQA2 自动 Crossref/S2/Unpaywall + **retraction check** | 🔵 自动元数据+撤稿 = 我们 vendored `citation-verify` 目前是手动 |
| 检索重排 | 无（取原始窗口） | PaperQA2 **RCS**（dense 检索→LLM 重排+上下文化摘要，其论文称对 RAG 决定性）；DAS 对 2M 湖做 LLM 抽取式 paper 表征 | 🔵 **L4 头号已知缺口**，可低成本镜像（BM25 级，零依赖） |

### L3 — Structure / Outline（结构与大纲）

| 维度 | 我们 | 对标 | 差距 |
|---|---|---|---|
| 大纲方式 | `_org`：2,000 字跨论文窗口 prompt → topics+outline | **STORM：Perspective-Guided Question Asking**（多专家视角交互式提问→大纲），FreshWiki +25%/organized、+10%/coverage，NAACL 2024；**DAS：候选接地 Taxonomy + 反向 PaperRouter**（section→papers 反向路由） | 🔵 我们更接近 STORM 的 "Direct Gen" baseline；**缺多视角分解**（STORM 最强测量增益处）与**反向路由**（DAS 未开源） |
| 引用归属 | 逐 paper + outline | DAS 反向路由修 section 级引用 scope | 🔵 结构层待补 |

### L4 — Claim-led Writing（写作）

| 维度 | 我们 | 对标 | 差距 |
|---|---|---|---|
| 证据→声明 | 逐 paper 一次 LLM 调用 over **原始首 ≤20,000 字符** → 接地 claims（5-gram 逐字门） | **PaperQA2**：Gather-Evidence top-k → **RCS 重排+上下文化摘要**；**OpenScholar**：自反馈环路 cite-evaluate-regenerate，8B 模型 >GPT-4o 6.1%、GPT-4o 引用幻觉 78–90%（Nature）；**DAS**：claim 级引用组 + 确定性校验（30/30 可编译 vs 27/30） | 🔵 无相关性选择是我们 L4 最大的自研短板（PaperQA2 RCS 镜像是零依赖可做项） |
| 双语/成稿 | intro + 逐节中英段落 + 问答速览 | — | 🟢 双语交付为差异化 |

### L5 — Orchestration & Resilience（编排与韧性）

| 维度 | 我们 | 对标 | 差距 |
|---|---|---|---|
| 状态机 | **LangGraph 7 节点** + 显式门 | DAS **stateful closed-loop**（共享手稿态 + scoped review-and-repair：评审通过率 74.59%，平均 0.79M tokens/篇修复成本）；orx 用你的 coding agent 当编排 harness | 🔵 我们的 revise 是全稿级；DAS 的 scoped-loop 是实打实增益但低频触发。orx 非固定管线，无法互换 |
| 并行 | `autoresearch` 模型无关并行子图（S26） | OpenResearch agent 并行；Perplexity "Search as Code"（2026，数千步并行） | 🟢 已具备模型无关并行 |
| 韧性 | run-memory ledger 断线/断电续跑、401 fail-fast | LangGraph checkpointer/thread+time-travel；AutoGen 无内置 HITL checkpoint（维护模式） | 🟢 我们的 ledger 是自研且被事故验证（S24–25） |
| 框架替代 | — | CrewAI Flows（事件式有序）、OpenAI Agents SDK（handoffs 如 router）、MetaGPT（SOP）、**AutoGen 维护模式=绿场勿入** | 🟢 LangGraph 仍是确定性首选；新 users 别选 AutoGen |

### L6 — Validation & Judge（校验与判题）

| 维度 | 我们 | 对标 | 差距 |
|---|---|---|---|
| 确定性门 | **零-LLM L6**（结构/引用形态/5-gram 接地/双语/多论文 + JSON 解析器），变异测试 23/23 杀灭 | DAS "deterministic before semantic" 同教义 | 🟢 教义对齐，且我们真正零成本、变异已测 |
| 判题 | 自实现 16 轴（BSC·MAR·TSQ·HDQ verbatim）→ **median-of-N harness**；单 run 漂移已实测（P-C −1.7σ 旗标） | **DAS-Eval 官方 harness 已公开但未在本仓运行**（需 ≥300B 冻结判题）；SOTA 判题研究：**JudgeLM**（位置/知识/格式 bias + swap/ref 缓解，7B 判决 >90% 与 teacher 一致 >人-人 82%上限）；Schroeder&Wood-Doughty（种子+温度改变评级 → 单样本不可靠） | 🔵 判题自实现=方向性（如实标注）；**median-of-N 有文献背书**（C2）；官方 harness 是等待项（≥300B key/GPU） |
| 引用幻觉检测 | 写时 5-gram 门（抓到伪造 claim 会拦） | **DRBench**：商用 DR 代理 URL 幻造 3–13%、不可解析 5–18%；**urlhealth**（MIT，83 行 Python）把不可解析 URL 降 6–79× 至 <1%；CITETRACER（arXiv:2605.08583）97.1% 检出 | 🔵 **urlhealth 是个一键补丁级资产**（https 健康自愈），现成 MIT 可并入 |

### Delivery / Evaluation / UX（交付·评测·体验）

| 维度 | 我们 | 对标 | 差距 |
|---|---|---|---|
| 交付 | md + 干货 PDF + 出版化 PDF（pandoc+xelatex）+ **知识库/阅读器**（本地，零外部网络，en/zh） | DAS 出 LaTeX/PDF 出版化稿（含自适应图表/交叉引用，无 web/技术报告源）；商用产品全在云 | 🟢 双档交付 + 本地产品面是差异化；DAS 的出版化排版更强 |
| 诚实评测 | DAS-Bench 16 轴方向性 + L6 1.00 + mock/real 34/34 + live trio 3.65 + health GREEN；所有数字带 provenance (D-4) | 商用产品**零自评估公开**；DRBench/DRACO/ReportEval 是第三方代理评测 | 🟢 self-measuring 是稀缺姿态（GOOD）；判题模型档位仍是短板 |
| UX | 温纸白卡 calm 风格、双语、mock/real 严守分界 | STORM live 版 (Co-STORM 70%/78% 偏好)、商用产品进度条+可打断（2026 已改善） | 🟢 本地可用；产品化打磨可再追 |

---

## 3. Per-tool profiles / 单工具评估卡

> 每个评估卡：定位 · 接地机制 · 分阶段最大强/弱 · 判题/评测 · 预算姿态 · 复用建议 · 一句话裁决。来源均访问 2026-09-23。

### 3.1 学术管线系统（深度卡）

**① STORM / Co-STORM — "多视角大纲 + 检索式写作"的开创者**
- 定位：从零写维基式长文的 RAG 管线（NAACL 2024，arXiv:2402.14207；Co-STORM=人机协同思维导图，2408.15232，MIT，`knowledge-storm` v1.1.1）。
- 接地：多专家 persona 对话生成提问→每视角答案锚定检索片段；Co-STORM 引入人工参与补 "unknown unknowns"。
- 强/弱：L3 最强（+25% organized / +10% coverage vs RAG baseline）；L6 无强制接地门、无判题门（专家反馈已知 source-bias 传递与无关事实过度关联）。
- 预算：LLM-API 重（多轮 persona 对话）；开权重模型更弱。无 per-run 成本公开。
- 复用建议：`knowledge-storm` 里 **VectorRM + Outline 模块** = 我们 L3 升级路径第一条；STORM 附录 B 含 DSPy 伪代码+prompts（可复刻：max_turn×(max_perspective+1) 预算）。
- 裁决：**思路该借（L3），代码别全借（重、无门）**。

**② OpenResearch (orx) — "本地优先的 agent 研究 harness"**
- 定位：把 Codex/Claude Code/OpenCode 变成研究 agent 的 CLI 工作区（官方 repo `alphaXiv/openresearch-cli`，MIT，5.6k★；**无 arXiv 论文**——常见引用 2504.01874 实为代数几何数学稿）。
- 接地：结构化的 `SearchResults/Document` JSON 喂你的 coding agent；查 arXiv(alphaXiv)/OpenAlex/bioRxiv；写完才落本地工作区。
- 强/弱：L1/L2 发现质量高（官方 API 免爬、无 login）；L3–L5 由宿主 agent 决定（非固定管线）；**L6 无内置判题**。
- 预算：CLI 免费；成本=你的 agent 的 API。
- 复用建议：`orx install-skills` 把 SKILL.md 直接丢进 OpenCode——**与我们的 agent 工作台同构**，接入成本低。
- 裁决：**借 rails（S_LIT_BACKEND=orx 现有休眠开关），不换编排（它没状态机/门）**。

**③ DAS / DAS-Bench / DAS-Eval / DAS-2M — "stateful closed-loop 综述+官方评测"**
- 定位：stateful agentic closed-loop 综述自动化（arXiv:2608.18034，已核实；Zhejiang Univ+SJTU，2026-08；repo `ZhikaiXu24/DAS`，Apache-2.0，**方法代码 "To be released"**；DAS-2M≈2M 元数据湖、DAS-Bench 30 话题、220 样例综述全公开）。
- 接地：元数据湖→查询/taxonomy 规划→有人路由→claim 分组→写作；**确定性校验**（30/30 可编译 vs 27/30）。
- 强/弱：L1 混合 lexical+semantic 覆盖 2M 湖；L5 scoped 修复（评审通过率 74.59%，0.79M tokens/篇成本）；**主对比全 30 话题 DAS 4.34 ≈ Human ref 4.34**（vs Naive RAG 4.03、Gemini-DR 3.92、GPT-DR 3.68、Codex 3.18；AutoSurvey 3.73/SurveyForge 3.78 仅 21 个 CS 话题）；专家偏好 DAS vs RAG 27/30。**数字方向性（LLM judge）**。
- 预算：token 大户（仅修复就 0.79M/篇）；无免费本地路径公开。
- 复用建议：**DAS-Bench 16 轴 rubric 已 verbatim 采用**；官方 Eval harness 待 ≥300B 判题；DAS-2M/220 样例可作 few-shot 校准。
- 裁决：**"最接近我们的基准对齐对象"；方法论不可复现（未开源）→ 继续按论文复现路线。**

**④ PaperQA2 — "科研 RAG + 元数据核验"**
- 定位：agentic 科研问答（arXiv:2409.13740；`Future-House/paper-qa` **Apache-2.0**，PyPI 2026.8.12，CalVer）。
- 接地：检索 top-k→**RCS**（重排+上下文化摘要）→带引文作答；Crossref/S2/Unpaywall 元数据 + **retraction check**（撤稿检查！）。
- 强/弱：L2 最强（RCS；矛盾检测 2.34±1.99/篇，70% 人验）；L6 self-verify 三项文献任务超人类；**L3 弱（答问题不做报告/无 taxonomy）**。
- 预算：默认 gpt-4o + text-embedding-3-small（paid API）；`paper-qa[local]`（llamafile/ollama）可行但 7B 档被建议别用。
- 复用建议：**RCS 重排 = 我们 L4 缺口的最小镜像（BM25 级、零依赖）**；retraction check 并入 metadata。
- 裁决：**借技术（RCS/撤稿），不整包换（它无综述结构层、且绑定模型档位）。**

**⑤ OpenScholar — "检索增强长文 + 引用幻觉公开锚点"**
- 定位：对 45M OA 论文 datastore 做文献综合（arXiv:2411.14199；**Nature 650:857, 2026-02-04**，DOI 10.1038/s41586-025-10072-4；repo `AkariAsai/OpenScholar` Apache-2.0，1.6k★）。
- 接地：SPLADE 式 retriever + 自反馈环路 cite-evaluate-refine；ScholarQABench（2,967 查询·208 长答）。
- 强/弱：L4/L5 强（OpenScholar-8B >GPT-4o 6.1%、>PaperQA2 5.5%；GPT-4o **78–90% 引用幻觉**）；L1 datastore 本地托管重（45M 篇）。
- 预算：8B 基座轻量；45M datastore 只能 API/演示。成本 *unverified*。
- 复用建议：**引用幻觉 78–90% 与专家级引用准确度 → 写进论文 related-work 与 §4**；数据/模型全开源可评估。
- 裁决：**"高效幻觉"vs"接地"之别的权威锚点；其 8B 路线印证免费档可行。**

**⑥ Tongyi DeepResearch — "开源最能打、最便宜本地档"**
- 定位：agentic deep research 开源基线（arXiv:2510.24701，v3 2026-05；repo `Alibaba-NLP/DeepResearch` Apache-2.0，20k★；模型 30.5B total/**3.3B active** MoE，128K ctx）。
- 接地：agentic mid/post-training（GRPO 族）+ 全自动数据合成；ReAct 与 "Heavy"（test-time scaling）双模式；Serper/Jina 工具。论文预印本称 HLE/BrowseComp/WebWalkerQA/FRAMES SOTA（具体分数表*未在本仓逐条提取*）。
- 强/弱：**预算端最强（3.3B active → 消费级 GPU 可自托管）**；L1 web 检索工具化；**评测是 agent benchmark 中心，≠综述质量**；citation 精度数据缺口。
- 复用建议：et al. 免费档深研"能力上限"对照；本地推理脚本即取即用。
- 裁决：**做"免费档上限"的现实参照；不做综述接地保证。**

**⑦ OpenResearcher (TIGER-AI-Lab) — "全开放轨迹合成"**
- 定位：15M 文档离线语料 + 3 个浏览器原语；GPT-OSS-120B 教师合成 97K 轨迹（有 >100 步长）→ SFT 30B-A3B → **BrowseComp-Plus 54.8%（+34.0 vs base）**（arXiv:2603.20278；license *unverified*）。
- 复用：全开放数据+模型，最可复现的 deep-research play；但目标=长程操作而非综述稿。
- 裁决：**复现友好；与综述接地正交。**

**⑧ Ragnarök — "TREC RAG 官方框架/评测台"**
- 定位：Pyserini BM25 + rank_llm 重排（top-100→20）+ sentence 级 IEEE 引文；ARENA 双盲人评（arXiv:2406.16828/corrected；`castorini/ragnarok` Apache-2.0）。
- 复用：**L5/L6 评测 harness 复用候选**（paired human eval arena 现成）。
- 裁决：**评测基建借用。**

### 3.2 商用深度研究产品（浓缩卡；全部 **cloud-only**）

| 产品 | 机制/引用 | 已测弱点（带源） | 预算姿态 | 裁决 |
|---|---|---|---|---|
| **OpenAI Deep Research**（2025-02-02；2026-02-10 迭代） | computer-use 多步浏览→带引用报告；可接 MCP/apps/可信源；可打断精简 | 启动期 HLE 26.6%/GAIA ~67.4%（o3 时代，勿当"当前"）；DRBench：**幻造 URL 3.5%（最低）/不可解析 10.1%**（arXiv:2604.03173） | 云；计划配额/30 天刻度 | 能力标杆；无方案无本地无自评 |
| **Gemini Deep Research**（consumer + API agent 2026-03/04） | 计划→执行→成稿报告；API 版 MCP/File Search/1M ctx；free Flash 档 | DRBench **幻造 URL 13.3%（最高）** | 云；免费档或 AI Pro/Ultra | 免费可试；引用质量最差可测 |
| **NotebookLM / Gemini Notebook**（2026-07 更名） | **语料接地**（仅你上传源，行内引用）；2026-06 起 Gemini 3.5+云端代码沙箱+出图表/PDF/PPTX 工件 | 上界=你给的语料；区域受付费档 | 免费 + Google One/Workspace | 理念最近（source-grounded）；无本地 |
| **Perplexity Deep Research**（2025-02；2026 "Search-as-Code"/Advanced） | "几十检索几百源"迭代；代码沙箱；Max→Opus 4.6 Thinking | 可核查的**伪造医生署名评论**事件（arXiv:2604.03173 引言） | 免费档/Pro/Max | 快、好用；信任靠它自己 |
| **Grok DeepSearch**（xAI 2025-02 起) | 原生工具调用并行检索 X+web；Grok 4.5/4.6 | 独立同行评测稀缺；引用/审计 UI 未标准化 | 订阅/API；X 集成需 Premium+ | 实时语料强；文献能力弱 |
| **DeepSeek** | **无官方 "DeepSeek-Research" 产品**（仅 V3.1 起 agentic 工具/搜索姿态，open weights） | 产品名 *unverified* | 开源+低价 API | "产品"指控要审慎 |
| **Microsoft Copilot**（消费版 2025-04 起） | 多步研究→引用报告 | **2026-08-18 消费版 Deep Research 退役**；企业版=Researcher/Analyst（M365 编排+OpenAI DR 模型，25 queries/mo 上限） | Copilot 订阅；M365 许可 | 消费端已收缩；企业端是 M365 生态 |

### 3.3 检索/证据基础件（浓缩卡）

| 组件 | 一句话 | 钱/证姿态 | 对我们的可复用处 |
|---|---|---|---|
| **Semantic Scholar S2AG API**（free） | 免费引用图 + relevance search(≤1000) + TLDR + SPECTER2 嵌入可下载 | 免费；公共端点 1k req/s 共享 | **L1 元数据湖/引用图/嵌入零成本替代**——最高优先接入 |
| Elicit | 138M+ 论文语义搜索 + 系统综述式筛选 + 报告 | SaaS；API 需 Pro($49/mo)；retracted 默认排除 | 设计灵感+付费升级版 |
| Consensus | 论文共识引擎（pro/con 分布） | API $0.05/调用，500–2000 credits/mo | 证据评级覆盖层 |
| Undermind | 2.3M arXiv 全文迭代搜+相关性三级标注 | closed；无 API 确认 | 仅设计借鉴 |
| Scite | 引用上下文分类 supporting/contrasting/mentioning | 免费 Tallies 端点 + Pro($50/mo) REST key | 证据方向性的零钱补丁 |
| AlphaXiv | arXiv 全文 + 社区评论线程（orx 的语料层） | SaaS；MCP server 官方 | 评论证据层（MCP 即插） |
| **Grobid** | PDF→TEI 结构化（含坐标）**纯 CPU 官方镜像** | Apache-2.0，需 Java/Docker | L2 可选并入（坐标→溯源） |
| **MinerU** | PDF/Office→Markdown/JSON（布局/表格/公式 UniMERNet/OCR 109 语种；MCP/CLI） | 开源（arXiv:**2409.18839**；license 以 repo 为准） | **已在用**；AGPL 嵌入注意 |
| PaddleOCR-VL | 0.9B VLM 两段式解析（DocLayoutV2+VL），109 语种，资源受限设计 | Paddle 系 Apache-2.0（*未复检*） | 扫描/多语/公式重的 PDF 补刀 |

### 3.4 agent 编排框架（浓缩卡；基准=LangGraph+显式门）

| 框架 | license/状态 | 强 | 弱 vs 我们的确定性路径 |
|---|---|---|---|
| **LangGraph**（在用） | MIT | StateGraph+checkpoint(HITL/time-travel)，唯一原生给"确定性图+可持久化" | 编译期检查；持久化需 backend |
| AutoGen | MIT；**维护模式，官方转向 Microsoft Agent Framework** | 事件驱动多 agent 先驱，API 稳定 | 无内置 HITL checkpoint（Team）；绿场慎入 |
| CrewAI | MIT | Crews(角色组)+Flows(事件式有序) | 自主 Cree 默认非确定；企业控制面付费 |
| MetaGPT | MIT（2024-01 起） | SOP 角色分解模式可借鉴 | 面向软件开发非证据管线 |
| OpenAI Agents SDK | MIT | handoff 显式路由≈我们阶段推进；100+ 模型含本地 | 持久化非一等公民 |
| opencode | MIT（我们脚下这个 agent） | skills/plugins/MCP + 75+ 提供商含本地 Ollama | 交互式为主，非无头管线——与 LangGraph 配合用 |

### 3.5 判题与评测工具（浓缩卡）

| 工具 | 关键事实（带源） | 对我们意味着 |
|---|---|---|
| **DAS-Eval 16 轴** | arXiv:2608.18034；16 criteria × 4 dim（citation/taxonomic/hierarchical/manuscript） | 已 verbatim 采用；官方 harness 待 ≥300B |
| **JudgeLM**（arXiv:2310.17631） | 7B/13B/33B；位置/知识/格式 bias + swap/ref 缓解；7B 判决与 teacher >90% 一致 > 人-人 82% 上限；MT-bench/GPT-4 judge >80% 人一致（2306.05685） | 我们的自实现判题可按 swap/self-consistency 加固 |
| **Schroeder & Wood-Doughty**（arXiv:2412.12509） | 评级随 seed+温度变；**单样本判决不可靠** | **median-of-N 判题的文献背书** |
| **Tyen et al.**（arXiv:2311.08516/corrected） | LLM judge **找不到推理错误，但给定位能改**（BIG-Bench Mistake）；2311.16502 实为 MMMU——勿混 | 判题必须配"可定位可验证"的机械门，别信整体"对/不对" |
| **GEPA**（arXiv:2507.19457） | 文本反馈 GP 优化 >GRPO 6% avg(≤20%)、rollout 至 35× 少；+12% AIME-2025 | prompt 级优化 CPU 可负担 → E-7 参考 |
| **DRBench / urlhealth**（arXiv:2604.03173；urlhealth MIT 83 行） | DR 代理 URL 幻造 3–13%/不可解析 5–18%；urlhealth 自愈后不可解析 <1%（6–79×） | 一键补丁级引用健康资产 |

---

## 4. Cross-cutting findings / 横向结论（带源，访问 2026-09-23）

1. **引用幻觉是有实测的普遍病**：商用 DR 代理幻造 URL 3–13%、不可解析 5–18%（DRBench, arXiv:2604.03173）。OpenAI 3.5%（最低）、Gemini 13.3%（最高）；**"引得多≠可靠"（RQ5 反向/无关）**。→ 我们的写时 5-gram 门抓住了与这些产品同层级的病（实测抓到伪造 claim 被 gate 拦截）。
2. **《Science/AAAS 并无 Deep Research 人类评测论文》**——论文量级评测活在 arXiv（DRACO 2602.11685、ReportEval 2510.07861、Rao 2604.03173）；Science 只有博客/专栏（Derek Lowe 2025-02-06 实测、Nature 652:26–29 2026-04-01 关于引用污染）。→ 论文 related-work 引用 arXiv 而非 Science 传闻。
3. **判题单样本不可靠 → median-of-N 有硬证据**（Schroeder&Wood-Doughty 2412.12509；JudgeLM bias 2310.17631；Tyen 定位而非判定 2311.08516）。→ 我们的中位数判题 harness 是"现在就对"的设计。
4. **成本姿态两极**：学术管线（STORM/PaperQA2/DAS）默认云 API 且 token 重；商用产品全 cloud、订阅/配额；**免费本地档只剩 Tongyi-DeepResearch(3.3B active)、OpenScholar-8B、DeepSeek open weights**。→ "≈$0 CPU-only"生态位依旧空白，但我们与 Tongyi/OpenScholar 是同一预算谱系。
5. **评测层新现成的可再借资产**（2026-08 起）比上次盘点更多：DAS-Eval 官方 harness（需 ≥300B）、`urlhealth`（MIT 自愈）、`pyragnarok`（TREC 竞技场）、S2AG Datasets（嵌入下载）、DAS-2M/220 样例。
6. **要审慎的跑路叙事**：无 "Deep Research 2" branding；DeepSeek-Research 非官方产品名；消费版 Copilot DR 已退役；Perplexity/Gemini 产品声明多为厂商自测。

---

## 5. Reuse & integration decision matrix / 复用决策矩阵（2026-09-23 更新）

| 资产 | 类型 | 来源/license | 复用决策（Feas × Val） | 状态 |
|---|---|---|---|---|
| **Semantic Scholar S2AG API + Datasets** | API+数据 | 免费/S2 | 🔵 L1 元数据湖+引用图+SPECTER2 嵌入本地库。**Feas 5 · Val 4** | 待接入（最高优先） |
| **urlhealth** | 包(MIT, 83 行) | arXiv:2604.03173 | 🔵 citation 健康自愈并入 L6。Feas 5 · Val 3 | 待接入 |
| Grobid（CPU 镜像） | 服务(Apache-2.0) | grobidorg | 🔵 L2 结构化+坐标可选。Feas 3 · Val 2 | 可选 |
| `knowledge-storm` VectorRM+Outline | pip(MIT) | Stanford OVAL | 🔵 L3 升级路径；需 OpenAI-compatible 端点。Feas 3 · Val 3 | 等端点 |
| DAS-Eval official harness | repo+HF | ZhikaiXu24/Apache-2.0(代码)；数据另计 | 🔵 替换自实现判题；需 ≥300B。Feas 2 · Val 5 | 等 ≥300B |
| DAS-2M + 220 样例综述 | HF | 公开 | 🔵 L1 湖/ few-shot 校准锚。Feas 3+4 · Val 3 | 可即取 |
| PaperQA2 RCS 最小镜像（BM25 级） | 自研 | — | 🔵 L4 检索重排零依赖。Feas 5 · Val 4 | 自研项 |
| STORM perspective-asking 复刻 | 方法 | NAACL/arXiv:2402.14207 附录 B | 🔵 L3 多视角。Feas 5 · Val 4 | 自研项 |
| orx CLI / S_LIT_BACKEND=orx | CLI(MIT) | alphaXiv | 🔵 启用 dormant switch + `orx install-skills`。Feas 4 · Val 2 | 可即取 |
| `pyragnarok` | pip(Apache-2.0) | castorini | 🔵 L5/L6 双盲评测 arena。Feas 3 · Val 2 | 可选 |
| Consensus API / Scite Tallies | API(SaaS) | Consensus/Scite | 🔵 证据评级覆盖层（$0.05/调用级）。Feas 4 · Val 2 | 可选 |
| es local skills（citation-verification / research / academic-research-writer） | skills | ~/.agents/skills | 🟢 L6 人工lane + 文档写作。Feas 5 · Val 3 | 已装待接线 |

---

## 6. Honest boundaries / 诚实边界（*unverified* 清单）

- DAS 方法代码未开源（"To be released"）→ 状态机/路由继续按论文复现，未被下游变化推翻。
- Tongyi DeepResearch 具体榜分数（论文表）未在本仓逐条提取；DAS "1 小时内出稿"为 repo 宣传语（未独立计时）。
- DAS-2M HF 许可细则、TIGER OpenResearcher license、PaperQA2 单查询成本（传闻 $1–3/查询）均 **unverified**。
- 判题全部数字方向性（free 模型权重），MAR 轴需 ≥300B page-aware（阻塞 keys/GPU）。
- 商用产品引用幻觉率（3.5%/13.3% 等）是**单一 DRBench 快照**，会随模型版更而变——勿外推为永恒属性。