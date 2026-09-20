# Research Foodie — Paper Outline (论文大纲, arXiv-style systems paper)

> **中文速览**
> 本文是 **research_foodie**（本地优先、成本敏感、证据必可溯源的主动学术研究流水线）拟投 arXiv 的论文大纲。当前是**简明完整版**：标题/摘要占位、Keywords、逐节大纲（引言→相关工作→系统设计→评测→讨论→结论）与已验证的参考文献草稿。每节标注"已实测数据 / 待补实验"，并以 `[PLAN]` 标记未来扩充。诚实性规则沿用 AGENTS.md：数字带 `as of` 日期、方向性结论标注、无法验证的引用标 *unverified*。全部引用来自本仓库已核验来源（PROGRESS U/LEDGER 行）。

- `Updated`: 2026-09-20
- `Status`: Outline v1 expanded into **Draft v1** → `docs/paper/research-foodie-paper.md`; outline kept as the section map / roadmap
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
3. **设计**：L0–L6 分层；LangGraph 状态机 `S_lit→S_org→S_write→S_final→gate→judge`；可插拔发现 rails（seed / arXiv 实时 / orx）；接地抽取式 QA 节点；写时反幻觉过滤（5-gram 接地）。
4. **成本面**：核心环 ≈$0（免费托管模型 `opencode/big-pickle` + 免费 arXiv API + 本地 MinerU）。
5. **实测**：mock 34/34 · real 34/34（P-A 例 121.7 s）；QA 面板 n=31 correctness 4.23 / groundedness 4.45、抽取式路径 12/13；30 话题判题电池 Total 3.13（22/30 有证据池）；判题噪音 P-A 3.88±0.53（基准线）。
6. **诚实性**：给出方差、覆盖率、失败单元（8 个空池、PubMedQA yes/no 8/14），明确方向性结论与 ≥300B 判题限制。

## 3. Keywords

`survey generation · evidence grounding · hallucination prevention · LLM evaluation · local-first · citation verification · DAS-Bench · self-evolution`

## 4. Introduction / 引言

1. **背景**：LLM 时代"深度研究"工具（OpenResearch/orx [1]、STORM [2]、PaperQA2 [3]、Tongyi DeepResearch [13]、OpenScholar [12]）把综述变成了自动化管线；但**事实性与可审计性**成为主缺口。
2. **问题陈述**：三个子问题——(a) 引用幻觉（GPT-4o 编造 78–90% [12]）；(b) 判题/评测不可复现（噪声、模型漂移、无方差记录）；(c) 高成本门槛（云模型/GPU）排除了本地/低成本用户。
3. **我们的方法**：本地优先 + 零 key + 每声明强制溯源 + 机械门/AI 门/人门三层 + 自测（方差感知阈值）。
4. **贡献（Contribution statement）**（3–4 条，成稿时对应用户要求）：
   - C1 一套**以接地为第一约束**的综述流水线：5-gram 写时过滤 + L6 确定性门 + 16 维判题，杜绝无源声明入稿。
   - C2 一个**成本近零**的端到端实现（免费模型 + 免费 API + 本地解析），在 CPU-only 主机跑通并给出完整复现命令（runbook）。
   - C3 一套**自演化测量机制**（Phase X）：外部测量触发、方差感知阈值、冻结基线、门覆盖变异测试——让"系统变好/变坏"可被数据判断，而非感觉。
   - C4 诚实评测报告法：判题噪音、覆盖失败、模型边界（PubMedQA 8/14）全部显式报告，不隐瞒失败单元。
5. **组织（paper organization）**：简述后续章节。

## 5. Related Work / 相关工作

按 P3 评测轴组织的对比（每行给 [n] + 一句差异）：
- **STORM** [2]（NAACL 2024）：多视角大纲 + 检索式写作；无强制接地门、无判题门 → 我们借大纲式样，加 grounding 约束。
- **OpenResearch / orx** [1]：agent 编排 + alphaXiv 全文检索；不承诺每声明可溯源 → 我们借发现 rail 式样，保留 LangGraph 确定性路径。
- **PaperQA2** [3]：检索重排 + 引用核验 + retraction check；未绑定免费模型路线 → 我们借 claim+quote 证据式样。
- **DAS / DAS-Bench** [4]：arXiv:2608.18034，30 话题/16 轴；判题规范 verbatim 借鉴，官方 harness **未运行**（自实现判题，方向性）；≥300B 判题 = 限制。
- **Tongyi DeepResearch** [13]（Apache-2.0 开放）；**OpenScholar** [12]（Nature 650:857，GPT-4o 幻觉基准）—— 作为"可理解高引用幻觉"的锚点。
- **MinerU** [5]、**DAS-2M**（HF 2026-08）、**GAIA**（466 Qs）——解析/数据/评测基准。
- **GEPA/DSPy** [15]、**Seddik** [16]、**Huang** [17]、**Tyen** [18] —— Self-Evolution 方法学（外部触发、防坍缩、评估噪音）。
- **空缺（research gap）**：现有系统或强能力（云/昂贵）或弱接地；**没有一套在 ≈$0、CPU-only、强制源码下达到可审计质量且自评"带噪声地诚实"** 的公开实现 —— 这是本文生态位。

## 6. System Design / 系统设计

> 大纲即"系统说明书压缩版"；成稿时配图 `fig:architecture`（L0–L6 分层 + 状态机）+ `fig:loop`（自演化循环）。

1. **总览**：L0–L6 分层（见 PROJECT.md §2）；两种路由模式（survey 图 vs `seed_id` 接地抽取式 QA 节点）。`[PLAN]` 配一张 Mermaid/矢量图。
2. **发现（L1）**：三 rails `seed | arxiv | orx`（`S_LIT_BACKEND` 可切）；arXiv 免费 API ~1.1 s（2026-09-16 实测）；失败链 orx→arxiv→seed 保底；无元数据湖（缺 DAS-2M）→ 精度受 arXiv 相关性 top-K 限制。
3. **证据与解析（L2）**：MinerU PDF→Markdown（`-m txt` 窗口 ≤6 页，K12 规避）；`resolved_evidence()` 多论文证据池。
4. **编排（L3–L5）**：LangGraph 状态机；STORM 式大纲；逐 paper 接地 claims（`paper_id` 标记）；逐节 survey 写作；`_finalize` 产出 Abstract/Evidence Table/References + audit annex。
5. **机械门（L6, zero-LLM）**：`validate.py`——结构 / 引用形态（arXiv/DOI）/ **5-gram 逐字接地**（写时丢弃未接地声明）/ 双语 / 多论文检查 + JSON 解析器（codewall 兼容）。
6. **AI 判题门**：DAS-Bench 16 轴 rubric（BSC·MAR·TSQ·HDQ verbatim from `evaluation_protocol.md`）；`judge_model` 记录实际判题模型；≤40K 字符视图。
7. **自演化（WS-C，Phase X）**：E-1 基线冻结 → E-2 方差感知 health check → E-2b 门覆盖变异测试 → E-5 防坍缩/溯源下限 → E-7（R 期）DSPy/GEPA 自动演进 + 判题人交换。设计规则：**演化只能由外部测量触发**、阈值方差感知（详见 `docs/design/self-evolution-mechanism.md`）。
8. **模型接入与路由（WS-D，Phase D）**：角色级 profiles（draft|qa 廉价 lane vs judge 强模型 lane）；key 只走环境变量；免费模型默认。`[PLAN]` 实现中。

## 7. Evaluation / 评测

> 所有数字 `as of 2026-09-19/20`，来自 `_eval_out/`。诚实性原则：方向性、不 head-to-head vs 官方 DAS 榜（缺 ≥300B 冻结判题）。

**7.1 纵切正确性（Pipeline tests）**：mock 34/34 · real `opencode/big-pickle` 34/34（≈2 篇真论文：Liang 2304.02819、Weber-Wulff 2306.15666 全环 PASS）。度量：正确章节归属、verbatim quotes、score 1.0 / judge=pass。

**7.2 接地抽取式 QA（Track C）**：面板 n=31，correctness 4.23 / groundedness 4.45 / 24/31；抽取与上下文路径 n=13 → 12/13；Qasper 外部金标 5/5 c=5.00 g=5.00；PubMEDQA yes/no 8/14 = 模型边界（诚实报告）。

**7.3 16 维判题（DAS-Bench 轴）**：canonical trio P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13；30 话题电池 n=10 Total 3.13（BSC 3.08 / MAR 2.67 / TSQ 3.05 / HDQ 3.73）；TSQ 2.42→3.17（Session 13 per-section 写作增益）。MAR 低位 = 图/表/排版（纯 Markdown 渲染限制，诚实标注）。

**7.4 自演化测量（Phase X 设计验证）**：P-A 判题噪音 0.53 → 2σ≈±0.50 的 FAIL 阈值含义；`[PLAN]` E-2 health_check + E-2b gate_coverage（≥20 变异、100% 杀灭）的实验与数字。

**7.5 成本与延迟（Cost & latency）**：核心环 ≈$0；P-A 全环 121.7 s / 149.8 s（real，免费模型）；`[PLAN]` 补正式 cost/latency 表（token 计数、API 调用数）。

**7.6 消融/待补（Ablations, P5）**：`[PLAN]` (a) 接地门开/关对判题分的影响；(b) 发现 rail 切换（arsiv vs seed）对 pools 覆盖的影响；(c) 判题模型 swap（免费 vs ≥300B）后的分差；(d) 变化后复测（mutation/kill 率）。

## 8. Discussion / 讨论

- **Claims 与约束**：这三层门没替代人工评审——定位是"防伪+降噪"，不主张自动发布（README/AGENTS 明确）。
- **局限性（诚实清单）**：
  1. 判题 Free 模型权重方向性，MAR Layout 轴需 ≥300B page-aware 判题（阻塞 keys/GPU）。
  2. 8/30 话题无证据池（arXiv 相关性与解析上限 = 实测属性，非静默）。
  3. PubMedQA yes/no 8/14 = 明确模型边界。
  4. 单机/CPU-only；无元数据湖与 GAIA 批量（HF gating）。
  5. 自演化 E-7 依赖强 reflection LM，仍属 R 期规划。
- **给社区的启示**：成本-接地-可审计三者的取舍可同时满足一部分——把"强制溯源"做成结构约束而非 prompt 约束是可行路径（写时过滤的证据：抓取到伪造 claim 被 gate 拦下）。

## 9. Conclusion / 结论

复述贡献 C1–C4 + 一句话总结：**"可审计的、≈$0 的、自带诚实测量的综述流水线是可构建的；其边界（判题模型、证据覆盖）应显式暴露而非隐藏。"** + 未来工作（≥300B judge、DAS-2M 湖、GAIA、Track B 中文证据层、R 期自动演进）。

## 10. References / 参考文献（draft, IEEE-style numbered）

> 均来自本仓库已核验来源（PROGRESS U 行与 TOOL-COMPARISON）。访问日期 2026-09-20。*unverified* 处为仍需一手复核的条目。

1. OpenResearch / orx (2025), meta-repo research/open-reserch+orx; CLI `orx discover`. (镜像官方仓库)— **官方仓库**
2. Y. Shao et al., "Assisting in Writing Wikipedia-like Articles from Scratch with Large Language Models," NAACL 2024, arXiv:2402.14207.
3. PaperQA2, arXiv:2409.13740 (retraction check; LitQA2 superhuman).
4. J. Xu et al., DAS: Efficient and Scalable Collaboration between Agents (tech survey), arXiv:2608.18034; DAS-Bench 30 topics / 16 criteria, repo ZhikaiXu24/DAS. —— **arXiv ID 未来出版前再核**（数据可能含合成内容）
5. MinerU open-source solution for precise document extraction, arXiv:2410.17381. (repo company (verified) —— 版本待核 *unverified*)
6. LangGraph (LangChain), docs.langchain.com. (library)
7. DAS-2M ≈2M arXiv papers (2020-01→2026-06), 8 field groups, HuggingFace. (dataset, 2026-08)
8. Qasper qasper-train-dev-v0.3.tgz (dev 281 papers; keys = arXiv IDs), allenai. (dataset)
9. PubMedQA: qiaojin/PubMedQA (HF). (dataset)
10. SciQ: AllenAI (provided-context mode). (dataset)
11. GAIA benchmark (466 Qs). (benchmark)
12. H. Chen et al. (OpenScholar), *Nature* vol. 650, pp. 857-863, 2025, DOI 10.1038/s41586-025-10072-4. (GPT-4o citation-hallucination anchor)
13. Tongyi DeepResearch, 30.5B total / 3.3B active, arXiv:2510.24701 (Apache-2.0). (open baseline)
14. Jiang et al., "STORM...", arXiv reference verified in TOOL-COMPARISON (feas 5 · val 4). —— 与 [2] 一致，一实一备
15. GEPA (vs GRPO up to 35× cheaper on text feedback), arXiv:2507.19457.
16. Seddik et al., arXiv:2404.05090. (self-evolution anti-collapse / provenance)
17. Huang et al., "Efficient Optimization..." arXiv:2310.01798. —— 主题：量化评测驱动优化 (外部测量触发) —— *unverified 精确标题待一手复核*
18. Tyen et al., arXiv:2311.08516. —— LLM-as-judge 评估方法 —— *unverified 待核*
19. PaddleOCR / PaddleOCR-VL, arXiv:2510.14528 (109 langs). (OCR engine)
20. Lloyd et al. (cookbooks LRM judging measure), 2025. —— *unverified*

> 出版前必做：逐条跑 `tools/citation-verify` 复核 [4][14][17][18][19][20]；删除未核实条目；Google Scholar 搜索补充 2024–2026 同类 systems 论文保持 related-work 新鲜。

---

## 11. / 中文速览 — 关键决策（用于扩张成稿）

- 论文定位一句话：**"把强制溯源从 prompt 约束升级为结构约束（write-time filter + L6 门），并在免费模型预算下把 '诚实评测' 做成可复现指标。"**
- 所有实验数字已在 `_eval_out/` 与 `docs/` 复现路径；**论文数字 = 复现命令清单 + 日期**（AGENTS 质量门）。
- Expansion roadmap（成稿顺序）：§7 补齐 P5 消融与成本表 → §5 补 1–2 个 2026 系统 → §6 配图 → IEEE refs 复核 → 中译版摘要。

---

*Lineage: outline authored 2026-09-20 from PROJECT.md / CAPABILITY-STATUS.md / TOOL-COMPARISON.md / PLAN.md / self-evolution-mechanism.md measured numbers; all quantitative claims have a runbook `$PY` command (docs/setup-runbook.md §3) for reproduction.*