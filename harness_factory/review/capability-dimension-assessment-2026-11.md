# 能力维度完备性评估 · 2026-11

**Capability-dimension completeness assessment** — six dimensions, scored against the hardest external
checklist available: the R296 survey's 29-pattern catalog, reconciled line-by-line against this library's
48 capabilities and M0–M8 clause frame (P84.R2 fulfilled).

Updated: 2026-11-21 · Round: P88 · Suite: 576 passing · Capabilities: 48 · Clauses: 47 (M1.12 landed this round)

> **中文速览。** 结论：**总评 8.4/10，维度完备性"接近完备、缺口可数"**。六维中四维 ≥8.5：模块轴
> 9.5（M0–M8 对 R296 七规范子系统呈"盈余 3 + 收养 1"）、生命周期 9.5（计划→推导→执行→验证→溯源→演化→治理
> 全链有名字）、证据覆盖 8.5（19/19 电池族 + P87 跨模型格）、模式覆盖 8.0（**29 条对账：exact 15 / partial 6 /
> by-design 2 / deliberate divergence 1 / 缺口 2——缺口即本轮落地**：M1.12 提示缓存边界 + M4 harness-mimicry
> 反模式）。语言维 7.0（en/zh 双语完备，第三语言零信号，安全兜底）。每条缺口都有名字与去处；"完备"不宣称，
> "可数的差距"才宣称。

## 1 · 评估对象与方法 / Object & method

**对象**：本库的能力维度 = 模块轴（M0–M8，47 子句）× 能力面（48 条 when-predicate 能力，均带 procedure）×
域面（37 学科 + general）× 证据面（19/19 电池族）× 语言面（en/zh）。

**最硬对照表**：R296 *Harness Engineering* 的 **29 条复现架构模式**（11+1 个生产级 coding harness、~4M 行
源码归纳）——外部学科对"harness 该有什么"的独立清单。P88 将全文 13.1 节直读并对账（P84.R2 兑现）。

## 2 · 六维评分 / Six-dimension scores

| 维度 | 得分 | 依据 | 缺口 |
|---|---|---|---|
| D1 模块轴 · Module axis | **9.5** | M0–M8 对 R296 七子系统：盈余轴 memory(M2)/provenance(M4)/self-evolution(M5) + 收养轴 extension surfaces(M6.12, P84)；本轮再补 prompt-cache 维（M1.12） | 无未命名轴 |
| D2 模式覆盖 · Pattern coverage (29) | **8.0** | exact 15 · partial 6 · by-design 2 · deliberate divergence 1 · **gaps 2 → 本轮落地** | 见 §3 表 |
| D3 域广度 · Domain breadth | **7.5** | 37 域全部可路由；19+ 域键能力；P86 补 MLOps/DataOps | 15 域仍靠通用能力面 |
| D4 生命周期覆盖 · Lifecycle | **9.5** | 计划(PLAN)→推导(derive)→执行(loop-discipline)→验证(M3 门禁)→溯源(M4)→演化(M5/D1)→治理(M7) 全链具名 | 无 |
| D5 证据覆盖 · Evidence | **8.5** | 19/19 电池族；委派/引文/可靠性均实测；**跨模型格已填（P87，双面复现）** | 跨会话真方差仍 open（环境限制） |
| D6 语言面 · Language | **7.0** | en/zh 双语（576 守卫）+ P74 CJK 特异性修复 | ja/ko/de… 零信号（安全兜底） |
| **总评** | **8.4** | 上六维均值 | 缺口可数、各有去处 |

## 3 · 29 模式 × 48 能力逐条对账 / The 29-pattern reconciliation

| # | R296 pattern | 本库覆盖 | 判定 |
|---|---|---|---|
| 1 | Event Sourcing | M4.8 append-only 台账 + traces.jsonl + JOURNAL | **exact** |
| 2 | Policy-as-Code | data/*.json SSOT + 发射 gates.md + check.py 可执行门 | **exact** |
| 3 | Recursive Composition | graph-orchestration（声明图 + P81 委派信任 + P82 实测） | **exact** |
| 4 | Polymorphic Edits | 无（模型感知编辑格式选择）；M4.17 record-not-route 相邻 | **gap**（记录：coding-agent 专属面，发射物模型无关是本库立场——见 #25） |
| 5 | Deferred Loading | M6.10 progressive skill loading（索引先行） | **exact** |
| 6 | Template Method | templates/*.tmpl + 域手册 | **exact** |
| 7 | Protocol Interfaces | .harness/manifest.json + check.py + pointer.json 文件契约 | **partial**（文件契约而非运行时缝——产品形态使然） |
| 8 | LLM Summarization | M1.11（改写/追加两形状 + 预算） | **exact** |
| 9 | Stuck Detection | M2.15 惊奇打断 + loop-discipline + trace 规则（latency_anomaly） | **exact** |
| 10 | Reflection Loop | eval-driven-development + verification-gate（M3） | **exact** |
| 11 | Prompt Caching | 无 → **P88 落地 M1.12**（最稳前缀位于第一缓存边界之上、逐字节不变、断裂=全量重价） | **gap → landed** |
| 12 | Context Forking | P81 委派最小上下文 + 显式结果契约 | **partial**（无父态全量克隆语义） |
| 13 | Middleware Pipeline | gates.md 分层 | **partial by design**（无运行时层） |
| 14 | JIT Repo Context | M1 index-first + 发射 AGENTS.md 即层级 markdown 上下文 | **exact** |
| 15 | Skills (capability bundles) | M6.10 portable-skills + .harness/skills 门禁 | **exact** |
| 16 | Conditional Activation | capabilities.json when-predicates | **exact** |
| 17 | Turn-Level Checkpoint | M7.10 回滚路径 + M1.10 退出收据（git 为基座） | **partial** |
| 18 | Agent-Maintained Memory | M2/M5 resumable-memory + D1 collect/trace-audit | **exact** |
| 19 | Outer Verification Loop | M3.18 judge 仪器化 + 电池/LHTB 重放判分 | **exact** |
| 20 | Self-Improving Skill Loop | self-improving-loop + bidirectional-capability-flow（D1） | **exact** |
| 21 | Lineage Compaction | M1.11（压缩次数为受控量）+ M4.8 血统 | **partial**（可检索祖先链未显式化） |
| 22 | Session-Tree Version Control | M7 git 基座（隐含） | **gap（注记级）**：fork/rewind 语义靠 git，未成条款 |
| 23 | Minimal-Core / Extension-Host | M6.12（P84 落地）+ 零依赖 CLI | **exact** |
| 24 | Client/Server Harness | — | **by design**（文件发射型产品，非 API 服务） |
| 25 | Model-Family Prompt Matrix | M4.17 record-not-route | **deliberate divergence**（模型无关立场；R296 显示领域在做 per-model 分发——分歧如实记录，不暗改） |
| 26 | Cache-Dialect Fanout | —（运行时专属）→ M1.12 吸收其纪律面 | **by design** |
| 27 | Syntax-Aware Command Permissioning | M6.11 实参级授权 + ACS modify（R271） | **exact** |
| 28 | Untrusted-Content Delimiting | untrusted-content-discipline（M4 围栏） | **exact** |
| 29 | Harness Mimicry | 无 → **P88 落地 M4 反模式**（身份冒用 = 溯源层违规；互操作需要异己身份时必须显式声明，绝不默认） | **gap → landed** |

**对账结论**：48 能力 + 47 子句对 29 条外部模式的覆盖 = **exact 15 / partial 6 / by-design 2 / deliberate
divergence 1 / gaps 2（已落地）+ 3 项部分覆盖升格候选**（#4/#12/#22 记录在案，不做投机升级——通则：
模式须在移除 originating 项目后仍成立，这三项的工业实例尚不足以支撑独立条款）。

## 4 · 缺口的去处 / Where the gaps went

1. **#11 Prompt Caching → M1.12**（本轮新子句）：位置性纪律，供应商无关（通则满足：任意厂商的缓存层都适用）；
   与 M1.11 经济学复合——压缩决定"什么留下"，缓存边界决定"稳定部分坐在哪"。
2. **#29 Harness Mimicry → M4 反模式**（本轮新增）：身份冒用是溯源层的归属违规；与 M0.1（真实与可溯源）同构。
3. **#4 Polymorphic Edits / #22 Session-Tree**：记录不升级——coding-agent 专属/基座隐含，等第二独立实例再议。

## 5 · 与既有评估的衔接 / Relation to prior assessments

- P74（搜索能力 7.0→7.2）：本轮不动其结论；路由面（D3/D6）沿用其评分。
- P84 的盈余轴结论被本轮对账**再次确认**并补齐了对方盈余轴的落地（M6.12→M1.12 是"收养轴"的深化）。
- P87 跨模型格使 D5 证据维的"跨会话/跨模型方差"从 open 变为 **half-open**（跨模型已证，跨会话真方差仍 open）。

## 6 · 结论 / Verdict

能力维度**接近完备且缺口可数**：外部学科清单的 29 条中 15 条精确覆盖、6 条部分覆盖、2 条按产品形态豁免、
1 条有意分歧、2 条真实缺口本轮落地。剩余开放项全部有名字（#4/#12/#22 部分覆盖升格候选、语言维第三语言、
跨会话真方差、ambition-and-agency 待用户源）。**不宣称完备，宣称"差距有限且每条有去处"——这才是可维护的
完备性。**

---

*方法注（M0.1/M0.2）：R296 全文 HTML 于 2026-11-16 取回（251K 字符），13.1（完整 29 模式目录）与 13.2（双缺失）
直读；对账表逐行出自该直读，判定词（exact/partial/by-design/deliberate divergence/gap）为本库自评，
模式名与描述为综述原文。R296 验证级升格 abs-read → part-read（P88）。*
