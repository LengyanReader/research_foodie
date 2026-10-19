# Evidence instruments · 证据仪器表

> **What this is.** `core/04` (M3.10) says *match the instrument to the claim*. This is the concrete
> map: **claim type → instrument → catalogued tool → the evidence the gate must observe**. Load it
> whenever a deliverable asserts something stronger than "I read it somewhere". · 本文把 **M3.10** 落地：
> **命题类型 → 仪器 → 目录中的工具 → 门禁必须看到的证据**。凡是超出「我读到过」的断言，都按本表选仪器。
> Same paths as every factory doc — these are **the harness-factory's** files, not your project's.

**Updated:** 2026-10-20 · Load via `harness skill evidence-instruments`. Machine-readable truth: `data/harnesses.json` (class `instruments`, 68 entries / 25 kinds). Sources: `review/references.md` §G–§J (formal & empirical instruments), §M (knowledge-engineering & digital-humanities instruments) and §N–§P (reasoners, prose instruments).

---

## 中文速览

三类命题要三样东西：**形式命题**（定义、定理、协议性质、程序正确性）靠**机器检查的推导**；**物理量**靠**单位 + 传播的不确定度**；**经验命题**（心理/认知/医学/社科/教育/经济）靠**效应量 + 区间 + 可靠性**，且分析须**先注册**。语言类数据另加**标注者一致性**与**许可/知情同意**。此外：**计算得到的量**（代数标准形、同调群、纽结多项式）要么精确/带界地算、要么独立重算；**统计估计**要声明框架与模型、报收敛诊断、给区间；**套用某套方法论**要给出协议、假设与报告规范（M3.13）。仪器目录（68 件，25 个工具族）是本仓库 SSOT 的一部分；**声明仪器就是声明可反驳性**——说不出仪器，就等于没验证。

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
| Combinatorial search / satisfiability · 可满足性与组合搜索 | SAT solver · SAT 求解器 | `cadical` | The instance encoded (cnf/DRAT), the solved/unknown verdict, and the model or proof log |
| Algebraic / geometric / topological computation · 代数·几何·拓扑计算 | Computer algebra / geometry-topology toolkit · 代数系统与几何拓扑工具 | `sagemath`, `singular`, `macaulay2`, `gap`, `pari-gp`, `oscar`, `sympy`, `cgal`, `gudhi`, `regina`, `snappy`, `polymake` | Exact (or certified-precision) result, degeneracies handled, and an **independent re-derivation** / perturbed-input invariance check |
| Physical quantity, formula, simulation result · 物理量、公式、仿真 | Units + propagated uncertainty · 单位与传播不确定度 | `pint`, `uncertainties` | Dimensionally consistent expression **and** a stated uncertainty budget (coverage factor `k`) |
| Simulation credibility · 仿真可信度 | V&V / credibility assessment · 校核验证与可信度评估 | *(standard, not tool)* `[R108]` | Verification + validation + sensitivity/UQ assessment recorded, or explicitly waived |
| Molecular structure / property · 分子结构与性质 | Cheminformatics toolkit · 化学信息学工具 | `rdkit` | Canonical structure (identifier + provenance of the coordinates), tool version |
| Structure / sequence identity · 结构与序列同一性 | Accession-backed reference database · 带登录号的数据库 | `rcsb-pdb`, `uniprot`, `biopython` | Accession id, release/version, and reviewed-vs-unreviewed status quoted |
| Token/word/morphology/parse annotation · 分词、形态、句法标注 | Corpus resource + agreement statistics · 语料资源与一致性统计 | `universal-dependencies`, `inception`, `elan` | Guideline version **and** inter-annotator agreement (κ/α) on a held-out double-annotated sample |
| Behavioural/cognitive measurement · 行为与认知测量 | Experiment runtime + preregistration + model · 实验运行时 + 预注册 + 模型 | `psychopy`, `jspsych`, `osf`, `statsmodels`, `lme4`, `stan` | Pre-registered primary analysis (or a declared deviation), effect size **with interval**, reliability estimate |
| Statistical estimate / posterior · 统计估计与后验 | Declared frame + diagnostics + interval · 声明框架 + 收敛诊断 + 区间 | `r-project`, `pymc`, `numpyro`, `arviz`, `brms`, `r-inla`, `emcee`, `stan` | Declared frame (frequentist/Bayesian), stated model & priors, convergence (R-hat/ESS), and an interval - not a point or a p-value |
| Causal effect claim · 因果效应主张 | Identification strategy + falsification · 识别策略与证伪 | `dowhy` | The identification assumption stated, plus placebo / sensitivity / refutation checks |
| Numerical result from a multi-step pipeline · 多步流水线结果 | Reproducible pipeline engine · 可复现流水线 | `snakemake`, `nextflow` | Re-runnable pipeline + per-step provenance (versions, containers, inputs→outputs) |
| Concept / entity identity across records · 概念·实体同一性 | Authority + alias vocabulary + merge rule · 权威表 + 别名词表 + 合并规则 | `openrefine`, `splink`, `dedupe`, `pleiades`, `geonames`, `getty-tgn` | One canonical id per entity, its **recorded aliases**, and the merge decisions with reasons — undecidable pairs escalated, never averaged (`[R139]`, `[R145]`, `[R150]`) |
| Schema conformance of a graph · 图谱与模式一致 | Ontology + constraint shapes · 本体 + 约束形状 | `protege`, `rdflib`, `apache-jena` | The **declared ontology version** plus a machine-checkable validation report (SHACL shapes pass/fail per assertion) (`[R137]`–`[R140]`) |
| Entailment / consistency of an ontology · 本体的蕴含与一致性 | Description-logic reasoner · 描述逻辑推理机 | `hermit`, `elk` | The entailment, or the **inconsistency witness** (unsatisfiable class / clash), with the reasoner version; a reasoner *decides* and does not *extract* (`[R166]`, `[R167]`) |
| An assertion grounded in a corpus · 断言在语料中有据 | Graph construction + provenance model · 图谱构建 + 溯源模型 | `microsoft-graphrag`, `neo4j` | Each named assertion resolves to a source span or record id, or is recorded as a defect; ungrounded candidates are not kept (`[R141]`, `[R148]`) |
| Historical text transcribed from an image · 图版转写 | HTR engine + model record · 手写识别引擎 + 模型记录 | `transkribus`, `escriptorium` | The transcription, the model id/version used, and a stated or measured character-error rate (`[R153]`, `[R154]`) |
| Prose is readable and in the right register · 文字可读、语域正确 | Declared style linter + readability *alarm* · 声明的风格 linter + 可读性*警报* | `vale`, `languagetool`, `textstat` | A clean run of the **declared** rules (never "taste"), plus a term-consistency check and a punctuation standard for the language; a readability score is a drift alarm, **not** an approval, and a reader still judges the result (`[R192]`–`[R200]`) |

---

## Formal claims · 形式命题

**When:** the deliverable contains a definition, a theorem, an invariant, or a correctness claim.
**Instrument:** a proof assistant (`lean4` + `mathlib`, `rocq`, `isabelle`, `agda`) for statements about mathematics; `dafny` (+ `z3`/`cvc5`) when the claim is about *code*; `tla-plus`/`alloy` when the claim is about *a design or protocol's behaviour over all executions*.

**Gate.** (1) The proof compiles under a **recorded toolchain version**; (2) no placeholder (`sorry`, `Admitted`, `postulate`, `assume`) remains — a placeholder turns a proof into a conjecture; (3) the *statement*, not just the proof, is reviewed by a human (a machine cannot check that you formalised the right thing); (4) model checking reports its **bound**: "no counterexample within scope N" is the claim, not "correct".

> Programme-level reference: `[R106]` (formal methods in practice — where proofs paid off and where they did not), `[R98]`/`[R99]` (mathlib / Lean 4). Algebra and automated reasoning deepen this row: a computer algebra system (`sagemath`, `singular`, `macaulay2`, `gap`, `pari-gp`, `oscar`, `sympy`) computes over exact polynomials and groups, and a SAT solver (`cadical`) settles an encoded combinatorial instance — neither is a proof, so an **unchecked CAS/solver output is a conjecture** until re-derived (M3.12).

## Certified computation · 可核验计算

**When:** the claim is a value produced by an *algorithm* over an exact structure — an algebraic normal form, a group order, a homology group, a knot polynomial, a triangulation's invariant.
**Instrument:** a computer algebra system (`sagemath`, `singular`, `macaulay2`, `gap`, `pari-gp`, `oscar`, `sympy`) or a geometry/topology toolkit (`cgal`, `gudhi`, `regina`, `snappy`, `polymake`).

**Gate.** (1) The algorithm and its version are recorded; (2) the computation runs under **exact or certified arithmetic**, or reports a stated precision/bound; (3) **degeneracies are handled explicitly** — a geometric predicate that flips under floating-point noise invalidates the invariant; (4) the result is **independently re-derived** (a second tool, a hand-checkable special case, or invariance under a small perturbation). An invariant that changes when you nudge the input was never an invariant. `[R114]` (interval arithmetic) is the numeric-precision reference.

## Statistical estimates & causal claims · 统计估计与因果主张

**When:** the deliverable carries an estimate, a posterior, or a causal statement.
**Instrument:** a statistics/Bayesian toolkit (`r-project`, `pymc`, `numpyro`, `arviz`, `brms`, `r-inla`, `emcee`, `stan`) for the estimate; a causal toolkit (`dowhy`) for the effect. Background: `[R111]` (Bayesian workflow), `[R112]` (rank-normalised R-hat).

**Gate.** (1) The **inferential frame** is declared (frequentist or Bayesian), and for Bayesian work the **priors and likelihood** are stated; (2) the computation **converged** — R-hat and effective sample size reported, not a trace eyeballed; (3) the answer is an **interval / credible interval**, never a bare point or p-value; (4) a **causal** claim names its identification assumption *and* runs a falsification/sensitivity check (placebo, refutation) — "the regression coefficient was significant" is not a causal identification. `[R111]` notes the workflow is *iterative*: model checking and prior sensitivity are part of the claim, not a footnote.

## Methodology · 方法论

**When:** the work follows (or claims to follow) a named field method — a systematic review, a causal-identification design, a qualitative coding, a design-science study, a DoE.
**Instrument:** none is a tool; the evidence is the **method's own artefacts**. Canonical demands and what the harness must enforce are mapped in `reference/methodology-map.md` (M3.13).

**Gate.** (1) The **protocol/registration** exists where the method has one (PRISMA `[R115]` protocol, pre-registration, registered report); (2) the method's **assumptions** are stated and checked (identification strategy, saturation, factorial randomisation); (3) the field's **reporting standard** is followed (CONSORT `[R117]`, GRADE `[R116]` for certainty of evidence); (4) the deliverable says which parts were *exploratory* vs *confirmatory*. A method name is not a method.

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

- **A `standard` kind for GUM/SI/NASA-STD-7009/V&V 20.** Standards are *norms*, not instruments; they live as references (`[R107]`–`[R110]`, `[R114]`–`[R117]`) and as gate text, so they cannot be "installed" and silently satisfied. The same holds for **methodology protocols** (PRISMA/GRADE/CONSORT): they are enforced by M3.13 + `reference/methodology-map.md`, not by a catalog entry.
- **Standalone statistics courses/packages beyond the eight above.** `pingouin`, `JASP`, `cmdstanpy`/`cmdstanr`, `pyro` etc. are interchangeable implementations of the same instrument; adding each would inflate the catalog without discriminating. (P10 did add the *distinct* frames now covered — Python probabilistic programming, JAX, R multilevel, approximate-Bayesian, ensemble MCMC — not more of the same.)
- **`proof-search` / `autoformalisation` services.** Techniques inside the formal row, not separate instruments — they change *how* a proof is found, not *what* counts as evidence.
- **A general "AI annotator" entry.** LLM annotation is a *risk* to agreement, covered by the linguistic gate above; cataloguing a model would suggest the model is the measurement.
- **A `geometry-topology` series duplicated under `mathematics`.** The toolkits (`cgal`, `gudhi`, `regina`, `snappy`, `polymake`) are catalogued once, under their own kind; the mathematics README points at them rather than re-listing.
- **A `standard` kind for TEI P5 / CIDOC-CRM / Dublin Core / EAD3 / IIIF.** The same rule as GUM/SI above: an encoding standard is a *norm*, not an instrument — it cannot be "installed" and silently satisfied, so the first-party texts live as references (`[R142]`–`[R147]`) and as domain gate text (`domains/digital-humanities/README.md`). A **gazetteer** is different in kind and *is* catalogued (`pleiades`, `geonames`, `getty-tgn`), because an authority table is a queryable resource the way `uniprot` is — not a norm.
- **A general "KG tool" entry.** Protégé/RDFLib/Jena are catalogued as `ontology-toolkit` because they validate a graph against a declared schema; GraphRAG is `kg-construction` because it derives the graph from text. A further generic "knowledge graph tool" row would name a category, not an instrument.

## Verification status · 核实状态

- **Verified this session (2026-10-19, §M):** all 13 new `instruments` entries were fetched directly (`protege`, `rdflib`, `apache-jena`, `neo4j`, `microsoft-graphrag`, `openrefine`, `splink`, `dedupe`, `pleiades`, `geonames`, `getty-tgn`, `transkribus`, `escriptorium`) — each returned HTTP 200 to a Firefox UA, so all are `verified: true`. The standards they sit beside (RDF/OWL/SKOS/SHACL/PROV-O, CIDOC-CRM, IIIF, DCMI, TGN, EAD3, TEI P5) were fetched in the same session and are **references**, not instruments.

- **Verified this session (2026-10-18, P10):** all 23 new `instruments` entries were checked against their first-party project pages — `sagemath`, `singular`, `macaulay2`, `gap`, `pari-gp`, `oscar`, `sympy`, `cadical`, `mathcomp`, `metamath`, `cgal`, `gudhi`, `regina`, `snappy`, `polymake`, `r-project`, `pymc`, `numpyro`, `arviz`, `brms`, `r-inla`, `emcee`, `dowhy` (all `verified: true`). `jspsych` remains the only entry with `verified: false`.
- **Verified this session (2026-10-18, P9):** all 27 P9 `instruments` entries were checked against the first-party project page except `jspsych`.
- **Standards & method sources:** `[R108]` (NASA-STD-7009B) read in full; `[R107]` (GUM) verified from the BIPM record incl. **Amendment 1: 2026** (`10.59161/PPDI3267`) — *as of 2026-10*; `[R111]`/`[R112]` (arXiv abstract pages) fetched; `[R113]` (Stan) confirmed via the R-hat appendix bibliography (`10.18637/jss.v076.i01`); `[R115]` (PRISMA 2020) confirmed from the EQUATOR record (`10.1136/bmj.n71`); `[R114]` (IEEE 1788-2015), `[R116]` (GRADE), `[R117]` (CONSORT 2010), `[R118]` (Hevner 2004), `[R119]` (Glaser & Strauss 1967) are recorded at the **bibliographic record** level — *listed, not deep-read* this session.
- **Body text not deep-read:** the tool documentation of the verified entries was **not** read in full — the entries are verified at the *project/landing page* level (identity, ownership, purpose), which is what the catalog asserts. Re-verify before relying on a specific API claim.

---

## See also · 另见

- `core/04-verification-and-gates.md` — M3.10–M3.13 and the gate checklist.
- `reference/methodology-map.md` — field → methodology system → what the harness must enforce (M3.13).
- `reference/outlet-map.md` — field → high-quality information outlets / portals / media (where to *look*; P11).
- `reference/cross-language.md` — how to carry a claim across languages without changing its meaning (M4.10).
- `domains/logic/README.md`, `domains/linguistics/README.md`, `domains/cognitive-science/README.md` — the domain workflows these instruments serve.
- `domains/digital-humanities/README.md` — the domain the §M instruments (HTR, gazetteers, ontologies) serve, and `review/knowledge-and-dh-crosswalk-2026-10.md` — the round that added them (M3.14, M4.11–M4.13).
- `domains/statistics/README.md`, `domains/geometry-topology/README.md` — the P10 domains.
- `review/disciplines-crosswalk-2026-10.md`, `review/integration-map-2026-10.md` — why these disciplines/capabilities exist and what is deferred.
- `review/harness-index.md` — generated index of all 183 catalogued entries.
