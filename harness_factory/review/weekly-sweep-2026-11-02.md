# Weekly sweep · 学界与业界周扫荡（P60 · 2026-10-26 → 11-02）

> **中文速览。** 用户先令扫学界（研究所/高校/机构），再补业界。方法：从本周 INTEL（3287 行）挖出 418 条学术相关 +
> 7 条业界条目 → 选能力形态最强的三篇入册（R279 ThinkingBox **全文** · R280 QueenBee **摘要级** · R281 LegoSR
> listed）。**三大发现**：① **ThinkingBox**（Microsoft+HF）把 LHTB 的重放评分做成了工业规模（121,680 次试验；
> 67.24% 的失败干净退出但 77.61% 状态错误；pass@1 与 20/20 一致性尖锐分化），且原生架在 OpenEnv 上；②
> **QueenBee** 是本库 D1 形态的独立外部实现（拓扑=可执行程序 + SFT-Bank 结构记忆库）；③ 判分者自身的教训：情报
> 抽取把 QueenBee 的 URL 串了行——扫荡工具也要过自己的门（M3.19）。

**Updated:** 2026-11-02 · **Round:** P60 · **Evidence:** R279 全文 · R280 摘要级 · R281 listed

## 1. The mine · 情报挖掘

本周 INTEL 3287 行：学术相关 **418 条**（arXiv cs.CL/LG/MA 新论文为主体）+ 业界 **7 条**（OpenAI/HF/Willison）。
能力形态最强者入册三条，其余高质量 lead 记于 §4。

## 2. The three finds · 三大发现

### 2.1 ThinkingBox（R279，业界，Microsoft+HF，全文）

- **形态**：507 个有状态业务工作流（零售/车险/旅行/银行/咨询），每任务从同一干净后端跑 20 遍 × 18 个 LLM；
  评分看**终端数据库状态与副作用**（确定性判分器比对副作用 diff 与要求终态），二元奖励经 **OpenEnv** 适配器出。
- **标语即条款**：「A trajectory is a claim. Database state is the evidence. Repetition is the trust test.」——
  M3.18(c)（重放评分、LHTB 谱系）的**工业规模独立佐证**：121,680 次试验中 67.24% 的失败干净退出、无报错，
  而可执行检查在其中 77.61% 发现错误字段值。
- **新度量维度**：pass@1 与 20/20 全过一致性**尖锐分化**（Kimi-K3 93.89% 至少一次 vs 13.41% 全过；Opus 5.5 的
  pass@1 提升换来零个新增全过任务）——「可靠任务数」（dependable tasks）是 at-least-once 之外的第一类度量，
  与 M3.17（一致≠验证）和未来 N>1 试验的记分口径直接相关。
- **失败分类**：约 4/5 的失败是工具处理而非推理（79.9% 工具使用签名）——harness 侧改进的空间被定量定位。
- **基础设施**：固定框架 commit + 固定数据版 + bundle hash（可复现三件套）；黄金状态/断言/判分内部凭证留在
  评测侧（信任边界）；MIT（代码）/CDLA（数据）。

### 2.2 QueenBee（R280，学界，摘要级）

- **形态**：冻结模型权重，演化**工作流层**——拓扑为「生成时序通信 DAG 的可执行程序」；**SFT-Bank**（执行诊断/
  设计假设/验证结果/历史程序的持久结构记忆）指导后续生成、验证与优化。
- **对本库的含义**：这就是 **D1 形态的独立外部实现**——trace 词表（诊断/假设/验证结果）与本库的
  gate_miss/human_correction/提案制一一对应；R252/R256 之外的第三个 stage-C 先例（已记 D1 roadmap）。
- **边界**：摘要级（全文未拉）；摘要未提 token 效率数字（搜索摘要的副题「Token-Efficient」无摘要支撑——按
  M0.1 只记摘要所述）；无显式防误进化机制（仅验证结果前馈）。

### 2.3 LegoSR（R281，学界，listed）

Agent 引导的符号回归（七求解器统一框架 + 任务经验），同预算下比通用 agent 高 29pp——科学发现的
agent 引导形态，记为 discovery 类目录条目。

## 3. Adjudication · 裁决

- **无新子句**：ThinkingBox 的状态评分是 M3.18(c) 的工业佐证（引用即足，条款不需改）；QueenBee 是 D1 先例
  （roadmap 注记）；「一致性度量」是记分口径候选——等 N>1 试验开跑时进 battery 设计（触发已记）。
- **无新能力**：三篇都落在既有模块/子句的辖域内（M3/M5/M8 + D1）——43 能力的判别面继续够用。
- **过程教训**：情报抽取脚本把 QueenBee 的 URL 串了行（取到邻行 LegoSR 的链接）——扫荡工具的抽取结果要按
  标题复核 URL（M3.19 的扫荡版）。

## 4. Leads · 未入册的高质量线索（按触发）

- **EvoMemBench**（2603.16886）：自演化视角的 agent 记忆基准——M2.12 记忆后端声明的评测对接候选。
- **M\*: Every Task Deserves Its Own Memory Harness**：每任务自配记忆 harness——与本库「按任务特征组装」
  同构，等全文。
- **VerifyMAS**（2610.41905）：MAS 失败归因的假设验证——M8.10/M3.15 的对接候选。
- **PrivacyFlow**：信息流分析 + 后果感知的 agent 隐私——P52 记的 data-sensitivity affordance lead 的
  可能一手内容源。
- **SoK: Agentic RAG**（分类学综述）· **Controllable User Simulation** · **Context as Infrastructure（知识编译
  作检索）** · **ProSearch**（多约束协议检索基准）——各自按域/能力触发。
- **业界**：OpenAI×ServiceNow（企业工作流）、Legora（法律 agentic OS）、Patch the Planet（漏洞挖掘 agent 群）、
  Willison「webframe：既是爬虫又是沙箱」（双重角色评测实践）。

## 5. Verification

catalog 218 → **221**（thinkingbox verified · queenbee · legosr）；references **§AD**（R279–R281）+ bib 3 条；
D1 roadmap 增 QueenBee stage-C 先例注记；`P60WeeklySweepTest` 守卫；`harness cycle audit` → **56 轮 · 0 硬 ·
0 缺口**（详见 PROGRESS 计数）。
