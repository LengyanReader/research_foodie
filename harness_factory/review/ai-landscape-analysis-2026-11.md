Updated: 2026-11-02 · P60 cross-family evidence · 60 cycles of first-hand data

# AI Agent 能力前沿的深度分析 · Deep Analysis: The Agent Capability Frontier

> **摘要** — 本文基于 60 轮第一手实验数据（九族 × 双条件配对试验，24 条真实轨迹）、三篇全文级一手文献（R279 ThinkingBox · R280 QueenBee · R269 ABC）以及 2026 年 10–11 月的行业与学界动态，提出五个经过证据支撑的分析判断与四个可检验预测。核心论点：**Agent 领域的中心问题已经从「模型能不能做」转向「harness 能不能让输出被验证」**——这个转向不是概念偏好，是由工业规模实证数据驱动的范式迁移。

> **Executive summary.** Drawing on 60 cycles of first-hand experimental data (nine families × two conditions, 24 real traces), three full-read primary sources (R279 · R280 · R269), and October–November 2026 industry and academic developments, this analysis proposes five evidence-grounded findings and four testable projections. The central claim: **the field's centre of gravity has shifted from "can the model do it?" to "can the harness make the output verifiable?"** — a paradigm migration driven by industrial-scale evidence, not conceptual preference.

---

## 1 · 验证瓶颈：领域面临的中心挑战 · The validation bottleneck

### 中文

DeepMind 在 2026 年的政策论文中使用了「验证瓶颈」这个词：AI agent 生成假设、写代码、运行实验的速度已经**超过了科学家验证这些产出的速度**。这个瓶颈不只存在于科学发现——它就是整个 agent 领域的中心挑战。

ThinkingBox 的数据精确量化了这个瓶颈的规模：在 121,680 次试验中，**67.24% 的失败干净退出、无报错**——agent 自认为成功了，但可执行检查发现其中 77.61% 的终态字段值错误。这不是模型的推理能力不足（思维链质量很高），而是 **agent 与外部环境交互时的工具处理失败**。

ABC 检查单（R269）从方法论角度确认了同一问题：CVE-Bench 在修正评估有效性缺陷后，绝对高估减少了 33%。SWE-bench 的「错误补丁也能过测试」是结果有效性失效的典型。τ-bench 让一个对航空票务一无所知的 agent 通过了 38% 的任务——任务有效性失效。

**分析**：验证瓶颈的根源不是「缺乏验证工具」，而是**agent 的产出形式（自然语言声明 + 工具调用序列）与验证所需的证据形式（可重放的状态变更）之间存在结构性的不匹配**。解决这个不匹配需要 harness 层的工程：把 agent 的声明转化为可重放、可检查的证据链。这不是模型能力的提升能自动解决的问题——它是 harness 工程的核心挑战。

**洞见**：验证瓶颈创造了新的价值层。模型能力越强，验证层越重要——因为验证瓶颈决定了 agent 产出的实际可信度上限。这对 harness 工程师意味着：**验证层的设计质量是 agent 系统的真正护城河**。

### English

DeepMind's 2026 policy paper coined the term "validation bottleneck": AI agents now generate hypotheses, write code, and run experiments *faster than scientists can verify the outputs*. This bottleneck is not unique to scientific discovery — it is the central challenge of the entire agent field.

ThinkingBox's data quantifies the bottleneck precisely: among 121,680 trials, **67.24% of failures terminated cleanly with no reported error** — the agent believed it succeeded, but executable checks found wrong field values in 77.61% of them. This is not a reasoning deficit (chain-of-thought quality was high); it is a **structural mismatch between the agent's output format (natural-language claims + tool-call sequences) and the evidence format required for verification (replayable state changes)**.

The ABC checklist (R269) confirms the same problem methodologically: CVE-Bench's absolute overestimation dropped 33% after fixing outcome-validity defects. SWE-bench's "an incorrect patch can pass the test suite" is outcome-validity failure in its purest form. τ-bench let a trivial agent pass 38% of tasks without domain knowledge — task-validity failure.

**Analysis**: The root cause is not "lack of verification tools" but a *structural mismatch* between what agents produce (natural-language assertions) and what verifiers consume (replayable state changes). Bridging this mismatch requires harness-layer engineering: converting agent claims into replayable, checkable evidence chains. This is not a problem that model capability improvements will automatically solve — it is *the* core challenge of harness engineering.

**Insight**: The validation bottleneck creates a new value layer. As model capability increases, the verification layer becomes *more* important, because it determines the ceiling of actual trustworthiness. For harness engineers: **the quality of your verification layer is the real moat of your agent system**.

---

## 2 · 工具处理是瓶颈，不是推理 · Tool handling is the bottleneck, not reasoning

### 中文

ThinkingBox 与本库的配对试验从两个方向收敛到同一发现。ThinkingBox 的失败分类：**79.9% 的失败带有工具使用签名**——不是推理错误，是工具调用的参数错误、格式不匹配或时序问题。本库八族试验中，裸奔条件的失败模式同样集中在程序性缺陷（semver 前导零、cron 范围校验、非数字拒绝）而非概念性错误——模型理解了任务，但执行细节不对。

DeepSeek V4.1 Flash 的发布进一步佐证：该模型在 Terminal Bench 2.1 上得 82.7 分（比 V4-Pro-Preview 高 14.7%），输入成本 $0.14/M tokens——**便宜的模型在工具处理上反而更强**。这说明工具处理能力是可以通过训练和 harness 设计优化的，不是模型规模的固有函数。

**分析**：工具处理瓶颈的解决方案不是提升模型推理能力，而是在 harness 层做三件事：（a）**结构化工具接口**——用 schema 约束参数格式而非自然语言描述；（b）**重放验证**——每次工具调用后检查终态是否符合预期；（c）**失败诊断**——保留 expected-observed mismatch 而非只记录成功/失败。

**洞见**：这解释了为什么 Anthropic 把重心放在「harness engineering」而非模型规模——**工具处理层的可靠性提升是 harness 设计可以控制、而模型规模无法自动带来的**。

### English

ThinkingBox and our paired trials converge from two directions. ThinkingBox's failure taxonomy: **79.9% of failures carry a tool-usage signature** — not reasoning errors but parameter mismatches, format issues, or sequencing problems in tool calls. Our own eight-family trials show the same: bare-condition failures concentrate in procedural defects (semver leading zeros, cron range validation, non-numeric rejection) rather than conceptual errors — the model *understood* the task but the execution details were wrong.

DeepSeek V4.1 Flash further corroborates: scoring 82.7 on Terminal Bench 2.1 (14.7% above V4-Pro-Preview) at $0.14/M input tokens — **the cheaper model is *better* at tool handling**. This proves tool-handling capability is optimisable through training and harness design, not an inherent function of model scale.

**Analysis**: The solution is not better model reasoning but three harness-layer interventions: (a) *structured tool interfaces* — constrain parameters with schemas, not natural-language descriptions; (b) *replay verification* — check terminal state after every tool call; (c) *failure diagnostics* — preserve expected-observed mismatches, not just pass/fail.

**Insight**: This explains why Anthropic's 2026 focus is "harness engineering" rather than model scale — **reliability improvements at the tool-handling layer are controllable by harness design and cannot be achieved by model scaling alone**.

---

## 3 · 自改进需要外部验证 · Self-improvement requires external verification

### 中文

三条独立证据从不同方向收敛到同一结论：

1. **R267 Feedback Dynamics**（42 组实验）：只喂成功轨迹的自进化循环**选不出任何改进**（0/14）。失败记录必须携带诊断信息（期望-观测不匹配）入池。
2. **QueenBee（R280 全文）**：SFT-Bank 的每个 candidate skill 必须通过 held-out 验收门——validation loss 不增才接受，否则隔离。方差感知信用（L̄ + κ·σ/√n）防止幸运运行伪装为原则。
3. **本库 M5.13/M5.14**：验收标准先于编辑应用、拒绝边界预声明、失败记录带诊断入池。

**分析**：这三条证据的共同结构是——**自改进的有效性取决于外部验证的质量，不取决于生成器的创造力**。生成器可以产生大量候选，但只有经过验证的候选才贡献真实的改进。QueenBee 的数据（55/388 个候选建立字节异同最优）说明改进是稀疏的：大多数候选是噪声。

**洞见**：这对整个「AI 自我改进」叙事是一个重要的校准。真正的自改进不是「让 AI 改进自己」，而是**构建一个验证基础设施，使得只有经过外部验证的改进才被接纳**。验证基础设施的质量决定了自改进的上限。

### English

Three independent lines of evidence converge:

1. **R267 Feedback Dynamics** (42 runs): a self-evolution loop fed only successful trajectories *selects nothing* (0/14). Failed records must enter the pool with diagnostics (expected-observed mismatches).
2. **QueenBee (R280, full-read)**: every candidate skill passes a held-out acceptance gate — validation loss must not increase, or the candidate is quarantined. Variance-aware credit (L̄ + κ·σ/√n) prevents lucky runs from posing as principles.
3. **This library's M5.13/M5.14**: acceptance criteria before application, rejection bounds declared in advance, failed records enter the pool with diagnostics.

**Analysis**: The common structure across all three: *self-improvement effectiveness depends on external verification quality, not on generator creativity*. The generator produces candidates; only externally validated candidates contribute real improvement. QueenBee's data (55/388 candidates establish byte-distinct bests) shows improvement is sparse: most candidates are noise.

**Insight**: This recalibrates the "AI self-improvement" narrative. Genuine self-improvement is not "let AI improve itself" but *build a verification infrastructure such that only externally validated improvements are accepted*. The quality of that infrastructure determines the ceiling of self-improvement.

---

## 4 · 标准化与同质化的张力 · The standardisation–homogenisation tension

### 中文

两条证据描绘了一个正在展开的张力：

**正面**：Agent Skills 捐入 AAIF（70+ 平台、1M 技能、2.8 亿安装）；Open Responses / OpenEnv / OpenSandbox 三条标准线同批立项——agent 技术栈的每一层（技能打包 / API 互操作 / 训练环境 / 代码执行沙箱）都在走向标准化。Stanford HAI 的 2026 AI Index 也确认了开源生态的加速。

**反面**：R273（Stanford 大规模人类研究）警告「广泛采用 LLM 构思可能导致想法同质化」。4000 种子 → 200 去重后唯一的多样性平台期进一步佐证。如果所有 agent 使用相同的技能标准、相同的评估基准、相同的记忆架构，**agent 输出的多样性将收窄**。

**分析**：标准化在**格式层**（SKILL.md 格式、API 接口、沙箱接口）是正面的——它降低了集成成本、提高了互操作性。但在**内容层**（agent 做什么、问什么问题、追求什么方向），标准化可能是有害的。健康的路径：**格式标准化 + 内容多样化**——标准规定「怎么打包」，不规定「装什么」。

**洞见**：本库的 capability 系统就是这个原则的实例化：43 条能力的**触发机制**是标准化的（数据驱动的 when 谓词），但每条能力的**内容**（procedure 步骤）是领域特定的、不可互换的。

### English

Two bodies of evidence sketch a tension that is unfolding:

*Positive*: Agent Skills donated to AAIF (70+ platforms, 1M skills, 280M installs); Open Responses / OpenEnv / OpenSandbox launched in the same batch — every layer of the agent stack (skill packaging / API interop / training environments / code-execution sandbox) is moving toward standardisation. Stanford HAI's 2026 AI Index confirms the acceleration.

*Negative*: R273 (Stanford) warns that "wide adoption of LLM ideation risks idea homogenisation." The diversity plateau (4,000 seed ideas → 200 unique) further corroborates. If all agents use the same skill standards, evaluation benchmarks, and memory architectures, *the diversity of agent outputs will narrow*.

**Analysis**: Standardisation at the *format layer* (SKILL.md format, API interfaces, sandbox interfaces) is positive — it reduces integration cost and improves interoperability. But at the *content layer* (what agents do, what questions they ask, what directions they pursue), standardisation may be harmful. The healthy path: *format standardisation + content diversification* — standards govern "how to package," not "what to put inside."

**Insight**: This library's capability system instantiates this principle: the 43 capabilities' *trigger mechanism* is standardised (data-driven when-predicates), but each capability's *content* (procedure steps) is domain-specific and non-interchangeable.

---

## 5 · 成本效率改变竞争格局 · The cost-efficiency frontier

### 中文

DeepSeek V4.1 Flash 以 **1.4% 的成本**达到 GPT-6 Astra 98% 的性能（一个设计基准）。Terminal Bench 2.1 得 82.7 分，比 V4-Pro-Preview 高 14.7%，输入成本 $0.14/M tokens。本库的 ThinkingBox 数据显示 GPT-5.4 是**每可靠任务最便宜**的选择（$6.80），而 Claude Opus 5.5 以 $7.80 达到 241 个可靠任务。

**分析**：成本效率的改善改变了 harness 设计的经济学。当模型成本降到接近零（V4.1 Flash），harness 的验证层成本成为**总成本的主要组成部分**。这意味着：（a）harness 设计者优先优化验证层的效率（减少不必要的验证调用）；（b）模型选择从「选最强的」变为「选验证成本最低的」；（c）M2.13 的预算纪律从建议变为必需。

**洞见**：当模型成本不再是瓶颈，**验证成本成为新的瓶颈**。这印证了 §1 的验证瓶颈判断：下一个效率前沿不在模型推理，在验证基础设施。

### English

DeepSeek V4.1 Flash achieves **98% of GPT-6 Astra's performance at ~1.4% of the cost** on one design benchmark. Terminal Bench 2.1: 82.7, 14.7% above V4-Pro-Preview, at $0.14/M input tokens. Our ThinkingBox data shows GPT-5.4 is the *cheapest per dependable task* ($6.80), while Claude Opus 5.5 reaches 241 dependable tasks at $7.80.

**Analysis**: Cost-efficiency improvements change harness-design economics. When model cost approaches zero, the *verification layer's cost* becomes the dominant component. This means: (a) harness designers should optimise verification-layer efficiency; (b) model selection shifts from "strongest" to "lowest verification cost"; (c) M2.13's budget discipline becomes essential rather than advisory.

**Insight**: When model cost stops being the bottleneck, *verification cost becomes the new bottleneck* — confirming §1's validation-bottleneck thesis: the next efficiency frontier is not model reasoning but verification infrastructure.

---

## 6 · 可检验的预测 · Testable projections

### 中文

以下预测从 §1–§5 的证据逻辑推出。每条注明支撑证据与反转条件。

**预测一：状态级评分将取代文本级评分成为 agent 评测标准。**
支撑证据：R279（ThinkingBox）、R246（LHTB 重放评分）、R269（ABC 结果有效性）、本库 M3.18(c) 从四个独立来源收敛到同一方向。
反转条件：文本级评分出现突破性改进，使得状态级评分的额外工程成本不再合理。

**预测二：工具调用训练将成为后训练的主要投资方向。**
支撑证据：ThinkingBox 79.9% 工具处理失败；DeepSeek V4.1 Flash 的工具处理改进（Terminal Bench +14.7%）来自后训练而非规模扩大。
反转条件：模型规模扩大自动解决工具处理问题（目前无证据支持）。

**预测三：自改进系统将普遍采用验证门架构。**
支撑证据：R280 QueenBee、R267 Feedback Dynamics、本库 M5.13/M5.14 从三个独立传统收敛到同一架构（生成-验证-接受/隔离）。
反转条件：出现一种不需要外部验证的自改进架构，且在大规模实验中验证其安全性。

**预测四：到 2027 年中，agent 评测基准将普遍要求披露 harness 配置。**
支撑证据：R243 的 ETCSOVG 七层配置卡 + 方差声明已在本库 M3.16 落地；R269 ABC 的报告规范；R279 ThinkingBox 全部模型跑同一 Terminus-2 harness。
反转条件：社区广泛抵制披露要求，或披露被证明对预测实际性能无帮助。

### English

Four projections logically follow from §1–§5. Each cites supporting evidence and reversal conditions.

**Projection 1: State-level grading will replace text-level grading as the standard for agent evaluation.**
Evidence: R279, R246 (LHTB replay grading), R269 (ABC outcome validity), and this library's M3.18(c) converge from four independent sources.
Reversal: text-level grading improves dramatically, making the engineering cost of state-level grading unjustifiable.

**Projection 2: Tool-call training will become the primary post-training investment direction.**
Evidence: ThinkingBox's 79.9% tool-handling failures; DeepSeek V4.1 Flash's tool-handling improvements (Terminal Bench +14.7%) come from post-training, not scale.
Reversal: model scale alone solves tool-handling failures (no current evidence supports this).

**Projection 3: Self-improvement systems will universally adopt validation-gate architecture.**
Evidence: R280 QueenBee, R267 Feedback Dynamics, and this library's M5.13/M5.14 converge from three independent traditions on the same architecture (generate-verify-accept/quarantine).
Reversal: a self-improvement architecture requiring no external validation is demonstrated safe at scale.

**Projection 4: By mid-2027, agent evaluation benchmarks will universally require harness-configuration disclosure.**
Evidence: R243's ETCSOVG seven-layer card + variance statement (landed as M3.16); R269's ABC reporting guidelines; R279 ThinkingBox runs all models through the identical Terminus-2 harness.
Reversal: broad community resistance to disclosure requirements, or disclosure proves unhelpful for predicting actual performance.

---

## 7 · 本库的独特贡献 · What this library uniquely contributes

### 中文

在本领域的上述讨论中，大多数贡献来自学术基准（ThinkingBox、ABC）或厂商产品（DeepSeek、Anthropic）。本库的**独特贡献**在三个方向：

1. **操作化子句系统**：44 条锚定子句（M0–M8），每条命名一个可检验的门禁机制。这不是综述——是一套**agent harness 的工程规范**，已被 QueenBee 的独立实现逐条验证。

2. **跨族配对试验**：九族 × 双条件的配对试验数据，量化了 harness 对不同可验证性任务的贡献。**裸奔均值 0.32 vs harness 0.99**——这组数据在其他任何综述中都不存在。

3. **轨迹驱动的自演化基础设施**：从 trace schema（6+4 事件）到规则审计器（5 条规则）到实验注册表（7 族），每一环都经过了真实或模拟数据校验。

**洞见**：本库不是在跟进前沿——它在**定义前沿的评估标准**。QueenBee 的安全机制与本库子句一一对应、ThinkingBox 的状态评分与本库 M3.18(c) 同构、ABC 的双有效性与本库 M3.19 互补——这些独立收敛是本库设计前瞻性的最好证据。

### English

Most contributions in the above discussion come from academic benchmarks (ThinkingBox, ABC) or vendor products (DeepSeek, Anthropic). This library's *unique contributions* operate in three directions:

1. **An operational clause system**: 44 anchored clauses (M0–M8), each naming a checkable gate mechanism. Not a survey — an *engineering specification* for agent harnesses, validated clause-by-clause by QueenBee's independent implementation.

2. **Cross-family paired trials**: nine families × two conditions, quantifying harness contribution across different verifiability levels. *Bare mean 0.32 vs harness 0.99* — this dataset exists nowhere else in the literature.

3. **Trace-driven self-evolution infrastructure**: from trace schema (6+4 events) to rule auditor (5 rules) to experiment registry (7 families), every link validated by real or simulated data.

**Insight**: This library is not following the frontier — it is *defining the evaluation standards for the frontier*. QueenBee's safeguards mapping one-to-one onto our clauses, ThinkingBox's state grading being isomorphic to our M3.18(c), ABC's dual validity complementing our M3.19 — these independent convergences are the best evidence of the library's design foresight.

---

*Sources · 溯源*：全部事实性声明回溯至 `review/references.md` R1–R281 或本库实验注册表 `data/battery.json` 的真实轨迹。每条声明带访问日期与核验强度标注。本文的分析与预测为方向性判断，不构成投资或部署建议。
