# Harness Factory

> **A generalizable library of agent-harness patterns, distilled across domains.**
> 跨域提炼、面向迁移复用的 **agent harness 模式库**。

**Updated:** 2026-10-12 · **Status:** active · **License:** MIT (see repo root)

---

## 中文速览

**这是什么。** *Harness* = 让一个（编码 / 科研 / 数据）智能体在**跨会话、长时程、有限上下文**条件下稳定把任务做对的**一整套外部化方法**：上下文工程、外部记忆、验证门禁、来源考证、自我演化、工具/技能接口、变更治理、协作协议。

**本库的目标是「泛化」而非「记录」。** 每一条模式都从具体项目里提炼，但**写成与具体项目无关的形式**——任何「用 LLM 智能体做某类工作」的仓库都可直接套用。原项目只作为**出处示例（Exemplar）**标注，不构成定义。

**结构。** `core/` 放**跨域通用**的 9 条主干模式；`domains/` 放各学科门类（20 个）的**域内专属**编排；`review/` 是对「AI harness」这一主题的**文献综述**与 `harness-index.md` 统一索引；`sources/` 是**提炼溯源表**（哪个模式来自哪份一手材料）。**完整介绍与实例见 [`GUIDE.md`](GUIDE.md)。**

**怎么用。** 新任务先读 `core/01-meta-principles.md`；再按任务性质进入对应 `domains/*`；实现时把对应 `core/*` 文件当作**操作手册**逐条落实；收尾跑域内的验证门禁。

---

## What a "harness" is · 什么是 harness

An **agent harness** is everything *around* the model that turns a probabilistic text generator into a reliable, long-running worker: the context you feed it, the memory you externalize, the tools you expose, the gates that decide "done", the provenance that keeps it honest, and the loop that makes the harness itself improve. The model is the engine; the harness is the vehicle, the dashboard, the seatbelts, and the maintenance manual.

**Key stance (inherited, generalized):** a harness may improve *efficiency and continuity* — it may **never** buy those at the cost of *truthfulness or traceability*. Automated mechanisms may only **observe, record, and rank**; they must never fabricate or mutate substantive output to close a task. (See `core/01-meta-principles.md` §M0.)

---

## The tool · 工具（`harness` CLI）

The library is executable. The `harness` CLI **compiles any task into the harness it needs** (rules over M0–M8; optional LLM assist), and **self-updates** its knowledge base on a cadence.

```bash
# task -> harness plan (explainable: which rule fired, and why)
harness derive  --task "write a literature review with citations over several weeks"
harness derive  --task "add unit tests to the parser" --json

# task -> harness scaffold on disk (.harness/manifest.json records every choice)
harness init    --task "add unit tests to the parser" --out ./my-task   # --out defaults to ./<slug>
harness check   --dir ./my-task          # verify the emitted harness (gate)

# agent-native consumption (no install): point an assistant at this repo + a task goal,
# or call the CLI from the path:
PYTHONPATH=src python -m harness_factory derive --task "…" --json
harness skill                            # print the agent load-index; `harness skill M4` prints a module
harness capabilities                     # the requirement -> capability -> modules map

# frontier-standard ratchet (aim at the best-known bar; applies to every domain)
harness standard --domain deep-research bar brief --level R4 --name "SOTA report" --source https://…
harness standard --domain deep-research score brief --set fidelity=2 --set coverage=3
harness standard --domain deep-research audit brief    # weighted gap (largest first)
harness standard --domain deep-research raise brief    # ratchet the floor (refuses a regression)

# profile a target project + learn from it (observe-only, project -> factory)
harness profile --project ./myproj --goal "…"   # -> updates/profile/<slug>.{json,md}
harness derive  --task "…" --project ./myproj   # adapts the harness to the project (weak domain hint)
harness learn   --task "…" --project ./myproj   # record a case -> updates/cases.jsonl
harness cases                                   # aggregate learned cases

# self-update loop (M5): pulls sources as PROPOSALS only
harness refresh --provider all --intel   # file + tracked feeds + (LLM if configured) -> intel
harness refresh-apply --accept 0 2601.12345   # human gate -> proposals

# intel + self-evolution (tracked sources: labs, vendor harnesses, venues, people, self-media)
harness sources --group harnesses        # list every tracked entity (109 across 7 groups)
harness intel --since 2026-01-01         # pull tracked feeds -> updates/INTEL.md (+ intel.jsonl)
harness evolve                           # audit coverage/gaps -> updates/EVOLUTION.md (proposals)
harness evolve --dry-run                 # same, write nothing
harness evolve-apply --accept <id|target>  # human gate -> updates/accepted.json (reversible)
```

`data/sources.json` is the tracked-entity registry: **projects & labs** (OpenAI, Anthropic, Google
DeepMind, Meta, Mistral, DeepSeek, Moonshot/Kimi, …), **vendor harnesses** (Agents SDK, Claude Code,
MCP, Gemini CLI, ADK, A2A, Llama Stack, …), **venues** (Nature/Science/NeurIPS/ICML/ICLR/ACL/arXiv),
**people** (Karpathy, Ilya, LeCun, Hassabis, …), **self-media** (Substack/YouTube/newsletters),
**libraries** (Project Gutenberg, Standard Ebooks, Internet Archive, Open Library, HathiTrust, DOAB), and
**tools** (search: Exa/Tavily/Brave/SearXNG; academic: Semantic Scholar/Crossref/Scite; retrieval: FAISS/Qdrant;
crawl: Trafilatura/Jina; screening: Rayyan/ASReview; eval: GAIA/BrowseComp/HLE).
Feeds are RSS/Atom; YouTube `@handle` pages are resolved to channel feeds on the fly.

**Agent-native first · 面向 agent 的用法.** The most flexible way to use this is to **point a
vibe-coding assistant (Claude Code / opencode / Cursor / …) at this repository plus a task goal**.
Read [`SKILL.md`](SKILL.md) first: it carries the cardinal rules, a load-index, the output contract,
and the provenance requirement, so the assistant can derive and emit the harness itself — no install.
The deterministic CLI (from the path) stays available when reproducibility matters. **Packaging
(`uv tool install` / PyPI) is cancelled as a distribution channel** (rationale in
`tasks/DISTRIBUTION.md` §8).

**Requirement → harness, and mutual learning · 需求配置与相互学习.** Module selection is driven by a
data-driven **capability map** (`data/capabilities.json`): a requirement (task features) matches
capabilities, which annotate the enabled modules — new requirements are added by editing JSON, not code.
And the tool **learns from every project it configures**: `profile` describes a target project
(observe-only), `learn` records a case, and `evolution` turns a capability that keeps recurring into a
human-gated proposal. Projects teach the factory; the factory's next harness is better.

**Two roots.** The **tool home** (catalogs, corpus, cycle output) lives in user space
(`%LOCALAPPDATA%\harness-factory`, overridable with `HARNESS_HOME`), so the tool runs from any
directory. Each **target project** receives its generated files via `init --out` (or from the agent, at
L0). In path mode the home is optional.

**Design stance.** The compiler only *classifies, selects, and emits* — it never fabricates task substance (M0.4). Every derivation is logged in `.harness/manifest.json`. The refresh loop is *observe-only*: it audits/counts/ranks and writes proposals under `updates/`; a human merges (M0.8). See `tasks/PLAN.md` for architecture and `tasks/REFRESH.md` for the self-update loop and scheduling.

---

## Layout · 结构

```
harness_factory/
├── README.md                      ← 本文件：定位 · 结构 · 用法
├── GUIDE.md                       项目指南 · Project Guide：介绍 + 命令速查 + 9 个实例（中英对照）
├── SKILL.md                        agent-native entry (cardinal rules + load-index + contract)
├── introduction.md                简介：是什么 · 心智模型 · Quickstart
├── pyproject.toml                 dev/CI convenience only (packaging cancelled as a channel)
├── refresh.ps1                    scheduler entry for the self-update loop
├── install-skill.ps1              optional: copy repo-as-skill into a skills dir
├── reference/derivation-rules.md  markdown mirror of the rule table (for L0 agents)
├── src/harness_factory/           the tool: spec·derive·classify·capabilities·assemble·check·collect·curate·journal·extract·evolution·profile·learning·standard·registry·catalog·skill·cli
│   ├── data/                      modules.json · capabilities.json · domains.json · rubrics.json · harnesses.json · watchlist.json · sources.json
│   └── templates/                 emitted harness files (AGENTS.md · tasks/* · .harness/* incl. PROVENANCE.md)
├── tests/                         stdlib unittest (no deps)
├── tasks/                         PLAN.md · PROGRESS.md · REFRESH.md · DISTRIBUTION.md
├── updates/                       cycle output (queue · REPORT · JOURNAL · INTEL · EVOLUTION · metrics · cases · profile · proposals)
├── core/                          ← 跨域通用主干（可移植到任何项目）
│   ├── 00-index.md                核心索引 + 阅读顺序
│   ├── 01-meta-principles.md      十条承重不变式（先读）
│   ├── 02-context-engineering.md  上下文是有限资源
│   ├── 03-long-running-agents.md  外部记忆 · 心跳 · 增量推进 · 续接
│   ├── 04-verification-and-gates.md 完成定义 · 门禁分类 · 验证验证器
│   ├── 05-provenance-and-integrity.md 来源分级 · 不确定词表 · 反伪造
│   ├── 06-self-evolution.md       信号→审计→变异→日志 自演化引擎
│   ├── 07-tools-and-skills.md     工具接口 · 最小工具集 · 技能渐进加载
│   ├── 08-change-governance.md    单一来源 · 提交卫生 · 部署治理
│   └── 09-collaboration-and-sessions.md 会话协议 · 决策升级 · 多 agent 交接
├── domains/                       23 disciplines · 23 个学科门类（每域一个 README）
│   ├── deep-research/ research/ reading/ excellence/ knowledge-management/ data-science/ model-selection/ (meta + methods)
│   ├── software-engineering/ devops/ engineering/ (engineering)
│   ├── physics/ chemistry/ biology/ earth-environment/ mathematics/ (natural sciences)
│   ├── medicine/ (health)
│   ├── economics-finance/ psychology/ social-science/ (social sciences)
│   ├── law/ humanities/ education/ arts-design/ (law/humanities/education/arts)
│   └── general/ (fallback，无独立 README)
├── review/
│   ├── practitioner-playbook.md   顶尖实践者技能提炼（Karpathy 及同级/更高级同行）
│   ├── masters-playbook.md        跨行业顶级人物的「能力支架」提炼（投资/创业/产品/科学/风险/内容/教育）
│   ├── harness-catalog.md         全部 agent harness 与自演化方法的分类总览（散文式）
│   ├── harness-index.md           全部 harness 的查找索引（由 data/harnesses.json 生成）
│   ├── ai-harness-survey.md       AI harness 全方位调研与文献综述
│   ├── references.md              合并参考文献（IEEE，统一编号 R1–R79）
│   └── references.bib             BibTeX
├── sources/
│   └── source-map.md              提炼溯源：模式 ← 一手材料
└── _archive/                      旧仓库目录归档（docs/ external/ tools/ …）
```

---

## How to use this factory · 使用方式

> New here? Read [`GUIDE.md`](GUIDE.md) — full intro, command reference, and nine worked examples (bilingual).
> 初次使用请读 [`GUIDE.md`](GUIDE.md)——完整介绍、命令速查与九个实例（中英对照）。

1. **Orient** — read `core/01-meta-principles.md`. These ten invariants govern everything else.
2. **Classify the task** — pick the domain in `domains/` that matches the *kind of work*, not the *topic*. A research repo that also ships a website still uses `research/` for its research loop and `devops/` for its build loop.
3. **Assemble** — the domain file names which `core/*` modules it composes and in what order; apply them as an operating manual.
4. **Gate** — run the domain's Definition-of-Done gates before claiming anything is done (`core/04`).
5. **Evolve** — end every work session with the `core/06` loop: harvest what the session taught and route it back into the harness.

**Agent-native workflow (recommended).** Instead of (or in addition to) driving the CLI yourself, point
a coding assistant at this repo and give it a task goal. The assistant reads [`SKILL.md`](SKILL.md), loads
only the modules it needs via the load-index (`harness skill`), derives with `reference/derivation-rules.md`
+ the `data/*.json` catalogs, emits the output contract into the target project, and records provenance in
`.harness/PROVENANCE.md`. It can also `profile`/`learn` the project so the factory keeps improving.

---

## Generalization rule · 泛化铁律

> **A pattern earns a place here only if it survives removal of its originating project.**

Concretely, when writing or extending a file here:

- State the pattern as a **rule/invariant/recipe** in domain-neutral terms.
- If a concrete detail is needed to make it vivid, label it **Exemplar** and name the source project — never let the exemplar become the definition.
- Anything that only makes sense inside one project (a specific table name, a specific scripture index) is **not** a core pattern; it belongs in that project's local harness, and here at most as an exemplar footnote.
- Prefer **named, checkable mechanisms** (a gate, a signal, a ledger schema) over vague advice.

See `sources/source-map.md` for exactly which upstream artifact each pattern was distilled from.
