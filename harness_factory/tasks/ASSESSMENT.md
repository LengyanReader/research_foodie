# Assessment & external-harness integration review — `harness_factory`

> **中文速览。** 本文两部分。**A｜完整性与可用性评估**（按 2026-10-15 实测）：模式库与编译器主干已成型，
> 整体 **完成度≈85%、可用性≈90%**；主要缺口是「自演化仅规则/提案、无轨迹驱动」「记忆只有规范、无可发射后端」
> 「联网与 LLM 路径未进 CI」。（原「产出物未对齐外部 skill 标准」「无沙箱/最小权限执行」两项已于 2026-10-15
> 通过 P1/P3 关闭。）**B｜外部 harness 整合评估**：结论是**可以整合，且以「格式对齐」为主、代码改动很小**。
> 最高杠杆是 **Agent Skills（`SKILL.md`）开放标准**（原 Anthropic 提出、现由 agentskills.io 维护，Hermes Agent
> 等数十个 harness 已实现）——本仓库已用 `SKILL.md` 作 agent 入口并发射 `.harness/skills/`，对齐该标准即可让
> 产出的 harness 跨 harness 通用。所有整合均按 **M0.4 提案 → 人工确认 → 落 SSOT**；P1/P2/P3 与能力总览
> `CAPABILITIES.md` 已按用户指示落地（见 **B.6**）。
>
> **2026-10-19 收尾判断：本阶段可以收束。** 三项长期诉求（各领域**仪器 / 方法论** · **跨语言意群保真** · 各领域**信息源地图**）均已落入 SSOT 并有测试守护（见 **A.5**）；剩余缺口（自演化缺证据机制、M2 记忆仅规范、联网/LLM 路径未进 CI、手工计数漂移）**均为既有项、非回归**，转入下一阶段 **P12**（`tasks/PLAN.md`）。

**Updated:** 2026-10-15 · **Scope:** `harness_factory/` · **Method:** measured against the repo's own SSOT
(`data/*.json`) + first-party sources cited inline (all accessed **2026-10-15**). Scores are *self-assessed
estimates*, not benchmarks.

---

## Part A · Completeness & usability assessment

### A.1 Measured surface (as of 2026-10-15)

> **Later cycles moved these numbers.** As of **2026-10-18** (P10): **29 capabilities** · **30 domains (29 disciplines + `general`) across 10 faculties** · **31 rubrics** · **183 catalog entries** · **23 CLI subcommands** · **184 tests**. The table below is the 2026-10-15 measurement and is kept as the snapshot it is.

| Facet | Value | Source of truth |
|---|---|---|
| Tool source | 27 `.py`, 5,574 lines | `src/harness_factory/` |
| Core modules | 9 (M0–M8) | `data/modules.json` |
| Capabilities | 13 | `data/capabilities.json` |
| Domains | 25 (24 disciplines + `general`) across 9 faculties | `data/domains.json` |
| Rubrics | 26 (25 domains + `default`) | `data/rubrics.json` |
| Harness catalog | 133 entries (11 classes × 33 kinds) | `data/harnesses.json` |
| Levers | 75 by-dim + 3 domain bars + default | `data/levers.json` |
| Watchlist | 8 topics + 4 frontier probes | `data/watchlist.json` |
| Tracked sources | 7 groups · 12 topic ids | `data/sources.json` |
| CLI | 22 top-level subcommands | `python -m harness_factory --help` |
| Docs | 56 `.md` (excl. `_archive/`, `updates/`); 24 domain READMEs; 10 worked examples | `harness_factory/**` |
| Tests / CI | 132 stdlib unittest cases; matrix ubuntu+windows × py3.10/3.12 + CLI smoke + e2e smoke | `tests/`, `.github/workflows/ci.yml` |

### A.2 Scorecard (self-assessed)

| Axis | Est. completeness | Basis / weakest link |
|---|---|---|
| Pattern library (`core/`, `domains/`, `review/`, `sources/`) | ~95% | 9 invariants + 24 disciplines + provenance map; gaps are per-domain depth, not structure |
| Compiler (`derive`/`init`/`check`/`gate`) | ~90% | explainable derivation + emitted `check.py` executed by `gate`; no versioning of emitted manifests |
| Self-update & evolution (`refresh`/`intel`/`evolve`) | ~80% | **proposal-only**, rules-based; no trace-driven mechanism; `updates/` deliberately untracked |
| Agent-native L0 path | ~90% | `SKILL.md` + load-index + two-step directive; not yet conformant to an external skill spec |
| Tests & CI | ~85% | 132 cases, cross-OS; network paths (`refresh`/`intel`) and the optional LLM path untested |
| Docs coherence | ~90% | single source after the README merge; residual drift risk in hand-copied counts |
| Packaging / distribution | N/A | **intentionally cancelled** (`tasks/DISTRIBUTION.md` §8) |

**Overall: ≈85% complete, ≈90% usable.** The library and compiler are production-shaped; the learning loop is
honest but thin; the biggest *missing* capability is interoperability with the wider harness ecosystem.

### A.3 Gaps & risks (ranked)

1. ~~**No external skill-format conformance.**~~ **Closed (P1, 2026-10-15):** emitted skills now follow the
   Agent Skills (`SKILL.md`) spec and are portable to other agents. (See Part B.)
2. **Self-evolution has no evidence mechanism.** M5 is rules/proposals; nothing consumes execution traces to
   propose prompt/skill changes.
3. ~~**No sandboxing / least-privilege story.**~~ **Partly closed (P3, 2026-10-15):** the `sandboxed-execution`
   capability now fires for external/high-stakes work → a declared execution posture (M3/M6/M7). A concrete
   backend profile is still not emitted.
4. **M2 memory is spec-only.** `core/03` describes external memory; no memory *backend profile* is emitted.
5. **Network + LLM paths untested in CI** (offline by design); correctness rests on `--dry-run` and manual runs.
6. **Hand-maintained counts drift** (127 / 24 / 25 …), mitigated by `harness catalog --write` but not eliminated.
7. **No "run the emitted harness to completion" CI** beyond the new smoke (`init → check → gate → harvest`).

### A.4 What "done" would look like

- Emitted skills conform to a published spec (portable).
- A trace/telemetry input that yields *proposal-only* prompt/skill mutations.
- A declared execution posture (backend + isolation) in the emitted manifest.
- CI covering the offline surface end-to-end, plus a gated, opt-in network job.

### A.5 Stage wrap-up — can this stage close? (as of 2026-10-19)

**Verdict: yes.** The stage that opened with the standing asks *"integrate each field's instruments and
methodology systems"*, *"carry meaning across languages at the level of whole meaning units"* and *"map
each field's high-quality information outlets"* is delivered end to end: every ask is in the SSOT
(clauses **M3.10–M3.13** · **M4.10**), each backed by first-party sources (`[R107]`–`[R126]`), each with
its own procedure doc **and** a guard that fails if it drifts. The gaps that remain are the *pre-existing*
ones (A.3 items 2/4/5/6/7) — none is a regression from this stage, and none blocks using the factory today.

| Facet | 2026-10-15 | **2026-10-19** | Source of truth |
|---|---|---|---|
| Tool source | 27 `.py`, 5,574 lines | **29 `.py`, 6,448 lines** | `src/harness_factory/` |
| Capabilities | 13 | **29** | `data/capabilities.json` |
| Domains / faculties | 25 / 9 | **30 / 10** | `data/domains.json` |
| Rubrics | 26 | **31** | `data/rubrics.json` |
| Harness catalog | 133 (11 × 33) | **183 (12 classes × 50 kinds)** | `data/harnesses.json` |
| Evidence instruments | — | **new `instruments` class (27 + 23 rows)** | `data/harnesses.json` |
| Field outlets | — | **68** (8th `sources` group) | `data/sources.json` |
| Watchlist / source topics | 8 / 12 | **9 / 30** | `data/watchlist.json`, `data/sources.json` |
| CLI | 22 | **23** | `python -m harness_factory --help` |
| Docs | 56 `.md` | **74 `.md`** (29 domain READMEs) | `harness_factory/**` |
| Tests / CI | 132 | **193** | `tests/`, `.github/workflows/ci.yml` |
| References | — | **`[R1]`–`[R126]`** (groups A–K) | `review/references.md` |

**Closed by this stage:** claim → instrument mapping (P9, **M3.10**); mathematics / statistics /
computer-algebra instruments plus methodology systems (P10, **M3.11–M3.13**); cross-language
meaning-unit fidelity (P11, **M4.10**); per-field information outlets (P11); and the pointer/usage chain
that reaches all of it from *one instruction* (P6 · P11.1 · P11.2).

**Still open — unchanged and ranked; this is the next stage's business:**

1. **No evidence-driven self-evolution** (A.3 #2) — M5 is rules/proposals; nothing consumes execution traces.
2. **M2 memory is spec-only** (A.3 #4) — a *declared memory backend* is not yet emitted, although the
   precedent exists (the evidence instrument is emitted by `assemble._evidence_instrument()` since P9).
3. **Network + LLM paths untested in CI** (A.3 #5) and **no full emitted-harness run in CI** (A.3 #7).
4. **Hand-maintained counts drift** (A.3 #6) — mitigated by `harness catalog --write`, not eliminated.
5. **P11 loose ends** — the 22 outlets the automated check could not reach (403/405) are recorded
   `listed, not confirmed`; `reference/cross-language.md` still lacks a worked example.

Items 1–4 are the *next* increments, not defects in what shipped. Planned as **P12** in `tasks/PLAN.md`.

---

## Part B · External-harness integration review (Hermes Agent & peers)

### B.0 Answer up front

**Yes — and the integration is mostly *format*, not code.** Hermes Agent and the ecosystem around it expose
capabilities that map onto modules this repo already has (M2 memory, M5 self-evolution, M6 tools/skills,
M8 collaboration). The single highest-leverage item is adopting the **Agent Skills (`SKILL.md`) open standard**:
this repo already ships a `SKILL.md` entry point and emits a skills index, so conformance is a small change that
makes every emitted harness portable across the harnesses that implement the standard.

### B.1 Hermes Agent — verified capabilities → `harness_factory` mapping

Hermes Agent is "the self-improving AI agent built by Nous Research" — open source, **MIT**, first-party docs at
`hermes-agent.nousresearch.com/docs` and source at `github.com/NousResearch/hermes-agent` (both accessed
2026-10-15).

| Hermes capability (verified) | Maps to | Integration shape |
|---|---|---|
| Closed learning loop: agent-curated memory + periodic nudges | **M2** (`core/03-long-running-agents.md`) | Cite as **Exemplar**; add a bounded-memory profile |
| Autonomous skill creation after complex tasks; skills self-improve during use | **M5** (`core/06-self-evolution.md`) | Add a *trace-driven skill evolution* mechanism as an optional lever |
| FTS5 session search + LLM summarization for cross-session recall | **M2** | Memory-backend profile (recall design) |
| Honcho dialectic user modeling | **M2** | Notes; external dependency |
| `agentskills.io`-compatible, **portable `SKILL.md`** | **M6** (`core/07-tools-and-skills.md`) | **Adopt the spec** (P1) |
| Built-in cron scheduler, delivery to any platform | **M2/M5 cadence** | Scheduling note (see `benschrauwen/hermit` heartbeat) |
| Subagents / parallel workstreams; `execute_code` RPC | **M8** (`core/09-collaboration-and-sessions.md`) | Multi-agent delegation pattern |
| 7 terminal backends (local/Docker/SSH/Daytona/Singularity/Modal/Vercel) + container hardening | **new capability** | `sandboxed-execution` (P3) |
| Command approval, DM pairing, container isolation | **M0.8 / M8** | Human-gate pattern (consistent with M0.4) |
| 60+ tools, MCP support | **M6** | Already conceptually covered |
| Batch trajectory generation, RL (Atropos), ShareGPT export | **M5 evidence** | Self-evolution input (P4) |

### B.2 The Agent Skills (`SKILL.md`) open standard — the key finding

From `agentskills.io` (accessed 2026-10-15):

- A skill is **a folder containing `SKILL.md`** with metadata (`name`, `description` minimum) plus instructions;
  it may bundle `scripts/`, `references/`, `assets/`.
- It loads by **progressive disclosure** in three stages: **Discovery** (name+description only) →
  **Activation** (full `SKILL.md`) → **Execution**.
- Originally developed by **Anthropic** and released as an **open standard**; adopted across a large client set
  (per its client showcase: Claude Code, Cursor, Gemini CLI, **OpenCode**, **OpenHands**, **Goose**, **Letta**,
  **pi**, **Hermes Agent**, **OpenClaw**, VS Code/Copilot, Codex, …).

**Why it matters here:** this repo already uses `SKILL.md` as its agent entry (`harness_factory/SKILL.md`) and emits
`.harness/skills/README.md` as a "progressive skill index" (M6). It is *one format-alignment away* from emitting
artifacts the whole ecosystem can consume — and from being consumable itself.

### B.3 Peer landscape

**Verified from first-party sources (accessed 2026-10-15):**

- **Hermes Agent** — Nous Research; self-improving agent, closed learning loop, MIT.
  `github.com/NousResearch/hermes-agent` · `hermes-agent.nousresearch.com/docs`
- **Agent Skills standard** — `agentskills.io` (+ `github.com/agentskills/agentskills`)
- **`benschrauwen/hermit`** — "local, file-first runtime for autonomous applications that improve themselves":
  heartbeat daemon, local telemetry, strategic review, git-native checkpoints, `nono` sandbox, `pi-mono` skill
  loading — a close sibling of this repo's self-evolution thesis. `github.com/benschrauwen/hermit`
- **`cashapp/hermit`** — hermetic, self-bootstrapping per-project toolchains; ships an AI-agent skill for
  Hermit-managed repos (the reproducibility angle). `github.com/cashapp/hermit`

**Already tracked in `data/sources.json` (harnesses group):** OpenAI Agents SDK, OpenAI Codex CLI, Claude Code,
Claude Agent SDK, MCP, Google ADK, Gemini CLI, A2A, Llama Stack, Mistral Agents, SWE-agent, …

**Now tracked in `data/sources.json` (2026-10-15, repo URLs verified by search):** Hermes Agent,
Agent Skills standard, OpenClaw, Goose, OpenHands, Letta, pi (`pi-mono`), `benschrauwen/hermit`, `cashapp/hermit`.
Catalog entries added for the first six (+`letta-code`, `pi-mono`, `hermit-file-first`).

**Peer tools listed in clients but *not* added** (secondary/ambiguous URLs, left untracked to avoid drift):
ZeroClaw, nanobot, fast-agent, Emdash, Mux, Kiro, Qodo, Junie, Factory, Amp, Cursor.

### B.4 Integration proposals (ranked; all proposal-only per M0.4)

| # | Proposal | Where | Effort | Value |
|---|---|---|---|---|
| **P1** | **Emit skills in the Agent Skills format**: `skills/<name>/SKILL.md` with `name`/`description` frontmatter + progressive disclosure; make `harness_factory/SKILL.md` spec-conformant | `src/harness_factory/templates/skills_README.md.tmpl`, `assemble.py`, `runtime.py` (M6 gate), docs | M | **High** — portability across the ecosystem |
| **P2** | **Track Hermes Agent + peers in the SSOT**: add `hermes-agent`, `agentskills-io`, `openclaw`, `goose`, `openhands`, `letta` to `data/sources.json`; add catalog entries to `data/harnesses.json`; then `harness catalog --write` | `data/sources.json`, `data/harnesses.json`, `review/harness-index.md` (generated) | S | High — surfaces them to the self-update loop |
| **P3** | **New capability `sandboxed-execution`** (requirement → capability → modules) + a lever | `data/capabilities.json`, `data/levers.json`, `reference/derivation-rules.md` | S–M | Medium — closes the isolation gap |
| **P4** | **Enrich M3/M6 with verified mechanisms** as Exemplars (bounded curated memory + recall; trace-driven skill evolution) | `core/03-long-running-agents.md`, `core/06-self-evolution.md`, `sources/source-map.md` | S | Medium |
| **P5** | **Emit a minimal memory-backend profile** in templates | `templates/`, `assemble.py` | L | Medium — only if a domain demands it |

**Recommendation:** do **P1 + P2** together — they are small, reversible, and turn the repo from an island into a
node in the standard ecosystem. Hold **P3–P5** until a target task needs them.

### B.6 Implementation status (2026-10-15)

Per user direction, **P1 + P2 + P3 were implemented** together with the Hermes/peer integration:

| Item | Status | Change |
|---|---|---|
| **P1** portable skills | ✅ Done | Emitted `.harness/skills/<name>/SKILL.md` (Agent Skills spec: `name`+`description` frontmatter, dir name = `name`, progressive disclosure) via new `templates/skills_SKILL.md.tmpl`; `assemble.py` emits it when M6; `runtime.py` M6 gate checks `skills/*/SKILL.md`; the factory's own `SKILL.md` gained `license`+`compatibility` frontmatter |
| **P2** track Hermes + peers | ✅ Done | +9 entities in `data/sources.json`; +6 catalog entries in `data/harnesses.json` (+`goose`/`openhands` upgraded with `tracked`/skills tags); `review/harness-index.md` regenerated (127→**133** entries) |
| **P3** `sandboxed-execution` | ✅ Done | New capability (fires on `tool_surface=external` OR `stakes=high` → M3,M6,M7); `security` lever enriched; mirrored in `reference/derivation-rules.md` |
| Integration (extra) | ✅ Done | New capability **`portable-skills`** (M6); prose ecosystem section **§5a** + refs [30]–[37] in `review/harness-catalog.md` |
| **New overview doc** | ✅ Done | `CAPABILITIES.md` — generated (purpose + how-it-works + modules + every capability); auto-evolves via `harness capabilities --write` (also refreshed by `harness catalog --write`), drift-guarded by a test |
| P4 / P5 | ⏸ Held | Exemplar enrichment + memory-backend profile — await a concrete task |

**Effect on scores:** A.1 counts move to 13 capabilities / 133 catalog entries / 132 tests; A.3 gap **#1
(external skill-format conformance)** and **#3 (sandboxing)** are now closed.

### B.5 Verification status

| Claim | Status | Source (accessed 2026-10-15) |
|---|---|---|
| Hermes Agent capabilities & design | **Verified** | `hermes-agent.org`, `github.com/NousResearch/hermes-agent`, `hermes-agent.nousresearch.com/docs` |
| Agent Skills format, progressive disclosure, open-standard lineage | **Verified** | `agentskills.io` |
| `benschrauwen/hermit` / `cashapp/hermit` descriptions | **Verified** | their GitHub READMEs |
| Skill self-evolution via DSPy + GEPA in Hermes | *Unverified* (community post) | Reddit r/hermesagent |
| Peer tools listed in B.3 "not yet tracked" | *Unverified* (secondary) | `agentskills.io` client showcase only |

---

## 中文要点（决策摘要）

- **A｜完成度≈85%、可用性≈90%**：模式库与编译器主干成型；缺口为 ①自演化只有规则/提案、缺轨迹驱动
  ②记忆仅规范、无可发射后端 ③联网与 LLM 路径未进 CI。（①产出物未对齐外部 skill 标准 ②无沙箱/最小权限已关闭。）
- **B｜Hermes 等可以整合，且以「格式对齐」为主、改动小。** 最高杠杆是 **Agent Skills（`SKILL.md`）开放标准**
  （Anthropic 提出、agentskills.io 维护；Hermes / OpenCode / OpenHands / Goose / Letta / pi 等已实现）——
  本仓库已用 `SKILL.md`、已发射技能索引，**P1** 按规范对齐即可让产物跨 harness 通用；**P2** 把 Hermes Agent
  等纳入 `data/sources.json` 追踪；**P3** 新增 `sandboxed-execution` 能力。
- **落地状态（2026-10-15）：P1 + P2 + P3 已实现**，并新增 `portable-skills` 能力、
  `review/harness-catalog.md` §5a 生态小节，以及**自动演化的能力总览 `CAPABILITIES.md`**；P4/P5 暂缓。
