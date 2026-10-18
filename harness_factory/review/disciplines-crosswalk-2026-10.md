# Disciplines crosswalk 2026-10 — formal & empirical sciences · 学科交叉能力图谱

**Updated:** 2026-10-18 · Companion to [`workflow-patterns-2026-10.md`](workflow-patterns-2026-10.md) (loops & graphs) and [`frontier-2026-10.md`](frontier-2026-10.md) (context · security · durability · spend · evals).

> **中文速览**
> 问题：本仓库此前只有 `mathematics` / `physics` / `psychology` 等域，**数理逻辑与逻辑学、语言学、认知科学**没有专属域；三门学科共享的「举证方式」也只在 M3 的通用条款里隐含。本文按一手资料核验后：**新增 3 个域**（`logic` · `linguistics` · `cognitive-science`，含 rubric，域数 25 → 28）与 **3 条通用能力**（`formal-verification` · `dimensional-analysis` · `empirical-measurement`，能力数 24 → 27），并在 **M3.10** 写下共享不变式「按主张选仪器」。**计算科学**无新域：其理论侧由 `formal-verification` 覆盖，工程侧由既有 `software-engineering` / `data-science` 覆盖（有意不加重复域）。**有意未加**：`proof-search`（M3 条款已覆盖）、`statistical-significance`（与 `empirical-measurement` / `reproducible-experiments` 重复）。

---

## 1 · The question · 问题

Survey the harness requirements of mathematics, physics, mathematical logic, logic, linguistics, cognitive science and computing science — **each on its own** and **where they cross** — and integrate the geniune gaps rather than restating what the library already carries.

Method: (a) audit the existing 25 domains / 24 capabilities / M0–M8 for what each field already gets; (b) verify what each field's *evidence standard* actually is from bare primary sources (§2); (c) add only what (a) missed and (b) supports; (d) record what was deliberately left out (§7).

## 2 · Verified sources · 核验来源

New group **G** in [`references.md`](references.md) (`[R98]`–`[R106]`), fetched/confirmed 2026-10-18:

| ref | source | what it pins down |
|---|---|---|
| `[R98]` | mathlib, *The Lean mathematical library* (arXiv:1910.09336) | mathematics as a **machine-checked, community library** — dependently typed foundations, versioned |
| `[R99]` | de Moura & Ullrich, *The Lean 4 Theorem Prover* (CADE 28) | the proof assistant as the instrument that makes a formal claim checkable |
| `[R100]` | Open Logic Project (open textbook) | logic's structure: **syntax → semantics → proof theory → model theory → computability**, with meta-theory kept separate |
| `[R101]` | de Marneffe *et al.*, *Universal Dependencies* (CL 47(2)) | cross-linguistically consistent **annotation** as the substrate of a linguistic claim |
| `[R102]` | Artstein & Poesio, *Inter-Coder Agreement* (CL 34(4)) | the **reliability measure** (κ/α) that makes an annotation claim evidence |
| `[R103]` | Munafò *et al.*, *A manifesto for reproducible science* (Nat Hum Behav 1:0021) | **pre-registration, effect sizes, power, analytic flexibility, blinding, open data/code** |
| `[R104]` | Buckingham 1914, *On Physically Similar Systems … Dimensional Equations* (Phys. Rev. 4:345) | **dimensional analysis** — the invariant any physical quantity must satisfy |
| `[R105]` | Anderson *et al.*, *An integrated theory of the mind* (Psych. Rev. 111(4)) | the **falsifiable cognitive model** as the unit of cognitive-science explanation |
| `[R106]` | Woodcock *et al.*, *Formal methods: practice and experience* (ACM CSUR 41(4)) | formal methods across the **software life-cycle** — theory side of computing science |

## 3 · Each field on its own · 各自

| field | domain (faculty) | long artifact | the gate that fits it |
|---|---|---|---|
| Mathematics | `mathematics` (natural-sciences) | document | step-checked derivation + edge cases; machine-checking when formal |
| Mathematical logic / logic | **`logic`** (formal-sciences) — *new* | document | licensed rule application + **countermodel** search; object vs meta level |
| Physics | `physics` (natural-sciences) | dataset | **dimensional consistency + error propagation** + tolerance |
| Linguistics | **`linguistics`** (humanities) — *new* | dataset | annotation scheme + **inter-annotator agreement** + glossed evidence |
| Cognitive science | **`cognitive-science`** (social-sciences) — *new* | dataset | operationalised construct + pre-registered design + **effect size & reliability** |
| Computing science — theory | *(no new domain)* → M3 + `formal-verification` | document/code | machine-checked or model-checked claim (`[R106]`) |
| Computing science — engineering | `software-engineering`, `data-science`, `devops` (engineering) | code/dataset | tests, CI, reproducible builds (already carried) |

New domains ship with the same wiring as every other domain: a `domains/<id>/README.md` (pipeline layers L0–L5, module combination, field-specific risks), a `domains.json` entry (signals, artifact, grounding) and a `rubrics.json` entry (weighted dimensions). New faculties: none except **`formal-sciences`** (形式科学), which gives logic a home; linguistics sits in `humanities`, cognitive science in `social-sciences`.

## 4 · Where they cross · 交叉

The crossing is not a new domain — it is the fact that three families of fields verify with **three different instruments**, and that this choice must be made explicit (M0.5). That is now one capability per instrument:

| capability (new) | fires when | annotates | shared by |
|---|---|---|---|
| `formal-verification` | `domain ∈ {mathematics, logic}` OR (`verifiability = high` AND `artifact = code`) | M3, M4, M6 | mathematics · logic · theory-side computing science |
| `dimensional-analysis` | `domain ∈ {physics, engineering, chemistry, earth-environment}` | M3, M6 | physics · engineering · chemistry · earth-environment |
| `empirical-measurement` | `domain ∈ {psychology, cognitive-science, medicine, economics-finance, social-science, education}` | M3, M4 | cognitive science · psychology · medicine · economics · social science · education |

Shared invariants the crosswalk surfaced (all already carried by M0–M8, now named by a capability):

| invariant | modules | why every one of these fields needs it |
|---|---|---|
| Explicit axioms / assumptions before derivation | M0, M7 | a proof, a model and a study are all **conditional** on their assumptions |
| Provenance for every imported result | M4 | `[R98]` axioms+lemmas, `[R104]` constants, `[R101]` corpora, `[R103]` pre-registration |
| Step-level verification, not final-artifact approval | M3 | a wrong step invalidates the result even if the conclusion is true |
| Reproducible computational step (pinned versions) | M6 | proof assistant, units-aware tooling, tagger, analysis pipeline |
| Counterexample / replication as the real test | M3, M5 | `[R100]` countermodel, `[R104]` limits, `[R103]` replication, `[R105]` model comparison |
| Instrument version & check recorded | M4, M6 | "which Lean/mathlib", "which tagset", "which analysis script" |

## 5 · What changed · 本次改动

**3 capabilities (data-only, `data/capabilities.json`; 24 → 27)**, **3 domains (`domains.json` + README + rubric; 25 → 28)**, **1 shared module clause**:

- `core/04-verification-and-gates.md` — new **M3.10 (match the instrument to the claim)**: machine-checked derivation for formal results, units + error propagation for physical quantities, effect size + interval + reliability for empirical measurements; plus one checklist line and one anti-pattern (*unit-free numbers and p-only claims*). This is the clause the three capabilities annotate.
- `domains/logic/README.md`, `domains/linguistics/README.md`, `domains/cognitive-science/README.md` — full domain docs in the house style.
- `tests/test_domains.py` — three new classification cases (`logic`, `linguistics`, `cognitive-science`) and the `formal-sciences` faculty.

## 6 · Deliberately not added · 有意未加

- **A `computer-science` domain** — it would duplicate `software-engineering` + `data-science` on the engineering side and `logic` on the theory side; the theory facet is carried by `formal-verification` + M3.10 (M0.5: one home per concept).
- **`proof-search`** — a technique, not a requirement; the requirement ("a deliverable is unfinished until the checker closes it") is M3.10 + `formal-verification`.
- **`statistical-significance`** as its own capability — it would fire on exactly the same features as `empirical-measurement` (and overlap `reproducible-experiments`); the discipline lives in that capability's `why` (effect sizes, intervals, multiplicity) and in `[R103]`.
- **`dimensionless-numbers` / unit-library** — an implementation choice inside M6, not a requirement of the task.
- **Per-field capability sprawl** (one capability per discipline) — the design keeps *fields* in `domains/` and *evidence standards* in capabilities; only the three instrument families are shared enough to be mechanisms.

## 7 · Verification status · 核验状态

- **Fetched in full:** `[R98]` (arXiv abstract page), `[R103]` (Nature Human Behaviour, full text).
- **Bibliographic record verified, body listed not deep-read:** `[R99]`, `[R100]`, `[R101]`, `[R102]`, `[R104]`, `[R105]`, `[R106]` — titles/authors/venue/DOI confirmed on first-party publisher or project pages.
- **Domain workflows are distilled from these sources plus the existing library's M0–M8**; they are **methodology**, not empirical claims about any dataset. Nothing here is `[unverified]`.
- Regenerate and re-check: `PYTHONPATH=src python -m harness_factory capabilities --write`, `... map --write`, `... catalog --write`; then `python -m unittest discover -s tests`.

## 8 · Next-cycle cues · 下轮线索

> **Status (2026-10-18, P9):** every cue below was addressed in the *evidence-instruments* pass —
> catalogue class `instruments` (27 entries), `reference/evidence-instruments.md`, the emitted
> *Evidence instrument* stanza, and instrument sections in the `logic`/`linguistics`/`cognitive-science`/
> `physics`/`chemistry`/`biology` READMEs. Remaining for a later cycle: **spectra/crystallography**
> evidence (MassBank, ICSD/COD) was not catalogued; **probabilistic parsing** tooling was not catalogued;
> and the multiverse/registered-report gates are stated in prose, not machine-checked.
>
> **Status (2026-10-18, P10):** the **mathematics & statistics** branch of this crosswalk was deepened —
> `statistics` + `geometry-topology` domains, `statistical-inference` + `certified-computation`
> capabilities (clauses M3.11/M3.12), and 23 new `instruments` (CAS/SAT/geometry-topology/Bayesian/causal).
> The **methodology systems** of every field here are now mapped in `reference/methodology-map.md` (clause
> M3.13). Live scope board + next cues: `review/integration-map-2026-10.md` (P11 candidates:
> spectra/crystallography, probabilistic parsing, multiverse gates, **qualitative rigour**).

- **Physics/engineering depth**: SI-brochure-level unit rules and error-propagation practice (`GUM`); simulation validation & verification (V&V) vocabulary.
- **Chemistry/biology**: structural evidence (spectra, crystallography) and sequence provenance — the next crosswalk family.
- **Logic**: proof-assistant interop beyond Lean (Coq/Rocq, Isabelle, Agda) as instruments in the catalog.
- **Linguistics**: probabilistic parsing / LLM-as-annotator reliability, and the licence/consent gates for corpora.
- **Cognitive science**: registered-report workflows and multiverse/sensitivity analysis as explicit gates.
- **Cross-cutting**: a `discipline-instrument` stanza in the emitted templates so a new harness states its evidence instrument by default.
