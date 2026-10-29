# Research ideation · AI 提出研究问题的能力评估（P51 · 用户指定入口 After42）

> **中文速览。** 用户给定入口（After42：*Can AI Propose Interesting Research Questions?*）并要求广泛深入调研。
> 三篇一手精读（After42 项目页 · Stanford 2409.04109 全文 · 两篇 listed 谱系锚）+ 既有条款映射。**裁决：新能力
> `research-question-generation`（填补 P18 记录的 plan-产物空洞），键 `artifact=plan × domain∈{research,
> deep-research}`；M5.11 深化（评判者校准的定量证据）；两篇 listed 谱系锚入册。** 同时按用户指示把真实场景模拟
> 使用升为**常设例行程序**（`tasks/BATTERY.md` + DoD 软轴 battery + 轮次契约电池步骤）。

**Updated:** 2026-10-28 · **Round:** P51 · **Evidence:** R272/R273 read in full（access 2026-10-28）；R274/R275 listed

## 1. What the three studies establish · 三项研究确立的事实

| 事实 | 来源 | 对本库的含义 |
|---|---|---|
| **解决是提问的前提**：solve-refine-critique 环把有趣占比从 3% 提到 33% | R272 | 构思不是纯生成——解题主张与失败尝试是提纯信号（M5.14 的构思版） |
| **过采样-过滤 + 显式判据**有效，但模型评审需**校准**：无判据时与人类评分一致性低于人类互评（45.0–53.3% vs 56.1%）；有判据+集成后召回 65–80%（集成 80%）——接近单个专家、**仍不可替代人类品味** | R273/R272 | M5.11 的「可信评估器」从格言变成可定量校准的义务：想法评判者须报告对专家共识的召回 |
| **新颖与可行要分开打分**：novelty 升（5.64 vs 4.84, p<0.05）、feasibility 持平，总分与可行性相关仅 r=0.097 | R273 | 单一总分掩盖 trade-off——构思产出必须双轴报告 |
| **多样性有平台期**：4000 种子 → 200 去重后唯一；同一生成器的广泛采用有**同质化**风险 | R273 | 去重率是构思环的被追踪数字；自演化环的输入多样性要显式管理 |
| **执行忠实性缺口**：执行 agent「跳过或改动基线/方法的步骤」、误定义指标——「只有结果不足以验证实现的忠实」 | R273 | M3.18(c) 重放纪律的又一独立佐证（跨两篇论文与 LHTB 收敛） |
| **行为反馈有效、声明偏好无效**（个性化） | R272 | 构思环的个性化要靠轨迹行为（本库 trace 正是行为记录），不靠问卷 |

## 2. Capability adjudication · 判别裁决（M5.10）

- **新增 `research-question-generation`**：键 `{artifact: plan}`——**填补 P18
  记录的真洞**（「plan 产物无专属能力」，重访触发为「洞被发现有实质内容可填」，本轮即该触发）。判别性：命中一切 plan 产物任务——校准义务在有专家共识处生效；普通项目规划同样拿到构思纪律（过采样/过滤/解决-提炼），这是 P18 洞的完整闭合。内容=(a)–(e) 五条纪律（见 capabilities
  why 字段）。模块 M2（solve-refine 环）· M3（评判者与门）· M4（文献包溯源）· M5（自评校准与多样性）。
- **M5.11 深化**：校准数字 + 多样性平台期 + 同质化警示（已落 core/06）。
- **刻意不加**：① 不加 `novelty-assessment` 独立能力——新颖性评估是 research-question-generation 的
  组成部分（(c)/(d)），单独成条会双触发；② 不给 AI Scientist 谱系落门禁义务——R274/R275 为 listed，
  且第三方批判评估（2502.14297）已录为警示；③ ResearchAgent（Baek et al., ACL 2025）无解析 id，按不猜规则
  只在本文件留名。

## 3. The routine · 例行机制（用户指示一）

真实场景模拟使用升为**常设程序**（不再是逐轮临时决定）：

- `tasks/BATTERY.md`——何时跑（触能力/模板/域信号的轮次；真实任务收尾；周期性）、跑什么（七族总表）、纪律
  （判据预声明 / 判分者过门 / 尺度收据 / 诚实边界 / 发现反哺）、收据流（traces → trace-audit → 提案 → 人）；
- `data/cycles.json` DoD 新增**软轴 battery**：触能力/模板/域信号的轮次必须报告重跑与收据，或说明为何不适用
  （cycle audit 可检查的登记义务，硬性=false——首次不必追溯 45 轮历史）；
- `reference/capability-cycle.md` 轮次契约补电池步骤。

## 4. Verification

`harness cycle audit` → **47 轮 · 0 硬 · 0 缺口**（新 DoD 轴通过校验）；能力 39 条（39→含新条 39？38→39）；
references **R1–R275**（§AB 四条）；路由新行；守卫见 `P51IdeationGuardTest`；测试计数见 PROGRESS。
