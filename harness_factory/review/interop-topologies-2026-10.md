# Interop topologies · 互操作拓扑（D8 关账轮 · P42）

> **中文速览。** D8 的触发在 P42 开题探测中生效：A2A 仓库/规范（a2a-protocol.org，v1.0.0）与 Agent Teams 文档
> （R250，listed→已读）双双可达。**审计结论：M8.11 的「产物即交接」被两份一手文本从两侧收敛确认**（A2A 规范化
> 之：「Messages should not deliver outputs」；Agent Teams 以邮箱 JSON 文件 + 共享任务列表实践之），并暴露一个
> 真实深化点——**接收方是另一个 agent/进程时，交接状态必须是可分支的声明词表**（terminal ≠ interrupted；
> A2A 规范义务、Agent Teams 文件锁任务状态同形）→ 并入 M8.11，**不新增子句**。M8.10 获第二家 peer-session 拓扑
> 范例。**不加能力**（A2A 已在 sources 追踪；协议机制不构成任务族判别）。D8 → done。

**Updated:** 2026-10-28 · **Round:** P42 (closes D8) · **Evidence level:** A2A spec core sections + Agent Teams doc read in full (access 2026-10-28)

## 1. What the round read · 读到的

| ref | what | load-bearing mechanics |
|---|---|---|
| R266 | A2A Protocol Specification v1.0.0（Linux Foundation；repo 26.3k★） |  opaque 应用间互操作：**Agent Card** 自描述清单（capabilities/skills/securitySchemes/接口序表/可选 JWS 签名/扩展卡）；**Task** 生命周期——终态（COMPLETED/FAILED/CANCELED/REJECTED）与中断态（INPUT_REQUIRED/AUTH_REQUIRED）**规范地区分**；**「Results SHOULD BE returned using Artifacts associated with a Task」「Messages should not deliver outputs」**；三种投递（轮询/SSE 流/ webhook）带事件不重排 MUST；三种绑定（JSON-RPC/gRPC/HTTP+JSON）功能等价要求；OpenAPI 式安全方案；服务端「MUST NOT reveal the existence of…」错误纪律 |
| R250↑ | Agent Teams 文档（listed → **已读**） | 一会话为 lead、队友为**完全独立会话**；**共享任务列表**（pending/in-progress/completed + 依赖阻塞 + **文件锁认领**）；**邮箱 JSON 文件**逐 agent；队友载入项目上下文而非会话历史；明示**实验性**（env 开关）、无会话恢复、一会话一队、无嵌套、token 显著更多；建议 3–5 队友、避免同文件编辑 |
| R251 | LF 新闻稿（listed → **repo 佐证**） | A2A 入 Linux Foundation 在仓库本体得到证实（linux-foundation topic + GOVERNANCE.md/ANTITRUST.md） |

## 2. The audit · M8 子句裁决

| clause | 两份文本的证词 | 裁决 |
|---|---|---|
| **M8.11**（交接走产物不走记忆 + 状态字段） | A2A：产物是**规范化的**输出通道、消息不应交付输出；终态 vs 中断态是规范义务。Agent Teams：交接状态=文件化任务列表 + 邮箱文件；队友不带记忆、载项目上下文——「不走记忆」的直接证实 | **深化（非新子句）**：当接收方是另一个 agent/进程，状态字段必须是**可分支的声明词表**（terminal ≠ needs-input 可区分），结果走产物通道——两源同形，已并入 M8.11 正文 + checklist 一行 |
| **M8.10**（声明拓扑） | Agent Teams 是第二家一手 peer-session 拓扑（lead/teammates/邮箱/任务列表）；A2A 把同一声明义务落在 Agent Card 与任务状态上 | **不变式不变**；范例集扩为 R93 + R250（peer-session）+ R266（应用间互操作） |
| M0.3 builder≠judge / M8 其余 | Agent Teams 队友不继承会话历史——与常驻引用靠项目规则文件持久化的设计互证；成本警告支持 M2.13 的协调开销入账 | 无需改动；记录为佐证 |

## 3. Deliberate non-additions · 刻意不加（M0.5）

- **不加 `agent-interop` 能力**：A2A 已在 `sources.json` 追踪（google-a2a），目录已有 protocols 类；「任务涉及跨应用互操作」在 8 轴上无判别 affordance（collaboration=multi_agent 只覆盖库内多 agent，不区分协议互操作）——与 P39 的 non-addition 同型。重访触发：出现真正以「对接外部 agent 服务」为主业的任务族。
- **不加 A2A 错误纪律子句**（MUST NOT reveal existence）：这是**服务端**实现义务，本库的 harness 绝大多数是客户端；待 harness 开始**作为 A2A 服务端**暴露时再议（触发已记）。
- **不给 Agent Teams 开目录条目**：它是 Claude Code 的实验性功能面（env 开关、明示限制），其价值在本轮是拓扑范例与 M8.11 佐证——P41 的 intake 门（tool-router）会按 metabolism 回访其转正状态。
- **R251 保持 press 级**：状态变化已由仓库本体佐证（P42），新闻稿本身仍不作为机制事实的来源。

## 4. Verification

`PYTHONPATH=src python -m unittest discover -s tests` → **389 OK**（+3 守卫：M8.11 深化内容锚 · §Z/R250 升级/bib · roadmap 关账）；
`harness cycle audit` → **38 轮 · 0 硬 · 0 缺口**；D8 → `done_in P42`；视图重生成。
