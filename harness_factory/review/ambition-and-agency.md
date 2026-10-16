# Ambition & agency · 野心与主动性（文学/实践综合）

> Distilled from Felix Rieseberg's *How to be more ambitious* (2026) and adjacent sources, mapped onto
> the harness-factory capability system. Answers: **how much of it can become a harness capability?**
> 从 F. Rieseberg《How to be more ambitious》(2026) 及相邻来源提炼，映射到本仓库能力体系，回答：**其中有多少能变成 harness 能力？**

**Updated:** 2026-10-16 · Access date 2026-10-16. Refs: [`references.md`](references.md) R80–R83.

---

## 中文速览

Rieseberg 把「用模型做得更多」拆成四种野心：**Speed（更快）· Altitude（更高）· Depth（更深）· Range（更广）**。其中 **Speed** 本仓库已覆盖（M1 上下文、M6 工具、最小高信噪）；真正的**缺口**是 **Altitude（把目标定得更高、先拔高再收敛）** 与部分 **Depth（坚持用本领域顶尖真正用的工具、用「外部裁判」而非自评）** 与 **Range（换词性、组多学科班底去「做」而不是「演」）**。**结论：四轴中约 60% 已在本仓库可表达；新增 3 条能力（`ambition-elevation`、`expert-instruments`、`cross-field-crew`）即可把缺口补上**，且**无需改代码**（能力是数据驱动的）。另新增 `reference/requirement-refinement.md` 把「先拔高再收敛」落成可执行协议。场外佐证：Locke & Latham 的目标设定理论（具体且有难度的目标 > 「尽力而为」）为「提升野心」提供了实证根基。

---

## 1. The source · 原文主张

Rieseberg [R80] argues that working with models is not about *answering faster* but about **raising the ambition of the work**. Four axes:

| axis | 中文 | core claim | representative techniques |
|---|---|---|---|
| **Speed** | 更快 | same work, less time | automate busywork (the default baseline) |
| **Altitude** | 更高 | go up an abstraction level; consider the **outcome beyond the task** ("what do you want to happen next?") | give the model the *environment* (logs, machines, app-version→commit map) so it can verify and remove the human from the loop |
| **Depth** | 更深 | make the model use the instruments of the **best professionals in the field** | insist on the real instrument (DB + statistical models, not a markdown table); pick unreasonable targets and call them reasonable; adversarially challenge your own assumptions from raw data; produce new knowledge (simulate, find the earliest signal, validate on unseen data); **use an outside judge** — never let the model grade itself — ideally a tool it can run for immediate feedback |
| **Range** | 更广 | consider the work from other fields' perspectives | assemble a diverse crew (analyst, journalist, editor, red-team like a short-seller / forensic accountant); **replace nouns with verbs** ("a deck" → "getting busy people to believe a story about cause and effect, and to decide under uncertainty, in 30 minutes"); and *do* what a short-seller does, not *write like* one |

The article's leverage is a **prompt to elevate**: ask the four "deeper version" questions (what would a top practitioner do that I'm not asking for · what rawest material would they start from · which specific methods/tools · what other than you or me would show it's right), then rewrite the ask.

## 2. Mapping to the capability system · 映射与判定

| source technique | axis | existing module / capability | verdict |
|---|---|---|---|
| Curate minimal context; automate busywork | Speed | `M1` (M0.6), `tool-use` (M6) | **covered** |
| Give the model the environment so it can verify (logs, machines, repro) | Altitude | `M2`/`M5` (long-lived loops), `sandboxed-execution` (M3/M6/M7) | **partial** — the *environment* is covered; the *intent to raise the target* is not |
| Consider the outcome beyond the task; raise the goal | Altitude | — | **gap → `ambition-elevation`** |
| Insist on the field's real instruments (no toy substitutes) | Depth | `M6` tools, `M4` grounding | **partial** — tooling exists; the *standard of instrument* is implicit |
| Adversarially challenge assumptions from raw data | Depth | `M3` (verify the verifier), `M4` | **partial** |
| Use an **outside judge**, not self-grading | Depth | `M3` (separate builder/critic; default-FAIL) | **covered** — M3 is exactly this |
| Schedule harder targets / "unreasonable, called reasonable" | Altitude/Depth | `frontier-standard`, `domains/excellence/standard-ladder.md` | **partial** — measures against best-known, but only for excellence/high-verifiability tasks |
| Reframe nouns as verbs; diverse crew; do (not role-play) | Range | `M8` collaboration, `M6` subagents | **gap → `cross-field-crew`** |
| Outside validation as a runnable tool (immediate feedback) | Depth | `M3`, `M6` | **partial → `expert-instruments`** |

Aggregate: of the article's moves, **~60% are already expressible** in M0–M8; the remaining ~40% cleanly collapse into **three data-driven capabilities** plus one protocol.

## 3. What was integrated · 已整合

Added to `data/capabilities.json` (no code change — the capability map is data-driven):

| capability | axis | fires when | modules |
|---|---|---|---|
| `ambition-elevation` | Altitude | horizon ≥ session | M0, M3, M8 |
| `expert-instruments` | Depth | verifiability = high **or** horizon ≥ multi_session | M3, M4, M6 |
| `cross-field-crew` | Range | collaboration = multi_agent **or** horizon = long_running | M6, M8 |

Plus `reference/requirement-refinement.md` (the six-step R0–R5 protocol: restate → elevate → classify constraints → offer candidates → confirm → converge) which turns "raise ambition" into an *executable, interruptible, human-confirmed* step.

## 4. Adjacent evidence · 相邻佐证

- **Goal-setting theory (empirical anchor).** Locke & Latham [R81], [R82]: across hundreds of studies, **specific and sufficiently challenging** goals yield higher performance than easy goals or "do your best". This is the psychological grounding for "elevate then converge" — and a caution: goals must be *accepted* and paired with *feedback*, or elevation becomes demotivation.
| citation | what it adds | status |
|---|---|---|
| [R81] Locke & Latham, *Goal setting and task performance 1969–1980*, Psych. Bulletin 90(1), 1981, DOI 10.1037/0033-2909.90.1.125 | specific + challenging goals > "do your best"; feedback & commitment are moderators | primary (verified) |
| [R82] Locke & Latham, "Building a practically useful theory of goal setting," *American Psychologist* 57(9), 2002, DOI 10.1037/0003-066X.57.9.705 | 35-year summary; self-efficacy & goal commitment moderate the effect | primary |
| [R83] J. Read, "When Agents Ship, the PM Job Becomes Raising Ambition," 2026-09-03 | practitioner framing: once the agent meets the brief, the brief is no longer the right goal; make "raise the target" a *recurring* step | secondary / commentary (unverified claims marked) |

> **Honesty note.** R80 was fetched and read in full (2026-10-16). R81/R82 are verified via their publisher DOIs/abstracts. R83 is an opinion article — treat its claims as *commentary*, not findings (M0.2).

## 4b. Boundaries · 不整合的部分

- **"Unreasonable targets" as a standing rule** is rejected: it conflicts with M0.3 (tests before work) and can drive reward-hacking-style over-claiming. Kept only as an *Elevated candidate* the human must accept.
- **Persona role-play** is rejected (Rieseberg's own warning): the crew is told to *do* the discipline's work, not *perform* it. Personas here change method/standard, never facts (M0.4).
- **Auto-merging** any of this into the catalogue is rejected: proposals only (M0.4/M0.8) — see `reference/capability-flow.md`.

## 5. Verification · 验证

- New capabilities fire correctly: `python -m unittest discover -s tests` (capability tests in `tests/test_agent_mode.py`).
- `CAPABILITIES.md` regenerated from the SSOT (`harness capabilities --write`) and guarded for drift by the suite.
- The protocol is a *document* (L0, read-and-reason) + template hooks; it adds no executable path, so it cannot fabricate task content.

## References · 参考文献

- [R80] F. Rieseberg, "How to be more ambitious: A tutorial for humans with models," Oct. 13, 2026. https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/ (accessed 2026-10-16).
- [R81] E. A. Locke, K. N. Shaw, L. M. Saari, G. P. Latham, "Goal setting and task performance: 1969–1980," *Psychological Bulletin*, 90(1):125–152, 1981. DOI: 10.1037/0033-2909.90.1.125.
- [R82] G. P. Latham, E. A. Locke, "Building a practically useful theory of goal setting and task motivation: A 35-year odyssey," *American Psychologist*, 57(9):705–717, 2002. DOI: 10.1037/0003-066X.57.9.705.
- [R83] J. Read, "When Agents Ship, the PM Job Becomes Raising Ambition," Sep. 3, 2026. https://drjoshuaread.com/pm-job-raising-the-next-request/ (accessed 2026-10-16) — *commentary*.

See [`references.md`](references.md) for the consolidated list and [`../sources/source-map.md`](../sources/source-map.md) for the distillation trace.
