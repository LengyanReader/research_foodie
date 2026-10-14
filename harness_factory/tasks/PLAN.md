# PLAN · Inclusive Harness Tool · 通用 harness 工具计划

**Updated:** 2026-10-14 · **Status:** active · **Owner:** user + agent

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
- `harness profile --project DIR` — scan a target project → `PROFILE.md` + capabilities (observe-only).
- `harness learn` / `harness cases` — record / review learned project cases (project → factory learning).
- `harness catalog [<id>] [--class/--kind/--module/--vendor/--tag/--search/--tracked/--markdown/--write/--json]` — unified harness catalog: list/search/filter; `--write` regenerates `review/harness-index.md`.
- `harness standard [--store F] --domain D bar|score|audit|raise|plan|frontier <name>` — the frontier-standard ratchet over a per-domain weighted rubric (`data/rubrics.json`); `raise` refuses regressions (unless `--force`); `plan` maps gaps → modules + catalog tools (`data/levers.json`).
- `harness doctor` / `harness self-update` — path/config/LLM status; re-seed the tool's own catalog (non-destructive).
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
      domains.json    domain catalog (23 disciplines + `general`; faculty taxonomy)
      harnesses.json  unified harness catalog (127 entries: class × kind × module-map × vendor)
      rubrics.json    per-domain weighted excellence rubric (`default` fallback)
      levers.json     rubric dimension -> modules (M0–M8) + catalog tool-kinds that close it
      watchlist.json  refresh topics + frontier probes (M5 signal source)
      sources.json    tracked entities (projects/harnesses/venues/people/media/libraries/tools) + feeds
      capabilities.json  requirement -> capability -> modules map (extensible, data-driven)
    derive.py      FeatureVector -> HarnessPlan   (explainable rule table + capability annotation)
    classify.py    task text -> FeatureVector      (rules; optional LLM)
    capabilities.py  load capability map; match(features) -> active capabilities + module reasons
    catalog.py     load/search/filter/render/validate/write_index over data/harnesses.json
    standard.py    frontier-standard ratchet: bar ledger, rubric scoring, gap audit, raise (no regress), plan
    skill.py       agent load-index: index / find / read (SKILL.md + core + data + domains)
    llm.py         OpenAI-compatible classify + discover + summarize (stdlib urllib), env-gated
    render.py      tiny {{key}} template engine (no deps)
    assemble.py    HarnessPlan -> files on disk
    check.py       validate an emitted harness against its manifest (gate)
    collect.py     refresh/intel: Candidate + file/llm/feed providers; RSS/Atom parse; YouTube resolve
    curate.py      refresh: audit / dedupe / score / trends (observe-only)
    journal.py     refresh: report / queue / proposal writers (append-only journal)
    extract.py     intel: candidates -> scored intel (INTEL.md + intel.jsonl)
    evolution.py   self-evolution: snapshot -> audit -> proposal -> journal + metrics; apply gate
    profile.py     project scan -> ProjectProfile (stacks/capabilities) + PROFILE.md (observe-only)
    learning.py    project cases: record / load / aggregate (project -> factory mutual learning)
    refresh.py     refresh: orchestrate signal->audit->proposal->journal; apply gate; watermark
    cli.py         argparse: derive / init / explain / check / profile / skill / refresh / refresh-apply / sources / intel / evolve / evolve-apply / learn / cases / doctor / self-update
    __main__.py    python -m harness_factory
    templates/     AGENTS.md, tasks/*, .harness/* (incl. PROVENANCE.md), check.py
  SKILL.md         agent-native entry point (cardinal rules + load-index + output contract)
  reference/       derivation-rules.md (markdown mirror of the rule table, for L0 agents)
  install-skill.ps1  copy repo-as-skill into a skills dir (optional global install)
  tests/           stdlib unittest (no deps)
  tasks/           PLAN.md · PROGRESS.md · REFRESH.md · DISTRIBUTION.md
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

- **P0 (done):** pattern library (`core/`, `domains/`, `review/`, `sources/`).
- **P1 (done):** CLI scaffold generator — `derive`/`init`/`explain`/`check`, rules engine, tests.
- **P1.5 (done):** self-update loop (M5) — `refresh`/`refresh-apply`, watchlist, curate, journal, scheduler, tests.
- **P1.6 (done):** cross-project packaging — user-home KB (`HARNESS_HOME`), `doctor`, `self-update`, re-rooted `refresh`; `uv tool install`.
- **P1.7 (done):** intel tracking (`sources.json`, feed/YouTube collection, `extract.py`) + self-evolution (`evolution.py`, metrics, proposal gate); CLI `sources`/`intel`/`evolve`/`evolve-apply`; run watermark.
- **P1.8 (done):** agent-native mode + project learning. Cancelled packaging as a distribution channel (PyPI/`uv tool install`); primary = agent-native skill (`SKILL.md` + `harness skill`) + CLI-from-path (L1). Data-driven **capability mechanism** (`capabilities.json`), **project profile** (`profile.py`), **mutual learning** (`learning.py` cases + `missing_capability` audit).
- **P2 (active):** comprehensiveness + discoverability.
  - **Disciplines · 学科门类（~20）:** expand `domains/` from 4 to a faculty-level taxonomy — natural sciences (physics, chemistry, biology, earth-environment, mathematics), engineering (engineering, software-engineering, devops), health (medicine), social sciences (economics-finance, psychology, social-science), humanities (humanities), law, business/education/arts (education, arts-design). Each = `domains/<id>/README.md` + `domains.json` entry (artifact/grounding/signals). Adds no new rules — features stay compositional (M0.5).
  - **Harness index · harness 索引:** a unified, machine-readable catalog `data/harnesses.json` (127 entries; classes × kinds × core-module maps × source), cross-linked to `sources.json` by id; `catalog.py` + CLI `harness catalog` (list/search/filter/`--json`); generated `review/harness-index.md` with a drift-guard test. Prose taxonomy in `review/harness-catalog.md` stays as the explanation; the index is the lookup surface.
  - **Frontier standard · 最高标准棘轮 (done):** `excellence` domain + `standard-ladder.md`; per-domain weighted rubrics (`data/rubrics.json`, `default` fallback) and the gap→lever map (`data/levers.json`); executable ratchet `standard.py` + CLI `harness standard bar|score|audit|raise|plan|frontier` (refuses regressions); `stale_frontier` audit in `evolution.py`; applied reflexively in `self-standard.md` + `security-model.md`.
  - **Writing domain · 写作域 (doc-level):** `domains/writing/README.md` — citation-first essay harness (thesis→outline→context pack→claim↔evidence→originality→clarity) with a humanities-aligned rubric. **Pending:** register in `domains.json`/`rubrics.json` so `--domain writing` becomes selectable.
  - **LLM-assisted discovery/classification hardening** and **feed/entity coverage expansion** — deferred to a later P2 slice.
- **P3:** emitted-harness runtime hooks (gate runner, signal harvest).
- **P4:** plugin protocol for new domains/templates.

## Verification · 验证门（for this project)
- `python -m unittest discover -s tests` passes.
- `harness init --task "..."` produces a dir that `harness check` passes.
- `harness refresh --dry-run` collects/scores without writing; a real run writes only under `updates/`.
- No placeholder text in emitted files; manifest validates.

## Risks · 风险
- **Over-fitting the rules to the 4 domains.** Mitigation: features are compositional; `general` domain is first-class.
- **LLM classification drift.** Mitigation: rules are default; LLM output is schema-validated and only fills gaps; never fabricates task substance (M0.4).
- **Refresh noise / auto-drift.** Mitigation: provenance gate drops untraceable items; proposals only; human gate via `refresh-apply`; append-only journal; `updates/` fully reversible.
- **Scaffold rot.** Mitigation: templates versioned; `check` gate; each emitted harness carries its manifest.
