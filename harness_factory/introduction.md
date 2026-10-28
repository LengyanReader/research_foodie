# Introduction · harness-factory 简介

**Updated:** 2026-10-28 · **Status:** working tool (post-P45) · **Version:** 0.1.0 · **License:** MIT

> **Give any task the agent harness it needs — and keep that know-how current.**
> 为任意任务生成它所需的 agent harness，并让这套 know-how 持续自我更新。

---

## 中文速览

**一句话。** `harness-factory` 把「**任务**」编译成该任务所需的 **agent harness**（上下文工程 · 外部记忆 · 验证门禁 · 来源考证 · 工具/技能 · 变更治理 · 协作协议），并用一个受人类把关的**自我更新循环**让这套知识库不被冻结。

**它是什么。** 一套跨域提炼的 **harness 模式库**（`core/`、`domains/`、`review/`）+ 一个把任务**编译成 harness** 的工具。工具既可由 **vibe-coding 助手直接读取（L0，免安装）**，也可用 CLI **从仓库路径调用（L1）**；打包分发（L2）已取消。

**它怎么工作。** `task → 特征向量 → 选模块 → 生成脚手架`。任务被归约为 8 个特征轴，规则据其启用 M0–M8 模块并推导参数；每一步的选择与理由写入 `.harness/manifest.json`，可解释、可复核。

**它如何自我校准（测量系统，P23–P45）。** 一个 7 任务记分集钉住 harness 发射质量（结构轴 1.0 基线 + 每任务 effect_metric 效果轴）；执行轨迹（失败与收尾判决）被采集、规则审计成提案；一次配对试验实测「裸奔 0.2 vs harness 1.0」（引用可核验性，机器判分）。`harness full-update --offline` 一句话跑完整个观察环。

**它不做什么（M0.4）。** 只做**分类 / 选择 / 生成 / 观察 / 排序**；绝不编造任务实质内容，绝不自动改写正文，破坏性动作（推送 / 发布 / 删除 / 花钱）必须人工确认。

**怎么用。** 分两步——先贴「配置」（如何引用与使用本工具），再给「任务」（同一轮或下一轮均可）；助手读 `SKILL.md` 自行推导并落盘 harness；或用 `harness init --task "…" --out <目录>` 在**任意目录**生成；`harness check` 校验；`harness profile/learn` 让它**从目标项目中学习**；`harness refresh/evolve` 定期抓取新前沿工作（只出提案）。

**给 vibe-coding 助手的用法（贴一次即常驻 · standing reference）。** ① **常驻引用**（贴一次，整个对话有效；写进项目规则文件可跨对话/子体）：「把本仓库当 harness 能力参考（常驻，直到我说「停止使用 harness_factory」撤销）。**先替换路径参数**：`<HF>` = 本仓库克隆后 `harness_factory/` 目录的真实路径（如 `~/src/research_foodie/harness_factory`）。先读 `<HF>/SKILL.md`，按 `<HF>/reference/capability-router.md` 路由、只加载命中行点名的文件；需求模糊/偏小时先跑 `<HF>/reference/requirement-refinement.md`（R0–R5，等我确认）。每次实质回答前先查有无适用能力，用了就声明用了哪个能力、哪个文件。推导 harness 时产出 `AGENTS.md` + `tasks/*` + `.harness/*`（含 `.harness/capabilities.local.md`），跑 `harness check --dir <产物目录>`（未安装时用 `PYTHONPATH=<HF>/src python -m harness_factory check --dir <产物目录>`）；本地能力留在任务里，通用模式只以提案回流 `updates/`（不直接改 `data|core|domains|templates`）。不编造任务内容（M0.4）；真实与可溯源优先于速度（M0.1/M0.2）；不可逆动作须我明确同意。」② **任务**（同一轮接着写，或下一轮再发）：直接写目标，或直接附上文件/目录。

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

The library is *readable by humans*; the tool is *executable by agents*. `data/modules.json`, `data/domains.json`, and `data/capabilities.json` are the single machine-readable bridge between them (M0.5).

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

34 disciplines across 10 faculties (from `research` through `history`/`philosophy`/`political-science`/`ai-safety` to `digital-humanities` and `writing`), each with its own `domains/<id>/README.md`, plus a first-class `general` fallback. Domains only set **defaults** (artifact, grounding, workflow, signals), and an explicit cue in the task text (`report`, `dataset`, `注明来源`…) overrides the artifact/grounding default; the features still decide.

---

## 4. Quickstart · 快速上手

```bash
# 0. Agent-native (L0), two steps: paste the config once (how to reference/use this tool),
#    then give the task (same turn or next). It reads SKILL.md and derives/emits the harness itself — no install.
#    Deterministic path (L1), no install either:
PYTHONPATH=src python -m harness_factory derive --task "…" --json
# The rest of this file uses `harness` as shorthand for the CLI; without an install, alias it first:
#   alias harness='PYTHONPATH=src python -m harness_factory'

# 1. See the plan for a task (explainable: which rule fired, and why)
harness derive --task "write a literature review with citations over several weeks"
harness derive --task "add unit tests to the parser" --json

# 2. Emit the harness into ANY directory (defaults to ./<task-slug>)
harness init --task "add unit tests to the parser" --out C:\work\parser-task
harness check --dir C:\work\parser-task        # gate: manifest + no placeholders

# 3. Explain an emitted harness later
harness explain --dir C:\work\parser-task

# 3b. Agent-native helpers + project profiling / learning (observe-only)
harness skill                       # agent load-index; `harness skill M4` prints a module
harness capabilities                # requirement -> capability -> modules map
harness map                          # whole-factory overview -> HARNESS-MAP.md (generated)
harness standard --domain deep-research bar brief --level R4 --name "SOTA report" --source https://…
harness standard --domain deep-research score brief --set fidelity=2 --set coverage=3
harness standard --domain deep-research audit brief   # gaps; `raise brief` ratchets the floor
harness profile --project C:\work\parser-task --goal "…"   # -> <home>/updates/profile/
harness learn   --task "…" --project C:\work\parser-task   # -> <home>/updates/cases.jsonl
harness cases                       # aggregate learned cases

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

# 6. The measurement & trace loop (P23-P45): the factory measures itself
harness scoreboard                    # 7-task holdout: structural axes (1.0 baseline) + per-task effect axis
harness brief --task "..." --out brief.md   # paste-ready task brief (confirm before work, R4/R5)
harness init --from-brief brief.md --out <dir>  # emit the harness from a confirmed brief
harness harvest --dir <dir> --event task_outcome --detail '{"judge":"human","score":4}'  # record a verdict
harness collect --project <dir>       # pull a project's local traces into the tool home
harness trace-audit                   # audit traces -> mutation proposals (proposal-only)
harness cycle audit                   # the round registry audit (39+ rounds, 0 hard, 0 gaps)
harness full-update --offline         # the whole observe loop in one instruction
```

**The loadable reference set (L0).** `harness skill` lists it, and it is exactly what an emitted harness's `.harness/pointer.json` `entry_docs` points at: `SKILL.md`, `core/00-index.md`, `CAPABILITIES.md`, `HARNESS-MAP.md`, and `reference/` — capability-router · requirement-refinement · derivation-rules · capability-flow · evidence-instruments · methodology-map · outlet-map · cross-language · capability-cycle · tool-router. Read any one with `harness skill <name>`. · 可加载参考集：`harness skill` 与生成物 `pointer.json` 的 `entry_docs` 指向**同一套**（SKILL.md + core 索引 + 生成总览 + 10 份 `reference/`），逐份用 `harness skill <name>` 打开。

**Consumption modes.** **L0** — the assistant reads `SKILL.md` + `core/` + `data/*.json` and derives
itself (most flexible, no install). **L1** — run the CLI from the path without installing
(`PYTHONPATH=src python -m harness_factory …`; deterministic). **L2** — an installed package; this is
**cancelled as a distribution channel** (see `tasks/DISTRIBUTION.md` §8).

**Two roots.** The **tool home** (`%LOCALAPPDATA%`\harness-factory on Windows, overridable via `HARNESS_HOME`) holds catalogs, corpus, and cycle output, so the tool works from any directory. Each **target project** receives its generated files via `init --out` (or directly from the agent). In path/L0 mode the home is optional.

**Exit codes:** `init`/`check` return non-zero if the self-check gate fails, so they compose in CI.

**Finding the factory again.** `.harness/manifest.json` records the *decisions*; `.harness/pointer.json` records **where the factory is** (resolved absolute path + the full loadable entry set: `SKILL.md`, the router, refinement/flow, the instrument/methodology/outlet maps, cross-language, derivation rules). So a later conversation need not be told the path: read the pointer, or run `harness doctor --project <out>` to check it still resolves (the runtime gate reports it as *advisory*, since another machine may legitimately not have the checkout). The pointer's `entry_docs` is **derived from the skill index**, so it cannot drift from `harness skill`.

---

## 5. What it produces · 生成物

`harness init` writes (minimum set; extras depend on modules):

```
<out>/
  AGENTS.md               operating manual for the task (bilingual)
  tasks/PLAN.md           plan-first scaffold
  tasks/PROGRESS.md       append-only progress log + handoff
  .harness/manifest.json  the decision record: features, capabilities, modules, reasons, files
  .harness/gates.md       definition of done (hard/soft gates)
  .harness/PROVENANCE.md  derivation record (which rule/capability fired; mark unverified)
  .harness/pointer.json   resolved path to this harness_factory checkout (how a later session finds it)
  .harness/check.py       standalone self-check (stdlib only)
  .harness/ledger.md      (if M2) append-only state
  .harness/skills/README.md (if M6) progressive skill index
  .harness/skills/<name>/SKILL.md (if M6) portable Agent Skills (SKILL.md) skill
  .harness/decisions.md   (if M8) decision log
  .harness/PROFILE.md     (if --project) read-only scan of the target project
```

Every emitted file is plain Markdown/Python — no lock-in, no runtime dependency.

---

## 6. Self-update · 自我更新（M5）

The knowledge base must not freeze. `harness refresh` runs `signal → audit → rank → proposal → journal`:

- **Signals** from `data/watchlist.json` (12 topics + 4 frontier probes, as of 2026-10-28), a local `updates/inbox.jsonl`, and optional LLM discovery.
- **Audit** drops anything without a traceable url/arXiv-id/DOI (M4) and dedupes against the existing `review/` corpus.
- **Report** a bilingual `updates/REPORT.md` with **hot topics** (frequency × recency) and **coverage gaps** (declared topics with zero hits) — the cue for boundary expansion.
- **Human gate:** `refresh-apply` only writes merge stubs to `updates/proposals/`; a human edits the catalogs. Nothing is auto-merged, and everything is reversible by deleting `updates/`.
- **Watermark:** the effective `since` date is persisted to `updates/state.json`, so repeated cycles only surface *new* items without passing `--since` each time.

**Tracked entities (`data/sources.json`).** 237 entities across 8 groups (as of 2026-10-28) — **projects** (frontier labs + frameworks), **harnesses** (vendor agent SDKs/CLIs/protocols: Agents SDK, Claude Code, MCP, Gemini CLI, ADK, A2A, Llama Stack, …), **venues** (journals + arXiv), **people**, **self-media** (newsletters/podcasts/YouTube), **libraries** (Project Gutenberg, Standard Ebooks, Internet Archive, Open Library, HathiTrust, DOAB), **tools** (deep-research/search/academic/retrieval/crawl/screening/eval tools), and **outlets** (per-field first-party portals/journals/databases/registries). RSS/Atom feeds are used where one exists; YouTube `@handle` pages are resolved to channel feeds. `harness sources` lists them.

**Intel (`harness intel`).** Pulls those feeds, scores relevance (topic keywords + entity mention + recency), tags by topic/entity, and writes a bilingual `updates/INTEL.md` + `updates/intel.jsonl`. Briefs are verbatim excerpts unless an LLM summary is configured (`llm.summarize`).

**Self-evolution (`harness evolve`).** The structural loop **snapshot → audit → mutation-proposal → journal**: audits topic coverage, empty groups, stale entities, accepted candidates from untracked sources, and **apex bars whose moving frontier is un-rechecked** (`stale_frontier`, from `updates/standard.json`); writes `updates/EVOLUTION.md` + `updates/evolution.jsonl` and appends a metric snapshot to `updates/metrics.jsonl`. `evolve-apply` accepts proposals into `updates/accepted.json` only (M0.8/M0.9).

Scheduling (weekly): run `refresh.ps1` (now: refresh `--provider all --intel` then `evolve`); details in `tasks/REFRESH.md` (Task Scheduler / cron / GitHub Actions).

**The trace-driven loop (D1, P22–P45).** Beyond the catalog-side loop, the factory consumes **execution traces**: an emitted harness records machine facts (a missed gate, a human correction, a capability that never fired, the task's final verdict with a judge and score) into `.harness/traces.jsonl`; `harness collect` pulls them into the tool home; `harness trace-audit` runs data-declared rules over them and emits **mutation proposals** (proposal-only, human-gated). Receipts carry a judge (`human` by default; `machine` only where the task family has a defined metric) — the machine records verdicts, it never makes them (M0.4). `harness full-update` chains the whole observe loop: intel → probe-domains → trace-audit → evolve → cycle audit → scoreboard.

**The measurement system (P23–P45).** `data/scoreboard.json` is the factory's own holdout: **7 canonical task families, each scored on five deterministic structural axes** (routing / capabilities / modules / structure / emission — 1.0 baseline pinned by tests, moves only by deliberate recorded edit) plus a per-task **effect axis** (`effect_metric`: the machine-scorable measure of whether the task actually went well — unmeasured until a real run records a receipt). The structural ablation baseline (P40/P44) ablated all 38 capabilities one at a time: **17 units are load-bearing** and protected; a paired trial (P45) ran bare vs harnessed on the same task — **0.2 vs 1.0 on citation-verifiability** (machine-judged; N=1, directional) — the first effect receipts, recorded as real traces.

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

## 9. Agent-native mode & project learning · 面向 agent 与项目学习（P1.8）

**Why.** The asset is the *knowledge + rules*, not the executable. The most flexible use is to let a
vibe-coding assistant read the factory directly: point it at this repo + a task goal, and it derives and
emits the harness itself. `SKILL.md` is the entry (cardinal rules + load-index + output contract);
`reference/derivation-rules.md` is the agent-readable mirror of the rule table; `harness skill` prints the
index. This removes install friction and works for any assistant (Claude Code / opencode / Cursor / …).

**Standing reference & routing.** Paste once (`SKILL.md` §"PASTE THIS EXACT INSTRUCTION") and the factory stays
active for the whole conversation, until explicitly revoked. `reference/capability-router.md` maps *situation →
capability → module → file*; `reference/requirement-refinement.md` (R0–R5: restate → elevate → classify
constraints → offer readings → confirm → converge) sharpens an under-aimed ask before anything is derived;
`reference/capability-flow.md` defines the **bidirectional** loop — concretise a capability into the task's own
`.harness/capabilities.local.md`, and send only generalisable patterns back as human-gated proposals.

**Capability mechanism (requirement → harness).** Module selection is driven by a data-driven **capability
map** (`data/capabilities.json`): a requirement (task features) matches capabilities, which *annotate* the
enabled modules and are recorded in the manifest. New requirements are added by editing JSON, not code, so
the configuration mechanism is complete and extensible.

**Mutual learning (project → factory).** When the tool configures a project it can also **distill it**:
`profile` scans the target project (stacks, existing capabilities, structure — observe-only) and `learn`
records a **case** (`updates/cases.jsonl`: features + capabilities + modules). `evolution` audits cases: a
project capability that keeps recurring but is missing from the registry becomes a `missing_capability`
proposal (human-gated). Projects teach the factory; capabilities discovered in one project become reusable
options for others; the factory's next harness is better.

**Packaging cancelled.** Installing a global command + maintaining a user-space KB is friction that does
not match the intended use. L0/L1 suffice; `pyproject.toml` remains only as dev/CI convenience. Rationale
and superseded decisions: `tasks/DISTRIBUTION.md` §8.

---

## 10. Status & roadmap

**The live roadmap lives in [`tasks/PLAN.md`](tasks/PLAN.md)** (rounds, next-round worklist, non-goals) with the
machine-readable registry in `data/cycles.json` (`harness cycle audit`). This section is deliberately a pointer,
not a copy — a second rendering of the roadmap is a drift source (M0.5): rounds P0–P45 are done as of 2026-10-28,
and [`CHANGELOG.md`](../CHANGELOG.md) records each round's counts and sources. Packaging history and the tool-form
decision: [`tasks/DISTRIBUTION.md`](tasks/DISTRIBUTION.md).
