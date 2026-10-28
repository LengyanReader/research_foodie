# Frontier sweep · 前沿扫荡（2026-10-28 · P43）

> **中文速览。** 六路扫荡（上下文工程 · 自演化 · 评测完整性 · 智能体安全 · 厂商 harness · 中文话语），四篇全文
> + 一份落地页：**R267**（自演化技能的反馈动力学——「只喂成功轨迹选不出任何改进」，M5.14 的定量根基）、**R268**
> （上下文压缩理论——压缩预算=通信复杂度，M1.11 深化）、**R269**（ABC 基准检查单——任务/结果双有效性，M3.19）、
> **R270**（OWASP ACS 发布——P20 观察项到期关闭）。二手命中（中文话语、多 harness 编排器、EvolveR 谱系）按不洗源
> 规则只作发现指针。**最重要的自证**：R267 的设计与本库 trace 词表同构——「通过的 gate 不记、错过的 gate 才是事件」
> 从此有了外部定量依据。

**Updated:** 2026-10-28 · **Round:** P43 · **Method:** 六路检索 → 解析 id（不猜）→ 全文读 → 判别性裁决

## 1. The fronts and what they hit · 六路与命中

| front | hits | disposition |
|---|---|---|
| 上下文工程/记忆 | **R268** Context Compaction Theory（全文）· Context Engineering 2.0（2510.26493，survey，listed）· HaystackCraft · 多篇生产者博客 | R268 落 M1.11 深化；survey 类列 listed |
| 自演化/轨迹 | **R267** Feedback Dynamics（全文，**D1 的定量同构**）· EvolveR 2510.16079 · SE-Agent 2508.02085 · Feedback-to-Plan 2605.26720（均 listed） | R267 落 M5.14；其余列 listed（谱系已在 R252/R256 覆盖主干） |
| 评测完整性 | **R269** ABC 2507.02825（全文）· Adaline 评测危机评论（二手）· Harbor 评测框架（Terminal-Bench 团队，listed） | R269 落 M3.19；Harbor 记为评测基础设施候选（`data/harnesses.json` eval 类回访项） |
| 智能体安全 | **R270** ACS 发布（落地页读，标准正文待深读）· OWASP Agentic Solutions Landscape Q2 2026（社区景观，目录页未定位到正式文档——lead）· Agentic 网络攻击工业化 2605.06713（listed） | ACS 关闭 P20 观察项；solutions 目录记为 P41 tool-router 的回访线索 |
| 厂商 harness | SKILL.md 兼容已成三家共识（Codex/Gemini CLI 支持 skills）· 多 harness 编排器（Claude Octopus 等，**仅 FB/Reddit 二手**） | 兼容性验证 P1 的判断（不落新条）；编排器全部不入目录（无可达一手 repo 本轮未核） |
| 中文话语 | 「从追求智商到追求耐久性」的范式叙事 · 文件式记忆自闭环 · MemGPT 冷热分离 · Agent Memory 综述（知乎/腾讯云社区，**全部二手**） | **生态信号记录**：harness 范式在中文工程话语中已成主流——与 R268 的生产系统分类互证；按不洗源规则不作引用，最多作为发现指针 |

## 2. What landed · 落地（判别性裁决）

- **M5.14 · 失败是必需信号**（`core/06`）：success-only 的进化循环 **0/14 选中**（42 组实验）；失败记录须带诊断
  （期望-观测不匹配）入池；停止条件先声明；验证-测试反转实测在案——验收门与部署读数保持两个数。
  **自证**：本库 trace 词表的「通过不记、miss 才记」与 harvest 只在失败时自动落行（P22 设计）获得外部定量支撑。
- **M3.19 · 基准双有效性**（`core/04`）：task validity（当且仅当具备能力才可解）+ outcome validity（检查真能指示
  成功）是可检验主张；量化失效：改题库拿满分（隔离失效）、数日志 SLEEP 子句（32.5% 高估）、清单修正后 −33%；
  构造侧义务（与真值隔离、冻结版本、评判器先导）与 M3.18 的评判者义务互补成完整闭环。
- **M1.11 深化**（`core/02`）：压缩预算是查询类属性（Θ(log n) 的 selection 惩罚；重复压缩误差累积——压缩次数本身
  是被追踪的数字；sketch 形负载该用 sketch——Bloom filter 范例）。
- **R270/ACS**：P20 观察项关闭（落地页级）；标准正文深读 = 后续轮候选（它与 M6.11 暴露≠授权、M7 治理的接口
  可能判别——待全文）。

## 3. Deliberate non-additions · 刻意不加（M0.5）

- **不加 context-compaction 能力**：压缩是 M1/M2 的参数空间（策略选择），不是任务族判别——R268 本身把它当
  **预算问题**而非能力问题。重访触发：出现以「为特定查询类选压缩策略」为主业的任务。
- **不加 skill-evolution 能力**：M5.14 落子句即可；R267 的机制（验证门 + 字节异同 + 哈希身份）全部被 M5.13/M5.14
  与 M4.8 账本纪律覆盖，能力条目只会重述。
- **多 harness 编排器不入目录**：仅二手来源（FB/Reddit），无可核一手 repo——记 lead，tool-router metabolism 回访。
- **Harbor 不入目录（本轮）**：评测基础设施与 `data/harnesses.json` 的 eval 类相关，但其任务套件与本库记分集的
  关系（可否作为 effect 轴的真实运行环境）是 D1 阶段 C 的问题——先记候选，阶段 C 开轮时一并核。
- **中文社区条目不进 sources**：无可追踪的一手实体（匿名社区文章）；生态信号只记录在本文件。

## 4. What this validates about the library itself · 对本库的自证

1. **trace 词表设计**（P22）：R267 的「失败轨迹是选择力的唯一来源」= 本库 gate_miss/human_correction 事件地位
   的外部定量版本——使用侧积累失败事件不是可选项，是循环能不能选出改进的前提（M5.14 化）。
2. **M5.13 的形态**：R267 的验证门/严格改进/回滚/字节异同与本库验收门（预声明判据 + 拒绝边界 + M4.8 只追加
   账本）逐条同构——两个独立传统收敛到同一程序。
3. **记分集文化**：R269 的 ABC 是「基准构造纪律」的社区化版本——本库的 CountDriftGuard/守卫测试/有意基线编辑
   在同一方向上，但 M3.19 提醒：**effect 轴开测时**（阶段 C），effect_metric 的任务/结果双有效性要按 ABC 过一遍。
4. **M1 的预算纪律**：R268 把「压缩有损」从格言变成可计算的上界——context_policy 的 token 预算从此有理论参照。

## 5. Verification

测试 **389 → 392**（+3 守卫：M5.14/M3.19 内容锚 · §AA 引用与 bib · frontier cue 关闭）；`harness cycle audit` →
**39 轮 · 0 硬 · 0 缺口**；参考文献 **R1–R270**（§AA 四条，其中三条全文级，作者列表自 abs 页逐条核录）；ACS 观察项关闭。
