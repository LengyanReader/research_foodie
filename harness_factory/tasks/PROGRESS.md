# PROGRESS · 进度日志

**Updated:** 2026-10-15

---

## 2026-10-15 — P2 (writing registered) + P3 runtime hooks + P4 plugin protocol (done)
- **Writing domain registered (P2 tail).** Added the `writing` entry to `data/domains.json` (faculty `humanities`, artifact `document`, grounding `required`, 9-step workflow, 20 signals — verified no signal collisions) and a weighted `writing` rubric to `data/rubrics.json`. `--domain writing` is now selectable, `standard --domain writing …` works, and `classify` reaches it by signals. Registered under the existing `humanities` faculty so the fixed `FACULTIES` test set is unchanged.
- **P3 — runtime hooks (new `runtime.py`).** **Gate runner** (`gate_report`, CLI **`gate`**): runs the structural self-check and **executes the emitted `.harness/check.py`** as its own hook; **hard** gates (manifest-valid, files-present, no-placeholders, check-py-runs) decide the exit code, while **advisory** module gates (M2/M4/M6/M8) report outstanding evidence (M0.3). **Signal harvest** (`harvest`/`record_signals`, CLI **`harvest`**): collects domain/modules/capabilities, gate outcomes, progress/ledger counts, and any agent-appended `.harness/signals.jsonl`, then appends **one** observation line to `<kb>/updates/signals.jsonl` — observe-only (M0.4/M5).
- **P4 — plugin protocol (new `plugins.py`).** Read-only discovery from `HARNESS_PLUGINS_DIR` (else `<data>/plugins`). **`domain`** plugins merge over the SSOT via `registry.domains()` + `standard.rubrics()` (`--domain <plugin-id>` becomes selectable) and may emit `extra_templates`; **`template`** plugins register reusable emitted files. Strict validation (id==dir, closed vocabularies, rubric weights sum ~1, template file present, no built-in shadowing) surfaced by CLI **`plugins [--validate]`**. The SSOT catalogs are never mutated; a plugin that shadows a built-in is reported and ignored.
- **Registry/standard caches** gained `clear_caches()` (used by tests and after a plugin-path change); `assemble.build_files` now emits a domain plugin's extra templates and lists them in `manifest.files`.
- **Tests:** +25 (`test_runtime.py`: gate pass/fail on fresh/tampered/missing/placeholder harnesses, advisory module gates, harvest bundle + JSONL record + custom signals; `test_plugins.py`: discovery, registry/rubric merge, classify reach, extra-template emission + check pass, validation for bad artifact/rubric/template/id/shadow/escape; `test_cli.py`: gate/harvest/plugins) → **128** passing.
- **Docs synced (task 1 — vibe-coding assistant usage).** `SKILL.md` rewritten with a clear "Using this repo as a skill · 把本仓库当作 skill 使用" section (L0 one-liner + concrete pasteable example + L0 checklist + variant-prompt table + L1 CLI block incl. gate/harvest + optional `install-skill.ps1` note); fixed `SKILL.md` cross-references in `README.md`/`README.zh-CN.md`/`harness_factory/README.md`/`GUIDE.md` (broken `harness_factory/harness_factory/…` and non-relative links); `GUIDE.md` command reference + Example 10 (runtime hooks & plugins) + roadmap; `tasks/PLAN.md`, `introduction.md`, `domains/writing/README.md` status, `AGENTS.md`/READMEs tree counts (23→24 disciplines).

## 2026-10-14 — P2: frontier-standard executable ratchet + writing domain (done)
- **Frontier-standard CLI.** New `standard.py` + CLI **`standard`**: `harness standard [--store F] --domain <D> bar|score|audit|raise|plan|frontier <objective>` over a bar ledger (default `updates/standard.json`). `bar` names a sourced apex bar (levels R1–R6); `score` records per-dimension scores on the domain rubric; `audit` prints weighted gaps largest-first; `raise` ratchets the floor (`floor_next = max(floor, achieved)`) and **refuses regressions** unless `--force`; `plan` turns gaps into a harness config; `frontier` records a re-check of a moving bar.
- **Per-domain rubrics.** `data/rubrics.json` (25 entries: `default` + every domain in `domains.json`) — weighted dimension tables per domain, so the same ratchet applies to code, math, law, medicine, the arts, etc.; unknown domains fall back to `default`.
- **Gap → lever map.** `data/levers.json`: each rubric dimension → the modules (M0–M8) and catalog tool-kinds that close it, anchored to Claude/Anthropic's documented practice where one exists; `standard plan` grounds its tool suggestions in `data/harnesses.json`.
- **Stale-frontier audit.** `evolution.audit` gains `stale_frontier`: an apex bar (R4+) not re-checked within `FRONTIER_MAX_AGE_DAYS` (90), or a floor with no named bar → proposal only (human-gated).
- **Excellence docs.** `domains/excellence/{standard-ladder.md,self-standard.md,security-model.md}` — the ratchet mechanism in detail; this project held to Anthropic's engineering bar (`standard --domain software-engineering plan harness-factory` → its own gap config); least-privilege / human-gate / reversibility security model.
- **Writing domain (doc-level).** `domains/writing/README.md` — citation-first essay harness for weak-spot writing (evidence/structure/originality): thesis→outline→context pack→forced claim→evidence pairing→originality check→clarity pass; humanities-aligned rubric. **Not yet registered** in `domains.json`/`rubrics.json` (SSOT) — registration is a pending decision, so `--domain writing` is not selectable in the CLI yet.
- **One-line agent directives (一句话指令词).** Paste-ready one-sentence prompts added to the main entry docs (root READMEs, `harness_factory/README.md`, `GUIDE.md`, `SKILL.md`) and to the excellence/writing domain READMEs.
- **Tests:** +17 (`test_standard.py`: rubric scoring, bar ledger roundtrip, ratchet no-regression, plan/levers, stale-frontier audit) → **103** passing.
- **Docs synced.** `GUIDE.md` (command reference, Example 9 ratchet walkthrough, test count), `harness_factory/README.md` (standard block + writing layout), root `README.md`/`README.zh-CN.md` (quickstart + standard), `domains/excellence/README.md`, `domains/writing/README.md`.

## 2026-10-12 — P1.8: agent-native mode + project learning (done)
- **Agent-native (L0/L1).** Added `SKILL.md` (front-matter + 4 cardinal rules + load-index + output contract + provenance requirement), `reference/derivation-rules.md`, `install-skill.ps1` (optional copy into a skills dir), and `skill.py` (`index`/`find`/`read`); CLI **`skill`** prints the load-index (`harness skill M4` prints one module). An assistant pointed at the repo + a task goal derives and emits the harness itself — no install.
- **Capability mechanism (requirement → harness).** `data/capabilities.json` (10 capabilities) + `capabilities.py` (feature match → annotate enabled modules); `spec.HarnessPlan.capabilities`; `derive` annotates. New requirements are added by editing JSON, not code. CLI **`capabilities`**.
- **Project profiling + mutual learning (project → factory).** `profile.py` scans a target project (stacks, tests/packaging, structure; observe-only) → `updates/profile/<slug>.{json,md}`; `learning.py` records **cases** (`updates/cases.jsonl`) and aggregates them. CLI **`profile`**, **`learn`**, **`cases`**; `--project` on `derive`/`init` wires a weak domain hint + optional `.harness/PROFILE.md`.
- **Evolution from cases.** `evolution.audit` gains `missing_capability` (a project capability recurring ≥2× but absent from the registry); `propose` emits an `add_capability` proposal; `run_evolution` loads cases via `learning.load_cases` (human-gated).
- **Provenance output.** `assemble` always emits `.harness/PROVENANCE.md` (derivation record; mark unverified); `AGENTS.md.tmpl` gains a capabilities section.
- **Packaging cancelled.** Locked with user: L0/L1 only; PyPI / `uv tool install` / pipx / zipapp / MCP dropped as distribution channels (`pyproject.toml` kept as dev/CI convenience). Decision in `tasks/DISTRIBUTION.md` §8; PLAN new consumption-model + requirement→harness + mutual-learning sections.
- **Docs synced.** `harness_factory/README.md`, root `README.md` + `README.zh-CN.md`, `introduction.md` (§9 agent-native & learning; §10 roadmap P1.8).
- **Tests:** +9 (`test_agent_mode.py`: skill index/read, capabilities match/annotate, profile scan, learning case roundtrip, mutual-learning missing_capability) → **71** passing.

## 2026-10-12 — P2 (partial): disciplines + unified harness catalog (done)
- **Disciplines expanded to 20.** `domains.json` now covers a faculty-level taxonomy: meta (research, knowledge-management, devops, general), engineering (software-engineering, engineering, data-science), natural-sciences (physics, chemistry, biology, earth-environment, mathematics), health (medicine), social-sciences (economics-finance, psychology, social-science), law, humanities, education, arts (arts-design). Added domain READMEs for all 19 non-general domains; `classify` picks a domain from signals (deterministic).
- **Unified harness catalog.** New `data/harnesses.json` (SSOT) — 55 entries across classes (coding/orchestration/self-evolution/memory/skills-protocols/evaluation/survey/safety), kinds (terminal-agent/ide-agent/sdk/protocol/self-modifying/evolutionary-search/weight-adaptation/inference-correction/skill-library/memory-system/benchmark/survey/safety-framework/skills-ecosystem), core-module maps, vendor/ecosystem, and `tracked` cross-links to `sources.json`. Unifies the conceptual taxonomy with vendor SDKs/CLIs (Claude Code, MCP, ADK, A2A, Gemini CLI, Agents SDK, etc.).
- **Catalog tooling.** `catalog.py` (load/search/filter/render/validate/write_index) + CLI `harness catalog` (`--class/--kind/--module/--vendor/--tag/--search/--tracked/--markdown/--write/--json` + `harness catalog <id>`). Generated `review/harness-index.md` from the data.
- **Discoverability.** `skill.py` derives domain entries dynamically from `domains.json`; added `harness-index` and `harnesses.json` to the load-index. `registry.py` falls back to bundled catalogs if user home lacks a file (keep checkout as SSOT).
- **Quality.** `tests/test_domains.py` (breadth, wellformedness, README presence, non-overlapping signals, classification smoke) and `tests/test_catalog.py` (validate clean, search/filter, tracked cross-links, index doc drift guard) added. All **86** tests pass.
- **Docs.** `README.md` + `README.zh-CN.md` + `introduction.md` + `core/00-index.md` + `tasks/PLAN.md` synced to reflect the 20-domain taxonomy and unified harness index.

- **Feed coverage:** probed + wired RSS/Atom feeds across the registry — **47/59 entities** now tracked (was ~20). `releases.atom` vs `commits.atom` chosen per repo; YouTube `@handle` → channel feed resolved and verified. 12 remain feedless by the honesty rule (no legitimate feed: ICML/ICLR/ACL/EMNLP/TMLR pages; a few people sites).
- **Watermark:** `refresh` persists the effective `since` to `updates/state.json` (`load_state`/`save_state`); repeated cycles surface only new items without re-passing `--since`.
- **Discovery→registry:** `evolution.audit` gains `queue_rows` and detects `untracked_source` (accepted candidate from an untracked host); `propose` emits `add_source` proposals; `run_evolution` loads `updates/queue.jsonl`.
- **Docs + scheduler:** `refresh.ps1` now runs `refresh --provider all --intel` then `evolve`; `introduction.md` + `tasks/PLAN.md` synced (sources/intel/evolve commands, P1.6/P1.7 milestones); stale legacy paths removed from `.gitignore`.
- **CI / packaging:** added `.github/workflows/ci.yml` (ubuntu+windows × 3.10/3.12), `CHANGELOG.md`, `.gitattributes`; `pyproject.toml` classifiers + `project.urls`.
- **Tests:** +12 (`test_cli.py` end-to-end CLI, `test_sources.py` registry validation, plus watermark + untracked-source cases) → **62** passing.
- Fixed a data bug: `langchain` topic `tool-surface` → canonical `agent-skills-tools`.

## 2026-10-12 — P1.7: intel tracking + self-evolution (done)
- Added `data/sources.json`: tracked-entity registry with 5 groups — **projects** (OpenAI, Anthropic, Google DeepMind, Meta, Mistral, DeepSeek, Moonshot/Kimi, …), **harnesses** (Agents SDK, Swarm, Codex, Claude Code, MCP, Claude Agent SDK, ADK, Gemini CLI, A2A, Llama Stack, Mistral Agents, …), **venues** (Nature/Science/NeurIPS/ICML/ICLR/ACL/arXiv), **people** (Karpathy, Ilya, LeCun, Hassabis, …), **media** (Substack/YouTube/newsletters). 59 entities.
- `collect.py`: RSS 2.0 + Atom `parse_feed`, `http_get`, `iter_entities`, `resolve_youtube_feed` (`@handle` → channel feed), `feed_provider`; `Candidate.entity` added.
- `extract.py`: deterministic intel (relevance = topic keywords + entity mention + recency, topic/entity tagging, verbatim brief); optional LLM summary; writes `updates/INTEL.md` + `intel.jsonl` (grouped projects/harnesses/venues/people/media).
- `llm.py`: refactored to `_chat_content` + added `summarize()`.
- `evolution.py`: complete cycle **snapshot → audit → mutation-proposal → journal** + metrics (`updates/EVOLUTION.md`, `evolution.jsonl`, `metrics.jsonl`); human-gated `apply_accepted` → `updates/accepted.json` (reversible). Audits: uncovered topics, empty groups, stale sources.
- `refresh.py`: `load_sources`, feed provider support, `--intel` extraction wired in; summary gains `intel_items`.
- CLI: **`sources`**, **`intel`**, **`evolve`**, **`evolve-apply`**; `refresh --provider {auto,file,llm,feed,all}` + `--intel` + `--sources`.
- Rewrote root `README.md` + `README.zh-CN.md` (project intro + tool usage; archived old content); synced `harness_factory/README.md`.
- Tests: +14 (`test_intel.py`: feed parse/resolve/provider, intel scoring/enrich/write, evolution snapshot/audit/propose/run/apply/dry-run) → **49** passing.

## 2026-10-12 — P1.6: cross-project packaging (done)
- Evaluated tool forms → `tasks/DISTRIBUTION.md`; wrote `introduction.md`.
- Locked with user: primary = **installable package via `uv tool install`**; state = **user data dir**; channel = **git-only first**; names = pkg `harness-factory`, cmd `harness`.
- Added `config.py` (tool home resolution: `HARNESS_HOME` → platform default; optional `config.toml`; catalog/corpus/updates dirs; seeding; corpus-root resolution).
- `registry.py` now prefers the user catalog (`HARNESS_DATA_DIR` → user catalog → bundled).
- `refresh` re-rooted: corpus from checkout `review/` if present else home `corpus/`; CLI `refresh`/`refresh-apply` default to the **user home** (`--root`/`--data-dir` override).
- New CLI: **`doctor`** (paths/config/seed/LLM) and **`self-update`** (re-seed tool catalog; non-destructive, journaled, `--force`).
- `init --out` defaults to `./<task-slug>`.
- `.gitignore`: exclude `harness_factory/_archive/` and `harness_factory/updates/` from version control.
- Verified from an arbitrary directory with isolated `HARNESS_HOME`: doctor/self-update/refresh/init all work; emitted harness self-check OK.
- Tests: +7 (`test_config.py`) → **35** passing.

## 2026-10-12 — P1.5: self-update loop (done)
- Added the M5 self-update subsystem: `refresh` (collect → audit → rank → proposal → journal) and `refresh-apply` (human gate).
- New modules: `collect.py` (Candidate + file/llm providers, `verify_url`), `curate.py` (audit/dedupe/score/trends), `journal.py` (report/queue/proposal writers + append-only journal), `refresh.py` (orchestrator + apply gate).
- `llm.py`: added `discover_items()` (env-gated, returns untrusted items; always audited).
- `data/watchlist.json`: 8 topics + 4 frontier probes (boundary expansion).
- CLI: `harness refresh` (`--root/--inbox/--watchlist/--provider/--since/--verify/--dry-run/--json`) and `harness refresh-apply --accept`.
- `refresh.ps1` + `tasks/REFRESH.md`: weekly scheduling (Task Scheduler / cron / GitHub Actions) and the human gate.
- **Guardrails honored:** provenance gate drops untraceable items (M4); observe-only (M0.4); human gate (M0.8); all output under `updates/`, append-only journal, fully reversible (M0.9).
- Tests: 28 total (`test_refresh.py` adds provider roundtrip, injected LLM discovery, dedupe/score, dry-run, apply-by-index, corpus key extraction).

## 2026-10-12 — P1: inclusive harness CLI (done)
- Locked decisions with user: CLI scaffolder · hybrid rules+LLM · Python · MVP = task→harness generator.
- Wrote `tasks/PLAN.md` (architecture, derivation model, milestones, risks).
- Built the package: `pyproject.toml`, `spec.py`, `registry.py`, `derive.py`, `classify.py`, `llm.py`, `render.py`, `assemble.py`, `check.py`, `cli.py`, `__main__.py`, `data/{modules,domains}.json`, 8 templates.
- Fixed: `__init__.py` now sources `__version__` from `_version.py` (SSOT); CLI forces UTF-8 output (Windows cp1252 console crash on `title_zh`); removed a literal `{{` from emitted gate text that would have tripped the self-check.
- Verified end-to-end: `harness init --task "..."` → 8 files, `harness check` OK.
- Tests: 21 unittest cases (derive rules, classify, assemble/check). All pass.

### Notes
- Python available: 3.12.9 (miniconda). `pytest` not installed → tests use stdlib `unittest` to stay dependency-free.
- Tool self-constraint: M0.4 (observe/classify/emit only; never fabricate task substance).
- Run tests: `$env:PYTHONPATH="src"; python -m unittest discover -s tests`.
