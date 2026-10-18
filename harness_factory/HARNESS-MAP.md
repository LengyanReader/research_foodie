# Harness Map · Harness 地图

> **Generated** from the catalogs + the CLI + the skill index -- **do not edit by hand**; run `harness map --write` (also refreshed by `harness catalog --write`).
> **生成文档**：由 SSOT 与 CLI 生成，**请勿手改**；用 `harness map --write` 重新生成（`harness catalog --write` 亦会同步刷新）。

**9 modules (M0–M8) · 27 capabilities · 28 domains · 160 catalog entries · 23 CLI subcommands**

---

## 中文速览

这张地图把 harness_factory **所有部件**画在一页上：9 个核心模块（M0–M8）、27 条能力（capability，任务特征 → 模块）、28 个学科域、160 条工具目录、23 个 CLI 子命令、以及 L0/L1 两种消费形态。它回答三个问题：**(1)** 有哪些部件；**(2)** 每个部件的数据源（SSOT）在哪；**(3)** 改完 SSOT 后跑哪条命令同步。整份文档**由代码生成**（`harness map --write`），并由 `tests/test_harness_map.py` 做漂移守卫——因此它随每次更新自动保持一致。

## 0 · At a glance · 一览

| surface · 面 | count | SSOT | view |
|---|---|---|---|
| Core modules | 9 (M0–M8) | `data/modules.json` | `core/00-index.md` |
| Capabilities | 27 | `data/capabilities.json` | [`CAPABILITIES.md`](CAPABILITIES.md) |
| Domains | 28 (27 + `general`) | `data/domains.json` | `domains/<id>/README.md` |
| Tool catalog | 160 (12 classes × 46 kinds) | `data/harnesses.json` | [`review/harness-index.md`](review/harness-index.md) |
| Rubrics | 29 | `data/rubrics.json` | `domains/excellence/standard-ladder.md` |
| Levers | 75 | `data/levers.json` | `harness standard plan` |
| CLI subcommands | 23 | `src/harness_factory/cli.py` | §7 below |
| Emitted templates | 11 | `src/harness_factory/templates/` | §8 below |

## 1 · The map · 全景

```
              you point an assistant at this directory (or paste the standing line)
                                    │
              ┌─────────────────────┴─────────────────────┐
              │ L0 · agent-native        L1 · CLI-from-path │
              │ SKILL.md + core/ + data  python -m harness_factory
              └─────────────────────┬─────────────────────┘
                                    ▼
   task ──▶ feature vector ──▶ capability match ──▶ modules M0–M8 ──▶ emitted harness
            (classify.py)       (capabilities.json)   (derive.py)      (.harness/, tasks/, AGENTS.md)
                                                                              │
                          ┌───────────────────────────────────────────────────┘
                          ▼
   updates/  ◀──proposals──(M5 self-evolution)── read: review/ · sources/ · updates/
             human gate
```

## 2 · How a task becomes a harness · 任务 → harness

1. **Classify** the goal into the 8-axis feature vector (`horizon·verifiability·stakes·grounding·artifact·tool_surface·collaboration·domain`).
2. **Match** every capability whose `when` matches that vector (`data/capabilities.json`).
3. **Select** the core modules M0–M8 the rules enable, with per-module reasons (`derive.py`).
4. **Annotate** the enabled modules with the matching capabilities -- explainability only, never an override (M0.4).
5. **Emit** the scaffold (`init`): `AGENTS.md`, `tasks/PLAN.md`, `tasks/PROGRESS.md`, `tasks/decisions.md`, `tasks/gates.md`, `tasks/ledger.md`, `.harness/*` (manifest, pointer, capabilities ledger, PROVENANCE) and `.harness/check.py`.

## 3 · Core modules · 核心模块 (M0–M8)

| id | module | rule | doc |
|---|---|---|---|
| M0 | Meta-principles · 元原则 | Truth and traceability outrank speed; automate only observe/record/rank | `core/01-meta-principles.md` |
| M1 | Context engineering · 上下文工程 | Context is a finite, scarce resource - curate, don't dump | `core/02-context-engineering.md` |
| M2 | Long-running agents · 长时程 agent | Externalize memory; advance incrementally; make every run resumable | `core/03-long-running-agents.md` |
| M3 | Verification & gates · 验证与门禁 | Define done before work; verify the verifier; hard vs soft gates | `core/04-verification-and-gates.md` |
| M4 | Provenance & integrity · 来源与完整性 | Every fact traceable to a primary source; uncertain means uncertain | `core/05-provenance-and-integrity.md` |
| M5 | Self-evolution · 自演化 | signal -> audit -> mutation -> journal, human-gated | `core/06-self-evolution.md` |
| M6 | Tools & skills · 工具与技能 | Minimal toolset; biased errors; skills load progressively | `core/07-tools-and-skills.md` |
| M7 | Change governance · 变更治理 | Single source of truth; reviewable diffs; no unsolicited destructive acts | `core/08-change-governance.md` |
| M8 | Collaboration & sessions · 协作与会话 | Explicit contracts; escalate decisions; hand off with state | `core/09-collaboration-and-sessions.md` |

## 4 · Capabilities · 能力（27）

A capability is a *reusable requirement*: it fires when the task's feature vector matches its `when`, then **annotates** the already-enabled modules with why they matter (M0.4). Trigger renderer shared with `CAPABILITIES.md`; full text (fires-when + why) there.

| capability | modules | fires when |
|---|---|---|
| `baseline-discipline` | M0, M1, M7 | always · 总是 |
| `verification-gate` | M3 | always · 总是 |
| `resumable-memory` | M2 | horizon ≥ session |
| `traceable-sources` | M4 | grounding ∈ {preferred, required} (来源要求) OR artifact ∈ {document, dataset, knowledge_base} (产物) |
| `self-improving-loop` | M5 | horizon ≥ multi_session |
| `tool-use` | M6 | tool_surface ∈ {read, read_write, external} (工具面) |
| `human-review-gate` | M8 | collaboration ∈ {human_review, multi_agent} (协作) OR stakes ∈ {high} (风险) |
| `high-stakes-guardrails` | M3, M8 | stakes ∈ {high} (风险) |
| `reproducible-experiments` | M3, M4, M5 | domain ∈ {data-science, research} (领域) and verifiability ∈ {high} (可验证性) |
| `long-horizon-autonomy-control` | M2, M3, M8 | horizon ≥ multi_session and stakes ∈ {high} (风险) |
| `frontier-standard` | M3, M5, M8 | domain ∈ {excellence} (领域) OR (verifiability ∈ {high} (可验证性) and horizon ≥ multi_session) |
| `sandboxed-execution` | M3, M6, M7 | tool_surface ∈ {external} (工具面) OR stakes ∈ {high} (风险) |
| `portable-skills` | M6 | tool_surface ∈ {read, read_write, external} (工具面) |
| `ambition-elevation` | M0, M3, M8 | horizon ≥ session |
| `expert-instruments` | M3, M4, M6 | verifiability ∈ {high} (可验证性) OR horizon ≥ multi_session |
| `cross-field-crew` | M6, M8 | collaboration ∈ {multi_agent} (协作) OR horizon ∈ {long_running} (时间跨度) |
| `bidirectional-capability-flow` | M0, M5, M7 | always · 总是 |
| `context-budget-policy` | M1, M2 | horizon ≥ session OR tool_surface ∈ {read, read_write, external} (工具面) |
| `untrusted-content-discipline` | M4, M6, M7 | tool_surface ∈ {external} (工具面) OR artifact ∈ {document, knowledge_base} (产物) OR grounding ∈ {required} (来源要求) |
| `durable-execution` | M2, M3 | horizon ≥ multi_session |
| `cost-budget-caps` | M3, M7 | tool_surface ∈ {external} (工具面) OR horizon ≥ multi_session |
| `eval-driven-development` | M3, M5 | verifiability ∈ {high} (可验证性) OR horizon ≥ multi_session |
| `loop-discipline` | M2, M3, M6 | tool_surface ∈ {read_write, external} (工具面) OR horizon ≥ multi_session |
| `graph-orchestration` | M2, M8 | collaboration ∈ {multi_agent} (协作) OR horizon ≥ multi_session |
| `formal-verification` | M3, M4, M6 | domain ∈ {mathematics, logic} (领域) OR (verifiability ∈ {high} (可验证性) and artifact ∈ {code} (产物)) |
| `dimensional-analysis` | M3, M6 | domain ∈ {physics, engineering, chemistry, earth-environment} (领域) |
| `empirical-measurement` | M3, M4 | domain ∈ {psychology, cognitive-science, medicine, economics-finance, social-science, education} (领域) |

## 5 · Domains · 学科域

28 domains across 10 faculties (`general` is the always-available fallback). Each domain is a *workflow + signals + artifact* hint; it adds no rule (M0.5).

| faculty | domains |
|---|---|
| arts · 艺术 | `arts-design` |
| education · 教育 | `education` |
| engineering · 工程 | `data-science`, `devops`, `engineering`, `model-selection`, `software-engineering` |
| formal-sciences · 形式科学 | `logic` |
| health · 健康 | `medicine` |
| humanities · 人文学科 | `humanities`, `linguistics`, `reading`, `writing` |
| law · 法学 | `law` |
| meta · 元 | `deep-research`, `excellence`, `general`, `knowledge-management`, `research` |
| natural-sciences · 自然科学 | `biology`, `chemistry`, `earth-environment`, `mathematics`, `physics` |
| social-sciences · 社会科学 | `cognitive-science`, `economics-finance`, `psychology`, `social-science` |

## 6 · Tool catalog · 工具目录（160）

`data/harnesses.json` indexes third-party agent harnesses, frameworks, protocols, evaluation tools and safety work, each mapped to the modules it exercises. Lookup with `harness catalog`.

| class | entries |
|---|---|
| coding · Coding / software harnesses | 12 |
| orchestration · Orchestration frameworks / agent SDKs | 11 |
| self-evolution · Self-evolution methods | 15 |
| memory · Memory & persistence | 5 |
| skills-protocols · Skills ecosystems & protocols | 4 |
| evaluation · Evaluation harnesses | 11 |
| survey · Surveys (orientation) | 5 |
| safety · Safety of self-evolution | 2 |
| discovery · Discovery / evidence & model search | 5 |
| reading · Reading, acquisition & distillation | 20 |
| deep-research · Deep research — search, retrieval & synthesis | 43 |
| instruments · Scientific & formal instruments (evidence tools) | 27 |

## 7 · CLI surface · 命令行（23 subcommands）

`PYTHONPATH=<harness_factory>/src python -m harness_factory <cmd>` (or the installed `harness`).

| cmd | what it does |
|---|---|
| `derive` | show the derived harness plan |
| `init` | write the harness scaffold to a directory |
| `explain` | explain a generated manifest |
| `check` | run a generated harness self-check |
| `gate` | run an emitted harness's runtime gates (structural + emitted check.py) |
| `harvest` | harvest observed signals from an emitted harness (observe-only) |
| `plugins` | list/validate third-party domain & template plugins |
| `refresh` | pull new/leading sources (proposal only; never edits docs) |
| `refresh-apply` | human gate: accept queued candidates into proposal stubs |
| `sources` | list tracked sources (projects/harnesses/venues/people/media) |
| `intel` | pull tracked feeds and extract intel into updates/INTEL.md |
| `evolve` | self-evolution audit: coverage/gaps -> mutation proposals (no writes to catalogs) |
| `evolve-apply` | human gate: accept evolution proposals into updates/accepted.json |
| `doctor` | show resolved paths, config, and LLM status |
| `self-update` | refresh the tool's own catalog from packaged defaults |
| `skill` | print the agent load-index, or one module (agent-native entry) |
| `capabilities` | list the capability map (requirement -> modules) |
| `map` | whole-factory overview (modules/capabilities/domains/CLI) -> HARNESS-MAP.md |
| `profile` | scan a target project -> PROFILE.md + capabilities (observe-only) |
| `learn` | profile a project + record a case (project -> factory learning) |
| `cases` | show aggregated learned project cases |
| `standard` | frontier-standard ratchet: name the bar, score, audit, raise (domains/excellence) |
| `catalog` | unified harness catalog: list / search / filter (data/harnesses.json) |

## 8 · Entry points & load order · 入口与加载顺序

The agent-native load index (`harness skill`). Read top-down; load only what you need (M0.6). Domain READMEs are omitted here -- see §5.

| load | path | why |
|---|---|---|
| `skill` | `SKILL.md` | Cardinal rules + load-index + output contract. Read first. |
| `index` | `core/00-index.md` | Library index (how core/domains/review fit). |
| `map` | `HARNESS-MAP.md` | Whole-factory map: modules/capabilities/domains/CLI + how to regenerate. |
| `M0` | `core/01-meta-principles.md` | Meta-principles: truth/traceability outrank speed. |
| `M1` | `core/02-context-engineering.md` | Context is scarce; curate, don't dump. |
| `M2` | `core/03-long-running-agents.md` | Externalize memory; resumable runs. |
| `M3` | `core/04-verification-and-gates.md` | Define done first; verify the verifier. |
| `M4` | `core/05-provenance-and-integrity.md` | Every fact traceable; uncertain = uncertain. |
| `M5` | `core/06-self-evolution.md` | signal->audit->mutation->journal, human-gated. |
| `M6` | `core/07-tools-and-skills.md` | Minimal toolset; progressive skills. |
| `M7` | `core/08-change-governance.md` | Single source of truth; reviewable diffs. |
| `M8` | `core/09-collaboration-and-sessions.md` | Explicit contracts; escalate; hand off state. |
| `capability-router` | `reference/capability-router.md` | Start here: situation -> capability -> module -> file (external-task router). |
| `derivation-rules` | `reference/derivation-rules.md` | Markdown mirror of the derive.py rule table (for L0). |
| `requirement-refinement` | `reference/requirement-refinement.md` | R0-R5: restate -> elevate -> classify -> offer -> confirm -> converge. |
| `capability-flow` | `reference/capability-flow.md` | Bidirectional flow: concretize (task-local) <-> distill (factory, human-gated). |
| `evidence-instruments` | `reference/evidence-instruments.md` | M3.10 made concrete: claim type -> instrument -> catalogued tool -> gate evidence. |
| `capabilities` | `CAPABILITIES.md` | Generated overview: purpose + every harness capability (requirement -> modules). |
| `reference` | `review/references.md` | Source-grounded reference list. |
| `harness-catalog` | `review/harness-catalog.md` | Prose taxonomy of harnesses & self-evolution methods. |
| `harness-index` | `review/harness-index.md` | Generated lookup index of all cataloged harnesses. |
| `survey` | `review/ai-harness-survey.md` | AI harness survey. |
| `source-map` | `sources/source-map.md` | Where every claim comes from. |
| `modules.json` | `src/harness_factory/data/modules.json` | Machine-readable module catalog. |
| `capabilities.json` | `src/harness_factory/data/capabilities.json` | Requirement->capability->modules map. |
| `domains.json` | `src/harness_factory/data/domains.json` | Machine-readable discipline/domain catalog. |
| `harnesses.json` | `src/harness_factory/data/harnesses.json` | Unified harness catalog (SSOT for the index). |
| `sources.json` | `src/harness_factory/data/sources.json` | Tracked entities + feeds. |
| `watchlist.json` | `src/harness_factory/data/watchlist.json` | Refresh topics + frontier probes. |

## 9 · Data sources → views · SSOT 与生成视图

| SSOT | drives | generated view |
|---|---|---|
| `data/modules.json` | M0–M8 + params | `core/*` (hand), §3 |
| `data/capabilities.json` | requirement → modules | `CAPABILITIES.md` |
| `data/harnesses.json` | tool catalog | `review/harness-index.md` |
| `data/domains.json` | disciplines + signals | `domains/<id>/README.md` |
| `data/rubrics.json` | per-domain excellence bar | `harness standard` |
| `data/levers.json` | gap → modules/tools | `harness standard plan` |
| `data/watchlist.json` | M5 frontier probes | `updates/REPORT.md` |
| `data/sources.json` | tracked entities + feeds | `updates/INTEL.md` |

## 10 · Keeping this current · 如何保持同步

This document is **generated**: edit an SSOT, regenerate, done.

| after you edit… | run | refreshes |
|---|---|---|
| any `data/*.json` | `harness catalog --write` | `review/harness-index.md` + `CAPABILITIES.md` + `HARNESS-MAP.md` |
| `data/capabilities.json` | `harness capabilities --write` | `CAPABILITIES.md` |
| anything | `harness map --write` | this file |

`tests/test_harness_map.py` fails when the file is stale; the fix is always `harness map --write`. An emitted harness reads the factory through `.harness/pointer.json`, and the standing reference lives in `SKILL.md`.

## See also · 参见

- [`CAPABILITIES.md`](CAPABILITIES.md) -- the same guarantees, per capability.
- [`reference/capability-router.md`](reference/capability-router.md) -- *situation → capability → file*.
- [`review/harness-index.md`](review/harness-index.md) -- the tool catalog.
- [`GUIDE.md`](GUIDE.md) · [`introduction.md`](introduction.md) -- usage, mental model.
