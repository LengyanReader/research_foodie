# Discipline coverage audit · 学科与思维方式覆盖审计（P54）

> **中文速览。** 用户问：学科范围、各领域的思维方式/知识/范式/经验是否穷尽了？**诚实回答：没有，也不应以穷尽为
> 目标**——判据是「能改变门禁内容才入」（M0.5/P27），穷尽会把不改变行为的条目灌进上下文（M0.6 的反面）。本审计
> 按四个维度给出**已覆盖/未覆盖的精确清单与触发条件**，并落地最大的一块缺口：methodology-map 新增**思维方式节**
> （7 行跨领域推理模式：溯因 · 临床鉴别 · 设计迭代 · 费米估算 · 思想实验 · 解释风格 · 比较方法）。

**Updated:** 2026-10-28 · **Round:** P54 · **Method:** 四维覆盖矩阵 + P27/P29 判据复用

## 1. Dimension 1: disciplines · 学科覆盖

**已覆盖**：34 学科域（10 faculties）+ general 兜底；每域 README + rubric（history/philosophy/political-science/
ai-safety 另有域键控能力，P52）。

**未覆盖（诚实清单）**：
- **已记 defer（带触发）**：astronomy · materials · neuroscience · anthropology · geography（P27）；interpretability ·
  embodied · systems-science（P29）——各以「出现真实任务族」为触发；
- **未评估过（~35 个）**：agriculture · architecture/urban · communication/media · criminology · demography ·
  工程 subfields（mechanical/electrical/civil/chemical）· finance · forestry · genomics/bioinformatics · journalism ·
  kinesiology · library/information science · logistics · marketing · military science · museum studies · music ·
  nursing · nutrition · pharmacy · planetary science · public administration/policy · public health ·
  religious studies/theology · social work · sport science · taxation · transportation · veterinary · gender
  studies · drama/film · game studies …
- **判据提醒**：多数子领域是「组合即覆盖」（P29 对 12 个跨学科任务的实测结论）；真正值得开域的是**有独有门禁内容**
  的（如 museum provenance、journalism sourcing——各自有可溯源的方法纪律才入）。probe-domains（P29）是常设的
  自动发现：情报中落 general 的条目会自己浮出来。

## 2. Dimension 2: thinking modes · 思维方式

**已覆盖（本轮前）**：流派表 16 行（诠释学/现象学/分析哲学/实用主义/批判理论/结构主义/实证主义/扎根理论/民族志/
古典社会学/经济学两派/行为主义/数学基础三派/经学考据/精神分析）——命名的**解读与论证传统**。

**本轮落地（7 行思维方式节）**：溯因推理 · 临床鉴别诊断 · 设计迭代 · 费米估算 · 思想实验 · 解释风格（范式维度：
覆盖律/机制/叙事不可互换）· 比较方法。这些是**跨领域推理模式**——同一个模式在多个领域出现，此前完全未覆盖。

**仍缺（候选，按触发）**：systems thinking（P29 推迟域同型）· genealogical method · action research ·
simulation/Monte-Carlo 思维 · network thinking · evolutionary variation-selection 思维 · cybernetics/control ·
辩证思维（已有批判理论行部分覆盖）。

## 3. Dimension 3: paradigms / 范式与解释风格

**已覆盖**：M3.13（方法及其假设与失效边界）· 流派表（范式承诺的纪律面）· 本轮的解释风格行（「什么算好解释」跨域
不同：统一/机制/叙事）。

**仍缺（候选）**：Lakatos 研究纲领（进步/退化的判定）· Research programmes per field（每个域的「normal science」
是什么）——方法论地图的 domain 行已有部分；候选按触发。

## 4. Dimension 4: experience · 经验与隐性知识

**已覆盖**：practitioner-playbook · masters-playbook · P16 表达设计（内容单元与读者任务决定形式）。

**仍缺（结构性的）**：**隐性知识（Polanyi）的收录受 D3 限制**——定性/诠释轴的 affordance 是引擎 (b)-move（P52
结论）。这是四维中唯一被引擎结构（而非判据）挡住的一维；触发不变：出现真实定性任务族 → 先记任务 → 再议轴。

## 5. Structural summary · 结构总结

| 维度 | 覆盖度 | 缺口性质 |
|---|---|---|
| 学科 | 34 域 + ~35 未评估 | 判据门控（probe-domains 常设自动发现）；不应穷尽 |
| 思维方式 | 流派 16 行 + **思维模式 7 行（本轮）** | 7 个候选按触发 |
| 范式/解释 | M3.13 + 解释风格行（本轮） | 少量候选（Lakatos 等） |
| 经验/隐性 | playbooks + 表达设计 | **被 D3 affordance 结构性挡住**（唯一的引擎门） |

**穷尽观的修正**：本库的对标不是「收录一切领域」，而是「**每个收录条目都能改变门禁内容**」（P27 判据）+「**漏掉的
会被机制浮出来**」（probe-domains + gap register M5.11 + roadmap 触发）。穷尽式收录违反 M0.6（上下文是有限资源）。

## 6. Verification

methodology-map 新增思维方式节（7 行，三件套格式同流派表）；`methodology-map` 既有守卫（P27 tokens）不受影响；
`P54ThinkingModesTest` 守卫；测试计数见 PROGRESS；`harness cycle audit` → **50 轮 · 0 硬 · 0 缺口**。
