# Self-model, gap awareness & bounded exploration · 自我模型·缺口意识·有界探索

> What an agent can reliably know about itself, how to find its own gaps, and how to explore without fooling itself.
> 自己能知道什么、如何找到自己的缺口、以及怎样不自我欺骗地探索。
**Updated:** 2026-10-20

## 0. The asymmetry this doc is built on

A harness that claims a strength has produced **testimony**, not evidence. A harness that runs a task it has never run has
produced **evidence**, not a claim. Everything below follows from that asymmetry: self-report is cheap and systematically
optimistic; an external check is expensive and decisive. The purpose of a **self-model** is therefore not to *assert*
capability but to *index* it — each entry points at the artefact that would disprove it.

This doc grounds **M5.11** and the capability `gap-seeking`. It deliberately does **not** restate M5.1–M5.10 (the
signal → audit → mutation → journal loop, and the round contract); those already exist. What is missing is the thing the
loop *assumes*: a way to know what is not covered.

---

## 1. Classic foundations (named, not re-read)

Metacognition research separates **monitoring** ("do I know this?") from **control** ("what do I do about it") — the same
split a harness needs between a self-model and a decision rule. The canonical sources (Flavell 1979; Nelson & Narens 1990)
are **not entered** in `review/references.md` because no first-party record was reachable this session; they are named here
so the lineage is honest, and **no rule below rests on them**. The empirically load-bearing part is §2, which is verified.

Two classic findings do transfer, and they are the reason this is a *gate* rather than a vibe:

- **Calibration and discrimination are different skills.** A system can be accurate on average and useless as a guide to
  its own reliability.
- **Confidence is a report, not a measurement.** Asking for it changes nothing unless it is scored against outcomes.

---

## 2. What models can and cannot know about themselves

| Finding | Source | Consequence for a harness |
|---|---|---|
| Self-correction **without external feedback** does not reliably improve reasoning, and can degrade it | R201 (`arXiv:2310.01798`) | "Review your own answer" is not a verification step. Only a criterion, instrument or fresh reader counts (M3.2, M3.9). |
| Modern networks are **poorly calibrated**; confidence needs recalibration to be usable | R202 (`arXiv:1706.04599`) | A stated probability is not a probability until it is scored. Track calibration or ignore the number. |
| Models **partly** know what they know — and the boundary is uneven | R203 (`arXiv:2207.05221`) | Self-knowledge is a weak prior, useful for triage, never for sign-off. |
| Ask a model what it does **not** know and you get a usable but incomplete map | R204 (`arXiv:2305.18153`) | "Known unknowns" can be elicited cheaply; "unknown unknowns" cannot (see §3). |
| Introspection recovers **some** facts about the model, not all | R205 (`arXiv:2410.13787`) | An introspective claim is a hypothesis to test against behaviour. |
| Self-feedback loops (Reflexion) help **with** a task signal, and drift without one | R206 (`arXiv:2303.11366`) | Bound the loop and attach an external criterion (cf. M3.7). |
| Sampling agreement (self-consistency) is a cheap **uncertainty signal** | R207 (`arXiv:2203.11171`) | Use disagreement to *route* to a check, not to conclude correctness. |

**Working rule.** A self-attributed strength is admissible only if it is paired with an **external** check: a test that
fails when the capability is removed, a measured run on data the harness was not tuned on, or a first-party record. This is
the same standard M5.1 already sets for mutations ("no metric, no promotion") — applied to *claims about the harness itself*.

---

## 3. Finding the gap

There are two kinds of gap, and they need different machinery.

**Known gaps (a register).** `harness cycle audit` already reports a gap surface — missing router rows, provenance rows,
guards, and clauses referenced but never anchored. That surface is mechanical and reliable *within its own definition*. It
is also **bounded by what the registry can express**: it cannot see a direction nobody registered. So the register needs a
second half — the **roadmap** entries that record deliberate non-additions with a reason and a revisit trigger (M5.10).

**Unknown gaps (the harder kind).** Three cheap instruments, in increasing cost:

1. **Disconfirming check.** Pick a claimed strength and try to *falsify* it, on purpose, once per round. Not "test the
   feature" — try to make it fail. A strength that has never been attacked is an assumption.
2. **Error-taxonomy mining.** Cluster real failures by *mechanism*, not by surface symptom. Two bugs with the same cause are
   one gap; ten symptoms with ten causes are ten.
3. **Holdout pressure.** Every new capability is measured on tasks it was not built from (M5.3). If the holdout never
   surprises you, it is not a holdout — it is a regression test.

**The measurement trap.** Gap metrics are **proxies**, and proxies get gamed (R216, `arXiv:1803.04585`). "More capabilities",
"more tests", "more sources" are all counts that can rise while quality falls. The guard is the one M5 already uses: a
capability is claimed only when it changes an outcome on a task the harness did **not** choose to make itself look good on.

---

## 4. Exploring without self-deception

Open-ended search has a long, honest literature, and its central lesson is uncomfortable: **novelty is not value.**

| Mechanism | Source | What it actually gives you |
|---|---|---|
| Quality-diversity (MAP-Elites) | R208 (`arXiv:1504.04909`) | Keeps a *diverse* set of good solutions instead of one optimum — the right shape for exploring "directions" rather than "answers". |
| POET | R209 (`arXiv:1901.01753`) | Co-evolves tasks and solutions; new tasks are generated *because* they are learnable-but-not-solved. |
| OMNI | R210 (`arXiv:2306.01711`) | Uses a model of "interestingness" to steer search — and makes the model of interestingness an explicit, attackable object. |
| Compression progress | R211 | A direction is interesting when it yields *learnable* structure, not when it is merely unfamiliar. |
| Bandits / expected value of information | R217 | Formalises "which question is worth the next unit of budget" — the only principled answer to "what should we explore next?". |

**Rule for this library.** An uncovered direction enters as a **candidate**, never as a capability. It must pass the round's
definition-of-done (M5.10) like any other: a clause, a discriminator the engine can evaluate, a guard, provenance, a router
row, reachability. Exploration changes *what is on the list*; it does not change *what counts as done*.

**Bound the exploration.** A holdout, a budget, and a written stop condition. Unbounded exploration is how a self-improving
system acquires scope it cannot verify — the failure mode M5 already names as misevolution.

---

## 5. The self-improvement frontier, read sceptically

| Work | Source | Honest reading |
|---|---|---|
| AI Scientist | R212 (`arXiv:2408.06292`) | An **automated research loop** (idea → experiment → write-up), evaluated with a model-based reviewer. Impressive as a loop; its quality claims inherit the reviewer's weaknesses. |
| Darwin Gödel Machine | R213 (`arXiv:2505.22954`) | Self-modifying agents kept in an **archive** and selected empirically — i.e. self-improvement implemented as *search plus evaluation*, not as introspection. |
| STOP | R214 (`arXiv:2310.02304`) | Recursive self-improvement of *code*, with the search space bounded by a scaffold; the gains are search gains. |
| Self-taught evaluators | R215 (`arXiv:2408.02666`) | Judgement can be bootstrapped without human labels — but bootstrapped judges inherit the generator's blind spots. |
| AlphaEvolve | R218 | A first-party announcement (not peer-reviewed) of evolutionary search over code with automated evaluators. Treat as a strong demo, not as evidence about general self-improvement. |

**Synthesis.** Almost every "self-improving agent" result is **search + a trusted evaluator**. The evaluator is where the
truth lives. A harness that wants to improve should invest in *evaluation* and *provenance*, not in introspection — which is
exactly where M3 (gates) and M4 (integrity) already point.

---

## 6. What a harness should actually do

1. **Keep a self-model artefact** (`self-standard.md` already is one). Each claimed strength names its **evidence**: a guard
   test, a shipped file, a measured run. No evidence, no claim.
2. **Keep the gap register in two halves** — the `cycle audit` surface (mechanical) *and* roadmap entries with reasons and
   revisit triggers (deliberate). The first is a bug list; the second is a decision log.
3. **Run one disconfirming check per round.** Choose a claimed strength; try to break it. Record the result either way.
4. **Route disagreement, don't average it.** When self-assessment and an external check disagree, the external check wins;
   the disagreement itself is a calibration data point (R207).
5. **Bound exploration** — budget, holdout, stop condition — and let candidates enter only through the round gate.
6. **Never let a self-report sign off.** Self-attributed strength is a hypothesis (R201, R205).

---

## 7. Deliberate non-additions & honest limits

- **No "consciousness"/"self-awareness" claim.** This is engineering: an index of coverage plus a falsification habit. The
  word "self-aware" is avoided deliberately.
- **No new introspection mechanism.** The reliable path is external checks; adding a "reflect deeply" step would be the very
  failure R201 documents.
- **No unbounded autonomy.** Exploration is budgeted and human-gated (M0.8); the doc does not authorise unattended
  self-modification.
- **No claim that the classic metacognition literature was re-read.** It was not (§1).
- **Gap metrics are proxies.** Counts of capabilities, tests or sources can all rise while quality falls (R216); the only
  defence is outcome measurement on tasks the harness did not design for itself.

---

## 中文

**本文的支点是一个不对称：** 声称自己有某种能力，只是**证词**；真去跑一个从没跑过的任务，才是**证据**。自我报告便宜且系统性乐观，外部检验昂贵但决定性。
所以**自我模型**的用途不是"宣称能力"，而是**索引能力**——每一条都要指向一个能证伪它的产物（守卫测试、已交付文件、实测运行）。

**三条已验证的边界。** ① 无外部反馈的"自我纠错"不可靠，甚至会变差（R201）——"你再检查一遍"不是验证步骤；② 现代网络校准很差（R202），
说出的概率在被打分之前不算概率；③ 模型**部分**知道自己的知识边界（R203/R204），内省只能取回**部分**事实（R205）。故：自评只能用于分诊，不能用于签核。

**缺口的两种。** **已知缺口**= 登记册（`cycle audit` 的缺口面 + 带理由与重访触发的路线图条目）；**未知缺口**靠三件便宜仪器：**反证检查**
（每轮挑一个自称的强项，故意去打碎它）、**错误分类学**（按机制聚类，不按症状）、**留出集压力**（若留出集从不让你意外，它就不是留出集）。

**探索的铁律：新颖不等于价值。** 质量-多样性（MAP-Elites）、POET、OMNI、压缩进展、以及"信息期望价值"都指向同一件事：一条未覆盖的方向只能作为**候选**进入，
必须照常通过轮次的完成定义（M5.10）。**有界**：预算、留出集、书面停止条件。无界探索正是 M5 所说的"误演化"。

**对前沿的冷静读法。** 几乎所有"自我改进 agent"的成果，实质是**搜索 + 一个可信的评估器**；真相在评估器里。所以要把钱花在**评估与溯源**上，而不是内省——
这正好指向 M3（门禁）与 M4（诚信）。

**有意不新增。** 不作"意识/自我觉知"的宣称（这是工程：覆盖索引 + 证伪习惯）；不新增"深度反思"步骤（那正是 R201 记录的失败）；不授权无人值守的自我修改；
不声称重读过经典元认知文献；不把"能力数/测试数/来源数"当质量——它们都能在质量下降时继续上升（R216）。
