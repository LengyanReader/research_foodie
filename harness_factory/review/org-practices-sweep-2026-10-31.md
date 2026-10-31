# Org practices sweep · 机构实践与创意评估（P57 · Anthropic/DeepSeek 等）

> **中文速览。** 用户问：Anthropic、DeepSeek 等机构近期有无 harness 能力与 workflow 的项目实践/创意可融入。方法：
> 多路检索 → 一手读两篇全文（R276 AAIF 捐赠公告 · R277 superpowers 仓库）+ 四项目 listed（R278）。**裁决：① Agent
> Skills 治理迁入 AAIF（Linux Foundation）——发射格式现为中立基金会治理，登记+目录注记；② superpowers 是
> Exemplar 级实践框架，采纳其一个具体机制（**压缩后重注入引导**入发射模板 + M1.11 范例），其余为佐证；③ AAIF
> 新三项目入目录（Open Responses/OpenEnv/**OpenSandbox**——后者直通 A.3 #3 悬置的「具体沙箱后端」缺口）；
> ④ DeepSeek V4.1-Flash/DeepInfer 记为景观 lead（模型/部署侧，不触能力面）；⑤ Opus 5.5（10-18）入 model-families
> 注记（P19 后续的方向性更新）。

**Updated:** 2026-10-31 · **Round:** P57 · **Evidence:** R276/R277 read in full；R278 listed；DeepSeek/Opus 条目 listed

## 1. What the orgs shipped · 机构动态清单（截至 2026-10-31）

| 机构 | 动态 | 日期 | harness 相关性 |
|---|---|---|---|
| Anthropic | **Agent Skills 捐入 AAIF**（Linux Foundation；与 Block/OpenAI 共建；MCP 同门） | 10-22 | 发射格式（SKILL.md）的治理去向——中立化完成 |
| AAIF | 四新项目：Agent Skills（Anthropic）· **Open Responses**（OpenAI，跨厂商 agent API 格式）· **OpenEnv**（HF+Meta，RL/智能体训练评测环境标准）· **OpenSandbox**（阿里，agent 代码隔离执行沙箱平台） | 10-22 | 三条新标准线全部在 harness 相关层（API 互操作 / 评测环境 / 沙箱执行） |
| Anthropic | Claude Opus 5.5（agentic coding 领先、比 Opus 5 便宜约 40%） | 10-18 | M4.17/M2.13 模型行更新（方向性） |
| DeepSeek | V4.1-Flash-1017（10-17）· DeepInfer 自托管推理框架（10-20，不依赖 Nvidia） | 10 月 | 模型/部署侧——能力面不触发；DeepInfer 是部署工具链 lead |
| 社区 | obra/superpowers（MIT）——方法论驱动技能框架 | 持续 | **Exemplar 级**：与本库 M0.3/M8/M1.11 多处同形 + 一个可采纳机制 |

## 2. The adjudication · 判别裁决

**融入（3 项）**：
1. **治理事实入册**（R276）：Agent Skills 标准及其名称/logo/GitHub org/域名全部捐入 AAIF——本库发射的
   `SKILL.md` 格式现在由中立基金会治理（70+ 平台、1M 技能、2.8 亿安装）；P1「格式对齐」的判断被采纳规模验证。
   落地：agentskills-standard 目录条目治理注记 + AAIF 实体入 sources + AAIF 目录条目。
2. **superpowers 的机制采纳**（R277，Exemplar 级）：其**压缩后重注入引导**（bootstrap meta-skill 在会话开始与
   压缩后重注入）是 M1.11 的具体生产实践——本库发射模板自此加一行：**任何上下文压缩后，先重读本文件与
   `.harness/pointer.json` 的 entry_docs 再继续**。其余同形佐证（TDD 删测试前代码→M0.3；四阶段系统化调试→P54
   临床鉴别思维行；双阶段子代理评审→M8.10/M3 构建者≠评判者；「mandatory workflows, not suggestions」→门禁姿态）
   记为 Exemplar 引用，不改条款。
3. **AAIF 三新标准入目录**（R278，listed）：Open Responses（M6/M8 API 互操作）、OpenEnv（M3 评测环境标准——
   D1 阶段 C 的真实运行批次的潜在环境层）、**OpenSandbox**（M3/M6 沙箱平台——A.3 #3 悬置的「具体沙箱后端」
   首个标准化候选，接入前按 M6.11 核其实际隔离机制）。

**不融入（记录）**：
- **DeepSeek V4.1-Flash / DeepInfer**：模型与部署侧——能力系统的触发器不含模型身份（M4.17 只记录不路由）；
  DeepInfer 记为部署工具链 lead（listed）。
- **Agent Teams**：P42 已全文审过（实验性、无会话恢复）——无新内容不重审。
- superpowers 的其余技能（writing-plans/executing-plans 等）：与 plan-first/M0.3/M5.13 同形，收录为 Exemplar
  引用即可，逐条开能力是 M0.5 反例。

## 3. Verification

目录 213 → **218**（superpowers/aaif/open-responses/openenv/opensandbox）；sources +aaif；agentskills-standard
治理注记；发射模板压缩后重注入行 + core/02 M1.11 范例句 + source-map 行；model-families Opus 5.5 注记；
references **§AC**（R276–R278）+ bib；`P57OrgSweepTest` 守卫；`harness cycle audit` → **53 轮 · 0 硬 · 0 缺口**。
