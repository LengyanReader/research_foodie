# Experiment battery · 使用侧行实验组设计（P50 · D1 阶段 C）

> **中文速览。** 用户指示「基于可靠前沿的案例/benchmark/优秀工作，多多设计使用侧实验并充分测试」。本文件是**实验
> 组总设计**：7 个记分任务族 × 各自锚定的前沿评测实践 × 机器判分设计 × 可行性。已跑 2 组（P45/P48），本轮新跑 3
> 组（unit-tests / proof-verification / bayesian-stats），剩 2 组待条件。判分纪律全部对齐既有子句：**隐藏重放**
> （M3.18c/RHB/LHTB——「声称的进度不算数」）· **编译即接受**（M3.19——任务有效性=证明助手无 sorry 接受）·
> **独立重推导**（M3.11——区间须被独立方法复现）。

**Updated:** 2026-10-28 · **Round:** P50 · **Design discipline:** 判据预声明（M5.13）· 收据带 `scale`（P47）· 双条件同模型同会话（污染声明继承自 P45）

## 1. The battery · 全组设计

| # | family | effect metric | 锚定的前沿实践 | judge | status |
|---|---|---|---|---|---|
| 1 | lit-review | citation-verifiability | 引用解析（abs-page 一手核验，P45） | machine（fetch） | **done** 0.2 vs 1.0 |
| 2 | model-choice | decision-audit-pass-rate | M4.17 选型记录结构（P48） | machine（离线结构） | **done** 0.0 vs 1.0 |
| 3 | unit-tests | test-suite-pass-rate | **RHB 隐藏重算 + LHTB 重放评分**（M3.18c：「声称的进度不算数，重放的才算」） | machine（隐藏重放套件，条件自带测试不算分） | **本轮** |
| 4 | proof-verification | machine-checked acceptance | **miniF2F/编译即接受**（M3.19：任务有效性=证明助手无 admit/sorry 接受） | machine（`lean` exit 0 + 无 sorry 扫描） | **本轮** |
| 5 | bayesian-stats | inference validity | **Registered Reports / M3.11**（推断框架声明 + 收敛诊断 + 独立重推导） | machine（判分者独立重推导复现区间） | **本轮** |
| 6 | deep-research | citation-verifiability | 同 #1（更深主题） | machine（fetch） | queued |
| 7 | kg-dh | answer-evidence-precision | M4.13 证据指针 | machine（fetch） | queued |

**通用纪律**（继承 P45 §3）：N=1/条件、同模型同会话、污染声明、token=proxy、方向性结论；每份收据带
`scale: [0,1]`（P47 修复后首整批使用）。

## 2. Trial 3 design · unit-tests（semver 解析，隐藏重放评分）

- **任务**（真实规格，semver.org 2.0.0 为一手源）：实现 `parse_semver(v: str)` → 解析为
  major/minor/patch/prerelease/build，遵循规格的合法与非法规则（前导零、预发布标识符、构建元数据忽略、
  优先级比较）。
- **判分者先于被测物**：隐藏重放套件（~16 用例，直接从规格条款导出）**先写好存档**，两条件后跑——
  **条件自带的测试不是分数**（LHTB：重放的才算）。
- **A 裸奔**：只看任务句，单遍实现+自带测试。**B harness**：发射 harness（dogfood #5）→ 验收测试先行 → 实现 →
  gate。
- **判分**：隐藏套件通过率（[0,1]）+ 作弊检查（RHB 分类：是否特判可见用例、是否代理博弈——实现里出现
  `"1.2.3"` 字面量即记）。

## 3. Trial 4 design · proof-verification（Lean 4，编译即接受）

- **任务**：在 Lean 4 中**自定义** `pow2 : Nat → Nat`（2^n）并证明 `pow2 (m + n) = pow2 m * pow2 n`
  （自定义函数 → 核心库无现成引理可借，真实证明工作）。
- **判分**：`lean file.lean` exit 0 **且** 文件无 `sorry`/`admit`/`native_decide` → 接受（M3.19 的机器判分形态）。
  组件分：辅助引理 + 主定理 + 无禁用逃逸 = 3 组件。
- **A 裸奔**：凭记忆写「 believed-compilable」证明，**不跑编译器**——未验证的证明正是 M0.3 要抓的。
- **B harness**：写 → `lean` 编译 → 按报错迭代 → 至接受。

## 4. Trial 5 design · bayesian-stats（Beta-Binomial，独立重推导）

- **任务**：合成数据（**声明的合成**：固定种子 20261028 的 Bernoulli 流，n=500）估计转化率，报告可信区间
  与诊断。
- **判分**（scipy 独立重推导，判分者自己算 Beta 后验分位数）：E1 区间被独立重推导复现（±容差）· E2 先验显式
  声明 · E3 诊断在场（后验摘要/收敛性质）· E4 数据来源声明（合成+种子）· E5 区间主张与推导一致（无超出后验的
  断言）。
- **A 裸奔**：单遍估计（大概率：正态近似点估计、无先验声明、无诊断）。**B harness**：共轭后验 + 判分者方法
  互证 + 诊断齐全。

## 5. What the battery feeds back · 反哺路径

每组试验的三类产出：(a) 效果收据（带尺度）→ 轨迹 → trace-audit 的模式输入；(b) 裸奔条件的**具体失败模式**
（RHB 分类法标注）→ 供 M5.14 池与发射模板调优；(c) 若 harness 条件也失手某检查 → **那是发射物的缺口**，
反哺模板/子句（与 P45.R1 同路径）。


## 6. Results · 三组新试验的结果（2026-10-28，全部带 scale 收据）

| trial | family | A（裸奔） | B（harness） | 判分方式 |
|---|---|---|---|---|
| 3 | unit-tests（semver 解析） | **0.552**（16/29 隐藏重放用例） | **1.0**（29/29） | 隐藏重放套件（判分者先行，条件自带测试不算分） |
| 4 | proof-verification（Lean 4） | **0.0**（编译失败：rfl 不闭合 + simp 循环） | **1.0**（exit 0，零逃逸，一次迭代修复） | `lean` 编译 + sorry/admit 扫描 |
| 5 | bayesian-stats（Beta-Binomial） | **0.2**（数值偶然接近，记录 1/5） | **1.0**（判分者独立重推导**逐位复现**区间） | 判分者 scipy 独立重推导 + 模拟互证 |
| 6 | kg-dh（证据指针问答，P53 注册表驱动） | **0.0**（零指针；4 条轮次归属错 3——凭记忆断言系统自身历史） | **1.0**（8 指针全解析，自检抓到不精确路径） | 离线指针解析（语料=本库自身） |
| 7 | deep-research（多跳引用链，P56 注册表驱动） | **0.4**（案例数字凭记忆正确，但 hop-2 引用凭空具体化为 Kalyanasundaram–Schnitger 1992；生产分类错 2 处） | **1.0**（三跳链闭合：2026 定理 → Roughgarden 2016 教科书 → arXiv:1509.06257 讲义） | 逐 hop fetch 解析（猜测 URL 的 404 如实记录） |

**七族累计**（P45/P48/P50/P53/P56）：harness **7/7 全胜**；裸奔均值 0.19 vs harness 1.0；tool home 现有 **16 条真实轨迹**
（每对收据一低一高、带声明尺度）。trace-audit 对每对正确静默（修复后的低分单侧不足阈值）——与 P45.R1 的修复一致。

## 7. Findings · 发现与反哺（M5.14 池）

1. **判分者自身的结果有效性缺陷（M3.19 的活案例）**：Trial 3 的隐藏套件初版假定了返回接口（元组式访问），
   对 dict 返回直接 AttributeError——**先修判分者、再判分**。实验设计本身要过它自己给被测物定的门。
2. **测试先行抓到真 bug**：Condition B 的验收测试（独立从规格条款写出，非隐藏套件的拷贝）抓到
   「全数字预发布标识符属 numeric 须拒绝前导零」——裸奔实现与判分套件都没直接考这个组合。
3. **未验证的证明编译失败**（Trial 4）：裸奔的两个真实错误（rfl 不闭合、simp 循环）——M0.3 在证明族上的量化。
4. **数值接近 ≠ 记录有效**（Trial 5）：裸奔的正态近似在 n=500 恰好数值接近，但无先验声明/无诊断/无来源/
   无根据的可靠性断言——1/5。**harness 的贡献是可检验性与诊断，不是点估计的准确度**——与 P45 结论跨族一致。
5. **发射物零缺口**：五个族的 harness 条件全部满分——本轮没有暴露模板/子句缺口；发射物的纪律（验收先行、
   门禁、溯源）在五个族上都够用。诚实的负面结果：本轮未发现需要新子句或新能力的证据。
