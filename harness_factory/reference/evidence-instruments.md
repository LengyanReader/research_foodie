# Evidence instruments · 证据仪器表

> **What this is.** `core/04` (M3.10) says *match the instrument to the claim*. This is the concrete
> map: **claim type → instrument → catalogued tool → the evidence the gate must observe**. Load it
> whenever a deliverable asserts something stronger than "I read it somewhere". · 本文把 **M3.10** 落地：
> **命题类型 → 仪器 → 目录中的工具 → 门禁必须看到的证据**。凡是超出「我读到过」的断言，都按本表选仪器。
> Same paths as every factory doc — these are **the harness-factory's** files, not your project's.

**Updated:** 2026-10-18 · Load via `harness skill evidence-instruments`. Machine-readable truth: `data/harnesses.json` (class `instruments`). Sources: `review/references.md` §G–§H.

---

## 中文速览

三类命题要三样东西：**形式命题**（定义、定理、协议性质、程序正确性）靠**机器检查的推导**；**物理量**靠**单位 + 传播的不确定度**；**经验命题**（心理/认知/医学/社科/教育/经济）靠**效应量 + 区间 + 可靠性**，且分析须**先注册**。语言类数据另加**标注者一致性**与**许可/知情同意**。仪器目录（27 件，12 个工具族）是本仓库 SSOT 的一部分；**声明仪器就是声明可反驳性**——说不出仪器，就等于没验证。

---

## How to use · 用法

1. **Name the claim**, not the topic. "The cache is linearisable" and "the effect is large" need different instruments.
2. **Pick the row** below; open the cited catalog entries (`harness catalog search <name>`, or `review/harness-index.md`).
3. **State the instrument's limits** in the deliverable (toolchain version, tolerance, sample size, assumption). An instrument with hidden limits is a false gate.
4. **Observed evidence only.** "I ran it" is not evidence; the artefact (proof term, unit-checked quantity, interval, agreement score) is.

> Anti-pattern (also in `core/04`): conclusions that report **unit-free numbers** or **p-values alone**. · 反模式：用量纲缺失的数字或单个 p 值充当结论。

---

## The map · 映射表

| Claim type · 命题类型 | Instrument · 仪器 | Catalogue ids (`instruments`) | Gate must observe · 门禁须看到 |
|---|---|---|---|
| Definition / theorem / algebraic identity · 定义、定理、恒等式 | Machine-checked derivation · 机器检查的推导 | `lean4`, `mathlib`, `rocq`, `isabelle`, `agda` | A compiled proof (no `sorry`/`Admitted`/`postulate` left), toolchain version recorded |
| Protocol / concurrent-design property (safety, liveness) · 协议与并发性质 | Specification + model check · 规约与模型检验 | `tla-plus`, `alloy` | An explored state space: bounded scope, invariant, counterexample or exhaustion statement |
| Program correctness / spec conformance · 程序正确性 | Verification-aware language + SMT · 验证语言 + SMT | `dafny`, `z3`, `cvc5` | Verified obligations, or the failing obligation quoted with the solver version |
| Physical quantity, formula, simulation result · 物理量、公式、仿真 | Units + propagated uncertainty · 单位与传播不确定度 | `pint`, `uncertainties` | Dimensionally consistent expression **and** a stated uncertainty budget (coverage factor `k`) |
| Simulation credibility · 仿真可信度 | V&V / credibility assessment · 校核验证与可信度评估 | *(standard, not tool)* `[R108]` | Verification + validation + sensitivity/UQ assessment recorded, or explicitly waived |
| Molecular structure / property · 分子结构与性质 | Cheminformatics toolkit · 化学信息学工具 | `rdkit` | Canonical structure (identifier + provenance of the coordinates), tool version |
| Structure / sequence identity · 结构与序列同一性 | Accession-backed reference database · 带登录号的数据库 | `rcsb-pdb`, `uniprot`, `biopython` | Accession id, release/version, and reviewed-vs-unreviewed status quoted |
| Token/word/morphology/parse annotation · 分词、形态、句法标注 | Corpus resource + agreement statistics · 语料资源与一致性统计 | `universal-dependencies`, `inception`, `elan` | Guideline version **and** inter-annotator agreement (κ/α) on a held-out double-annotated sample |
| Behavioural/cognitive measurement · 行为与认知测量 | Experiment runtime + preregistration + model · 实验运行时 + 预注册 + 模型 | `psychopy`, `jspsych`, `osf`, `statsmodels`, `lme4`, `stan` | Pre-registered primary analysis (or a declared deviation), effect size **with interval**, reliability estimate |
| Numerical result from a multi-step pipeline · 多步流水线结果 | Reproducible pipeline engine · 可复现流水线 | `snakemake`, `nextflow` | Re-runnable pipeline + per-step provenance (versions, containers, inputs→outputs) |

---

## Formal claims · 形式命题

**When:** the deliverable contains a definition, a theorem, an invariant, or a correctness claim.
**Instrument:** a proof assistant (`lean4` + `mathlib`, `rocq`, `isabelle`, `agda`) for statements about mathematics; `dafny` (+ `z3`/`cvc5`) when the claim is about *code*; `tla-plus`/`alloy` when the claim is about *a design or protocol's behaviour over all executions*.

**Gate.** (1) The proof compiles under a **recorded toolchain version**; (2) no placeholder (`sorry`, `Admitted`, `postulate`, `assume`) remains — a placeholder turns a proof into a conjecture; (3) the *statement*, not just the proof, is reviewed by a human (a machine cannot check that you formalised the right thing); (4) model checking reports its **bound**: "no counterexample within scope N" is the claim, not "correct".

> Programme-level reference: `[R106]` (formal methods in practice — where proofs paid off and where they did not), `[R98]`/`[R99]` (mathlib / Lean 4).

## Physical quantities · 物理量

**When:** any number carrying a unit, or any derived quantity from a model/simulation.
**Instrument:** `pint` for dimensional discipline at the code level; `uncertainties` for first-order propagation (`x ± u`); the **GUM** (`[R107]`) for how an uncertainty budget is defined, combined, and reported.

**Gate.** (1) Units are never dropped "for readability" — the report names them; (2) every reported value has an uncertainty with a stated coverage factor; (3) the budget lists contributions (type A/B), not just a final number; (4) for simulation results, declare whether V&V (`[R108]`) was performed and what it covered. Physical constants and unit definitions follow the SI brochure (`[R109]`).

> Non-instrument: a spreadsheet. Reproducing a unit-checked, uncertainty-propagated computation from a spreadsheet is a provenance failure, not an instrument choice.

## Chemical & biological claims · 化学与生物命题

**When:** a claim about a molecule, a structure, or a sequence.
**Instrument:** `rdkit` for structure handling and canonical identifiers; `rcsb-pdb` / `uniprot` for the **accession-backed** record of a structure or sequence; `biopython` for the I/O glue.

**Gate.** (1) Every entity is identified by a **canonical identifier plus accession** (InChI/SMILES + PDB/UniProt id), not by a name alone; (2) the database **release/version** is quoted (these resources change monthly); (3) for structures, experimental vs computed models are distinguished; (4) tool parameters are recorded, since descriptors and alignments are parameter-dependent. · 名称不足以为证；须给规范标识符 + 登录号 + 版本。

## Linguistic data · 语言数据

**When:** a claim rests on annotation (tokens, morphology, syntax, discourse, speech) — including LLM-produced annotation.
**Instrument:** `universal-dependencies` (scheme + treebanks + validators), `inception` / `elan` (annotation and audio/video tiers), and **agreement statistics** as the measurement (`[R102]`).

**Gate.** (1) The annotation **guideline/version** is named; (2) agreement is reported on a **double-annotated sample** (κ/α), not asserted; (3) when a model annotates, report the same agreement quantity **plus** a human-verified sample — "the model agreed with itself" is not agreement; (4) corpus **licence and consent** permit the use claimed (a licence question is a provenance question). · 模型标注也要报一致性：模型与自己一致不算一致性。

## Empirical claims · 经验命题

**When:** the claim is about behaviour, cognition, health, society, education, or the economy — any population-level assertion.
**Instrument:** `psychopy` / `jspsych` (task runtime), `osf` (preregistration / registered reports, `[R110]`), and a modelling toolkit (`lme4` for clustered data, `statsmodels`, `stan` for full-Bayesian intervals).

**Gate.** (1) The **primary analysis is pre-registered** (or the deviation from the registration is declared and dated); (2) the claim is an **effect size with an interval**, never a bare significance test; (3) **reliability** of the measure is reported (internal consistency / test–retest); (4) where analytic choices are arbitrary (variable selection, exclusions, model family), report a **multiverse/sensitivity spread** rather than a single specification; (5) any LLM-in-the-loop step is treated as an instrument with its own reliability, not as an oracle. Background: `[R103]` (reproducibility manifesto).

> Reminder (`[R103]`, `[R110]`): pre-registration does **not** certify a result — it makes the analysis path auditable. Exploratory results are welcome when labelled exploratory.

## Computational provenance · 计算溯源

**When:** a number in the deliverable came out of more than one computational step.
**Instrument:** a workflow engine (`snakemake`, `nextflow`) that records inputs, versions, and container identity per step.

**Gate.** (1) The pipeline re-runs to the same outputs from the recorded inputs; (2) environment/version identity travels with each step; (3) the report says which steps were manual. · 手工步骤必须写明；否则"可复现"是空话。

---

## Deliberate non-entries · 有意不收录

- **A `standard` kind for GUM/SI/NASA-STD-7009/V&V 20.** Standards are *norms*, not instruments; they live as references (`[R107]`–`[R110]`) and as gate text, so they cannot be "installed" and silently satisfied.
- **Standalone statistics courses/packages beyond the four above.** `pingouin`, `JASP`, `PyMC` etc. are interchangeable implementations of the same instrument; adding each would inflate the catalog without discriminating.
- **`proof-search` / `autoformalisation` services.** Techniques inside the formal row, not separate instruments — they change *how* a proof is found, not *what* counts as evidence.
- **A general "AI annotator" entry.** LLM annotation is a *risk* to agreement, covered by the linguistic gate above; cataloguing a model would suggest the model is the measurement.

## Verification status · 核实状态

- **Verified this session (2026-10-18):** every catalog entry carries `verified`; all 27 `instruments` entries were checked against the first-party project page except `jspsych` (`verified: false` — `www.jspsych.org` answered with a client-side redirect stub; the library itself is well known, but this session did not read its documentation).
- **Standards:** `[R108]` (NASA-STD-7009B) read in full (scope text + public availability); `[R107]` (JCGM 100:2008 GUM) verified from the BIPM publications record, including **Amendment 1: 2026** (nonlinearity in measurement models, DOI `10.59161/PPDI3267`) — *as of 2026-10*; `[R109]` (SI brochure) landing page fetched, brochure PDF not read; `[R110]` (COS registered reports) landing page listed.
- **Body text not deep-read:** the tool documentation of the 26 verified entries was **not** read in full — the entries are verified at the *project/landing page* level (identity, ownership, purpose), which is what the catalog asserts. Re-verify before relying on a specific API claim.

---

## See also · 另见

- `core/04-verification-and-gates.md` — M3.10 and the gate checklist.
- `domains/logic/README.md`, `domains/linguistics/README.md`, `domains/cognitive-science/README.md` — the domain workflows these instruments serve.
- `review/disciplines-crosswalk-2026-10.md` — why these disciplines and capabilities exist.
- `review/harness-index.md` — generated index of all 160 catalogued entries.
