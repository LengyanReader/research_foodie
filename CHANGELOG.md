# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Added
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
- **Pattern library**: `core/` (M0–M8), `domains/` (research/knowledge-management/data-science/devops),
  `review/` (survey, catalog, playbooks, references), `sources/` (provenance map).
- CI (GitHub Actions), `CHANGELOG.md`, `.gitattributes`.

[Unreleased]: https://github.com/LengyanReader/research_foodie/commits/main
