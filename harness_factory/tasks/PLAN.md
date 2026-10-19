# PLAN · Inclusive Harness Tool · 通用 harness 工具计划

**Updated:** 2026-10-18 · **Status:** active · **Owner:** user + agent

> Goal: turn `harness_factory/` from a pattern **library** into a working **harness compiler** — given any task, emit the harness that task needs.
> 目标：把 `harness_factory/` 从模式**库**升级为可运行的**harness 编译器**——给定任意任务，产出该任务所需的 harness。

---

## 中文速览

**决策（已确认）。** 形态 = **CLI 脚手架工具**；选配逻辑 = **规则为主 + LLM 辅助**；实现 = **Python**；首个里程碑 = **「任务 → harness 脚手架」生成器**（覆盖现有 4 域 + general，选择可解释、带验证门）。

**核心机制。** `task → intake → feature vector → selection → assembly → emitted harness`。harness 由**任务特征向量**（horizon / verifiability / stakes / grounding / artifact / tool_surface / collaboration / domain）**推导**出来，而不是由固定枚举决定——这是「inclusive」的来源。选择结果写入 `.harness/manifest.json`，可解释、可复核。

**自我约束（M0）。** 工具本身遵守 M0.4：只做**分类 / 推荐 / 生成**，绝不编造任务实质内容；每次推导给出理由（rule that fired）。

---

## Scope · 范围

**In scope (MVP).**
- `harness derive` — from a task (text or flags) → a HarnessPlan, printed as text/JSON, with per-module reasons.
- `harness init` — write the concrete scaffold into an output dir.
- `harness explain` — read a `manifest.json` and explain the selection.
- `harness check` — run the emitted harness's self-check gate (M0.3).
- `harness refresh` — the self-update loop: pull new/leading sources, audit + dedupe
  against the corpus, rank, and write a bilingual report + queue (proposal only).
- `harness refresh-apply` — human gate: accept queued candidates into merge stubs.
- `harness sources` — list tracked entities (projects/harnesses/venues/people/media).
- `harness intel` — pull tracked RSS/Atom/YouTube feeds → `updates/INTEL.md` (scored, tagged; optional LLM brief).
- `harness evolve` / `harness evolve-apply` — self-evolution audit → mutation proposals → human gate.
- `harness skill [<name>]` — print the agent load-index (or one module/doc) so a vibe-coding
  assistant pointed at this path can consume the factory as an agent-native skill (no install).
- **Standing reference** (`SKILL.md` §"PASTE THIS EXACT INSTRUCTION"; mirrored in both root READMEs and the
  workspace `AGENTS.md`) — paste once; active for the whole conversation; durable in the target's rules
  file; revoked by "stop using harness_factory". The emitted `AGENTS.md` carries the same convention.
- `reference/capability-router.md` — the entry for external tasks: *situation → capability → module → file*
  (load only what the matched row names).
- `reference/requirement-refinement.md` — R0–R5 (restate → elevate → classify constraints → offer
  MVP/Elevated/Exploratory → confirm → converge) run **before** deriving, so an under-aimed ask is raised,
  not tooled.
- `reference/capability-flow.md` — the **bidirectional** loop: concretise a capability into the task's own
  `.harness/capabilities.local.md`; distill only generalisable patterns back as human-gated proposals.
- `harness profile --project DIR` — scan a target project → `PROFILE.md` + capabilities (observe-only).
- `harness learn` / `harness cases` — record / review learned project cases (project → factory learning).
- `harness catalog [<id>] [--class/--kind/--module/--vendor/--tag/--search/--tracked/--markdown/--write/--json]` — unified harness catalog: list/search/filter; `--write` regenerates `review/harness-index.md`.
- `harness standard [--store F] --domain D bar|score|audit|raise|plan|frontier <name>` — the frontier-standard ratchet over a per-domain weighted rubric (`data/rubrics.json`); `raise` refuses regressions (unless `--force`); `plan` maps gaps → modules + catalog tools (`data/levers.json`).
- `harness doctor [--project DIR]` / `harness self-update` — path/config/LLM status; with `--project`, verify the target's `.harness/pointer.json` resolves (and whether its rules file carries the standing reference); re-seed the tool's own catalog (non-destructive).
- Deterministic rule engine over M0–M8 + capability map + 4 domains + general.
- Optional LLM classifier (off by default; plugs in via env config).

**Out of scope (later phases).**
- Live runtime that enforces gates during work (Phase D).
- Autonomous self-evolution of user projects (Phase D/E).
- Plugin marketplace for third-party domains (Phase E).

---

## Architecture · 架构

```
harness_factory/
  pyproject.toml                 packaging (src layout, console script `harness`)
  refresh.ps1                    scheduler entry (Task Scheduler / cron; see tasks/REFRESH.md)
  src/harness_factory/
    spec.py        TaskSpec · FeatureVector · ModulePlan · HarnessPlan (dataclasses)
    config.py      tool home / catalog / corpus / updates resolution; seed catalog
    data/
      modules.json   module catalog M0–M8 (id, titles, rule)
      domains.json    domain catalog (27 disciplines + `general`; faculty taxonomy)
      harnesses.json  unified harness catalog (183 entries: class × kind × module-map × vendor)
      rubrics.json    per-domain weighted excellence rubric (`default` fallback)
      levers.json     rubric dimension -> modules (M0–M8) + catalog tool-kinds that close it
      watchlist.json  refresh topics + frontier probes (M5 signal source)
      sources.json    tracked entities (projects/harnesses/venues/people/media/libraries/tools) + feeds
      capabilities.json  requirement -> capability -> modules map (extensible, data-driven)
    derive.py      FeatureVector -> HarnessPlan   (explainable rule table + capability annotation)
    classify.py    task text -> FeatureVector      (rules; optional LLM)
    capabilities.py  load capability map; match(features) -> active capabilities + module reasons
    harness_map.py  whole-factory map (HARNESS-MAP.md): modules/capabilities/domains/CLI, generated
    catalog.py     load/search/filter/render/validate/write_index over data/harnesses.json
    standard.py    frontier-standard ratchet: bar ledger, rubric scoring, gap audit, raise (no regress), plan
    skill.py       agent load-index: index / find / read (SKILL.md + core + data + domains)
    llm.py         OpenAI-compatible classify + discover + summarize (stdlib urllib), env-gated
    render.py      tiny {{key}} template engine (no deps)
    pointer.py     the emitted .harness/pointer.json: build/verify a project's link back to this factory
    assemble.py    HarnessPlan -> files on disk
    check.py       validate an emitted harness against its manifest (gate)
    runtime.py     runtime hooks: gate_report (structural + runs the emitted check.py); harvest/record_signals (observe-only)
    plugins.py     third-party domain/template plugin discovery + validation (merged read-only over the SSOT)
    collect.py     refresh/intel: Candidate + file/llm/feed providers; RSS/Atom parse; YouTube resolve
    curate.py      refresh: audit / dedupe / score / trends (observe-only)
    journal.py     refresh: report / queue / proposal writers (append-only journal)
    extract.py     intel: candidates -> scored intel (INTEL.md + intel.jsonl)
    evolution.py   self-evolution: snapshot -> audit -> proposal -> journal + metrics; apply gate
    profile.py     project scan -> ProjectProfile (stacks/capabilities) + PROFILE.md (observe-only)
    learning.py    project cases: record / load / aggregate (project -> factory mutual learning)
    refresh.py     refresh: orchestrate signal->audit->proposal->journal; apply gate; watermark
    cli.py         argparse: derive / init / explain / check / gate / harvest / plugins / profile / skill / refresh / refresh-apply / sources / intel / evolve / evolve-apply / learn / cases / standard / catalog / doctor / self-update / capabilities / map
    __main__.py    python -m harness_factory
    templates/     AGENTS.md, tasks/*, .harness/* (incl. PROVENANCE.md), check.py
  SKILL.md         agent-native entry point (cardinal rules + load-index + output contract)
  CAPABILITIES.md  generated capability overview (purpose + every capability; `harness capabilities --write`)
  HARNESS-MAP.md   generated whole-factory map (modules/capabilities/domains/CLI; `harness map --write`)
  reference/       derivation-rules.md (markdown mirror of the rule table, for L0 agents)
  install-skill.ps1  copy repo-as-skill into a skills dir (optional global install)
  tests/           stdlib unittest (no deps)
  tasks/           PLAN.md · PROGRESS.md · REFRESH.md · DISTRIBUTION.md · ASSESSMENT.md
  updates/         cycle output (queue.jsonl · REPORT.md · JOURNAL.md · INTEL.md · EVOLUTION.md · metrics.jsonl · cases.jsonl · profile/ · proposals/)
```

## Derivation model · 推导模型

**Feature vector → modules + parameters (rules), reasons logged.**

| Module | Enabled when | Key params |
|---|---|---|
| M0 Meta-principles | always | — |
| M1 Context | always | context policy |
| M2 Long-running/memory | horizon ≥ session | memory_depth |
| M3 Verification/gates | always | gate_strictness |
| M4 Provenance | grounding ≥ preferred, or artifact ∈ {document, dataset, knowledge_base} | provenance |
| M5 Self-evolution | horizon ≥ multi_session | evolution_cadence |
| M6 Tools/skills | tool_surface ≠ none | tool policy |
| M7 Governance | always | commit policy |
| M8 Collaboration | collaboration ≠ solo or stakes = high | autonomy |

**Parameters (derived).**
- `gate_strictness`: strict if verifiability low OR stakes high; relaxed if verifiability high AND stakes low; else standard.
- `autonomy`: low if stakes high OR verifiability low; high if stakes low AND verifiability high; else medium.
- `memory_depth`: session if horizon = session; durable if ≥ multi_session.
- `evolution_cadence`: per_session if multi_session; periodic if long_running.

## Consumption model · 消费形态（P1.8）

| Level | Form | Install | Determinism | Use |
|---|---|---|---|---|
| **L0** agent-native | assistant reads `SKILL.md` + `core/` + `data/*.json`, derives itself | none | model-dependent | any file-reading Vibe-coding assistant |
| **L1** CLI-from-path | `PYTHONPATH=<path>/src python -m harness_factory derive …` | none | high | reproducible without install |
| **L2** installed | `uv tool install` → `harness …` | yes | high | **cancelled as a distribution channel** |

### Requirement → harness mechanism · 需求配置机制
`requirement → FeatureVector (rules/LLM) → capability match (data/capabilities.json) → modules + params`.
Capabilities are data-driven entries `{id, title_en/zh, when, modules, why}`; new requirements are added by
editing JSON, not code. The derivation always records which capability and which rule fired.

### Mutual learning · 相互学习
`project → profile (observe-only) → case (features+capabilities+modules) → updates/cases.jsonl`.
`evolution` audits cases: a capability recurring across projects but missing from the registry becomes a
`missing_capability` proposal (human-gated) — projects teach the factory, the factory's next harness is
better, and capabilities discovered in one project become reusable options for others.

## Milestones · 里程碑

### Next session worklist · 下次工作单（排定于 2026-10-19）

Machine-readable source of record: `harness cycle roadmap` (`data/cycles.json`). This table is a pointer to it, not a second SSOT. The user asked for the *remaining* work to be parked here rather than restated in chat, so the next session can pick it up cold.

| id | cycle | what | why it is still open |
|---|---|---|---|
| **P12.1** | P12 | End-to-end emitted-harness job in CI on linux + windows (`init → check → gate → harvest → pointer verify`) | CI claims coverage it does not run (ASSESSMENT A.3 #7) |
| **P12.2** | P12 | Opt-in network job (`workflow_dispatch` only) running `refresh --dry-run` + `intel --provider feed --verify` | the network paths are untested by design offline, so they are never exercised at all |
| **P12.3** | P12 | **M2.12** — declared memory backend + resume protocol + an emitted Memory stanza (the P9 evidence-instrument stanza is the precedent) | M2 externalises memory as a rule but ships no backend posture |
| **P12.4** | P12 | Re-verify the 22 `verified: false` outlets by a method bot protection does not block → flip, or record a permanent `listed` rationale | 22 outlets were listed, not confirmed |
| **P12.6** | P12 | Clear the **17** roundup-only items (12 numbers + 5 affiliations) by opening the PDFs | the repo may not cite what it has not read; the group L rows are abstract-level only |
| **P12.7** | P12 | **Bounded backfill**: 8 weeks of *Top AI Papers of the Week* → a searchable inventory (Pass A). Pass B (deep verification) only if Pass A shows a hit rate worth the cost | full-history backfill costs more than it is worth; recent weeks are on-axis |
| **P14.1** | P14 | Verify the gazetteer paper's **primary source** and read what the web rendering hides (stage prompts, P/R/F1 table, mechanism comparison are all images) | every number quoted from it is currently unverifiable |
| **P14.2** | P14 | Mechanism-by-mechanism **crosswalk** against existing clauses/capabilities, with a covered / partially / gap verdict each | a mapping that only restates the library adds nothing |
| **P14.3** | P14 | Land **only what discriminates** (proposal-first) and record the non-additions | candidates: a clause on evidence-tagged output, a digital-humanities domain assembly, or an M4.10-style worked example |

Detail for the sourcing items: `updates/2026-10-19-paper-roundup-proposal.md` (loop product, deliberately not under version control). Detail for the case study: `updates/2026-10-19-domain-harness-case-study-plan.md`.

- **P0 (done):** pattern library (`core/`, `domains/`, `review/`, `sources/`).
- **P1 (done):** CLI scaffold generator — `derive`/`init`/`explain`/`check`, rules engine, tests.
- **P1.5 (done):** self-update loop (M5) — `refresh`/`refresh-apply`, watchlist, curate, journal, scheduler, tests.
- **P1.6 (done):** cross-project packaging — user-home KB (`HARNESS_HOME`), `doctor`, `self-update`, re-rooted `refresh`; `uv tool install`.
- **P1.7 (done):** intel tracking (`sources.json`, feed/YouTube collection, `extract.py`) + self-evolution (`evolution.py`, metrics, proposal gate); CLI `sources`/`intel`/`evolve`/`evolve-apply`; run watermark.
- **P1.8 (done):** agent-native mode + project learning. Cancelled packaging as a distribution channel (PyPI/`uv tool install`); primary = agent-native skill (`SKILL.md` + `harness skill`) + CLI-from-path (L1). Data-driven **capability mechanism** (`capabilities.json`), **project profile** (`profile.py`), **mutual learning** (`learning.py` cases + `missing_capability` audit).
- **P2 (active):** comprehensiveness + discoverability.
  - **Disciplines · 学科门类（~20）:** expand `domains/` from 4 to a faculty-level taxonomy — natural sciences (physics, chemistry, biology, earth-environment, mathematics), engineering (engineering, software-engineering, devops), health (medicine), social sciences (economics-finance, psychology, social-science), humanities (humanities), law, business/education/arts (education, arts-design). Each = `domains/<id>/README.md` + `domains.json` entry (artifact/grounding/signals). Adds no new rules — features stay compositional (M0.5).
  - **Harness index · harness 索引:** a unified, machine-readable catalog `data/harnesses.json` (183 entries; classes × kinds × core-module maps × source), cross-linked to `sources.json` by id; `catalog.py` + CLI `harness catalog` (list/search/filter/`--json`); generated `review/harness-index.md` with a drift-guard test. Prose taxonomy in `review/harness-catalog.md` stays as the explanation; the index is the lookup surface.
  - **Agent Skills conformance + ecosystem integration · 可移植技能与生态整合 (done, 2026-10-15):** M6 emits `.harness/skills/<name>/SKILL.md` in the open **Agent Skills** format; **Hermes Agent** + peers tracked in `data/sources.json`/`data/harnesses.json`; new capabilities **`sandboxed-execution`** + **`portable-skills`**; ecosystem subsection `review/harness-catalog.md` §5a. See `tasks/ASSESSMENT.md` §B for the review and B.6 for status.
  - **Generated capability overview · 能力总览 (done, 2026-10-15):** `harness_factory/CAPABILITIES.md`, generated from `data/capabilities.json` + `modules.json` (`harness capabilities --write`; also refreshed by `harness catalog --write`), drift-guarded by a test — so it auto-evolves with the SSOT.
  - **Whole-factory map · 全景地图 (done, 2026-10-18):** `harness_factory/HARNESS-MAP.md`, generated by `harness map --write` (`harness_map.py`) from the CLI parser, the skill index, `templates/` and the catalogs — §0 counts, §3 modules, §4 capabilities, §5 domains, §6 catalog classes, §7 CLI, §8 entry points, §9 SSOT→view, §10 how to sync. `harness catalog --write` refreshes it too; `tests/test_harness_map.py` guards staleness.
  - **Workflow patterns · 工作流模式 (done, 2026-10-18):** `loop-discipline` + `graph-orchestration` capabilities (**22 → 24**) distilled from bare primary sources — Anthropic *Building effective agents* (`[R93]`), ReAct (`[R94]`), Reflexion (`[R95]`), ADK graph workflows (`[R96]`), LangGraph persistence (`[R97]`). Module clauses **M2.10** (loop contract), **M2.11** (declared control graph), **M8.10** (declare the topology); `langgraph.maps_to` corrected `M6,M7` → `M2,M6,M7,M8`; audit + coverage matrix in `review/workflow-patterns-2026-10.md` §3.
  - **Disciplines crosswalk · 学科交叉 (done, 2026-10-18):** **3 domains** `logic` (new faculty `formal-sciences`) · `linguistics` · `cognitive-science` (each + `domains/<id>/README.md` + rubric) and **3 evidence-instrument capabilities** `formal-verification` · `dimensional-analysis` · `empirical-measurement` (**24 → 27**), all grounded in the new clause **M3.10** (match the instrument to the claim). Sources `[R98]`–`[R106]`; coverage matrix + non-additions in `review/disciplines-crosswalk-2026-10.md`.
  - **Frontier standard · 最高标准棘轮 (done):** `excellence` domain + `standard-ladder.md`; per-domain weighted rubrics (`data/rubrics.json`, `default` fallback) and the gap→lever map (`data/levers.json`); executable ratchet `standard.py` + CLI `harness standard bar|score|audit|raise|plan|frontier` (refuses regressions); `stale_frontier` audit in `evolution.py`; applied reflexively in `self-standard.md` + `security-model.md`.
  - **Writing domain · 写作域 (done):** `domains/writing/README.md` + registered `writing` entry in `data/domains.json` (faculty `humanities`, artifact `document`, grounding `required`, 20 signals) and a weighted rubric in `data/rubrics.json` — citation-first essay harness (thesis→outline→context pack→claim↔evidence→originality→clarity). `--domain writing` is now selectable; `standard --domain writing` works; classification reaches it. · 写作域已注册。
  - **LLM-assisted discovery/classification hardening** and **feed/entity coverage expansion** — deferred to a later P2 slice.
- **P3 (done):** emitted-harness runtime hooks. `runtime.py` — **gate runner** (`gate_report`, CLI `harness gate`): structural check + executes the emitted `.harness/check.py` as its own hook; hard gates decide pass/fail, module gates (M2/M4/M6/M8) are advisory. **Signal harvest** (`harvest`/`record_signals`, CLI `harness harvest`): observe-only, appends one observation to `<kb>/updates/signals.jsonl`.
- **P4 (done):** plugin protocol for new domains/templates. `plugins.py` — read-only discovery from `HARNESS_PLUGINS_DIR` (or `<data>/plugins`); `domain` plugins merge into the registry + rubrics (`--domain <plugin-id>` becomes selectable) and may emit extra templates; `template` plugins register reusable emitted files. Strict validation + CLI `harness plugins`. SSOT catalogs are never mutated; a plugin may not shadow a built-in.
- **P7 (done, 2026-10-18):** frontier capability refresh — distil 2026 frontier work into the capability SSOT. Verified primary sources (`review/references.md` §E, R84–R92): context rot (Chroma R84), lethal trifecta + OWASP *Top 10 for Agentic Applications 2026* `ASI01–ASI10` (R42, R86), MCP security best practices (R87), CaMeL (R88), durable execution (Temporal R90 + METR R89), hard budget caps (Willison R85), step-level evaluation (R92) + OpenTelemetry GenAI conventions (R91). **5 new capabilities** — `context-budget-policy`, `untrusted-content-discipline`, `durable-execution`, `cost-budget-caps`, `eval-driven-development` (**17 → 22**, data-only) — with distinct triggers, plus router rows, a provenance row per capability, and the distillation `review/frontier-2026-10.md`. Deliberate non-additions recorded (agent identity, A2A, OTel status). Run `PYTHONPATH=src python -m harness_factory capabilities --write`.
- **P11 (done, 2026-10-19):** **cross-language meaning units + per-field information outlets.** *Slice 1 — cross-language 意群 fidelity (the user's standing ask: accurate exchange and mutual corroboration at the level of whole meaning units, not word-for-word translation):* new clause **M4.10** in `core/05` (align by **meaning unit** — 意群 / sense group / translation unit — not word or surface sentence; **mutually corroborate** a claim carried across languages instead of assuming word-match = meaning-match; preserve stance/scope/modality; **gloss, never silently substitute**), + checklist + anti-pattern *word-for-word fidelity*; new **`reference/cross-language.md`** (meaning-unit alignment procedure, mutual-corroboration protocol, term-handling, deliberate non-entries); load-index + router + `SKILL.md` step wiring; sources group **K**. **No `cross-language` capability** — the feature vector has no language axis, so it could not discriminate (recorded as a deliberate non-addition). *Slice 2 — per-field information outlets/portals/media (the user's standing ask):* a new **`outlets` group** in `data/sources.json` — ~60 curated, first-party, reachability-checked entries (portals · journals · preprint servers · databases/registries · data repositories · media) keyed by field via domain-id `topics`, each with `outlet_kind` + `why` + `not_for` + `verified` + `access`; new **`reference/outlet-map.md`** (field → outlets → what/why high-quality/not-for + deliberate non-entries); field READMEs point at their rows; the live view is `harness sources --group outlets`. Guards: `tests/test_sources.py`. 跨语言意群对齐 + 各领域信息源地图。**Shipped (2026-10-19):** **68** outlets (not ~60); guards `tests/test_docs_integrity.py::LoadIndexWiringTest` + `tests/test_sources.py::OutletDataTest`; plus two follow-ups — **P11.1** (the emitted `.harness/pointer.json` `entry_docs` is now **derived from the skill index**, 4 → 12 docs, so a generated harness can reach every loadable doc) and **P11.2** (the five usage rules + the one-instruction standing reference live in the root READMEs). **193 tests.**
- **P12 (active, started + partially shipped 2026-10-19):** **evidence-driven loop + CI hardening + P11 closeout.** Every slice closes a *recorded* gap (A.3 · integration-map §3) and lands a **checkable mechanism**, not prose.
  - **Slice 0 · the first audit worklist (done).** P13's audit produced 12 soft gaps; this round consumed them instead of restating them: two **router rows** (`portable-skills`, `reproducible-experiments` — capabilities that existed but were unreachable from the entry table) and **explicit trigger guards** for the 10 capabilities no test named (`tests/test_capabilities.py::TriggerCoverageTest`, each pinning the declared trigger *and* the quiet vector it must not fire on). **Audit gaps 12 → 0.** The audit's own roadmap rule was corrected at the same time: a `done` item now records `done_in` instead of a `revisit_when`, since a closed item is not a deferral.
  - **Slice 3a · M4.10 shown, not stated (done, roadmap P12.5).** One real EN↔ZH pair — the standing-reference block — carried through `reference/cross-language.md` §7: master segmented into 8 units, a first-pass "drift" **rejected** by widening the unit (revoke condition), and **two real defects found**: units 4 (declare the capability + file) and 8 (M0.4 · M0.1/M0.2 · irreversible acts) were missing from the compressed Chinese renderings, and 「只提案、不编造任务内容」 had fused two units into a claim the master lacks. Fixed in `AGENTS.md` §6, `GUIDE.md`, `introduction.md` — master untouched.
  - **Slice 3a-bis · the renderings the user actually pastes (done).** The first sweep fixed the guides but missed the two **READMEs**; a user pasting the block back exposed it. Then the user raised the location itself: the block assumed `./harness_factory`, but the repo is *cloned* wherever the reader wants it, so the factory location must be a **parameter** (`<HF>` = the real path of the cloned `harness_factory/`), not an assumption. All **eight** renderings (2 README quick-starts · 2 full README templates · `AGENTS.md` §6 · `GUIDE.md` · `introduction.md` · `SKILL.md`) now carry units 4/5/8, name `harness check --dir <output>` (with the no-install form), and mark the path parameter; `SKILL.md` keeps its own wording and cross-references `<HF>`. Guard: `tests/test_standing_reference.py::QuickStartFidelityTest` (5 cases) asserts per *block*, not per file.
  - **Slice 1 · CI covers what it claims.** `.github/workflows/ci.yml` gains an **end-to-end emitted-harness job** on both OSes (`init → check → gate → harvest → pointer verify`) and an **opt-in network job** (`workflow_dispatch` only, never on push) running `refresh --dry-run` + `intel --provider feed --verify`, so the offline-by-design paths are exercised on demand. *Closes A.3 #5/#7.*
  - **Slice 2 · M2 made concrete (memory backend).** Apply the evidence-instrument precedent (P9 template stanza) to memory: new clause **M2.12** (declare the memory backend + resume protocol) and an emitted **Memory** stanza in `templates/AGENTS.md.tmpl` derived by `assemble` from the matched capabilities; a `reference/` note names the backend options (file ledger · sqlite · external store) and what each must guarantee. *Closes A.3 #4.* **Non-addition:** no memory *runtime* is shipped — the harness declares the posture; the tool does not impersonate a store.
  - **Slice 3 · P11 closeout.** (a) Re-verify the 22 `verified: false` outlets by a method not blocked by bot protection → flip or record a permanent `listed` rationale; (b) ✅ **done in Slice 3a** — one real **EN↔ZH worked example** in `reference/cross-language.md` §7 (source unit → coordinated rendering → back-translation diff) using an artifact from this repo, so **M4.10 is shown, not only stated**.
  - **Deferred, with reasons (recorded — not dropped):** trace-driven self-evolution (needs a design doc first; the largest remaining gap, A.3 #2) · spectra/crystallography instruments (per-database licence/API verification, integration-map §1c) · a `qualitative-rigour` capability (needs a feature-vector affordance first, §3 #1–#2) · outlet *feeds* in the intel loop (outlets stay reference by design).
- **P13 (done, 2026-10-19):** **the capability round as a mechanism.** The ask: every round of capability expansion / deepening / update / evolution needs a *systematic* mechanism, so the capability set can grow perpetually. Recon first (M0.5): `refresh` (entities), `evolve` (mutation proposals) and `capability-flow` (per task) already exist — what was missing was **the round itself**.
  - **Slice 1 · the registry.** `data/cycles.json`: 9 rounds (`baseline` → `P13`) with git-verified `added` ids; the **definition-of-done as data** (7 axes, each flagged hard or soft); **11 roadmap items**, each with `reason` + `revisit_when` + `source`. Counts for scale (`catalog_delta`), ids for verification.
  - **Slice 2 · the audit.** `cycle.py` + CLI `harness cycle [list|show|audit|roadmap|dod]`. `audit` splits **hard problems** — phantom ids, a clause not anchored in its own `core/` doc, a `when` predicate the engine cannot evaluate (`any` / `min_horizon` / feature axis / `domain`), a deferral with no reason or trigger — from the **soft gap surface** (missing router row, guard test, provenance row, unreachable reference doc). The soft list *is* the next round's input; that is the part that makes growth perpetual rather than episodic.
  - **Slice 3 · the contract + procedure.** Clause **M5.10** in `core/06` (a round is recorded, audited, **closed**; a deferral is a decision with a revisit trigger; proposal-first, M0.4); `reference/capability-cycle.md` (inputs → rank → 2–4 slices → seven-axis DoD → record → defer → close, with a worked P13 example and deliberate non-entries); load-index / `SKILL.md` / router / README / GUIDE wiring.
  - **Slice 4 · first use — it found real defects.** The first `audit` reported that **`M2.10`**, **`M2.11`**, **`M3.10`** and **`M8.10`** were cited across review/router docs but *never anchored* in `core/` (and `M2.11` was mislabelled inside `core/09`). All four are now anchored in their own module; `sources/source-map.md` gained rows for M2.10/M2.11, M3.10–M3.13, M5.10 and M8.10. Guard `tests/test_cycle.py` (16 cases; `test_no_hard_problems` makes the mechanism gate itself). **209 tests.** 能力轮次机制化：注册表 · 完成定义 · 缺口面。
- **P14 (planned, opened 2026-10-19):** **domain-harness case studies — agent-built knowledge bases behind an evidence gate.** The user's ask: study harness patterns of this kind, survey and plan them, to be completed next session. **Case 1** is 关书朋, 何宇佳, 张英聘, *智能体驱动的方志人物知识图谱构建与检索增强生成问答研究* (《文献与数据学报》2026 年第 3 期), read through `https://mp.weixin.qq.com/s/zzsWOP6g2a9w2Q_y9d6aSQ`. The round is scoped to a **class** of source — published real-world domain harnesses — not to that one paper. Slices: **P14.1** verify the primary source and read the parts the web rendering shows only as images (表1 stage prompts · 表2 the P/R/F1 table · 表3 the mechanism comparison); **P14.2** crosswalk each mechanism against the existing clauses with an explicit **covered / partially / gap** verdict; **P14.3** land only what discriminates (proposal-first, M0.4) and record the non-additions. Its `added` block stays empty until Slice 3 decides — a round that opens with its deliverable pre-decided would be the habit M5.10 exists to forbid. First-pass triage and candidate outcomes: `updates/2026-10-19-domain-harness-case-study-plan.md`. 领域 harness 案例研究：首例「方志人物知识图谱 + RAG」，只落有判别力的结论。
- **P10 (done, 2026-10-18):** **mathematics, statistics & methodology systems.** *Slice 1 — statistics & computation:* **2 domains** `statistics` and `geometry-topology` (faculty `formal-sciences`; README + rubric each) and **2 capabilities** `statistical-inference` (M3, M4; keyed on `domain = statistics`) and `certified-computation` (M3, M6; keyed on `domain = geometry-topology`), grounded in the new clauses **M3.11** (declare the inferential frame) and **M3.12** (certify the computation). *Slice 2 — instrument depth:* **23 new `instruments`** rows and **4 new kinds** (computer-algebra-system, sat-solver, geometry-topology-toolkit, causal-inference-toolkit) — catalog **160 → 183** (12 classes × 50 kinds) — covering CAS (`sagemath`/`singular`/`macaulay2`/`gap`/`pari-gp`/`oscar`/`sympy`), SAT (`cadical`), proof library/verifier (`mathcomp`/`metamath`), geometry & topology (`cgal`/`gudhi`/`regina`/`snappy`/`polymake`), Bayesian (`r-project`/`pymc`/`numpyro`/`arviz`/`brms`/`r-inla`/`emcee`) and causal inference (`dowhy`). *Slice 3 — methodology systems (the standing ask):* new **`reference/methodology-map.md`** (field → methodology system → canonical source → what it demands → **who enforces it**), the new clause **M3.13** (declare the method and its assumptions) + checklist + anti-pattern *method-by-vibes*, and the instrument-map §Methodology; **no `methodology-fit` capability** (it would fire on nearly everything — recorded as a deliberate non-addition). *Slice 4 — roadmap:* new **`review/integration-map-2026-10.md`** (status board done/next/later × **discriminating criteria** + next-cycle cues). Sources `[R111]`–`[R119]`; guards `tests/test_capabilities.py::MathStatsCapabilityTest` + `tests/test_catalog.py` + `tests/test_domains.py`. 数学·统计·方法论做实：2 域 + 2 能力 + 23 仪器 + 方法论地图 + 路线图。
- **P9 (done, 2026-10-18):** **evidence instruments made concrete.** *Slice 1 — instrument catalog:* a new class **`instruments`** in `data/harnesses.json` — 13 kinds, **27 entries** (proof assistants `lean4`/`mathlib`/`rocq`/`isabelle`/`agda`/`dafny`; solvers & checkers `z3`/`cvc5`/`tla-plus`/`alloy`; units & uncertainty `pint`/`uncertainties`; chem/bio `rdkit`/`biopython`/`rcsb-pdb`/`uniprot`; language `universal-dependencies`/`inception`/`elan`; empirical `psychopy`/`jspsych`/`osf`/`statsmodels`/`lme4`/`stan`; pipelines `snakemake`/`nextflow`) — catalog **133 → 160** (12 classes × 46 kinds), data-only. *Slice 2 — the claim→instrument map:* new **`reference/evidence-instruments.md`** (claim type → instrument → catalogued tool → gate evidence, plus deliberate non-entries), wired into the skill load-index, `SKILL.md` step 6 and a router row, so **M3.10 stops being a slogan**. *Slice 3 — emitted default:* `templates/AGENTS.md.tmpl` gains an **Evidence instrument** stanza whose value `assemble._evidence_instrument()` derives from the matched capabilities (formal ⇒ machine-checked derivation; dimensional ⇒ units + propagated uncertainty; empirical ⇒ effect size + interval + reliability; else the observed-artefact fallback). *Slice 4 — domain depth:* concrete instrument lines added to `logic`/`linguistics`/`cognitive-science`/`physics`/`chemistry`/`biology` READMEs. Sources `[R107]`–`[R110]` (GUM + 2026 amendment, NASA-STD-7009B, SI brochure, Registered Reports); guards `tests/test_catalog.py::InstrumentCatalogTest` + `tests/test_assemble.py::EvidenceInstrumentTest`. 仪器做实：仪器目录 + 声明→仪器映射 + 生成模板默认声明仪器。
- **P8 (done, 2026-10-18):** **workflow shape + discipline coverage.** *Slice 1 — loops & graphs* (`review/workflow-patterns-2026-10.md`, §F/R93–R97): `loop-discipline` + `graph-orchestration` (**22 → 24**) with module clauses **M2.10** (loop contract), **M2.11** (declared control graph), **M8.10** (declare the topology), and a `langgraph.maps_to` correction. *Slice 2 — formal & empirical sciences* (`review/disciplines-crosswalk-2026-10.md`, §G/R98–R106): **3 domains** `logic` (new faculty `formal-sciences`) · `linguistics` · `cognitive-science` (README + rubric each) and **3 evidence-instrument capabilities** `formal-verification` · `dimensional-analysis` · `empirical-measurement` (**24 → 27**) grounded in **M3.10** (match the instrument to the claim). Deliberate non-additions recorded in both docs (a `computer-science` domain, `proof-search`, `statistical-significance`).
- **P6 (done, 2026-10-16):** make "mention the directory once" a **structural** guarantee rather than prose. `config.factory_root()` resolves the checkout that provides the code; `pointer.py` builds/verifies the emitted `.harness/pointer.json`; `assemble.py` emits it and writes the **resolved** path into `AGENTS.md` (no `<harness_factory path>` placeholder left); `runtime.gate_report` adds an *advisory* `pointer-resolves` gate; `harness doctor --project <dir>` reports reachability. Tests `tests/test_pointer.py`. Also hardened **structure** (not just content) with `tests/test_docs_integrity.py`: no raw assistant/tool markup in shipped docs, balanced code fences in shipped docs *and* every emitted file.

## Verification · 验证门（for this project)
- `python -m unittest discover -s tests` passes.
- `harness init --task "..."` produces a dir that `harness check` passes.
- `harness refresh --dry-run` collects/scores without writing; a real run writes only under `updates/`.
- No placeholder text in emitted files; manifest validates.
- *(P12 target)* the emitted-harness path runs end to end in CI (`init → check → gate → harvest → pointer verify`) on ubuntu + windows.

## Risks · 风险
- **Over-fitting the rules to the 4 domains.** Mitigation: features are compositional; `general` domain is first-class.
- **LLM classification drift.** Mitigation: rules are default; LLM output is schema-validated and only fills gaps; never fabricates task substance (M0.4).
- **Refresh noise / auto-drift.** Mitigation: provenance gate drops untraceable items; proposals only; human gate via `refresh-apply`; append-only journal; `updates/` fully reversible.
- **Scaffold rot.** Mitigation: templates versioned; `check` gate; each emitted harness carries its manifest.
- **CI network-job flakiness.** Mitigation: the network job is **opt-in** (`workflow_dispatch`) and never gates a push; the offline jobs stay the required gate.
