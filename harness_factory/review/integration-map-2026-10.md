# Integration map · 2026-10 — scope, status, and what would make each candidate discriminating

> **What this is.** A durable roadmap for *what has been integrated into the factory, what is next, and what is
> deliberately deferred* — with, for every candidate, **what would make it discriminating** (the test the factory
> applies before adding anything). It answers two standing asks: *integrate statistics / Bayesian inference /
> basic mathematics*, and *search, organise and integrate each field's methodology systems*. · 本文是可持续的
> 路线图：**已整合 / 下一步 / 有意推迟**，并对每个候选写明**「怎么才算判别性」**（工厂新增任何东西前要过的测试）。

**Updated:** 2026-10-19 · Load via `harness skill integration-map`. Companion reviews: `review/disciplines-crosswalk-2026-10.md` (§G), `review/frontier-2026-10.md` (§E), `review/workflow-patterns-2026-10.md` (§F).

---

## 中文速览

本轮（P10）把两条长期线索做实：**(1) 数学与统计**——新增 `statistics`、`geometry-topology` 两个域 + `statistical-inference`、`certified-computation` 两个能力，并把 23 件代数/几何拓扑/贝叶斯仪器收进目录（M3.11/M3.12）；**(2) 各领域方法论体系**——新增 `reference/methodology-map.md`（领域 → 方法论 → 来源 → 要求 → 由谁执行），并把 M3.13「声明方法及其假设」写进不变量层；**方法论不做成能力**（会到处触发、不判别），这是有意的设计取舍。

**P11（2026-10-19）** 落地另两条长期线索：**(3) 跨语言意群保真**——把「按意群（语义单元）对齐、靠回译互证、不可译词加注、不逐字对译」写进不变量 **M4.10**，并新增 `reference/cross-language.md`（对齐规程 / 互证协议 / 术语处理 / 双语交付）；**`cross-language` 不做成能力**（特征向量无语言轴，无法判别）；**(4) 各领域信息源**——在 `data/sources.json` 新增 `outlets` 组（68 条：门户 · 期刊 · 预印本 · 数据库/登记库 · 数据仓储 · 媒体，按领域分），新增 `reference/outlet-map.md`；每条标注 `outlet_kind` + `why` + `not_for` + `verified` + `access`。本表列出**已完成 / 下一步 / 以后**三个状态，并逐条说明**判别性判据**与**证据门**，供后续循环直接取用。

---

## 0. The discriminating test · 判别性判据

Before anything is added to the SSOT, it must pass **all four**:

1. **It fires distinctly.** A capability is added only if some feature vector turns it on *and* off across realistic tasks. If it fires on nearly everything (or nothing), it is documentation, not a mechanism.
2. **It maps to a real invariant.** Every capability annotates an existing clause in `core/` (a module item) — a capability with no clause is a label.
3. **It is traceable.** Every factual claim behind it cites a first-party source (`review/references.md`) with an access date; unverifiable items are marked `verified: false` / *listed, not deep-read*, never smoothed over.
4. **It is not a duplicate.** A domain/capability/instrument that another entry already covers is refused, and the refusal is **recorded** (this doc / the companion review).

---

## 1. Status board · 状态表

Status keys: **done** = in the SSOT with a gate · **next** = scoped, evidence and design identified, not yet built · **later** = real gap, deferred (reason given) · **out** = deliberately rejected.

### 1a. Mathematics & statistics · 数学与统计（P10, **done**）

| Item | Kind | Entry | Discriminating because | Gate |
|---|---|---|---|---|
| Statistics | domain | `statistics` (faculty `formal-sciences`) | 45 unique signals; wins on Bayesian/frequentist phrasing without stealing `data-science` (checked) | rubric `统计质量` |
| Geometry & topology | domain | `geometry-topology` (faculty `formal-sciences`) | signals are computational-geometry/topology specific (`persistent homology`, `triangulation`, `流形`…); distinct from `mathematics`' `几何`/`代数` | rubric `几何与拓扑质量` |
| Statistical inference | capability | `statistical-inference` (M3, M4) | fires only on `domain = statistics` — not on `data-science`, not on the empirical domains (`empirical-measurement` covers those) | **M3.11** frame + convergence + interval |
| Certified computation | capability | `certified-computation` (M3, M6) | fires only on `domain = geometry-topology`; the clause M3.12 also covers mathematics computations (which `formal-verification` already annotates), so no overlap | **M3.12** exact/certified + independent re-derivation |
| 23 instruments | catalog | CAS (`sagemath`,`singular`,`macaulay2`,`gap`,`pari-gp`,`oscar`,`sympy`), SAT (`cadical`), proof library/verifier (`mathcomp`,`metamath`), geometry-topology (`cgal`,`gudhi`,`regina`,`snappy`,`polymake`), Bayesian (`r-project`,`pymc`,`numpyro`,`arviz`,`brms`,`r-inla`,`emcee`), causal (`dowhy`) | each names a *different* computation/observation face; catalog 160 → 183, kinds 46 → 50 | `reference/evidence-instruments.md` §Certified computation / §Statistical estimates |

**Deliberately not added (P10):** a `geometry-topology` *series* duplicated under `mathematics` (pointed at, not re-listed); more interchangeable stats packages (`pingouin`/`JASP`/`cmdstanpy`) — `evidence-instruments.md` §non-entries; a `statistics`-as-faculty split (it sits in `formal-sciences` with `logic`).

### 1b. Methodology systems per field · 各领域方法论（P10, **done** for the map; per-field depth **next**）

| Item | Kind | Entry | Discriminating because | Gate |
|---|---|---|---|---|
| Methodology map | reference | `reference/methodology-map.md` | field → method → source → what it demands → **who enforces it**; one row per system, three-part contract | **M3.13** declare the method |
| Method invariant | clause | `core/04` **M3.13** + checklist + anti-pattern *method-by-vibes* | applies to every task with a method; **not** a capability (see §2) | — |
| Method protocols as references | references | `[R115]` PRISMA 2020, `[R116]` GRADE, `[R117]` CONSORT 2010, `[R118]` Hevner 2004, `[R119]` grounded theory | each is a field's own reporting/assurance standard; not installable instruments | prose gates in the map |

**Next (methodology depth):**
- **Qualitative rigour** — codebook + double-coding + saturation for grounded-theory/thematic work. *Discriminating if* it can key on something other than "empirical domain" (which `empirical-measurement` already takes); today the feature vector cannot tell a qualitative study from a quantitative one. Candidate: widen `artifact`/add a `data_kind` hint, then a capability `qualitative-rigour` (M3, M4). **This is the strongest next candidate** because it closes a real gap: a single coder's reading currently passes every gate.
- **Design of experiments** — randomisation/blocking/factorial declarability. *Discriminating if* keyed on a design vocabulary that does not merely re-trigger `dimensional-analysis`/`empirical-measurement`.
- **Per-field methodology sections** in the domains not in scope (medicine, social-science, education, law, humanities) — currently only the map; adding sections would duplicate it unless each names *field-specific* traps.

### 1c. Evidence & instruments · 证据与仪器（P9 **done**, extensions **later**)

| Candidate | Status | Discriminating because | Why deferred |
|---|---|---|---|
| Spectroscopic / crystallographic evidence (MassBank, ICSD/COD) | **later** | a spectrum/reflection is a *different* observation face than a structure: peaks + assignment + reference library, not an accession | needs first-party verification of each database's licence and API; keep as a P11 slice |
| Probabilistic-parsing / model-based NLP tooling | **later** | a parser is an instrument whose *reliability* (not existence) is the claim | overlaps the linguistic agreement gate; add only with a measured-reliability requirement |
| Multiverse / registered-report *machine* gates | **later** | the gate must read the registration and diff it against the code | prose-only until the registration can be parsed; `osf` is catalogued but not wired to the gate |
| Simulation V&V tooling (verification/validation harnesses) | **later** | NASA-STD-7009 (`[R108]`) is a standard, not a tool; a tool would need to *produce* the V&V report | standards stay references by the non-entry rule |

### 1d. Frontier & workflow · 前沿与工作流

`done` (P7/P7.2/P7.3/P9): context budget, untrusted content, durability, spend caps, evals, loop discipline, graph orchestration, formal/empirical instruments. **next:** agentic-eval methodology beyond held-out sets (trajectory scoring of *multi-agent* runs); **later:** plugin marketplace, live gate runtime (out of P2 scope by design).

### 1e. Cross-language fidelity & per-field outlets · 跨语言保真与各领域信息源（P11, **done**）

| Item | Kind | Entry | Discriminating because | Gate |
|---|---|---|---|---|
| Meaning-unit fidelity | clause | `core/05` **M4.10** + checklist + anti-pattern *word-for-word fidelity* | applies whenever text crosses languages; **not** a capability (§2) | **M4.10** align by sense group + corroborate |
| Cross-language procedure | reference | `reference/cross-language.md` | alignment, mutual corroboration, term handling, bilingual deliverables, non-entries — one procedure, no textbook | §3 round-trip / second reader |
| Per-field outlets | data + reference | `data/sources.json` group `outlets` (68 entries; topics use **field domain ids**) + `reference/outlet-map.md` | keyed on the *field*, not the AI-intel topic vocabulary; each entry carries `outlet_kind`, `why`, `not_for`, `verified`, `access` | `harness sources --group outlets`; `tests/test_sources.py::OutletDataTest` |
| Standards & theory refs | references | `[R120]` ISO 17100, `[R121]` ISO 5060, `[R122]` Halliday & Hasan, `[R123]` XLIFF 2.2, `[R124]` Vinay & Darbelnet, `[R125]` Nida & Taber, `[R126]` MQM | each is a *fidelity standard or procedure*, not a product | prose gates in `cross-language.md` |

**Deliberately not added (P11):**
- **`cross-language` capability** — the 8-axis feature vector has no language axis; the requirement is an invariant (M4.10) + a procedure, not a mechanism.
- **A translation-metric instrument in the catalog** (BLEU/COMET) — a surface score is not a fidelity gate (§6 of the doc).
- **A parallel outlets registry** — folded into `sources.json` (M0.5); the AI/ML `venues`/`media` groups are **not** duplicated, only cross-referenced.
- **Outlet feeds in the intel loop** — outlets are reference (`feed: null`); they do not enter AI-intel relevance scoring.

---

## 2. Deliberate non-additions, recorded · 有意不新增（留档）

- **`methodology-fit` as a capability** — would fire on almost every task; carried by M3.13 + the map instead.
- **`standard` kind for norms** (GUM/SI/NASA-STD-7009/PRISMA/GRADE/CONSORT) — norms are not installable instruments (P9 rule, reaffirmed P10).
- **A `computer-science` domain; `proof-search`; `statistical-significance`** — recorded in `review/disciplines-crosswalk-2026-10.md`.
- **`geometry-topology` tools duplicated under `mathematics`** — catalogued once, referenced from the mathematics README.
- **A `statistics` faculty** — `statistics` sits in `formal-sciences` beside `logic`; a new faculty for one domain would be taxonomy noise.
- **`cross-language` as a capability** — no language axis in the feature vector; carried by **M4.10** + `reference/cross-language.md` (P11).
- **A machine-translation metric as a fidelity gate** — BLEU/COMET rank candidates; they do not certify that a claim's meaning survived (P11).

---

## 3. Next-cycle cues · 下一轮线索

1. **Qualitative rigour** (§1b) — the clearest gap; needs a small feature-vector affordance first.
2. **Design of experiments** — after (1), to avoid double-firing.
3. **P11 instruments slice: spectra/crystallography** — verify licences/APIs first (`later` in §1c).
4. **Domain-methodology sections** for medicine/social-science/education/law/humanities — only where they name field-specific traps the map does not.
5. **`jspsych` re-verification** — the single `verified: false` entry; re-check the landing page on the next instrument pass.
6. **Outlet re-verification** — the 22 `verified: false` outlets in `sources.json` were **listed, not confirmed** (automated check blocked 403/405); re-check via a browser on the next pass and, where an RSS exists, consider tracking a subset.
7. **Cross-language worked example** — add one bilingual EN↔ZH worked example to `reference/cross-language.md` (source unit → rendering → back-translation diff) when a real artifact is available.

---

## See also · 另见

- `reference/methodology-map.md` — the methodology deliverable (M3.13).
- `reference/cross-language.md` — the cross-language deliverable (M4.10).
- `reference/outlet-map.md` — the per-field information-outlet map (P11).
- `reference/evidence-instruments.md` — the claim → instrument map (M3.10–M3.12).
- `review/disciplines-crosswalk-2026-10.md` — §G (formal & empirical sciences) and §8 (P9 status note).
- `CAPABILITIES.md` / `HARNESS-MAP.md` — generated views of the current SSOT (29 capabilities · 30 domains · 183 catalog entries).
