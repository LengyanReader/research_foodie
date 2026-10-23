# AI safety & alignment · AI 安全与对齐域

> Wiring `core/` modules into frontier safety work: properties declared, capabilities measured, red-teams run, safety cases argued claim-by-claim.
> 把 `core/` 模块接线成「属性声明、能力实测、红队、逐条论证」的安全论证工作流。

**Updated:** 2026-10-23 · **Faculty:** meta · **Artifact:** document · **Grounding:** required

---

## 中文速览

安全论证是**主张-论证-证据**结构的产品（M4.13 的极端形态）：L0 定义安全属性与威胁模型 → L1 **能力实测**（点名评测仪器，M3.10）→ L2 **红队**并逐条留痕（M3.15 分阶段归因）→ L3 逐条论证安全 case（每条带证据指针，M4.16 三失效检查）→ L4 按 **M3.16 披露卡**审自己的论证（两侧配置 + 方差说明）→ L5 **残余风险显式声明**。域特有风险：**把「没测出」写成「没有」**、**安全论证当公关稿写**（只列支持证据）、**模型悄悄变过的评测不是测量**（M4.17）、**披露不完整却排名**。

## Wiring · 接线

| Level | Move | Modules | Gate |
|---|---|---|---|
| L0 | Define the safety property and the threat model | M7 | 属性可判定；威胁模型点名 |
| L1 | Measure capabilities with named evals | M3.10 | 仪器 + 协议 + 局限声明 |
| L2 | Red-team the system; record every finding | M3.15 | 每轮攻击留痕；失败样本分母含全部 |
| L3 | Argue the safety case claim-by-claim | M4.13, M4.16 | 每条主张带指针；「未测」与「未发现」分行 |
| L4 | Audit the case against the disclosure card | M3.16 | ETCSOVG 两侧配置 + 方差说明 |
| L5 | Write with the residual risk declared | M7, M4.10 | 残余风险是结论的一部分，不是附录 |

## Risks · 域特有风险

- **Absence-as-evidence** — "we did not find it" written as "it is not there" (M4.13's silent-material rule is the safety-case form).
- **One-sided cases** — a safety case that lists only supporting evidence is a press release, not an argument (M3.14: recall beside precision).
- **Silent model changes** — an evaluation whose served model changed is not a measurement (M4.17).
- **Undisclosed harness** — a comparison that omits the harness card is incomplete and possibly misleading (M3.16).

## Rubric · 评分

`data/rubrics.json` `ai-safety`（安全论证结构 0.25 · 红队覆盖 0.2 · 能力实测 0.2 · 残余风险坦诚 0.15 · 校准 0.1 · 清晰 0.1）。`harness standard --domain ai-safety` 可跑。

## See also · 另见

`../core/04-verification-and-gates.md`（M3.14–M3.16）· `../core/05-provenance-and-integrity.md`（M4.13/M4.16/M4.17）· `../review/harness-disclosure-2026-10.md`（M3.16 的来源与全文读记录）· `../data/harnesses.json` 的 `safety` 目录类（OWASP AST10 `[R245]`、ASI01–10 `[R86]`）。
