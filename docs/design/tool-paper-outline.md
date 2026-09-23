# Research Foodie — Paper Outline (论文大纲, arXiv-style systems paper)

> **中文速览**
> 本文是 **research_foodie**（本地优先、成本敏感、证据必可溯源的主动学术研究流水线）拟投 arXiv 的论文大纲。当前是**简明完整版**：标题/摘要占位、Keywords、逐节大纲（引言→相关工作→系统设计→评测→讨论→结论）与已验证的参考文献草稿。每节标注"已实测数据 / 待补实验"，并以 `[PLAN]` 标记未来扩充。诚实性规则沿用 AGENTS.md：数字带 `as of` 日期、方向性结论标注、无法验证的引用标 *unverified*。全部引用来自本仓库已核验来源（PROGRESS U/LEDGER 行）。

- `Updated`: 2026-09-22
- `Status`: **Outline v2** — tuned from v1: S22–27 results folded in (self-evolution E-3/E-4/E-5 implemented, L-1/L-2/L-3/D-3 delivered, free-model 401 root-cause + resolution, first live run on the free base), stale `[PLAN]` markers moved to measured, §7 numbers refreshed with 2026-09-22 live runs, `autoresearch` (L5) + run-memory + key-hygiene added, E-1/E-2/E-2b marked verified. Draft stays `docs/paper/research-foodie-paper.md`; **bidirectional outline↔draft map added in §12** — each outline node ↔ one draft section, kept in step by the cadence.
- `Living doc`: §7 numbers in the draft are regenerated/verified by `python -m tools.eval.capability_report` (`_eval_out/capability_report.md`), which the WS-C self-evolution cadence refreshes each run
- `Language`: English master + 中文速览; later draft bilingual-ready
- `Target`: arXiv (cs.CL / cs.AI), systems / applied-NLP track

---

## 0. 如何用这份大纲 / How to use this outline

每节 = 一段摘要式骨架：**已写好的句子直接可用**，`[…]` 括注的是写作时需填的占位，`[PLAN]` 是待补实验。正文分四个工作流未来成文：WS-A（核心流水线 Phase L）、WS-C（自演化 Phase X）、WS-D（模型路由 Phase D）、WS-B（web 前端 Phase F），本文大纲以 **WS-A + WS-C** 为主叙事。

---

## 1. Title / title (draft)

> **Research Foodie: A Local-First, Cost-Sensitive, Citation-Mandatory Survey Pipeline with Evidence-Grounded Drafting and Honest Self-Evaluation**

替补：`Evidence-Grounded Academic Survey Generation under a Zero-Key, Local-First Budget`；`Always-Grounded: … Gate, Judge, Publish`. 最终随评测结果定（突出"citation-mandatory + honest variance"）。

## 2. Abstract / 摘要 (planned, ~180–250 words)

逐一写清六件事（成稿为一段流）：
1. **问题**：通用 LLM 综述生成器会编造引用（GPT-4o 编造率 78–90%，见 [12]；OpenScholar Nature 实测），且黑盒系统不可审计。
2. **主张**：本工具把"每个事实性声明必须溯源到具体论文+段落"当作**强制约束**（L6 确定性门）+ 双层评审（机械门 + 16 维 AI 判题）做成可复现流水线。
3. **设计**：L0–L6 分层；LangGraph 状态机 `S_lit→S_org→S_write→S_final→gate→judge`；可插拔发现 rails（seed / arXiv 实时 / orx）；接地抽取式 QA 节点；写时反幻觉过滤（5-gram 接地）。**编排层含 O*（并行 `autoresearch`，无关工作区/多方向/证据并集）**（S26）。
4. **成本面**：核心环 ≈$0（免费托管模型 `opencode/big-pickle` + 免费 arXiv API + 本地 MinerU）。
5. **实测（as of 2026-09-22，free 基座已打通）**：mock 34/34；health check **GREEN（exit 0）**（mock+pools+arxiv_probe+gate_coverage 23/23）；QA 面板 n=31 correctness 4.23 / groundedness 4.45、抽取式路径 12/13；**live proxy trio（2026-09-22 全流程真实跑分）Total 3.65（P-A 4.31 / P-B 3.25 / P-C 3.38）**；30 话题判题电池 Total 3.13（22/30 有证据池）；判题噪音 P-A 3.88±0.53（冻结基线）。
6. **诚实性**：给出方差、覆盖率、失败单元（8 个空池、PubMedQA yes/no 8/14）、**P-C live −1.7σ 单轮 flagged（E-3 待 2–3 轮确认）**，明确方向性结论与 ≥300B 判题限制。

## 3. Keywords

`survey generation · evidence grounding · hallucination prevention · LLM evaluation · local-first · citation verification · DAS-Bench · self-evolution`

## 4. Introduction / 引言

1. **背景**：LLM 时代"深度研究"工具（OpenResearch/orx [1]、STORM [2]、PaperQA2 [3]、Tongyi DeepResearch [13]、OpenScholar [12]）把综述变成了自动化管线；但**事实性与可审计性**成为主缺口。
2. **问题陈述**：三个子问题——(a) 引用幻觉（GPT-4o 编造 78–90% [12]）；(b) 判题/评测不可复现（噪声、模型漂移、无方差记录）；(c) 高成本门槛（云模型/GPU）排除了本地/低成本用户。**Plus（S24–25 教训）**：长跑工具的真实墙不是质量而是**韧性**——key 墙（401 阻塞）、断线断电丢账。故系统把"断电可续、账目可审、限流可探测"放进设计而非售后。
3. **我们的方法**：本地优先 + 零 key + 每声明强制溯源 + 机械门/AI 门/人门三层 + 自测（方差感知阈值）。
4. **贡献（Contribution statement）**（5 条，成稿时对应用户要求 + S24–27 新增）：
   - C1 一套**以接地为第一约束**的综述流水线：5-gram 写时过滤 + L6 确定性门 + **门覆盖变异测试（23/23 杀灭）** + 16 维判题，杜绝无源声明入稿。
   - C2 一个**成本近零**的端到端实现（免费模型 + 免费 API + 本地解析），在 CPU-only 主机跑通并给出完整复现命令（runbook）；**2026-09-22 live 三篇代理全流程 3–5 分钟/篇**。
   - C3 一套**自演化测量机制**（Phase X E-1..E-5）：外部测量触发、方差感知阈值、冻结基线、门覆盖变异测试、**E-3 调试票板 / E-4 依赖台账 / E-5 防坍缩金标配额 + 晋升规则**——让"系统变好/变坏"可被数据判断，而非感觉。
   - C4 **运行韧性**：断线续跑（run-memory ledger）、D-5 密钥卫生强制审计、client 401 fail-fast——长跑不因断电/限流损失，账目可审（S24–25）。
   - C5 诚实评测报告法：判题噪音、覆盖失败、模型边界（PubMedQA 8/14）、**单轮方差旗标（P-C −1.7σ 待证）**全部显式报告，不隐瞒失败单元。核心环 **≈$0**，免费基座 live 打通（S26b–27）。
5. **组织（paper organization）**：简述后续章节。

## 5. Related Work / 相关工作

按 P3 评测轴组织的对比（每行给 [n] + 一句差异）：
- **STORM** [2]（NAACL 2024, arXiv:2402.14207）+ **Co-STORM** [21]（arXiv:2408.15232）：多视角大纲 + 检索式写作；FreshWiki 实测 **+25% organized / +10% coverage**；无强制接地门、无判题门 → 借大纲式样，加 grounding 约束。
- **OpenResearch / orx** [1]（**无 arXiv 论文**，repo `alphaXiv/openresearch-cli`）：agent 编排 + alphaXiv/OpenAlex 检索；不承诺每声明可溯源 → 借发现 rail 式样，保留 LangGraph 确定性路径。
- **PaperQA2** [3]（arXiv:2409.13740, Apache-2.0）：**RCS 检索重排** + 引用核验 + **retraction check**；未绑定免费模型路线 → 借 claim+quote 证据式样 + RCS 最小镜像（L4 头号自研缺口）。
- **DAS / DAS-Bench** [4]（arXiv:2608.18034，**已核实**）：30 话题/16 轴；**主对比全 30 话题 DAS 4.34 ≈ Human ref 4.34**（vs Naive RAG 4.03、Gemini-DR 3.92、GPT-DR 3.68）；判题规范 verbatim 借鉴，官方 harness **未运行**（自实现判题，方向性）；**方法代码仍未开源**；≥300B 判题 = 限制。
- **商用深度研究层**（**全 cloud-only**）：OpenAI Deep Research [26]（HLE 26.6% 系 2025-02 启动期数字，勿当"当前"）、Gemini Deep Research [28]、Perplexity Deep Research [31]、Grok DeepSearch、NotebookLM/Gemini Notebook [29]（语料接地、与我们姿态最近）；**DRBench [25] 实测：引用 URL 幻造 3–13%、不可解析 5–18%、"引得多≠可靠"**；**《Science》并无 Deep Research 人类评测论文**（量化评测活在 arXiv：DRACO [26]/ReportEval [27]/Rao [25]）。
- **证据/检索基础件**：**Semantic Scholar S2AG API** [30]（免费：引用图 + relevance search ≤1000 + SPECTER2 嵌入可下载）、**Grobid**（Apache-2.0，纯 CPU 官方镜像）、**MinerU** [5]（arXiv:2409.18839，在用）、PaddleOCR-VL [19]、Elicit/Consensus/Scite/AlphaXiv（付费/覆盖层）——构成 **L1/L2 低/零成本补丁层**。
- **Tongyi DeepResearch** [13]（arXiv:2510.24701，**3.3B active MoE 最便宜本地档**）；**OpenScholar** [12]（**Nature 650:857, 2026-02**，GPT-4o 幻觉基准，OpenScholar-8B >GPT-4o 6.1%）——"可理解高引用幻觉"与"免费档能力上限"锚点。
- **判题与自演化方法学**：**GEPA/DSPy** [15]、**Seddik** [16]、**Huang** [17]；**Tyen** [18]（arXiv:2311.08516：判"对不对"≠找"错在哪"→ 判题必须配机械验位）；**JudgeLM** [22]（bias+swap/ref 缓解）/ **MT-bench** [23]；**Schroeder & Wood-Doughty** [24]（单样本判题随 seed/temp 漂移 → **median-of-N 背书**）。
- **空缺（research gap）**：现有系统或强能力（云/昂贵）或弱接地；**没有一套在 ≈$0、CPU-only、强制源码下达到可审计质量且自评"带噪声地诚实"** 的公开实现 —— 这是本文生态位。

**5.1 工具综述对照表（system survey table）** — 成稿配 `tab:tools`，列为：系统 | 接地机制（grounding）| 判题 / 评测 | 预算·硬件姿态 | 与本文关系：

| System [n] | Grounding mechanism | Evaluation / judge | Budget posture | Relation to ours |
|---|---|---|---|---|
| STORM [2] | none mandatory | none | cloud LLM | borrow perspective-outline; we add hard gate |
| Co-STORM [21] | none mandatory; human-in-the-loop | n/a | cloud LLM | collaborative mind-map concept (L3) — not core |
| OpenResearch/orx [1] | alphaXiv full-text retrieval; no per-claim commit | none reported | agentic, cloud | borrow discovery rail; keep deterministic path |
| PaperQA2 [3] | claim + verbatim quote + cite-verify + retraction check | LitQA2 | paid models | borrow evidence style + minimal RCS mirror |
| DAS-Bench [4] | n/a (benchmark) | 16-axis frozen ≥300B rubric | eval harness | adopt rubric verbatim; judge self-implemented (directional) |
| OpenAI Deep Research [26] | agent plan → browse → cited report; no mandatory provenance | DRBench: **3.5% hallucinated URLs** | cloud, subscription | capability ceiling; not auditable/open |
| Gemini Deep Research [28] | plan → execute → cited report | DRBench: **13.3% hallucinated URLs** (highest) | cloud, free/paid tiers | free to try; worst measured citation health |
| NotebookLM / Gemini Notebook [29] | corpus-grounded, inline citations | n/a | cloud SaaS | closest grounding posture; sources-only scope |
| Perplexity DR [31] | agentic search-then-synthesize; numbered cites | fabricated-attribution incidents | cloud, paid | fast; trust self-published |
| Tongyi DeepResearch [13] | n/a¹ | n/a¹ | open (Apache-2.0); 3.3B active | free-lane capability ceiling anchor |
| OpenScholar [12] | 45M-paper datastore + self-feedback loop | Nature; GPT-4o 78–90% fabricated cites | 8B model cheap / datastore heavy | hallucination frontier anchor |
| S2AG API [30] | citation graph + relevance search + SPECTER2 embeddings | n/a | **free** | L1 metadata/embedding patch |
| **Ours** | write-time 5-gram filter + zero-LLM L6 gate (mutation-tested 23/23) + 16-axis judge on top | DAS-Bench 16 axes; L6 1.00; mock/real 34/34; live trio 3.65 | **≈$0, CPU-only, free hosted model** | the ≈$0 + mandatory provenance + self-measuring niche |

> ¹ 以原始论文/公开评测为准，未在本仓库逐条复跑（见 §12 诚实边界）。

## 6. System Design / 系统设计

> 大纲即"系统说明书压缩版"；成稿时配图 `fig:architecture`（L0–L6 分层 + 状态机）+ `fig:loop`（自演化循环）。

1. **总览**：L0–L6 分层（见 PROJECT.md §2）；两种路由模式（survey 图 vs `seed_id` 接地抽取式 QA 节点）。`[PLAN]` 配一张 Mermaid/矢量图。
2. **发现（L1）**：三 rails `seed | arxiv | orx`（`S_LIT_BACKEND` 可切）；arXiv 免费 API ~1.1 s（2026-09-16 实测）；失败链 orx→arxiv→seed 保底；无元数据湖（缺 DAS-2M）→ 精度受 arXiv 相关性 top-K 限制。
3. **证据与解析（L2）**：MinerU PDF→Markdown（`-m txt` 窗口 ≤6 页，K12 规避）；`resolved_evidence()` 多论文证据池。
4. **编排（L3–L5）**：LangGraph 状态机；STORM 式大纲；逐 paper 接地 claims（`paper_id` 标记）；逐节 survey 写作；`_finalize` 产出 Abstract/Evidence Table/References + audit annex。**并行轨道（L5, `autoresearch`）**（S26）：多方向独立子图、隔离工作区、证据并集、模型无关——与 OpenResearch/orx [1] 的 agent 并行对齐但保持 LangGraph 确定性路径与门。
5. **Run 韧性（run-memory ledger）**（S24–25）：每次运行落 `_eval_out/ledgers/` 账目；断线/断电后基于指纹（profile+ids）续跑，`--no-resume` 强制重跑；原子写 + hydrate/replay。客户端对 key 缺失/401 **fail-fast**（root-caused: 401 系服务端额度阻塞，非本工具缺陷）。
6. **机械门（L6, zero-LLM）**：`validate.py`——结构 / 引用形态（arXiv/DOI）/ **5-gram 逐字接地**（写时丢弃未接地声明）/ 双语 / 多论文检查 + JSON 解析器（codewall 兼容）。**门覆盖变异测试**（E-2b）：23 变异体、100% 杀灭（2026-09-22 复跑 GREEN）。
7. **AI 判题门**：DAS-Bench 16 轴 rubric（BSC·MAR·TSQ·HDQ verbatim from `evaluation_protocol.md`）；`judge_model` 记录实际判题模型；≤40K 字符视图。**判题矩阵 harness（D-3）**：`judge_matrix` 多轴 × 多轮 × median-of-N。
8. **自演化（WS-C，Phase X）**：E-1 基线冻结（`baselines.json`）→ E-2 方差感知 health check（exit 0 GREEN）→ E-2b 门覆盖变异测试（23/23）→ E-3 调试票板（one-open-per-component）→ E-4 依赖/版本台账 → E-5 防坍缩（real-gold 金标配额 ≥half、N≥3∧Δ≥2σ∧无回归晋升）。**设计规则：演化只能由外部测量触发、阈值方差感知**（详见 `docs/design/self-evolution-mechanism.md`）。**E-7（R 期）**：DSPy/GEPA 自动演进 + 判题人交换（需强 reflection LM）。
9. **模型接入与路由（WS-D，Phase D）**：角色级 profiles（draft|qa 廉价 lane vs judge 强模型 lane）；**三选项** `free-opencode`（默认）| `openai-compat`（任意 OpenAI 兼容）| `judge-strong`（draft 免费 + judge 升级）——实现 + 测试覆盖（S23）；key 只走环境变量，**D-5 密钥卫生审计 33→39 守卫**（S25）；免费模型默认且 live 已打通（S26b–27）。
10. **溯源（D-4）**：每个 report（bench / health / sprint / judge matrix / capability snapshot）带 model·judge_model·温度·profile·as-of 时间戳——任意数字可回溯到产出它的那次 run。

## 7. Evaluation / 评测

> 所有数字 `as of 2026-09-19/20`（sync 后注：`as of 2026-09-22` 已含 live 基座跑分）。诚实性原则：方向性、不 head-to-head vs 官方 DAS 榜（缺 ≥300B 冻结判题）。网络/判题条件变化会标出。

**7.1 纵切正确性（Pipeline tests）**：mock 34/34 · real `opencode/big-pickle` 34/34（≈2 篇真论文：Liang 2304.02819 WASM、Weber-Wulff 2306.15666，全环 PASS）。度量：正确章节归属、verbatim quotes、score 1.0 / judge=pass。`self_check.ps1` ~15 s 跑全离线网。

**7.2 接地抽取式 QA（Track C）**：面板 n=31，correctness 4.23 / groundedness 4.45 / 24/31；抽取与上下文路径 n=13 → 12/13；Qasper 外部金标 5/5 c=5.00 g=5.00；PubMEDQA yes/no 8/14 = 模型边界（诚实报告）。

**7.3 16 维判题（DAS-Bench 轴）**：canonical trio P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13（冻结基线）；30 话题电池 n=10 Total 3.13（BSC 3.08 / MAR 2.67 / TSQ 3.05 / HDQ 3.73）；TSQ 2.42→3.17（Session 13 per-section 写作增益）。**live（2026-09-22，free 基座连通后首次全流程真实跑分）**：P-A 4.31 / P-B 3.25 / P-C 3.38 → family **Total 3.65**（BSC 3.83 / MAR 2.92 / TSQ 3.58 / HDQ 4.25）；L6 1.00 全过、DAS-16 覆盖 16/16、~275–315 s/篇 → 36 场景全量 ≈ 2.5–3h（可后台/夜间）。MAR 低位 = 图/表/排版（纯 Markdown 渲染限制，诚实标注）。

**7.4 自演化测量（Phase X 设计验证）**：P-A 判题噪音 0.53 → 2σ≈±0.50 的 FAIL 阈值含义。**health_check GREEN（exit 0, 2026-09-22）**：mock 34/34 · pools 22/30（14 满）· arxiv probe reachable · gate_coverage 23/23 · judge sanity 对缓存手稿 live 判题全 PASS。`test_capability.py` 47 asserts、`test_evolution.py` 31 asserts 全绿。

**7.5 成本与延迟（Cost & latency）**：核心环 ≈$0；P-A 全环 121.7 s / 149.8 s（real，免费模型）；**live trio ~275–315 s/篇（3-paper 池）**；`[PLAN]` 补正式 cost/latency 表（token 计数、API 调用数）——usage 字段已回传，S27 起可统计。

**7.6 消融/待补（Ablations, P5）**：**(a) 已完成**——接地门 ON/OFF 对照（fixture 8 un-grounded → 0 leakage、5 grounded 保留 5/5、0 false drops）+ E-2b 变异杀灭 23/23；(b) **已完成**——rail 切换对 pools 覆盖影响、30 话题 73% 覆盖（14 满 / 8 partial / 8 empty）；(c) **已完成（median-of-N）**——P-C 分散 0.19、0.31 mean 单 draws；(d) judge swap（free vs ≥300B）**待 ≥300B key**（harness 已实现、mock 验证）。

## 8. Discussion / 讨论

- **Claims 与约束**：这三层门没替代人工评审——定位是"防伪+降噪"，不主张自动发布（README/AGENTS 明确）；自演化 E-3–E-5 只写 ledger、不写代码/不自动 commit，晋升由人执行。
- **局限性（诚实清单）**：
  1. 判题 Free 模型权重方向性，MAR Layout 轴需 ≥300B page-aware 判题（阻塞 keys/GPU）。
  2. 8/30 话题无证据池（arXiv 相关性与解析上限 = 实测属性，非静默）。
  3. PubMedQA yes/no 8/14 = 明确模型边界。
  4. 单机/CPU-only；无元数据湖与 GAIA 批量（HF gating）。
  5. 自演化 E-7 依赖强 reflection LM，仍属 R 期规划。
  6. 免费基座跑分当评委存在**单轮漂移**（P-C −1.7σ 单轮 flag，需 E-3 2–3 轮确认才开票）——这正验证了 median-of-N + 方差阈值的必要。
- **给社区的启示**：成本-接地-可审计三者可同时满足一部分——把"强制溯源"做成结构约束而非 prompt 约束是可行路径（写时过滤的证据：抓取到伪造 claim 被 gate 拦下）。

## 9. Conclusion / 结论

复述贡献 C1–C5 + 一句话总结：**"可审计的、≈$0 的、自带诚实测量的综述流水线是可构建的；其边界（判题模型、证据覆盖、单轮方差）应显式暴露而非隐藏。"** + 未来工作（≥300B judge、DAS-2M 湖、GAIA、Track B 中文证据层、R 期自动演进、36 场景全量跑分收进 §7.3）。

## 10. References / 参考文献（draft, IEEE-style numbered）

> 均来自本仓库已核验来源（PROGRESS U 行与 TOOL-COMPARISON）。访问日期 2026-09-20（新增条目 21–31 为 2026-09-23）。*unverified* 处为仍需一手复核的条目。

1. OpenResearch / orx (2025), meta-repo research/open-reserch+orx; CLI `orx discover`. (镜像官方仓库)— **官方仓库；无 arXiv 论文**（2504.01874 系代数几何数学稿，勿引）
2. Y. Shao et al., "Assisting in Writing Wikipedia-like Articles from Scratch with Large Language Models," NAACL 2024, arXiv:2402.14207.
3. PaperQA2, arXiv:2409.13740 (retraction check; LitQA2 superhuman).
4. J. Xu et al., DAS: Efficient and Scalable Collaboration between Agents (tech survey), arXiv:2608.18034; DAS-Bench 30 topics / 16 criteria, repo ZhikaiXu24/DAS. —— **ID 已核实**（2026-09-23）；方法代码 "To be released" 未开源；数据可能含合成内容
5. MinerU open-source solution for precise document extraction, arXiv:2409.18839. (repo company verified) —— **ID 已修正 2026-09-23**（旧 2410.17381 作废）
6. LangGraph (LangChain), docs.langchain.com. (library)
7. DAS-2M ≈2M arXiv papers (2020-01→2026-06), 8 field groups, HuggingFace. (dataset, 2026-08)
8. Qasper qasper-train-dev-v0.3.tgz (dev 281 papers; keys = arXiv IDs), allenai. (dataset)
9. PubMedQA: qiaojin/PubMedQA (HF). (dataset)
10. SciQ: AllenAI (provided-context mode). (dataset)
11. GAIA benchmark (466 Qs). (benchmark)
12. H. Chen et al. (OpenScholar), *Nature* vol. 650, pp. 857-863, **2026-02-04**, DOI 10.1038/s41586-025-10072-4. (GPT-4o citation-hallucination anchor; OpenScholar-8B >GPT-4o 6.1%) —— 出版年已修正为 2026
13. Tongyi DeepResearch, 30.5B total / 3.3B active, arXiv:2510.24701 (Apache-2.0). (open baseline)
14. Jiang et al., "STORM...", arXiv reference verified in TOOL-COMPARISON (feas 5 · val 4). —— 与 [2] 一致，一实一备
15. GEPA (vs GRPO up to 35× cheaper on text feedback), arXiv:2507.19457.
16. Seddik et al., arXiv:2404.05090. (self-evolution anti-collapse / provenance)
17. Huang et al., "Efficient Optimization..." arXiv:2310.01798. —— 主题：量化评测驱动优化 (外部测量触发) —— *unverified 精确标题待一手复核*
18. Tyen et al., "Why do LLMs quote sources?" arXiv:2311.08516. —— LLM-as-judge 要找推理错误而非下整体结论（**2311.16502 系 MMMU，勿混**）—— **ID 已核实**
19. PaddleOCR / PaddleOCR-VL, arXiv:2510.14528 (109 langs). (OCR engine)
20. Lloyd et al. (cookbooks LRM judging measure), 2025. —— *unverified*
21. Y. Moon et al. (Co-STORM), arXiv:2408.15232. (IEEE S&P 2026 / arXiv 2024, MIT) —— **新增**
22. L. Zhu et al. (JudgeLM), arXiv:2310.17631. —— **新增**（judge bias + swap/ref 缓解）
23. M. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2024, arXiv:2306.05685. —— **新增**
24. B. Schroeder & B. Wood-Doughty, arXiv:2412.12509. —— **新增**（seed/temp 改变评级 → median-of-N 判题背书）
25. Rao et al., "Agentic AI Reviews: Final Verdicts Are More Reliable but Not Always Better," 2026; + urlhealth (MIT, 83-line URL self-heal). arXiv:2604.03173. —— **新增**（商用 DR 引用幻觉 3–13% URL / 5–18% 不可解析；OpenAI 3.5% 最低 / Gemini 13.3% 最高）
26. DRACO benchmark (deep-research agent code compilation), arXiv:2602.11685. —— **新增**；OpenAI Deep Research 产品层参见产品官方页
27. DeepResearch-ReportEval (report-grounded metrics), arXiv:2510.07861. —— **新增**
28. Gemini API "Deep Research" agent (official docs, GA 2026-03/04; 1M ctx + Google Search + MCP File Search). —— **新增**
29. NotebookLM / Gemini Notebook (official product docs; 2026-07 更名; 2026-06 Gemini 3.5+ code sandbox + PDF/PPTX artifacts). —— **新增**
30. Semantic Scholar S2AG API (official docs; free; relevance search ≤1000, batch 500 IDs / 9999 citations, SPECTER2 embeddings downloadable). —— **新增**
31. Perplexity Deep Research (official docs; "Search-as-Code", Advanced). —— **新增**

> 出版前必做：逐条跑 `tools/citation-verify` 复核 [4][14][17][19][20]；删除未核实条目；Google Scholar 搜索补充 2024–2026 同类 systems 论文保持 related-work 新鲜。21–31 已一次一手核对（2026-09-23），属"低风险"段。

---

## 11. / 中文速览 — 关键决策（用于扩张成稿）

- 论文定位一句话：**"把强制溯源从 prompt 约束升级为结构约束（write-time filter + L6 门），并在免费模型预算下把 '诚实评测' 做成可复现指标。"**
- 所有实验数字已在 `_eval_out/` 与 `docs/` 复现路径；**论文数字 = 复现命令清单 + 日期**（AGENTS 质量门）。
- Expansion roadmap（成稿顺序）：§7 补齐 cost/latency 表（usage 已回传）→ §5 已补 2026 系统（35c，商用层 + 证据基础件 + 判题方法学入表）→ §6 配图（architecture + loop + autoresearch 并行）→ IEEE refs 复核（剩余 [4][14][17][19][20]）→ 中译版摘要 → 36 场景全量 live 收进 §7.3。

---

## 12. Outline ↔ Draft bidirectional map (大纲↔正文 对应联动)

> **规则：大纲是主干，正文是展开。body 每节必须顶格标注 `(⇐ outline §X)`；outline 每节反向列 `→ draft §Y`。改大纲先，改正文后；新增数字先进大纲，再由 cadence 同步正文。** 序号不对齐（大纲 §0–§12 vs 正文 §1–§6）由本表消除歧义。

| Outline node | → Draft section | Notes / sync state |
|---|---|---|
| §0 How to use | (n/a, meta) | 不映射 |
| §1 Title | Draft H1 title | v2 未改标题 |
| §2 Abstract | Draft `Abstract` | ✓ synced (v2) |
| §3 Keywords | Draft `Keywords` | 一致 |
| §4 Intro (bg/problem/approach) | Draft `§1 Introduction` | ✓ synced: resilience problem + C4/C5 |
| §5 Related Work (§5.1 `tab:tools` survey + comparison) | Draft `§2 Related Work` (§2.1 survey · §2.2 comparison w/ ours row) | ✓ markers; table mirrored both sides (2026-09-22) |
| §6.1–6.3 Overview/Discovery/Evidence | Draft `§3.1–3.3` | 一致 |
| §6.4 Orchestration (+autoresearch) | Draft `§3.4` (+`O*` worker) | ✓ autoresearch paragraph; `O*` subsection `[TODO]` |
| §6.5 Run-resilience | Draft `§3.5` | ✓ run-memory subsection |
| §6.6 L6 gate + mutation test | Draft `§3.6` | 一致 (23/23) |
| §6.7 AI judge + D-3 matrix | Draft `§3.7` | ✓ judge_matrix mention |
| §6.8 Self-evolution E-1..E-5 | Draft `§3.10` | ✓ implemented; E-7 R-phase |
| §6.9 Model routing / profiles | Draft `§3.8` | ✓ 3-option profiles + key hygiene (D-5) |
| §6.10 Provenance (D-4) | Draft `§3.9` | 一致 |
| §7.1 Vertical & self_check | Draft `§4.1` | 一致 |
| §7.2 Track C | Draft `§4.2` | 一致 |
| §7.3 16-axis judge | Draft `§4.3` | ✓ live trio + 30-topic battery (as of 2026-09-22) |
| §7.4 Self-evol measurement | Draft `§4.4` | ✓ health GREEN exit 0 + coverage |
| §7.5 Cost & latency | Draft `§4.5` | `[PLAN]` usage table, live ~275–315s/篇 |
| §7.6 Ablations a–d | Draft `§4.6` | ✓ a/b/c done, d deferred (≥300B) |
| §8 Discussion | Draft `§5 Discussion` | ✓ P-C −1.7σ variance-as-evidence (lim 6) |
| §9 Conclusion | Draft `§6 Conclusion` | ✓ C1→C5 + live Total 3.65 |
| §10 References | Draft `References` | *unverified* [4][14][17][18][19][20] both sides |
| §11 roadmap (draft-numbers refer here) | n/a | roadmap 序号以正文 § 为准 |

---

*Lineage: outline v1 authored 2026-09-20 from PROJECT.md / CAPABILITY-STATUS.md / TOOL-COMPARISON.md / PLAN.md / self-evolution-mechanism.md measured numbers; v2 tuned 2026-09-22 by folding in S24–27 delivered results (autoresearch, run-memory, key hygiene, 401 root-cause, live trio 3.65, health GREEN, ablation a/b/c done) and adding §12 bidirectional map. All quantitative claims have a runbook `$PY` command (docs/setup-runbook.md §3) for reproduction.*