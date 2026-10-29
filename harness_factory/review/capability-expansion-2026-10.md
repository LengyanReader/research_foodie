# Capability expansion · 能力开拓轮（P52）

> **中文速览。** 用户指示「全面探索还有哪些新能力可纳入」。方法：**内部覆盖矩阵**（34 域 × 43 能力的键控分析）
> + 前沿确认（2026 共识「Agent = Model + Harness」的关切面——scope/沙箱/可观测——均已被既有条款承载）。**裁决：
> 落 4 个域键控能力**——它们是 **P27 判别力表格里预命名但未落地**的学科纪律（history→source-criticism ·
> philosophy→argument-reconstruction · political-science→concept-definition · ai-safety→safety-argumentation），
> 内容已溯源、触发天然判别（各只命中本域）。**诚实的结构结论**：8 轴向量上的 (a)-move（既有轴×域组合）已近饱和；
> 剩余候选多为 (b)-move（需要引擎 affordance），逐项带触发记录。

**Updated:** 2026-10-28 · **Round:** P52 · **Method:** 覆盖矩阵 + 判别裁决（M5.10）

## 1. The internal matrix · 覆盖分析

- 19 个域无直接域键控能力，但多数经 `any` 旁路覆盖（`evidence-bounded-generation` 经 `grounding=required` 触达
  大量研究族域；`formal-verification` 经 `verifiability=high × artifact=code` 触达代码族）；
- **四个域的 README 带独有门禁内容却无能力钉住**——且 P27/P29 的判别力表格**已预命名**它们（判据先行先于建域，
  内容已溯源）：这是最便宜也最合法的一批 (a)-move；
- 其余域（arts-design/devops/reading/…）的门禁内容或不具独有的判别结构（组合即覆盖），或需新的溯源工作才可落。

## 2. What landed · 落地（4 条，各只命中本域——判别力由构造保证）

| capability | domain | 纪律内容（溯源） |
|---|---|---|
| `source-criticism` | history | 史源分级 · 独立见证互证 · 断代显式 · **沉默入账**（P27 表格预命名） |
| `argument-reconstruction` | philosophy | 前提-结论形式重构 · 立场声明 · **反例坦诚**（先陈述对手最强形式） |
| `concept-definition` | political-science | 概念界定先于案例选择（concept stretching 是失效模式）· 方法声明 · **案例选择留痕** |
| `safety-argumentation` | ai-safety | L0–L5：安全属性/威胁模型先行（M3.10）· 红队留痕（M3.15）·「拒答」≠「无能力」 |

各条 modules/why 见 capabilities.json；router 四行；source-map 四行。

## 3. Deliberate non-additions · 刻意不加（逐项带理由）

| 候选 | 裁决 | 理由 / 触发 |
|---|---|---|
| scope 泄漏纪律（上下文/权限越界） | 不加 | M6.11（暴露≠授权）+ M1 的预算纪律已承载；2026 前沿的「scope」关切与现有条款同形 |
| GUI/computer-use 纪律 | 不加 | P19 已裁「属沙箱执行（M6）」；无 GUI affordance，触发器造不出来 |
| agent 身份/凭证scoping | 不加 | R271（ACS）身份概念是 M6.11 的深化路径，非独立判别能力 |
| 个人数据/合规纪律 | 不加（lead） | 8 轴无 data-sensitivity affordance——**引擎演化项**，与 D3 同型；出现真实合规任务族时先记任务再议轴 |
| arts-design 创作纪律 | 不加（lead） | 判别内容需要已溯源的创作方法一手材料（设计引注/资产许可）——现有 grounding=off 边界是有意裁决 |
| qualitative-rigour | 不加 | D3 原样（需 interpretive affordance） |
| 谱系能力（spec-driven、agentic-RAG 等） | 不加 | 分别被 plan-first/M0.3、evidence-instruments+outlets 覆盖（P14/P18 已录非新增） |

**结构结论**：(a)-move（既有轴×域的判别组合）经本轮后**接近饱和**——剩余域要么组合即覆盖、要么需新溯源；
下一批能力的正门是 (b)-move（引擎 affordance：interpretive/modality/data-sensitivity），每次都要付「引擎+全部
能力触发器」的两次代价（P16.6 先例）——按触发逐个开。

## 4. Verification

`harness cycle audit` → **48 轮 · 0 硬 · 0 缺口**；能力 **39 → 43**；router +4 行；source-map +4 行；
`P52DomainCapabilityTest` 守卫（四能力各命中本域任务、不命中邻域任务）；测试计数见 PROGRESS。
