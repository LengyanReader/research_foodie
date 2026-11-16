# Trend Review (weekly issue 3) · 趋势周报（第三期）

**Updated:** 2026-11-16 · **Round:** P84 · **Data window · 数据窗口:** intel 2026-11-09 → 2026-11-16（1 周 · 1 week, 3,041 items）· **Previous issue · 上一期:** [trend-review-2026-11-09.md](trend-review-2026-11-09.md)

> **中文速览。** 第三期（自动化 11-09 首跑成功、11-16 计划触发未见产出，本轮人工补位，自动化保持启用）。两条主线：
> ① **"harness engineering" 已成综述级学科**——Barbaste 的 *Harness Engineering* 综述（arXiv:2609.00006，R296 新入册）
> 解剖 **11+1 个生产级 coding harness / 约 400 万行源码**：七规范子系统（loop·tools·context·safety·orchestration·
> extension surfaces）、29 个复现设计模式、18 条设计建议、90 行最小可行 harness；头条实证：**无任何运行时引入
> agent 框架、无任何向量嵌入检索**（"hand-rolled async loops and deterministic retrieval"），且 **Skills 采用 9/11
> 胜 MCP 8/11**——本库的零依赖 CLI + 确定性信号匹配 + portable-skills 姿态三条设计押注同时获得独立实证背书。
> ② **dsh 规模化**：1.54M DAU（SCMP，二手）、v0.2.2-rc.2（11-11）、"Super Agent" 原型（11-02）；星数存在源间
> 分歧（repo 页 ~278k vs 博客 95k+，取 repo 页为准并记录分歧）。论断 T8（平台转向）见 §5。对账与行动项见 §3/§6。

> **Executive summary.** Issue 3 (the automation's 11-09 first fire succeeded; the 11-16 scheduled fire produced no
> output — this issue is the manual backfill, automation left armed). Two main threads: **(1) "harness engineering"
> is now a survey-grade discipline** — the Barbaste *Harness Engineering* survey (arXiv:2609.00006, R296 newly
> registered) dissects **11+1 production coding harnesses / ~4M lines of source**: seven canonical subsystems
> (loop · tools · context · safety · orchestration · extension surfaces), 29 recurring design patterns, 18 design
> recommendations, a 90-line minimum-viable harness; headline empirics: **no runtime imports an agentic framework
> and none uses vector-embedding retrieval** ("the field runs on hand-rolled async loops and deterministic
> retrieval"), and **Skills adoption 9/11 beats MCP 8/11** — three of this library's standing design bets
> (zero-dependency CLI, deterministic signal matching, portable-skills-first) got independent empirical backing in
> one paper. **(2) dsh at scale**: 1.54M DAU (SCMP, secondhand), v0.2.2-rc.2 (11-11), a "Super Agent" prototype
> (11-02); star counts disagree across sources (repo page ~278k vs a blog's 95k+ — repo page kept as primary, the
> disagreement recorded). Thesis T8 (the platform turn) in §5; reconciliation and action items in §3/§6.

---

## 1 · 本周信号 · Weekly signals

| # | 信号 · Signal | 源 · Source · Date | 判读 · Reading | 核验 · Verified |
|---|---|---|---|---|
| 1 | **Harness Engineering 综述**：11+1 系统 / ~4M 行源码研究；七规范子系统；29 模式；18 建议；90 行 MVH；纵向 re-diff | [arXiv:2609.00006](https://arxiv.org/abs/2609.00006)（abs 页直读） | "harness engineering" 的独立学科化标志——解剖学与模式目录同时成立 | ✅ abs-read |
| 2 | 综述头条实证：**无运行时引入 agent 框架、无向量嵌入代码检索**；"hand-rolled async loops and deterministic retrieval" | 同上 | 零依赖 + 确定性检索不是本库的怪癖，是**领域的实测主流** | ✅ abs-read |
| 3 | **Skills 采用 9/11 胜 MCP 8/11**；行为策略「从提示散文迁移到配置」；"convergence becoming imitation" | 同上 | portable-skills 优先姿态获采用面数据背书；SSOT 数据化条款与「配置迁移」同构 | ✅ abs-read |
| 4 | **平台转向**："in the first half of 2026 the coding harness completed a turn from tool to platform"；ACP 出现于 6 系统，催生「第三角色：harness hosting」 | 同上 | 本库 T1/T4 线索的学科级表述；harness 成为被托管对象 | ✅ abs-read |
| 5 | **dsh 规模化**：1.54M DAU（上线 <3 月）；"Super Agent" 编码代理原型（对位 Claude Code） | [SCMP](https://www.scmp.com/tech/big-tech/article/3373757/can-deepseek-challenge-openai-anthropic-ai-agents-harness-adoption-takes)（二手）；[SiliconRepublic](https://www.siliconrepublic.com/machines/deepseek-rival-anthropic-new-coding-agent-ai-rivals-anthropic)（11-02，二手） | dsh 从 dev preview 走到规模采用；R295 生命周期注记升级 | ✅ search-verified（二手转述） |
| 6 | **dsh v0.2.2-rc.2**（11-11）——rc 节奏延续 | dsh releases feed（P81 重锚后入流） | 四周 11 个 tag；beta 快速迭代未收敛 | feed-sourced |
| 7 | 星数源间分歧：repo 页 ~278k（2026-11-11 直读）vs 博客 95k+ | repo 页 vs [flowtivity 博客](https://flowtivity.ai/blog/deepseek-harness-open-source-agent-explained) | 取 repo 页为准（一手），分歧如实记录——二手数字混用是常见引用病 | ✅（分歧已记录） |
| 8 | 综述家族成形：*Code as Agent Harness*（2605.18747）· *Agentic Harness Engineering: Observability*（2604.25850）· 110+ 论文分类法 · awesome-agent-harness（RUCAIBox） | arXiv / GitHub（搜索发现） | 学科化的多源印证；本库避免逐一入册（引用膨胀），家族记于 R296 条目内 | ✅ search-verified（家族注记） |

## 2 · 行业全景与相邻领域 · Industry landscape and adjacent fields

### 中文

数据基座：industry 簇 2,577 条（30 天内 235），28 源；delta −132（窗口锚点混杂：上张快照 11-10 生成、窗口更长——
非热度判断依据，见 §7）。

**dsh 的规模化三连。** 信号 5+6+7 合读：一个 8 月才进 dev preview 的 harness，11 月已有 1.54M DAU 的二手报道、
持续 rc 节奏、与 Claude Code 对位的产品线（Super Agent）。辩证面：DAU 是**二手转述**（SCMP），星数源间差近 3 倍——
规模数据先记方向、不记精确值；真正一手的是 feed 里的 rc 节奏（每周 2–3 个 tag）。「dev preview + 破坏性变更声明 +
百万级采用」并存，本身就是平台转向（T8）的用户侧证据。

**执行环境商品化再确认。** 上两期的基建版本节奏主线本周延续（Langfuse/E2B/LiteLLM 线仍在发版）；新增的是
**托管位**信号：ACP 六系统采用、"harness hosting" 作为第三角色（信号 4）——执行环境从「商品」走向「被托管平台」。

### English

Data base: 2,577 industry items (235 within 30 days), 28 sources; delta −132 (window-anchor confound — the previous
snapshot was generated 11-10 with a longer window; not a heat signal, see §7).

**dsh's scaling triple.** Read signals 5+6+7 together: a harness that entered dev preview in August already has a
secondhand 1.54M-DAU report, a sustained rc cadence, and a Claude Code-counterpart product line (Super Agent).
Dialectics: the DAU figure is **secondhand** (SCMP) and star counts differ ~3x across sources — record direction, not
precision; the first-hand fact is the feed's rc cadence (2–3 tags/week). "Dev preview + breaking-changes warning +
million-scale adoption" coexisting is itself user-side evidence of the platform turn (T8).

**Execution-environment commodification, reconfirmed.** The infra release-cadence thread continues; what is new is the
**hosting slot**: ACP in six systems and "harness hosting" as a third role (signal 4) — execution environments moving
from commodity toward hosted platform.

## 3 · Harness 文献综述 · Harness literature synthesis

### 中文

**七规范子系统 ↔ M0–M8 对账（R296，本周核心对账线）。** 综述的解剖轴（loop · tools · context management ·
safety controls · orchestration · extension surfaces）映射：loop/tools→**M6**（loop-discipline、tool-use）；
context management→**M1**；safety→**M0/M3/M7**（元原则·门禁·治理）；orchestration→**M8**（graph-orchestration）。
两个结构性发现：① **本库的盈余轴**——综述七子系统未把 memory（M2）、provenance（M4）、self-evolution（M5）
列为规范子系统，本库在这三轴上的持续投入是**差异化所在**，且各有实证背书（R268/R279 记忆线、M4 引用纪律线、
D1 自演化线）；② **对方的盈余轴**——"extension surfaces"（插件/技能扩展面）被列为规范子系统，而本库把它收纳在
M6 之内（portable-skills）。dsh 的"Everything is a Plugin"正是扩展面优先的极端形态。处置：**提案级**范围注记
（P84.R1），不新开模块——扩展面的纪律内容（版本化、安全审查、可移植门禁）本库已有，缺的只是把它从 M6 的
隐含位提到命名位。

**零依赖与确定性检索的实证背书（设计验证）。** 信号 2：~4M 行生产 harness 源码里**零 agent 框架导入、零向量
嵌入检索**——本库 AGENTS.md 的 stdlib-only 门与 classify.py 的确定性信号匹配，从「工程偏好」升格为「领域实测
主流」。这不结束辩证：综述观察的是 11 个系统的**现状**，不是最优解的**证明**——语义检索在长尾词汇上的优势
仍可能让下一代 harness 改判；记录为「押中一次」，不是「永远正确」。

**Skills>MCP 的采用面数据（R296）。** 9/11 vs 8/11——本库 portable-skills 一等、M6 技能门禁的设计与采用面
数据同向。与 R276/R278（AAIF 治理线）合并读：技能生态既有治理（基金会）又有采用（9/11）——T2 双轨论的
新证据点。

### English

**Seven canonical subsystems ↔ M0–M8 reconciliation (R296, this issue's core line).** The survey's anatomy
(loop · tools · context management · safety controls · orchestration · extension surfaces) maps: loop/tools→**M6**;
context management→**M1**; safety→**M0/M3/M7**; orchestration→**M8**. Two structural findings: (1) **this library's
surplus axes** — the survey's canonical subsystems do NOT include memory (M2), provenance (M4) or self-evolution
(M5) as separate subsystems; this library's sustained investment there is its differentiation, each with empirical
backing (R268/R279 memory; M4 citation discipline; the D1 self-evolution line). (2) **Their surplus axis** —
"extension surfaces" is a canonical subsystem while this library hosts it inside M6 (portable-skills). dsh's
"Everything is a Plugin" is extension-surface-first in the extreme. Disposition: a **proposal-level** scope note
(P84.R1), not a new module — the discipline content (versioning, security review, portability gates) already exists
here; what's missing is promoting it from M6's implicit slot to a named slot.

**Empirical backing for zero-dependency + deterministic retrieval (design validation).** Signal 2: across ~4M lines
of production harness source, **zero agentic-framework imports and zero vector-embedding retrieval** — this library's
stdlib-only gate and classify.py's deterministic signal matching upgrade from "engineering preference" to "measured
field mainstream". Dialectics stay open: the survey observed eleven systems' *status quo*, not a *proof of optimum* —
semantic retrieval's long-tail advantage could still flip the next generation; recorded as "bet won once", not
"right forever".

**Skills>MCP adoption data (R296).** 9/11 vs 8/11 — portable-skills-first and the M6 skill gates point the same way
as the adoption data. Read with R276/R278 (the AAIF governance line): the skills ecosystem now has both governance
and adoption — a new datapoint for the T2 dual-track thesis.

## 4 · 新兴方向 · Emerging directions

### 中文

诚实声明：trajectories/domains 两簇仍各 1 源（探针已落、产出待新锚点生效——devops-platform 的 17 个探针词
已充实，缺口在情报产出侧）。本周「新兴」主体是**学科化本身**：harness engineering 从工程实践升格为有综述、
有模式目录、有分类法的学科（信号 1/8）。次级方向：综述家族中的 *Code as Agent Harness*（2605.18747）主张
「代码即 harness」的本体论——与本库「emitted harness 就是文件树」的立场同构，记为观察。

### English

Honest disclosure: the trajectories/domains clusters still have one source each (probes landed; yield awaits the
re-anchored sources — devops-platform's 17 keywords are adequate, the gap is yield-side). This week's "emerging"
story is **disciplinization itself**: harness engineering graduating from practice to a field with surveys, pattern
catalogs and taxonomies (signals 1/8). Secondary: *Code as Agent Harness* (2605.18747) in the survey family argues
a "code as the harness" ontology — isomorphic to this library's "an emitted harness is a file tree" stance; logged
as an observation.

## 5 · 分析与预测 · Analysis & predictions

| # | 论断 · Thesis | 证据 · Evidence | 置信 · Confidence | 反转条件 · Reversal condition |
|---|---|---|---|---|
| T8 | **平台转向**：coding harness 在 2026 上半年完成「工具→平台」转向；harness 成为被托管对象（hosting 第三角色），竞争位从功能表转向生态位 | R296 中心论断 + ACP 6/11 + dsh 托管化采用（二手 DAU） | 中高 · Med-high | 若托管 harness 的采用曲线在 2027H1 走平且自托管比例反升 |
| T9 | **学科固化**：harness engineering 在 12–18 个月内出现标准教科书式课程与专项会议/workshop | 综述家族（110+ 论文分类法 · 多 survey 并发） | 中 · Med | 若综述家族引用衰减且无后续实证研究跟进 |
| T1″ | （T1 状态更新）可信度工程基础设施化：**reinforced again**——R296 的 18 设计建议与 29 模式目录是「工程知识固化」的学科级形态 | 信号 1 | 维持中高 · holds | 不变 |

### 中文（论断补充）

**辩证面：** T8 的反例——平台化可能重演「框架膨胀」老路（被托管 = 被锁定），而综述实证的「零框架导入」恰恰
说明**一线在逃离框架**；平台层与运行时层的诉求可能分道扬镳（托管平台赢、框架库输）。T9 的反例——综述激增
也可以是领域过热的晚期信号（学科化与泡沫化在别的历史上多次共生）；观察指标是**实证研究比例**而非综述数量。
本库的对位动作：保持零依赖与可移植（不被任何平台层锁定），把「被托管」当部署选项而非架构前提。

### English (thesis notes)

**Dialectics:** T8's counter — platformization could replay the framework-bloat story (hosted = locked in), and the
survey's zero-framework empiric shows **the front line is fleeing frameworks**; platform-layer and runtime-layer
interests may diverge (hosting platforms win, framework libraries lose). T9's counter — survey proliferation can be
a late-stage overheat signal (disciplinization and bubble-formation have co-occurred elsewhere); the watch metric is
the **ratio of empirical studies**, not survey count. This library's counter-move: stay zero-dependency and portable
(locked into no platform layer), treat "being hosted" as a deployment option, never an architectural premise.

## 6 · 对 harness 的行动项 · Action items for the harness

### 中文

1. **P84.R1（提案级）**：M6 范围注记——「extension surfaces（插件/技能扩展面）是 R296 的规范子系统；本库将其收纳于 M6（portable-skills 门禁、版本化、安全审查、可移植），显式命名其在 M6 内的位置」；不新开模块。
2. **P84.R2（下轮全读候选）**：R296 的 29 模式目录 vs 本库 46 能力逐条对账（判别：已覆盖/部分覆盖/缺口）——学科模式目录是能力面最硬的外部对照表。
3. **P84.R3（观察级）**：devops-platform 探针已充实（17 词），缺口在情报产出侧——观察下两期是否随新锚点生效而回升，不再加词。
4. **P84.R4（运维注记）**：自动化 11-09 首跑成功（runCount=1，产出 P79）；11-16 计划触发未见产出——本轮人工补位，自动化保持启用；若下周一仍未见产出，考虑检查宿主会话常驻条件。

### English

1. **P84.R1 (proposal):** M6 scope note — "extension surfaces (plugin/skill extension plane) is an R296 canonical
   subsystem; this library hosts it inside M6 (portable-skills gates, versioning, security review, portability)";
   no new module.
2. **P84.R2 (next-round full-read candidate):** reconcile R296's 29-pattern catalog against this library's 46
   capabilities line by line (covered / partial / gap) — a discipline-grade pattern catalog is the hardest external
   checklist the capability face can get.
3. **P84.R3 (observation):** devops-platform probes are adequate (17 keywords); the gap is yield-side — watch the
   next two issues as re-anchored sources take effect; no more keyword stuffing.
4. **P84.R4 (ops note):** the automation's 11-09 first fire succeeded (runCount=1, produced P79); the 11-16
   scheduled fire produced no output — this issue is the manual backfill, automation left armed; if next Monday
   again shows no output, check the host-session residency condition.

## 7 · 方法与数据附录 · Method & data appendix

### 中文

**管线：** `harness intel --root . --since 2026-11-09`（上周一锚点）→ 3,041 条 → `trend --write`（判别性打分 +
每源 ≤3 + hex 噪声惩罚 + 周际 delta）。承重信号核验四级标注（abs-read / search-verified / feed-sourced / 分歧已记录）。

**窗口混杂声明：** 本期窗口 11-09→11-16（7 天）；上张快照 11-10 生成（窗口起点更早）——delta（−132/−160）不可
读作降温；且上期 full-update（11-11）的 trend 相以不同窗口计数（3,297），快照序列的干净衔接从本期锚点起算。

**自动化状态（诚实记录）：** CronList 显示 runCount=1 / lastRunAt=2026-11-09——首跑即 P79；11-16 触发未见产出，
本轮人工补位；自动化未删除、保持启用。

**星数分歧处置：** dsh 星数以 repo 页直读值（~278k，2026-11-11）为一手；博客 95k+ 记为分歧来源；不取平均、
不隐去任何一方。

### English

**Pipeline:** `harness intel --root . --since 2026-11-09` (last-Monday anchor) → 3,041 items → `trend --write`
(discriminator scoring + per-source cap + hex-noise penalty + weekly delta). Load-bearing signals carry four
verification grades (abs-read / search-verified / feed-sourced / discrepancy-recorded).

**Window-confound disclosure:** this window is 11-09→11-16 (7 days); the previous snapshot was generated 11-10 with
an earlier window start — the delta (−132/−160) must not be read as cooling; the 11-11 full-update's trend phase
also counted a different window (3,297). Clean snapshot sequencing starts from this issue's anchor.

**Automation status (honest record):** CronList shows runCount=1 / lastRunAt=2026-11-09 — the first fire produced
P79; the 11-16 fire produced no output; this issue is the manual backfill; the automation remains enabled.

**Star-count discrepancy handling:** dsh stars use the repo page's direct read (~278k, 2026-11-11) as primary; the
blog's 95k+ is recorded as the disagreeing source; no averaging, nothing hidden.

## 溯源表 · Provenance

| 声明 · Claim | 一手源 · Primary source | 访问日期 · Accessed |
|---|---|---|
| Harness Engineering 综述（11+1 系统 / ~4M 行 / 七子系统 / 29 模式 / 零框架·零向量检索 / Skills 9/11 vs MCP 8/11 / 平台转向） | [arXiv:2609.00006](https://arxiv.org/abs/2609.00006)（abs 页直读） | 2026-11-16 |
| dsh 1.54M DAU | [scmp.com](https://www.scmp.com/tech/big-tech/article/3373757/can-deepseek-challenge-openai-anthropic-ai-agents-harness-adoption-takes)（二手转述） | 2026-11-16 |
| dsh "Super Agent" 原型（11-02） | [siliconrepublic.com](https://www.siliconrepublic.com/machines/deepseek-rival-anthropic-new-coding-agent-ai-rivals-anthropic)（二手） | 2026-11-16 |
| dsh v0.2.2-rc.2（11-11） | dsh releases feed（P81 重锚） | 2026-11-16 |
| 星数分歧（~278k vs 95k+） | repo 页直读（2026-11-11）vs [flowtivity.ai](https://flowtivity.ai/blog/deepseek-harness-open-source-agent-explained) | 2026-11-16 |
| 综述家族（2605.18747 · 2604.25850 · 110+ 分类法 · awesome-agent-harness） | arXiv / GitHub（search-verified，家族注记于 R296） | 2026-11-16 |

*引用即生命线 · Citations are the lifeline：abs-read = arXiv 摘要页直读；search-verified = 搜索核验（未读全文）；
feed-sourced = 管线抓取原始 URL；二手转述均标注、不冒充一手。*
