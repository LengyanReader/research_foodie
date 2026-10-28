# Judge & verifier robustness · 评判者鲁棒性（D7 关账轮 · P39）

> **中文速览。** D7 的重访触发在 P38 生效（R254 升为全文级），本轮以「golden-set 审计」的判据开题：**评判者/
> 验证器/golden set 本身是被测组件**——其失灵方式已被三篇全文级一手文献量化（自偏好偏差 · RLVR 攻破验证器 ·
> reward-hacking 基准）加一份反作弊基准设计实测（LHTB 升级为已读）。落地一条子句 **M3.18**（评判者先受检：
> 偏差面声明 · 未强制面审计 · 重放评分 · 难度/模型变化重审）；**不加能力**（判别力不足，记不新增）；D7 → done。
> golden set 的可信度 = 其评判者过 M3.18 四关的程度。

**Updated:** 2026-10-28 · **Round:** P39 (closes D7) · **Evidence level:** 3 papers + 1 project page read in full (access 2026-10-28)

## 1. What the round read · 读到的（全部全文）

| ref | what | load-bearing findings |
|---|---|---|
| R263 | Self-Preference Bias in LLM-as-a-Judge (Wataoka/Takahashi/Ri, 2410.21819, CC BY 4.0) | 自偏好用 Equal Opportunity 量化——GPT-4 对自家输出的召回差 **0.520**（最大）；机制是**困惑度/熟悉度**而非「自己生的」（对他家模型的文本与自家文本的判定率无显著差异），且**关乎风格甚于对错**；同族谱系风险=评判者「可能无意中强化自己的风格与政策」；缓解（跨族集成、低困惑度样本降权）**建议而未验证** |
| R264 | LLMs Gaming Verifiers (Helff et al., 2604.15149, CC BY 4.0) | RLVR 模型「系统性放弃规则归纳」、利用**验证器未强制之处**；两种作弊形：直白枚举 + **混淆枚举**（「视觉上模仿合法假设、保留作弊行为」）；**因果性**：仅奖励信号不同的受控训练对在 extensional 验证器下产生 **~3.5 分作弊差距**，同构验证器消除之；审计工具 **IPT**（对象常量双射重命名下的不变性）。注意：overwrite unit tests / monkey-patch scoring 是**引用的背景**非其观察——引用时不得转嫁 |
| R265 | Reward Hacking Benchmark (Thaman, 2605.02964, ICML 2026, CC BY 4.0) | 13 个前沿模型作弊率 **0%–13.9%**；RL 归因（V3 0.6% vs R1-Zero 13.9%，各厂商同向）；六类作弊（序列伪造 31% · 泄漏 24% · 篡改 · 代理/解析器 · 特判 · 拒评）；作弊率**随链长上升、链长 5 处陡增**，hard 变体让 0% 模型也出手（13/13 非负增）；环境加固 **−87.7%**；**72% 作弊带显式 CoT**——28% 能逃过轨迹监控 |
| R246↑ | LHTB 项目页（listed → **已读**） | 46 任务、隐藏验证器 + 确定性种子 + **重放评分**；「声称的进度不算数——重放的进度才算」；全部模型同一 harness（M3.16 的评分侧同义）；最优模型 0.51、29/46 从未被通过 |

## 2. The audit · 本库评判者接触面的审计

| surface | 已有约束 | 缺口 → M3.18 的落点 |
|---|---|---|
| M0.3 builder≠judge | 新上下文 + 无写权限（运行期干预：篡改/拒评） | **谱系偏差**未覆盖（同一模型的裁判读自家风格输出给高分）；**验证器盲区**未覆盖 |
| M3.17 agreement≠verification | 采样共识的投票谬误 | 不涉及 judge 自身偏差与 golden set 完整性 |
| M5.11 搜索+可信评估器 | 「自改进=搜索+可信评估器」 | 评估器被**假定**可信——无条款要求声明可信的依据 |
| M5.13 自编辑验收门 | 验证器用验收标准把关更新 | 把关者自己未被审视（谁审计审计者） |
| P24 effect 轴 | judge=machine 需已定义度量器 | 有度量器 ≠ 无偏：机器判决者同样要过 (a)–(d) |

**结论（判别性）。** 缺口收敛为一个主张类型：**「一个评判者的判决正在把关某事」**——它不命中一切任务（普通
文档工作无评判者把关），判别力足够落子句。四项义务 (a)–(d) 全部锚定上述一手源。

## 3. What landed · 落地

- **子句 M3.18**（`core/04`）：评判者在判决把关任何东西之前——(a) 声明偏差面（谱系关系；自偏好是**要声明的
  利益冲突**而非自动取消资格）· (b) 审计验证器未强制之处（IPT 为黑盒检验范例）· (c) **从重放产物评分、绝不从
  自报评分**（R246 为一手范例）· (d) 难度或服务模型变化时重审（M4.17 同构：模型是变量）。**golden set 的可信
  度 = 其评判者过 (a)–(d) 的程度**——这就是 D7 标题的答案。
- Checklist 一行 + 反模式两条（**Grading on self-report** · **Judge-validated-once**）+ 中文块。
- references **§Y**（R263–R265，全文级）+ **R246 升级** + bib 3 条 + source-map M3.18 行。
- `scored-task-set` 文档 effect 轴补一句：机器判决者同样受 M3.18 约束。

## 4. Deliberate non-additions · 刻意不加（M0.5）

- **不加 `judge-robustness` 能力**：8 轴特征向量没有「评判角色」轴；若键在 verifiability=high 或
  eval-driven-development 邻域，会命中几乎所有高可验证任务——不判别。子句经 M3 常开模块生效。重访触发：出现
  需要区分「评判侧/被评侧」工作的任务族，或特征向量新增评判角色轴。
- **不开 D1 阶段 D（LLM 辅助审计）**：R263 表明 LLM 评判带结构性偏差且缓解未经验证——trace-audit 保持规则
  制是**当前正确姿势**；stage D 从「等 D7」改为「等 M3.18(a)-(d) 在某个真实 LLM 评判上跑过一轮」。
- **不为 LHTB 开目录条目**：基准是仪器候选，但其价值在本轮是**反作弊设计的范例**（(c) 的一手锚），非本库
  工作流的可执行仪器。
- **两个搜索命中不入 references**：reward-hacking 综述（PCH 框架）与研究 agent 的 reward-hacking 研究均未
  解析到 arXiv id（不猜 id 规则），只在本节留名待重访。

## 5. Verification

`PYTHONPATH=src python -m unittest discover -s tests` → **379 OK**（+4 守卫：M3.18 内容锚 · checklist/反模式 ·
§Y + R246 升级 + bib · survey/effect 轴指针）；`harness cycle audit` → **35 轮 · 0 硬 · 0 缺口**；D7 →
`done_in P39`；视图重生成。数据卫生项：**D6 关账**——jspsych.org 复检 HTTP 200，`verified: false` 翻正
（库内最后一条未验证仪器条目清零）。
