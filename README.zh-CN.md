# research_foodie

**本地优先、成本敏感（核心成本≈$0）的主动式学术研究流水线**：输入一个研究问题（或一个受监控领域），输出一份**逐句可溯源到已解析论文**、中英双语的综述手稿——每个事实 claim 锚定原文逐字引文；先机械校验、后人工把关。

> English version: [`README.md`](README.md) · 总览主入口（目标/组件/工作流/实测能力）：[`docs/PROJECT.md`](docs/PROJECT.md) · 架构蓝图：[`docs/design/research-foodie-blueprint.md`](docs/design/research-foodie-blueprint.md)

`Updated: 2026-09-20` · `许可证：MIT`

---

## 为什么做这个 / Why this exists

通用"深度研究"工具产出的综述读起来漂亮，却**会编造引用**——实测 GPT-4o 编造率约 78–90%（*OpenScholar*, Nature 650:857, 2025）。它们还是黑盒、花真钱、把失败单元平均掉。

research_foodie 反向设计：

- **引用即生命线**：每个声明必须锚定本地已解析论文（arXiv）的**逐字引文**；确定性 5-gram 接地门在任何人审之前机械屏蔽幻觉。
- **≈$0 核心链路**：MinerU（本地解析）+ 免费托管模型 `opencode/big-pickle` + 免费 arXiv API，核心环节零 API key。
- **诚实自评**：判题噪音、证据池覆盖率、模型边界全部显式报告，不平均掉。

## 做什么 / What it does

- **模式 1 — 研究综述**：问题 → 实时发现 → MinerU 解析 → 分类 + STORM 式大纲 → 逐论文接地 claims → **综述级双语（EN + 中文）草稿**，内联 `(arXiv:…)` 归属、分歧/缺口处理 → 手稿（Abstract / 证据表 / References）→ 本地 **PDF**（pandoc + xelatex + CJK）。
- **模式 2 — 证据接地 QA（Track C）**：直接基于单篇论文/上下文回答基准问题（Qasper / SciQ / PubMedQA / 语料锚定）。
- **模式 3 — 判题电池**：任意跑 30 个 DAS-Bench 话题端到端（发现 → 证据池 → 判题）。
- **评估**：DAS-Bench 16 项标准逐字重实现；判题方差测试台；30 话题证据池；引用核验（CrossRef / arXiv / Semantic Scholar）。

## 架构 / Architecture

```text
[L0] 问题 / 领域监控
  ▼
[L1] S_lit   发现 rails：种子清单 · 实时 arXiv API · orx CLI
  ▼
[L2] 证据   MinerU PDF→Markdown → 多论文证据池（逐论文接地）
  ▼
[L3] S_org  分类 + STORM 式大纲（节 + 要点）
  ▼
[L4] S_write 逐论文证据化 claims（逐字引文）→ 跨论文写作
  ▼
[L5] S_final 组装手稿（来源 + 逐 claim 归属）→ 本地 PDF
  ▼
[L6] 门控  确定性零-LLM 校验 → DAS-Bench 式 AI 判题 → 人工
```

以 LangGraph 状态机实现（`tools/pipeline/graph.py`）：`lit → org → write → revise_para → finalize → gate → judge`。定点重写只重进违规段落；机械门失败按范围回环。`seed_id`/`ctx` 问题改走接地抽取式回答节点。发现 rails 可插拔（`S_LIT_BACKEND=seed|arxiv|orx`；arXiv API 实测可达 ~1.1 s，2026-09-16）。

## 快速上手 / Quickstart

环境为 conda env `ds0509`（Python 3.12，Windows），请显式使用该解释器：

```powershell
$PY = 'C:\Users\data\miniconda3\envs\ds0509\python.exe'
$UTF8 = '-X','utf8'                 # 避免 opencode 子进程 cp1252 解码噪声
```

**集成测试**（mock = 秒级确定性；real = 完整免费模型链路，2–4 分钟）：

```powershell
& $PY -m tools.pipeline.test_pipeline mock      # 34/34 PASS
& $PY $UTF8 -m tools.pipeline.test_pipeline real  # opencode/big-pickle，verdict PASS
```

**示例问题：** *"GPT detectors bias against non-native English writers"*（Liang `2304.02819`）· *"How reliable are automatic detection tools for AI-generated text?"*（多论文池：Liang + Weber-Wulff `2306.15666` + GLTR `1906.04043`）。

**DAS-Bench 16 轴基准**（报告 → `_eval_out/bench_pilot_das.md`；`--out` 会整份覆盖，务必一次跑全场景集）：

```powershell
& $PY $UTF8 -m tools.eval.bench_eval --scenarios P-A,P-B,P-C,001,019
```

**证据接地 QA 面板子集：**

```powershell
& $PY $UTF8 -m tools.eval.bench_eval --scenarios QA-6,QA-7,SQ-1,PQ-1
```

**30 话题电池 + 判题方差：**

```powershell
& $PY $UTF8 -m tools.eval.pools_30          # → _eval_out/pools_30.json + pools_30_report.md
& $PY $UTF8 -m tools.eval.variance_run      # → _eval_out/variance_runs.json
```

**本地 Web 观测台（WS-B）：** 一键触发、SSE 实时进度、可取消、手稿 PDF、feedback——全在浏览器：

```powershell
& $PY -X utf8 -m uvicorn tools.web.app:app --host 127.0.0.1 --port 8787
# → http://127.0.0.1:8787/
```

仅绑定 **127.0.0.1**，定位是*本地观测面*：**GitHub Pages 是纯静态托管，不执行任何服务端代码**（Python/Node/PHP 运行时均不受支持），故活版前端留本地、静态只读导出（F-3）才是可部署到 Pages 的形态。

**LLM 后端**（`tools/llm/client.py`）：默认 `opencode`（免费托管模型，零 key）· `openai` 适配任意 OpenAI 兼容端点（DeepSeek / DashScope·Qwen / Moonshot·Kimi / OpenRouter / OpenAI），经 `OPENAI_BASE_URL` / `OPENAI_MODEL` / `OPENAI_API_KEY` 配置。Phase D 将加角色级 profiles（廉价草稿 lane / 强判题 lane）。**解析论文**用 MinerU（`-m txt`；长 PDF 用 ≤6 页窗口，见 runbook K12）。

> 逐工具速查表 + 四条端到端 demo：[`docs/setup-runbook.md §3.1`](docs/setup-runbook.md) · 端到端使用流程（从问题出发 → 干货设置 → 规范/格式约束）：[`§3.0`](docs/setup-runbook.md)。

## 实测能力 / Measured status (as of 2026-09-19)

> 方向性数据，不与官方 DAS 榜单 head-to-head（那需要 ≥300B 冻结判题）；每个 verdict 记录实际判题模型。完整盘点：[`docs/CAPABILITY-STATUS.md`](docs/CAPABILITY-STATUS.md)。

| 项 | 数字 | 含义 |
|---|---|---|
| 流水线测试 | **mock 34/34 · real 34/34** | 确定性 + 完整 LLM 链路全绿（2 篇真论文：Liang、Weber-Wulff） |
| QA 面板 n=31 | correctness **4.23** · groundedness **4.45** · 24/31 | Track C，含 Qasper 金标 5/5 · SciQ 上下文 5/5 · PubMedQA 8/14 |
| 抽取/上下文路径（n=13） | **12/13** | 单篇/上下文事实题≈可解 |
| PubMedQA 是/否（PQ-1..14） | **8/14** | 是/否*结论* = 实测模型边界 |
| 代理三元组（方差） | **P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13** | 判题模型（免费）运行间噪声 |
| 电池判题（n=10） | **Total 3.13**（BSC 3.08 · MAR 2.67 · TSQ 3.05 · HDQ 3.73） | 含发现噪声的端到端；HDQ 为强项，MAR 受池小拖累 |
| 证据池覆盖 | **22/30 DAS 话题**有已解析证据（12 个满池） | 8 个空池 = 相关性/网络上限，度量而非静默 |

**诚实契约**：判题噪声显式（P-A σ≈0.53）；001/019 正确判 no-evidence；PubMedQA 8/14 边界直认；隐藏失败单元列出而非平均掉。链路三道闸：确定性 L6（事实完整性，零成本）→ AI 判题（质量）→ **人工**（放行；永不自动发布）。

## 仓库地图 / Repository map

| 路径 | 说明 |
|---|---|
| `README.zh-CN.md` | 本项目中文入口 |
| `docs/PROJECT.md` | **总览主入口：** 目标 / 组件 / 工作流 / 实测能力 / 路线图 |
| `docs/design/research-foodie-blueprint.md` | 架构蓝图：L0–L6、状态模型、成本矩阵、路线图 |
| `docs/design/self-evolution-mechanism.md` | 自演化设计（WS-C）：四相循环、证据、失败模式 |
| `docs/design/tool-paper-outline.md` | 本工具投稿 arXiv 的系统论文大纲（双语） |
| `docs/DATAFLOW-AND-REUSE.md` | 各模式输入输出、逐节点阶段 I/O、框架缝合程度诚实账本 |
| `docs/TOOL-COMPARISON.md` | 逐阶段对比 STORM / orx / PaperQA2 / DAS / MinerU 等 |
| `docs/CAPABILITY-STATUS.md` | 实测数字、GREEN/BLOCKED 清单、复现命令 |
| `docs/setup-runbook.md` | 操作手册：环境、命令、使用流程 §3.0、演示 §3.1、已知问题 K1–K12 |
| `docs/PLAN.md` · `docs/PROGRESS.md` | 计划先行 / 边做边记（§8 = 并行工作流 WS-A/B/C/D/R） |
| `tools/llm/` | 统一 LLM 客户端（`opencode` + `openai`）· mock 服务 · smoke test |
| `tools/pipeline/` | LangGraph：`corpus.py` · `graph.py` · `validate.py`（L6）· `judge.py` · `answer.py` · `test_pipeline.py` |
| `tools/eval/` | `bench_eval.py`（DAS-16）· `pools_30.py` · `variance_run.py` · `add_paper.py` · `render_manuscript.py` |
| `tools/web/` | 本地 FastAPI 观测台（runs / SSE / cancel / manuscripts / feedback）——WS-B |
| `tools/citation-verify/` | CrossRef / arXiv / Semantic Scholar 批量引用核验 |
| `_eval_out/` | 真实结果：bench 报告、pools、variance、手稿、web 运行日志（gitignore） |

## 质量护栏 / Governance

- **引用即生命线**——每个事实声明回溯一手资料（已解析论文、arXiv ID）并附访问日期；无法验证 → 标 *unverified*，绝不冒充事实。
- **日期显式化**——当前状态类陈述带 `as of <date>`；价格/榜单数字为方向性并附来源。
- **成本敏感**——默认开源/免费；付费 API 仅用于质量关键升级 lane。
- **不主动提交；计划先行、边做边记**（`docs/PLAN.md` → `docs/PROGRESS.md`）。

## 路线图与开放工作流 / Roadmap & open workstreams

进度按**并行工作流**组织（见 `docs/PLAN.md §8`）：

- **WS-A** 核心流水线（Phase L）：L-1 检索重排 · L-3 判题 median-of-3（攻 P-A σ 0.53）· L-4 引用核验接线。
- **WS-B** Web 观测台（Phase F）：✅ F-1/F-2 已交付（runs/SSE/cancel）· F-3 只读静态导出（可部署 GH Pages）· F-4 进入自演化节奏（E-2/E-3/E-4/E-5 同一 URL）。
- **WS-C** 自演化（Phase X）：基线冻结 → 方差感知健康检查 → 门覆盖变异测试 → 带溯源下限的周更节奏（E-1…E-7）。
- **WS-D** 模型路由（Phase D）：角色级 profiles；在 OpenAI 兼容 API key 上开**强判题 lane**（今日无 key 亦可跑）——目标 P-A sd < 0.40。
- **WS-R** 资源门控（Phase R）：官方 DAS-Eval 工具包 · DAS-2M 元数据湖 · knowledge-storm · ≥300B 页面感知判题（需 key / GPU / 网络）。

**阻塞项（需 key · GPU · 输入）：** ≥300B 页面感知判题对渲染 PDF 打分（MAR Layout 轴 + 全量 DAS-Bench 合规）· GAIA 批量 · 中文证据层（Track B）——裁决见 [`docs/CAPABILITY-STATUS.md §3`](docs/CAPABILITY-STATUS.md)。

---
*MIT 许可证 · 双语文档由 [`AGENTS.md`](AGENTS.md) 约束 · Windows 11 / CPU-only / conda `ds0509` 构建。*