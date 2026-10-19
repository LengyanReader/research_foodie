# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Added
- **Depth round (P15) - KG canon · training boundary · scholarly channels · language polish · self-model.** Five
  surveys, two new invariants and the first round to *state what the library does not cover*.
  - **Knowledge graphs (`review/knowledge-graph-patterns-2026-10.md`, §N R155-R170).** A layered stack (data model >
    schema > vocabulary > constraints > query > provenance > reasoning) with the failure mode named - *layer confusion* -
    the classic method narrowed to **competency questions first** (Ontology Development 101; METHONTOLOGY/NeOn/OntoClean
    named but not re-read), and "knowledge feature" split into four different things: embeddings *rank*, GNNs *learn
    structure*, reasoners *decide*, OBDA *maps*. Frontier (generative construction, GraphRAG, agentic maintenance) did not
    repeal **identity** or **evidence**. Instruments `hermit`, `elk` (entailment can be refuted, not asserted).
  - **Training (`review/training-methodology-coverage-2026-10.md`, §O R171-R191).** Every family graded *in axis /
    adjacent / out of scope* against a stated criterion. Verdict: the stack is surveyed, the library covers the
    **boundary**. A `training-*` capability is refused because the feature vector cannot distinguish "train" from "use",
    so it would be a predicate the engine silently ignores (M5.10); recorded with a revisit trigger.
  - **Channels (`review/scholarly-channels-2026-10.md`, +20 outlets).** ~95 channels with observed statuses,
    first-party-vs-aggregator marks and seven no-laundering rules; OpenAIRE, DataCite, ROR, BASE, Connected Papers,
    ResearchRabbit, OpenReview, PubPeer, SciELO, Redalyc, HAL, CiNii, J-STAGE, CNKI, Wanfang, EThOS, PMLR, SpringerLink,
    Cambridge Core, PLOS. No duplicate ids: Semantic Scholar/Crossref/CORE/scite live in `tools`, OpenAlex in `projects`,
    AI/ML venue indices in `venues` - surfaced in prose, not re-registered.
  - **Language polish - clause M4.14 (`core/05`) + capability `prose-polish`** (`review/language-polish-2026-10.md`, §P
    R192-R200). A gate separate from truth: a machine may **reject** (declared house style, term consistency, punctuation
    per GB/T 15834-2011) and only a reader may **approve**; a readability score is a drift alarm, never a pass mark.
    Chinese failure modes named (欧化句式/翻译腔, 四字格堆砌, 的的不休, 全半角混用, 繁简不等价). Instruments `vale`,
    `languagetool`, `textstat` (+ kinds `prose-linter`, `readability-metric`).
  - **Self-model - clause M5.11 (`core/06`) + capability `gap-seeking`** (`review/self-model-and-gap-seeking-2026-10.md`,
    §Q R201-R218). Self-report is testimony; an external check is evidence. Three artefacts: an evidence-backed
    self-model, a two-halved gap register, and one **disconfirming** check per round. Exploration is bounded (holdout,
    budget, stop condition) and novelty is not value.
  - **Counts.** 33 > **35** capabilities · 24 > **26** clauses · 63 > **68** instruments (23 > 25 kinds) · 75 > **95**
    outlets · R154 > **R218**. **237 tests** (233 + 4 guards). `cycle audit`: 0 hard, 0 gaps.
- **Knowledge engineering & digital humanities (P14)** - the ask was a *class*: how to build, maintain,
  manage and evolve a knowledge base / graph / ontology, and what digital-humanities work adds. Grounded in
  a **full primary-source read** (关书朋 · 何宇佳 · 张英聘, 《文献与数据学报》 **8(3): 56–72**, Sep 2026, open
  publisher PDF; the printed DOI does **not** resolve and is recorded as printed-only) crosswalked against
  **normative first-party standards** (RDF 1.1, OWL 2, SKOS, SHACL, PROV-O, CIDOC-CRM, IIIF, DCMI Terms,
  Getty TGN, EAD3, TEI P5 → **§M, R136–R154**). The 11-mechanism crosswalk found **9 covered / 1 partial /
  2 real gaps**, so the round landed **4 clauses** — **M3.14** (a gate trades *precision*, not coverage:
  report recall beside precision — the case moves relation precision 88.79% → 97.67% while recall moves only
  83.05% → 83.42%), **M4.11** (ontology as a contract: types, relation directions and identity rules declared
  *before* extraction; an untypeable candidate is a defect to record), **M4.12** (one canonical identity per
  entity: aliases recorded, authorities reused, undecidable merges escalated to a human — never averaged),
  **M4.13** (bound the answer by the evidence: every named assertion carries a pointer, and "the sources are
  silent" is a complete answer) — **4 capabilities** (`ontology-as-contract`, `entity-resolution`,
  `evidence-bounded-generation`, `schema-evolution`) with router + provenance rows and guard tests, the
  **`digital-humanities` domain** (31st; faculty `humanities`, artifact `dataset`) with its weighted rubric,
  **13 `instruments` under 6 new kinds** (ontology toolkits, graph stores, KG construction, entity
  resolution, gazetteers, HTR), and **7 outlets** for standards/authorities. **Deliberate non-additions
  recorded:** no KG-retrieval capability, no `knowledge-engineering` domain, and **no `encoding-standard`
  instrument kind** — TEI/CIDOC/Dublin Core/EAD3/IIIF are norms, so they stay references. Crosswalk +
  verdicts: `review/knowledge-and-dh-crosswalk-2026-10.md`; domain: `domains/digital-humanities/README.md`.
- **P12 closeout — two negative results kept honest** — the 22 `verified: false` outlets were re-checked with
  a browser UA: **3 answered** (NOAA, APA PsycNet, CourtListener) and were flipped, while **19 remain
  host-blocked** and stay `verified: false` with their reason (the re-check is done; the flags are the
  result). The roundup's 17 uncited figures were cleared against the papers' own HTML: **16 confirmed
  verbatim**, **2 readings corrected in kind** (the 4.1×–39× range is the *TQ-cost gain* column, and
  41.1→53.3 is the **avg@5** metric), and **1 stays `unverified`** because `2610.20563` has no reachable
  HTML full text. A bounded 8-week backfill (Pass A) mapped 90 papers → 68 (75.6%); the archive carries no
  top-pick labels, so **Pass B is not worth its cost yet**.
- **Agent-harness frontier sourcing pass (group §L)** — the Oct 12–18 *Top AI Papers of the Week*
  roundup was entered through **primary records, not summaries**: nine arXiv preprints (R127–R135 in
  `review/references.md` §L + `references.bib`) recorded at **abstract level only** — one batched arXiv
  `id_list` query, id · title · authors · date agree in every case, zero phantom entries — with the
  roundup's own numbers and institutional attributions left **`[unverified]`** instead of carried across.
  Seven `sources/source-map.md` rows map them to **existing** capabilities (no new capability, no new
  clause); one item (LoGRA, `arXiv:2610.06647v2`) is recorded as **considered and declined** rather than
  listed. Same pass: the tracked entity `nlpnews` was repointed off a host this environment blocks
  (`*.substack.com` → the publication's own domain, whose paginated archive API also answers), the outlet
  map gained a retrieval-route rule plus an explicit **non-entry** for aggregator digests, and
  `harness refresh --provider feed` now ingests the feed end-to-end (20/20 accepted, **no new code** —
  the weekly loop rides the existing `refresh` callback). `references.bib`'s stale header count
  (`R1–R79` → `R1–R135`) was corrected in passing.
- **First round driven by the mechanism itself (P12, partial)** — the audit's 12 soft gaps were consumed,
  not restated: router rows for `portable-skills` and `reproducible-experiments` (capabilities that
  existed but were unreachable from the entry table), and `tests/test_capabilities.py::TriggerCoverageTest`
  (10 guards, each pinning a capability's declared trigger *and* the quiet vector it must not fire on).
  `harness cycle audit` now reports **0 hard problems and 0 gaps**.
- **M4.10 worked example** — `reference/cross-language.md` §7 carries a real EN↔ZH pair (the
  standing-reference block) through unit segmentation, a **rejected** first-pass drift hypothesis
  (widening the unit dissolved it), and two **real** defects: units 4 (declare the capability + file) and
  8 (M0.4 · M0.1/M0.2 · irreversible acts) were missing from the compressed Chinese renderings, and
  「只提案、不编造任务内容」 fused two units into a claim the English master does not make. Fixed in
  `AGENTS.md` §6, `GUIDE.md` and `introduction.md`; the master is untouched.
- **Quick-start fidelity gate** — the first sweep fixed "the guides" but missed the **READMEs**, the two
  copies users actually paste; a user pasting the block back exposed it. Both READMEs now carry units 4,
  5 and 8 and name `harness check --dir <output>`. New guard
  `tests/test_standing_reference.py::QuickStartFidelityTest` (5 cases) pins every copy, so this cannot
  silently regress; §7 records the miss and the rule it yields (enumerate renderings from the reader's
  entry points, not the writer's edits).
- **Path parameter in every paste block** — the block assumed the factory sits at `./harness_factory`, but
  the repo is cloned wherever the reader wants it. All eight renderings (`README` ×2, both README
  templates, `AGENTS.md`, `GUIDE.md`, `introduction.md`, `SKILL.md`) now mark the location as a parameter
  to fill — `<HF>` = the real path of the cloned `harness_factory/` directory, e.g.
  `~/src/research_foodie/harness_factory` — and give the no-install check form
  (`PYTHONPATH=<HF>/src python -m harness_factory check --dir <output>`); `check` is no longer named bare.
  The master keeps its own wording (「把 `./harness_factory` 换成真实路径」) and now cross-references `<HF>`,
  so the two conventions are one. `QuickStartFidelityTest` rejects the unmarked `./harness_factory` form.
- **Capability rounds as a mechanism (M5.10)** - new SSOT `data/cycles.json`: 9 recorded rounds
  (`baseline` -> `P13`, git-verified `added` ids), the **definition-of-done as data** (7 axes with
  hard/soft severity) and **11 roadmap items**, each carrying a `reason`, a `revisit_when` trigger and a
  `source`. `cycle.py` + CLI `harness cycle [list|show|audit|roadmap|dod]`: `audit` separates **hard
  problems** (phantom ids, clauses not anchored in their own module, `when` predicates the engine cannot
  evaluate, deferrals without a reason or trigger) from the **soft gap surface** (missing router rows,
  guards, provenance) - the gap list is the next round's worklist. New clause **M5.10** in `core/06`
  (a round is recorded, audited and closed; a deferral is a decision, not an omission); procedure
  `reference/capability-cycle.md`; guard `tests/test_cycle.py` (16 cases).
- **Clause anchoring repair** - `M2.10`, `M2.11`, `M3.10` and `M8.10` were cited across review/router docs
  but never anchored in `core/` (and `M2.11` was mislabelled inside `core/09`); all four are now anchored
  in their own module, and `sources/source-map.md` gained rows for M2.10/M2.11, M3.10-M3.13, M5.10 and
  M8.10.
- **Usage in the README** — the five usage rules (router · evidence instruments · methodology · outlets ·
  cross-language) now live in the root READMEs' *How to use this factory* section, beside the
  one-instruction standing reference and its revocation, so "how to use" is findable without the CLI.
  Guarded: each README must name all five reference docs + the revoke phrase.
- **Cross-language fidelity (M4.10)** — new invariant in `core/05`: when a claim moves into another
  language, align by **meaning unit** (意群 / sense group / *translation unit*), **corroborate** by
  back-translation / a target-language reader / a second-language source, preserve stance·scope·modality·
  entity identity, and **gloss — never silently substitute**. New procedure `reference/cross-language.md`
  (alignment · corroboration · term handling · bilingual deliverables · non-entries); sources R120–R126
  (ISO 17100, ISO 5060, XLIFF 2.2, Halliday & Hasan, Vinay & Darbelnet, Nida & Taber, MQM). No
  `cross-language` capability (no language axis in the feature vector → would not discriminate).
- **Per-field information outlets** — new `outlets` group in `data/sources.json` (**68** curated
  entries: portals · journals · preprint servers · databases/registries · repositories · media) keyed by
  field via 17 new field `topic_ids`, each with `outlet_kind` + `why` + `not_for` + `verified` + `access`;
  new `reference/outlet-map.md` (field → outlet → why / NOT-for). Live view: `harness sources --group
  outlets`; 18 field domains link it. Verification honest: 46 URLs reachable (HEAD/GET 2026-10-19), 22
  blocked (403/405) recorded `verified: false` + note (*listed, not confirmed*).
- **Guards** — `tests/test_docs_integrity.py::LoadIndexWiringTest` (index paths resolve; entry docs link
  the new reference) and `tests/test_sources.py::OutletDataTest` (outlet shape + every field covered).
- **Harness compiler CLI** (`harness`): `derive` / `init` / `explain` / `check` — derive a task's
  feature vector (M0–M8 rules; optional LLM) and emit a runnable harness scaffold.
- **Self-update loop** (M5): `refresh` / `refresh-apply` — collect → audit → rank → proposal → journal,
  with a hard human gate; output under `updates/`.
- **Cross-project packaging**: user-space tool home (`HARNESS_HOME`, platform default), `doctor`,
  `self-update`; installable via `uv tool install`.
- **Intel tracking**: `data/sources.json` (59 entities: labs, vendor harnesses, venues, people,
  self-media) with RSS/Atom + YouTube feed collection → `updates/INTEL.md` / `intel.jsonl`.
- **Self-evolution**: `evolve` / `evolve-apply` — snapshot → audit → mutation-proposal → journal plus
  metrics (`updates/EVOLUTION.md`, `evolution.jsonl`, `metrics.jsonl`); discovery→registry proposals.
- **Run watermark**: effective `since` persisted to `updates/state.json` so cycles only surface new items.
- **Generated overviews**: `CAPABILITIES.md` (per capability) and **`HARNESS-MAP.md`** — the whole
  factory on one page (modules · capabilities · domains · catalog classes · CLI · how to sync), rendered
  from the CLI parser + skill index + `data/*.json` by `harness map --write`; both drift-guarded.
- **Workflow capabilities**: `loop-discipline` + `graph-orchestration` (22 → 24) — the agent-loop
  contract (termination · step budget · per-step ground truth · stall detection) and a declared
  topology (typed state · nodes/edges · fan-out/fan-in · per-node checkpoints); module clauses
  M2.10/M2.11 + M8.10; sources R93–R97.
- **Discipline coverage**: 3 new domains — `logic` (new `formal-sciences` faculty), `linguistics`,
  `cognitive-science` — each with a rubric, plus 3 cross-cutting capabilities `formal-verification`,
  `dimensional-analysis`, `empirical-measurement` sharing one new clause **M3.10** (match the instrument
  to the claim: machine-checked derivation / units & error / effect size & reliability); sources R98–R106.
- **Evidence instruments**: a new catalog class **`instruments`** (13 kinds, **27 entries**, catalog 133 → 160)
  for the tools those capabilities name — proof assistants (Lean 4/mathlib/Rocq/Isabelle/Agda/Dafny), solvers
  and checkers (Z3/cvc5/TLA+/Alloy), units & uncertainty (Pint/uncertainties), chemistry & biology
  (RDKit/Biopython/RCSB PDB/UniProt), language (Universal Dependencies/INCEpTION/ELAN), empirical work
  (PsychoPy/jsPsych/OSF/statsmodels/lme4/Stan) and pipelines (Snakemake/Nextflow) — plus
  **`reference/evidence-instruments.md`** (claim type → instrument → catalogued tool → gate evidence, with
  deliberate non-entries) and an **Evidence instrument** stanza in the emitted `AGENTS.md` so every generated
  harness states what would settle its claim; sources R107–R110.
- **Mathematics, statistics & methodology systems (P10)**: 2 new domains — `statistics` and
  `geometry-topology` (faculty `formal-sciences`) — with rubrics; 2 new capabilities
  `statistical-inference` (frame · convergence · interval) and `certified-computation`
  (exact/certified + independent re-derivation), grounded in the new clauses **M3.11**/**M3.12**;
  **23 new `instruments`** rows (catalog 160 → 183; kinds 46 → 50 — computer-algebra-system, sat-solver,
  geometry-topology-toolkit, causal-inference-toolkit) covering SageMath/Singular/Macaulay2/GAP/PARI-GP/OSCAR/SymPy,
  CaDiCaL, mathcomp/Metamath, CGAL/GUDHI/Regina/SnapPy/polymake, R/PyMC/NumPyro/ArviZ/brms/R-INLA/emcee and
  DoWhy; the **methodology layer** — `reference/methodology-map.md` (field → methodology system → what the
  harness must enforce) plus clause **M3.13** (declare the method and its assumptions; *no* `methodology-fit`
  capability, by design); and the scope roadmap `review/integration-map-2026-10.md`; sources R111–R119.
- **Pattern library**: `core/` (M0–M8), `domains/` (research/knowledge-management/data-science/devops),
  `review/` (survey, catalog, playbooks, references), `sources/` (provenance map).
- CI (GitHub Actions), `CHANGELOG.md`, `.gitattributes`.

### Changed
- **A closed roadmap item records `done_in`, not a revisit trigger** — a `done` entry is no longer a
  deferral, so `cycle.audit()` now requires `reason` + `revisit_when` only while the item is open and
  `done_in` once it ships; `harness cycle roadmap` renders `done in …`.

### Fixed
- **Pointer coverage (P11.1)** — `.harness/pointer.json` hard-coded only **4** entry docs, so an emitted
  harness could not reach `derivation-rules`, `evidence-instruments`, `methodology-map`, `cross-language`
  or `outlet-map` by pointer alone. `pointer.ENTRY_DOCS` is now **derived from the skill index**
  (the `overview` + `reference` groups; 4 → 12 docs) so it can never drift from `harness skill`, and
  `pointer.verify` checks them all (plus the emitted `AGENTS.md` pointer block states the full set).
- **Doc link integrity** — new guard: every relative markdown link in a shipped doc must resolve
  (an audit found 0 broken before the guard was added).

[Unreleased]: https://github.com/LengyanReader/research_foodie/commits/main
