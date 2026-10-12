# PLAN · Inclusive Harness Tool · 通用 harness 工具计划

**Updated:** 2026-10-12 · **Status:** active · **Owner:** user + agent

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
- Deterministic rule engine over M0–M8 + 4 domains + general.
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
    data/
      modules.json   module catalog M0–M8 (id, titles, rule)
      domains.json    domain catalog (research, knowledge-management, data-science, devops, general)
      watchlist.json  refresh topics + frontier probes (M5 signal source)
    derive.py      FeatureVector -> HarnessPlan   (explainable rule table)
    classify.py    task text -> FeatureVector      (rules; optional LLM)
    llm.py         OpenAI-compatible classify + discover (stdlib urllib), env-gated
    render.py      tiny {{key}} template engine (no deps)
    assemble.py    HarnessPlan -> files on disk
    check.py       validate an emitted harness against its manifest (gate)
    collect.py     refresh: Candidate + file/llm providers (fetch only)
    curate.py      refresh: audit / dedupe / score / trends (observe-only)
    journal.py     refresh: report / queue / proposal writers (append-only journal)
    refresh.py     refresh: orchestrate signal->audit->proposal->journal; apply gate
    cli.py         argparse: derive / init / explain / check / refresh / refresh-apply
    __main__.py    python -m harness_factory
    templates/     AGENTS.md, tasks/*, .harness/*, check.py
  tests/           stdlib unittest (no deps)
  tasks/           PLAN.md · PROGRESS.md · REFRESH.md
  updates/         refresh output (queue.jsonl · REPORT.md · JOURNAL.md · proposals/)
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

## Milestones · 里程碑

- **P0 (done):** pattern library (`core/`, `domains/`, `review/`, `sources/`).
- **P1 (done):** CLI scaffold generator — `derive`/`init`/`explain`/`check`, rules engine, tests.
- **P1.5 (done):** self-update loop (M5) — `refresh`/`refresh-apply`, watchlist, curate, journal, scheduler, tests.
- **P2:** LLM-assisted discovery/classification hardening + more domains.
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
