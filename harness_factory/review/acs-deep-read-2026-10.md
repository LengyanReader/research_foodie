# ACS deep read · Agent Control Standard 深读（P49 · 观察项链条闭环）

> **中文速览。** P20 观察项 → P43 落地页入册（R270）→ 本轮标准正文深读（R271，v0.1.0）。**裁决：M6.11 深化而非
> 新子句**——ACS 把「授权在具体实参上」物化为可执行的强制架构（19 个生命周期钩子 + allow/deny/**modify**/ask/defer
> 五处置；`modify` 通过**实参重写**实现实参级授权；确定性策略层永远先行、LLM 层从属且不得读策略源）。其 v0.1.0 的
> 两个**自报缺口**（线缆未认证 #70、决策失败默认 **fail-open** #32/#37）正是本库 default-fail 原则所禁的反模式——
> 采纳警示与范例一并记录。

**Updated:** 2026-10-28 · **Round:** P49 · **Evidence:** repo overview + spec structure read (access 2026-10-28); 44 JSON Schemas 未逐条核（预-1.0 阶段无必要）

## 1. What ACS is · 标准本体

OWASP GenAI Security Project 的**线上规范**（wire specification），三支柱：
- **Instrument**——钩子与处置机制（ACS-Core 强制基线 = Instrument + wire format + 审计链）；
- **Trace**——每个钩子与决策都是 OTel span + OCSF 事件（`.acs/envelopes.jsonl`——与 M4.8 账本纪律同构）；
- **Inspect**——AgBOM：agent 的模型/工具/依赖活体清单（CycloneDX/SPDX/SWID 序列化）。

双方角色：**Observed Agent**（被观察的 LLM 系统）与 **Guardian Agent**（线上另一端做决定者）。19 个生命周期钩子
（工具调用请求、会话起止、轮边界、知识检索、记忆读写……），每个钩子等 Guardian 的五处置之一：
**allow / deny / modify / ask / defer**——`ask` 即 M0.8 人类门的协议化（路由到人/agent/服务审批者）。

## 2. The audit · 对本库的裁决

| 本库条款 | ACS 的证词 | 裁决 |
|---|---|---|
| **M6.11**（暴露≠授权；授权在具体实参上） | `modify` 处置**物化**了实参级授权（重写 `SELECT *` → 具名列 + LIMIT）；确定性策略层永远先行，LLM 层从属且不得读策略源（M3.17/M5.13 的评判者从属结构的执行化） | **深化**：M6.11 增一句强制架构范例（已落） |
| **M3 默认失败 + 证据门** | v0.1.0 默认决策失败 = **fail-open**（Guardian 崩溃即静默失去治理，需显式设 deny）——本库 default-fail 原则所禁的反模式，一手实例 | 记录为警示（随 M6.11 深化句） |
| **M0.8 人类门** | `ask` 处置协议化路由 | 范例记录，无改动 |
| **M4.8 只追加账本** | 审计链 envelopes.jsonl | 同构佐证，无改动 |

**刻意不加**：不加 `policy-enforcement` 能力（ACS 是 M6.11 的强制架构范例，不构成任务族判别）；不据 v0.1.0（预-1.0、
自声明符合、自报未认证线缆）落任何门禁义务——**标准自身声明了它的不成熟**，引用即带此标注（M0.2）。

## 3. Verification

M6.11 深化句落 core/07；levers security 行增 ACS 指针；references **R271**（+bib）+ 范围 R1–R271；source-map
M6.11 行扩展；frontier 文档 P43 注记更新（深读完成）。`P49AcsGuardTest` 守卫；测试 **396 → 399**（含 P47/P48 守卫）。
