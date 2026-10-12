# Introduction · harness-factory 简介

**Updated:** 2026-10-12 · **Status:** working tool (P1 + P1.5) · **Version:** 0.1.0 · **License:** MIT

> **Give any task the agent harness it needs — and keep that know-how current.**
> 为任意任务生成它所需的 agent harness，并让这套 know-how 持续自我更新。

---

## 中文速览

**一句话。** `harness-factory` 把「**任务**」编译成该任务所需的 **agent harness**（上下文工程 · 外部记忆 · 验证门禁 · 来源考证 · 工具/技能 · 变更治理 · 协作协议），并用一个受人类把关的**自我更新循环**让这套知识库不被冻结。

**它是什么。** 一个可安装的 **Python 命令行工具 `harness`**，外加一套跨域提炼的 **harness 模式库**（`core/`、`domains/`、`review/`）。工具与知识库在同一个仓库里：`core/` 定义「有哪些模式」，`data/*.json` 是机器可读目录，`src/` 是编译器。

**它怎么工作。** `task → 特征向量 → 选模块 → 生成脚手架`。任务被归约为 8 个特征轴，规则据其启用 M0–M8 模块并推导参数；每一步的选择与理由写入 `.harness/manifest.json`，可解释、可复核。

**它不做什么（M0.4）。** 只做**分类 / 选择 / 生成 / 观察 / 排序**；绝不编造任务实质内容，绝不自动改写正文，破坏性动作（推送 / 发布 / 删除 / 花钱）必须人工确认。

**怎么用。** `harness init --task "…" --out <目录>` 在**任意目录**生成 harness；`harness check` 校验；`harness refresh` 定期抓取新前沿工作（只出提案）。

---

## 1. The problem · 要解决的问题

A capable model is not a reliable worker. Between *the model* and *a task done right*, there is always a **harness**: the context you feed it, the memory you externalize, the tools you expose, the gates that decide "done", the provenance that keeps it honest, and the loop that makes the harness itself improve. Hand-rolling that harness for every new project is where most of the effort and most of the failure goes.

`harness-factory` fixes the *recurrence*: the same harness questions come up in research, data science, knowledge management, and ops. It answers them once, as portable patterns, and then **compiles a concrete harness per task** instead of making you re-derive it.

---

## 2. What it is · 它由什么组成

Two halves, one repository:

| Half | Lives in | Role |
|---|---|---|
| **Pattern library** (knowledge) | `core/`, `domains/`, `review/`, `sources/` | Domain-neutral harness patterns + domain compositions + literature review, all sourced. |
| **Compiler & loop** (tool) | `src/harness_factory/` | Classify → derive → assemble → check, plus the self-update loop. |

The library is *readable by humans*; the tool is *executable by agents*. `data/modules.json` and `data/domains.json` are the single machine-readable bridge between them (M0.5).

---

## 3. Mental model · 心智模型

```
        task (text or flags)
              │
              ▼
    classify  ──► FeatureVector        (8 axes, rules-first; optional LLM fills gaps)
              │     horizon · verifiability · stakes · grounding
              │     artifact · tool_surface · collaboration · domain
              ▼
    derive    ──► HarnessPlan          (M0–M8 enabled? with what params? + reasons)
              │
              ▼
    assemble  ──► files on disk        (AGENTS.md · tasks/* · .harness/*)
              │
              ▼
    check     ──► gate                (manifest validates; no placeholders)
```

**The delayering idea.** A harness is not a fixed template; it is a *composition* of modules selected by the task's features. That is what makes it "inclusive": cover a new kind of task by adding a feature value or a domain, not a new branch everywhere.

### Modules (M0–M8)

| id | module · 模块 | enabled when |
|---|---|---|
| M0 | Meta-principles · 元原则 | always |
| M1 | Context engineering · 上下文工程 | always |
| M2 | Long-running / memory · 长时程/记忆 | horizon ≥ session |
| M3 | Verification & gates · 验证与门禁 | always |
| M4 | Provenance & integrity · 来源与完整性 | grounding ≥ preferred, or cited artifact |
| M5 | Self-evolution · 自演化 | horizon ≥ multi_session |
| M6 | Tools & skills · 工具与技能 | tool_surface ≠ none |
| M7 | Change governance · 变更治理 | always |
| M8 | Collaboration & sessions · 协作与会话 | collaboration ≠ solo or stakes = high |

### Domains

`research`, `knowledge-management`, `data-science`, `devops`, and a first-class `general` fallback. Domains only set **defaults** (artifact, grounding, workflow, signals); the features still decide.

---

## 4. Quickstart · 快速上手

```bash
# install once, use in ANY directory (see tasks/DISTRIBUTION.md for the evaluation)
uv tool install .        # global, isolated `harness` on PATH
# (development: `uv run python -m harness_factory ...` against src/)

harness doctor           # show the tool home / catalog / config / LLM status

# 1. See the plan for a task (explainable: which rule fired, and why)
harness derive --task "write a literature review with citations over several weeks"
harness derive --task "add unit tests to the parser" --json

# 2. Emit the harness into ANY directory (defaults to ./<task-slug>)
harness init --task "add unit tests to the parser" --out C:\work\parser-task
harness check --dir C:\work\parser-task        # gate: manifest + no placeholders

# 3. Explain an emitted harness later
harness explain --dir C:\work\parser-task

# 4. Self-update the knowledge base (proposals only; writes to the tool home)
harness self-update                  # refresh the tool's own catalog from packaged defaults
harness refresh --dry-run            # collect + score, write nothing
harness refresh --provider all --intel   # file + tracked feeds + LLM(opt) -> intel
harness refresh-apply --accept 0 2601.12345   # human gate -> <home>/updates/proposals/

# 5. Intel + self-evolution (tracked sources: labs, harnesses, venues, people, media)
harness sources --group harnesses    # list every tracked entity (see data/sources.json)
harness intel --since 2026-01-01     # pull tracked feeds -> <home>/updates/INTEL.md
harness evolve                       # coverage/gap audit -> <home>/updates/EVOLUTION.md
harness evolve-apply --accept <id|target>    # human gate -> <home>/updates/accepted.json
```

**Two roots.** The **tool home** (`%LOCALAPPDATA%`\harness-factory on Windows, overridable via `HARNESS_HOME`) holds catalogs, corpus, and refresh output, so the tool works from any directory. Each **target project** receives its generated files via `init --out`.

**Exit codes:** `init`/`check` return non-zero if the self-check gate fails, so they compose in CI.

---

## 5. What it produces · 生成物

`harness init` writes (minimum set; extras depend on modules):

```
<out>/
  AGENTS.md               operating manual for the task (bilingual)
  tasks/PLAN.md           plan-first scaffold
  tasks/PROGRESS.md       append-only progress log + handoff
  .harness/manifest.json  the decision record: features, modules, reasons, files
  .harness/gates.md       definition of done (hard/soft gates)
  .harness/check.py       standalone self-check (stdlib only)
  .harness/ledger.md      (if M2) append-only state
  .harness/skills/README.md (if M6) progressive skill index
  .harness/decisions.md   (if M8) decision log
```

Every emitted file is plain Markdown/Python — no lock-in, no runtime dependency.

---

## 6. Self-update · 自我更新（M5）

The knowledge base must not freeze. `harness refresh` runs `signal → audit → rank → proposal → journal`:

- **Signals** from `data/watchlist.json` (8 topics + frontier probes), a local `updates/inbox.jsonl`, and optional LLM discovery.
- **Audit** drops anything without a traceable url/arXiv-id/DOI (M4) and dedupes against the existing `review/` corpus.
- **Report** a bilingual `updates/REPORT.md` with **hot topics** (frequency × recency) and **coverage gaps** (declared topics with zero hits) — the cue for boundary expansion.
- **Human gate:** `refresh-apply` only writes merge stubs to `updates/proposals/`; a human edits the catalogs. Nothing is auto-merged, and everything is reversible by deleting `updates/`.
- **Watermark:** the effective `since` date is persisted to `updates/state.json`, so repeated cycles only surface *new* items without passing `--since` each time.

**Tracked entities (`data/sources.json`).** 59 entities across 5 groups — **projects** (frontier labs + frameworks), **harnesses** (vendor agent SDKs/CLIs/protocols: Agents SDK, Claude Code, MCP, Gemini CLI, ADK, A2A, Llama Stack, …), **venues** (journals + arXiv), **people**, and **self-media** (newsletters/podcasts/YouTube). RSS/Atom feeds are used where one exists; YouTube `@handle` pages are resolved to channel feeds. `harness sources` lists them.

**Intel (`harness intel`).** Pulls those feeds, scores relevance (topic keywords + entity mention + recency), tags by topic/entity, and writes a bilingual `updates/INTEL.md` + `updates/intel.jsonl`. Briefs are verbatim excerpts unless an LLM summary is configured (`llm.summarize`).

**Self-evolution (`harness evolve`).** The structural loop **snapshot → audit → mutation-proposal → journal**: audits topic coverage, empty groups, stale entities, and accepted candidates from untracked sources; writes `updates/EVOLUTION.md` + `updates/evolution.jsonl` and appends a metric snapshot to `updates/metrics.jsonl`. `evolve-apply` accepts proposals into `updates/accepted.json` only (M0.8/M0.9).

Scheduling (weekly): run `refresh.ps1` (now: refresh `--provider all --intel` then `evolve`); details in `tasks/REFRESH.md` (Task Scheduler / cron / GitHub Actions).

---

## 7. Design principles · 设计原则（M0）

Priority chain (higher wins on conflict):

> **Truth ≻ Trace ≻ Verify ≻ Observe-only ≻ SSOT ≻ Human-gate ≻ Context ≻ Resumable ≻ Reversible ≻ Evolvable**

Practically, in every mechanism:

- **Truth before throughput** — never invent content to look finished.
- **Provenance or `unverified`** — every load-bearing claim traceable, or explicitly flagged.
- **Verify before "done"** — "done" is an observed state with evidence, not a feeling.
- **Machines observe, humans decide** — automation may classify/record/rank, never fabricate or silently mutate.
- **Human gate + reversible** — irreversible acts need authorization; changes are reviewable and undoable.

---

## 8. Relationship to the pattern library

Start with `core/01-meta-principles.md` (the ten invariants). Then `core/00-index.md` → the M1–M8 files → `domains/*/README.md` for domain compositions → `sources/source-map.md` for exactly which primary source each pattern came from. The tool is the *executable* projection of that library; the library is the *explanation* of the tool.

---

## 9. Status & roadmap

- **P0 done** — pattern library.
- **P1 done** — CLI compiler (`derive`/`init`/`explain`/`check`), rules engine, stdlib tests.
- **P1.5 done** — self-update loop (`refresh`/`refresh-apply`), watchlist, curate, journal, scheduler.
- **P1.6 done** — cross-project packaging: user-home KB (`HARNESS_HOME`), `doctor`, `self-update`, re-rooted `refresh`; installable via `uv tool install`.
- **P1.7 done** — intel tracking (`data/sources.json`, 59 entities, feed/YouTube collection) + self-evolution loop (`evolve`, metrics, proposal gate) + CLI `sources`/`intel`/`evolve`/`evolve-apply`.
- **P2** — LLM discovery/classification hardening; more domains; feed/entity coverage expansion.
- **P3** — runtime hooks (gate runner, signal harvest); optional SQLite event store.
- **P4** — plugin protocol for third-party domains/templates; optional zipapp / MCP server.

See `tasks/PLAN.md` (plan), `tasks/PROGRESS.md` (log), and `tasks/DISTRIBUTION.md` (packaging & tool-form evaluation).
