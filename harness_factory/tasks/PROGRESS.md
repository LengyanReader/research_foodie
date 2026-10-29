# PROGRESS · 进度日志

**Updated:** 2026-10-28

---

## 2026-10-28 · P53：实验注册表轮 —— 电池成为数据，自行探索与试验机械化

- **开轮依据。** 用户指示「应该具备自行探索和实验、测试验证的能力」。落地形态：**实验注册表成为数据**（M0.5）——`data/battery.json` 持有七任务族的预声明判据（M5.13）、声明尺度（P47）、grounding 实践、状态与结果；`battery.py`（load/validate/next_pending/mark_done/render）+ `harness battery [--next] [--json]`。任何 agent 会话可自行领取下一组实验的完整 spec、执行、回写收据、翻状态——不再需要用户指名跑哪个。
- **首次注册表驱动试验（kg-dh 族）。** 语料=本库自身（离线指针判分，M4.13）。裸奔 **0.0**：**零指针**，且 4 条轮次归属**错 3 条**（M3.19 实为 P43 非 P50、M5.13 实为 P34 非 P50、M5.14 实为 P43 非 P39——凭记忆对系统自身历史的断言，可核验且错大多数；M5.14 池新材料）。harness **1.0**：8 指针在**指针自检抓住一处不精确路径**（data/ → src/harness_factory/data/）修正后全解析，修正记录入档；归属全部内容核验；沉默小节落地。收据 = 轨迹 **#13/#14**（tool home 现 **14 条真实轨迹**）。
- **注册表现状。** **6/7 族完成**（裸奔均值 0.126 vs harness 1.0）；deep-research（多跳引用核验）为 `--next` 的活演示——待任何会话领取。
- **顺带验证。** map 守卫抓到新子命令的 HARNESS-MAP 过期——`map --write` 修复（守卫网继续起作用）。
- **登记。** `P53BatteryRegistryTest` 3 守卫；cycles **P53**（0/0/0/0）；PLAN P53 章节；BATTERY.md 注册表节；AGENTS.md 计数 410 → 413。
- **状态。** 测试 **410 → 413** 全过；`cycle audit` **49 轮 · 0 硬 · 0 缺口**；`catalog --write` + `map --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P52：能力开拓轮 —— 四个域键控能力落地（P27/P29 预命名的学科纪律）

- **开轮依据与方法。** 用户指示「全面探索还有哪些新能力可纳入」。方法：**内部覆盖矩阵**（34 域 × 39 能力键控分析——19 域无直接键控但多数被 `any` 旁路覆盖）+ **P27/P29 交付文档核查**（判别力表格**预命名**了四条学科纪律却从未落成能力）+ **前沿确认**（2026 共识关切面——scope 泄漏/沙箱/可观测——均已被既有条款承载）。
- **落地（4 条，39 → 43）。** `source-criticism`（history：史源分级/独立见证互证/断代显式/**沉默入账**）· `argument-reconstruction`（philosophy：前提-结论重构/立场声明/反例坦诚）· `concept-definition`（political-science：概念先行防 concept stretching/方法声明/**案例选择留痕**）· `safety-argumentation`（ai-safety：L0–L5/红队留痕/**拒答≠无能力**）。各只命中本域——判别力由构造保证；router +4、source-map +4；三语任务句实测入守卫（域信号词表是路由的真相源，测试句必须用域内词汇）。
- **刻意不加（逐项带理由）。** scope 泄漏（M6.11/M1 已载）· GUI/computer-use（P19 已裁、无 affordance）· 身份凭证（R271/M6.11 路径）· **个人数据/合规（8 轴无 data-sensitivity affordance——引擎演化 lead，与 D3 同型）**· arts-design（需溯源的创作方法一手材料）· D3 原样 · 谱系能力（plan-first/evidence-instruments 已覆盖）。
- **结构结论。** 8 轴向量上的 (a)-move **接近饱和**；下一批能力的正门是 (b)-move（引擎 affordance：interpretive/modality/data-sensitivity），每次付两次代价（P16.6 先例），按触发逐个开。
- **登记。** 交付 `review/capability-expansion-2026-10.md`；cycles **P52**（+4 能力）；`P52DomainCapabilityTest` 2 守卫；AGENTS.md 计数 408 → 410。
- **状态。** 测试 **408 → 410** 全过；`cycle audit` **48 轮 · 0 硬 · 0 缺口**；`capabilities --write` + `catalog --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P51：研究构思轮 —— research-question-generation（填 P18 洞）· M5.11 校准深化 · 电池升为例行

- **入口与扫荡（用户指定 After42）。** 三篇一手：R272（After42 项目页全文：solve-refine-critique、有趣占比 3%→33%、模型评审召回 65–80%/集成 80%、行为反馈有效声明偏好无效、97/100 组合式）+ R273（Stanford 2409.04109 全文：novelty 升 feasibility 平、总分与可行性相关仅 r=0.097、**LLM 自评低于人类互评且「可能是拿方差换偏差」**、多样性平台期 4000→200、执行忠实性缺口）+ R274/R275（AI Scientist 谱系 listed，批判评估 2502.14297 录为警示）。
- **新能力 `research-question-generation`（38 → 39）。** 触发 `{artifact: plan}`——**填补 P18 记录的 plan 产物空洞**（该重访触发本轮生效）。实战校验记录：域限制形式（plan×research/deep-research）会漏掉域信号指向别处的真实 plan 任务 → 取裸产物轴。五条纪律入 why：过采样-过滤带显式判据 · solve-refine-critique（失败尝试是信号，M5.14 构思版）· 新颖/可行分开打分 · 评判者校准（对专家共识的召回，行为反馈≠声明偏好）· 多样性/去重率被追踪。人类把关最终选择。classify 侧 plan 线索补 research questions/研究问题。
- **M5.11 深化（core/06）。** 校准定量证据 + 「拿方差换偏差」警示 + 多样性平台期与同质化风险。
- **例行机制（用户指示一：真实场景模拟使用升为例行）。** `tasks/BATTERY.md` 常设程序（何时/跑什么/纪律/收据流）；DoD 新增**软轴 battery**（cycle audit 可查，不追溯历史）；`capability-cycle.md` 轮次契约补电池步骤。
- **刻意不加。** 不加 novelty-assessment 独立能力（新能力组成部分）；AI Scientist 谱系不落门禁义务；ResearchAgent 无解析 id 留名不录。
- **登记。** references **§AB**（R272–R275）+ bib；source-map/router 行；交付 `review/research-ideation-2026-10.md`；cycles **P51**（+1 能力 / +4 参考）；`P51IdeationGuardTest` 3 守卫；AGENTS.md 计数 405 → 408。
- **状态。** 测试 **405 → 408** 全过；`cycle audit` **47 轮 · 0 硬 · 0 缺口**；`catalog --write` + `capabilities --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P50：行实验组轮 —— 三组新配对试验，五族已测（harness 5/5）

- **开轮依据。** 用户指示「基于可靠前沿设计使用侧实验、充分测试、提升能力」。电池设计锚定前沿评测实践：unit-tests 锚 **RHB 隐藏重算 + LHTB 重放评分**（判分者先行、条件自带测试不算分）、proof-verification 锚 **miniF2F 编译即接受**（M3.19 的机器形态）、bayesian-stats 锚 **Registered Reports / M3.11 独立重推导**。环境探测：**Lean 4 工具链可用**（elan 装 v4.35.0）+ numpy/scipy——三族全可行。
- **Trial 3（semver 解析）。** 判分者隐藏套件先行存档；**判分者自身初版有结果有效性缺陷**（元组接口假定 → dict 崩）先修再判（M3.19 活案例）。A **0.552**（16/29；漏前导零/空 build/空白/v 前缀/非 ASCII；无优先级助手）vs B **1.0**（独立写出的验收测试抓到真 bug：全数字预发布 id 属 numeric 须拒前导零；迭代至绿；无特判——RHB 作弊扫描干净）。
- **Trial 4（Lean 4）。** A **0.0**（未验证证明编译失败：rfl 不闭合 + simp 循环——M0.3 在证明族量化）vs B **1.0**（exit 0，一次编译-迭代修复，零 sorry/admit/native_decide）。
- **Trial 5（Beta-Binomial，声明的合成数据）。** A **0.2**（正态近似数值偶然接近，但无先验/无诊断/无来源/「近似可靠」无根据；置信 vs 可信混用）vs B **1.0**（判分者 scipy 独立重推导**逐位复现**区间 + 模拟互证；先验/诊断/来源齐全）。
- **五族累计。** harness **5/5 全胜**（P45/P48/P50），裸奔均值 **0.19** vs **1.0**；**12 条真实轨迹**（每对一低一高、带尺度）；trace-audit 各对正确静默。**跨族一致结论：harness 的贡献是可检验性与诊断，不是点估计准确度。**
- **诚实负面结果。** 本轮未发现发射物缺口——五族 harness 全满分，无新子句/能力证据（发射纪律：验收先行/门禁/溯源在五族都够用）。
- **登记。** 交付 `review/experiment-battery-2026-10.md`（全组设计 + 三组结果 + 五条发现；deep-research/kg-dh queued）；cycles **P50**（0/0/0/0）；`P50BatteryGuardTest` 2 守卫；AGENTS.md 计数 403 → 405。
- **状态。** 测试 **403 → 405** 全过；`cycle audit` **46 轮 · 0 硬 · 0 缺口**。按默认指示 commit，不 push。

---

## 2026-10-28 · P47+P48+P49：三组推进 —— 尺度修复 · 第二组配对试验 · ACS 深读

- **P47（P45.R1 修复）。** effect 收据可声明 `scale: [lo, hi]`；low-outcome 规则按**归一化分数**判低（`low_max_normalized: 0.4`），无尺度收据保持 legacy 原值检查（歧义写明）；scoreboard 收据同样接受可选 scale。trace.py 校验 + trace_audit.py 比较 + 规则 why + scoreboard.py 四处落地，+3 守卫。
- **P48（第二组配对试验，model-choice 族）。** decision-audit-pass-rate（结构完整性）：裸奔 **0.0** vs harness **1.0**（占位 id 显式标 unverified、档位=预算行、验收先于决策、沉默专节、归因列就绪；决策=条件性暂缓而非假装结论）。收据带 `scale: [0,1]`——**P47 修复现场验证**：trace-audit 对这对收据正确静默。轨迹 **#5/#6**（tool home 现 6 条）。配对试验文档新增 §5。
- **P49（ACS 深读，R271 v0.1.0）。** 观察项链条闭环（P20→P43→本轮）。**M6.11 深化**：ACS 把「授权在具体实参上」物化为强制架构（19 钩子 + 五处置；modify=实参重写；确定性层先行、LLM 层从属不得读策略源；ask=人类门协议化）；其 v0.1.0 自报缺口（未认证线缆、fail-open 默认）= 本库 default-fail 原则所禁反模式的一手实例。刻意不加：无 policy-enforcement 能力；预-1.0 自声明标准不落门禁义务。交付 `review/acs-deep-read-2026-10.md`；levers/source-map/frontier/R271+bib 同步。
- **登记。** cycles **P47/P48/P49**；**P45.R1 → done_in P47**；守卫 +7（P47 3 + P48 1 + P49 3，随 docs_integrity 计入）；AGENTS.md 计数 396 → 403。
- **状态。** 测试 **396 → 403** 全过；`cycle audit` **45 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P45+P46：配对试验轮 + 文档刷新轮

- **P45（用户指示「模拟或试验真实案例」）。** 双条件配对试验（同任务/同模型/同会话）：**裸奔 0.2 vs harness 1.0**（lit-review 族 effect_metric=citation-verifiability，5 项机器判据预声明后执行）。裸奔缺陷全部真实可检：记错 id（LanguageBind 当 MemGPT）、张冠李戴（Context Engineering 2.0 非方法 survey）、正文级当摘要级、无溯源、无界定——**harness 的贡献集中在可检验性**。收据入轨迹 **#3/#4**；trace-audit 产出**第一条真实轨迹驱动提案**并暴露 low-outcome 规则的**尺度盲**（1.0 满分被判低）→ **P45.R1**（effect 收据需声明尺度）。`full-update --offline` 六相链首跑全绿。诚实边界：N=1、污染声明、token=proxy、非受控实验。交付 `review/paired-trial-2026-10-28.md`。
- **P46（用户指示「更新文档、详实介绍」）。** introduction.md 补测量系统与轨迹环叙述 + 现行计数；两语 README quickstart 补测量/轨迹命令块；**zh 版缺失 full-update/brief 的跨语漂移补齐**（P30/P32 只更了英文侧）。zh 命令清单无守卫看护——扩展候选。
- **状态。** 测试 **394 → 396** 全过；`cycle audit` **41 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P44：留出集覆盖扩大轮 —— P40 点名的有意基线编辑（钉住 10 → 17，7 任务）

- **开轮依据。** 「继续加强」队列的首位可离线项：P40 发现 28/38 能力未被 must 钉住，本轮以**有意基线编辑**（M0.5）关闭。准则：**钉「缺了就算错」的，不钉「碰巧命中」的**。
- **Must 扩充（裁决记录在案）。** lit-review / kg-dh / deep-research += untrusted-content-discipline · context-budget-policy · resumable-memory · tool-use（外部来源/长程上下文/持久记忆/工具=任务族定义性纪律）；model-choice += untrusted-content-discipline · tool-use · **reproducible-experiments**（M4.17）；unit-tests **不加**（既有两条已是定义对）。逐能力 pin/skip 决策在 cycles note。
- **两个新 canonical 任务。** proof-verification（mathematics/logic/geometry-topology；must: formal-verification + verification-gate/traceable-sources/evidence-bounded-generation）· bayesian-stats（statistics/data-science；must: statistical-inference + 同三条）——allowed/must 全部来自 2026-10-28 实测 derive（M0.4），各带 P24 effect_metric，且都是**天然 machine-judge 族**（证明无 admit 接受 / R-hat/ESS + 独立重推导）——阶段 C 效果测量时这两个任务可全自动判分。
- **重测（38/38 再消融，`ablation-results-p44.json`）。** 保护集 **10 → 17**、未钉 **28 → 21**；新增承重恰好=有意钉入的 7 个——地面灵敏性第二次自证。剩余 21 个是七族下的真实边界（继续扩=钉噪声），记为声明非缺陷。
- **卫生项。** GUIDE 过期实例计数 9 → 10（两个 README 本为 10——一致）。
- **登记。** scoreboard.json note 记编辑与日期；ablation 报告新 §5；scored-task-set 表 +2 行 + note 更新；cycles **P44**（0/0/0/0）；`P44CoverageGuardTest` 2 守卫；AGENTS.md 计数 392 → 394。
- **状态。** 测试 **392 → 394** 全过；`cycle audit` **40 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P43：前沿扫荡轮 —— M5.14 失败是必需信号 · M3.19 基准双有效性 · M1.11 压缩预算 · ACS 关闭

- **开轮依据。** 用户指示「全面评估 + 继续全方位扫荡前沿动态」。六路检索（上下文/自演化/评测完整性/安全/厂商 harness/中文话语），避开 P39（评判）/P41（MCP 技能）/P42（互操作）已扫面。四篇全文 + 一份落地页，作者自 abs 页逐条核录（不猜规则）。
- **M5.14 · 失败是必需信号**（R267 Feedback Dynamics 全文，cs.SE→cs.AI 交叉）：验证门控的技能修订循环中 **success-only 0/14 选中**（42 组实验/14 设置）；失败记录带诊断（期望-观测不匹配）入池；仅 55/388 候选建立字节异同最优（改进稀疏非稳态）；验证-测试反转实测（一设置验证涨、released test 跌 6.6）。落地 core/06 子句 + checklist + 中文。**本库自证：P22 的「通过不记、miss 才记」trace 词表获得外部定量支撑；M5.13 的验收门/回滚/字节异同与 R267 独立收敛到同一程序。**
- **M3.19 · 基准双有效性**（R269 ABC 2507.02825 全文，25 作者）：task validity（当且仅当具备能力才可解——τ-bench 平凡 agent 过 38%）+ outcome validity（检查真能指示成功——错补丁过测试套件）；量化失效：SWE-Lancer 隔离失效改题库满分、SLEEP 日志检查 32.5% 高估、CVE-Bench 按清单修正 **−33% 绝对高估**、OSWorld 坏选择器 −28% 低估。落地 core/04 子句 + checklist + 中文——与 M3.18 构成「评判者四关 × 构造双有效性」闭环；**阶段 C 开测时 effect_metric 按此过检**。
- **M1.11 深化**（R268 Context Compaction Theory 全文）：压缩预算=单向通信复杂度（Thm 1）；selection 比 generation 差 **Θ(log n)**（Thm 3）；重复压缩作用于「摘要的摘要」误差累积（开放问题）→ 压缩次数是被追踪数字；Bloom filter 在案例负载近最优。落地 core/02 一句（预算按查询类定）。
- **R270/ACS**：P20 观察项到期关闭——ACS 于 2026-09-01 发布（中间件钩子 + 可移植声明式运行时控制；「inspectable, traceable and instrumentable」）；标准正文深读=后续轮候选（与 M6.11/M7 的接口可能判别）。
- **刻意不加。** 不加 context-compaction 能力（预算问题非判别）；不加 skill-evolution 能力（M5.13/M5.14/M4.8 覆盖）；多 harness 编排器（仅二手）、Harbor（待阶段 C 核其任务套件可否作 effect 运行环境）、中文社区条目（无可追踪一手实体）——全部记 lead 于扫荡文档。
- **登记。** references **§AA**（R267–R270）+ bib 4 条（作者补全）+ source-map 行（M5.14/M3.19 新增、M1.11 扩展）+ frontier 观察项关闭；交付 `review/frontier-sweep-2026-10-28.md`；cycles **P43**（0/0/**2 子句**/**4 参考**）；`P43ClauseAnchorTest` 3 守卫；AGENTS.md 计数 389 → 392。
- **状态。** 测试 **389 → 392** 全过；`cycle audit` **39 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P42：互操作拓扑轮 —— M8.11 增边界状态词表（关闭 D8）· P40 补账

- **跨会话接续。** 先了解并行会话的 P41（工具生态路由轮，18eb102）：tool-router 四步环、catalog 205→213、编号冲突诚实披露；其把 P40 的 in-flight 产物随提交携带、但 **P40 的 PROGRESS/CHANGELOG 补账留给本会话**——已补（含 PLAN 计数订正：380 非 381）。
- **开轮依据。** 队列评估发现 **D8 触发可测**：P38/P40 证明网络可达性已变，探测证实 A2A 规范 v1.0.0（a2a-protocol.org）与 Agent Teams 文档（R250）双双全文可达 → 开轮。
- **读到的。** R266（A2A 规范核心节：Agent Card 自描述清单/可选 JWS；Task 终态 vs 中断态**规范区分**；**「Results SHOULD BE via Artifacts」「Messages should not deliver outputs」**；三种投递带事件不重排 MUST；三绑定功能等价；服务端不得泄露资源存在性）· R250↑（lead/teammates 完全独立会话、共享任务列表 + **文件锁认领**、邮箱 JSON、明示实验性与成本、无会话恢复/无嵌套）· R251 佐证于仓库本体（LF topic + GOVERNANCE.md）。
- **审计裁决。** M8.11 的「产物即交接」两侧收敛确认；真实深化点=**接收方是另一 agent/进程时，状态字段必须是可分支的声明词表**（terminal ≠ needs-input；两源同形）→ 并入 M8.11（正文 + checklist），**不新增子句**。M8.10 范例集扩为 R93 + R250 + R266。
- **刻意不加。** 不加 agent-interop 能力（8 轴无 affordance，与 P39 同型）；不加错误披露子句（服务端义务、触发已记）；不给 Agent Teams 开目录条目（tool-router metabolism 回访转正状态）；R251 保持 press 级。
- **登记。** references **§Z**（R266）+ R250/R251 升级 + bib + source-map 行扩展 + 中文速览 R1–R266；交付 `review/interop-topologies-2026-10.md`；cycles **P42**（0/0/0/1 参考）；**D8 → done_in P42**；`P42ClauseAnchorTest` 3 守卫；AGENTS.md 计数 386 → 389。
- **状态。** 测试 **386 → 389** 全过；`cycle audit` **38 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。**队列剩余**：D1 阶段 C 效果级消融（需真实模型运行批次）；P41.R1（CBETA MCP 源审计，触发未生效）；P28.R1/P35.R1/D2/D3/D5（触发未生效）。按默认指示 commit，不 push。

---

## 2026-10-28 · P40：D1 阶段 C 第一片 —— 结构性消融基线（M5.12 第一次真跑）

- **开轮依据与链路。** 队列下一项 D1 阶段 C 的可执行前置。dogfood #2：`brief` → `init --from-brief` → 判据先于工作（M5.13，5 项验收预声明）→ 执行 → gate 过 → `task_outcome`（judge=machine, 5/5）→ collect → trace-audit。**第二条真实轨迹**入 tool home（现 2 条）。
- **程序。** 消融单元=能力；38 个逐一从 `data/capabilities.json` 隔离剪除（全新子进程跑 scoreboard——注册表缓存按进程隔离；try/finally 恢复；git diff 验证干净）；基线 + 逐消融分数机器可读落盘（`updates/dogfood/p40-ablation-baseline/`，未入版本控制）。
- **三个发现。** ① **承重集恰 10 个** = 5 任务 must_capabilities 并集——记分集对承重单元的检测灵敏性双向验证；掉分者受保护，改动=有意基线编辑。② **留出集覆盖缺口**：28 个非承重单元含结构性重要者（context-budget-policy / untrusted-content-discipline / sandboxed-execution 等）——不是不重要，是 must 集没钉住；扩 must=有意编辑，登记为阶段 C 后续切片候选。③ **架构自证**：全部掉分只在 capabilities 轴（modules/structure/emission 从不动）——M0.4「能力只注释、规则引擎启用」数据上成立。
- **诚实边界（预声明 A4）。** 确定性地面无方差，M5.12 配对检验不可做且不假装；效果级消融（裸跑 vs 带单元 vs 剪单元，M2.13 固定模型档位）需真实模型运行 = 阶段 C 剩余。N=1，方向性结论。
- **交付与登记。** `review/ablation-baseline-2026-10.md`；cycles P40（0/0/0/0）；D1 阶段 C roadmap 更新（slice 1 done）；`P40AblationGuardTest` 守卫。
- **跨会话注记（如实）。** 本轮收尾被打断，未及 commit；P41 会话在工作区发现 in-flight 产物并随 P41 提交携带（commit message 披露），PROGRESS/CHANGELOG 补账留给本会话——即本条目。PLAN 段计数笔误（误写 381）由本会话订正为 380。

---

## 2026-10-28 · P41：工具生态路由轮 —— 按任务族盘 MCP/技能，入表有门、后续有代谢

- **用户两段指示。** (1) 探索态度入则：参考但不局限给定范围，围绕话题继续广泛探索发现；(2) 具体到任务族：以古籍梳理为样例，先盘可用 MCP/skill/工具/拓展，入表做质量评估，后续更新优化、新陈代谢（工欲善其事必先利其器层）。**编号事故如实记录**：本轮原计划 P36，执行中发现 P36–P40 已被并行会话占用（P40 全套产物仍在工作区未提交），改记 P41；提交时一并携带 P40 的 in-flight 产物并在 commit message 中披露（其 PROGRESS/CHANGELOG 补账留给该会话或另行指示；其 PLAN 段中“测试 379→381”与实际发现的 380 不符，不代修）。
- **扫描与探测（一手，2026-10-28，探针脚本用后即删）。** 通用面：MCP 官方注册表 L 200 + `/v0/servers` JSON 200；servers/registry 仓库、anthropics/skills、agentskills、vercel-labs/skills 均 releases.atom 200；MCP 博客 RSS 实路在 `/index.xml`（rss/feed 404）；Smithery L+API 200；Glama/PulseMCP/MCP.so 可达但计数分歧（7k–99k，PulseMCP 自报 22,290+）只作方向性；安全：tool poisoning（Invariant Labs 2025-04-01）+ CSA v1，与 M6.11 一致。古籍面：CBETA/CBDB org/ctext/guji.nlc.cn/维基文库/端砚/SikuBERT 200；api.cbdb.org/bdrc/dict.sinica/jwldatalab SSL 失败、marco 502——全部如实入 unverified 线索而非事实。
- **落地面。** `reference/tool-router.md`（四步环 + 发现面表 + 古籍整理 worked example + intake 质量门 + 代谢政策）注册进 SKILL.md/skill.py/capability-router；catalog **205 → 213**（2 kinds + 8 entries）；sources +5 馈送实体（agentskills 馈送补齐）+9 outlets；watchlist +2 主题；survey `review/mcp-skills-landscape-2026-10.md`。机制接线：JSON-API 发现走 P35.R1（named consumers 已补）、P28.R1 锚点由本轮消费、新延项 P41.R1（CBETA MCP 源码审计+被拦门复探）。
- **刻意不加（M0.5）。** 无新能力/子句/域（盘的是实例层）；探测失败不入 verified。
- **登记与守卫。** cycles **P41**（0/0/0/0，catalog 8 / outlets 9）；`P41ToolRouterTest` 6 守卫；EXEMPT +mcp-blog；工作区 AGENTS.md §5 两条原则入则 + 计数 **379 → 386**（380=含 P40 未提交守卫，+6 本轮）；顺手修复 P40 遗留的守卫断 token（消融报告去 backtick）。**状态：测试 386 全过；`cycle audit` 37 轮 · 0 硬 · 0 缺口；catalog 三视图已重生成。** 按默认指示 commit，不 push。

---

## 2026-10-28 · P39：评判者鲁棒性轮 —— M3.18 评判者先受检（关闭 D7）

- **开轮依据。** D7 触发在 P38 生效（R254 全文级）。方法：主源检索 → 解析 id → 全文读三篇 + R246 升级。检索命中两个无 id 的候选（reward-hacking 综述 PCH · 研究 agent reward-hacking）按不猜 id 规则**不入 references**，只在蒸馏文档留名。
- **读到的（全文级）。** R263（自偏好偏差：GPT-4 召回差 0.520；机制是困惑度/熟悉度而非「自己生的」；关乎风格甚于对错；缓解建议未验证）· R264（RLVR 利用验证器**未强制之处**；受控训练对 ~3.5 分作弊差距——验证器设计**因果地**诱导/消除作弊；IPT 黑盒审计；注意 overwrite tests 系引用背景非其观察）· R265（13 模型 0–13.9%；RL 归因 V3 0.6% vs R1-Zero 13.9%；链长 5 陡增；hard 变体让 0% 模型也出手；加固 −87.7%；28% 无 CoT 逃轨迹监控）· R246（LHTB：隐藏验证器 + 重放评分，「声称的进度不算数」）。
- **审计与落地。** 五个评判者接触面（M0.3/M3.17/M5.11/M5.13/effect 轴）的共性缺口=「把关者自身未被审视」→ **M3.18**（偏差面声明 · 未强制面审计 · 重放评分 · 难度/模型变化重审；golden set 可信度=评判者过四关的程度）+ checklist + 反模式两条 + 中文块；scored-task-set effect 轴补 M3.18 指针。
- **刻意不加。** 不加 judge-robustness 能力（8 轴无评判角色轴）；**D1 阶段 D 重定触发**（等 M3.18 在真实 LLM 评判上跑过一轮——R263 缓解未验证，规则制 trace-audit 仍是正确姿势）；不为 LHTB 开目录条目。
- **数据卫生：D6 关账。** jspsych.org 复检 HTTP 200（2.8s），`verified:false` 翻正——库内最后一条未验证仪器条目清零。
- **登记与守卫。** cycles **P39**（0 能力 / 0 域 / **1 子句 M3.18** / **3 参考 R263–R265**）；**D7 → done_in P39**；references **§Y** + R246 升级 + bib 3 条 + source-map 行 + 中文速览编号 R1–R265；`P39ClauseAnchorTest` 4 守卫；PLAN.md P39 章节；AGENTS.md 计数 375 → 379。
- **状态。** 测试 **375 → 379** 全过；`cycle audit` **35 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。**排队剩余**：D1 阶段 C（可排，开轮即跑 M5.12 消融梯——需真实模型跑任务）；dogfood 轨迹积累（现 1 条，等真实任务）。按默认指示 commit，不 push。

---

## 2026-10-28 · P37：dogfood 轮 —— 第一个真实任务走通全链路（VeriHarness 发布池一手核验）

- **任务自选（用户授权）**：选 P38 登记的后续「发布池核验」——服务真实需要（消融/留出素材直通 D1 阶段 C）而非演练。
- **全链路首次真实数据走通**：`brief`（P32 首用，research 域/verifiability=high/grounding=required/external 工具面，交叉域 data-science 正确报出）→ `init --from-brief`（P33，落盘 updates/dogfood/p37-veriharness-pool/，gitignored）→ **判据先于工作**（M5.13：7 项检查写入项目 PLAN）→ 执行 → `gate` 过 → `harvest task_outcome`（judge=machine, score=1.0——**工厂历史上第一条真实轨迹**）→ `collect`（项目本地无轨迹，正确 no-op）→ `trace-audit` 首跑（单轨迹低于阈值，正确报无提案）。
- **核验结果（7/7）**：数据集存在/公开/与附录 E 逐项相符；**实测 23,197 rollouts**（摘要 ~26,000 的 **−10.8%**——以实测数为准）；五基准 × 双模型全对上；载荷字段齐（official_id/grader 分/轨迹/交付 tar+sha256）；许可证 `other/mixed-upstream-see-readme`；GitHub 仓库 Apache-2.0 属实。**注意事项**：HF 主站当日对本机整体不可达（对照 /papers 亦 000），经 **hf-mirror.com** 公共镜像读取（一手性折扣已记录）；APEX 平均 9.74 rollout/任务非整 10。
- **交付与登记**：`review/veriharness-pool-check-2026-10.md`（tracked 报告）；P38 survey §4 升级（池已一手查验）；cycles **P37**（0/0/0/0，**DoD 修订如实记录**：machine 收据按 P24 定义度量器规则合法，human 确认可随时追加升级）；`P37PoolCheckGuardTest` 2 守卫；AGENTS.md 计数 373 → 374。
- **后续规划（用户授权裁决，已入 roadmap）**：**D7 排队**（触发已满足；golden-set 审计，可选用已核验发布池作素材——上游许可先过）；**D1 阶段 C 可排**（开闸条件已满足：第一份 measured 收据；开轮即跑 M5.12 消融梯）；**生态扫描 → defer 为 P28.R1**（提案与判据原样保留，触发：某轮需要生态锚点或用户点名）。建议顺序：真实任务继续 dogfood → D7 → D1 阶段 C。
- **状态。** 测试 **373 → 374** 全过；`cycle audit` **34 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。按默认指示 commit，不 push。

---

## 2026-10-28 · P38：全文重读轮 —— R252–R259 全文核验，digest 台账逐项裁决（关闭 P34.R1）

- **开轮依据。** P36 探测确认 arXiv HTML 端点恢复可达（P34.R1 重访触发生效）。方法：9 篇 HTML 全文逐条抓取（每条主张带节/表定位）+ R260 机构归属块（abs 页不显示机构，HTML 才显示）。台账六项 + 一项新增，全部裁决。
- **裁决结果（3 验证 · 3 纠正 · 1 前提有误 · 1 归属为真）。** ① HERMES 6.5→31.0 属实但指标是 **composite score** 非 digest 的 pass rate；论文自身 26.2% vs 37.4% 成本数字张力记录在案。② VERA「+5% 接受 / −20% 拒绝」实为**两条判据**（≥5pp 增益＝advance bound / ≤20% 容忍回归＝tolerance bound）——digest 压缩失真，M5.13(d) 获双界范例。③ Agent Plasticity「$1,073 总成本」实为 **Opus 5.5 单模型先验学习成本 $1,072.73**（附录 C）——digest 压缩改变了主张的范围。④ **对 P34 自己的纠错**：CorpusMap 量级数字本来就在摘要里（M3.17 微缩样本：认真的单次阅读也是一次抽样）；CMM→Sakana AI **证实为真**（六作者全 Sakana）。⑤ Sharpening Tax（36/42 组合、k* 128→3、观察性研究）与 MASS（1.2–1.6× 确认但绝对分低、对照非匹配数据）正文侧数字收编并带各自告诫。
- **R254 发布池定位（一手 URL）。** HF `caiqizh/veriharness` + GitHub `google-research/veriharness`（附录 E）；技能自演化 +6.8/+3.7 held-out。定位了、未下载——检索与检验是另一个任务。
- **子句升级。** core/04 M3.17 / core/06 M5.13 的 abstract 级 hedge 全部升级（机制 §3.2/§3.3 逐字核验、Table 2 增益确认）；**无一撤回**；M5.13(d) 增 VERA 双界范例。references §X 8 条标记升级 + 组注记 + 核验状态段。
- **登记与守卫。** cycles **P38**（0/0/0/0）；**P34.R1 → done_in P38**；D7 触发生效（R254 现为 full-read 级）、保持 defer、理由升级；`P38RereadGuardTest` 3 守卫（证据级+池 URL+纠正项 · 恰好 8 条标记 · 两条子句升级）；PLAN.md P38 章节；AGENTS.md 计数 370 → 373。
- **状态。** 测试 **370 → 373** 全过；`cycle audit` **33 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成。**待用户裁决（未变）**：生态扫描提案；**P37 dogfood** 等下一个真实任务。按默认指示 commit，不 push。

---

## 2026-10-28 · P36：调优轮 —— 修两个分类缺陷 · 有意基线编辑 · dogfood 接线

- **开轮依据。** 2026-10-28 全局评估（用户确认「根据建议方向调优」）。评估事实：工厂侧机制齐装（trace→audit→提案 / full-update / brief 管道），使用侧数据为零；两个已报告分类缺陷仍未修，其一已被记分集基线固化。
- **① horizon 补 `week` 系。** `_MULTI_SESSION` += `week`（词首匹配，覆盖 weeks/weekly）· `long-term` · `数周/几周/每周`。旗舰示例 "over several weeks" 从 `session` 修正为 `multi_session`（M5 自演化 + durable 记忆启用）——README 亲自演示的第一条命令此前就在演示一个次优推导。
- **② `review` 消歧。** 裸词 `review` 移出 `_HUMAN_REVIEW`（它是「文献综述」的产物名词，非协作信号；每次文献综述都被读成人审工作流）；补复合形式 code review / peer review / reviewer / review my / review our / review comments；**`review the` 刻意不加**（"review the literature" 正是误命中）；`评审`/`复核` 等中文信号无此歧义，保留。
- **③ 有意基线编辑（第一次真实行使）。** lit-review `must_modules` **M8 → M5**：M8 是误判下游产物（裸 review → human_review → M8 启用 → 被 P23 钉进基线），修引擎后 M5 才是正解。理由记入 `scoreboard.json` note（M0.5）+ `scored-task-set` §3 新增「基线有意编辑记录」小节。`scoreboard` 5/5 total=1.0。
- **④ dogfood 接线。** **P37（dogfood 轮）在 PLAN 登记**（完成定义：一个真实任务走 brief/init → 工作 → harvest 记 `human_correction`/`task_outcome` → collect → trace-audit 出第一份 TRACE-EVOLUTION.md + 第一份 effect 收据 = D1 阶段 C 开闸条件）；工作区 AGENTS.md §5 新增**会话收尾轨迹纪律**（数据积累靠流程不靠记忆）。
- **⑤ P34.R1 重访触发生效（探测）。** 2026-10-27 时 arXiv HTML/ar5iv 七次取文失败；本日实测 `arxiv.org/abs` 可达、`arxiv.org/html/<id>` 渲染完整正文章节 + 表格。**P38（全文重读轮）登记待开**——M3.17/M5.13 的摘要级证据欠账可清。
- **守卫与登记。** `test_classify.py` +3（week→multi_session 双语 · literature review 不再 human_review · 复合形式正例守卫防过度移除）；cycles.json **P36**（0/0/0/0）；PLAN.md P36 章节 + P37/P38 登记；AGENTS.md 测试计数 367 → 370（CountDriftGuard 抓的）。
- **状态。** 测试 **367 → 370** 全过；`cycle audit` **32 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成（视图内容无变化）。**待用户裁决**：`updates/2026-10-23-ecosystem-scan-proposal.md`（生态扫描轮）仍挂起——开轮或 defer 请明示。按默认指示 commit，不 push。

---

## 2026-10-27 · P35：论文发现渠道补全轮 —— 门户梳理完备 · 接入自更新循环

- **开轮依据。** 用户要求把 Hugging Face Papers、arXiv、Google Scholar、Semantic Scholar 等论文站点梳理完备，并列入**能力更新与内容检索**的重要渠道（“之前可能提过”——即 P15.3 `review/scholarly-channels-2026-10.md` 已扫 ~95 个渠道）。但该清单缺自更新循环真正轮询的 **AI 每日发现层**（HF Papers / AlphaXiv / PWC / arXiv 分类 feed），且状态停在 2026-10-19。
- **逐门户一手实测（2026-10-27）。** 用 `python`+`urllib` 从本机实测：HF `/papers` L 200、`/api/daily_papers` **A 200 JSON**（每项含 arXiv id）、`/papers/feed` 401（无 RSS）；arXiv `export.arxiv.org/rss/cs.{AI,CL,LG,MA,SE,HC}` **六类全 200**；Semantic Scholar 产品页 200 / API **429**（无 key）；Google Scholar 200；OpenAlex works **200**（共享免费额度）；AlphaXiv 200（SPA 无 API）；OpenReview notes **403**（挑战门）；dblp **202**（Anubis 机器人门）。
- **发现真缺陷并修。** **Papers with Code 已停维**（Meta 2025-07 关闭）：实测 `paperswithcode.com`（含 `/api/v1`）**重定向至 `huggingface.co/papers/trending`**。两处 SSOT 行（目录 `harnesses.json` + `sources.json` projects）此前都声称在线——现均降级为**重定向标记**：sources 行 `feed:null` + redirect why；catalog 行 `verified:false` + 双语 defunct 注记。HF Daily Papers 接棒为其发现渠道。
- **落地（纯数据 + 参考，0 子句 0 能力）。** venues 新增 `hf-papers`（JSON API 门径，注明无 RSS）+ `arxiv-cs-ma`（cs.MA 为缺失的多智能体 feed）；`semantic-scholar`/`google-scholar` 行刷新今日门径与主题（S2 加 retrieval-grounding）；survey `scholarly-channels` 新 **§8「AI-paper discovery portals」**（门户表 +「循环如何消费」列 + 中英）；outlet-map 新节（门户→门径→循环路径→登记处）；watchlist 新 `scholarly-discovery` 主题。**立场**：除 arXiv 外全为聚合器，命中只作线索、按 §6.1 取 id 回产出方；只有 arXiv 真可被 `refresh --provider feed` 拉取，其余经 LLM 发现/人工摄入——故不新增子句（M4.5 + source-map + refresh 两路已约束），JSON-API 发现 provider 登记 **P35.R1** deferred（M0.4：不建无人消费的路径）。
- **守卫。** `test_docs_integrity.py` 增 `P35ChannelTest` **6 用例**（两 venue 存在·cs.MA feed·PWC 两面均退役·watchlist 主题·survey §8 记号·outlet-map 路由节·registry P35/P35.R1）。
- **状态。** 测试 **361 → 367**（+6）全过；`cycle audit` **31 轮 · 0 硬 · 0 缺口**；`catalog/map/capabilities --write` 重生成三视图。按默认指示 commit，不 push。

---

## 2026-10-27 · P34：周报摄取轮 —— 一致不等于验证（M3.17）· 自我编辑先过验收门（M5.13）

- **开轮依据。** 用户问 DAIR.AI「Top AI Papers of the Week」X 文章（2026-10-11，十项）能否整合，并指出该账户应纳入自动更新来源。评估通过后排定本轮：二手摘要=**仅发现用、永不引用**（P11 汇总 / P16 微信先例），经 fxtwitter API 镜像读取正文（x.com 不可达），十条 arXiv 记录逐条回一手 abs 页核验。证据级：**摘要级核实**（P12 先例）——0 篇全文可达（HTML/ar5iv 七次取文失败、S2 429），digest 正文独有数字与全部机构归属入**未验证台账**（survey §4），全文重读登记 **P34.R1**。
- **落地两子句。**
  1. **M3.17**（`core/04`，VeriHarness R254）：分歧以环境证据裁决而非多数票；共识要反查「每一次 rollout 都漏掉的需求」。把 M5.11「采样一致只是廉价路由信号」的旁注升为门禁义务，补 M3.14。
  2. **M5.13**（`core/06`，VERA R256）：自我编辑在被接纳前须归因且过门——(a) 验收标准在应用前先于开发集写明；(b) 更新须针对原因而非症状；(c) 归因哪个轴动了（借 R234 混淆接地）；(d) 预声明拒绝边界。M5.12 的接纳侧孪生；R252 警示别假定逐轮必然累积。
- **评审文档。** `review/self-modifying-harnesses-2026-10.md`（§0–§6）：十条记录的摘要级评级表、两子句判别、七条既有模块映射（含 HERMES(R255) 与目录 `hermes-agent` **重名不合**的告警）、未验证台账、许可证卫生（VERA **CC BY-NC-SA 4.0**、CorpusMap/Agent Plasticity arXiv 非独占、MIMESIS CC0）。
- **边界裁决。** MASS/MIMESIS/CMM 在权重级与模型内部一侧，不入（P15 边界）；不新增能力/域/目录条目（M0.5）。
- **data 面。** references §X **R252–R262** + bib 11 条 · source-map M3.17/M5.13 两行 + P34 注 · capabilities `why`×4（verification-gate、self-improving-loop、entity-resolution 离线双付、model-portfolio-discipline pass@1/pass@K）· sources 媒体行 `dair-ai-x`（kind=post）· watchlist 三主题关键词。**cycles.json：P33 补登记**（8c3e144 发货时漏登记，正是 M5.10 点名的「无闭环轮」）+ P34 条目 + D7（摘要级候选已识别）/D1（阶段 C 先例）理由更新 + P34.R1 deferred。
- **守卫。** `test_docs_integrity.py` 增 `P34ClauseAnchorTest` **7 用例**（两子句锚点与关键措辞、checklist 行数、反模式、source-map 行、references §X + bib keys、评审文档记号与回链、四数据面 outlet、registry P33/P34/P34.R1）。
- **状态。** 测试 **354 → 361**（+7）全过；`cycle audit` **30 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成三视图（CAPABILITIES / HARNESS-MAP / harness-index）。按默认指示 commit，不 push。

---

## 2026-10-25 · P33：环境鲁棒与简报串联 —— doctor 只读探测容错 + init --from-brief 管道

- **开轮依据。** 实测与自检发现两处断点：① 受限沙箱/只读容器中 `harness doctor` 因无条件调用 `ensure_home()` 触发 `PermissionError` 崩溃，违背纯观察原则（M0.4）；② P32 `harness brief` 生成的高质量执行草案与 `harness init` 之间无直接输入通道，确认后需重新手敲任务目标。
- **落地两项。**
  1. `doctor` 容错探测：`_cmd_doctor` 捕获 `OSError`/`PermissionError`，安全报告 `[unwritable / access denied]` 与 `$env:HARNESS_HOME` 环境变量引导，不崩溃并返回诊断退出码 1；正常环境 exit 0。
  2. `brief` 管道串联：`brief.py` 增 `load_brief`（自动解析 markdown 或 json 简报中的 Goal 与 Domain）；`assemble.py` 支持 `extra["brief_md"]` 生成 `.harness/BRIEF.md`；`cli.py` 的 `derive` 与 `init` 增加 `--from-brief` 参数，实现确认草案一键落盘脚手架。
- **守卫。** `test_cli.py` +2 用例（`doctor` 成功/无权写入容错）；`test_brief.py` +3 用例（Markdown 解析/JSON 反序列化/`init --from-brief` 端到端自检通过）。
- **状态。** 测试 **349 → 354**（+5）全过；`CountDriftGuardTest` 同步守护；`cycle audit` 0 硬 0 缺口。

---

## 2026-10-24 · P32：任务简报轮 —— `harness brief` 渲染可粘贴的执行简报

- **开轮依据。** 双能力评估的第二项结论：「指令生成缺一步成型」——R0–R5 是给 agent 的程序不是产物，缺「目标 → 可执行简报」的一步。本轮补齐。
- **落地。** ① `brief.py`：渲染规则**能算**的精炼字段（R0 重述 · R2 硬/软/假设三级约束 · R3 三档——MVP / Elevated（horizon 升一档 + grounding 升级，纯机械增量）/ Exploratory（点名 P31 的交叉域，方向由人定））+ 8 轴特征向量带理由 + 模块/能力计划 + 域工作流 + **第一阶段行动**（工作流首步 + PLAN 骨架 + 证据仪器声明 + 自检）+ 门禁 + **R4/R5 确认块**。② CLI `harness brief --task … [--domain D] [--out FILE] [--json]` + README quickstart 一行。
- **立场写死（测试钉住）。** 简报是**草案不是开工许可**：「8. Confirm」节引 requirement-refinement 的 WAIT 纪律；工厂只渲染规则能算的部分，绝不替人写任务实质（M0.4）——`test_brief_is_a_draft_not_a_licence` 断言「草案」「M0.4」字样在文。
- **守卫。** `tests/test_brief.py` **6 用例**（八节齐全 · 草案非许可 · 三档在文 · 不同任务形态计划不同（solo 无 M8 / 多 agent 有）· JSON 序列化 · 落盘）。**刻意不进记分板**：brief 复用记分板五任务已钉的同一 derive 管线（登记理由）。
- **状态。** 测试 **343 → 349**（+6）全过；`cycle audit` **28 轮 · 0 硬 · 0 缺口**；HARNESS-MAP 重生成（新子命令）。按默认指示 commit，不 push。

---

## 2026-10-24 · P31：交叉轮 —— 学科交集显式化：overlaps 声明 · 近失域报告 · 能力并集

- **开轮依据。** 用户指出「学科之间很多都是有交叉和交集的」——单域路由在交叉处的三个洞：域键控能力在交集另一半丢失、信号所有权逼出硬边界（方志误路由：史学梳理任务被数字人文的「方志」捕走）、第二名域在计划里隐形。
- **落地三层（全部证据驱动）。** ① **数据**：32 个域声明 `overlaps`（相邻域 → 一行判别要点，如 digital-humanities↔history「编码工作 vs 史学梳理」）；history 补「修纂」信号让平局成真。② **引擎**：`classify.domain_scores` 抽出共享；`derive._attach_secondary_domains`——声明过重叠的邻域得分 ≥1 且（接近 ≤1 分差 **或** 自身 ≥2 分）即进 `secondary_domains`（至多 2 个，带判别要点）；得分 ≥2 的邻域**并集**其域键控能力（用替换域重跑既有匹配器，不发明任何东西，M0.4）。③ **表面**：发射物 AGENTS.md 增「Secondary domains · 交叉域」stanza（assemble 预构建，空则空串）。
- **顺带修的两个自己埋的 bug（写测试即审己）。** 交叉评分没 lowercase——句首大写 "Bayesian" 逃过词首匹配（union 案例因此静默失败）；域计分重构把平局决胜从「注册表插入序」改成「字母序」——法语样本被路由测试当场抓住（devops 按字母胜过 research），改回稳定排序保插入序。
- **守卫。** `tests/test_overlaps.py` **7 用例**：overlap 目标必须存在 · 已知交集必须声明 · **8 样本路由电池**（评估轮的实测样本固化为回归）· 方志案例必须报出 history · 统计/数据科学并集必须加上 statistical-inference · 干净任务零交叉 · stanza 只在非空时出现。
- **状态。** 测试 **336 → 343**（+7）全过；`cycle audit` **27 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成（domains.json 变更）。按默认指示 commit，不 push。

---

## 2026-10-24 · P30：一句话轮 —— `harness full-update` 串起完整观察环

- **开轮依据。** 用户问「说一声『全面更新 harness』是否就能触发以上所有」——诚实回答：还没有（六个半环是分开的命令），缺的是编排层。本轮补齐。
- **落地。** ① `full_update.py`：六个半环按序串联（intel → probe-domains → trace-audit → evolve → cycle audit → scoreboard），**每相失败隔离**（一相报错、其余照跑，绝不伪造完成——M0.3），最后写一份双语报告 `updates/FULL-UPDATE.md`，以**人工裁决行**收尾（M0.4/M0.8）。CLI `harness full-update [--root] [--since] [--offline] [--json]`；任一相 error 则退出码 1。② **接线四处的「一句话」UX**：SKILL.md 第 8 步（agent 的 L0 六步等效程序）、capability-router 加「全面更新 harness」情境行、README quickstart 一行、工作区 AGENTS.md 常驻引用补一句、refresh.ps1 调度器改为 refresh + `full-update --offline`。③ 守卫 `tests/test_full_update.py` 2 用例。
- **实测（CLI smoke，离线 + 临时 kb）。** 六相全部 ok（probe 0 簇 · trace 0 提案 · evolve 1 提案 · cycle audit 0 硬 0 缺口 · scoreboard 1.0/5 任务），报告以人工裁决行收尾。
- **登记。** cycles.json **P30**（0 能力 / 0 域 / 0 子句 / 0 参考——它是既有机制的**组合**，M0.5）。测试 **334 → 336**（+2）全过；`cycle audit` **26 轮 · 0 硬 · 0 缺口**；HARNESS-MAP 重生成（新子命令）。按默认指示 commit，不 push。

---

## 2026-10-23 · P29：跨学科与前沿域 —— 检视 + 自动发现机制

- **开轮依据。** 用户两问：跨学科/超学科与前沿域能否整合？未提到的域能否让工厂**自动发现**？
- **切片 1 · 12 任务实测检视。** 四类裁决：**组合即覆盖**（多数跨学科任务按「工作性质」分类已覆盖——network-science/systems-science/HCI/STS/futures/neuro-symbolic/climate 不新开域，M0.5）；**信号修复**（2 处实测误路由：single-cell RNA-seq pipeline → devops（"pipeline" 误命中）、transformer circuit interpretability → devops（"circuit" 被当电气电路）——biology +3（rna-seq/single-cell/transcriptomic）、earth-environment +3（satellite/urban climate/遥感））；**落 1 个真前沿域** `ai-safety`（安全论证的 L0–L5 门禁结构判别力足：属性/威胁模型 → 能力实测 M3.10 → 红队留痕 M3.15 → 逐条论证 M4.13/M4.16 → M3.16 披露自审 → 残余风险显式；6 维 rubric；入口文档 33 → **34 学科**）；**推迟 3 个带触发**（interpretability / embodied / systems-science）。
- **切片 2 · 自动发现机制（机制性答案）。** 新模块 `domain_probe.py` + CLI `harness probe-domains`：读 `updates/intel.jsonl` → 每条 classify+derive → **落 general 的判为 unmapped** → 按共享关键词**贪婪互斥聚类**（min 2 条）→ 每簇附最近的既有域（= 最便宜的信号修复）→ 提案只写 `updates/DOMAIN-PROBES.md`（M0.4/M0.8，不碰 SSOT）。分工闭环：`refresh/intel` 拉已知主题 → `probe-domains` 找未知簇 → `evolve` 审目录健康 → 人裁决。
- **自己埋自己修的两个错（写测试即审己）。** 聚类非互斥（同批条目拆成多簇）→ 改贪婪互斥 + min_cluster；测试夹具的 brief 词（"clinical"）命中 medicine 信号 → 换无信号词——实测定位后修。
- **守卫。** `tests/test_domain_probe.py` **4 用例**（空情报静默 · unmapped 簇浮现且不带 mapped 项 · 全映射零提案 · emit 只写报告）。
- **登记。** cycles.json **P29**（0 能力 / **1 域** / 0 子句 / 0 参考）；交付 `review/interdisciplinary-frontier-domains-2026-10.md`（12 任务实测表 + 推迟触发）。
- **状态。** 测试 **330 → 334**（+4）全过；`cycle audit` **25 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成（34 域）；P18 32 族回归全过。按默认指示 commit，不 push。

---

## 2026-10-23 · P28：整合轮 —— 注册表双向核验 · 补两个真缺口 · 生态扫描提案

- **开轮依据。** 评估发现「15 个 tracked 实体在目录里无同 id 条目」。机械核验给出定论：交叉链接是**单向**的（目录 `tracked` 字段 → sources id），方向 1 **71/71 全部解析**、完全健全；方向 2（harnesses 组 33 个实体被谁引用）有 5 个零引用——裁决：3 个**豁免有据**（anthropic-building-effective-agents 是 R93 的博客源不是产品；deepseek-repos / kimi-moonshot 是公司级情报追踪器，各带重访触发），**2 个真缺口已补**。
- **两个真缺口（同名不同物的教训）。** `mistral-agents`——目录里的 smolagents 是 **Hugging Face** 的，不是 Mistral 的；Mistral 的 agents API 此前完全没条目，现已入 orchestration/sdk。`hermit-cashapp`——目录里的 'hermit' 是**牛津推理器**，Cash App 的封闭工具链（B.5 已核验）没有条目，现已入 coding/terminal-agent。目录 203 → **205**。
- **守卫。** `RegistryBidirectionalTest` 2 用例（catalog `tracked` 必须解析到任一组的实体；harnesses 组实体必须被引用或列在带理由的豁免表）——双向一致性从此进 CI。
- **网络半环 = 提案。** 生态扫描候选（AGENTS.md 标准 · ACP · LangMem · AgentOps · skills 注册表 · computer-use 栈 · D7/D8）写成 `updates/2026-10-23-ecosystem-scan-proposal.md`（observe 半环，P20 方法 + 缩水条件预登记），**待确认后开轮**。
- **状态。** 测试 **328 → 330**（+2）全过；`cycle audit` **24 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成（目录 205 条）。按默认指示 commit，不 push。

---

## 2026-10-23 · P27：广度轮 —— 基础学科 + 思想/学术流派梳理（用户指示）

- **开轮依据。** 用户指示「基础学科和重要的思想/学术流派要好好梳理」+ 评估的广度缺口清单。判据先行（M0.5）：域 = 能改变路由/门禁内容才入。
- **切片 1 · 3 个新域。** `history`（史源批判·断代显式·沉默入账）· `philosophy`（论证重构·立场声明·反例坦诚）· `political-science`（概念先行·方法声明·案例选择留痕）——各带 workflow、双语信号、README、加权 rubric；入口文档 30 → **33 学科**（CountDriftGuard 强制同步两 README 树）。
- **切片 2 · 流派表 16 行**（methodology-map 新节）。哲学 4（诠释学 Gadamer · 现象学 Husserl · 分析哲学 Frege/Wittgenstein · 实用主义 Peirce/James）+ 批判传统 2 + 社会科学 4（Popper/Kuhn · 扎根理论 Glaser & Strauss · 民族志 Malinowski/Geertz · 古典社会学 Durkheim/Weber）+ 经济/心理 4（Smith/Marshall/Keynes · Kahneman & Tversky · Watson/Miller · Freud）+ 形式科学 1（数学基础三派）+ **中文经学与考据** 1（朱熹/顾炎武/戴震：训诂先于义理）。每行三件套：书目式经典源 · 该传统内的纪律 · 谁执行；边界写死：不评流派优劣、不按派开能力。
- **切片 3 · outlets。** 8 个候选实测（2×200 核验为真；5×403 按 P12 惯例诚实登记 + note；Europeana **合并**进既有条目补 topic）。`topic_ids` 补注册 `digital-humanities`/`cognitive-science`；`OutletDataTest` 的 access 钉死日期放宽为格式校验（守卫变更，记录在案）。
- **守卫与判别纪律的产物。** 信号唯一性守卫逼出的决定：通用词（history/philosophy/历史/哲学/诠释学）留在 humanities，新域持**学科专属信号**——英文裸词「history」路由到 humanities（与 reading/humanities 分工同构），重访触发写在交付文档 §5。`P27SchoolsAndDomainsTest` 2 守卫（域+rubric 在场 · 流派锚点在文）。
- **登记。** cycles.json **P27**（0 能力 / **3 域** / 0 子句 / 0 参考 / outlets +7）；交付 `review/basic-disciplines-schools-2026-10.md`（含推迟项：astronomy/materials/neuroscience/anthropology/geography，各带重访触发）。
- **状态。** 测试 **326 → 328**（+2）全过；`cycle audit` **23 轮 · 0 硬 · 0 缺口**；`catalog --write` 重生成（33 域同步进 CAPABILITIES/HARNESS-MAP/harness-index）；P18 32 族路由回归全过。按默认指示 commit，不 push。

---

## 2026-10-23 · P26：深度补平轮 —— M6/M7/M8 落可锚定子句

- **开轮依据。** 评估发现子句分布不对称：M3/M4 有 15 条编号子句，M6/M7/M8 零或一条——`cycle audit` 对这三模块无事可做。本轮把既有散文规则**编号化**并全部锚在**已核验的既有来源**上（0 新参考）。
- **落地四条。** **M6.10**（技能=版本化可复用方法、索引先行渐进加载——agentskills.io 开放标准的契约，sources.json 已追踪、2026-10-15 已核验）· **M6.11**（暴露≠授权、「沙箱」须点名后端——R241/R242，2026-10-20 已读）· **M7.10**（每个治理性变更=可审阅可归因 diff + 回滚路径；回滚与 diff 是同一纪律的正反两向——Conventional Commits 规范（AGENTS.md §4 已链）+ R90 Temporal 的「状态日志化可重放」作机制底座）· **M8.11**（交接走**产物**不走记忆——R93 handoffs）。
- **各带** checklist 行 + source-map 行；core/07/08/09 日期刷新（07 曾停在 10-20、08 停在 10-12、09 停在 10-18）。
- **守卫。** `P26ClauseAnchorTest` 4 条内容在场守卫（每子句在自身模块点名机制 + source-map 有行）。
- **状态。** 测试 **322 → 326**（+4）全过；`cycle audit` **22 轮 · 39 子句 anchored · 0 硬 · 0 缺口**；cycles.json P26（0 能力 / 0 域 / 4 子句 / 0 参考）。按默认指示 commit，不 push。

---

## 2026-10-23 · P25（D1 阶段 B）：规则审计器 —— 把轨迹自动变成提案

- **开轮依据。** 评估结论「自动化拼图缺的那块」：P22/P24 采集的事实没有任何东西把它们转成提案。按 D1 设计文档 §3 开阶段 B，先于任何晋升（M0.4/M0.8）。
- **落地。** ① `data/trace-rules.json`：5 条规则（gate-miss-repeat → Deepen · capability-unused-repeat → Archive · re-derive-repeat → Promote · correction-focus → Deepen · **low-outcome → Deepen**——P24 effect 轴的回流：`task_outcome` 数字分 ≤2 计，等级串留给人类）。② `trace_audit.py`：validate（未知事件/变异词表/group_by 拒）→ audit（按模式分组、过阈值出提案）→ emit（只写 `updates/traces-proposals.jsonl` + `TRACE-EVOLUTION.md`，**绝不碰 data|core|domains|templates**）。③ CLI `harness trace-audit [--root] [--no-write] [--json]`（离线）。
- **自己埋自己修的两个错。** low-outcome 的 group_by 误写 detail.task（task 是顶层字段）；测试断言 updates 目录含 trace-rules.json（它在 data/）——写测试即审己（M3）。
- **守卫。** `tests/test_trace_audit.py` **7 用例**（规则合法 · 幻影名拒 · 各规则阈值触发/不足静默 · low-outcome 只计数字分 · emit 只写日志+报告）。
- **登记。** cycles.json **P25**（0 能力 / 0 域 / 0 子句 / 0 参考）；D1 `revisit_when` 更新（B 已落地；C 待用户开或第一份 measured 收据）。按默认指示 commit，不 push。

---

## 2026-10-23 · P24：效果反馈轮 —— task_outcome 事件 + 记分集 effect 轴

- **开轮依据。** 用户确认评估建议（「双向流补上结果侧采集 + 留出集补效果轴，第一步由真实任务自然完成」）。评估的两个事实支撑：双向流能回传的 6 个 trace 事件**全是过程/失败形状**，没有「任务最终做得多好」的通道；P23 留出集 5 轴全是结构轴，D1 阶段 C 即使开闸也**检验不了效果提升**。
- **落地 ①（trace 词表 6 → 7）。** `task_outcome` 成为词表唯一的结果侧事件：`detail` 必须带 `judge`（`human` 默认；`machine` 仅当该任务族有已定义度量器时合法）+ `score`（数字或等级）；缺任一被 `trace.validate` 拒绝、永不落盘——**机器记判决、不做判决**（M0.4）。发射模板 `AGENTS.md.tmpl` 的 trace 合同补记收尾事件；D1 设计文档（updates/，不入版本控制）词表同步。CLI 现成可用：`harness harvest --event task_outcome --detail '{"judge":"human","score":4,"rubric":"writing"}'`。
- **落地 ②（记分集第 6 轴）。** `data/scoreboard.json` 每任务声明 `effect_metric`（机器可判分指标，锚既有条款：citation-verifiability · answer-evidence-precision（M4.13）· decision-audit-pass-rate（M4.17）· test-suite-pass-rate）；真实测量前一律 `effect=unmeasured`（**0 分也是编造**）；测得值须带完整收据 `{status: measured, score, judge, measured_on}`，`validate_scoreboard` 拒绝残缺收据；**effect 永不进结构总分**——5 轴 1.0 结构基线原样钉死，结构与效果分开报告、分开钉死。
- **顺带修正一个真实交互。** 模板里 task_outcome 的 JSON 示例以嵌套对象结尾（`…}}`）会撞 emission 轴的占位符检查——第一次全量跑就红了（emission=0）；示例在 `detail` 后补真实字段 `session` 后回到全绿。结构守卫先于文档意图，一次自证。
- **证据分层（写进 D1 文档与记分集文档）。** L1 过程事实 / L2 结果观察（task_outcome）→ **只提案**；L3 晋升仍须阶段 C 留出集检验。留给使用侧：第一个真实任务的 `task_outcome`、第一份 effect 收据、第一次消融实跑。
- **守卫与登记。** `tests/test_trace.py` **+6**（合法组合 · 缺 judge · 缺 score · `judge=vibes` 拒 · 无效行永不落盘 · 机器判决合法）· `tests/test_scoreboard.py` **+4**（每任务有 metric · unmeasured 且不进 total · 残缺收据拒 · 完整收据受呈）；cycles.json **P24**（0 能力 / 0 域 / 0 子句 / 0 参考）；PLAN.md P24 章节；`scored-task-set-2026-10.md` 更新（第 6 轴 · 消融第二问 · 非目标改写——「结构分不是任务效果」与 effect 轴的存在理顺）；AGENTS.md 测试计数 305 → 315（CountDriftGuard 抓的，按规矩同步）。
- **状态。** 测试 **305 → 315** 全过；`cycle audit` **20 轮 · 0 硬 · 0 缺口**；结构基线 5/5 任务 total=1.0 不变；`catalog --write` 重生成（CAPABILITIES / harness-index 内容无变化，HARNESS-MAP 仅行尾）。按默认指示 commit，不 push。

---

## 2026-10-23 · P23：记分轮 —— 本库自己的最小打分任务集（关闭 P16.9）

- **开轮依据。** 用户确认；触发来自 PLAN 队列「记分轮」+ P16.9 的重访条件（「本库有打分任务集」）。它同时是 M5.12（component-ablation）在本库自跑的留出集、D1 阶段 C 的前置依赖。
- **落地。** ① `data/scoreboard.json`：5 个任务（lit-review / unit-tests / kg-dh / deep-research / model-choice），各带 allowed_domains / must_capabilities / must_modules——**全部来自 2026-10-23 一次实测 classify+derive**（model-choice 验证了 P19 的选型路由修复），不凭记忆（M0.4）。② `scoreboard.py`：5 轴确定性打分（routing / capabilities / modules / structure / emission）+ 幻影 id 校验（未知域/能力/模块即拒，M0.5）。③ CLI `harness scoreboard [--task ID] [--json]`（离线、确定性）；实测 5/5 任务 total=1.0。
- **守卫。** `tests/test_scoreboard.py` 3 用例：board 合法 · 幻影 id 被拒 · **每任务 1.0 基线钉死**（分数变动=一次有意编辑，绝不静默漂移）。
- **登记。** cycles.json **P23**（0 能力 / 0 域 / 0 子句 / 0 参考）；**P16.9 → done（done_in P23）**；交付 `review/scored-task-set-2026-10.md`（非目标写死：不是任务质量基准、不替代 rubric、不自动晋升）。
- **状态。** 测试 **302 → 305**（+3）全过；`cycle audit` **19 轮 · 0 硬 · 0 缺口**；HARNESS-MAP 重生成（新子命令 scoreboard）。按默认指示 commit，不 push。

---

## 2026-10-23 · P22（D1a）：trace schema + 采集 —— 轨迹驱动自演化的第一段落地

- **开轮依据。** 用户确认 D1 设计文档（`updates/2026-10-23-trace-driven-evolution-design.md` §7），先开零风险的阶段 A。按 M5.10 登记：**P22 = D1a**；阶段 B（规则审计→提案）、C（带测量晋升，须等记分轮）、D（LLM 辅助，D7 之后）仍 defer。
- **落地。** ① 新模块 `src/harness_factory/trace.py`：schema v1（6 事件封闭词表 `gate_miss / human_correction / re_derive / capability_unused / check_fail / context_eviction` + 必填字段 + 只追加 + 旧行读作 `signal`）+ `collect_traces`（copied/rejected，绝不静默丢弃，M0.4）。② `runtime.record_gate_miss_trace`：gate 失败即记一行（失败是事实不是意见；通过不记）。③ CLI：`gate` 失败自动落 trace（best-effort，不影响退出码）；`harvest --event/--detail` 写结构化事件（旧行为不变）；新子命令 `harness collect --project DIR`（离线、人跑）。④ 发射模板 `AGENTS.md.tmpl` 自检节增可选 trace 合同（`gate_miss`/`human_correction` 追加到 `.harness/traces.jsonl`，人跑 `collect` 拉回）。
- **守卫。** `tests/test_trace.py` **13 用例**（schema 校验、存储往返、旧行兼容、collect 拒绝与拷贝、gate 挂钩绑定 manifest 哈希）；`test_cli` 的 gate 失败测试改为 hermetic（HARNESS_HOME 指向临时目录）并顺带断言 gate_miss 落盘。修一个自己引入的 bug：`validate` 把 `v`（int）当字符串必填字段误伤。
- **状态。** 测试 **289 → 302**（+13）全过；`cycle audit` **18 轮 · 0 硬 · 0 缺口**；HARNESS-MAP 重生成（新子命令 collect）；cycles.json P22（0 能力 / 0 域 / 0 子句 / 0 参考）+ D1 `revisit_when` 更新（设计已接受，B/C 仍 defer）。按默认指示 commit，不 push。

---

## 2026-10-23 · D1 设计文档提案（`updates/`，不入版本控制）

- 按 D1 的 `revisit_when` 验收标准写了设计文档**提案**：`updates/2026-10-23-trace-driven-evolution-design.md`——点名 **trace schema**（6 事件词表 + 3 采集点，全部本地、可匿名化）· **留出集**（= 记分轮的产物；阶段 A/B 无需留出集即可动工，阶段 C 带测量的晋升须等记分轮——依赖顺序写明）· **回滚路径**（只追加 + updates 删除即撤销 + git revert + harness 哈希可重放）。
- 阶段表 A–D（schema+采集 / 规则审计→提案 / 带测量晋升 / LLM 辅助，各带完成定义）；规则审计器**不用 LLM 评判**（D7 未决），审计规则入 `data/` 可测试（M0.5）。
- D1 的触发条件名义上满足，**待用户确认后开 D1a**（阶段 A：schema + 采集，零风险）；待决问题四条写入提案 §7。

---

## 2026-10-23 · P21：dogfood 轮 —— 把 M4.15 用在入口文档上（10 处缺陷全修；5 处超出四缺陷）

- **触发。** PLAN 队列的自用轮候选两条触发齐了：同日项目评估点名入口文档可读性 + M4.15 需要最便宜的可操作性检验。按 M5.10 开轮：先定判据（四缺陷检索 + SSOT 交叉核对）再动手，交付 `review/dogfood-m415-2026-10.md`。
- **M4.15 命中的 5 处（价值最高在前）。** ① **未声明前置条件**：README 与 introduction 两份 Quickstart 在「免安装」的 `PYTHONPATH=src python -m harness_factory` 形式后直接用裸 `harness` 命令，而 L2 打包已取消、没有东西会创建 `harness`——新用户第一条命令就失败；GUIDE §3 早有 alias 行，两份入口文档却没有，已按 GUIDE 方式补上。② README 首现 `(M0.4)` 未定义 → 加注「machines observe, humans decide」。③ introduction §3 列 4+general 域而 §10 同文档说 30 域 → 改「30 disciplines / 10 faculties」。④ SKILL.md 写 Python 3.11+，与 pyproject `>=3.10`、CI 3.10/3.12、GUIDE 3.10+ 矛盾 → 改 3.10+。
- **M4.15 没抓住的 5 处：跨文档漂移（记录在案，不新增子句）。** 过期计数（GUIDE「132 tests OK」→ 去数字化指向 CHANGELOG；introduction §6「8 topics / 109 entities / 7 groups」→ 实测 9+4 / 213 / 8 并带 `as of` 日期）、漏列的组（README 来源枚举补 outlets）、**重复渲染的路线图**（introduction §10 停在 P11——M0.5 双重渲染即漂移源，压缩为指向 PLAN.md 的指针）、过期日期（Updated 2026-10-14 → 2026-10-23）。可推广修法：**声明带日期（M0.1）+ 同一状态不渲染两次（M0.5）**。**不新增 `cross-doc-consistency` 子句**：命中几乎所有文档工作、不判别；重访触发：漂移的散文声明**导致 agent 做错事**时再开。
- **登记。** `cycles.json` P21（0 能力 / 0 域 / 0 子句 / 0 参考）；PLAN.md P21 节 + 队列候选行标记关闭；CHANGELOG 记轮。
- **状态。** 测试 **289 OK**；`cycle audit` **17 轮 · 0 硬 · 0 缺口**；视图重生成（cycles.json 属 SSOT，按门禁跑 `catalog --write`）；M4.17 可操作性仍开放（文档维护不涉及模型运行，留待真正消费模型输出的轮次）。按默认指示 commit，不 push。

---

## 2026-10-23 · 卫生项收尾（评估轮后续）：计数漂移修复 · bib 欠账清零 · CRLF 归一 · 防漂移守卫

- **背景。** 项目评估（同日）点名 ASSESSMENT A.3 #6「手写计数漂移」的三个活例，按推荐顺序先做卫生清理；不另开能力轮（PLAN 卫生项约定）。全程只读 SSOT + 实测，不臆造数字（M0.4）。
- **实测事实。** `PYTHONPATH=src python -m unittest discover -s tests` → **284 通过**（与 CHANGELOG P20 一致；裸命令因缺 PYTHONPATH 直接 ImportError）；`data/domains.json` → **31 域**（30 学科 + general，10 faculties）；`references.bib` 207 条，缺 **R237–R242 + R246–R251** 共 12 条（R243–R245 已在）。
- **修复。** ① `AGENTS.md`：27 学科 → **30**（+10 faculties）；242 用例 → 实测数；测试门禁命令补 `PYTHONPATH=src`。② 两份 README 布局树按 SSOT 真实 faculty 重新分组并补全（statistics / geometry-topology / logic → formal-sciences；digital-humanities / writing / reading → humanities；data-science / model-selection → engineering；meta 不再含 reading）；参考文献范围 R1–R106 → **R1–R251**。③ `review/references.bib` 补 12 条（anthropic2025context · skarlinski2024language · anthropic2026opus55 · deepmind2026gemini4argon · openai2026sdksandbox · openai2026sdkcontext · lhtb2026 · polyworkbench2026 · agentif2026 · metr2026timehorizons · anthropic2026agentteams · linuxfoundation2026a2a）；作者名严格照 `.md` 缩写与核验状态，R247/R248 未核实的题目照原文标 *listed*。④ 两个遗留 CRLF 文件直接剥离 CR 归一为 LF（`git checkout --` 因归一化内容与索引相同而不重写；剥离后 `git ls-files --eol` 为 w/lf，且工作树 blob 哈希与索引一致）。
- **守卫（+5，漂移从此在 CI 现形）。** `tests/test_docs_integrity.py` 新增 `CountDriftGuardTest`：AGENTS.md 域数 == SSOT−1；两份 README 域数 == SSOT−1；布局树点名全部 30 个域 id（漏列即红）；AGENTS.md 用例数 == `discover().countTestCases()`（增删测试强制同步该数字）；测试门禁行必须带 `PYTHONPATH=src`。
- **状态。** 测试 **284 → 289**（+5 守卫）全过；`cycle audit` 0 硬 0 缺口；`catalog/map/capabilities --write` 无需重生成（SSOT 未动）；按默认指示 commit，不 push。

---

## 2026-10-23 · P20：全网扫描轮 —— 一条披露子句、MCP 核心修订消化、两个触发器关闭

- **Ask（用户原话）。**「请先加载本项目中的 harness 能力系统，对全网涉及 harness 的研究和实践方向进行广泛调研，分析和评估是否可以进行一次项目更新和升级。」→「可以，请开始。」两个半环分开执行：observe 半环 `review/harness-landscape-scan-2026-10.md`（已提交 `a78e75e`），用户确认后落地 apply 半环（本轮）。**编号修正**：提案时写作 P18，但 P18/P19 已被 2026-10-20 两轮占用，实际以 **P20** 登记，scan 文档已重编号并标记 applied。
- **读全 / 仅列。** 全文读三份：arXiv:2605.23950（含 Appx. A/B/E）、MCP 2026-07-28 GA 博客、OWASP AST10 README（十条风险 + 证据表）。§5 三个缩水条件经全文核验**均未触发**，四切片全量落地。其余信号只 *listed*（Agent Teams、METR 1.1、LHTB/PolyWorkBench/AgentIF、A2A/LF、context editing/memory 文档）；`platform.claude.com` 仍区域封锁，机制线只认 R237，不冒充新事实。
- **落地的子句：M3.16**（`core/04`）「比较披露其 harness」：跨模型/跨 harness 的比较必须附两侧 **ETCSOVG 七层配置卡**（执行/工具/上下文/调度/观测/验证/治理）+ 方差说明，否则只能标注「不完整、可能误导」；合法协议只有两种——**锁定 harness 换模型**，或**双因子分解方差**（η²_p 须配 ω²/bootstrap 与排名翻转数）。证据数字按方向性载：单受控 3×3 网格 HV̄/MV̄ = 7.80×（run 级 8.72×/6.76×）、6/9 排名翻转，作者自声不具普遍性。反直觉细节一并记录：跨模型方差 H2 最小、H3 最大——控制既可吸收也可暴露模型差异。**不加能力**：它按*主张类型*触发而非特征向量（methodology-fit 同规则）；与 `component-ablation`（M5.12）互为镜像（剪枝拆一个 harness 内的部件，披露点名跨 harness 的配置）。
- **数据面（P20.2/P20.3/P20.4，均 data-only）：** `levers.json` security 便签指向 AST10（技能执行层，与 R86 的 ASI01–10 **不重复**——更新漂移/扫描缺失等风险是它没有的）；`portable-skills`/`untrusted-content-discipline` 的 why 获得 AST10 溯源（R245）；`context-budget-policy` 获得 API 级参考参数（R237 委托 + R244 缓存提示）；`durable-execution` 的 why 指向 MCP Tasks 扩展；`long-horizon-autonomy-control` 记 METR 1.1 ~1.1 h/~105 天（R249，*listed，方向性*）；`harnesses.json` `mcp` 映射 M1,M6 → M1,M6,**M2,M8**（MRTR = M8 人类门的记录状态；Tasks = M2 持久执行），claude-code 条目补 Agent Teams（*listed*）；`sources.json` 两条 `why` 带日期回执。
- **评审交付物：** 新 `review/harness-disclosure-2026-10.md`（全文读记录 + 交叉表 + 核验状态）；MCP 修订落在 `review/workflow-patterns-2026-10.md` **§9**（四个映射 + 明写「不改任何不变量」）；`references.md` **§W R243–R251**（3 全读 / 6 listed）+ `.bib` 3 条；`source-map.md` M3.16 行；frontier §6b 两条线索关闭（AST10、context-editing 参数化），agent-judge 仍开放（转 D7）。
- **记录：** `cycles.json` P20（added：0 能力 / 0 域 / 1 子句 / 9 参考）；roadmap +4（P20.W1/W2 done；D7 agent-judge 鲁棒性；D8 A2A/peer-session 全文再审）。
- **状态。** 测试 279 → **284**（`P20ClauseAnchorTest` 5 个内容守卫）；`cycle audit`：**16 轮 · 38 能力 · 35 子句 anchored · 0 硬问题 · 0 缺口**；重生成 `CAPABILITIES.md` / `HARNESS-MAP.md` / `review/harness-index.md`；按默认指示 commit，**不 push**。
- **交接（下一轮可直接接手）。** ① trace-driven 自演化仍是最大结构缺口（D1，先设计文档再动代码）；② D7：出现可全文读的评价者鲁棒性一手材料时再开；③ D8：A2A 文本与 agent-teams 文档全文读后再判 M8 互操作子句；④ `references.bib` 欠账增至 R237–R242（本轮已另加 R243–R245，旧欠下次动 bib 时一并补）。

---

## 2026-10-20 · P19：模型是变量 —— 御三家读完后落 3 条子句 + 1 个能力，另记 6 项不加

- **Ask（用户原话）**：「检查，分析和评估一下最新的御三家的大模型，有哪些相关 harness 能力可以整合进来。」处理方式：不做榜单裁决，改问**哪条暴露的机制会让按本库建出的 harness 做错事**。结论是**收敛**：三家的差异在模型，收敛在 harness。
- **读到 / 读不到（写清，不用二手补洞）**：一手读到 Claude Opus 5.5 公告、Gemini 4 Argon 模型卡、OpenAI Agents SDK 两份文档。**403 / 超时 / 区域封锁**：`openai.com`、`platform.openai.com`、`help.openai.com`、`ai.google.dev`、`cloud.google.com`、`platform.claude.com/docs`、`raw.githubusercontent.com`。因此 OpenAI 在这一轮只是**文档行**（`gpt-5.6-sol` 出自其 SDK 示例），其模型名只记为「另两家对比表所点名」，不冒充产品事实。
- **五个收敛机制**：① 努力档位成为计价商品（同表对比用了 xhigh 对 high）；② 服务模型未必是请求模型（安全改路由 + 别名漂移）；③ 历史可能不可改写（preserved thinking）；④ 工作区/沙箱成为产品级契约（Manifest ≠ 活工作区 ≠ 快照；会话不保证 OS 级隔离）；⑤ 暴露≠授权（开关只决定「看得见」）。另两条已被既有条款覆盖：长上下文要实测（1M 窗口在厂商自有评测里从 99.7% 掉到 84.2%，属 M1.5/M1.10）、computer use 属沙箱执行（M6）。
- **落地的子句**：
  1. **M1.11**（`core/02`）不可改写的历史只能向前摘要：压缩有**改写**与**追加**两种形状，供应商保留推理时只能追加，摘要只写状态（决策 / 未决 / 证据指针 / 下一步），原文仍须可达；与 M4.8 台账、M1.10 退出收据同一纪律。
  2. **M2.13**（`core/03`）努力是预算行不是质量档：按阶段对着门禁花，机械环节压低，档位与模型 id 同录；**跨档位对比是设置对比**；缓存价（$0.20 读 vs $4 输入）进入同一笔账，上下文布局因此是预算决策。
  3. **M4.17**（`core/05`）服务的模型也是来源的一部分：记录请求 id、服务 id 与版本、档位、替换及理由；**模型悄悄变过的评测不是测量**；不可见的回退即使输出不错也是溯源缺陷。与 M4.16 同构：指针指到真正支撑断言的东西，模型 id 指到真正产出它的东西。
- **加深而不新增**：M6 补两条清单 + 两条反模式——**暴露即授权**（可见工具列表不是安全边界，授权落在工具内部的具体实参）、**把「沙箱」当形容词**（须点名机制、不覆盖什么、哪些路径持久）。理由：义务本来就在，缺的只是失败模式的名字。
- **能力缺口与可达性**：`model-selection` 域有 L0–L5 说明却没有任何能力触发（与 P18 的「域有文档、路由无入口」同型）。新增 **`model-portfolio-discipline`**（仅 `domain=model-selection`）：需求矩阵 → 按阶段组合 → 在**声明的档位**上跑自己的留出集 → 带 id / 版本 / 档位记录的硬门禁；同分取更便宜的层，换层或换档即重开评测。但只加能力不够——实测「在 GPT 和 Claude 之间选一个模型…」被判成 `data-science`：邻域的通用信号（`model`/`模型`/`eval`/`评测`）按计数压过了选型域的精确短语，**能力等于不可达**。修法与 P18 同一条规则：**显式线索压过领域默认**——`_SELECTION_CUES`（which model / choose a model / 选一个模型 / 哪个模型 / 选型…）命中即定向 `model-selection`；`模型对比`/`model comparison` 刻意不做线索（消融与文献综述也这么写）。router 上原本是「—」的那一行现在指向它。
- **刻意不加（M0.5，各记重访触发）**：厂商引用 API（义务已在 M4.13/M4.16）、computer-use 细节、fast mode、CCL 案例、`provider-routing` 能力（要求是记录与作废，不是选路）、1M 上下文指引（M1.5/M1.10 已覆盖，新数字只是确认）。
- **证据与守卫**：`review/references.md` 新增 **V 组 + R239–R242**（含一条核验状态：哪些读到了、哪些被挡、哪些数字只是厂商自报）；`sources/source-map.md` 三行；`P19ClauseAnchorTest` 4 个内容守卫（每条子句必须仍点名其机制 + 必须仍有溯源行）；`ModelPortfolioCapabilityTest` 2 个触发守卫（只在该域触发、不泄漏到邻域）；`DomainsClassifyTest` 2 个路由守卫（中英显式选型两例须可达、`模型对比` 反例不算选型）。
- **状态**：测试 271 → **279**；32 族路由基线仍 **32/32**；`cycle audit` 15 轮 · 38 能力 · 34 条子句 anchored · 0 hard · 0 gaps；重生成 `CAPABILITIES.md` / `HARNESS-MAP.md`；EOL 规范化；提交 `c3b061a`，已按指示 push。
- **交接（下一轮可直接接手的四件事）**：① OpenAI 模型页恢复可达时，补 §1 那行「文档行」为模型行，并按 M4.17 记录访问日期对应的快照；② `preserved thinking` 目前只有一家，若第二家也禁止编辑既有推理，把 M1.11 从「厂商约束」升为通用默认；③ `model-portfolio-discipline` 只在显式选型线索下触发，若真实使用中出现「隐性选型」（只给任务、不提模型）仍落 data-science，补的是线索而不是域信号；④ `review/references.bib` 仍停在 R1–R236（R237–R242 只在 `.md`），属既有欠账，下次动 bib 时一并补齐。

---

## 2026-10-20 · P18：路由完备性审计 —— 32 个任务族里 9 个落错域，三类根因，修后 32/32

- **Ask（用户问）。** 「double check 一下现阶段 harness_factory 的完备程度，是否对任何 task 都可以定位到适合的能力。」这不是一句表态能回答的，拆成三个可检验命题：**① 总量**（有任务掉空吗）· **② 判别**（不同任务真拿到不同能力集吗）· **③ 正确**（分类对吗）。交付物 `review/routing-coverage-2026-10.md`。
- **做法。** 32 个手写任务族（16 中 / 16 英，含「do the thing」「help me with this」两个空提示），每族给**允许域集合**，集合外即算错；八轴逐值相对安静基线翻转，看能力集是否变化；37 条能力逐条**构造性**求满足向量；router 表正则解析后与目录**双向**比对。
- **① 总量：成立。** 32/32 出计划；最少 9 条能力、中位 13；**没有一例只剩 3 条常驻底线**；37/37 能力可满足、37/37 在 router 里点名；条件取值 0 处越界。
- **② 判别：大体成立，两个真洞。** 13 个轴值不增加能力，其中 8 个是「比基线更少」的语义（one_shot/off/none/solo/medium/low），`artifact=code` 只在 `verifiability=high` 时组合承重，`artifact=mixed` 是「没具名产物」。**真洞两个**：`artifact=plan`（计划无专属要求）· `domain=arts-design`（无域能力，且 `grounding=off` 连带丢掉 `traceable-sources`，9 条为全池最低）。**不硬补**——按 M0.5 记重访触发（计划类产物「漏写自己的验收标准」时；媒体/设计交付物带第三方素材时）。
- **③ 正确：原先不成立。** 9/32 落错域，三类根因，各有可复现例：
  1. **子串误命中**：`ci` ∈ "exer**ci**ses" → 课程设计判 devops（假阳性）；`art` ∈ "p**art**ial"/"**art**icle" → 散文判 arts-design；**`eval` ∈ "retri**eval**" → 所有 RAG 任务被当成高可验证**，能力数虚高 18→15 就是这条的账。
  2. **常用任务族缺信号**：python package / type hints、线上服务/内存泄漏、incident/postmortem、course/syllabus、pcb/sensor、brand/logo、视频/音乐 —— 全部落到 `general`。
  3. **两个轴从不读文本**：`artifact`、`grounding` 只继承域默认，于是「研究报告」「注明来源」都改不了它们——而这两轴正是决定 M4 与指针类能力是否触发的。
- **修法（不改模块规则，不加能力）。** ① 信号改为**词首匹配**（`deploy` 仍匹配 deployment；`ci` 不再匹配 exercises），并把同一匹配器用于可验证性/风险/时间跨度关键词表——`retrieval` 误判由此根治，这不是补词能解决的。② 补 84 条高精度信号（6 个域）；删 3 条错键信号（`art`；devops 的 `evolution`/`governance`/`演化`——那是本库概念，不是部署工作）。③ **显式线索压过域默认**：产物名词（report/dataset/knowledge graph/codebase/proposal/报告/幻灯片/随笔…）→ `artifact`；来源要求（cite/references/provenance/注明来源/可溯源）→ `grounding=required`；只有明说「不用外部知识」才降到 `off`（静默不降级：假 off 比假 preferred 更坏）。规则写进 `reference/derivation-rules.md` §「分类器怎么填向量」。
- **修后效应（方向都对）。** 报告/写作族 10 → 14 条（拿到 M4 与指针能力）；设计/音乐族仍 9（该域本就 `grounding=off`）；RAG 综述 **18 → 15**（它从来不是高可验证）；32/32 落在允许域内。
- **守卫（6 条，数据驱动、不点名具体能力）。** 能力取值已声明（域拼错会静默失效，这是最阴的坏法）· 每条能力可满足 · router 双向覆盖（原先只有单向）· 任务族回归 · 短信号误命中回归（ci/art）· 线索压过默认。
- **顺带修的潜伏不一致。** `_cond_matches` 遇到 `when` 里同时有 `any` 与其他键时**提前返回**、忽略其余键；而 `_when_text` 渲染一直把其余键读成 AND。当前无一条目用该组合，所以行为未变——但 DSL 现在与它印出来的话一致，避免下一个人按文档写、按代码跑。
- **验证。** 271 测试通过（+8：能力 3、分类 3、域 2）；`cycle audit` **14 轮 · 37 能力 · 31 子句 · 0 硬问题 · 0 缺口**；重生成 `CAPABILITIES.md` / `HARNESS-MAP.md`（样例 A 现在真按 software-engineering/code 走）；EOL 归一。

---

## 2026-10-20 · P17.6：工作集退出（M1.10）—— 把"取用"补成"取用+退出"

- **Ask（用户插入项）。** 除了继续 P17，还要有能力**检查某些能力在当前任务里暂时不需要，就先退出加载**——「随用随取，不多占上下文窗口，不浪费 token」。
- **审计结论：半就位，缺的是退出侧。** 取用侧齐：M0.6 最小高信噪、M1.1「不改变下一步动作的 token 就删」、M1.2 渐进披露、M6.6 技能渐进加载、`capability-router` 「只加载命中行”已存在；`context-budget-policy` 管"什么进入窗口"。缺三件：**没有再检查点**（加载在 `init` 时决定一次，之后靠惯性留着）· **没有退出判据与收据**（M5.10 只管轮次级的"推迟"，不管运行期"已加载集"）· **没有机械信号**（"不浪费 token"此前只是断言，没有可校验的账）。
- **落地（四项，全部可验证）。**
  1. **新子句 M1.10「工作集是租的，不是买的」**（`core/02-context-engineering.md`）：在阶段边界（新子目标 / 换产物 / 某能力一个阶段没改动任何决策）重查；保留当且仅当 (a) 触发器仍成立或 (b) 上一阶段它定过事；其余带 `{reason, reload_when}` 退回索引；**硬不变式（always-on）不退**；能安全退出的前提是**索引仍在上下文里**（M1.2）——否则那是遗忘不是释放。同时补 checklist 与三条反模式（静默退出 / 退掉闸门 / 无索引退出）。
  2. **`.harness/working-set.json`**（`assemble.py` 新增 `_working_set()`）：`vector` + `matched` + `active` + `evicted`，`init` 时全量 active；agent 在阶段边界维护。前端 AGENTS 模板与 `SKILL.md` 输出契约同步（工作集是**任务本地**的账，与 `capabilities.local.md` 的"具体化"账分工不同）。
  3. **`harness check` 真闸门**（`check.py` 新增 `_check_working_set()`）：拒 `active ⊄ matched` · 拒 **静默丢弃**（既不在 active 也不在 evicted）· 拒同一能力既 active 又 evicted / 重复 · 拒缺 `reason` 或 `reload_when` · **拒退 always-on**（`baseline-discipline`/`verification-gate`/`bidirectional-capability-flow`，由 `when == {}` 现算，不写死名单）· 拒手改 `matched`（应与 manifest 一致，要改用 `derive`）。旧 harness 没有该文件则不报错（manifest 未声明即跳过）。
  4. **来源与入口**：`review/references.md` 新组 §T + **R237**（Anthropic "Managing context on the Claude Developer Platform"，2025-09-29，本次以**文本**读页面：context editing 在接近 token 上限时**自动清除陈旧 tool 调用与结果**并保留对话流；memory tool 落到窗口外持久化；文中 +29% / +39% / **token 减 84%** 均为**厂商自报内部评测**，已如实标注非同行评审；`docs.claude.com` 两页**地区封锁**，故不据其立论）；`sources/source-map.md` 新增 M1.10 行；router 用法第 3 条改成"行不再命中就把行放回去"。
- **为什么不加新能力（M0.5 判定，留痕）。** 候选 `working-set-eviction` 的 `when` 若写 `min_horizon: session`，则被 `context-budget-policy` 的 `any[session, tool_surface∈{read,read_write,external}]` **严格包含**（任何会触发退出的任务都已触发预算纪律）；若收窄到 `multi_session`，仍只是子集，不产生分离集——只会在 37→38 上加一条几乎总与邻居同亮的标注。按 P16 的先例（只差一个参数时**深化 M4.14**而非新增）记为**深化 `context-budget-policy`**（`why` 补一句指向 M1.10）。**重访触发**：若出现"单次调用内也需退出"的场景（同一上下文里反复换子任务、且索引无法常驻），则退出需要自己的触发器，那时再立能力。
- **验证。** 260 测试通过（新增 7 个 `WorkingSetTest`：初始全量 active / 有收据可退出 / 静默丢弃被拒 / 退 always-on 被拒 / 缺 reason+reload_when 被拒 / active 越界被拒 / 手改 matched 被拒）；`cycle audit` **0 硬问题 0 缺口**（29 条子句 anchored）；重新生成 `CAPABILITIES.md` + `HARNESS-MAP.md`；EOL 归一。
- **仍开放。** P17.3–P17.5 未动，P14.4 仍未关闭。

---

## 2026-10-20 · P17.3–P17.5：四例全文打分 · 两条判据被推翻 · 落 M3.15 + M4.16（P14.4 关闭）

- **读法。** 三篇 PDF 下载后抽正文（GraphRAG 26 页 / LongHarness 19 页 / PaperQA2 25 页），逐条按**读之前写定**的 C1/C2/C3a/C3b 打分，每格给节/表定位；N/A 与 0 分开（「没报告」≠「没做」）。Case 1 沿用 P14 的全文读，**明确标注未重读**。
- **六条预登记预测，四条被推翻，方向一致：案例比摘要好，二元判据在替它们说好话。**
  - Case 1 C3b 预测 0 → **1**：P 与 R 并列报告，闭集抽取不需要弃答分母。
  - GraphRAG C3a 预测 0 → **1**：附录 E.3/E.4 明确要求「每个要点列报告引用」+「不知道就说不知道」+「证据不支持就别写」。它是**一级**（提示里要求、无人核验、指针指向社区摘要而非原文），不是零级——这比预测更有用。
  - LongHarness C3b 预测 0 → **1**：r1（覆盖，分母含全部题）/ r2 / r3 三级漏斗，V2 = 87.8 / 87.3 / 79.7。**同时记下它自己的计分约定**：全对样本按约定算过前两级，故 r1/r2 天然偏高。
  - PaperQA2 C3b 预测 0/N/A → **1**：precision 85.2 / accuracy 66.0 / 拒答 21.9，三数同报且算术闭合（85.2 × 78.1% ≈ 66.5%）。
  - GraphRAG C2 = 0 被**确认且更强**：论文自述用 exact string matching 做实体匹配，并以「重复实体通常会被聚到同一社区」为由主张可容忍——是**声明的不作为**，不是没讨论。
- **C4 判决（判据本身是否判别）。** ① **C1 留**，但拆出「有模式」vs「公布模式」：GraphRAG 把实体类型做成提示参数、却从不印出类型表，关系无模式 → 记 0（described but missing a necessary element），比记 N/A 诚实。② **C2 改写**：身份的对象是**引用单元**，实体只是其中一种；LongHarness 做了证据记录身份（active / superseded / retracted），PaperQA2 做了来源身份（citation key → DOI），原判据对这两例只会记 N/A。③ **C3a 四例全 1 → 作 0/1 不判别**，改写成**三级阶梯**：提示要求（GraphRAG）→ 可解析到原文、按句挂键（PaperQA2、Case 1）→ **由机制强制**、且解析对**当前生效**证据集（LongHarness）。判据没问题是**位数**有问题：一句提示和一个阻断式门禁被记成同一个 1。④ **C3b 留**，并记下两种形态（两步的 precision/accuracy/拒答；三步的条件漏斗）。
- **落地两条子句（0 能力、0 域）。** **M3.15**「把损失分阶段归因」——单个端到端分数说不清该修检索还是推理；首级分母含全部样本与失败，任何抬高某级的计分约定必须写明。**M4.16**「指针是对支持关系的断言」——**悬空**（不解析）/ **过期**（解析到已被取代或撤回的条目）/ **不支撑**（解析到但原文不支持）三种缺陷各有各的检查；解析须对**生效集**，撤回只标待复核、不自动改写下游；指针必须落到**原文片段**而不是它的摘要；「准确但引错」要与「不准确」分开报。两条都**不动**既有 M4.9（机械校验引用）与 M4.13（带指针）：它们说得对，但没说指针会以三种方式失效。
- **一处真实触发缺口顺手修掉。** `evidence-bounded-generation` 原先只在 `artifact: knowledge_base` 或 KM/DH 域触发——**PaperQA2 那种「研究域 + 文档产物 + 回答语料」的形态永远不触发**，而它正是该要求最清楚的实例。加 `grounding: required`；**故意不加 `preferred`**（偏好不是契约）。`tests/test_capabilities.py` 里原先断言「grounding 不足以触发」的那条随之翻面，并写清翻面理由。
- **来源与账。** `review/references.md` 新组 §U + **R238**（PaperQA2，本次全文读；数字均出自正文）；`sources/source-map.md` 新增 M3.15 / M4.16 两行；`cycles.json` 记 **P17**（+M1.10/M3.15/M4.16、+R237/R238、0 能力、0 域、catalog 0）；**P14.4 → `done`**（移除已失效的 revisit 触发，否则渲染器仍印旧列）。
- **验证。** 263 测试通过（新增 3 条守卫：M3.15 三阶段在文中、M4.16 三失效模式在文中、横向表保持四例一行）；`cycle audit` **13 轮 · 31 条子句 anchored · 0 硬问题 · 0 缺口**；重生成 `CAPABILITIES.md` / `HARNESS-MAP.md`（能力 37 不变，grounding 轴计数 60 → 61，图注同步）；EOL 归一。

---

## 2026-10-20 · P17.1–P17.2：候选池定到一手 id · 三条判据先写成可判定问句

- **P17.1 候选池 6 → 4。** 全部一手核验（abs 页或 `id_list`），**无一条凭记忆**：Case 1（方志人物 KG，已全文读过）· **GraphRAG** `arXiv:2404.16130v2`（CC BY 4.0）· **LongHarness** `arXiv:2610.13075v1`（arXiv 非独占分发）· **PaperQA2** `arXiv:2409.13740v2`（CC BY-SA 4.0）。**PaperQA2 的 id 是这一轮新解析的**：此前只用过 `[R235]`（SHarP）里的实验对象身份，它自己的论文从未解析——按题名 `all:"PaperQA2"` 搜到 4 条，再开 abs 页核对摘要自述「PaperQA2 … optimized for improved factuality」，与 `arXiv:2411.14199`（OpenScholar，引用它）区分开。HTR 两篇（`2411.03340` · `2504.00414`）**有意不入**：属预处理体裁（转写/OCR 纠错/NER），无模式声明、无身份合并、无证据-覆盖输出契约，硬拉进来等于**替它们换考卷**；重访触发写成「若四例结果完全一致，则补一个异质体裁以区分『判据不判别』与『池子太同质』」。
- **P17.2 判据操作化（写于读正文之前）。** 三条标准 → C1 模式先于抽取 / C2 实体身份 / C3 证据有界（a）+ 覆盖报告（b），每条给**必要件**、「不算」的**反例**（如「类型清单只在附录」「同名合并一句话就算完成」「precision 97% 却不谈 recall 83% 的覆盖」）与 **N/A 规则**（没报告 ≠ 没做）。加一条**元判据 C4**：某判据在全部案例上取值相同，即不判别，退役或改写。底稿在 `updates/2026-10-20-p17-criteria.md`（不入版本控制）。
- **预登记。** 读正文前先记下只凭摘要的预测（C1 仅在「建库」类可判；C2 大面积 N/A；C3b 是最可能的判别点），并声明「若预测被推翻，改的是判据，不是案例」——这样 P17.4 的判决不能事后编故事。
- **仍开放.** P17.3（四例全文阅读与逐条打分）· P17.4（横向表 + 判别力判决）· P17.5（`cycles.json` 记 P17；P14.4 → `done` 或带新理由再 `deferred`）。**P14.4 尚未关闭。**

---

## 2026-10-20 · 地图重做 P17.0：能力架构图 · 模块边界 · 实跑样例

- **Ask（三项）。** ① 按推荐开 P17；② `HARNESS-MAP.md` **仍太粗枝大叶**，要在现有基础上加**更详实但简明**的要点解释；③ 再增一张**能力架构图**。
- **形式先定（M4.15 自用，P18 的预演）。** 三种读者任务分开：**看形状**用图（§2 Mermaid）、**查枚举**用表（§4/§5/§6/§7）、**看流水线怎么跑**用**实跑样例**（§3 两段 `classify`+`derive` 真实输出，非手写示意）。「要点」不重写，而是从 SSOT 取最短完整句（能力取 `why` 首句、域取 `summary` 首句），所以地图永远只是**索引**，正文仍在 `core/` 与 `CAPABILITIES.md`。
- **SSOT 只加一件事。** `modules.json` 增 `excludes_en` / `excludes_zh`（9×2）——「这个模块**不**负责什么」是唯一既缺失、又没在别处编码的信息（各 `core/` 文档的 Anti-patterns 有素材但没有一句话，且散落）。其余**全部现算**：轴计数 `axis_counts()`、模块计数 `module_capability_counts()`、图 `render_architecture()`、样例 `worked_example()`。守则是 P7.1 立的：**图不能手绘，否则一定腐化**。
- **图（§2）。** 六层：入口 → 分类 → 能力 → 模块 → 产物 → 演化；只有一条回边，且必须过**人工闸门**。能力层按**触发轴**分簇并给计数（`always 3 · horizon 15 · …`），图注先声明「一条能力可命中多轴，各轴之和 60 > 37，不是重复计算」——否则读者会以为数错了。
- **样例（§3）。** A（为 Python 项目补类型注解与单测）13 条能力 / 7 个模块；B（长期高代价的生产级系统 + 人工复核）21 条 / 9 个模块全开。结论句由**差集**算出：B 多出 9 条（`self-improving-loop`…`gap-seeking`），A 独有 `formal-verification`。这就是能力层的存在理由——**模块回答「用哪些规矩」，能力回答「这些规矩在这单任务上意味着什么」**。规则分类、未用 LLM，可复算。
- **表。** §4 加「不负责」列 + `<details>` 可折叠反向索引（M3 载 20 条能力，摊在单元格里会毁掉表格）；§5 每条能力加「买到了什么」；§6 每个域加 `artifact`/`grounding` 与要点；§7 每个工具类加 `maps_to`。§1 给三种读者的入口路径，§8 补「日常只用五条命令」的分组说明。
- **守卫（11 个新测试，`tests/test_harness_map.py`）。** 漂移比对；Mermaid 围栏闭合且**节点 id 唯一**；每个模块与每条轴都出现在图里；`_AXIS_ASK_*` 的键集 == `spec.FEATURE_FIELDS`（新轴不能悄悄出现）；轴计数自洽（每条能力按其轴数计一次）；未知轴**报错而非静默丢弃**；每模块边界非空、≤220 字、且不照抄 `rule_en`；样例覆盖 9 个模块且两条样例确实不同；文档里确有样例任务与命中数。
- **顺带修正。** `SKILL.md` 的 "29 disciplines" 是旧数（实为 30 + `general`）。
- **Verified.** `python -m unittest discover -s tests` → **253**（242 + 11）；`harness cycle audit` → **OK · 12 cycles · 32 roadmap · 37 capabilities · 28 clauses · 0 hard · 0 gaps**；`catalog --write` 重生成（内容未变，仅 EOL），LF 归一。
- **诚实边界.** ① Mermaid **未在本地渲染器验证**，只做语法与结构守卫（节点唯一、围栏闭合、内容来自 catalog）——GitHub 端的渲染结果本轮无法自证；② 「不负责」一句是我从各模块 Anti-patterns 提炼的**编辑判断**，每条能在对应 `core/` 文件找到依据，但不是原文引用；③ 域要点是 `summary` **截断**，不是替作者重写的提要，长域仍要看 `domains/<id>/README.md`。
- **未做（有意）。** 不给 emitted `AGENTS.md` 的模块表加边界列（`ModuleSpec` 无该字段，属引擎改动，另轮）；不给 CLI 命令手工分组（会引入手写映射，与「全部现算」相悖，改为一句分组说明）。

---

## 2026-10-20 · 表达轮 P16：先定形式再定措辞 · 翻译即表达 · 组件消融

- **Ask（三项，一轮五片，M5.10）。** ① 语言/文本修饰要**随语境自动调整**；② 同一内容与目标，要能**挑最合适的表达形式**——手册按读者谋篇、翻译求**信达雅**而非字字对应、且**不受输出类型约束**（图表/可视化/分镜/视频/音乐，只要更快更好让人懂）；③ 用户给的三个链接（`arXiv:2609.36630`、`UCSB-NLP-Chang/SHarP`、一篇微信文）里的能力与洞见，必须**回到一手源头**、认真评估再融合。
- **P16.1 三个源头的定级（关键发现）。** 两个 arXiv 都是**全文精读**（下载 PDF、抽取文本、读方法与结果）：`2609.36630`《Distilling Agentic Systems》57 页，`2610.04178`《SHarP》29 页；官方实现 README 已核。**那篇微信文其实是 SHaRP 的中文解读**——方法讲得准确，但仍**不是源**，因为它恰好漏掉三条最要紧的：**27 个模块全剪后掉到 14.44%**（24/27 时的 35.00% 才是峰值）、**PaperQA2 是反例**（全量最好、剪了就掉）、以及**全剪枝基线仍能得分该怎么读**（是**任务覆盖**问题，不是模块无用）。降级为**检索线索**；漏项记在 `review/harness-ablation-2026-10.md` §1——这是「不得洗白」规则被**演示**而非被声明。
- **P16.2 表达设计（M4.15 + `expression-design` + `review/expression-design-2026-10.md`）。** 先问三件事：**内容单元**（主张/关系/流程/数量/随时间变化）、**读者任务**（学/做/查/懂）、**每种形式的代价**。四类需求→四类文档（教程/how-to/参考/解释，R219），**一节只服务一类**；「哪里需要解释」可**检索**：首次出现的未定义术语、未声明的前置条件、缺中间步的跳跃、无例子的规则。阶梯：文字→列表→表格→图→图表→形式记法→动画→声音，只在关系需要时上爬；**优先选真源可复核者**（图由产物生成 R227、图表由代码声明 R232、故视频以**脚本**为存档物）；动画成立的条件是**时间本身即被编码的变量**（R228）。**换形式只改读者能核验的东西，不改主张**（丢「未验证」、缺单位、合并状态＝假陈述，M4.10），故非文字形式须有**文字脊**（图注：主张·数据·单位·保留条件 + 替代文本，R225）。仪器 `mermaid`（`diagramming`）、`vega-lite`（`visualization-grammar`）。参考 **§R（R219–R233）**。
- **P16.3 翻译即表达（信达雅的一手文本）。** 严复《天演论·译例言》经 Wikisource **全文取到**（R233，1898）：**「譯事三難：信、達、雅……顧信矣不達，雖譯猶不譯也」**；**「不斤斤於字比句次，而意義則不倍本文」**——许可与边界在同一句；**「一名之立，旬月踟躕」+「即義定名」**——自铸术语是**须留痕的决定**。现代证据补上可测性：130,486 段、106 部小说、16 种源语中，**流畅与忠实呈负相关**（R229），故「流畅」不能证明「忠实」；文学文本的**句级对齐是不现实的假设**（R230）；质量以 **MQM 错误类目**报告（R224），不以形容词报告。**不新增能力**：M4.10 已管跨语言保真，这里只补一手源头与可测口径。
- **P16.4 语境自适应（深化 M4.14，不新增）。** 补上缺失的**参数**：动笔前**声明受众·语域·渠道**，并**逐节复核**——未声明的受众会静默变成「谁在写就是谁」。表在 `review/language-polish-2026-10.md` §3.1。**不新增能力**：操作没变，缺的是参数，故按「深化」而非「扩张」处理（M0.5 记录）。
- **P16.5 组件消融（M5.12 + `component-ablation` + `review/harness-ablation-2026-10.md`）。** 回路只加不减，模块数于是被误读为能力。**留存 ≠ 因果贡献 ≠ 部署效用**（R234：agent 基准里模型/产物/harness 效应**混杂**，只能靠**干预**分开）。程序（R235/R236）：按实现边界切**耦合功能单元**（工具＋其说明算一个）、为每个单元写**反事实**、**一次只摘一个**、基准取**同一任务上全部消融的中位数**（不是那一次完整运行）、**性能与 token 两轴**各做单侧配对检验、α=0.05 定**保护集**、留出集上重复评估、报 **Pareto 前沿**。三条反直觉必须写进正文：**摘掉单元可能更贵**（判完成机制没了，agent 继续调用）、**PaperQA2 是反例**（冗余不是普适）、**全剪枝仍得分＝任务覆盖不足**。
- **Deferred（记 `cycles.json`，带重访触发）。** `modality` 特征轴（引擎改动要付两遍；`artifact ∈ {document,dataset}` 已与 `prose-polish` 区分）· 按体裁发模板（会被当成「架构决定」的替代品）· CLI 自动剪枝（切分本就是人工，自动化只自动了非瓶颈）· 冗余率指标（本仓库没有打分任务集，代理指标正是 Goodhart 的靶子）· `harness-pruning` 域（是程序，不是领域）。
- **Verified.** `harness cycle audit` → **OK · 12 cycles · 32 roadmap items · 37 capabilities · 28 clauses anchored · 0 hard · 0 gaps**；`python -m unittest discover -s tests` → **242**（237 + 5 guard：`ExpressionAndAblationCapabilityTest`）；`catalog --write` + `map --write` + `capabilities --write` 重生成；EOL LF。
- **仍开放（有意，M0.4）.** **P14.4**：按三条固定标准评 3–5 个已发表领域 harness——本轮读的是**两篇方法论文全文**，不是领域 harness 案例，故仍不冒充完成。
- **诚实边界.** ① 两篇 §S 论文**全文**读（PDF 抽文），但**单一模型**（Qwen3.5-122B-A10B）、**每设定 50 题**的结论只在其任务集上成立；② 经典理论书（Mayer/Sweller/Paivio/Tufte/Rosenfeld & Morville/Nida）**未读**，只在文中列名，无一条规则依赖它们；③ `atanet.org` 403、`observablehq.com` 429，两者**不登记**；④ 微信文**只作线索**，不作为引用。

---

## 2026-10-20 · 纵深轮 P15：图谱经典 · 训练边界 · 学术渠道 · 语言润色门 · 自我模型

- **Ask（五项，一轮一 `added` 块，M5.10）。** ① 收尾前轮未完成项，并系统梳理**知识图谱/本体/知识特征**的经典·前沿·管理演化模式；② 确认**模型训练方法论**的覆盖度；③ 补齐**高质量论文/发表渠道**；④ 把**语言润色（人读得下去的文体）**做成一等能力；⑤ 给 harness 一个**自我模型、缺口意识与有界探索**规则。
- **P15.1 图谱经典（`review/knowledge-graph-patterns-2026-10.md`）。** 以**分层**为主线（数据模型→模式/本体→词表对齐→约束→查询→溯源→推理），点明最常见 bug 是**层级混淆**；经典方法只认**能力问题先行**（Ontology Development 101 已取到 PDF；METHONTOLOGY/NeOn/OntoClean 为书/论文，**未重读**，只作谱系）；把「知识特征」拆成四件不同的事——嵌入（RotatE/ComplEx/ConvE）**排序**、GNN（R-GCN/CompGCN）学结构、推理机（HermiT/ELK）**判定**、OBDA（Ontop）映射；前沿（生成式构建 R149、GraphRAG R148、agentic 维护）**没有取消**两条硬约束：**身份**与**证据**。参考 **§N（R155–R170）**；新增仪器 `hermit`/`elk`（蕴含/一致性可被判**反驳**）。**不新增子句**：仪器选择已由 M3.10 管，新开 `knowledge-feature` 子句只是换名词重复它（M0.5 记录）。
- **P15.2 训练边界（`review/training-methodology-coverage-2026-10.md`）。** 逐族分级为**在轴内 / 相邻 / 不在轴内**，判据先写明；结论：**栈被梳理了，库覆盖的是「边界」而非「栈」**。卡点不是工作量，而是特征向量**无法区分「训练一个模型」与「使用一个模型」**，故 `training-*` 会是引擎静默忽略的谓词（正是 M5.10 点名的失败）→ 记为**带重访触发条件的有意不新增**（若将来加入 `model_role: consume|adapt|produce`）。参考 **§O（R171–R191）**，**摘要级核验**，不依赖任何 PDF 内数字。两行重点：**评估在轴内**（HELM/LiveBench 是对过拟合与污染的设计回应）、**谄媚是 harness 可见的缺陷**。
- **P15.3 学术渠道（`review/scholarly-channels-2026-10.md`）。** ~95 个渠道逐条记录**实测 HTTP 状态**、一手/聚合标记与**七条「不得洗白」规则**；落地 **20 个 outlet** + `outlet-map.md` 三个新节（检索与引用基础设施 · 多语种与区域学术 · 版本记录与论文集）。**无重复 id**：Semantic Scholar/Crossref/CORE/scite/Europe PMC 在 `tools`、OpenAlex 在 `projects`、AI/ML 会议索引属 `venues`——**只在正文点名，不重复登记**。Google Scholar 的 `verified: true` 于 **2026-10-20 复测确认**（真实结果页；此前的「被拦」记录已过期）。
- **P15.4 语言润色门（M4.14 + `prose-polish` + `review/language-polish-2026-10.md`）。** 先给**病灶命名**（对冲堆叠/套话/列表化/假平衡/总结的总结/语域错位/翻译腔）；门禁**非对称**：机械项只可**否决**（房规 linter、术语一致、标点按 GB/T 15834-2011、数字与标识符照录），**只有读者可放行**；可读性分数只作**漂移警报**。中文点名的病灶：**欧化句式/翻译腔 · 四字格堆砌 · 的的不休 · 全半角混用 · 繁简不等价**（按翻译处理）。仪器 `vale`/`languagetool`/`textstat`，新增 2 个 kind（`prose-linter`、`readability-metric`）。参考 **§P（R192–R200）**；ISO 标准与经典文体书（403/付费墙/503）**明确不登记**，不作证据。
- **P15.5 自我模型（M5.11 + `gap-seeking` + `review/self-model-and-gap-seeking-2026-10.md`）。** 支点是不对称：**自我报告是证词，外部检验才是证据**；三件产物=带证据的**自我模型**、两半的**缺口登记册**（`cycle audit` 机械面 + 带理由/重访触发的路线图）、每轮一次的**反证检查**。依据：无外部反馈的自我纠错会**变差**（R201）、校准差（R202）、知识边界只部分可知（R203–R205）；探索**有界**（留出集/预算/停止条件），**新颖不等于价值**（R208–R211、R216），问题选择用**信息期望价值**（R217）；前沿「自我改进」实为**搜索+可信评估器**（R212–R214）。参考 **§Q（R201–R218）**。
- **Verified.** `harness cycle audit` → **OK · 11 cycles · 22 roadmap items · 35 capabilities · 26 clauses anchored · 154→218 references · 0 hard · 0 gaps**；`python -m unittest discover -s tests` → **237**（233 + 4 guard：`ReaderAndSelfModelCapabilityTest`）；`catalog --write` + `map --write` 重生成；EOL LF。
- **仍开放（有意，M0.4）.** **P14.4**：按三条固定标准评 3–5 个已发表领域 harness——本轮做的是**经典梳理**，不是论文精读，故不冒充完成。
- **诚实边界.** ① arXiv 全部经一次 `id_list` 批量解析（id/标题/作者/日期一致），属**摘要级**；② 6 个我原以为正确的 arXiv id 实为**别的论文**（如「TransE」解析到 LHCb 物理），已用标题检索改正——**核验救了错误**；③ ISO/经典文体书/元认知经典**未读**，只列名。

---

## 2026-10-19 — 知识工程与数字人文：本体即契约 · 实体归一 · 输出侧证据约束 · 模式演化（P12 余项 + P14 全部落地）· Knowledge engineering & DH

- **Ask.** 「请剩余未做的放入后续计划，下一次再来完成」+「数字人文，以及涉及知识库/知识图谱/知识本体的开发维护管理演化 的 harness 能力，做深入检索、调研、梳理并整合」。即：**一次会话内既清 P12 余项，又完成 P14 的整轮。**
- **一手来源先过门（不是二手转述）.** Case 1 = 关书朋 · 何宇佳 · 张英聘《智能体驱动的方志人物知识图谱构建与检索增强生成问答研究》，《文献与数据学报》**8(3): 56–072, 2026-09**。**出版方开放 PDF 已下载通读**（无付费墙）：`wxysjxb.ajcass.com`；印在刊物上的 DOI `10.31193/SSAP.J.ISSN.2096-6695.2026.03.05` **在 doi.org 不可解析 → 标为「仅印刷」**。表1 四阶段提示词、表2 的 P/R/F1、表3 的三机制对照、8 类实体本体、检索权重（α=0.25 / β=0.08 / γ=0.10）**均已读到**，不再依赖公众号版（其正文可读但三张表是图片）。
- **一处自我更正（重要）.** 先前把「核验令精确率 **88.79%→97.67%**」读成「组合成本/召回同涨」；读原文后更正为：**该数字是关系抽取的精确率**，而**召回率仅 83.05%→83.42%**（实体识别的 P 92.55%→98.05%，R 88.25%→88.03%）。这正是**「门禁只买精确率，不买覆盖率」**的实证 → 落成条款 **M3.14**。同类更正两处：4.1×–39× 是 **TQ 成本增益**列（非「组合成本」）；41.1→53.3 是 **avg@5** 指标。
- **Crosswalk（P14.2）.** 案例 11 个机制逐条对照既有条款：**9 已覆盖 · 1 部分 · 2 缺口**（`review/knowledge-and-dh-crosswalk-2026-10.md`，含三条固定判据与可比对象表——**诚实标注**：只有 Case 1 通读，GraphRAG 仅读其项目 README，LongHarness/HTR 仅元数据 → **不给判词**，转 P14.4）。
- **Landed（改动分层，全部可核验）.** 数据层：4 条条款（**M3.14** · **M4.11** · **M4.12** · **M4.13**）+ 4 个能力（`ontology-as-contract` · `entity-resolution` · `evidence-bounded-generation` · `schema-evolution`）+ 域 **`digital-humanities`**（第 31 个；faculty `humanities`、artifact `dataset`、grounding `required`）+ 其加权 rubric + **13 件仪器 / 6 个新 kind** + **7 个 outlet**。文档层：`domains/digital-humanities/README.md`、`reference/capability-router.md` 4 行、`reference/evidence-instruments.md` 5 行 + 计数 50/17 → 63/23、`reference/methodology-map.md` 4 行、`sources/source-map.md` 5 行、`reference/outlet-map.md` 新节 + 3 处 ○→✔、`review/references.md` **§M（R136–R154）** + `references.bib` 同步。
- **P12 余项（全部关闭，含两处负结果）.** P12.4：用浏览器 UA 重核 22 个 `verified: false` outlet → **3 个翻真**（NOAA / APA PsycNet / CourtListener，caveat 改写为内容提示），**19 个仍被主机拦截**（403/412/429/SSL）→ 保持 `verified: false` 并留 `note`；**核查已完成，标记即诚实结果**。P12.6：周报 17 处未核数字 → **16 处在该文自有 HTML 全文逐字确认**，另一篇 `2610.20563` **无可达 HTML 全文** → 其 VLIW 周期数**保持 unverified**。P12.7：有界 8 周 Pass A → 9 帖 / 90 篇 / 68 篇映射 = **75.6% 命中率**；档案页 HTML 与 JSON **无 top-pick 标签** → 只能关键词映射，故 Pass B 暂不值其成本。
- **Deliberate non-additions（记录，非疏漏，M0.5）.** 不新增 KG 检索能力（已被 `context-budget-policy` + 检索仪器覆盖）· 不新增 `knowledge-engineering` 域（`knowledge-management` 已占，图谱细则应落**条款**而非域）· 不新增 `prosopography` 域（是 DH 的一道工序）· **不设 `encoding-standard` 仪器 kind**——TEI/CIDOC/Dublin Core/EAD3/IIIF 是**规范**不是仪器，故留作参考文献与域门禁文本（**地名表则不同**：可查询的权威表，照 `uniprot` 例入册）· CBDB 与 ISAD(G) **不引**（本环境反复 403，不可达即不引）。
- **Verified.** `harness cycle audit` → **OK · 10 cycles · 17 roadmap items · 33 capabilities · 31 domains · 24 clauses anchored · 154 references · 0 hard · 4 gaps→已由 4 个 guard 测试消除**；`python -m unittest discover -s tests` → **233 例通过**（229 + 新增 4 个能力 guard）；`catalog --write` + `map --write` 重生成（`CAPABILITIES.md` · `HARNESS-MAP.md` · `harness-index.md`）；EOL 归一。

---

## 2026-10-19 — Plan parked: the P12 remainder + a new P14 round for domain-harness case studies · 计划落库：P12 余项 + 新增 P14 轮次
- **Ask.** 「请剩余未做的放入后续计划，下一次再来完成」，并给出一篇论文链接（`mp.weixin.qq.com/s/zzsWOP6g2a9w2Q_y9d6aSQ`），要求「类似这种 harness 能力…深入调研探究和梳理，也可以制定规划，下次一并完成」——即：**这轮只排计划**，深读留到下次。
- **读到的（不是猜的）.** 该链接是中文期刊论文（关书朋 · 何宇佳 · 张英聘，《文献与数据学报》2026 年第 3 期）。公众号版**正文全文可读**（2026-10-19 抓取），但 **表1 四阶段提示词全文 / 表2 P/R/F1 评估表 / 表3 三机制对照** 与图 1–5 都渲染成**图片**，正文里没有可机读数值 → 该文自述的一切数字一律 `unverified`；卷/期/页码/DOI 亦未确认。
- **它为什么算 harness 能力.** 这是一份**真跑过的领域 harness**：人物条目识别 → 三元组抽取 → **独立于生成的「约束核验」门禁（通过 / 修正 / 拒绝）** → 实体规范化；「**原文**」是**一等实体**且 `entry_id` 贯穿「证据 → 候选三元组 → 核验 → 规范化 → 图谱节点」；问答受三条证据约束（只用给定证据 · 具名须有依据 · **证据不足须明说**）；反馈回路按环节归因并改规则（实例：「正定 / 真定」异名导致召回遗漏）。作者自述核验令关系抽取精确率 **88.79% → 97.67%**，而**召回率变化有限**（核验不额外扩展候选）——这条**仪器边界**自述少见，值得当作「门禁＝精度仪器」的实证。
- **三处落地（下次可冷启动）.**（1）`data/cycles.json`：新增 cycle **P14**（`status: planned`，`added` 留空至 Slice 3）+ roadmap **P14.1–P14.3**；并补 **P12.6**（17 处 PDF 数字/机构归属的核验）与 **P12.7**（有界 8 周回溯 Pass A）——把「剩余未做」从对话搬进**机器可渲染的计划**（`harness cycle roadmap`）。（2）`tasks/PLAN.md`：§Milestones 顶部新增 **Next session worklist · 下次工作单** 表（P12.1/2/3/4/6/7 + P14.1–3，各带「为何仍未做」），并新增 **P14 (planned)** 里程碑条目。（3）`updates/2026-10-19-domain-harness-case-study-plan.md`：首轮机制盘点 **M-1…M-11** + 首轮映射（covered / partially / **gap 候选**）+ P14.1–P14.3 的做法、入口与风险对策。
- **首轮判别力判断（待 P14.2 定案）.** 多数机制**已被既有条款覆盖**（M0.2/M0.3/M0.6 · M2.11 · M3.10 · M4 · M5.1–M5.5）；**两处可能是缺口**：①**输出侧证据约束**（现有条款偏输入侧「把检索内容当数据」，缺「每个具名断言须带证据指针，否则声明证据不足」）；②**「门禁只换精确率」的措辞**。P14.3 的候选产出**至多一二**：一条新子句 / 一条既有子句的注记 / 一个 worked example；**不新增领域**（`humanities` 已覆盖，「方志」不是能力轴），**不为 KG+RAG 新增能力**（属既有条款的组合应用）。
- **Verified.** `harness cycle audit` → **OK · 10 cycles · 16 roadmap items · 29 capabilities · 0 hard · 0 gaps**；`python -m unittest discover -s tests` → **225 例通过**；`catalog --write` + `map --write` 产出**内容无变化**（cycles.json 不进 catalog 内容），EOL 归一后工作树只剩本轮的两个**有意改动**。
- **Deliberately not done（M0.5）.** 未做深读：不取期刊 PDF、不扫同类案例、不动 `core/` 与 SSOT——本轮止于「计划 + 首轮盘点」，盘点里所有数值标 `unverified`；同类来源的筛选判据与「有意不收录」的记法写进 P14.2，避免下次退化成凑篇数。

---

## 2026-10-19 — Sourcing pass landed: roundup → group L, outlet repaired · 溯源落地：周报入 §L + outlet 修复
- **Ask.** 「按照你建议的下一步做吧」——把上一轮提案落成实际改动（涉 `data/*.json`，须 `catalog --write` + 全量测试）。
- **Landed（5 个文件）.**
  - `review/references.md`：新开 **§L**（**R127–R135**，9 条 arXiv 预印本）+ 文首取数说明 + 「§L 核验」条目——明写 **abstract-level only / no PDF opened**，把「未核者不引」写进文件本身。
  - `review/references.bib`：同步 9 条 `@misc`；顺手更正头部过期值 `R1–R79` → `R1–R135`。
  - `sources/source-map.md`：§Capability additions 增 **7 行**，全部映射到**既有** capability（`context-budget-policy` · `self-improving-loop` · `resumable-memory` · `graph-orchestration` · `traceable-sources` · `durable-execution` · `reproducible-experiments`/`eval-driven-development`）——**不新增能力、不改子句**。
  - `data/sources.json`：修**既有** `nlpnews`（url/feed → 自有域名 + `note` 记同一性判据），**不新增实体**（M0.5）。
  - `reference/outlet-map.md`：§How to use 增「规范域不可达时的取数路径」；§Deliberate non-entries 增「聚合摘要不作 outlet」——把「不新增」写成显式非收录，而不是默默略过。
- **Verified end-to-end（用仓库自己的工具，不是文本推断）.** 造一份仅含该实体的探针 `sources.json`，跑 `refresh --provider feed --verify --dry-run` → **collected=20 · accepted=20 · rejected=0**，hot topics 命中 `context-engineering / provenance-integrity / agent-harness`。即：周更机制由**既有** `refresh` 回调驱动，**不需要新代码**（上一轮 §8 的「复用而非新建」由此得到实证）。
- **Regenerated.** `catalog --write` + `map --write` 产出与 HEAD **逐字节一致**（未新增 outlet/能力，故 `CAPABILITIES.md` · `HARNESS-MAP.md` · `harness-index.md` 无实质变化）；CRLF 已归一，工作树无 EOL 噪声。
- **Result.** **225 例通过**（`python -m unittest discover -s tests`）。
- **Deliberate non-addition（记录，非疏漏）.** 落地后全量扫描仍指向被封域名的有 **5 处**（3 个人物 `x.com` 主页 + `jack-clark` 的 `importai.substack.com` url/feed）。**不修、也不加「禁止 substack feed」的守卫**：该可达性是**环境事实**而非模型性质（把环境约束编码进测试就是把环境写死），且 Import AI 的规范地址就是该 subdomain——**未查到自有域名就不臆造**。可达性仍由 `refresh --verify` 承担。详见 `updates/2026-10-19-paper-roundup-proposal.md` §6.4。
- **Still open.** §5 的 **17 处** PDF 数字/机构归属核验属**独立一轮**（成本独立）；有界回溯 Pass A（8 周清单）未启动。

---

## 2026-10-19 — Sourcing pass: can a weekly roundup be a first-party source? · 一周刊能否作一手来源
- **Ask.** 用户给出同一期 AI 周报的两条链接（自有域名 + X 文章）：(1) 评其论文**能否用作本仓库的一手来源**；(2) 评「**每周跟随**」是否可行；(3) 评「**回溯梳理**」此前一段是否必要。判据（用户选定）：**作一手来源 = 须能回到一手并经核验；二手转述一律不引**。
- **Entry points first.** 两条链接经 ID 反查确认为**同一内容**（`id=221016675`，`post_date=2026-10-18T16:39:01Z`，canonical `…/p/top-ai-papers-of-the-week-f5e`）。取数路径实测：`*.substack.com` 与 `x.com` **被拦**；出版物**自有域名**（`/feed`、`/api/v1/archive`，**分页实测可用**：`offset=23` 仍返 2026-07 条目）、`api.fxtwitter.com`、`export.arxiv.org` **可达**。周报本身是**二次索引**，按本仓库规则**不可引**，只作检索入口。
- **Verification (10/10).** 一次 `id_list` 批量核验：十条全部为 arXiv 预印本，ID/标题/作者/日期一致，**无幻影条目**；版本：LoGRA `v2`，其余 `v1`。处置：**7 采纳**、**2 背景**（#1 量子电路——方法同向但学科轴偏离；#3 推理模式切换——轴正交）、**1 有意不采用**（#9 LoGRA：训练期优化，非 harness 轴；按 M0.5 记录理由与「若日后出现训练预算类能力再评估」，**不预占位**）。
- **Correction (self-reported).** 对话里先说「12 处待核」，逐条点算后为 **17 处 = 12 数字 + 5 机构归属**——少算已更正，且在提案 §5 明写。未核前一律 `unverified`。
- **Defect found in our own data.** `groups.media` 的既有 `nlpnews` 条目 `url/feed` 指向**被拦域名** `nlpnews.substack.com`；该刊现居自有域名（同一性线索：RSS 的 owner/webMaster 为 `nlpnews@substack.com`、频道标题 "AI Newsletter"）。提议**修既有条目而非新增**（M0.5；`outlets` 组亦按「不与 `media` 重复」的既有非收录条款不新增）。
- **Q1 weekly follow — yes, reuse not build.** 落地该修复后，周报即成为 `sources.json` 追踪实体，`harness refresh --provider feed` 自动纳入候选；**两级门禁**：Tier 1 元数据机械核（一次批量请求，全部条目）→ Tier 2 深度核验（仅映射到既有 clause/capability 者，**每周上限 3 篇**）。产出**只到候选 + 提案**，且**不引入「周报可引」**。诚实边界：本环境**无定时任务**，所谓每周 = 每周一次由人/会话触发。
- **Q2 backfill — bounded, not full history.** 证据：上一期（Oct 5–11）榜首即 **"Harness Learning"**，再上一期榜首 **"Context Language Models"**；该刊另一条线 *AI Agents Weekly* 2026-08/09 标题已含 *Harness Evolution Papers*、*FrontierHarness Eval* → 近期确实同轴。方案：**有界 8 周** Pass A（`/api/v1/archive` 建清单，仅作检索底账）+ Pass B（仅核「可映射既有模式」且「跨周重复出现」者，约 80 条中 10–20 条）；**明确拒绝全史**（成本 ≫ 价值、更早条目更易被取代）。
- **Deliverable.** `updates/2026-10-19-paper-roundup-proposal.md`：9 条参考文献行（R127–R135，§L 新组）· 7 条 `source-map` 行 · 17 项 PDF 核验清单 · 2 处 outlet 改动（1 修 1 显式不新增）· LoGRA 不采用记录 · 周更机制 · 落地清单。
- **Scope discipline.** 本轮**只出提案**，未改 `data|core|domains|templates`；因未动 SSOT，**无需** `catalog --write`，测试维持 **225**。

---

## 2026-10-19 — P12 (partial): the first worklist consumed · 首张工作单被消化
- **Ask.** 「更新一轮，我看看效果」——用 P13 的机制本身跑一轮，检验「缺口面 → 工作单 → 收口」是否闭环。
- **Input (what the mechanism said).** `harness cycle audit` → 0 硬问题、**12 条软缺口**：10 条「无测试提到该能力」+ 2 条「路由表从不指向该能力」（`portable-skills`、`reproducible-experiments`）。工作单来自 P13 自己的审计，不是另起需求。
- **Slice 0（收口软缺口）.**
  - 路由：补 `reproducible-experiments`（实证分析要他人可复跑）与 `portable-skills`（能力本身要跨 harness 携带）两行——两者此前存在但**入口表不可达**。
  - 门禁：新增 `tests/test_capabilities.py::TriggerCoverageTest`（10 例），每个能力同时钉住**声明触发**与**必须不触发的安静向量**；不是「名字出现即算」，而是「该能力确实会被激活、且不会被悄悄放宽」。
  - 结果：**审计软缺口 12 → 0**。
- **Slice 3a（roadmap P12.5，M4.10 从「说到」到「做到」）.** `reference/cross-language.md` 新增 **§7 实例**：以本仓库的**常驻引用块**为母本，切 8 个意群 → 对照压缩版中文渲染 → 回译比对。它做了三件事：(1) 先把一个**看似漂移**的撤销条件（「明确说停止」vs "revoke"）通过**放宽意群**判为**无问题**——单位边界错，不是译文错；(2) 找出**两处真缺陷**：意群 4（用了能力要声明能力与文件）与意群 8（M0.4 · M0.1/M0.2 · 不可逆动作须明确同意）在压缩渲染中**全部缺失**；(3) 指出「只提案、不编造任务内容」把两个意群**熔成一句**，读起来反而**多出母本没有的主张**（"只提案" 可读成「只准提案、不准产出」）。
  - 处置：母本不动（它是权威且被逐字粘贴）；修正 `AGENTS.md` §6、`GUIDE.md`、`introduction.md`，并按意群重新拆分该融合句。
- **Slice 3a 补漏（用户把块贴回来才暴露）.** 第一遍把范围定成「guides」，**漏了两份 README**——恰恰是「快速开始」真正交给用户复制的那两份。用户贴回后即验证：三份指南已修、两份 README 仍是旧文。补齐后**五处压缩渲染**一致，并解决两个可用性缺陷：(1) 「跑 `check`」含混——`harness check --dir <产物目录>` 与产物内 `.harness/check.py` 是两个东西，现写明前者；(2) 块内未给**撤销原语**——补「直到我说「停止使用 harness_factory」撤销」，使块自足。
  - 实测（非文本推断）：`init` 12 个产物恰为 `AGENTS.md` + `tasks/*` + `.harness/*`（含 `capabilities.local.md`），`harness check --dir` 退出 0；三条路径全部存在。
- **Slice 3a 二次补漏：路径参数化（用户提出「仓库会 clone 到相关目录」）.** 把 `harness_factory/…` 写成仓库相对路径，等于**假定读者把它 clone 在了当前项目根**——clone 到别处即解析不到。八处渲染（两份 README 的快速开始 + 两份完整模板 + `AGENTS.md` §6 + `GUIDE.md` + `introduction.md` + `SKILL.md`）统一改为**参数化**：`<HF>` = 本仓库克隆后 `harness_factory/` 目录的真实路径（例 `~/src/research_foodie/harness_factory`），并给出免安装调用式 `PYTHONPATH=<HF>/src python -m harness_factory check --dir <产物目录>`。母本保留自己的措辞（「把 `./harness_factory` 换成真实路径」）并**交叉引用 `<HF>`**，两套说法归一。
  - 判定依据：这是**意群 1（读哪里）的显式化**，不是新增主张（§5）；失效方式却是机械的——未标记的相对路径在别处静默解析为不存在。
- **机制自身也被修正（自举）.** 收口 roadmap 条目时发现审计把 `done` 条目仍当「延后」要求 `revisit_when`。按语义改为：**未完成**必须给理由 + 重访条件；**已完成**只需记 `done_in`（落在哪一轮、哪一节）。同时 `harness cycle roadmap` 渲染 `done in …`。
- **Result.** `harness cycle audit` → **OK**（0 硬问题、**0 软缺口**）；**225 例通过**（+10 触发门禁、+1 roadmap 落点守卫、+5 快速开始保真门禁 = 8 处渲染 · 参数 + 意群 + 英文母本三条断言）。
- **Guard.** `TriggerCoverageTest` 覆盖上一轮审计点名的全部 10 个能力；`test_roadmap_says_where_a_done_item_landed` 守住 `done_in` 的可见性；`QuickStartFidelityTest` 按**块**（而非整文件）断言每处渲染都带路径参数、含可运行的 `check` 命令、压缩版含意群 4/5/8 且无 `./harness_factory` 未标记形式，并独立守住英文母本的三个意群——修法与教训同时被钉住。

---

## 2026-10-19 — P13: the capability round as a mechanism · 能力轮次机制化
- **Ask.** 每一轮能力拓展 / 深化 / 更新 / 演化都需要一套**机制性**的 harness 能力系统，以支撑能力集的**永续增强**；没有就建立。
- **Non-redundancy check first (M0.5).** 已有三套相邻机制：`refresh`（情报实体）、`evolve`（对实体的变异提议）、`capability-flow`（单次任务的双向流动）。缺的是**能力集自身的轮次**——谁登记、何谓完成、被有意不做的事去哪。故新增第四套，而不是改前三套。
- **Built.** `data/cycles.json`（SSOT：9 轮 `baseline`→`P13`、**七轴完成定义（带 hard/soft 标志）**、11 条 roadmap）· `cycle.py`（audit，硬/软分离）· CLI `harness cycle [list|show|audit|roadmap|dod]` · 子句 **M5.10**（`core/06`）· `reference/capability-cycle.md` · `tests/test_cycle.py`（16 例）。
- **Mechanism, not prose.** 完成定义是**数据**而非散文：`audit` 把「登记 / 判别力 / 子句锚定」当**硬问题**，「门禁 / 溯源 / 路由 / 可达」当**软缺口**；**软缺口列表就是下一轮的工作单**——这是「永续」的机制部分。
- **First audit run found real defects.** `M2.10`、`M2.11`、`M3.10`、`M8.10` 在综述/路由文档中被引用，却从未在 `core/` 锚定（`M2.11` 还被误标进 `core/09`）。本轮全部锚定并更正标签，同时补齐 `sources/source-map.md` 的 M2.10/M2.11、M3.10–M3.13、M5.10、M8.10 溯源行。
- **Result.** `harness cycle audit` → **OK**（0 硬问题）；**14 条软缺口**（缺门禁测试 / 缺路由行的既有能力）成为 P12 的具体工作单。**209 例通过。**
- **Guard.** `tests/test_cycle.py::CycleDoDTest::test_no_hard_problems` 让机制**自门禁**：幻影 id、未锚定子句、引擎无法求值的 `when` 谓词、无理由/无重访条件的延后，任一出现即 CI 失败。

## 2026-10-19 — P11.2: usage lives in the README · 用法集中到 README
- **Ask.** 「用法放在 readme 文档即可」；并明确机制：用户给**一句指令词** → 能力**常驻上下文** → 后续**随需求自动**使用相关 harness 能力 → 用户**随时可撤销**。
- **Change.** 在 `README.md` / `README.zh-CN.md` 的 **How to use this factory · 使用方式** 中补：①「一句指令词 → 常驻 → 随需自动用 → 随时说『停止使用 harness_factory』撤销」的生命周期；②**五条用法表**（情境 → 读哪份 → 用法一句话），指向 `capability-router` · `evidence-instruments` · `methodology-map` · `outlet-map` · `cross-language`。常驻粘贴块与撤销句本已在同文件「给 agent 的提示词模板」中，两处现互相呼应。
- **No new file.** 按指示不新增 `reference/usage.md`——用法归 README；`reference/` 五份仍各保留自己的 **How to use · 用法**（细节），README 给**总入口**。
- **Guard.** `test_standing_reference.py::test_readmes_carry_the_usage_map`（两份 README 必须列全五份参考文档 + 撤销句）。**193 用例通过。**

---

## 2026-10-19 — P11.1: pointer covers the whole capability reference · 指针覆盖全部可加载参考 + 链接完整性门
- **Trigger (standing check).** 「确保对该项目路径的指向可以充分使用该项目能力」——凡 agent 会跟随的**路径指向**，都必须能到达**整套**能力参考，而不是一个冻结的子集。
- **Found (defect).** `.harness/pointer.json`（`pointer.ENTRY_DOCS`）**硬编码 4 份**入口文档（SKILL.md、capability-router、requirement-refinement、capability-flow）。因此仅凭指针，生成的 harness **无法发现** `derivation-rules`、`evidence-instruments`、`methodology-map`、`cross-language`、`outlet-map`。静态清单正是 M0.5 禁止的漂移形态。
- **Fix.** `ENTRY_DOCS` 改为**由 skill 索引派生**（`overview` + `reference` 两组）→ **12** 份，与 `harness skill` 不再可能漂移；`pointer.verify` 逐一校验其存在。`how_to_use` 与生成的 `AGENTS.md` 指针段同步改为陈述「完整可加载集」。
- **Also.** 新增**文档链接完整性门**：shipped 文档中每条相对 markdown 链接都必须可解析（加门前审计为 **0** 处坏链）；`skill.py` 中 sources.json 的描述补上 `outlets` 组。
- **Guards & views.** `test_pointer.py`（+2：entry_docs ⊇ 可加载集；四份领域参考文档在列）、`test_docs_integrity.py::DocLinkIntegrityTest`（+1）。重生成 `HARNESS-MAP.md`（skill 索引描述已变）。**192 用例通过。**

---

## 2026-10-19 — P11: cross-language meaning-unit fidelity · 跨语言意群保真 + per-field information outlets · 各领域信息源地图
- **Question (two standing asks).** (1) Support **accurate multilingual communication at the level of whole meaning units (意群 / 语义内涵)** — mutual corroboration across languages, **not** word-for-word translation. (2) **Survey and organise each field's high-quality information outlets / portals / media.**
- **Method (asks 1 & 2).** For ask 1, bare primary sources confirmed this session (new group K, `[R120]`–`[R126]`): ISO 17100:2015 and ISO 5060:2024 (first-party ISO records); OASIS XLIFF 2.2 CS01 (standard page fetched); Vinay & Darbelnet 1995, Benjamins BTL 11, DOI `10.1075/btl.11` (publisher record); Halliday & Hasan 1976, DOI `10.4324/9781315836010` (publisher record); Nida & Taber 1969 (bibliographic); MQM Council (`themqm.org`, aligned with ISO 5060). For ask 2, all 68 outlet URLs were **reachability-checked** with `collect.verify_url` (HEAD/GET, 2026-10-19): **46 reachable**, **22 blocked** (403/405/transport — large sites' bot protection) and therefore recorded `verified: false` + a `note` (**listed, not confirmed this session**). No claim is smoothed over.
- **Slice 1 — the cross-language invariant (M4.10).** New clause **M4.10** in `core/05` + checklist line + anti-pattern *word-for-word fidelity* (with siblings **false friend**, **silent term substitution**, citing a translation as the primary): align by **meaning unit** (意群 / sense group / *translation unit*), **corroborate** by round-trip / target-language reader / cross-source, preserve stance·scope·modality·entity identity, **gloss — never silently substitute**. New procedure **`reference/cross-language.md`** (what a meaning unit is; the alignment procedure; mutual corroboration; term handling; bilingual deliverables = two coordinated renderings of one meaning; what this is NOT (BLEU/COMET, TM-as-authority); deliberate non-entries). Wired: `skill.py` `_TAIL`, `SKILL.md` step 6 + load-index row, router row + See also, and `domains/{linguistics,humanities,writing}` READMEs.
- **Slice 2 — the per-field outlet map.** New **`outlets` group** in `data/sources.json` (**68** curated entries: portals · journals · preprint servers · databases/registries · data repositories · media), keyed by field via **17 new `topic_ids`** (the field domain ids + `scholarly-infrastructure`), each with `outlet_kind` + `why` + `not_for` + `verified` + `access`. New **`reference/outlet-map.md`** (field sections → outlet · kind · why · NOT-for; verification statement; deliberate non-entries). Live view: **`harness sources --group outlets`** (no CLI change — the group is picked up by `iter_entities`). 18 field domains point at it from their README See-also. The AI/ML `venues`/`media` groups are **cross-referenced, not duplicated** (M0.5).
- **Deliberate non-additions (recorded).** No **`cross-language` capability** (the 8-axis feature vector has no language axis → cannot discriminate; carried by M4.10 + the procedure). No **BLEU/COMET instrument** in the catalog (a surface score is not a fidelity gate). No **`sources.json` feed** on outlets (they are reference, not intel-loop inputs). No parallel outlet registry (folded into `sources.json`). All in `review/integration-map-2026-10.md` §1e/§2.
- **Guards & views.** New `tests/test_docs_integrity.py::LoadIndexWiringTest` (every skill-index path exists; entry docs link `cross-language`) and `tests/test_sources.py::OutletDataTest` (outlet shape, `outlet_kind` vocabulary, `verified`/`access` present, **every field covered**); `test_groups_present` now includes `outlets`. Regenerated `HARNESS-MAP.md` / `CAPABILITIES.md` / `review/harness-index.md` (counts unchanged: 9 modules · 29 capabilities · 30 domains · 183 catalog · 31 rubrics · **68 outlets**). **189 tests pass.**
- **Next-cycle cues.** Re-verify the 22 `verified: false` outlets in a browser; add one bilingual EN↔ZH worked example to `cross-language.md` when an artifact is available. See `review/integration-map-2026-10.md` §3.

---

## 2026-10-18 — P10: mathematics, statistics & methodology systems (27 → 29 capabilities · 28 → 30 domains · 160 → 183 catalog entries)
- **Question (two standing asks).** (1) Integrate **statistics, Bayesian inference and basic mathematics** (algebra, geometry, topology, formal logic) as harness capability rather than prose; (2) **survey, organise and integrate each field's methodology systems**.
- **Method.** Bare primary sources fetched/confirmed this session (new groups I, `[R111]`–`[R114]` and J, `[R115]`–`[R119]`): Bayesian Workflow (`arXiv:2011.01808`); rank-normalised R-hat (`arXiv:1903.08008`); Stan (`10.18637/jss.v076.i01`); IEEE 1788-2015 interval arithmetic; PRISMA 2020 (`10.1136/bmj.n71`); GRADE, CONSORT 2010, Hevner 2004 (`MIS Quarterly` 28(1):75-105, publisher record), Glaser & Strauss 1967. All 23 new `instruments` entries were checked against their **first-party project pages** (SageMath, Singular, Macaulay2, GAP, PARI/GP, OSCAR, SymPy, CaDiCaL, mathcomp, Metamath, CGAL, GUDHI, Regina, SnapPy, polymake, R, PyMC, NumPyro, ArviZ, brms, R-INLA, emcee, DoWhy) — all `verified: true`; `jspsych` remains the single `verified: false`.
- **Slice 1 — the two domains (+ rubrics).** `statistics` (45 uniquely-named signals; wins on Bayesian/frequentist phrasing **without** stealing `data-science`, verified) and `geometry-topology` (signals are computational-geometry/topology specific — `topology`/`几何`/`代数` are already taken by `mathematics`, so compounds like `persistent homology`/`triangulation`/`流形` are used). Classifier: 2 new representative cases; **no** previously-passing case changed domain (checked case-by-case).
- **Slice 2 — the two capabilities + two clauses.** `statistical-inference` (`domain = statistics`; M3, M4) annotates **M3.11** (declare the inferential frame: priors/likelihood, R-hat/ESS, interval — not a point or p-value); `certified-computation` (`domain = geometry-topology`; M3, M6) annotates **M3.12** (exact/certified arithmetic, degeneracies handled, **independent re-derivation**). Deliberately **not** keyed on `mathematics` too: `formal-verification` already fires there, and M3.12 covers its computations as an *invariant* — so the capability keeps discriminating.
- **Slice 3 — instrument depth (data-only).** 23 rows + 4 kinds (computer-algebra-system, sat-solver, geometry-topology-toolkit, causal-inference-toolkit); catalog **160 → 183**, kinds **46 → 50**. Wired into `reference/evidence-instruments.md` (new §Certified computation, §Statistical estimates & causal claims, §Methodology + 3 new map rows + revised non-entries), the two domain READMEs, and `assemble._INSTRUMENTS` (two new emitted stanza lines).
- **Slice 4 — the methodology layer.** New `reference/methodology-map.md`: **field → methodology system → canonical source → what it demands → which module/capability/gate enforces it** (18 systems across statistics, causal inference, medicine/GRADE, design science, DoE, qualitative traditions, formal sciences, measurement, humanities, law, writing, frontier evals), plus the three-part contract (protocol · assumptions · reporting standard) and deliberate non-additions. New clause **M3.13** + checklist + anti-pattern *method-by-vibes*; router row; `SKILL.md` step 6 + load-index rows.
- **Deliberate non-additions (recorded).** No `methodology-fit` capability (would fire on almost every task → non-discriminating; carried by M3.13 + the map instead); no `standard`-kind entries for PRISMA/GRADE/CONSORT/IEEE 1788 (norms, not instruments); no `geometry-topology` tool series duplicated under `mathematics`; no `statistics` faculty (it sits in `formal-sciences` with `logic`). All in `review/integration-map-2026-10.md` §2.
- **Slice 5 — the roadmap.** New `review/integration-map-2026-10.md`: status board (done / **next** / later / out) with, for **every** candidate, *what would make it discriminating*; strongest next candidate = **qualitative rigour** (codebook + double-coding + saturation), blocked on the feature vector not distinguishing qualitative from quantitative work; plus spectra/crystallography, probabilistic-parsing and multiverse-gate cues deferred to P11.
- **Docs + provenance.** `review/references.md` §I–§J + `references.bib` groups I/J + `sources/source-map.md` rows (capabilities + domain assemblies + P10 pass note); `core/04` M3.11–M3.13; `reference/capability-router.md` (3 rows + See-also); `reference/derivation-rules.md` (2 rows); `domains/mathematics`/`logic` READMEs deepened (algebra/CAS, SAT/automated reasoning) and both bumped to 2026-10-18; counts refreshed in `GUIDE.md`, `introduction.md`, `tasks/PLAN.md`, `CHANGELOG.md`, workspace `AGENTS.md`.
- **Verified.** `PYTHONPATH=src python -m harness_factory catalog --write` → `review/harness-index.md` (183) + `CAPABILITIES.md` (**29 capabilities**) + `HARNESS-MAP.md` (**9 modules · 29 capabilities · 30 domains · 183 catalog · 31 rubrics · 23 CLI · 11 templates · 12 classes × 50 kinds**); **184** tests OK (181 + 3); every touched file normalised to LF (no doubled CRs).

---

## 2026-10-18 — P9: evidence instruments — catalog · map · emitted default (133 → 160 catalog entries)
- **Question.** P7.3 made *"match the instrument to the claim"* (M3.10) a rule with **no instruments**: the three discipline capabilities named a kind of evidence and stopped there, and the emitted harness never stated what would settle its own claim.
- **Method.** Bare primary sources fetched/confirmed this session (new group H, `[R107]`–`[R110]`): JCGM 100:2008 **GUM** (+ **Amendment 1: 2026**, nonlinearity in measurement models — `as of 2026-10`); **NASA-STD-7009B** *Standard for Models and Simulations* (read in full: scope text, version B, public-access statement); BIPM **SI brochure** (landing page); COS **Registered Reports**. The 27 tool entries were checked against first-party project pages; **`jspsych` is the one entry recorded `verified: false`** (its landing page answered with a client-side redirect stub) — stated rather than smoothed over.
- **Slice 1 — instrument catalog (data-only).** New class **`instruments`** in `data/harnesses.json`: 13 kinds (proof-assistant, proof-library, smt-solver, model-checker, units-uncertainty, chem-bio-toolkit, bio-database, corpus-resource, annotation-platform, experiment-runtime, prereg-archive, stats-toolkit, workflow-engine) and **27 entries** — `lean4`, `mathlib`, `rocq`, `isabelle`, `agda`, `dafny`, `z3`, `cvc5`, `tla-plus`, `alloy`, `pint`, `uncertainties`, `rdkit`, `biopython`, `rcsb-pdb`, `uniprot`, `universal-dependencies`, `inception`, `elan`, `psychopy`, `jspsych`, `osf`, `statsmodels`, `lme4`, `stan`, `snakemake`, `nextflow`. Catalog **133 → 160** (12 classes × 46 kinds); `validate()` clean, index + `HARNESS-MAP.md` regenerated.
- **Slice 2 — the claim→instrument map.** New `reference/evidence-instruments.md`: ten claim types → instrument → catalogued ids → **the evidence the gate must observe**, then one section per family (formal / physical / chemical-biological / linguistic / empirical / computational provenance) with the *limits* of each instrument (toolchain version, explored bound, coverage factor, agreement on a double-annotated sample, pre-registration deviations, multiverse spread). Wired into the load-index (`harness skill evidence-instruments`), `SKILL.md` step 6, and one router row (*"unsure what evidence would settle it"*).
- **Slice 3 — the emitted default.** `templates/AGENTS.md.tmpl` gains an **Evidence instrument · 证据仪器** stanza whose value `assemble._evidence_instrument()` derives from the matched capabilities: `formal-verification` ⇒ machine-checked derivation (no `sorry`/`Admitted`/`postulate` left); `dimensional-analysis` ⇒ units + propagated uncertainty (no unit-free numbers); `empirical-measurement` ⇒ effect size + interval + reliability + pre-registration; `reproducible-experiments`/`eval-driven-development` ⇒ re-runnable pipeline + frozen golden cases; otherwise the observed-artefact fallback. A generated harness now states its instrument **before** work starts.
- **Slice 4 — domain depth.** `logic`, `linguistics`, `cognitive-science`, `physics`, `chemistry`, `biology` READMEs each gain an **Instruments · 仪器** section naming the concrete tools, the gate evidence, and the field-specific trap (e.g. corpus **licence/consent**; an LLM annotator is an instrument, not an oracle).
- **Deliberate non-entries.** No `standard` kind for GUM/SI/NASA-STD-7009 (norms, not installable instruments — they stay references + gate text); no extra statistics packages beyond the four (`pingouin`/`JASP`/`PyMC` are interchangeable implementations, so adding them would not discriminate); no `proof-search` entry (a technique inside the formal row); no "AI annotator" entry (a risk to agreement, not a measurement). Recorded in the doc itself.
- **Verified.** `harness catalog --write` → `harness-index.md` (160) + `CAPABILITIES.md` + `HARNESS-MAP.md` (12 classes × 46 kinds · 160 catalog); new guards `tests/test_catalog.py::InstrumentCatalogTest` (3) + `tests/test_assemble.py::EvidenceInstrumentTest` (5); **181** tests OK (173 + 8). The instrument stanza was checked to **discriminate** on four representative tasks (formal / physical / empirical / generic).

---

## 2026-10-18 — P7.3: disciplines crosswalk — formal & empirical sciences (24 → 27 capabilities · 25 → 28 domains)
- **Question.** Survey the harness needs of mathematics, physics, mathematical logic / logic, linguistics, cognitive science and computing science — each on its own and where they cross — and integrate the real gaps.
- **Method.** Bare primary sources, fetched/confirmed this session (new group G, `[R98]`–`[R106]`): mathlib `[R98]` + Lean 4 `[R99]`; Open Logic Project `[R100]`; Universal Dependencies `[R101]` + Artstein & Poesio inter-coder agreement `[R102]`; Munafò *et al.* reproducible-science manifesto `[R103]`; Buckingham dimensional analysis `[R104]`; Anderson ACT-R `[R105]`; Woodcock formal methods `[R106]`. `[R98]`/`[R103]` fetched in full; the rest verified at the bibliographic record (not deep-read) — stated as such.
- **3 new domains (+ rubrics).** `logic` (new faculty `formal-sciences`), `linguistics` (humanities), `cognitive-science` (social-sciences) — each with `domains/<id>/README.md` (L0–L5 pipeline, module combination, field-specific risks) + `domains.json` signals + `rubrics.json`. Classifier: 3 new representative cases; the appended domains are designed to outscore overlapping signals.
- **3 new capabilities (data-only).** `formal-verification` (M3,M4,M6; `domain ∈ {mathematics, logic}` OR `verifiability = high AND artifact = code`), `dimensional-analysis` (M3,M6; physical domains), `empirical-measurement` (M3,M4; empirical domains). All three annotate **M3.10 (match the instrument to the claim)** — the new clause in `core/04` (+ checklist line + anti-pattern *unit-free numbers and p-only claims*).
- **Deliberately not added.** A `computer-science` domain (duplicates `software-engineering` + `data-science` + `logic`); `proof-search` (a technique; the requirement is M3.10); `statistical-significance` (same features as `empirical-measurement`). Reasoning + coverage matrix in `review/disciplines-crosswalk-2026-10.md`.
- **Docs + provenance.** New `review/disciplines-crosswalk-2026-10.md` (§3 each-field table, §4 crosswalk, §6 non-additions); `review/references.md` §G + `references.bib` group G; `sources/source-map.md` rows; router + `derivation-rules.md` rows; count refresh in `GUIDE.md`, `SKILL.md`, `PLAN.md`, `README.md`, `README.zh-CN.md`, `AGENTS.md`, `tasks/ASSESSMENT.md` (now carries a "later cycles moved these numbers" note).
- **Verified.** `harness catalog --write` → `harness-index.md` + `CAPABILITIES.md` (**27 capabilities**) + `HARNESS-MAP.md` (**9 modules · 27 capabilities · 28 domains / 10 faculties · 133 catalog · 29 rubrics · 23 CLI · 11 templates**); **173** tests OK (170 + 3).

---

## 2026-10-18 — P7.2: workflow patterns — loop & graph engineering (22 → 24 capabilities)
- **Question.** The 22 capabilities covered *context, security, durability, spend, evals* but had no entry for the **shape of the workflow itself**: the agent loop (termination, budget, per-step ground truth, stall detection) and the **declared topology** (branches, parallel workers, checkpointed nodes). `core/03` (M2) hinted at budgets/heartbeats and "an externalized state machine"; nothing named either requirement.
- **Method.** Bare primary sources, fetched this session (new group F, `[R93]`–`[R97]`, access 2026-10-18): Anthropic *Building effective agents* (workflow taxonomy + "agents … in a loop", ground truth per step, stopping conditions), ReAct `[R94]`, Reflexion `[R95]`, Google ADK docs `[R96]` (sequential/loop/parallel template workflows *superseded* by graph-based workflows; resume/cancel/event loop), LangGraph persistence docs `[R97]` (checkpointers vs stores).
- **2 new capabilities (data-only).** `loop-discipline` (M2,M3,M6; fires on `tool_surface ∈ {read_write, external}` OR `horizon ≥ multi_session`) and `graph-orchestration` (M2,M8; fires on `collaboration = multi_agent` OR `horizon ≥ multi_session`). Deliberately **not** added: `routing`, `prompt-chaining`, `reflection-loop` (already module items M2.2/M3.7 or catalog entries — a capability would duplicate `eval-driven-development`).
- **Invariants, not just labels.** `core/03-long-running-agents.md` gains **M2.10 (loop contract)** and **M2.11 (declared control graph)** + checklist + 2 anti-patterns; `core/09-collaboration-and-sessions.md` gains **M8.10 (declare the topology)** — so the capabilities annotate real clauses (M0.4).
- **Catalog correction.** `langgraph.maps_to` was `M6,M7` while its own summary says "with checkpointing"; corrected to `M2,M6,M7,M8` (`[R97]`), and `review/harness-index.md` regenerated.
- **Consumer side (asked).** `.harness/capabilities.local.md` (task-local, append-only) + `harness learn`/`cases`/`evolve` are the harvest channel, but **`updates/` holds no cases yet** — nothing to integrate from users; `profile.py` project capabilities (`has-tests`, `has-ci`, …) are a *different namespace* and are deliberately not merged. Reported honestly in `review/workflow-patterns-2026-10.md` §6.
- **Docs + provenance.** New `review/workflow-patterns-2026-10.md` (coverage matrix · decisions · non-additions · consumer audit); `review/references.md` §F + `references.bib` group F; `sources/source-map.md` rows; router rows; `derivation-rules.md` table; `tests/test_capabilities.py` gains 3 trigger tests.
- **Verified.** `harness catalog --write` → `harness-index.md` + `CAPABILITIES.md` (**24 capabilities**) + `HARNESS-MAP.md`; **170** tests OK (167 + 3).

---

## 2026-10-18 — P7.1: generated whole-factory map (`HARNESS-MAP.md`, `harness map`)
- **Motivation.** The library now holds 9 modules, 22 capabilities, 25 domains, 133 catalogued harnesses, a rubric+lever layer and ~23 CLI commands — but no single view. A reader (human or agent) had to open `core/`, `domains/`, `data/`, `reference/` and `cli.py` separately, and every release risked the prose drifting from the code.
- **Decision (why generated).** A hand-written overview decays; a *rendered* one cannot. New `src/harness_factory/harness_map.py` renders `HARNESS-MAP.md` from surfaces that already exist — the **CLI parser** (§7 command table), the **skill index** (§8 load order), `templates/` (§0), and the catalogs (§0/§3/§4/§5/§6). It only *reads* the SSOT (M0.4).
- **Sync mechanism (this is the point).** `tests/test_harness_map.py` (4 cases) asserts `render_doc() == HARNESS-MAP.md` and that every module/capability id appears; a stale map fails the suite with the fix command in the failure message. `harness catalog --write` now also refreshes the map, so the existing AGENTS.md rule ("after editing `data/*.json`, run `catalog --write`") already keeps it current.
- **Recorded in.** `HARNESS-MAP.md` (new, 226 lines: at-a-glance · 全景 · task→harness · modules · capabilities · domains · catalog classes · CLI · entry points · SSOT→view · how to sync); `cli.py` (`map` subcommand + dispatch); `skill.py` (`map` entry in the load index); both root READMEs; `SKILL.md`; `GUIDE.md` §5 + roadmap; `introduction.md`; `tasks/PLAN.md` (architecture + P2 bullet).
- **Verified.** `PYTHONPATH=src python -m harness_factory map --write` → `HARNESS-MAP.md`; `harness catalog --write` regenerates it too; **167** tests OK (163 + 4).

---

## 2026-10-18 — P7: frontier refresh into the capability SSOT (17 → 22)
- **Motivation.** The capability map is the *data-driven* middle layer between a requirement and modules (`capabilities.py`; `data/capabilities.json`). It had absorbed practitioner playbooks but not the 2025–26 frontier consensus on **context as a finite budget**, **untrusted content as data-not-instructions**, **durable execution**, **hard spend caps**, and **trajectory-level evaluation**. A library that is *referenced* must stay current (`tasks/REFRESH.md`).
- **Method (plan-first; citations are the lifeline).** Each candidate was (1) probed, (2) **fetched as a primary source** (arXiv abs page / official docs / standards body), (3) diffed against `core/`, `review/`, and the 17 existing capabilities before any addition, then (4) written to the SSOT. Aggregator blogs were read for orientation, never cited.
- **Verified refs (new group E, R84–R92).** Context Rot (Chroma R84); Willison "hard budget caps" (R85); OWASP Top 10 for Agentic Applications 2026, `ASI01–ASI10` (R86); MCP Security Best Practices (R87); CaMeL (R88); METR long-task time horizon (R89); Temporal *Durable AI* (R90); OpenTelemetry GenAI conventions (R91 — *listed*, README fetch timed out); Agent-as-a-Judge (R92). Pre-existing: lethal trifecta (R42), Anthropic context engineering (R52).
- **5 new capabilities (data-only).** `context-budget-policy` (M1,M2); `untrusted-content-discipline` (M4,M6,M7); `durable-execution` (M2,M3); `cost-budget-caps` (M3,M7); `eval-driven-development` (M3,M5). Each has a **distinct trigger** and does **not** fire on a plain local `read_write` coding task (`untrusted-content-discipline` keys on `grounding=required`, not the default `preferred`) — a capability that never discriminates is documentation, not a mechanism.
- **Docs + provenance.** New distillation `review/frontier-2026-10.md` (bilingual: converged signals, new-capability table, per-capability notes, deliberate non-adoptions, verification status, next-cycle cues); `review/references.md` §E + `references.bib` group E; `sources/source-map.md` capability rows; router rows in `reference/capability-router.md`; `reference/derivation-rules.md` capability table brought up to date (was 13, now 22). Regenerated `CAPABILITIES.md` (**22 capabilities · 9 modules**).
- **Verified.** `PYTHONPATH=src python -m harness_factory capabilities --write` → `CAPABILITIES.md`; ...tests below.

---

## 2026-10-16 — P6: make "mention the directory once" a **structural** guarantee (pointer + resolved path + self-check)
- **Motivation.** A standing reference held only in *prose* is a promise, not a mechanism: it is lost on context compaction, not inherited by subagents, and useless if the path changes. The fix is structural — the emitted harness must be able to **find** its factory on its own.
- **Resolved path instead of a placeholder.** `templates/AGENTS.md.tmpl` previously carried a literal `<harness_factory path>` that was never substituted. It now renders `{{ factory_root }}` (POSIX-normalised absolute path); when no checkout is reachable it falls back to the explicit placeholder — never an invented path.
- **`.harness/pointer.json` (new, emitted).** New `src/harness_factory/pointer.py` + `config.factory_root()`; `assemble.build_files` emits the pointer (native-escaped JSON) and `write_harness` threads a `factory_root` override (used by tests). Payload: resolved `harness_factory`, `skill_md`, `entry_docs` (router / refinement / flow), `capabilities_local`, `how_to_use`, `revoke`. Null path ⇒ the factory was not on disk at generation time.
- **Self-check.** `runtime.gate_report` gains an **advisory** gate (`.harness/pointer.json`) so `harness gate` reports reachability + whether the rules file carries the convention; `harness doctor --project <dir>` prints the same `pointer.verify()` result (`reachable: yes/no` + concrete problems). Advisory, not hard: another machine may legitimately not have the checkout.
- **Verified.** `init` → 12 files incl. `.harness/pointer.json`; emitted `AGENTS.md` names the real path (no placeholder); broken pointer → reported honestly (`factory not reachable at … (SKILL.md missing)`); new `tests/test_pointer.py` (+11) covers emission, null/unreachable/missing cases, gate wiring and `doctor`. **152** tests OK.

---

## 2026-10-16 — P5: frontier assimilation (ambition/agency) + capability router + bidirectional flow + standing reference
- **Frontier assimilation — F. Rieseberg, *How to be more ambitious* (2026-10-13), verified by full fetch.** New `review/ambition-and-agency.md` maps its four axes (**Speed / Altitude / Depth / Range**) onto M0–M8 and names the gaps. Anchor refs added: Rieseberg `[R80]`, Locke & Latham goal-setting `[R81]/[R82]` (DOIs verified), J. Read `[R83]` (marked **commentary**).
- **4 new capabilities** (`data/capabilities.json`; 13→**17**; data-only, no code): `ambition-elevation` (horizon ≥ session), `expert-instruments` (verifiability=high OR horizon ≥ multi_session), `cross-field-crew` (collaboration=multi_agent OR horizon=long_running), `bidirectional-capability-flow` (always). `CAPABILITIES.md` regenerated (`harness capabilities --write`); drift guard still green.
- **3 new reference docs** (`reference/`): `capability-router.md` (*situation → capability → module → file* — the entry for external tasks), `requirement-refinement.md` (R0 restate → R1 elevate → R2 classify constraints → R3 offer MVP/Elevated/Exploratory → R4 confirm → R5 converge), `capability-flow.md` (bidirectional loop). Registered in `skill.py` `_TAIL`, `SKILL.md` load-index, root README doc maps, `AGENTS.md` map.
- **Standing reference convention (per user, 2026-10-16).** `SKILL.md` §"PASTE THIS EXACT INSTRUCTION" rewritten: paste once → the factory stays active for the **whole conversation**; durable when pasted into the target's rules file (survives a new conversation + spawned subagents); revoked by saying **"stop using harness_factory"**. Updated consistently: root `README.md` / `README.zh-CN.md`, `GUIDE.md` (Example 4), `introduction.md` §9, workspace `AGENTS.md` §6.
- **Bidirectional capability flow is now materialised in the emitted harness.** `templates/capabilities_local.md.tmpl` → `.harness/capabilities.local.md` (task-local ledger; wired in `assemble.py` `_TEMPLATE_MAP` + `_selected_files`); `templates/AGENTS.md.tmpl` emits **Standing reference** + **Requirement refinement** + **Bidirectional capability flow** sections; `templates/tasks_PLAN.md.tmpl` gains a *Confirmed reading (R0–R5)* block. Smoke: `init` → 11 files incl. `capabilities.local.md`, `check` OK.
- **Fix (honesty).** Removed the non-existent "(M9 protocol)" label from `AGENTS.md.tmpl` — `core/` is **M0–M8** only (the new work is added as **capabilities + reference docs**, not new modules).
- **Tests:** +4 (`tests/test_standing_reference.py`: entry / root READMEs / emitted AGENTS.md carry the convention, **and no shipped doc still quotes the old config**) → **136** passing.
- **Double-check pass (same day).** Fixed three real gaps found by verification: (1) the *summary callouts* in `README.md` / `README.zh-CN.md` / `GUIDE.md` / `introduction.md` still quoted the **old** two-step config — rewritten to the standing version; (2) the emitted `AGENTS.md` / `.harness/capabilities.local.md` referenced factory-relative paths (`reference/*.md`) that do not resolve inside the **target** project — added an explicit **path convention** note and qualified the references (`harness-factory's …` / `harness skill <name>`); (3) added a drift guard test. Verified: 136 tests OK; router cites only real capabilities (15 ids); module ids M0–M8; each new capability fires exactly as declared; emitted harness = 11 files with no `{{ }}` leftovers; `_archive/` excluded (historical, out of VC).
- **Integrity repair (second, deeper check — found two real defects).** (1) **`GUIDE.md` was corrupted:** a previous session's raw assistant output had been written into Example 4 — scratchpad notes (`Wait — …`, `old:`/`new:`) plus literal DeepSeek-style tool-call markup (`<｜DSML｜ calls>`, `<｜DSML｜ parameter name="newString" …>`), with a duplicated fence. Repaired deterministically (749 → 695 lines, fences balanced, Example 4 replaced by the intended standing-reference version). (2) **`templates/AGENTS.md.tmpl` had an odd code-fence count**, so the emitted `AGENTS.md` rendered the standing-reference / refinement / flow sections *inside* one unclosed code block — i.e. the load-bearing instruction was visually swallowed. Why the earlier checks missed both: they grepped **content** for a few known strings but never verified **structure**. New `tests/test_docs_integrity.py` (+5) now guards: no raw assistant/tool markup in shipped docs; **balanced code fences** in shipped docs *and in every emitted file*; no unfilled `{{ }}` placeholders; GUIDE.md documents the standing reference → **141** passing.

## 2026-10-15 — P1+P2+P3 implemented: portable skills, Hermes/peer integration, capability overview doc
- **P1 — Agent Skills conformance (portable skills).** M6 now emits a spec-conformant skill at `.harness/skills/<name>/SKILL.md` (dir name = frontmatter `name`; `name` ≤64 lowercase-hyphen; `description` ≤1024), via new `templates/skills_SKILL.md.tmpl`; `assemble.py` gained `skill_name()`/`skill_path()` and emits the dynamic path; `templates/skills_README.md.tmpl` links it; `runtime.py` M6 advisory gate now also checks `skills/*/SKILL.md` (multi-artifact `_MODULE_ARTIFACTS`). The factory's own `harness_factory/SKILL.md` gained `license`+`compatibility` frontmatter (spec-valid). Spec: `agentskills.io/specification` (verified 2026-10-15).
- **P2 — tracked Hermes + peers.** `data/sources.json` +9 entities (Hermes Agent, Agent Skills standard, OpenClaw, Goose, OpenHands, Letta, pi, `benschrauwen/hermit`, `cashapp/hermit`; repo URLs verified by search); `data/harnesses.json` +6 entries (`hermes-agent`, `agentskills-standard`, `openclaw`, `letta-code`, `pi-mono`, `hermit-file-first`) and `goose`/`openhands` upgraded with `tracked`+skills tags → catalog **127→133**; `review/harness-index.md` regenerated.
- **P3 — capability `sandboxed-execution`.** New capability in `data/capabilities.json` (fires on `tool_surface=external` OR `stakes=high` → annotates M3/M6/M7); `security` lever enriched to M3/M6/M7 + sandbox note; mirrored in `reference/derivation-rules.md`.
- **Integration (extra) — capability `portable-skills`** (M6) + prose ecosystem subsection **§5a** ("Self-improving agent runtimes") with refs [30]–[37] in `review/harness-catalog.md`.
- **New generated overview doc `harness_factory/CAPABILITIES.md`** (purpose + how-it-works + modules table + every capability). Generated from `data/capabilities.json` + `modules.json` by `capabilities.render_doc()/write_doc()`; CLI **`harness capabilities --write|--markdown`**, and `harness catalog --write` now refreshes it too; drift-guarded by `test_agent_mode.CapabilitiesDocTest`. So it **auto-evolves with the SSOT**. Registered in `skill.py` (`harness skill capabilities`) and folded into `SKILL.md`, `GUIDE.md`, `introduction.md`, both root READMEs (tree + doc map), `reference/derivation-rules.md`.
- **Fixed (honesty):** `tasks/ASSESSMENT.md` Part B had a module-index off-by-one (used doc-file numbers) — corrected M3→**M2** (memory), M6→**M5** (self-evolution), M7→**M6** (tools), M9→**M8** (collab), `M0.2/M4`→**`M0.8/M8`** (human gate); added **B.6 implementation status** and refreshed A.1 counts (13 caps / 133 catalog / 132 tests / 56 docs).
- **Tests:** +4 (`test_agent_mode.py`: capabilities-doc drift, portable-skill conformance + runtime gate, `sandboxed-execution` firing rules, `portable-skills` default) → **132** passing.

## 2026-10-15 — Completeness assessment + external-harness integration review (doc only)
- **`tasks/ASSESSMENT.md` written (new).** Two parts. **A｜完整性/可用性评估** — measured surface (27 py files / 5,574 lines; 9 modules M0–M8; 11 capabilities; 25 domains across 9 faculties; 26 rubrics; 127 catalog entries = 11 classes × 33 kinds; 75 levers; 22 top-level CLI subcommands; 54 md docs; 128 stdlib tests) with a self-assessed scorecard → **≈85% complete, ≈90% usable**; ranked gaps: no external skill-format conformance, no trace-driven self-evolution evidence, no sandbox/least-privilege posture, M3 memory spec-only, network+LLM paths untested in CI, hand-maintained counts drift.
- **B｜外部 harness 整合评估（Hermes Agent 等）.** User corrected the earlier "hermit" to **Hermes** — the target is **Hermes Agent** by Nous Research (MIT; self-improving agent: agent-curated persistent memory, autonomous skill creation, skills that improve during use, `agentskills.io`-compatible `SKILL.md`, cron scheduler, subagents, multiple terminal backends, MCP). Verified from first-party sources only (`hermes-agent.org`, `github.com/NousResearch/hermes-agent`, `hermes-agent.nousresearch.com/docs`, all accessed 2026-10-15); community claims (DSPy+GEPA skill self-evolution) marked *unverified*.
- **Key finding:** the **Agent Skills (`SKILL.md`) open standard** (`agentskills.io`; originally Anthropic; ~50 clients incl. OpenCode, OpenHands, Goose, Letta, pi, Hermes, OpenClaw) is the highest-leverage integration — this repo already ships a `SKILL.md` entry point and emits `.harness/skills/README.md`, so spec conformance is small and makes emitted harnesses portable.
- **Proposals recorded (P1–P5, proposal-only per M0.4):** **P1** emit skills as `skills/<name>/SKILL.md` per the standard; **P2** track `hermes-agent` / `agentskills-io` / `openclaw` / `goose` / `openhands` / `letta` in `data/sources.json` (+ catalog entries, then `harness catalog --write`); **P3** new capability `sandboxed-execution`; **P4** enrich M3/M6 exemplars; **P5** optional memory-backend profile. Recommendation: do **P1+P2** first; hold P3–P5. Not yet implemented — awaiting user go-ahead (SSOT changes).
- **Drift prevention.** Added `ASSESSMENT` to the `tasks/` lines in `AGENTS.md`, root `README.md`, `README.zh-CN.md`, `tasks/PLAN.md`; extended `GUIDE.md` §12 and both root doc maps to point at the new file.
- **Peer landscape verified:** `benschrauwen/hermit` (file-first self-improving runtime: heartbeat, telemetry, strategic review, git checkpoints, `nono` sandbox, `pi-mono`) and `cashapp/hermit` (hermetic per-project toolchains) — the user's originally-typed "hermit", kept in the review as a peer.

## 2026-10-15 — P2 (writing registered) + P3 runtime hooks + P4 plugin protocol (done)
- **Writing domain registered (P2 tail).** Added the `writing` entry to `data/domains.json` (faculty `humanities`, artifact `document`, grounding `required`, 9-step workflow, 20 signals — verified no signal collisions) and a weighted `writing` rubric to `data/rubrics.json`. `--domain writing` is now selectable, `standard --domain writing …` works, and `classify` reaches it by signals. Registered under the existing `humanities` faculty so the fixed `FACULTIES` test set is unchanged.
- **P3 — runtime hooks (new `runtime.py`).** **Gate runner** (`gate_report`, CLI **`gate`**): runs the structural self-check and **executes the emitted `.harness/check.py`** as its own hook; **hard** gates (manifest-valid, files-present, no-placeholders, check-py-runs) decide the exit code, while **advisory** module gates (M2/M4/M6/M8) report outstanding evidence (M0.3). **Signal harvest** (`harvest`/`record_signals`, CLI **`harvest`**): collects domain/modules/capabilities, gate outcomes, progress/ledger counts, and any agent-appended `.harness/signals.jsonl`, then appends **one** observation line to `<kb>/updates/signals.jsonl` — observe-only (M0.4/M5).
- **P4 — plugin protocol (new `plugins.py`).** Read-only discovery from `HARNESS_PLUGINS_DIR` (else `<data>/plugins`). **`domain`** plugins merge over the SSOT via `registry.domains()` + `standard.rubrics()` (`--domain <plugin-id>` becomes selectable) and may emit `extra_templates`; **`template`** plugins register reusable emitted files. Strict validation (id==dir, closed vocabularies, rubric weights sum ~1, template file present, no built-in shadowing) surfaced by CLI **`plugins [--validate]`**. The SSOT catalogs are never mutated; a plugin that shadows a built-in is reported and ignored.
- **Registry/standard caches** gained `clear_caches()` (used by tests and after a plugin-path change); `assemble.build_files` now emits a domain plugin's extra templates and lists them in `manifest.files`.
- **Tests:** +25 (`test_runtime.py`: gate pass/fail on fresh/tampered/missing/placeholder harnesses, advisory module gates, harvest bundle + JSONL record + custom signals; `test_plugins.py`: discovery, registry/rubric merge, classify reach, extra-template emission + check pass, validation for bad artifact/rubric/template/id/shadow/escape; `test_cli.py`: gate/harvest/plugins) → **128** passing.
- **Docs synced (task 1 — vibe-coding assistant usage).** `SKILL.md` rewritten with a clear "Using this repo as a skill · 把本仓库当作 skill 使用" section (L0 one-liner + concrete pasteable example + L0 checklist + variant-prompt table + L1 CLI block incl. gate/harvest + optional `install-skill.ps1` note); fixed `SKILL.md` cross-references in `README.md`/`README.zh-CN.md`/`harness_factory/README.md`/`GUIDE.md` (broken `harness_factory/harness_factory/…` and non-relative links); `GUIDE.md` command reference + Example 10 (runtime hooks & plugins) + roadmap; `tasks/PLAN.md`, `introduction.md`, `domains/writing/README.md` status, `AGENTS.md`/READMEs tree counts (23→24 disciplines).
- **Directive restructured to two steps: 配置 → 任务 (per user, 2026-10-15).** The single one-liner became a **reusable configuration** (how to reference & use the tool) followed by the **task**, which may be sent in the same turn or the next (or as attachments). Updated: `SKILL.md` (§L0: Step 1 config + Step 2 task; variant table reframed as task sentences), `AGENTS.md` §6, root `README.md`/`README.zh-CN.md`, `harness_factory/README.md`, `GUIDE.md` (中文速览 + Example 4 two-step walkthrough), `introduction.md`. Rationale: set the config once, type only a short task each time.
- **Copy-paste prompt templates written into the root READMEs (per user, 2026-10-15).** A standalone `PROMPTS.md` was tried first, then dropped in favour of inlining: the two-step templates now live **directly in the root `README.md` (English) and `README.zh-CN.md` (Chinese)** under 「Agent prompt templates · 给 agent 的提示词模板」 — ① paste-once configuration, ② task + variant task lines, ③ domain task lines (writing / excellence), ④ save-as-snippet / project rule + the L1 CLI block. The top blockquotes and doc maps now point at the in-file section; `SKILL.md`, `harness_factory/README.md`, and `GUIDE.md` §12 reference the root READMEs. Also fixed a stale example count in `harness_factory/README.md` (9 → 10 实例).
- **A/B/C hardening from the completeness review (2026-10-15).** **A** — fixed module-range drift: `core/` is **M0–M8** (9 modules in `data/modules.json`), so the three stale `M0–M9` mentions in `AGENTS.md` / root `README.md` / `README.zh-CN.md` were corrected and the root README `Updated` dates bumped to 2026-10-15. **B** — added a cross-OS **end-to-end CI smoke** (`.github/workflows/ci.yml`: `init → check → gate → harvest → plugins --validate`, `shell: bash`, `set -euo pipefail`) and pinned the existing CLI smoke to bash so `/dev/null` works on `windows-latest`. **C** — made offline-vs-network explicit: a `network` line in `harness doctor` plus an "Offline by default / 默认离线" note in both root READMEs (only `refresh`/`intel` feeds and the optional LLM classifier reach the network).
- **READMEs consolidated (per user, 2026-10-15).** Removed the duplicated `harness_factory/README.md` — its positioning/structure/usage had kept drifting from the root pair. Its unique content (the *Key stance* invariant, the tracked-source registry detail, the *requirement → harness & mutual learning* paragraph, the full annotated **Layout** tree, the *How to use this factory* 5 steps, and the *Generalization rule*) was folded into the root [`README.md`](../README.md) (English master) and its mirror [`README.zh-CN.md`](../README.zh-CN.md). The root READMEs are now the **single source** for positioning / structure / usage; `harness_factory/` keeps [`GUIDE.md`](../harness_factory/GUIDE.md) (full guide + 10 examples) and [`SKILL.md`](../harness_factory/SKILL.md) (agent entry) as its detailed docs. Fixed every inbound reference (`AGENTS.md` repo map, `GUIDE.md` §12, both doc-map rows) and switched `pyproject.toml` `readme` to inline text so it no longer points at the deleted file. Tests 128 OK; all markdown links in the entry docs verified to resolve.

## 2026-10-14 — P2: frontier-standard executable ratchet + writing domain (done)
- **Frontier-standard CLI.** New `standard.py` + CLI **`standard`**: `harness standard [--store F] --domain <D> bar|score|audit|raise|plan|frontier <objective>` over a bar ledger (default `updates/standard.json`). `bar` names a sourced apex bar (levels R1–R6); `score` records per-dimension scores on the domain rubric; `audit` prints weighted gaps largest-first; `raise` ratchets the floor (`floor_next = max(floor, achieved)`) and **refuses regressions** unless `--force`; `plan` turns gaps into a harness config; `frontier` records a re-check of a moving bar.
- **Per-domain rubrics.** `data/rubrics.json` (25 entries: `default` + every domain in `domains.json`) — weighted dimension tables per domain, so the same ratchet applies to code, math, law, medicine, the arts, etc.; unknown domains fall back to `default`.
- **Gap → lever map.** `data/levers.json`: each rubric dimension → the modules (M0–M8) and catalog tool-kinds that close it, anchored to Claude/Anthropic's documented practice where one exists; `standard plan` grounds its tool suggestions in `data/harnesses.json`.
- **Stale-frontier audit.** `evolution.audit` gains `stale_frontier`: an apex bar (R4+) not re-checked within `FRONTIER_MAX_AGE_DAYS` (90), or a floor with no named bar → proposal only (human-gated).
- **Excellence docs.** `domains/excellence/{standard-ladder.md,self-standard.md,security-model.md}` — the ratchet mechanism in detail; this project held to Anthropic's engineering bar (`standard --domain software-engineering plan harness-factory` → its own gap config); least-privilege / human-gate / reversibility security model.
- **Writing domain (doc-level).** `domains/writing/README.md` — citation-first essay harness for weak-spot writing (evidence/structure/originality): thesis→outline→context pack→forced claim→evidence pairing→originality check→clarity pass; humanities-aligned rubric. **Not yet registered** in `domains.json`/`rubrics.json` (SSOT) — registration is a pending decision, so `--domain writing` is not selectable in the CLI yet.
- **One-line agent directives (一句话指令词).** Paste-ready one-sentence prompts added to the main entry docs (root READMEs, `harness_factory/README.md`, `GUIDE.md`, `SKILL.md`) and to the excellence/writing domain READMEs.
- **Tests:** +17 (`test_standard.py`: rubric scoring, bar ledger roundtrip, ratchet no-regression, plan/levers, stale-frontier audit) → **103** passing.
- **Docs synced.** `GUIDE.md` (command reference, Example 9 ratchet walkthrough, test count), `harness_factory/README.md` (standard block + writing layout), root `README.md`/`README.zh-CN.md` (quickstart + standard), `domains/excellence/README.md`, `domains/writing/README.md`.

## 2026-10-12 — P1.8: agent-native mode + project learning (done)
- **Agent-native (L0/L1).** Added `SKILL.md` (front-matter + 4 cardinal rules + load-index + output contract + provenance requirement), `reference/derivation-rules.md`, `install-skill.ps1` (optional copy into a skills dir), and `skill.py` (`index`/`find`/`read`); CLI **`skill`** prints the load-index (`harness skill M4` prints one module). An assistant pointed at the repo + a task goal derives and emits the harness itself — no install.
- **Capability mechanism (requirement → harness).** `data/capabilities.json` (10 capabilities) + `capabilities.py` (feature match → annotate enabled modules); `spec.HarnessPlan.capabilities`; `derive` annotates. New requirements are added by editing JSON, not code. CLI **`capabilities`**.
- **Project profiling + mutual learning (project → factory).** `profile.py` scans a target project (stacks, tests/packaging, structure; observe-only) → `updates/profile/<slug>.{json,md}`; `learning.py` records **cases** (`updates/cases.jsonl`) and aggregates them. CLI **`profile`**, **`learn`**, **`cases`**; `--project` on `derive`/`init` wires a weak domain hint + optional `.harness/PROFILE.md`.
- **Evolution from cases.** `evolution.audit` gains `missing_capability` (a project capability recurring ≥2× but absent from the registry); `propose` emits an `add_capability` proposal; `run_evolution` loads cases via `learning.load_cases` (human-gated).
- **Provenance output.** `assemble` always emits `.harness/PROVENANCE.md` (derivation record; mark unverified); `AGENTS.md.tmpl` gains a capabilities section.
- **Packaging cancelled.** Locked with user: L0/L1 only; PyPI / `uv tool install` / pipx / zipapp / MCP dropped as distribution channels (`pyproject.toml` kept as dev/CI convenience). Decision in `tasks/DISTRIBUTION.md` §8; PLAN new consumption-model + requirement→harness + mutual-learning sections.
- **Docs synced.** `harness_factory/README.md`, root `README.md` + `README.zh-CN.md`, `introduction.md` (§9 agent-native & learning; §10 roadmap P1.8).
- **Tests:** +9 (`test_agent_mode.py`: skill index/read, capabilities match/annotate, profile scan, learning case roundtrip, mutual-learning missing_capability) → **71** passing.

## 2026-10-12 — P2 (partial): disciplines + unified harness catalog (done)
- **Disciplines expanded to 20.** `domains.json` now covers a faculty-level taxonomy: meta (research, knowledge-management, devops, general), engineering (software-engineering, engineering, data-science), natural-sciences (physics, chemistry, biology, earth-environment, mathematics), health (medicine), social-sciences (economics-finance, psychology, social-science), law, humanities, education, arts (arts-design). Added domain READMEs for all 19 non-general domains; `classify` picks a domain from signals (deterministic).
- **Unified harness catalog.** New `data/harnesses.json` (SSOT) — 55 entries across classes (coding/orchestration/self-evolution/memory/skills-protocols/evaluation/survey/safety), kinds (terminal-agent/ide-agent/sdk/protocol/self-modifying/evolutionary-search/weight-adaptation/inference-correction/skill-library/memory-system/benchmark/survey/safety-framework/skills-ecosystem), core-module maps, vendor/ecosystem, and `tracked` cross-links to `sources.json`. Unifies the conceptual taxonomy with vendor SDKs/CLIs (Claude Code, MCP, ADK, A2A, Gemini CLI, Agents SDK, etc.).
- **Catalog tooling.** `catalog.py` (load/search/filter/render/validate/write_index) + CLI `harness catalog` (`--class/--kind/--module/--vendor/--tag/--search/--tracked/--markdown/--write/--json` + `harness catalog <id>`). Generated `review/harness-index.md` from the data.
- **Discoverability.** `skill.py` derives domain entries dynamically from `domains.json`; added `harness-index` and `harnesses.json` to the load-index. `registry.py` falls back to bundled catalogs if user home lacks a file (keep checkout as SSOT).
- **Quality.** `tests/test_domains.py` (breadth, wellformedness, README presence, non-overlapping signals, classification smoke) and `tests/test_catalog.py` (validate clean, search/filter, tracked cross-links, index doc drift guard) added. All **86** tests pass.
- **Docs.** `README.md` + `README.zh-CN.md` + `introduction.md` + `core/00-index.md` + `tasks/PLAN.md` synced to reflect the 20-domain taxonomy and unified harness index.

- **Feed coverage:** probed + wired RSS/Atom feeds across the registry — **47/59 entities** now tracked (was ~20). `releases.atom` vs `commits.atom` chosen per repo; YouTube `@handle` → channel feed resolved and verified. 12 remain feedless by the honesty rule (no legitimate feed: ICML/ICLR/ACL/EMNLP/TMLR pages; a few people sites).
- **Watermark:** `refresh` persists the effective `since` to `updates/state.json` (`load_state`/`save_state`); repeated cycles surface only new items without re-passing `--since`.
- **Discovery→registry:** `evolution.audit` gains `queue_rows` and detects `untracked_source` (accepted candidate from an untracked host); `propose` emits `add_source` proposals; `run_evolution` loads `updates/queue.jsonl`.
- **Docs + scheduler:** `refresh.ps1` now runs `refresh --provider all --intel` then `evolve`; `introduction.md` + `tasks/PLAN.md` synced (sources/intel/evolve commands, P1.6/P1.7 milestones); stale legacy paths removed from `.gitignore`.
- **CI / packaging:** added `.github/workflows/ci.yml` (ubuntu+windows × 3.10/3.12), `CHANGELOG.md`, `.gitattributes`; `pyproject.toml` classifiers + `project.urls`.
- **Tests:** +12 (`test_cli.py` end-to-end CLI, `test_sources.py` registry validation, plus watermark + untracked-source cases) → **62** passing.
- Fixed a data bug: `langchain` topic `tool-surface` → canonical `agent-skills-tools`.

## 2026-10-12 — P1.7: intel tracking + self-evolution (done)
- Added `data/sources.json`: tracked-entity registry with 5 groups — **projects** (OpenAI, Anthropic, Google DeepMind, Meta, Mistral, DeepSeek, Moonshot/Kimi, …), **harnesses** (Agents SDK, Swarm, Codex, Claude Code, MCP, Claude Agent SDK, ADK, Gemini CLI, A2A, Llama Stack, Mistral Agents, …), **venues** (Nature/Science/NeurIPS/ICML/ICLR/ACL/arXiv), **people** (Karpathy, Ilya, LeCun, Hassabis, …), **media** (Substack/YouTube/newsletters). 59 entities.
- `collect.py`: RSS 2.0 + Atom `parse_feed`, `http_get`, `iter_entities`, `resolve_youtube_feed` (`@handle` → channel feed), `feed_provider`; `Candidate.entity` added.
- `extract.py`: deterministic intel (relevance = topic keywords + entity mention + recency, topic/entity tagging, verbatim brief); optional LLM summary; writes `updates/INTEL.md` + `intel.jsonl` (grouped projects/harnesses/venues/people/media).
- `llm.py`: refactored to `_chat_content` + added `summarize()`.
- `evolution.py`: complete cycle **snapshot → audit → mutation-proposal → journal** + metrics (`updates/EVOLUTION.md`, `evolution.jsonl`, `metrics.jsonl`); human-gated `apply_accepted` → `updates/accepted.json` (reversible). Audits: uncovered topics, empty groups, stale sources.
- `refresh.py`: `load_sources`, feed provider support, `--intel` extraction wired in; summary gains `intel_items`.
- CLI: **`sources`**, **`intel`**, **`evolve`**, **`evolve-apply`**; `refresh --provider {auto,file,llm,feed,all}` + `--intel` + `--sources`.
- Rewrote root `README.md` + `README.zh-CN.md` (project intro + tool usage; archived old content); synced `harness_factory/README.md`.
- Tests: +14 (`test_intel.py`: feed parse/resolve/provider, intel scoring/enrich/write, evolution snapshot/audit/propose/run/apply/dry-run) → **49** passing.

## 2026-10-12 — P1.6: cross-project packaging (done)
- Evaluated tool forms → `tasks/DISTRIBUTION.md`; wrote `introduction.md`.
- Locked with user: primary = **installable package via `uv tool install`**; state = **user data dir**; channel = **git-only first**; names = pkg `harness-factory`, cmd `harness`.
- Added `config.py` (tool home resolution: `HARNESS_HOME` → platform default; optional `config.toml`; catalog/corpus/updates dirs; seeding; corpus-root resolution).
- `registry.py` now prefers the user catalog (`HARNESS_DATA_DIR` → user catalog → bundled).
- `refresh` re-rooted: corpus from checkout `review/` if present else home `corpus/`; CLI `refresh`/`refresh-apply` default to the **user home** (`--root`/`--data-dir` override).
- New CLI: **`doctor`** (paths/config/seed/LLM) and **`self-update`** (re-seed tool catalog; non-destructive, journaled, `--force`).
- `init --out` defaults to `./<task-slug>`.
- `.gitignore`: exclude `harness_factory/_archive/` and `harness_factory/updates/` from version control.
- Verified from an arbitrary directory with isolated `HARNESS_HOME`: doctor/self-update/refresh/init all work; emitted harness self-check OK.
- Tests: +7 (`test_config.py`) → **35** passing.

## 2026-10-12 — P1.5: self-update loop (done)
- Added the M5 self-update subsystem: `refresh` (collect → audit → rank → proposal → journal) and `refresh-apply` (human gate).
- New modules: `collect.py` (Candidate + file/llm providers, `verify_url`), `curate.py` (audit/dedupe/score/trends), `journal.py` (report/queue/proposal writers + append-only journal), `refresh.py` (orchestrator + apply gate).
- `llm.py`: added `discover_items()` (env-gated, returns untrusted items; always audited).
- `data/watchlist.json`: 8 topics + 4 frontier probes (boundary expansion).
- CLI: `harness refresh` (`--root/--inbox/--watchlist/--provider/--since/--verify/--dry-run/--json`) and `harness refresh-apply --accept`.
- `refresh.ps1` + `tasks/REFRESH.md`: weekly scheduling (Task Scheduler / cron / GitHub Actions) and the human gate.
- **Guardrails honored:** provenance gate drops untraceable items (M4); observe-only (M0.4); human gate (M0.8); all output under `updates/`, append-only journal, fully reversible (M0.9).
- Tests: 28 total (`test_refresh.py` adds provider roundtrip, injected LLM discovery, dedupe/score, dry-run, apply-by-index, corpus key extraction).

## 2026-10-12 — P1: inclusive harness CLI (done)
- Locked decisions with user: CLI scaffolder · hybrid rules+LLM · Python · MVP = task→harness generator.
- Wrote `tasks/PLAN.md` (architecture, derivation model, milestones, risks).
- Built the package: `pyproject.toml`, `spec.py`, `registry.py`, `derive.py`, `classify.py`, `llm.py`, `render.py`, `assemble.py`, `check.py`, `cli.py`, `__main__.py`, `data/{modules,domains}.json`, 8 templates.
- Fixed: `__init__.py` now sources `__version__` from `_version.py` (SSOT); CLI forces UTF-8 output (Windows cp1252 console crash on `title_zh`); removed a literal `{{` from emitted gate text that would have tripped the self-check.
- Verified end-to-end: `harness init --task "..."` → 8 files, `harness check` OK.
- Tests: 21 unittest cases (derive rules, classify, assemble/check). All pass.

### Notes
- Python available: 3.12.9 (miniconda). `pytest` not installed → tests use stdlib `unittest` to stay dependency-free.
- Tool self-constraint: M0.4 (observe/classify/emit only; never fabricate task substance).
- Run tests: `$env:PYTHONPATH="src"; python -m unittest discover -s tests`.
