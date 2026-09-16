# research_foodie

**本地优先、成本敏感（核心成本≈$0）的主动式学术研究流水线**：输入一个研究问题（或一个受监控领域），输出一份**逐句可溯源到已解析论文**的草稿——每个事实claim都锚定原文逐字引文，先机械校验、后人工把关。

> English version: [`README.md`](README.md).

Updated: 2026-09-16 · 许可证：MIT

## 项目做什么

- 输入问题 → 输出**双语（英文 + 中文）**大纲驱动草稿，每个章节由证据驱动。
- 每个事实 claim 锚定本地已解析论文（arXiv）的**逐字引文**；确定性 5-gram 接地门在任何人审之前机械屏蔽幻觉引用。
- 以 LangGraph 状态机运行：`S_lit → S_org → S_write → S_final → L6 校验门 → P3 评审 → 人工`。
- **成本敏感**：核心链路用开源工具 + 免费/开放 LLM（核心成本≈$0）。

**不是什么**：不是黑盒"深度研究"产品——永不在无人闸门时自动交付稿件。机械校验先于 AI 评审；AI 修订、人工批准（蓝图 §0）。

## 流水线总览

```
[L0] 问题 / 领域监控
  ▼
[L1] S_lit  发现 rails（种子清单 · arXiv API · orx CLI）→ 候选
  ▼
[L2] 证据   MinerU PDF→Markdown → 多论文证据池（逐论文接地）
  ▼
[L3] S_org  分类学 + STORM 式大纲（节 + 要点）
  ▼
[L4] S_write 逐论文证据化 claims（逐字引文）→ 跨论文写作
  ▼
[L5] S_final 组装输出（来源清单 + 逐 claim 归属）
  ▼
[L6] 门控  确定性校验 → DAS-Bench 式 AI 评审 → 人工核签
  ▼
稿件  （Zotero + Pandoc + LaTeX）· Track B：OCR + 翻译 + 专家闸门
```

当前交付 **P2 最小纵切**（问题 → 接地草稿 → 校验产物）已端到端闭环；主动式 *stale → 重新发现* 循环与 DAS-2M/实时大规模扫描为路线图项目。

## 快速上手

环境为 conda env `ds0509`（Python 3.12，Windows）。请显式使用该解释器：

```powershell
$PY='C:\Users\data\miniconda3\envs\ds0509\python.exe'
```

**运行集成测试**（mock = 秒级确定性回归；real = 完整 opencode LLM 链路）：

```powershell
& $PY -m tools.pipeline.test_pipeline mock      # 25/25 PASS
& $PY -m tools.pipeline.test_pipeline real      # 默认模型 opencode/big-pickle（约 8 分钟，10 次 LLM 调用）
```

**示例问题：** *"GPT detectors bias against non-native English writers"*（Liang et al. 2023）与 *"How reliable are automatic detection tools for AI-generated text?"*（多论文池：Liang + Weber-Wulff + GLTR）。

**LLM 后端**（`tools/llm/client.py`）：默认 `opencode`（免费托管模型，经 `opencode run --format json`）；`openai` 适配任意 OpenAI 兼容端点（DeepSeek / DashScope / OpenRouter / Moonshot / OpenAI）。通过 `LLM_BACKEND` / `OPENCODE_MODEL` / `OPENAI_BASE_URL` / `OPENAI_MODEL` / `OPENAI_API_KEY` 配置。

**发现 rail**（默认种子清单）：`$env:S_LIT_BACKEND='seed'|'arxiv'|'orx'`。

**解析论文**（MinerU；长/OCR 重 PDF 用 ≤6 页窗口，见 runbook K12）：

```powershell
& 'C:\Users\data\miniconda3\envs\ds0509\Scripts\mineru.exe' -p paper.pdf -o mineru_out_ds0509 -b pipeline -m txt -s 0 -e 5
```

**基准试点评测**（按原文逐字重实现 DAS-Bench 16 项标准）：

```powershell
& $PY -m tools.eval.bench_eval --backend opencode --scenarios P-A,P-B,P-C,001,019 --out _eval_out/bench_pilot_das.md
```

## 当前状态

- **Phase 0/1（文档）**：完成。**P1 工具链**：MinerU PDF→Markdown PASS；PaddleOCR 中文 OCR PASS（K7 关闭）。
- **P2 最小纵切 + 框架整合（GREEN）**：LangGraph 流水线 + 可插拔 S_lit rails（seed / arXiv API——2026-09-16 已验证可达 / orx CLI）、多论文证据池（`resolved_evidence`，3 份本地解析）、逐论文接地 claims（`paper_id` 归属）、STORM 式大纲（4-6 节）、**综述级分节写作**（intro + 每节 `## <heading>` 段落 + conclusion，内联 arXiv 归属、分歧/缺口处理）、L6 确定性门控（+ 新增 `multi_paper` 指标）、DAS-Bench 式 AI 评审。
- **测试**：mock **33/33** · real `opencode/big-pickle` **33/33**（real 约 4–8 分钟成稿 + 严格评审，verdict=pass）。
- **评估试点**（`tools/eval/bench_eval.py`，Session 11-13）：DAS-16 家族均值 **BSC 3.25 / MAR 2.50 / TSQ 3.17 / HDQ 3.75 / Total 3.17**——**TSQ 由 2.42 升至 3.17**（分节写作驱动）；产物 23-26K 字符；代理话题 2.94–3.38；DAS 话题 001 种子精度修复后正确判定 no-evidence。报告：`_eval_out/bench_pilot_das.md`。
- **默认配置**：全链路 `opencode` 后端（Ollama 后端已于 2026-09-16 移除）；种子清单保持确定性离线发现默认。

## 仓库地图

| 路径 | 说明 |
|---|---|
| `docs/refs/ai-research-tools-workflow-guide.md` | 已核验工具调研（2026-09-15），含验证台账 |
| `docs/design/research-foodie-blueprint.md` | 双语架构蓝图：目的/非目标、L0–L6、状态机、成本矩阵、路线图 |
| `docs/setup-runbook.md` | 双语操作手册：环境、命令、冒烟测试、已知问题 K1–K12 |
| `docs/PLAN.md` · `docs/PROGRESS.md` | 执行计划 + 进度日志（计划先行、边做边记） |
| `tools/llm/` | 统一 LLM 客户端（`opencode` + `openai`）+ mock 服务 |
| `tools/pipeline/` | LangGraph 流水线：`corpus.py`（发现+证据池）· `graph.py`（S_lit…S_final）· `validate.py`（L6）· `judge.py`（P3）· `test_pipeline.py` |
| `tools/eval/bench_eval.py` | DAS-Bench 16 项标准评估工具 |
| `tools/citation-verify/` | 引文核验测试台（CrossRef/arXiv/Semantic Scholar） |
| `external/` | 下载的框架仓库（已 gitignore）：STORM、DAS(+DAS-Bench)、paper-qa、MinerU、DeepResearch、orx、OpenResearch… |

## 治理原则

- **引用即生命线**：每个事实声明都回溯一手资料（已解析论文、arXiv ID）并附访问日期；无法验证的声明标记 *unverified*，绝不冒充事实。
- **日期显式化**：当前状态类陈述带 `as of <date>`。
- **成本敏感**：默认开源/免费工具；付费 API 仅用于质量关键环节。
- **不主动提交**；文档双语原则仅在单语会导致信息损失时启用。

## 路线图（下一步）

1. MAR 渲染轴——页面渲染产物 / 图表抽取（纯 markdown 无法给 Figure/Table Quality 打分；残余短板轴）。
2. DAS-Bench 全量合规——DAS-2M 话题池 + ≥300B 冻结评审（需要 API key / GPU / 网络）。
3. Track B（人文）：PaddleOCR 中文证据层接入主动循环。

可度量验收见 `docs/PLAN.md §7`。