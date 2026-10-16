# research_foodie → Harness Factory

> **A generalizable library of agent-harness patterns — plus an executable compiler that derives
> the harness any task needs.**
> 跨域提炼的 **agent harness 模式库**，外加一个**把任务编译成所需 harness**的可执行工具。

**Updated:** 2026-10-16 · **Status:** active · **License:** MIT

> 中文速览：本仓库现聚焦 **`harness_factory/`**——一个「agent harness」模式库 + `harness` CLI。
> *Harness* = 让 LLM 智能体在**跨会话、长时程、有限上下文**下把任务做稳的**一整套外部化方法**
> （上下文工程 · 外部记忆 · 验证门禁 · 来源考证 · 自我演化 · 工具/技能 · 变更治理 · 协作协议）。
> 工具只做**分类/选择/生成/观察/排序**，绝不编造任务实质；所有循环产物先作为**提案**，由人确认。详见
> [`harness_factory/introduction.md`](harness_factory/introduction.md) 与 [`harness_factory/GUIDE.md`](harness_factory/GUIDE.md)。
>
> **给 agent 的用法（贴一次即常驻 · standing reference）· Two steps for an agent.** ① **常驻引用**（贴一次，整个对话有效；写进项目规则文件可跨对话/子体）：「把本仓库当 harness 能力参考（常驻，直到我明确撤销）：先读
> `harness_factory/SKILL.md`，按 `reference/capability-router.md` 路由、只加载命中行点名的文件；需求模糊/偏小时先跑 `reference/requirement-refinement.md`
> （R0–R5，等我确认）。推导 harness 时产出 `AGENTS.md` + `tasks/*` + `.harness/*`（含 `.harness/capabilities.local.md`），跑 `check`；只提案、不编造任务内容。」
> ② **任务**（同一轮接着写，或下一轮再发）：直接写目标，或直接附上文件/目录。完整模板见下方
> [「Agent prompt templates」](#agent-prompt-templates--给-agent-的提示词模板) 一节。

---

## What this is · 这是什么

An **agent harness** is everything *around* the model that turns a probabilistic text generator into
a reliable, long-running worker: the context you feed it, the memory you externalize, the tools you
expose, the gates that decide "done", the provenance that keeps it honest, and the loop that makes
the harness itself improve. The model is the engine; the harness is the vehicle, the dashboard, the
seatbelts, and the maintenance manual.

This repository holds two things:

1. **A pattern library** — cross-domain harness patterns distilled so they survive removal of their
   originating project (`core/`, `domains/`, `review/`, `sources/`). Original projects appear only as
   **Exemplar** footnotes, never as the definition — see [Generalization rule](#generalization-rule--泛化铁律).
2. **The `harness` CLI** — a compiler that classifies a task, selects the modules it needs, emits a
   runnable harness scaffold, and **self-updates** its own knowledge base on a cadence.

**Key stance.** A harness may improve *efficiency and continuity* — it may **never** buy those at the
cost of *truthfulness or traceability*. Automated mechanisms may only **observe, record, and rank**;
they must never fabricate or mutate substantive output to close a task.

**Design stance.** The compiler only *classifies, selects, and emits* — it never fabricates task
substance (M0.4). Every derivation is logged in `.harness/manifest.json`. The refresh/evolution loop is
*observe-only*: it audits, counts, and ranks, then writes proposals under `updates/` for a human to
merge (M0.8). See [`harness_factory/core/01-meta-principles.md`](harness_factory/core/01-meta-principles.md).

---

## Quickstart · 快速开始

```bash
cd harness_factory

# fastest path: set the config once (how to reference/use this repo as a skill), then give the task —
# same turn or next. It reads harness_factory/SKILL.md and derives/emits the harness itself (no install). Or use the CLI:
PYTHONPATH=src python -m harness_factory derive --task "write a literature review with citations" --json
harness derive --task "write a literature review with citations over several weeks"
harness init   --task "add unit tests to the parser" --out ./my-task   # --out defaults to ./<slug>
harness check  --dir ./my-task
harness gate   --dir ./my-task          # runtime gates: structural + runs the emitted check.py
harness harvest --dir ./my-task         # observe-only: append a signal line to <kb>/updates/signals.jsonl
harness plugins --validate              # third-party domain/template plugins (read-only over the SSOT)
harness skill                            # agent load-index; `harness skill M4` prints a module
harness capabilities                     # requirement -> capability -> modules map
harness catalog --class deep-research    # unified harness catalog: list/search/filter

# frontier-standard ratchet: aim at the best-known bar (every domain has a rubric)
harness standard --domain deep-research bar brief --level R4 --name "SOTA report" --source https://…
harness standard --domain deep-research score brief --set fidelity=2 --set coverage=3
harness standard --domain deep-research audit brief   # weighted gap, largest first
harness standard --domain deep-research raise brief   # ratchet the floor (refuses a regression)
harness standard --domain deep-research plan brief    # gaps -> harness config (modules + tools)

# profile + learn from a real project (observe-only, project -> factory)
harness profile --project ./myproj --goal "…"
harness derive  --task "…" --project ./myproj   # adapt the harness to the project
harness learn   --task "…" --project ./myproj   # -> updates/cases.jsonl
harness cases

# self-update + intel + self-evolution (all human-gated, all reversible)
harness refresh --provider all --intel   # tracked sources -> proposals + updates/INTEL.md
harness refresh-apply --accept <id>      # human gate -> proposals
harness sources --group harnesses        # every tracked entity (labs, harnesses, venues, people, media)
harness intel   --since 2026-01-01       # pull tracked feeds -> updates/INTEL.md (+ intel.jsonl)
harness evolve                           # coverage/gap audit -> updates/EVOLUTION.md (proposals)
harness evolve --dry-run                 # same, write nothing
harness evolve-apply --accept <id|target>
```

**Consumption modes.** L0 — an assistant reads `harness_factory/SKILL.md` + `core/` + `data/*.json` and derives itself
(no install); L1 — run the CLI from the path (`PYTHONPATH=src python -m harness_factory …`);
L2 — an installed package. **L2 (packaging) is cancelled as a distribution channel** — see
[`harness_factory/tasks/DISTRIBUTION.md`](harness_factory/tasks/DISTRIBUTION.md) §8.

**Offline by default.** Everything runs offline — `derive`, `init`, `check`, `gate`, `harvest`, `profile`, `learn`,
`cases`, `standard`, `catalog`, `plugins`, and `skill` need no network. Only `refresh` and `intel` (external
RSS/YouTube feeds) and the optional LLM classifier (`HARNESS_LLM_*`) reach the network.

**Two roots.** The **tool home** (catalogs, corpus, cycle output) lives in user space
(`%LOCALAPPDATA%\harness-factory`, overridable with `HARNESS_HOME`); each **target project** receives
its generated files via `init --out` (or directly from the agent). In path mode the home is optional.

**Requirement → harness, and mutual learning.** Module selection is driven by a data-driven **capability map**
(`data/capabilities.json`): a requirement (task features) matches capabilities, which annotate the enabled
modules — new requirements are added by editing JSON, not code. And the tool **learns from every project it
configures**: `profile` describes a target project (observe-only), `learn` records a case, and `evolution` turns a
capability that keeps recurring into a human-gated proposal. Projects teach the factory; the factory's next
harness is better.

**Sources & intel.** `data/sources.json` is the tracked-entity registry: **projects & labs** (OpenAI, Anthropic,
Google DeepMind, Meta, Mistral, DeepSeek, Moonshot/Kimi, …), **vendor harnesses** (Agents SDK, Claude Code, MCP,
Gemini CLI, ADK, A2A, Llama Stack, …), **venues** (Nature/Science/NeurIPS/ICML/ICLR/ACL/arXiv), **people**
(Karpathy, Ilya, LeCun, Hassabis, …), **self-media** (Substack/YouTube/newsletters), **libraries** (Project
Gutenberg, Standard Ebooks, Internet Archive, Open Library, HathiTrust, DOAB), and **tools** (search:
Exa/Tavily/Brave/SearXNG; academic: Semantic Scholar/Crossref/Scite; retrieval: FAISS/Qdrant; crawl:
Trafilatura/Jina; screening: Rayyan/ASReview; eval: GAIA/BrowseComp/HLE). Feeds are RSS/Atom; YouTube `@handle`
pages are resolved to channel feeds on the fly — `refresh`/`intel` pull them as **proposals only**.

---

## Agent prompt templates · 给 agent 的提示词模板

Set the tool up in **two steps**: paste the **configuration** once — it makes the factory a *standing
reference* for the whole conversation (and beyond, if it lives in the project's rules file) — then give the
**task** each time, in the same turn or the next (attachments welcome). The assistant keeps using it until
you say to stop.

**Step 1 · Configuration (paste once — becomes a *standing reference*)**

```text
STANDING REFERENCE (until I revoke it) — use ./harness_factory as my harness capability reference for this
whole conversation.

1. Read ./harness_factory/SKILL.md first; its load-index is authoritative.
2. Route: read ./harness_factory/reference/capability-router.md and load ONLY the files the matching row names.
3. If my ask is vague / under-aimed: run ./harness_factory/reference/requirement-refinement.md (R0 restate -> R1 elevate -> R2 classify constraints hard/soft/assumed -> R3 offer MVP/Elevated/Exploratory -> R4 confirm with me -> R5 converge) and WAIT — do not start work before I confirm.

Standing behaviour: before each substantive answer, check whether a capability applies; when you use one,
declare which capability + which file. Keep it active until I say "stop using harness_factory".
When deriving a harness: emit only AGENTS.md, tasks/PLAN.md, tasks/PROGRESS.md and .harness/* (incl.
capabilities.local.md); keep "Generated by harness-factory" + .harness/manifest.json + provenance; run `check`.
Bidirectional flow: task-specific capability notes stay in the task's own .harness/capabilities.local.md;
only generalisable patterns go back as proposals (updates/, gitignored) — never edit data|core|domains|templates directly.
Never fabricate task substance (M0.4); truth/traceability outrank speed (M0.1/M0.2); irreversible acts need my OK.
```

> **Durable.** Paste the same block into the target project's rules file (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, …)
> and it survives a new conversation and spawned subagents. **Revoke:** "stop using harness_factory". Canonical
> version: [`harness_factory/SKILL.md`](harness_factory/SKILL.md) §"PASTE THIS EXACT INSTRUCTION" — keep them in sync.

**Step 2 · Task (same turn or next)**

Just write the goal, or attach files / directories / links. Example:

```text
Add complete type annotations and unit tests to the existing Python project, with a verifiable closed loop.
```

**Variant task lines** (use after the configuration):

| Situation | Task line |
|---|---|
| Set up a harness for a new project/task | "Derive and emit the required harness for «<goal>»." |
| Want the plan only, no files | "Derive the harness plan for «<goal>» (per module: rule, reason, capability match) — plan only, write no files." |
| Dissect an existing project and learn from it | "Scan <project path> from the `profile` angle; emit `PROFILE.md` and record it as a case (observe-only); observe only — don't change the project." |
| Aim at the highest standard | "Using `domains/excellence/standard-ladder.md`, set an R4-level apex bar for «<goal>», list the weighted gaps and the config to close them." |

**Domain task lines** (optional, after the configuration):

- **writing** — "Build a writing harness with the writing domain: fix the thesis and outline first, force a
  traceable citation for every claim (semantic-scholar / crossref / openalex), run an originality check and
  verification after the first draft, then self-score against the `writing` rubric and ratchet the floor (no regressions)."
- **excellence** — "Process <artifact> with the excellence domain's highest-standard ratchet: name a traceable top
  bar (R4+, with sources), score against the domain rubric → audit the largest gap → improve → ratchet the achieved
  score into a new floor (no regression without a human exemption), and re-check whether the bar has moved."

**Save it · deterministic runs.** Keep Step 1 as an editor snippet or write it into the target project's rules file
(`AGENTS.md`, `.cursor/rules`, `CLAUDE.md`, …) so it is always in force. Prefer a reproducible, machine-verifiable
path? Use the CLI (L1, no install):

```bash
PYTHONPATH=harness_factory/src python -m harness_factory derive --task "<goal>"
PYTHONPATH=harness_factory/src python -m harness_factory init   --task "<goal>" --out <project>
PYTHONPATH=harness_factory/src python -m harness_factory check  --dir <project>
```

---

## Layout · 结构

```
harness_factory/          the project — pattern library + `harness` CLI (start here)
├── SKILL.md              agent-native entry (cardinal rules + load-index + output contract)
├── GUIDE.md              full guide: intro + command reference + 10 worked examples (bilingual)
├── introduction.md       简介：是什么 · 心智模型 · Quickstart
├── CAPABILITIES.md       generated: purpose + every harness capability (do not edit; `harness capabilities --write`)
├── pyproject.toml        dev/CI convenience only (packaging cancelled as a channel)
├── refresh.ps1           scheduler entry for the self-update loop
├── install-skill.ps1     optional: copy repo-as-skill into a skills dir
├── reference/            derivation-rules.md（规则表的 agent 可读镜像）
├── src/harness_factory/  the tool: spec·derive·classify·capabilities·assemble·check·runtime·plugins·collect·curate·journal·extract·evolution·profile·learning·standard·registry·catalog·skill·cli
│   ├── data/             modules · capabilities · domains · rubrics · levers · harnesses · watchlist · sources (.json)
│   └── templates/        emitted harness files (AGENTS.md · tasks/* · .harness/* incl. PROVENANCE.md)
├── tests/                stdlib unittest (no external deps)
├── tasks/                PLAN · PROGRESS · REFRESH · DISTRIBUTION · ASSESSMENT
├── updates/              cycle output (queue · REPORT · JOURNAL · INTEL · EVOLUTION · metrics · cases · profile · proposals)
├── core/                 跨域通用主干（M0–M8），可移植到任何项目
│   ├── 00-index.md                 核心索引 + 阅读顺序
│   ├── 01-meta-principles.md       十条承重不变式（先读）
│   ├── 02-context-engineering.md   上下文是有限资源
│   ├── 03-long-running-agents.md   外部记忆 · 心跳 · 增量推进 · 续接
│   ├── 04-verification-and-gates.md 完成定义 · 门禁分类 · 验证验证器
│   ├── 05-provenance-and-integrity.md 来源分级 · 不确定词表 · 反伪造
│   ├── 06-self-evolution.md        信号→审计→变异→日志 自演化引擎
│   ├── 07-tools-and-skills.md      工具接口 · 最小工具集 · 技能渐进加载
│   ├── 08-change-governance.md     单一来源 · 提交卫生 · 部署治理
│   └── 09-collaboration-and-sessions.md 会话协议 · 决策升级 · 多 agent 交接
├── domains/              24 学科门类 + general 兜底（每域一个 README；含 `writing/` 写作域）
│   ├── deep-research/ research/ reading/ excellence/ knowledge-management/ data-science/ model-selection/ (meta + methods)
│   ├── software-engineering/ devops/ engineering/ (engineering)
│   ├── physics/ chemistry/ biology/ earth-environment/ mathematics/ (natural sciences)
│   ├── medicine/ (health)
│   ├── economics-finance/ psychology/ social-science/ (social sciences)
│   ├── law/ humanities/ education/ arts-design/ (law/humanities/education/arts)
│   └── general/ (fallback，无独立 README)
├── review/               文献综述 · harness 分类总览与索引 · 实践者/大师 playbook · 参考文献（R1–R79）
└── _archive/             旧目录归档（docs/ external/ tools/ …，已移出版本控制）
```

## How to use this factory · 使用方式

> New here? Read [`harness_factory/GUIDE.md`](harness_factory/GUIDE.md) — full intro, command reference, and ten worked examples (bilingual).
> 初次使用请读 [`harness_factory/GUIDE.md`](harness_factory/GUIDE.md)——完整介绍、命令速查与十个实例（中英对照）。

1. **Orient** — read `core/01-meta-principles.md`. These ten invariants govern everything else.
2. **Classify the task** — pick the domain in `domains/` that matches the *kind of work*, not the *topic*. A research repo that also ships a website still uses `research/` for its research loop and `devops/` for its build loop.
3. **Assemble** — the domain file names which `core/*` modules it composes and in what order; apply them as an operating manual.
4. **Gate** — run the domain's Definition-of-Done gates before claiming anything is done (`core/04`).
5. **Evolve** — end every work session with the `core/06` loop: harvest what the session taught and route it back into the harness.

**Agent-native workflow (recommended).** Instead of (or in addition to) driving the CLI yourself, set it up in
**two steps**: paste the **configuration** once (how to reference and use this repo as a skill), then give the
**task** — same turn or next (see [Agent prompt templates](#agent-prompt-templates--给-agent-的提示词模板)). The assistant
reads [`harness_factory/SKILL.md`](harness_factory/SKILL.md), loads only the modules it needs via the load-index
(`harness skill`), derives with `reference/derivation-rules.md` + the `data/*.json` catalogs, emits the output
contract into the target project, and records provenance in `.harness/PROVENANCE.md`. It can also `profile`/`learn`
the project so the factory keeps improving.

---

## Generalization rule · 泛化铁律

> **A pattern earns a place here only if it survives removal of its originating project.**

Concretely, when writing or extending a file here:

- State the pattern as a **rule/invariant/recipe** in domain-neutral terms.
- If a concrete detail is needed to make it vivid, label it **Exemplar** and name the source project — never let the exemplar become the definition.
- Anything that only makes sense inside one project (a specific table name, a specific scripture index) is **not** a core pattern; it belongs in that project's local harness, and here at most as an exemplar footnote.
- Prefer **named, checkable mechanisms** (a gate, a signal, a ledger schema) over vague advice.

See [`harness_factory/sources/source-map.md`](harness_factory/sources/source-map.md) for exactly which upstream artifact each pattern was distilled from.

---

## Documentation map · 文档地图

| What you want | Where |
|---|---|
| **Standing reference (paste once)** | [`harness_factory/SKILL.md`](harness_factory/SKILL.md) §"PASTE THIS EXACT INSTRUCTION" |
| **Use directly from an agent (L0)** | [`harness_factory/SKILL.md`](harness_factory/SKILL.md), `harness_factory/reference/derivation-rules.md` |
| **Locate the capability a task needs** | [`harness_factory/reference/capability-router.md`](harness_factory/reference/capability-router.md) |
| **Refine a vague / under-aimed ask** | [`harness_factory/reference/requirement-refinement.md`](harness_factory/reference/requirement-refinement.md) |
| **Bidirectional capability flow (task ⇄ factory)** | [`harness_factory/reference/capability-flow.md`](harness_factory/reference/capability-flow.md) |
| **Copy-paste prompt templates** | [Agent prompt templates](#agent-prompt-templates--给-agent-的提示词模板) (in this file) |
| Positioning, layout, usage | this file — [`README.md`](README.md) / [`README.zh-CN.md`](README.zh-CN.md) |
| Full guide + worked examples | [`harness_factory/GUIDE.md`](harness_factory/GUIDE.md) |
| **Harness capabilities overview (generated)** | [`harness_factory/CAPABILITIES.md`](harness_factory/CAPABILITIES.md) |
| Mental model + quickstart | [`harness_factory/introduction.md`](harness_factory/introduction.md) |
| Core harness invariants | `harness_factory/core/01-meta-principles.md` |
| Domain playbooks | `harness_factory/domains/*/README.md` |
| Literature & catalog | `harness_factory/review/` |
| Plans & progress | `harness_factory/tasks/PLAN.md`, `harness_factory/tasks/PROGRESS.md` |
| Completeness & integration review | [`harness_factory/tasks/ASSESSMENT.md`](harness_factory/tasks/ASSESSMENT.md) |
| Self-update + evolution | `harness_factory/tasks/REFRESH.md`, `harness_factory/src/harness_factory/evolution.py` |

Licensed under MIT — see [`LICENSE`](LICENSE). 中文入口见 [`README.zh-CN.md`](README.zh-CN.md)。
