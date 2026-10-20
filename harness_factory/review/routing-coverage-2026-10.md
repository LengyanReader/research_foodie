# Can any task find its capabilities? · 任何任务都能定位到能力吗

> A routing-completeness audit: totality, discrimination, correctness — with the nine families that used to land in the wrong place.
> 路由完备性审计：总量、判别、正确性——以及此前会落错地方的九个任务族。
**Updated:** 2026-10-20

> **中文速览**
> **问法**：把「任何 task 都能定位到适合的能力」拆成三个可检验的命题——**① 总量**（是否有任务掉空：无向量、无计划、只余底线）·**② 判别**（不同任务是否真的得到不同的能力集，还是某几个轴值根本不承重）·**③ 正确**（分类对不对）。
> **结果**：① **成立**：32 个任务族全部产出向量与计划，最少 9 条能力，没有一例只剩 3 条底线；37 条能力全部可满足、全部在 router 里点名。② **大体成立**：13 个轴值相对安静基线不增加能力，其中 8 个是「比基线更少」的语义（one_shot / off / none / solo / medium / low），3 个是真洞（`artifact=plan`、`artifact=mixed`、`domain=arts-design`）。③ **原先不成立，已修**：32 个任务族里 **9 个落错域**，根因三类——**子串误命中**（`ci` 命中 "exer**ci**ses" 把课程设计判成 devops；`art` 命中 "p**art**ial"；`eval` 命中 "retri**eval**" 让所有 RAG 任务变成「高可验证」）、**常用任务族缺信号**（python package / incident / course / pcb / brand / 视频 / 音乐…）、**两个轴从不读文本**（`artifact`、`grounding` 只取领域默认）。修完后 **32/32**。
> **没修的**：无媒体域（视频/音乐归 arts-design）；`plan` 产物无专属能力；arts-design 的 `grounding=off` 让它拿到全池最少的能力；关键词路由只覆盖中英双语（其他语言请显式 `--domain`/flags）。每条都写了重访触发。

---

## 0. The claim under test

`harness_factory` promises that a task, compiled through the feature vector, lands on capabilities that
say what must be done. "Any task" is a strong claim, so it is tested in three parts, because a system can
satisfy one and fail the next:

1. **Totality** — every task produces a vector, a plan, and something more than a vacuous answer.
2. **Discrimination** — different tasks produce *different* capability sets; an axis value that never
   changes the answer is decoration.
3. **Correctness** — the classification is right for tasks people actually type, not only for the
   vocabulary in the docs.

A routing layer can be total and useless (everything gets the floor), or discriminating and wrong (a course
design lands in devops). Both were live risks here; the third test found real defects.

## 1. Method

- **Battery:** 32 task families, 16 Chinese and 16 English, written as a user would type them, spanning
  code, docs, knowledge graphs, writing, translation, decks, data, ops, law, medicine, teaching, design,
  video, music, agents, long-running systems, research, datasets, hardware, trials, courses, audits, plus
  two deliberately empty prompts ("do the thing", "help me with this"). Each family has an **allowed set**
  of domains; anything outside it is a miss.
- **Axis sweep:** the quiet baseline vector (`one_shot / medium / low / off / code / read / solo / general`)
  and then every value of every axis flipped in isolation, recording whether the active capability set
  changes.
- **Constructive satisfiability:** for each capability, build a vector from its `when` clause and assert it
  fires — a capability nothing can trigger is invisible, and a typo in a domain name fails open.
- **Router parse:** the capability table in `reference/capability-router.md` is parsed and compared with
  the catalogue in both directions.

## 2. Totality — holds

| Check | Result |
|---|---|
| Tasks that produced a plan | 32 / 32 |
| Tasks that fired only the 3 always-on capabilities | 0 |
| Minimum / median capabilities per task | 9 / 13 |
| Capabilities with a satisfying vector | 37 / 37 |
| Capabilities named in the agent router doc | 37 / 37 |
| Condition values that name a declared axis/domain | 100% (0 invalid) |

The floor is 3 capabilities (`baseline-discipline`, `verification-gate`, `bidirectional-capability-flow`)
plus M0/M1/M3/M7 — by design (M0.4). Nothing can fall through to "no harness", and reaching only the floor
means the task is under-specified, not that the library is empty.

## 3. Discrimination — mostly holds, two real holes

Flipping each axis value against the quiet baseline (which already fires 6 capabilities):

| Axis value | Delta | Reading |
|---|---|---|
| `one_shot`, `grounding=off`, `tool_surface=none`, `collaboration=solo` | 0 | **by design:** these values *remove* capabilities rather than add; the baseline already reflects them |
| `verifiability=medium` · `low`, `stakes=low` · `medium` | 0 | **by design (parameter-only):** low/medium change `gate_strictness` and `autonomy`, not the requirement set; the soft-gate requirement lives inside the always-on `verification-gate` |
| `artifact=code` | 0 alone | **combination-only:** it loads `formal-verification` only together with `verifiability=high` |
| `artifact=mixed` | 0 | **absence of a deliverable**, not a deliverable — correctly no requirement |
| **`artifact=plan`** | 0 | **hole:** a plan/proposal has no capability of its own (scope, milestones and acceptance live in `verification-gate` + `ambition-elevation`, but nothing names the artifact) |
| **`domain=arts-design`** | 0 | **hole:** no capability keys on it, *and* its `grounding=off` removes `traceable-sources`, so a design task gets the fewest capabilities in the whole battery (9) |

Neither hole is a bug to patch blindly: a capability that fires on every plan would be annotation, and
"creative work needs no sources" is a defensible default (though image rights make it arguable). Both are
recorded with revisit triggers in §6.

## 4. Correctness — this is where it failed

Nine of the 32 families used to land outside their allowed set. Three distinct root causes, each with a
reproducible example:

| # | Before | Why |
|---|---|---|
| 1 | "build an online course with exercises" → **devops** | the devops signal `ci` matched inside "exer**ci**ses" |
| 2 | "summarise the partial results in this article" → **arts-design** | the signal `art` matched inside "p**art**ial" and "**art**icle" |
| 3 | "survey the literature on retrieval augmented generation" → verifiability **high** | the verifiability keyword `eval` matched inside "retri**eval**" — every RAG task looked machine-checkable |
| 4 | "add type hints and tests to a legacy python package" → **general** | no signals for `python`, `package`, `type hints` |
| 5 | "排查线上服务的内存泄漏并修复" → **general** | no signals for `线上`/`内存泄漏` |
| 6 | "debug a production incident and write the postmortem" → software-engineering | `incident`/`postmortem` absent; `debug` is not a signal |
| 7 | "设计一门本科生的数据素养课程大纲" → **data-science** | `数据` outweighed `课程`/`大纲`; education had no `course`/`syllabus` |
| 8 | "design a pcb for a low-power sensor" → **arts-design** | `design` won because engineering had no `pcb`/`sensor` |
| 9 | "做一个品牌视觉方案，包含 logo 和配色" · "科普视频" · "背景音乐" → **general** | no vocabulary for brand, video, music |

Two of the eight axes were **never read from the text at all**: `artifact` and `grounding` came only from
the domain's defaults. So "write a report from these interviews" stayed `artifact=mixed` and "注明来源"
could not raise `grounding` — the two axes that decide whether M4 and the pointer capabilities fire were
inherited, never evidenced.

**Fixes** (all in `classify.py` + `domains.json`, no new capability):

- Signals now match at a **word start**, not anywhere: `deploy` still matches "deployment", but `ci` no
  longer matches "exercises" and `art` no longer matches "partial". The same matcher now backs the
  verifiability/stakes/horizon keyword lists, which is what removed the "retrieval = eval" false positive.
- 84 high-precision signals added across software-engineering, devops, arts-design, writing, education and
  engineering; three broad or mis-keyed signals removed (`art`; `evolution`/`governance`/`演化` from devops —
  those are library concepts, not deployment work).
- **Artifact and grounding cues:** an explicit deliverable noun (`report`/`dataset`/`knowledge graph`/
  `codebase`/`proposal`/`报告`/`幻灯片`…) sets `artifact`; an explicit demand for sources (`cite`,
  `references`, `provenance`, `注明来源`, `可溯源`) raises `grounding` to `required`. Only an explicit
  "no external knowledge" lowers it. Silence never lowers a level: a false `off` is worse than a false
  `preferred`.
- The classifier's rules are now written down where an agent can read them:
  `reference/derivation-rules.md` §"How the classifier fills the vector".

After: **32/32** families land in an allowed domain, and the capability counts move in the right direction —
the report/writing families gained M4 and the pointer capabilities (10 → 14), the design/music families
stayed at 9 because their domain has no provenance requirement, and the RAG survey **lost** three
capabilities (18 → 15) because it was never high-verifiability in the first place.

## 5. Guards added (so the audit does not need repeating)

| Guard | What it prevents |
|---|---|
| `CatalogReachabilityTest.test_condition_values_are_declared` | a typo in a `when` value or domain name that silently kills a capability |
| `CatalogReachabilityTest.test_every_capability_fires_on_some_vector` | a capability no vector can trigger |
| `CatalogReachabilityTest.test_every_capability_is_reachable_from_the_router_doc` | one direction of the router table going stale (the other direction already had a test) |
| `DomainsClassifyTest.test_task_families_reach_a_domain` | the nine families regressing when signal lists are edited |
| `DomainsClassifyTest.test_short_signals_do_not_fire_inside_longer_words` | the `ci`/`art` class of false positive coming back |
| `ClassifyTest.test_explicit_artifact_cue_beats_the_domain_default` | the two dead axes reverting to domain-default-only |

One latent inconsistency was fixed while auditing: `_cond_matches` returned early when a `when` clause had
`any`, silently ignoring the clause's other keys even though the rendered trigger text read them as an AND.
No shipped capability used that combination, so behaviour is unchanged today — but the DSL now matches what
it prints.

## 6. What is still not covered (with triggers)

- **No media domain.** Video, film, music and storyboard tasks land in `arts-design` (`mixed`/`off`, 9
  capabilities). *Trigger:* a second media task whose capability set differs from a design task's — then a
  `media-production` domain (artifact `document`, grounding `preferred`) is doing independent work.
- **`artifact=plan` has no capability.** *Trigger:* a plan whose failure mode is not already covered by
  `verification-gate` — e.g. a plan that omits its own acceptance criteria.
- **`arts-design` grounding=off** costs creative work the provenance floor, though image rights and
  attribution are real. *Trigger:* a design deliverable that ships third-party assets.
- **Language boundary.** Signals are English and Chinese. A French or Japanese task still routes (it lands
  on `general` + whatever the text cues give), but quality is calibrated for EN/ZH; the supported path for
  other languages is an explicit `--domain` / flags, or the opt-in LLM classifier.
- **Ambiguous genres stay ambiguous.** "Turn my notes into a non-fiction book chapter" → `reading`
  (book/chapter) rather than `writing`; both are allowed, and both produce `document` + `required`.

## 7. Verdict

**Yes for any task, with a stated boundary.** Every task gets a vector, a plan and at least the three
invariants; 37/37 capabilities are satisfiable and reachable; 32/32 task families land on a defensible
domain; the two axes that decide provenance now read the text instead of inheriting a default. The boundary
is inferential, not structural: outside English and Chinese the *quality* of the guess drops, and three
axis values still carry no requirement of their own — each recorded above rather than papered over.
