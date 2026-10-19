# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Added
- **First round driven by the mechanism itself (P12, partial)** — the audit's 12 soft gaps were consumed,
  not restated: router rows for `portable-skills` and `reproducible-experiments` (capabilities that
  existed but were unreachable from the entry table), and `tests/test_capabilities.py::TriggerCoverageTest`
  (10 guards, each pinning a capability's declared trigger *and* the quiet vector it must not fire on).
  `harness cycle audit` now reports **0 hard problems and 0 gaps**.
- **M4.10 worked example** — `reference/cross-language.md` §7 carries a real EN↔ZH pair (the
  standing-reference block) through unit segmentation, a **rejected** first-pass drift hypothesis
  (widening the unit dissolved it), and two **real** defects: units 4 (declare the capability + file) and
  8 (M0.4 · M0.1/M0.2 · irreversible acts) were missing from all three Chinese renderings, and
  「只提案、不编造任务内容」 fused two units into a claim the English master does not make. Fixed in
  `AGENTS.md` §6, `GUIDE.md` and `introduction.md`; the master is untouched.
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
