# 趋势周报 · 2026-11-07 · Trend review (weekly model, first issue)

**Updated:** 2026-11-07 · **Round:** P77 · **数据窗口:** intel 2026-10-24 → 2026-11-07（2 周，2995 条）· **上一期:** [trend-review-2026-11-03.md](trend-review-2026-11-03.md)

> **中文速览。** 本期起趋势综述改为**周更模型**：确定性管线（`harness intel` 拉流 → `harness trend` 四簇聚合 +
> 周际动量 delta）供原材料，本文供分析。管线本身先做了三项质量升级（判别性打分 · 源多样性上限 · 噪声惩罚），
> 因为旧聚合的行业簇与 harness 簇 top 几乎相同、且单一源可垄断表格——分析的上限取决于原材料的质量。
> 本周四条承重信号均经一手核验：① OpenAI 前沿训练环境**完全离线化**（基础设施安全成为一等控制问题）；
> ② Agent Skills 标准捐入 Linux 基金会旗下 AAIF（Anthropic+Block+OpenAI 共建）；③ SWE-Bench Pro 审计的
> 后续——V2 基准以"更干净、更难操纵"为卖点上世；④ Terminal-Bench 转向**持续语义版本**基准（4.x 连续演化）。
> 四者共同指向同一判断：**评测与执行环境的"可信度工程"正在从论文话题变成行业基础设施**。分析详见 §5；
> 对本库的行动项见 §6。周更规程见 `tasks/TREND.md`。

## 1 · 本周信号 · Weekly signals

| # | 信号 | 源 · 日期 | 一句话判读 | 核验 |
|---|---|---|---|---|
| 1 | OpenAI 前沿模型训练环境改为**离线无外网**，网络安全升格为一等控制问题（含红队演练） | [OpenAI blog](https://openai.com/index/securing-our-frontier-model-training-environment) · 2026-10-23 | 会写代码的模型 + 有外网的训练设施 = 承认的风险面；containment 成为训练基础设施的一部分 | ✅ 一手 |
| 2 | Anthropic 把 **Agent Skills 标准**（名称/logo/GitHub org/agentskills.io 域名）捐给 Linux 基金会下的 **Agentic AI Foundation**（Anthropic+Block+OpenAI 共建） | [Simon Willison](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) · 2026-10-22 | 技能生态从中立化走向**基金会治理**；标准竞争从"谁定义"转向"谁执行得好" | ✅ 一手 |
| 3 | SWE-Bench Pro 审计后续：**V2 基准**（2026-10-16）以更干净、更难操纵为卖点，引用 OpenAI 审计（731 任务逐项核查） | [OpenAI blog](https://openai.com/index/separating-signal-from-noise-coding-evaluations)（审计 2026-07-08；V2 为窗口内后续） | 基准的双重有效性（任务有效性 vs 分数有效性）从学术批评变成**发布工程** | ✅ 一手（审计）；V2 *unverified*（转述） |
| 4 | **Terminal-Bench 4.x** 持续语义版本演化（4.0 换 agent 环境，v4.1.0 点版本跟进），leaderboard 按 模型×agent 组合排名 | [tbench.ai](https://www.tbench.ai) · [repo](https://github.com/laude-institute/terminal-bench) | "基准即持续演化服务"——与 pass^k 可靠性口径（R282/R279）同构 | ✅ 一手（站点/仓库） |
| 5 | MIT **VISTA**：把 context engineering 扩展到图像域的 agent 工作流 | The Batch · 2026-11-06 · [link](https://charonhub.deeplearning.ai/context-engineering-for-images/) | 上下文工程（M1）的证据面从纯文本扩到多模态 | feed 源 |
| 6 | OpenAI 发布 **wet-lab 日常科学** agent 能力测量 | [OpenAI](https://openai.com/index/measuring-how-ai-agents-handle-wet-lab-science) · 2026-11-06 | 实验室操作类任务进入"可测量"清单——具身/湿域判分语义（P71 映射）的行业印证 | ✅ 一手 |
| 7 | **skills.sh v1.7.2**（`npx skills` 生态）与 skills 市场工具持续发版 | intel 流 · 2026-11 窗口 | 技能分发基础设施在基金会化（信号 2）的同时**商品化** | feed 源 |
| 8 | Microsoft Research：从**合成企业数据评测**到真实 Copilot 置信度 | [MSR blog](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/) · 2026-10-30 | 评测的"合成→真实"迁移问题（scope non-transferability 的行业版） | feed 源 |

## 2 · 行业全景与相邻领域 · Industry & adjacent fields

数据基座：industry 簇 2546 条（30 天内 242），27 源。三条行业级主线：

**基础设施的"安全内转"。** 信号 1 不是孤例而是方向：当模型能力足以操纵基础设施，训练/评测环境本身成为攻击面，
头部实验室把 containment 内化为工程常项。对本库的映射是直接的——M6 工具面与沙箱纪律（M0.9）的行业正当性
又添一层：**离线优先不只是成本选择，也是安全姿态**。

**标准治理的中立化。** 技能生态（信号 2、7）走出了"厂商标准 → 基金会标准"这一步。辩证面：基金会化解决
"控制权"问题，不解决"质量"问题——skills 市场的良莠分布（本库 `.harness/skills/` 的 portable-skill 门禁
正是针对此）不会因为治理中立而自动改善。**趋势与声量的区分点**：捐标准是事件，生态质量是过程。

**评测的行业化重构。** 信号 3、4 合并读：基准正在从"静态排行榜"转向"持续演化 + 可审计"的服务形态
（Terminal-Bench 的 semver 演化、SWE-Bench Pro V2 的防操纵声明）。这印证本库 P70 把 pass^k/状态判分/
模型×外壳披露列为一等判据的判断——行业在向同一个方向收敛。

## 3 · Harness 文献综述 · Harness-direction literature review

本周信号与既有参考库（R1–R293）的对账，三条线：

**评测生态线（§AF，R283–R285）。** Princeton 综合的"评估者独立性 + 范围不可迁移"在本周得到行业级印证：
信号 8（合成→真实 Copilot）就是 scope non-transferability 的第一人称叙述；信号 3 的 V2 则是 benchmark
dual validity 的工程化落地。**判断强化：**评测有效性是 2026 下半年 harness 议程的中心，不是边缘。

**可靠性线（§AE，R282/R279）。** Terminal-Bench 的持续演化模式（信号 4）与 τ-bench 的 pass^k 口径同构，
但增加了一个新变量：**基准本身的版本成为实验变量**（4.0 换了 agent 环境）。本库 battery 的 `scale` 声明
与 trial_projects 绑定需要意识到：跨版本比较分数是范围错误（M3.19 扫荡形式的新案例）。

**上下文工程线（M1，R268/R277）。** VISTA（信号 5）把 context engineering 从文本扩展到图像工作流。
对本库是"复核触发器"而非行动项：M1.11 的 compaction 预算论证基于文本 token，多模态上下文的预算语义
尚未进入本库范围——登记为观察，不臆造（M0.4）。

## 4 · 新兴方向 · Emerging directions

trajectories 簇本周 10 条（此前为 0——聚合升级后 retrieval-grounding 主题首次有命中），domains 簇仍只有
Internet Archive 一源。**诚实声明：**这两簇的数据面还很薄，以下是"信号 + 推理"，不是"证据 + 结论"：

- **检索增强的自我改进**（GraphRAG v3.3.0 持续发版 vs 本库已知的维护模式先例）：检索基础设施在长记忆
  生态位上仍是活跃供给，但"热点"与"可持续"要分开——GraphRAG 的维护状态需要逐版本核对。
- **湿域/具身判分**（信号 6）：OSWorld/Terminal-Bench 的状态判分语义向物理域延伸（P71 已映射 RoboDojo），
  行业开始供给"日常科学"测量——这是本库 evidence-instruments 门禁 6 的行业对照。

## 5 · 分析与预测 · Analysis & predictions

| # | 论断 | 证据 | 置信 | 反转条件 |
|---|---|---|---|---|
| T1 | **可信度工程基础设施化**：训练/评测/执行环境的 containment、审计、版本治理在 2026Q4-2027 成为头部 labs 的一等工程线，并出现事实标准（审计披露格式等） | 信号 1（训练环境离线化）+ 信号 3（基准审计→V2）+ 信号 4（semver 演化基准） | 中高 | 若 2027Q1 前无第二家 lab 跟进环境隔离披露，或 V2 类"防操纵基准"未形成品类 |
| T2 | **技能生态双轨化**：基金会标准（AAIF）与商业市场并行，"可移植性门禁"成为消费侧的刚需——标准组织不管质量 | 信号 2 + 信号 7 | 中 | 若 AAIF 发布质量分级/认证计划（则质量由治理解决） |
| T3 | **基准版本成为实验变量**：跨基准版本的分数比较被社区正式视为无效（类比 M3.19），leaderboard 语义转向"版本内排名" | 信号 4 的 semver 模式 + 信号 3 的审计-重估循环 | 中 | 若 Terminal-Bench 类基准发布跨版本可比性承诺 |
| T4 | 评测从"跑分"转向"测量学"：环境状态判分 + pass^k + 披露三元组成为 agent 评测的默认口径 | R282–R289 既有锚点 + 本周信号 3/4/6/8 同向 | 中高 | 若行业回归单次 pass@1 排行榜叙事 |

**辩证面（每个被看好方向的强反例）：** T1 的反例是"安全 theater"风险——离线化可以只是声明而非实践，
审计格式可以变成新的洗白载体；本库的应对是只认**可重放的披露**（LHTB 原则）。T4 的反例是测量学成本：
pass^k × 状态判分比单次跑分贵一个数量级，预算压力可能让行业退回便宜口径。

## 6 · 对 harness 的行动项 · Action items for the harness

1. **P77.R1（提案级）**：`data/watchlist.json` 的 trajectories 主题探针加宽（ai-scientist / autonomous-research /
   wet-lab / lab-in-the-loop），下期验证 trajectories 簇能否脱离 1 源状态。
2. **P77.R2（核对级）**：M3.19 增补一行"基准版本变量"注记（跨 semver 比较无效），引用本周边信号 4——
   走提案流程，不直改 core/。
3. **P77.R3（观察级）**：VISTA 类多模态上下文工程——登记观察；M1 预算语义多模态扩展不在本库范围。
4. **P77.R4（已落地）**：管线三项升级（判别性打分/源上限/噪声惩罚 + 周际 delta）即本轮完成，见 §7。

## 7 · 方法与数据附录 · Method & data appendix

**管线（确定性，M0.4 引擎只聚合不评论）：** `harness intel --root . --since <date>` 拉跟踪源 RSS →
`updates/intel.jsonl`（本窗口 2995 条）→ `harness trend --root . --write` 四簇聚合 → `updates/TREND.md` +
`data/trend-snapshot.json`（含周际 delta）。分析（本文）由 agent 撰写，承重声明逐条回一手源。

**P77 管线升级（本周落地）：** ① **判别性打分**——集群分 = 全局相关度 + 0.5×主题命中 + 0.3×判别词命中
（跟踪主题高度共现，行业簇与 harness 簇的 top 曾几乎相同）；② **源多样性上限**——每源最多 3 行 top
（OpenAI+HF 曾占一周条目的 ~75%）；③ **噪声惩罚**——标题含 8+ 位 hex 哈希的 commit-feed 条目 −1.0；
④ **周际动量**——快照记录对上一张快照的 count/recent delta，趋势综述从此读"变动"而非"总量"。

**窗口混杂声明（诚实边界）：** 本期 delta 为负（industry −305）主因是**窗口缩短**（上期数据窗更长），
不代表热度下降——周际 delta 从下一期起才有干净的同窗口可比性。trajectories 簇此前恒 0 是聚合缺陷
（已修），其 delta 记为"从 0 到 10"。

## 溯源表 · Provenance

| 声明 | 一手源 | 访问日期 |
|---|---|---|
| OpenAI 训练环境离线化 | [openai.com/index/securing-our-frontier-model-training-environment](https://openai.com/index/securing-our-frontier-model-training-environment) | 2026-11-07 |
| Agent Skills → AAIF（Linux 基金会） | [simonwillison.net/2026/Oct/22/donating-agent-skills](https://simonwillison.net/2026/Oct/22/donating-agent-skills/)（转述一手公告） | 2026-11-07 |
| SWE-Bench Pro 审计 | [openai.com/index/separating-signal-from-noise-coding-evaluations](https://openai.com/index/separating-signal-from-noise-coding-evaluations) | 2026-11-07 |
| SWE-Bench Pro V2 | 第三方转述（*unverified*，未读原始发布页） | — |
| Terminal-Bench 4.x | [tbench.ai](https://www.tbench.ai) · [github.com/laude-institute/terminal-bench](https://github.com/laude-institute/terminal-bench) | 2026-11-07 |
| wet-lab agent 测量 | [openai.com/index/measuring-how-ai-agents-handle-wet-lab-science](https://openai.com/index/measuring-how-ai-agents-handle-wet-lab-science) | 2026-11-07 |
| Copilot 置信度评测 | [microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/) | 2026-11-07 |
| VISTA / skills.sh / GraphRAG v3.3.0 | intel 流条目（feed 源，URL 见 intel.jsonl） | 2026-11-07 |

*引用即生命线：✅ = 本会话一手核验；feed 源 = 管线抓取的原始 URL（未二次核验）；*unverified* = 未读到原始发布页。*
