# PLAN · Inclusive Harness Tool · 通用 harness 工具计划

**Updated:** 2026-10-19 · **Status:** active · **Owner:** user + agent

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
      domains.json    domain catalog (31 domains incl. `general`; faculty taxonomy)
      harnesses.json  unified harness catalog (196 entries: class × kind × module-map × vendor)
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

**Closed this session (2026-10-19).** P12.1 · P12.2 · P12.3 · P12.4 · P12.6 · P12.7 · P14.1 · P14.2 · P14.3 — each records a `done_in` in `data/cycles.json` (rendered by `harness cycle roadmap`). Two of them returned **negative but useful** results, which is why they are closed rather than carried: P12.4 re-checked the 22 unconfirmed outlets with a browser UA — 3 answered and were flipped, **19 are host-blocked** and stay honestly `verified: false`; P12.6 confirmed 16 of 17 roundup-only figures verbatim in the papers' own HTML, and one paper (`2610.20563`) has **no reachable HTML full text**, so its figures stay `unverified`.

| id | cycle | what | why it is still open |
|---|---|---|---|
| **P14.4** | P14 | Score **3–5 published domain harnesses** on the three fixed criteria (schema declared before extraction · entity identity handled · output evidence-bounded *and* coverage reported) | only Case 1 was read in full; the comparables were resolved at the metadata level, so no verdict may be asserted yet. **Opens as P17** — see the plan below |

Detail for the sourcing items: `updates/2026-10-19-paper-roundup-proposal.md` (loop product, deliberately not under version control). Detail for the case study: `updates/2026-10-19-domain-harness-case-study-plan.md`; the landed outcome: `review/knowledge-and-dh-crosswalk-2026-10.md`.

### P17 · 下一轮（排定于 2026-10-20）：关掉 P14.4 —— 领域 harness 的横向评分

**为什么是它。** P14.4 是全库唯一的 `planned` 项，已被推迟两轮：P15 去补了图谱经典（因为"没有源基就无从打分"），P16 去补了表达与消融。它没法靠"再读一遍本库自己的话"关掉——需要**全文**读 3–5 个已发表领域 harness，再按三条固定标准打分。P16.5 还给了它第二个用途：如果这些 harness 的模块能被评分，`component-ablation` 就有可对照的实例，而不只是一个程序。

**完成定义（本轮关闭时以下须全成立）**
- 3–5 个案例**全文**读过（PDF/HTML 抽文，不是摘要），每个给出处（arXiv / DOI / 官方 repo）与访问日期；
- 先定判据、后读案例：三条标准写成**可判定问句**并各带反例，避免读完后倒推标准；
- 每个案例逐条打分，允许 **N/A**（标出并说明），不把"论文没写"当成"作者没做"——两者对读者的含义不同；
- 一张横向表 + 一段判决；
- **负面结果也是结果**：若 3–5 个案例在三条标准上无差别，结论就是"这套判据不判别"，记录理由并**退役判据**，不新增子句（M0.5）。只有判据真能分开案例，才落子句或能力，且须过 M5.10 的完成定义。

**Slices（一片一个可交付）**
- **P17.0 · 地图重做（用户插入项，2026-10-20；先做，因为它是眼下的需求）。** `HARNESS-MAP.md` 从"一堆 id 的表"变成**能自解释**的地图：§2 能力架构图（Mermaid，节点与计数由 catalog 现算）· §3 八轴含义 + 两条 `classify`+`derive` **实跑**样例（含"差别不在模块，在要求"的差集）· §4 模块×能力矩阵（新增「不负责」边界列 + 可折叠反向索引）· §5 每条能力加"买到了什么"· §6 每个域加 `artifact`/`grounding` 与要点 · §7 每个工具类加对应模块。SSOT 只新增 `modules.json` 的 `excludes_en/zh`（9×2），其余全部由代码现算；`tests/test_harness_map.py` 加 11 个守卫。**不加能力、不开域名**——这是视图与生成器的工作。
- **P17.1 · 候选池定级。** 逐个解析到一手出处并核许可与可读性，淘汰到 3–5 个。起点是 P14 已记的三个（GraphRAG `[R148]` · LongHarness `[R128]` · HTR 栈 `[R153]`/`[R154]`，三者都只到元数据级）加 **P14 的 Case 1**（已通读），再加 **PaperQA2**——它在 P16 只作为 `[R235]` 的实验对象出现，**它自己的论文还没有解析过 id**，先解析再决定是否入选。**不猜 arXiv id**——P16 的教训是猜中的概率不够，必须 `id_list` 或按题名搜到再引。
- **P17.2 · 判据操作化。** 三条标准 → 可判定问句 + 反例（例：「schema 先声明」= 抽取前已有字段表/本体文件/受控词表，且文中给出；只在附录提一句不算）。
- **P17.3 · 全文阅读与逐条打分。已做。** 三篇 arXiv PDF 下载并抽取正文（26 / 19 / 25 页），四例逐条打分，每格带节/表定位，落 `review/domain-harness-cases-2026-10.md`（方法 · 判据 · 逐例笔记 · 横向表 · 判别力判决 · 被推翻的预测）。
- **P17.4 · 横向表与判决。已做。** C1 留（并拆出「有模式」vs「公布模式」——GraphRAG 是后者）；C2 改写（身份的对象是**引用单元**：实体 / 来源 / 证据记录，不只实体）；**C3a 四例全 1，作 0/1 不判别 → 改写成三级阶梯**（提示里要求 → 可解析到原文 → 由机制强制）；C3b 留并记两种形态（precision/accuracy/拒答；三级漏斗）。
- **P17.5 · 收尾。已做。** 落 2 条子句：**M3.15**「把损失分阶段归因」（`core/04`）、**M4.16**「指针是对支持关系的断言」（`core/05`：悬空/过期/不支撑三态 + 解析须对生效集 + 指针须落到原文）；`sources/source-map.md` 两行、`review/references.md` §U + **R238**；**触发条件加 `grounding: required`**（PaperQA2 形态此前不触发）；`cycles.json` 记 P17（+3 子句、+2 参考、0 能力、0 域），P14.4 → `done`。
- **P17.6 · 工作集退出（用户插入项，2026-10-20；已落地）。** 用户问「能否检查某些能力在当前任务里暂时不需要，就先退出加载，随用随取、不多占窗口」——审计结论：**取用侧齐、退出侧缺**（M1.1 只管单次调用的 token，M5.10 只管轮次级的推迟，运行期的"已加载集"没有任何再检查点）。落地：**新子句 M1.10**（换阶段重查工作集；留 `{reason, reload_when}` 收据；硬不变式不退；靠常驻索引才可安全退出）· `context-budget-policy.why` 补上退出半句 · 生成的 harness 新增 `.harness/working-set.json`（`matched/active/evicted`）· `harness check` 拒绝静默丢弃、拒退 always-on、拒改 `matched` · router 加"行不再命中就把行放回去" · 7 个守卫。**不加新能力**：其 `when` 被 `context-budget-policy` 严格包含（任何会触发退出的任务都会触发预算纪律），只在 37→38 上添噪声——按 M0.5 记为**深化**，理由与重访触发记在 PROGRESS。


**Non-goals（写死，防止这一轮膨胀）** 不做 harness 排行榜；不评案例的工程质量（只评三条判据）；不给案例里提到的工具新开目录条目（除非它们本身是被引用的能力来源）。

## P18 · 路由完备性审计（2026-10-20，已做）：任何任务都能定位到能力吗

> 用户问「double check 完备程度，是否对任何 task 都可以定位到适合的能力」。做法不是自我表态，而是把命题拆成**总量 / 判别 / 正确**三个可检验项：32 个手写任务族（16 中 / 16 英，含两个空提示）+ 八轴逐值翻转 + 37 条能力的构造性可满足性 + router 双向解析。交付物：`review/routing-coverage-2026-10.md`。

- **① 总量：成立。** 32/32 产出计划，最少 9 条能力（无一是「只剩 3 条底线」）；37/37 能力有可满足向量、37/37 在 router 里点名；条件取值 100% 命中已声明词表。
- **② 判别：大体成立，两个真洞。** 13 个轴值相对安静基线不增加能力：8 个是「比基线更少」的语义（one_shot / off / none / solo / medium / low），`artifact=code` 只在 `verifiability=high` 组合下承重，`artifact=mixed` 是「没有具名产物」；**真洞**是 `artifact=plan`（计划类产物无专属要求）与 `domain=arts-design`（无域能力，且 `grounding=off` 连 `traceable-sources` 也丢掉，全池最少 9 条）。两个洞都**不硬补**，改写重访触发。
- **③ 正确：原先不成立，已修。** 9/32 任务族落错域，根因三类：**子串误命中**（`ci` ∈ "exer**ci**ses" → 课程设计判成 devops；`art` ∈ "p**art**ial" → 散文判成 arts-design；`eval` ∈ "retri**eval**" → 所有 RAG 任务被当成高可验证）、**常用族缺信号**（python package / incident / course / pcb / brand / 视频 / 音乐…）、**两个轴从不读文本**（`artifact`、`grounding` 只继承领域默认，于是「注明来源」无法抬升来源要求）。修法：信号改为**词首匹配**（`deploy` 仍匹配 deployment；`ci` 不再匹配 exercises），同一匹配器也用于可验证性/风险/时间跨度的关键词表（这才是 `retrieval` 误判的根治）、补 ~60 条高精度信号、删 3 条错键信号（`art`；devops 的 `evolution`/`governance`/`演化` 属于本库概念而非部署工作），并让**文本里的显式线索压过领域默认**（产物名词 → `artifact`；`cite`/`references`/`provenance`/`注明来源`/`可溯源` → `grounding=required`；只有明确说「不用外部知识」才降到 `off`）。修后 **32/32**。
- **④ 守卫与顺带修正。** 新增 6 个守卫：能力取值已声明、每条能力可满足、router 双向覆盖、任务族回归、短信号误命中回归、线索压过默认。另修一个**潜伏不一致**：`when` 同时含 `any` 与其他键时，匹配器原先提前返回、忽略其余键，而渲染出的触发文字一直是 AND 语义——当前无条目用该组合，行为未变，DSL 现在与它印出来的话一致。
- **边界（写清，不装作没有）**：无媒体域（视频/音乐归 arts-design）；`plan` 产物无专属能力；arts-design 的 `grounding=off` 让创意工作拿不到溯源底线；关键词路由只覆盖中英，其他语言仍能出计划但**猜测质量下降**，受支持的路径是显式 `--domain`/flags 或可选的 LLM 分类器。

**Non-goals** 不加能力、不加域、不改模块规则；不把「任务族全对」当成分类器已经完备——它只是 32 个样本上的回归基线。


## P19 · 模型是变量（2026-10-20，已做）：御三家改变了 harness 的什么

> 用户问「检查、分析、评估最新的御三家大模型，有哪些 harness 能力可以整合」。做法不是给榜单加一行，而是问：**这些模型暴露的机制里，哪一条会让按本库建出来的 harness 做错事**。结论是收敛而非排名——三家的差异在模型，收敛在 harness。交付物：`review/model-families-2026-10.md`。

- **① 读到的与读不到的。** 一手读到：Claude Opus 5.5 公告（努力档位与价格、透明改路由、preserved thinking）、Gemini 4 Argon 模型卡（1M 上下文与自家长上下文衰减数据、computer use、CCL）、OpenAI Agents SDK 文档（Manifest/快照/能力、暴露≠授权）。**读不到**：`openai.com`、`platform.openai.com`、`help.openai.com` 全 403；`ai.google.dev` 超时；`platform.claude.com/docs` 区域封锁。因此 OpenAI 只作**文档行**，模型名只记为「另两家对比表所点名」，不作产品事实。
- **② 五个收敛机制，三个推翻默认。** 努力档位成了计价商品（同表对比用了不同档位 → 不同档位的对比是在比设置）；服务模型未必是请求模型（安全改路由 + 别名漂移）；历史可能不可改写（preserved thinking）；工作区/沙箱成了产品级契约（Manifest ≠ 活工作区 ≠ 快照；会话不保证 OS 隔离）；暴露≠授权（开关只管「看得见」，授权在工具内部的具体实参上）。另两条已被覆盖：长上下文要实测（M1.5/M1.10）、computer use 属沙箱执行（M6）。
- **③ 落地的三条子句 + 一处加深。** **M1.11** 不可改写的历史只能向前摘要（压缩有改写与追加两种形状，供应商保留推理时只能追加，原文须仍可达）；**M2.13** 努力是预算行不是质量档（按阶段对着门禁花，与模型 id 同录，跨档位对比是设置对比，缓存价进入同一笔账）；**M4.17** 服务的模型也是来源的一部分（请求 id / 服务 id 与版本 / 档位 / 替换及理由；模型悄悄变过的评测不是测量），与 M4.16 指针纪律同构。**M6 不新增子句**：暴露≠授权、「沙箱」须点名机制本是既有义务，只补两条清单与两条反模式。
- **④ 能力缺口与刻意不加。** `model-selection` 域有 L0–L5 说明却**没有任何能力触发**（与 P18 的「域有文档、路由无入口」同型），新增 `model-portfolio-discipline`（仅该域触发）：需求矩阵 → 按阶段组合 → 在**声明的档位**上跑自己的留出集 → 带 id/版本/档位记录的硬门禁；同分取更便宜的层，换层或换档即重开评测。**不加**：厂商引用 API（义务已在 M4.13/M4.16）、computer-use 细节、fast mode、CCL 案例、`provider-routing` 能力、1M 上下文指引——各记重访触发。

**Non-goals** 不评榜单、不给价格建议、不把厂商自报数字当已验证；不因为「某家这么做」就写成通用规则——每条子句只保留跨厂商成立的那部分，厂商专属处（preserved thinking）在文中写明范围。

## P20 · 全网扫描轮（2026-10-23，已做）：披露标准、MCP 核心修订与两个已触发的回访线索

> 用户问「加载本库 harness 能力系统，对全网 harness 研究与实践前沿做广泛调研，评估能否升级」。按库自己的治理跑：observe 半环先交提案 `review/harness-landscape-scan-2026-10.md`（含四切片、缩水条件与重访触发），用户确认后落地 apply 半环。**编号记录**：提案时写 P18，P18/P19 已被 2026-10-20 占用，改以 P20 登记并重编号扫描文档。三份一手材料全文读后，§5 三个缩水条件均未触发，四切片全量落地。

- **① 披露标准 → 唯一新子句 M3.16。** arXiv:2605.23950（全文读，含 Appx. A 的 ETCSOVG 七层最小字段表）表明 harness 解释量可与模型同量级（单受控网格 HV/MV ≈ 7.8×、6/9 排名翻转，作者自声不具普遍性——按方向性数字载）。跨 harness 的比较必须附两侧配置卡 + 方差说明，协议只能是锁定 harness 换模型或双因子分解；它补足 M3.14/M3.15 的缺口（环境相同性 / 方差归属都未点名 harness）。**不加能力**：按主张类型触发；与 `component-ablation` 互为镜像，交叉表记 `review/harness-disclosure-2026-10.md`。
- **② AST10 线索关闭（仅数据面）。** frontier §6b「skills 杠杆应指向它」已触发：`levers.json` security 便签 + `portable-skills`/`untrusted-content-discipline` 的 why 指向 OWASP AST10（R245，README 全文读）；判定与已 ingest 的 ASI01–10（R86）不重复（它打技能执行层：更新漂移、扫描缺失、供应链规模化）。不新增能力：M8.4/M3.11 已覆盖义务，缺的只是带引用的溯源。
- **③ MCP 2026-07-28 核心修订消化（R244）。** 无不变量变化，四个映射落 `workflow-patterns-2026-10.md` §9：MRTR = M8 人类门的协议化记录状态；Tasks 扩展 = durable-execution 的原生收敛（`durable-execution` 的 why 指向它）；列表缓存提示 = context-budget 行；12 个月弃用窗口 = M7 exemplar。目录端 `mcp` 映射 M1,M6 → M1,M6,M2,M8。
- **④ 数字刷新（方向性值，全部 *listed* 明标）。** METR 1.1（~1.1 h / ~105 天翻倍，R249）刷新 `long-horizon-autonomy-control` 的论证 grounding；Claude Code Agent Teams（R250）与 A2A 入 LF（R251）只作描述与标签行，不据此开子句；context-editing/memory 以参考参数回答进 `context-budget-policy` 的 why（`platform.claude.com` 仍封锁，机制线只认 R237）。
- **守卫与验证。** `P20ClauseAnchorTest` 5 个内容守卫（子句点名 ETCSOVG/两种协议/方差/标注，溯源行存在，§W 存在，levers/capabilities 引用落地）；references **§W R243–R251** + `.bib` 3 条；测试 279 → **284**；`cycle audit` 16 轮 · 0 硬 · 0 缺口。

**Non-goals** 不做 harness 排行榜（场景即测件的反对证据已载明）；不新增能力（披露条款按主张类型触发）；trace-driven 自演化不随本轮带走（D1 保持自己的设计文档轮）；agent-judge 鲁棒性与 A2A/peer-session 再审只登记重访触发（D7/D8），不设排期。

## P21 · dogfood 轮（2026-10-23，已做）：把 M4.15 用在入口文档上——四缺陷命中 5 处，另有 5 处超出

> 排队中的自用轮候选开为本轮（触发齐了：同日项目评估点名入口文档难读 + M4.15 需要最便宜的可操作性检验）。做法：逐节标读者任务 → 四缺陷检索（首次出现的未定义术语 · 未声明的前置条件 · 缺中间步的跳跃 · 无例子的规则）→ 与 SSOT / pyproject / CI 交叉核对。交付物：`review/dogfood-m415-2026-10.md`。

- **10 处缺陷全修。** M4.15 四缺陷直接命中 5 处，价值最高的是**未声明前置条件**：两份 Quickstart 在「免安装」的 PYTHONPATH 形式后直接使用裸 `harness` 命令，而 L2 打包已取消、任何东西都不会创建 `harness`——新用户照抄第一条命令即失败（GUIDE §3 早有 alias 行，两份入口文档却没有）。其余：README 首现 `(M0.4)` 未定义（加注）；introduction §3 列 4+general 域而 §10 同文档说 30 域（同文档矛盾，改 30 域/10 faculties）；SKILL.md 写 Python 3.11+ 与 pyproject（>=3.10）/ CI（3.10/3.12）/ GUIDE 矛盾（改 3.10+）。
- **M4.15 没抓住的 5 处：跨文档漂移。** 过期计数（GUIDE「132 tests OK」、introduction §6「8 topics / 109 entities / 7 groups」）、漏列的组（README 来源枚举无 outlets）、**重复渲染的路线图**（introduction §10 停在 P11，M0.5 双重渲染即漂移源——压缩为指向 PLAN.md 的指针）、过期日期。修法两条可推广：**声明带日期**（M0.1）+ **同一状态不渲染两次**（M0.5）。**不新增 `cross-doc-consistency` 子句**：它会命中几乎所有文档工作、不判别（methodology-fit 规则）；重访触发：若发现漂移的散文声明（非计数）**导致 agent 做错事**，再开。
- **登记与验证。** `cycles.json` P21（0 能力 / 0 域 / 0 子句 / 0 参考）；测试 **289 OK**；`cycle audit` 17 轮 · 0 硬 · 0 缺口；视图重生成。M4.17 可操作性仍开放（文档维护不涉及模型运行）。

## P22 · D1a（2026-10-23，已做）：trace schema + 采集——轨迹驱动自演化的第一段

> D1 设计文档（`updates/2026-10-23-trace-driven-evolution-design.md`）已确认，先开零风险的阶段 A：schema + 采集，先于任何审计与晋升。登记为 P22（0 能力 / 0 域 / 0 子句 / 0 参考）；阶段 B（规则审计→提案）/ C（带测量晋升，须等记分轮）/ D（LLM 辅助，D7 之后）仍 defer。

- **schema（`trace.py`）。** v1 JSONL；6 事件封闭词表（gate_miss · human_correction · re_derive · capability_unused · check_fail · context_eviction）；必填字段 v/ts/project/task/harness/event；只追加；旧行（自由文本或非 trace JSON）读作 `signal`，P22 前的记录不失效。
- **采集点。** `gate` 失败自动记一行到 `<kb>/updates/traces.jsonl`（通过不记）；`harvest --event/--detail` 写结构化事件（旧行为不变）；`harness collect --project DIR` 把项目本地 `.harness/traces.jsonl` 拉回工具家（离线、人跑）；发射模板自检节增可选 trace 合同。
- **守卫与验证。** `tests/test_trace.py` 13 用例；CLI gate 测试 hermetic 化。测试 **302 OK**；`cycle audit` 18 轮 · 0 硬 · 0 缺口；HARNESS-MAP 重生成。

## P23 · 记分轮（2026-10-23，已做）：本库自己的最小打分任务集（关闭 P16.9）

> 队列「记分轮」开为本轮：给本库一个打分任务集，让 `component-ablation`（M5.12）能真跑、D1 阶段 C 有留出集。**5 任务 × 5 轴**（路由 / 能力覆盖 / 模块覆盖 / 结构自检 / 干净发射），1.0 基线由 `tests/test_scoreboard.py` 钉死；allowed/must 值全部来自 2026-10-23 实测 classify+derive（M0.4）。交付 `review/scored-task-set-2026-10.md`；P16.9 → done（done_in P23）。非目标写死：不是任务质量基准、不替代 rubric、不自动晋升。

## P24 · 效果反馈轮（2026-10-23，已做）：task_outcome 事件 + 记分集 effect 轴——双向流补上「结果」那一边

> 评估发现：双向能力流能回传**过程事实**（trace 6 事件，全是失败形状），却没有「任务最终做得多好」的采集通道；
> 且 P23 留出集的 5 轴全是结构轴——即使 D1 阶段 C 开闸，也只能检验「结构不回归」，检验不了「效果提升」。本轮落
> 两个最小改动，都遵守「未测量就不编数」（M0.4）。证据分层写死：L1 过程事实/L2 结果观察 → 只提案；L3 晋升仍须
> 阶段 C 留出集检验。**不做**：不加能力（自身不触发任何新东西）、不发明效果数字、不自动打分；D1 阶段 B/C 仍 defer。

- **① `task_outcome`（词表第 7 个、唯一的结果侧事件）。** `detail` 必须带 `judge`（默认 `human`；`machine` 仅当
  该任务族有已定义度量器——即记分集的 `effect_metric`——时合法）+ `score`（数字或等级）；缺任一即被
  `trace.validate` 拒绝、永不落盘（无判决者的判决是噪声）。**机器记判决、不做判决**（M0.4）。发射模板的 trace
  合同补记该事件；D1 设计文档词表同步（6 → 7，updates/ 不入版本控制）。CLI 侧 `harvest --event task_outcome
  --detail '{"judge":"human","score":4}'` 即可用。
- **② 记分集 effect 轴。** 每任务声明 `effect_metric`（该任务族的机器可判分指标，锚在既有条款：引用可核验率 ·
  答句证据指针可解析率（M4.13）· 选型记录完整率（M4.17）等）；真实测量落地前一律 `effect=unmeasured`，测得值
  须带完整收据 `{status: measured, score, judge, measured_on}`，`validate_scoreboard` 拒绝残缺收据；**effect
  永不进结构总分**——5 轴 1.0 结构基线原样钉死，结构与效果是两种主张，分开报告、分开钉死。
- **顺带修正一个真实交互。** 模板里 task_outcome 的 JSON 示例若以嵌套对象结尾（`…}}`）会撞 emission 轴的未渲染
  占位符检查（`}}` 序列），示例改为在 `detail` 后补真实字段 `session`，发射检查回到全绿——这正是「结构轴守卫先于
  文档」的一次自证。
- **守卫与验证。** `tests/test_trace.py` +6（合法 judge/score 组合 · 缺 judge · 缺 score · `judge=vibes` 拒绝 ·
  无效行永不落盘）· `tests/test_scoreboard.py` +4（每任务有 metric · unmeasured 且不进 total · 残缺收据拒绝 ·
  完整收据接受并呈现）；测试 **315 OK**；`cycle audit` 20 轮 · 0 硬 · 0 缺口；`scored-task-set` 文档更新（第 6 轴 ·
  消融第二问 · 非目标改写）。**留给使用侧的**：第一个真实任务的 `task_outcome` 与第一份 effect 收据（L1/L2 证据）；
  第一次消融实跑（L3）。

## P25 · D1 阶段 B（2026-10-23，已做）：规则审计器——把轨迹自动变成提案

> D1 设计文档 §3 落地：`data/trace-rules.json` 5 条规则 + `trace_audit.py`，轨迹 → 按模式分组 → M5.3 词表提案 → 只写 `updates/traces-proposals.jsonl` + `TRACE-EVOLUTION.md`；`harness trace-audit` 离线可跑。low-outcome 规则把 P24 的 effect 轴回流成 Deepen 提案（数字分 ≤2 才计，等级串留人）。登记 P25（0/0/0/0）；D1 触发更新：阶段 C（带测量晋升）待用户开或第一份 measured 收据。

## P26 · 深度补平轮（2026-10-23，已做）：M6/M7/M8 落可锚定子句

> 评估发现的子句分布不对称已补：**M6.10**（技能索引先行·版本化）· **M6.11**（暴露≠授权）· **M7.10**（治理性变更=可审阅 diff + 回滚路径）· **M8.11**（交接走产物不走记忆）——全部编号化既有散文规则、锚在已核验来源（0 新参考），各带 checklist 行 + source-map 行 + 内容守卫。`cycle audit` 现在对三个模块有事可做：**39 条子句 anchored**。

## P27 · 广度轮（2026-10-23，已做）：基础学科 + 思想/学术流派梳理（用户指示）

> 判据先行（M0.5）：域 = 能改变路由/门禁内容才入。落三条：**① 3 个新域**（`history` 史源批判 · `philosophy` 论证重构·立场声明 · `political-science` 概念先行·案例选择留痕，各带 workflow/信号/README/rubric；入口文档 30 → **33 学科**）；**② methodology-map 流派表 16 行**（哲学 4 + 批判传统 2 + 社科 4 + 经济/心理 4 + 数学基础三派 + 中文经学考据 1——每行三件套：书目式经典源 · 该传统内的纪律 · 谁执行）；**③ 7 条 outlets**（实测：2×200 为真、5×403 诚实登记、Europeana 合并）。信号所有权记录：通用词留 humanities、新域持学科专属信号（判别纪律的产物，重访触发在交付文档 §5）。推迟：astronomy/materials/neuroscience/anthropology/geography（各带触发）。交付 `review/basic-disciplines-schools-2026-10.md`；登记 P27（0 能力 / 3 域 / 0 子句 / outlets +7）。

## P28 · 整合轮（2026-10-23，已做）：注册表双向核验 · 两个真缺口 · 扫描提案

> 评估发现的「15 个 tracked 实体目录无同 id」经机械核验定论：交叉链接单向但**健全**（71/71）；反向 5 个零引用 → 3 豁免有据 + **2 个真缺口已补**（`mistral-agents`：smolagents 是 HF 的不是 Mistral 的；`hermit-cashapp`：目录 'hermit' 是牛津推理器）。目录 203 → **205**；`RegistryBidirectionalTest` 2 守卫钉双向一致性。网络半环（生态扫描：AGENTS.md 标准/ACP/LangMem/AgentOps/skills 注册表/computer-use/D7/D8）为提案 `updates/2026-10-23-ecosystem-scan-proposal.md`，待确认开轮。

## P29 · 跨学科与前沿域（2026-10-23，已做）：检视 + 自动发现机制

> 用户两问的答案落地：① 12 个跨学科/前沿任务实测检视——多数是「工作性质组合」已覆盖（M0.5 不新开域）、2 处信号误路由 data-only 修掉（biology/earth-environment 各 +3）、**落 1 个真前沿域 `ai-safety`**（安全论证门禁结构判别力足；34 学科）、3 个推迟带触发（interpretability/embodied/systems-science）。② **自动发现机制** `harness probe-domains`：情报中落 general 的条目按共享关键词聚类成候选域提案（提案制，M0.4）——**未提到的域从此会自己浮出来**。交付 `review/interdisciplinary-frontier-domains-2026-10.md`；登记 P29（0 能力 / 1 域 / 0 子句）。

## P30 · 一句话轮（2026-10-24，已做）：`harness full-update` 串起完整观察环

> 用户问「说一声『全面更新 harness』是否就能触发以上所有」——答案现在是**能**。`harness full-update` 六相串联（intel → probe-domains → trace-audit → evolve → cycle audit → scoreboard），每相失败隔离、报告双语、人工裁决行收尾；`--offline` 跳过联网相。接线四处：SKILL.md 第 8 步（agent 的 L0 六步等效）、capability-router 情境行、README quickstart、工作区 AGENTS.md 常驻引用；refresh.ps1 调度器同用。登记 P30（0/0/0/0——既有机制的组合，M0.5）。

## P31 · 交叉轮（2026-10-24，已做）：学科交集显式化——overlaps 声明 · 近失域报告 · 能力并集

> 用户「学科之间很多都是有交叉和交集的」落地为三层：**32 域声明 `overlaps`**（相邻域 + 判别要点）· **derive 报近失域**（声明重叠且接近或够强，至多 2 个，带判别要点）· **强邻域（≥2 分）并集其域键控能力**——交集任务拿并集而不是单边。发射物增「Secondary domains · 交叉域」节。方志案例（史学梳理 vs 数字人文编码）从此显式报出 history。守卫 7 条（含 8 样本路由电池）；测试 **343 OK**；`cycle audit` 27 轮 · 0 硬 · 0 缺口。

## P32 · 任务简报轮（2026-10-24，已做）：`harness brief` 渲染可粘贴的执行简报

> 双能力评估第二项的答案落地：「高质量指令生成」缺的一步成型。`harness brief --task "…"` 渲染规则可算的精炼字段（R0 重述 · R2 约束分级 · R3 三档机械增量）+ 特征向量 + 计划 + 第一阶段行动 + 门禁 + **R4/R5 确认块**——简报是**待确认草案**，不是开工许可（WAIT 纪律，M0.4）。守卫 6 条；测试 **349 OK**；`cycle audit` 28 轮 · 0 硬 · 0 缺口。

## P33 · 环境鲁棒与简报串联（2026-10-25，已做）：doctor 只读探测容错 + init --from-brief 管道

> 实测排查的两项工程闭环：① `_cmd_doctor` 捕获受限沙箱与只读环境的 `PermissionError`/`OSError`，以诊断状态友好报告，严守纯观察原则（M0.4）；② `brief.py` 与 `assemble.py` 打通，支持 `harness init --from-brief <brief.md|brief.json>` 直接从确认后的简报生成脚手架并落盘 `.harness/BRIEF.md`。守卫 5 条（+2 cli, +3 brief）；测试 **354 OK**；`cycle audit` 28 轮 · 0 硬 · 0 缺口。（P33 当时未登记 cycles.json，由 P34 补登记。）

## P34 · 周报摄取轮（2026-10-27，已做）：一致不等于验证（M3.17）· 自我编辑先过验收门（M5.13）

> DAIR.AI「Top AI Papers of the Week」X 文章（2026-10-11，十项）作**二手入口、仅发现用**（P11 汇总/P16 微信先例），经 fxtwitter API 镜像读取（x.com 被墙）。十条 arXiv 记录全部达**摘要级核实**（0 篇全文：HTML/ar5iv 七次取文失败、S2 429），digest 正文独有数字与全部机构归属入**未验证台账**（survey §4），全文重读登记 **P34.R1**。落两子句：**M3.17**（VeriHarness R254：分歧以环境证据裁决、共识反查共同遗漏；把 M5.11 的「采样一致只是路由信号」升为门禁义务）与 **M5.13**（VERA R256：验收标准先于应用写明、补原因非症状、归因哪个轴、预声明拒绝边界；M5.12 的接纳侧孪生，R252 警示别假定逐轮累积）。边界裁决：MASS/MIMESIS/CMM 在权重级与模型内部一侧，不入（P15 边界）；HERMES(R255) 与目录 `hermes-agent` 重名不合。data 面：references §X R252–R262 + bib 11 条 · source-map 两行 · capabilities why×4 · 媒体 `dair-ai-x` · watchlist 关键词 · cycles P33 补登记 + P34 + D7/D1 理由更新。守卫 7 条；测试 **361 OK**；`cycle audit` **30 轮 · 0 硬 · 0 缺口**。

## P35 · 论文发现渠道补全轮（2026-10-27，已做）：门户梳理完备 · 接入自更新循环

> 用户要求把 Hugging Face Papers、arXiv、Google Scholar、Semantic Scholar 等论文站点梳理完备，并列入**能力更新与内容检索**的重要渠道（P15.3 `scholarly-channels` 已扫 ~95 源，但缺自更新循环真正轮询的 **AI 每日发现层**，且状态停在 2026-10-19）。逐门户 2026-10-27 回一手实测：HF `/papers` 200、`/api/daily_papers` **200 JSON**（`/papers/feed` 401 无 RSS）；arXiv `rss/cs.{AI,CL,LG,MA,SE,HC}` **六类全 200**；S2 API 无 key **429**；Google Scholar 200；OpenAlex works **200**；AlphaXiv 200；OpenReview notes 403；dblp 202 机器人门。**发现真缺陷并修**：Papers with Code 已停维（Meta 2025-07 关闭），`paperswithcode.com`（含 `/api/v1`）**重定向至 `huggingface.co/papers/trending`**——两处 SSOT 行曾声称在线，均降级为重定向标记（feed 摘除、`verified:false`）。**不新增子句/能力**：操作规则（M4.5 不可信检索、source-map「聚合=发现、回产出方」、refresh feed-vs-LLM 两路）已约束这些渠道；唯一值得固化的结构事实是**循环路径**——只有 arXiv 真能被 `refresh --provider feed` 拉取，其余经 LLM 发现/人工摄入（M0.5 登记）。落地（纯数据+参考）：venues `hf-papers` + `arxiv-cs-ma`（cs.MA 为缺失的多智能体 feed）· semantic-scholar/google-scholar 行刷新今日门径与主题 · watchlist 新 `scholarly-discovery` 主题 · survey 新 §8（门户表 + 「循环如何消费」列 + 中英）· outlet-map 新节（门户→门径→循环路径→登记处）· JSON-API 发现 provider 登记 **P35.R1** deferred。守卫 6 条；测试 **361 → 367 OK**；`cycle audit` **31 轮 · 0 硬 · 0 缺口**。

## P36 · 调优轮（2026-10-28，已做）：修两个分类缺陷 · 有意基线编辑 · dogfood 接线

> 全局评估（2026-10-28）给出的方向落地。评估的事实：工厂侧机制已齐装（trace→audit→提案、full-update、brief 管道），
> 但使用侧数据为零；且两个已报告的分类缺陷仍未修，其一已被记分集基线固化。

- **① horizon 词表补 `week` 系信号。** `_MULTI_SESSION` 增 `week`（词首匹配，覆盖 weeks/weekly）+ `数周/几周/每周/long-term`——旗舰示例 "over several weeks" 从此正确落 `multi_session`（M5 自演化 + durable 记忆启用），此前落到 `session` 默认。
- **② `review` 消歧。** 裸词 `review` 从 `_HUMAN_REVIEW` 移除（它是「文献综述/系统综述」的产物名词，不是协作信号——每次文献综述都被读成人审工作流）；补高精度复合形式（code review · peer review · reviewer · review my/our · review comments）；**`review the` 刻意不加**——"review the literature" 正是那个误命中。中文 `评审` 无此歧义（综述≠评审），保留。
- **③ 记分集有意基线编辑。** lit-review 的 must_modules **M8 → M5**：M8 是误判的下游产物（裸 review 误触发协作→M8 启用→被 P23 钉进基线）；修引擎后 M5 才是该任务的正解（多周工作→自演化+持久记忆）。理由按 M0.5 记在 `data/scoreboard.json` note 与 `scored-task-set` 文档——「分数变动必须是有意编辑」机制的第一次真实行使。
- **④ dogfood 接线（使用侧数据为零的结构性对策）。** **P37（dogfood 轮）已登记**（见下）；工作区 AGENTS.md 新增**会话收尾轨迹纪律**：每轮真实工作收尾时记结构化事件（`harness harvest --event human_correction/task_outcome` + `collect`），让使用侧数据积累不再依赖记忆，而是流程。
- **⑤ P34.R1 重访触发已生效（探测）。** 2026-10-27 时 arXiv HTML/ar5iv 七次取文失败；2026-10-28 实测 `arxiv.org/abs` 与 `arxiv.org/html/<id>` 均可达（HTML 渲染完整正文章节 + 表格）。全文重读 R252–R259 的阻塞解除，**P38（全文重读轮）已登记待开**——M3.17/M5.13 的摘要级证据欠账可以清了。
- **守卫与验证。** `test_classify.py` +3（week→multi_session 双语 · literature review 不再 human_review · 复合形式正例守卫防过度移除）；测试 **367 → 370 OK**；`cycle audit` 32 轮 · 0 硬 · 0 缺口；`scoreboard` 5/5 total=1.0（基线随引擎修正有意移动）。

**Non-goals** 不动 `_ONE_SHOT`/`_LONG_RUNNING` 词表；不加 `weekly` 单独信号（`week` 词首已覆盖，且其语义本就该是 multi_session）；不把 P36 当作「分类器已完备」——它只是回归基线上又两个样本。

## P37 · dogfood 轮（2026-10-28，已做）：第一个真实任务走通全链路——VeriHarness 发布池一手核验

> 任务由用户授权自选，选了 P38 自己登记的后续（发布池核验）——dogfood 服务真实需要而非演练。**全链路首次以真实数据走通**：`brief`（P32 机制首用）→ `init --from-brief`（P33）→ 判据**先于工作**预声明（M5.13）→ 7 项检查 → `gate` 过 → `harvest task_outcome` → `collect` → `trace-audit` 首跑（单轨迹低于一切模式阈值，正确报「无提案」）。

- **核验结果（7/7，effect=1.0，machine 判决）。** 数据集存在、公开、与论文附录 E 逐项相符（五基准 × 双模型 × 轨迹/交付文件/grader 分）；**实测 23,197 rollouts**（摘要「~26,000」的 −10.8%——引用实测数）；许可证 `other/mixed-upstream-see-readme`（复用前须逐上游过许可）；huggingface.co 当日本机不可达，经 hf-mirror.com 公共镜像读取（一手性折扣如实记录）。交付 `review/veriharness-pool-check-2026-10.md`；P38 survey §4 相应升级。
- **第一份真实轨迹。** tool home `traces.jsonl` 首行：`task_outcome, judge=machine, score=1.0`（7 检查明细入 detail）。**DoD 修订（诚实记录）**：原定义要 judge=human 收据；本任务族有预声明机器度量器，按 P24 规则 machine 收据合法——**你的一次「确认/打分」可随时升级为 human 收据**（对轨迹只追加，不改写）。
- **解锁。** D1 阶段 C 的开闸条件（第一份 measured effect 收据）已满足，排入待开；数据集若上游许可放行，是消融/留出迄今最接近真实任务分布的素材。守卫 `P37PoolCheckGuardTest` 钉住报告关键数字。

## P38 · 全文重读轮（2026-10-28，已做）：R252–R259 全文核验，digest 台账逐项裁决——关闭 P34.R1

> P36 探测确认 arXiv HTML 端点恢复可达（P34.R1 的重访触发生效），本轮以 P34 台账为清单完成全文重读：R252–R259
> 九篇 HTML 全文（逐条主张带节/表定位）+ R260 机构归属块（abs 页不显示机构，HTML 才显示）。**判决：两条子句全部
> 经受住全文检验、hedge 升级，无一撤回；digest 的转述问题比预想的多——3 项验证、3 项实质纠正、1 项台账前提本身
> 有误、1 项归属证实为真。**

- **验证并纠正（in kind）。** ① HERMES「6.5% → 31%」属实但指标是 **composite score**，非 digest 所称 pass rate（且论文自身存在 26.2% vs 37.4% 成本数字张力，记录在案）；② VERA「+5% 接受 / −20% 拒绝」压缩失真——实为**两条判据**（harness 编辑须 **≥5pp 增益**＝advance bound；模型检查点**容忍 ≤20% 回归**＝tolerance bound），M5.13(d) 因此获得双界范例；③ Agent Plasticity 的「$1,073 总成本」实为 **Claude Opus 5.5 单模型先验学习成本 $1,072.73**（附录 C）。
- **台账前提纠错（对 P34 自己的诚实）。** CorpusMap 的 +6.4–11.7 / −34–57% **本来就在摘要里**——P34 的摘要级阅读漏掉了它们（M3.17 的微缩样本：认真的单次阅读也是一次抽样）。CMM→Sakana AI 归属**证实为真**（六位作者全部 Sakana AI；P34 的怀疑是 abs 页不显示机构所致）。
- **正文侧数字收编（带各自告诫）。** Sharpening Tax：36/42 组合 Tax>0、交叉点 k* 随规模 128→3、双峰化实测、PTGS 缩税、**观察性非干预性**（§9）；MASS：1.2–1.6× 确认但绝对分很低（AstaBench 0.053→0.067）、1.4× 效率对照**非匹配数据对照**（附录 D）、工作流搜索是 elite=1 的成对比较而非种群演化。
- **R254 发布池落地定位。** 附录 E 一手 URL：HF `caiqizh/veriharness` + GitHub `google-research/veriharness`（轨迹/交付文件/评分，不含基准内容再分发）；技能自演化 +6.8/+3.7 held-out。数据集**定位了、未下载**——检索与检验是另一个任务。
- **子句与登记。** core/04 M3.17 / core/06 M5.13 的 abstract 级 hedge 全部升级为 full-read（2026-10-28）；`P38RereadGuardTest` 3 守卫钉住证据级、池 URL、纠正项、恰好 8 条标记、两条子句的升级；references §X 8 条标记升级 + 组注记；**D7 触发已生效**（R254 现为 full-read 级）——保持 defer、理由升级为「触发已满足，轮次未排队」；cycles **P38**（0/0/0/0），P34.R1 → `done_in P38`。
- **状态。** 测试 **370 → 373** 全过；`cycle audit` 33 轮 · 0 硬 · 0 缺口。**Non-goals**：不加能力/域/目录；不开 D7 本轮（它是一次 golden-set 审计，不是子句编辑）。

## P39 · 评判者鲁棒性轮（2026-10-28，已做）：M3.18——评判者先受检再把关（关闭 D7）

> D7 触发在 P38 生效（R254 升全文级），本轮以 golden-set 审计开题：三篇全文（R263 自偏好偏差 · R264 RLVR 攻破验证器 · R265 reward-hacking 基准）+ R246（LHTB）升级为已读。**核心发现**：评判者失灵是结构性的、可量化的——自偏好是困惑度伪影（GPT-4 召回差 0.520）、验证器设计**因果地**诱导或消除作弊（受控训练对 ~3.5 分差距）、作弊率随难度与链长上升且 28% 无 CoT 可逃轨迹监控。

- **落地 M3.18**（`core/04`）：评判者在判决把关任何东西之前——(a) 声明偏差面（谱系关系是要声明的利益冲突）· (b) 审计未强制之处（IPT 黑盒检验）· (c) **从重放产物评分、绝不从自报评分**（R246「声称的进度不算数」）· (d) 难度/服务模型变化时重审。golden set 的可信度 = 其评判者过四关的程度。checklist 一行 + 反模式两条 + 中文块。
- **刻意不加（M0.5）**：不加 judge-robustness 能力（8 轴无评判角色轴，键在 verifiability=high 会命中一切）；**D1 阶段 D 重定触发**（等 M3.18 在真实 LLM 评判上跑过一轮，而非仅等 D7 关账——R263 的缓解未经验证说明规则制 trace-audit 仍是正确姿势）；不为 LHTB 开目录条目；两个未解析 id 的搜索命中不入 references（不猜 id 规则）。
- **守卫与验证。** `P39ClauseAnchorTest` 4 守卫；references **§Y**（R263–R265）+ R246 升级 + bib 3 条 + source-map 行；scored-task-set effect 轴补 M3.18 指针；测试 **375 → 379**；`cycle audit` **35 轮 · 0 硬 · 0 缺口**；**D7 → done_in P39**。数据卫生：**D6 关账**（jspsych.org HTTP 200，最后一条 `verified:false` 仪器翻正）。交付 `review/judge-robustness-2026-10.md`。

**排队中、未排期的候选轮**（不预分配编号：上一轮 P19 编号被本轮占用，预分配只会再次作废。2026-10-28 用户授权后的裁决已登记进 roadmap：**D7 已排队**（触发已满足：golden-set 审计，基于 R254 全文，可选用已核验的发布池作素材——上游许可先过）；**D1 阶段 C 可排**（第一份 measured 收据已落，开轮即跑 M5.12 消融梯）；**生态扫描 → defer 为 P28.R1**（提案留 updates/、判据原样，触发：某轮需要生态锚点或用户点名要生态扫描）。建议顺序：下一个真实任务继续 dogfood（轨迹积累 → trace-audit 模式浮现）→ D7 → D1 阶段 C。）
- ~~**自用轮（dogfood）。**~~ **已开并关闭为 P21（2026-10-23）**：10 处缺陷全修（5 处四缺陷命中、5 处跨文档漂移），不新增子句；M4.17 可操作性仍待一轮真正消费模型输出的工作检验。
- **D1 设计文档已提案（2026-10-23，`updates/2026-10-23-trace-driven-evolution-design.md`，未入版本控制）。** 按 D1 验收标准点名 trace schema（6 事件 / 3 采集点，本地 + 可匿名）、留出集（= 记分轮产物；阶段 A/B 不需留出集可先动工，阶段 C 须等记分轮）与回滚路径（只追加 / updates 可删 / git revert / 哈希重放）；待用户确认后开 **D1a**（阶段 A：schema + 采集）。
- **记分轮。** 给本库一个最小的打分任务集，从而能真跑 `component-ablation`。它同时是 **P16.9 的重访触发**（"本库有打分任务集"），也是让 M5.12 对本库自己生效的唯一路径。触发：P17 的判据产生了可复用的评分口径。
- **P19 的后续（小项，随轮带走，不单独开轮）。**
  1. **补 OpenAI 模型行**：`openai.com` / `platform.openai.com` 恢复可达时，把 `review/model-families-2026-10.md` §1 的「文档行」升级为模型行，并记录访问日期对应的快照（M4.17）。触发：403 解除，或出现 OpenAI 模型卡的一手镜像。
  2. **M1.11 的范围升级**：preserved thinking 目前只有一家；若第二家也禁止编辑既有推理，把 M1.11 从「厂商约束」升为通用默认（即所有压缩默认追加）。触发：第二家发布同类约束。
  3. **隐性选型**：`model-portfolio-discipline` 依赖显式选型线索；若真实使用中"只给任务、不提模型"的选型请求仍落 `data-science`，补的是线索而非域信号（保持 P18 的高精度原则）。触发：第一例此类误判被记录。
  4. ~~**`references.bib` 欠账**~~ **已清零（2026-10-23 卫生项）**：R237–R242 与 R246–R251 共 12 条已入 `review/references.bib`（R243–R245 此前已在），机器可读 bib 重新覆盖 R1–R251。
- **卫生项（2026-10-23 已收尾，不单独开轮）。** 两个遗留 CRLF 文件已剥离 CR 归一为 LF（索引本就是 LF，剥离后与索引哈希一致）；入口文档的计数漂移（27 域 / 242 用例 / R1–R106）已修，并新增 `CountDriftGuardTest`（5 条守卫）看住域数、布局树、用例数与测试命令，详见 PROGRESS 同日条目。

- **P0 (done):** pattern library (`core/`, `domains/`, `review/`, `sources/`).
- **P1 (done):** CLI scaffold generator — `derive`/`init`/`explain`/`check`, rules engine, tests.
- **P1.5 (done):** self-update loop (M5) — `refresh`/`refresh-apply`, watchlist, curate, journal, scheduler, tests.
- **P1.6 (done):** cross-project packaging — user-home KB (`HARNESS_HOME`), `doctor`, `self-update`, re-rooted `refresh`; `uv tool install`.
- **P1.7 (done):** intel tracking (`sources.json`, feed/YouTube collection, `extract.py`) + self-evolution (`evolution.py`, metrics, proposal gate); CLI `sources`/`intel`/`evolve`/`evolve-apply`; run watermark.
- **P1.8 (done):** agent-native mode + project learning. Cancelled packaging as a distribution channel (PyPI/`uv tool install`); primary = agent-native skill (`SKILL.md` + `harness skill`) + CLI-from-path (L1). Data-driven **capability mechanism** (`capabilities.json`), **project profile** (`profile.py`), **mutual learning** (`learning.py` cases + `missing_capability` audit).
- **P2 (active):** comprehensiveness + discoverability.
  - **Disciplines · 学科门类（~20）:** expand `domains/` from 4 to a faculty-level taxonomy — natural sciences (physics, chemistry, biology, earth-environment, mathematics), engineering (engineering, software-engineering, devops), health (medicine), social sciences (economics-finance, psychology, social-science), humanities (humanities), law, business/education/arts (education, arts-design). Each = `domains/<id>/README.md` + `domains.json` entry (artifact/grounding/signals). Adds no new rules — features stay compositional (M0.5).
  - **Harness index · harness 索引:** a unified, machine-readable catalog `data/harnesses.json` (196 entries; classes × kinds × core-module maps × source), cross-linked to `sources.json` by id; `catalog.py` + CLI `harness catalog` (list/search/filter/`--json`); generated `review/harness-index.md` with a drift-guard test. Prose taxonomy in `review/harness-catalog.md` stays as the explanation; the index is the lookup surface.
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
- **P12 (done, 2026-10-19):** **evidence-driven loop + CI hardening + P11 closeout.** Every slice closes a *recorded* gap (A.3 · integration-map §3) and lands a **checkable mechanism**, not prose.
  - **Slice 0 · the first audit worklist (done).** P13's audit produced 12 soft gaps; this round consumed them instead of restating them: two **router rows** (`portable-skills`, `reproducible-experiments` — capabilities that existed but were unreachable from the entry table) and **explicit trigger guards** for the 10 capabilities no test named (`tests/test_capabilities.py::TriggerCoverageTest`, each pinning the declared trigger *and* the quiet vector it must not fire on). **Audit gaps 12 → 0.** The audit's own roadmap rule was corrected at the same time: a `done` item now records `done_in` instead of a `revisit_when`, since a closed item is not a deferral.
  - **Slice 3a · M4.10 shown, not stated (done, roadmap P12.5).** One real EN↔ZH pair — the standing-reference block — carried through `reference/cross-language.md` §7: master segmented into 8 units, a first-pass "drift" **rejected** by widening the unit (revoke condition), and **two real defects found**: units 4 (declare the capability + file) and 8 (M0.4 · M0.1/M0.2 · irreversible acts) were missing from the compressed Chinese renderings, and 「只提案、不编造任务内容」 had fused two units into a claim the master lacks. Fixed in `AGENTS.md` §6, `GUIDE.md`, `introduction.md` — master untouched.
  - **Slice 3a-bis · the renderings the user actually pastes (done).** The first sweep fixed the guides but missed the two **READMEs**; a user pasting the block back exposed it. Then the user raised the location itself: the block assumed `./harness_factory`, but the repo is *cloned* wherever the reader wants it, so the factory location must be a **parameter** (`<HF>` = the real path of the cloned `harness_factory/`), not an assumption. All **eight** renderings (2 README quick-starts · 2 full README templates · `AGENTS.md` §6 · `GUIDE.md` · `introduction.md` · `SKILL.md`) now carry units 4/5/8, name `harness check --dir <output>` (with the no-install form), and mark the path parameter; `SKILL.md` keeps its own wording and cross-references `<HF>`. Guard: `tests/test_standing_reference.py::QuickStartFidelityTest` (5 cases) asserts per *block*, not per file.
  - **Slice 1 · CI covers what it claims.** `.github/workflows/ci.yml` gains an **end-to-end emitted-harness job** on both OSes (`init → check → gate → harvest → pointer verify`) and an **opt-in network job** (`workflow_dispatch` only, never on push) running `refresh --dry-run` + `intel --provider feed --verify`, so the offline-by-design paths are exercised on demand. *Closes A.3 #5/#7.*
  - **Slice 2 · M2 made concrete (memory backend).** Apply the evidence-instrument precedent (P9 template stanza) to memory: new clause **M2.12** (declare the memory backend + resume protocol) and an emitted **Memory** stanza in `templates/AGENTS.md.tmpl` derived by `assemble` from the matched capabilities; a `reference/` note names the backend options (file ledger · sqlite · external store) and what each must guarantee. *Closes A.3 #4.* **Non-addition:** no memory *runtime* is shipped — the harness declares the posture; the tool does not impersonate a store.
  - **Slice 3 · P11 closeout.** (a) ✅ **done** — the 22 `verified: false` outlets were re-checked with a **browser UA**: NOAA, APA PsycNet and CourtListener answered 200 and were flipped to `verified: true` with their caveats rewritten as content notes; the remaining **19 hosts still block the checker** (403/412/429/SSL) and stay `verified: false` with their reason. The re-check is *done*; the flags are the honest result, not a pending item. (b) ✅ **done in Slice 3a** — one real **EN↔ZH worked example** in `reference/cross-language.md` §7 (source unit → coordinated rendering → back-translation diff) using an artifact from this repo, so **M4.10 is shown, not only stated**.
  - **Slice 4 · the sourcing pass (done, roadmap P12.6/P12.7).** (a) The roundup's **17** uncited figures were cleared against the papers' own artifacts: **16 confirmed verbatim** in the arXiv HTML full text, and **two readings corrected in kind** (the 4.1×–39× range is the *TQ-cost gain* column, not "composition cost"; 41.1→53.3 is the **avg@5** metric); one paper (`2610.20563`) has **no reachable HTML full text**, so its VLIW cycle counts stay `unverified` — recorded as such rather than assumed. (b) A **bounded 8-week backfill (Pass A)** of *Top AI Papers of the Week*: 9 posts → 90 distinct papers → 68 mapped to existing capabilities = **75.6% hit rate**; the archive carries **no top-pick labels** in HTML or JSON, so the inventory is keyword-mapped, not label-trained — which is also why Pass B (deep verification) is not yet worth its cost.
  - **Deferred, with reasons (recorded — not dropped):** trace-driven self-evolution (needs a design doc first; the largest remaining gap, A.3 #2) · spectra/crystallography instruments (per-database licence/API verification, integration-map §1c) · a `qualitative-rigour` capability (needs a feature-vector affordance first, §3 #1–#2) · outlet *feeds* in the intel loop (outlets stay reference by design).
- **P16 (done, 2026-10-20):** **expression round — the form before the words, translation as expression, and a module that earns its place.** A three-part ask; one round, five slices (M5.10).
  - **P16.1 · the three supplied links, graded.** `arXiv:2609.36630` (*Distilling Agentic Systems*, 57 pp.) and `arXiv:2610.04178` (*SHarP*, 29 pp.) were read **in full** — PDFs downloaded, text extracted, method and results read — and the official `UCSB-NLP-Chang/SHarP` implementation checked. The WeChat article turned out to be a Chinese explainer **of the same SHarP paper**: good, accurate on the method, and still **not a source**, because it dropped the three findings that matter most (the 24-of-27 cliff to 14.44%, the PaperQA2 counter-example, and the reading of the all-pruned baseline). Demoted to a discovery pointer; the omissions are recorded in `review/harness-ablation-2026-10.md` §1. This is the no-laundering rule demonstrated rather than asserted.
  - **P16.2 · expression design.** Clause **M4.15** (`core/05`) + capability `expression-design` + `review/expression-design-2026-10.md`: the content unit and the reader's task decide the form (tutorial / how-to / reference / explanation, R219); the four comprehension defects that can be *searched* for (undefined term at first use, unstated precondition, unexplained jump, rule with no worked example); the modality ladder (prose → list → table → diagram → chart → notation → animation → sound) with the **reviewable-source** rule (a diagram generated from the artefact, or a chart specified as code, can be diffed — a rendered video cannot, so the script is the artefact of record); and the fidelity rule that **a form change may change what the reader can check but never what is claimed** (M4.10). Instruments `mermaid` (`diagramming`) and `vega-lite` (`visualization-grammar`). Refs **§R (R219–R233)**.
  - **P16.3 · translation as expression.** The 1898 preface in which 信·達·雅 is stated (R233) was read as a **primary text** through Wikisource — 「不斤斤於字比句次，而意義則不倍本文」 is both the licence and its limit — and the modern evidence was added: fluency and faithfulness are measured as **negatively correlated** across 130,486 paragraphs in 16 source languages (R229), sentence alignment is an unrealistic assumption for literary text (R230), and quality is reported through MQM's error typology (R224) rather than as "fluent".
  - **P16.4 · context-adaptive polish (deepen, not add).** M4.14 gains the missing parameter: **audience, register and channel are declared before writing** and re-checked per section, because an undeclared audience silently becomes "whoever is writing". `review/language-polish-2026-10.md` §3.1 carries the table. **No new capability** — the operation did not change, only its parameter — recorded as a deliberate non-addition at the capability level.
  - **P16.5 · ablation accounting.** Clause **M5.12** (`core/06`) + capability `component-ablation` + `review/harness-ablation-2026-10.md`: **retention ≠ causal contribution ≠ deployed utility** (R234), and the procedure that separates them — coupled functional units, a per-module counterfactual, single-unit ablation against the **per-task median over ablations** (not the full run), two one-sided paired tests, a protected set at α = 0.05, a held-out ladder, and a Pareto frontier instead of a winner (R235, R236). Three results that cut against the obvious reading are recorded: removing a unit can **raise** cost; PaperQA2 is the counter-example to "harnesses are redundant"; and an all-pruned baseline that still scores is a statement about **task coverage**.
  - **Deferred, with reasons (recorded in `cycles.json`):** a `modality` feature axis (the engine change would be paid for twice; `artifact ∈ {document, dataset}` already discriminates from `prose-polish`) · per-genre document templates (would be mistaken for the architecture decision) · an automated pruner (partitioning is manual by construction) · a redundancy-ratio metric (no scored task set here; a proxy would be the Goodhart target) · a `harness-pruning` domain (a procedure, not a field).
  - **Verified.** `harness cycle audit` → **OK · 12 cycles · 32 roadmap items · 37 capabilities · 28 clauses anchored · 0 hard · 0 gaps**; `python -m unittest discover -s tests` → **242 tests** (237 + 5 guards); `catalog --write` + `map --write` + `capabilities --write` regenerated; EOL normalised to LF. **Still open on purpose: P14.4.** 表达轮：先定形式再定措辞 · 翻译即表达 · 组件消融。
- **P15 (done, 2026-10-20):** **depth round — the KG canon, the training boundary, scholarly channels, language polish, and a self-model.** A five-part ask, one slice each (M5.10: one cycle, one `added` block).
  - **P15.1 · the knowledge-graph / ontology / knowledge-feature canon.** `review/knowledge-graph-patterns-2026-10.md` — layered stack (data model → schema → vocabulary → constraints → query → provenance → reasoning), with the classic engineering methods (competency questions, METHONTOLOGY/NeOn/OntoClean named but **not re-read**), the four things "knowledge feature" conflates (embeddings *rank* · GNNs *learn structure* · reasoners *decide* · OBDA *maps*), the frontier turn (generative construction, GraphRAG, agentic maintenance) and what it did **not** repeal (identity, evidence). Refs **§N (R155–R170)**; one new instrument row (`hermit`, `elk`) for entailment. **No new clause**: instrument choice is already M3.10, and a `knowledge-feature` clause would restate it with new nouns (recorded, M0.5).
  - **P15.2 · the training stack, and the boundary stated.** `review/training-methodology-coverage-2026-10.md` surveys pretraining/scaling → SFT → RLHF/RLAIF → DPO family → PEFT → distillation → quantization → reasoning RL → agent post-training → evaluation, each graded **in axis / adjacent / out of scope** against a written criterion. Verdict: **the stack is surveyed and the library covers the boundary, not the stack.** The blocker is not effort — the feature vector has no affordance distinguishing "train a model" from "use a model", so a `training-*` capability would be a predicate the engine silently ignores (M5.10). Recorded as a non-addition with a revisit trigger (`model_role: consume|adapt|produce`). Refs **§O (R171–R191)**, abstract-level only.
  - **P15.3 · scholarly discovery & citation channels.** `review/scholarly-channels-2026-10.md` — ~95 channels with observed HTTP statuses, first-party vs aggregator marks, and seven no-laundering rules. Landed **20 outlets** (OpenAIRE · DataCite · ROR · BASE · Connected Papers · ResearchRabbit · OpenReview · PubPeer · SciELO · Redalyc · HAL · CiNii · J-STAGE · CNKI · Wanfang · EThOS · PMLR · SpringerLink · Cambridge Core · PLOS) plus three new `outlet-map.md` sections. **No duplicate ids**: Semantic Scholar / Crossref / CORE / scite / Europe PMC already live in `tools`, OpenAlex in `projects`, and the AI/ML venue indices (NeurIPS, ACL, ICML, ICLR, TMLR) belong to `venues` — they are *surfaced in prose*, not re-registered. Google Scholar's `verified: true` was **re-confirmed** on 2026-10-20 (a real results page; the earlier "blocked" note was stale).
  - **P15.4 · language polish as a gate.** Clause **M4.14** (`core/05`) + capability `prose-polish` + `review/language-polish-2026-10.md`: the failure taxonomy (hedge stacking, stock phrases, list-ification, false balance, summary-of-summary, register mismatch, translationese), the split between what a machine may **reject** (declared house style, term consistency, punctuation per standard) and what only a reader may **approve**, and the Chinese-specific modes (欧化句式/翻译腔, 四字格堆砌, 的的不休, 标点混用, 繁简不等价). A readability score is a **drift alarm**, never a pass mark. Instruments `vale`, `languagetool`, `textstat` (+2 kinds: `prose-linter`, `readability-metric`). Refs **§P (R192–R200)**.
  - **P15.5 · self-model and gap-seeking.** Clause **M5.11** (`core/06`) + capability `gap-seeking` + `review/self-model-and-gap-seeking-2026-10.md`: three artefacts (self-model with evidence per claim · a two-halved gap register · one **disconfirming** check per round), grounded in the asymmetry that unassisted self-correction fails and calibration is poor (R201, R202, R203–R205), and in the finding that "self-improving agents" are **search plus a trusted evaluator** (R212–R214). Exploration is bounded (holdout, budget, stop condition) and novelty is not value (R208–R211, R216, R217). Refs **§Q (R201–R218)**.
  - **Verified.** `harness cycle audit` → **OK · 11 cycles · 22 roadmap items · 35 capabilities · 26 clauses anchored · 0 hard · 0 gaps**; `python -m unittest discover -s tests` → **237 tests** (233 + 4 guards); `catalog --write` + `map --write` regenerated; EOL normalised to LF. **Still open on purpose: P14.4** (scoring 3–5 published harnesses) — this round surveyed the canon instead; closing it needs full-text reads it did not do. 纵深轮：图谱经典 · 训练边界 · 学术渠道 · 语言润色门 · 自我模型。
- **P13 (done, 2026-10-19):** **the capability round as a mechanism.** The ask: every round of capability expansion / deepening / update / evolution needs a *systematic* mechanism, so the capability set can grow perpetually. Recon first (M0.5): `refresh` (entities), `evolve` (mutation proposals) and `capability-flow` (per task) already exist — what was missing was **the round itself**.
  - **Slice 1 · the registry.** `data/cycles.json`: 9 rounds (`baseline` → `P13`) with git-verified `added` ids; the **definition-of-done as data** (7 axes, each flagged hard or soft); **11 roadmap items**, each with `reason` + `revisit_when` + `source`. Counts for scale (`catalog_delta`), ids for verification.
  - **Slice 2 · the audit.** `cycle.py` + CLI `harness cycle [list|show|audit|roadmap|dod]`. `audit` splits **hard problems** — phantom ids, a clause not anchored in its own `core/` doc, a `when` predicate the engine cannot evaluate (`any` / `min_horizon` / feature axis / `domain`), a deferral with no reason or trigger — from the **soft gap surface** (missing router row, guard test, provenance row, unreachable reference doc). The soft list *is* the next round's input; that is the part that makes growth perpetual rather than episodic.
  - **Slice 3 · the contract + procedure.** Clause **M5.10** in `core/06` (a round is recorded, audited, **closed**; a deferral is a decision with a revisit trigger; proposal-first, M0.4); `reference/capability-cycle.md` (inputs → rank → 2–4 slices → seven-axis DoD → record → defer → close, with a worked P13 example and deliberate non-entries); load-index / `SKILL.md` / router / README / GUIDE wiring.
  - **Slice 4 · first use — it found real defects.** The first `audit` reported that **`M2.10`**, **`M2.11`**, **`M3.10`** and **`M8.10`** were cited across review/router docs but *never anchored* in `core/` (and `M2.11` was mislabelled inside `core/09`). All four are now anchored in their own module; `sources/source-map.md` gained rows for M2.10/M2.11, M3.10–M3.13, M5.10 and M8.10. Guard `tests/test_cycle.py` (16 cases; `test_no_hard_problems` makes the mechanism gate itself). **209 tests.** 能力轮次机制化：注册表 · 完成定义 · 缺口面。
- **P14 (done, 2026-10-19):** **knowledge engineering & digital humanities — ontology as a contract, entity identity, evidence-bounded output, schema evolution.** The user's ask: research and integrate the harness capabilities behind 数字人文 and knowledge-base / knowledge-graph / knowledge-ontology development, maintenance, management and evolution. **Case 1** is 关书朋 · 何宇佳 · 张英聘, *智能体驱动的方志人物知识图谱构建与检索增强生成问答研究*, 《文献与数据学报》 **8(3): 56–72**, 2026-09 — reached in **full** through the publisher's open PDF (the printed DOI does **not** resolve; recorded as printed-only). The round was scoped to a **class** of source, not one paper.
  - **The crosswalk found real gaps, not restatements.** `review/knowledge-and-dh-crosswalk-2026-10.md` scores the case's **11 mechanisms** against the existing clauses: **9 covered · 1 partial · 2 gaps**. The gaps were: (i) **output-side evidence bounding** — the library bound *input* (M4.5, untrusted retrieval) but nothing required every named assertion in a *generated* answer to carry a pointer, with "the material is silent" as a valid result; (ii) the **reading** of a verification stage's statistics — the paper reports relation **precision 88.79% → 97.67%** with recall moving only **83.05% → 83.42%**, a filter, not a discovery.
  - **Landed (4 clauses · 4 capabilities · 1 domain · 13 instruments · 6 kinds · 7 outlets · §M).** Clauses **M3.14** (a gate trades precision, not coverage — report recall beside precision), **M4.11** (ontology as a contract: declare types/directions/identity rules *before* extraction; a candidate that cannot be typed is a defect to record), **M4.12** (one canonical identity per entity — aliases recorded, authorities reused, undecidable merges to a human gate), **M4.13** (bound the answer by the evidence). Capabilities `ontology-as-contract` · `entity-resolution` · `evidence-bounded-generation` · `schema-evolution`, each with a router row, a provenance row and a guard test. Domain **`digital-humanities`** (31st; faculty `humanities`, artifact `dataset`, grounding `required`) + its weighted rubric — *encoding* work as distinct from `humanities` *interpretation*. 13 first-party `instruments` under 6 new kinds (`ontology-toolkit`, `graph-database`, `kg-construction`, `entity-resolution`, `gazetteer`, `htr-toolkit`): Protégé/RDFLib/Jena · Neo4j · Microsoft GraphRAG · OpenRefine/Splink/Dedupe · Pleiades/GeoNames/Getty TGN · Transkribus/eScriptorium. 7 outlets (W3C · IIIF · CIDOC-CRM · LOC standards · Getty vocabularies · TEI-C · Wikidata). References **§M (R136–R154)**.
  - **Deliberate non-additions (recorded, M0.5).** No KG-retrieval capability (retrieval is already `context-budget-policy` + instruments) · no `knowledge-engineering` domain (`knowledge-management` owns it; the graph specifics belong in *clauses*) · no `prosopography` domain (a DH workflow step) · **no `encoding-standard` instrument kind** — TEI/CIDOC/Dublin Core/EAD3/IIIF are *norms*, not instruments, so they live as references and as domain gate text (a gazetteer is different in kind and *is* instrumented, like `uniprot`). CBDB and ISAD(G) are **not cited**: both proved unreachable from this environment (403 on repeat), and the repo may not cite what it has not read.
  - **Open:** **P14.4** — score 3–5 published domain harnesses on the three fixed criteria; only Case 1 has been read in full. 领域 harness 案例研究 → 知识工程与数字人文落地：本体即契约 · 实体归一 · 输出侧证据约束 · 模式演化。
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
