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
- **Pattern library**: `core/` (M0–M9), `domains/` (research/knowledge-management/data-science/devops),
  `review/` (survey, catalog, playbooks, references), `sources/` (provenance map).
- CI (GitHub Actions), `CHANGELOG.md`, `.gitattributes`.

[Unreleased]: https://github.com/LengyanReader/research_foodie/commits/main
