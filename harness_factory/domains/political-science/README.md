# Political science · 政治学域

> Wiring `core/` modules into political-science work: concept definition first, method declared, case selection honest.
> 把 `core/` 模块接线成「概念先行、方法声明、案例选择留痕」的政治学工作流。

**Updated:** 2026-10-23 · **Faculty:** social-sciences · **Artifact:** document · **Grounding:** required

---

## 中文速览

政治学域的承重墙是**概念与方法的显式化**：L0 界定问题与关键概念 → L1 **声明方法与假设**（M3.13，methodology-map 行）→ L2 案例/数据选择**规则先行** → L3 模型点名（理性选择 / 制度主义 / 历史制度主义）→ L4 检验反假设 → L5 带**适用条件**写作。域特有风险：**概念漂移**（同一术语前后不同义）、**选择偏差隐身**（案例因结论而选）、**把相关性当因果**、**规范性主张冒充实证结论**。

## Wiring · 接线

| Level | Move | Modules | Gate |
|---|---|---|---|
| L0 | Define the question and the key concepts | M7 | 每个承重概念首现即定义（M4.15） |
| L1 | Declare the method and its assumptions | M3.13 | 方法 + 假设 + 报告规范点名（methodology-map） |
| L2 | Select cases or data with the rule stated | M3, M4 | 选择规则先于选择结果；被排除案例留痕 |
| L3 | Analyze with the model named | M3 | 模型（rational choice / institutional / historical）显式 |
| L4 | Check the counter-hypothesis | M3 | 反假设检验，不是只找支持证据 |
| L5 | Write with scope conditions declared | M7, M4.10 | 结论带适用边界；规范主张与实证主张分行 |

## Risks · 域特有风险

- **Concept drift** — the same term means different things in the question and the conclusion.
- **Selection on the dependent variable** — cases chosen because of the outcome; the selection rule must be written before the choice (M4.11's schema-before-extraction discipline).
- **Correlation as causation** — a mechanism must be named, not implied (M3.13's inferential frame).
- **Normative smuggling** — a value judgment reported as an empirical finding.

## Rubric · 评分

`data/rubrics.json` `political-science`（概念界定 0.25 · 方法声明 0.2 · 比较严谨 0.2 · 案例选择 0.15 · 校准 0.1 · 清晰 0.1）。`harness standard --domain political-science` 可跑。

## Outlets · 信息源

一手文献与数据：APSA 系期刊（APS journals 已在 outlets）· 选举与制度数据集以 ICPSR / 官方统计登记处为起点；中国研究先看 CNKI / Wanfang。检索前读 `outlet-map.md` 各条 `not_for`。

## See also · 另见

`../domains/economics-finance/README.md`（理性选择的相邻域）· `../reference/methodology-map.md`（理性选择/制度主义行）· `../core/03-long-running-agents.md`（长时程数据集工作）· `../reference/evidence-instruments.md`（因果与统计工具）。
