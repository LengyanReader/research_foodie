# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Added
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

### Fixed
- **Pointer coverage (P11.1)** — `.harness/pointer.json` hard-coded only **4** entry docs, so an emitted
  harness could not reach `derivation-rules`, `evidence-instruments`, `methodology-map`, `cross-language`
  or `outlet-map` by pointer alone. `pointer.ENTRY_DOCS` is now **derived from the skill index**
  (the `overview` + `reference` groups; 4 → 12 docs) so it can never drift from `harness skill`, and
  `pointer.verify` checks them all (plus the emitted `AGENTS.md` pointer block states the full set).
- **Doc link integrity** — new guard: every relative markdown link in a shipped doc must resolve
  (an audit found 0 broken before the guard was added).

[Unreleased]: https://github.com/LengyanReader/research_foodie/commits/main
