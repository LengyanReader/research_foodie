# Methodology map · 方法论地图

> **What this is.** `core/04` (M3.13) says *declare the method, its assumptions, and where it stops being valid*.
> This is the field-by-field map: **field → methodology system(s) → canonical source → what the method demands
> → which module / capability / gate enforces it in this factory.** Load it whenever work follows (or claims to
> follow) a named method — a systematic review, a causal design, a qualitative coding, a design-science study,
> an experiment. · 本文把 **M3.13** 落地：**领域 → 方法论体系 → 一手来源 → 该方法的要求 → 本工厂由哪个模块/能力/门禁执行**。
> 凡是套用命名方法（综述、因果设计、质性编码、设计科学、实验设计）的任务，都按本表核对。
> Same paths as every factory doc — these are **the harness-factory's** files, not your project's.

**Updated:** 2026-10-18 · Load via `harness skill methodology-map`. Sources: `review/references.md` §H–§J. Companion: `reference/evidence-instruments.md` (M3.10 — what *observes*); this doc answers *what procedure licenses the inference* (M3.13).

---

## 中文速览

**方法 ≠ 方法名。** 说「我做了系统性综述 / 双重差分 / 扎根理论 / 设计科学」不等于完成了这些方法：每种方法都自带**协议、假设、报告规范**三件套。本文给出每个领域的**方法论体系 → 其要求 → 由谁执行**的对照表。用法：命中你的方法所在行 → 检查三件套是否齐 → 缺哪件就补哪件（协议先注册、假设先声明、报告按规范）。**通用规则**：任何命名方法都必须写明 (a) 协议/注册，(b) 假设与失效边界，(c) 该领域的报告标准；探证性(exploratory)与验证性(confirmatory)必须分清。若某方法本仓库尚无专章，表中标注 **status**，并说明「差什么才算判别性」。

---

## How to use · 用法

1. **Name the method**, not the field. "a systematic review" and "a qualitative interview study" are different methods even in one field.
2. **Read the row's three columns**: *demands* (what the method requires), *enforced by* (the module/capability/gate that makes it real here), *check first* (the most-skipped item).
3. **Where `status = later`**, treat the row as a checklist to honour, not a machine gate — and do not claim the factory enforces it.
4. Methodology is **invariant-layer** (M3.13), not a capability: it would fire on almost everything, so a `methodology-fit` capability would not discriminate. Recorded as a deliberate non-addition in `review/integration-map-2026-10.md`.

> Rule of thumb: **a method is a contract with reality about what you did not choose.** The protocol, the assumptions, and the reporting standard are exactly the parts you cannot improvise after seeing the result.

---

## The map · 映射表

| Field(s) · 领域 | Methodology system · 方法论体系 | Canonical source · 一手来源 | What it demands · 要求 | Enforced by · 本仓库执行者 | Status · 状态 |
|---|---|---|---|---|---|
| all empirical fields · 所有实证领域 | Scientific method: hypothesis → design → test → revise; reproducibility | Popper; Munafò *et al.*, reproducibility manifesto | Pre-specified analysis path; analysis code + data available; exploratory vs confirmatory labelled | M3 (gates), M4 (provenance), `empirical-measurement`, `[R103]` | **done** |
| statistics · 统计 | Bayesian workflow (prior → model → compute → validate → compare → revise) | Gelman *et al.*, *Bayesian Workflow*, `[R111]` | Declared frame; priors & likelihood stated; convergence (R-hat / ESS); *iterative* model checking & prior sensitivity | **`statistical-inference`** (M3, M4); M3.11 | **done** |
| statistics · 统计 | Frequentist design: power, pre-registration, multiplicity control | standard (Fisher/Neyman-Pearson); pre-registration (`[R110]`) | Analysis plan fixed before data; power/α/多重要控制; effect size + interval, not p alone | `statistical-inference`, `empirical-measurement` | **done** |
| causal inference · 因果推断 | Potential outcomes + identification (back-door, IV, DiD, RD, placebo) | Rubin / Pearl; `dowhy` docs (`[R111]`-adjacent) | Identification **assumption** named and defended; falsification/sensitivity check; separation of identification from estimation | `empirical-measurement` (M3, M4); `reference/evidence-instruments.md` §Statistical estimates & causal claims | **done** |
| medicine / health · 医学健康 | Systematic review & meta-analysis: PRISMA 2020 | Page *et al.*, PRISMA 2020, `[R115]` | Registered protocol; documented search string; screening + risk-of-bias; PRISMA flow | M3, M4; `deep-research`, `osf` | **done (prose gate)** |
| medicine / health · 医学健康 | Certainty of evidence: GRADE | GRADE Handbook, `[R116]` | Rate certainty (high→very low) via risk of bias, inconsistency, indirectness, imprecision, publication bias | M3; methodology row | **done (prose gate)** |
| medicine / health · 医学健康 | Trial reporting: CONSORT 2010 | Schulz *et al.*, CONSORT 2010, `[R117]` | Randomisation, allocation concealment, blinding, participant flow reported | M3, M4 | **done (prose gate)** |
| social science · 社会科学 | Qualitative traditions: grounded theory | Glaser & Strauss, *Discovery of Grounded Theory*, `[R119]` | Open→axial coding, constant comparison, **memoing**, theoretical saturation; codebook + double-coding | M3 (successor-proxy of the linguistic agreement gate); M4 | **next** (no qualitative capability yet) |
| social science / education · 社科教育 | Mixed methods; survey methodology (sampling frames, validity) | standard (Creswell; AAPOR) | Sampling frame stated; validity/reliability of instruments; integration of strands | `empirical-measurement` | **later** |
| engineering / information systems · 工程与信息系统 | Design science research (build-and-evaluate) | Hevner *et al.*, MIS Quarterly 28(1), `[R118]` | A designed artefact; a stated design problem; evaluation against explicit criteria; contribution articulated | M3, M4; `software-engineering`/`engineering` | **done (prose gate)** |
| engineering / natural sciences · 工程与自然科学 | Design of experiments: randomisation, blocking, factorial | standard (Fisher; Box–Hunter–Hunter) | Randomisation + blocking declared; factorial structure; pre-specified responses | `dimensional-analysis`, `empirical-measurement` | **next** |
| software / devops · 软件与运维 | Empirical SE: controlled/observational studies, benchmark protocols, ablation | standard (empirical SE community) | Benchmark + baseline + ablation; threat-to-validity section; re-runnable pipeline | `eval-driven-development`, `reproducible-experiments` | **done** |
| formal sciences · 形式科学 | Proof methodology: state the language & axioms; checked derivation; counterexample search | mathlib/Lean (`[R98]`/`[R99]`), Open Logic (`[R100]`) | No unclosed goal; statement reviewed by a human; SAT/SMT/CA counterexample attempt; exact/certified computation | `formal-verification`, `certified-computation` (M3.12) | **done** |
| natural sciences (physics/chemistry/… ) · 自然科学 | Measurement framework: GUM; V&V for models | JCGM 100 (`[R107]`), NASA-STD-7009 (`[R108]`) | Uncertainty budget with coverage factor; V&V/UQ for simulations; SI units | `dimensional-analysis`; M3.10 | **done** |
| earth / life sciences · 地学生命 | Field & lab protocols; instrument calibration; blinded scoring | standard (FAIR, MIAPPE/… domain norms) | Protocol + calibration record; blinding where relevant; FAIR data | M4, M6; `reproducible-experiments` | **next** |
| humanities · 人文学科 | Source criticism; close reading; philology; hermeneutics | standard (documentary-edition norms) | Provenance & dating of every cited source; competing readings considered; editorial principles stated | M4; `humanities`/`writing` | **done (prose gate)** |
| law · 法学 | Doctrinal method; comparative method; case analysis | standard (legal methodology) | Primary sources (statutes/cases) as authority; jurisdiction fixed; counter-authority addressed | M4; `law` | **done (prose gate)** |
| writing · 写作 | Argumentation & IMRaD/reporting structure | standard academic writing norms | Claim↔evidence mapping; structure by genre; citation to primary sources | M4; `writing`, `traceable-sources` | **done** |
| frontier AI evaluation · AI 评测 | Model/harness evaluation methodology: held-out sets, freezing, contamination control | `[R92]`, `eval-driven-development` | Golden set frozen before change; contamination checked; step/trajectory-level scoring | `eval-driven-development` | **done** |

---

## The three-part contract · 方法的三件套

For **any** named method, M3.13 asks three questions — missing any one turns the method into decoration:

1. **Protocol / registration.** What was fixed *before* seeing the data (search string, analysis plan, coding frame, design matrix, identification strategy)? Where is it recorded?
2. **Assumptions & validity boundary.** Under what conditions does the method's inference hold, and where does it break? (Independence, no-unmeasured-confounding, saturation, factorial additivity, closed-world of the formalisation.)
3. **Reporting standard.** Which field standard does the write-up follow, and which required items are genuinely *not* met (declared, not hidden)?

> 三件套缺一即为装饰：**先注册的协议**、**假设与失效边界**、**该领域的报告规范**。探证性与验证性必须分清；偏离注册处须写明并注明日期。

---

## Deliberate non-additions · 有意不新增

- **No `methodology-fit` capability.** It would fire on nearly every task (any empirical or qualitative work has a method), so it would not discriminate — the invariant lives in **M3.13** + this map instead. A capability that never discriminates is documentation, not a mechanism.
- **No methodology "instrument" catalog entries** for PRISMA/GRADE/CONSORT/DiD/grounded-theory *as tools*: they are protocols/norms, not installable instruments. They live as references (`[R115]`–`[R119]`) and gate text. The one place a method *does* have a tool (`dowhy` for identification) is catalogued as an instrument.
- **No per-field methodology READMEs yet.** The map is the single surface; per-field READMEs would duplicate it. Extending the *domains in scope* (statistics, geometry-topology) with methodology lines is done; the rest stay `status = next/later` here.

---

## See also · 另见

- `core/04-verification-and-gates.md` — M3.13 (declare the method) and the checklist.
- `reference/evidence-instruments.md` — the companion map (claim → instrument → tool → gate evidence; M3.10–M3.12).
- `reference/capability-router.md` — the situation → capability → file entry.
- `review/integration-map-2026-10.md` — what is integrated, what is next, and what is deliberately out of scope.
