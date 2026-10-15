# Assessment & external-harness integration review — `harness_factory`

> **中文速览。** 本文两部分。**A｜完整性与可用性评估**（按 2026-10-15 实测）：模式库与编译器主干已成型，
> 整体 **完成度≈85%、可用性≈90%**；主要缺口是「产出物未对齐外部 skill 标准」「自演化仅规则/提案、无轨迹驱动」
> 「无沙箱/最小权限执行」「M3 记忆只有规范、无可发射后端」「联网与 LLM 路径未进 CI」。
> **B｜外部 harness 整合评估**：结论是**可以整合，且以「格式对齐」为主、代码改动很小**。最高杠杆是
> **Agent Skills（`SKILL.md`）开放标准**（原 Anthropic 提出、现由 agentskills.io 维护，Hermes Agent 等数十个
> harness 已实现）——本仓库已用 `SKILL.md` 作 agent 入口并发射 `.harness/skills/`，对齐该标准即可让产出的
> harness 跨 harness 通用。其次是把 **Hermes Agent** 等纳入 `data/sources.json` 追踪、并新增能力项
> `sandboxed-execution`。所有整合均为**提案**（M0.4），须人工确认后再落 SSOT。

**Updated:** 2026-10-15 · **Scope:** `harness_factory/` · **Method:** measured against the repo's own SSOT
(`data/*.json`) + first-party sources cited inline (all accessed **2026-10-15**). Scores are *self-assessed
estimates*, not benchmarks.

---

## Part A · Completeness & usability assessment

### A.1 Measured surface (as of 2026-10-15)

| Facet | Value | Source of truth |
|---|---|---|
| Tool source | 27 `.py`, 5,574 lines | `src/harness_factory/` |
| Core modules | 9 (M0–M8) | `data/modules.json` |
| Capabilities | 11 | `data/capabilities.json` |
| Domains | 25 (24 disciplines + `general`) across 9 faculties | `data/domains.json` |
| Rubrics | 26 (25 domains + `default`) | `data/rubrics.json` |
| Harness catalog | 127 entries (11 classes × 33 kinds) | `data/harnesses.json` |
| Levers | 75 by-dim + 3 domain bars + default | `data/levers.json` |
| Watchlist | 8 topics + 4 frontier probes | `data/watchlist.json` |
| Tracked sources | 7 groups · 12 topic ids | `data/sources.json` |
| CLI | 22 top-level subcommands | `python -m harness_factory --help` |
| Docs | 54 `.md` (excl. `_archive/`, `updates/`); 24 domain READMEs; 10 worked examples | `harness_factory/**` |
| Tests / CI | 128 stdlib unittest cases; matrix ubuntu+windows × py3.10/3.12 + CLI smoke + e2e smoke | `tests/`, `.github/workflows/ci.yml` |

### A.2 Scorecard (self-assessed)

| Axis | Est. completeness | Basis / weakest link |
|---|---|---|
| Pattern library (`core/`, `domains/`, `review/`, `sources/`) | ~95% | 9 invariants + 24 disciplines + provenance map; gaps are per-domain depth, not structure |
| Compiler (`derive`/`init`/`check`/`gate`) | ~90% | explainable derivation + emitted `check.py` executed by `gate`; no versioning of emitted manifests |
| Self-update & evolution (`refresh`/`intel`/`evolve`) | ~80% | **proposal-only**, rules-based; no trace-driven mechanism; `updates/` deliberately untracked |
| Agent-native L0 path | ~90% | `SKILL.md` + load-index + two-step directive; not yet conformant to an external skill spec |
| Tests & CI | ~85% | 128 cases, cross-OS; network paths (`refresh`/`intel`) and the optional LLM path untested |
| Docs coherence | ~90% | single source after the README merge; residual drift risk in hand-copied counts |
| Packaging / distribution | N/A | **intentionally cancelled** (`tasks/DISTRIBUTION.md` §8) |

**Overall: ≈85% complete, ≈90% usable.** The library and compiler are production-shaped; the learning loop is
honest but thin; the biggest *missing* capability is interoperability with the wider harness ecosystem.

### A.3 Gaps & risks (ranked)

1. **No external skill-format conformance.** Emitted skills are bespoke (`.harness/skills/README.md`) and are not
   portable to other agents. (See Part B.)
2. **Self-evolution has no evidence mechanism.** M6 is rules/proposals; nothing consumes execution traces to
   propose prompt/skill changes.
3. **No sandboxing / least-privilege story.** Emitted harnesses don't declare an execution backend or isolation posture.
4. **M3 memory is spec-only.** `core/03` describes external memory; no memory *backend profile* is emitted.
5. **Network + LLM paths untested in CI** (offline by design); correctness rests on `--dry-run` and manual runs.
6. **Hand-maintained counts drift** (127 / 24 / 25 …), mitigated by `harness catalog --write` but not eliminated.
7. **No "run the emitted harness to completion" CI** beyond the new smoke (`init → check → gate → harvest`).

### A.4 What "done" would look like

- Emitted skills conform to a published spec (portable).
- A trace/telemetry input that yields *proposal-only* prompt/skill mutations.
- A declared execution posture (backend + isolation) in the emitted manifest.
- CI covering the offline surface end-to-end, plus a gated, opt-in network job.

---

## Part B · External-harness integration review (Hermes Agent & peers)

### B.0 Answer up front

**Yes — and the integration is mostly *format*, not code.** Hermes Agent and the ecosystem around it expose
capabilities that map onto modules this repo already has (M3 memory, M6 self-evolution, M7 tools/skills,
M9 collaboration). The single highest-leverage item is adopting the **Agent Skills (`SKILL.md`) open standard**:
this repo already ships a `SKILL.md` entry point and emits a skills index, so conformance is a small change that
makes every emitted harness portable across the harnesses that implement the standard.

### B.1 Hermes Agent — verified capabilities → `harness_factory` mapping

Hermes Agent is "the self-improving AI agent built by Nous Research" — open source, **MIT**, first-party docs at
`hermes-agent.nousresearch.com/docs` and source at `github.com/NousResearch/hermes-agent` (both accessed
2026-10-15).

| Hermes capability (verified) | Maps to | Integration shape |
|---|---|---|
| Closed learning loop: agent-curated memory + periodic nudges | **M3** (`03-long-running-agents.md`) | Cite as **Exemplar**; add a bounded-memory profile |
| Autonomous skill creation after complex tasks; skills self-improve during use | **M6** (`06-self-evolution.md`) | Add a *trace-driven skill evolution* mechanism as an optional lever |
| FTS5 session search + LLM summarization for cross-session recall | **M3** | Memory-backend profile (recall design) |
| Honcho dialectic user modeling | **M3** | Notes; external dependency |
| `agentskills.io`-compatible, **portable `SKILL.md`** | **M7** (`07-tools-and-skills.md`) | **Adopt the spec** (P1) |
| Built-in cron scheduler, delivery to any platform | **M5/M3 cadence** | Scheduling note (see `benschrauwen/hermit` heartbeat) |
| Subagents / parallel workstreams; `execute_code` RPC | **M9** (`09-collaboration-and-sessions.md`) | Multi-agent delegation pattern |
| 7 terminal backends (local/Docker/SSH/Daytona/Singularity/Modal/Vercel) + container hardening | **new capability** | `sandboxed-execution` (P3) |
| Command approval, DM pairing, container isolation | **M0.2 / M4** | Human-gate pattern (consistent with M0.4) |
| 60+ tools, MCP support | **M7** | Already conceptually covered |
| Batch trajectory generation, RL (Atropos), ShareGPT export | **M6 evidence** | Self-evolution input (P4) |

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

**Not yet tracked — secondary evidence only, treated as *unverified* here:** OpenClaw, Goose, OpenHands, Letta,
`pi` / `pi-mono`, ZeroClaw, nanobot, fast-agent, Emdash, Mux, Kiro, Qodo, Junie, Factory, Amp, Cursor.
(Pointers from the `agentskills.io` client showcase; not independently fetched.)

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

- **A｜完成度≈85%、可用性≈90%**：模式库与编译器主干成型；缺口为 ①产出物未对齐外部 skill 标准
  ②自演化只有规则/提案、缺轨迹驱动 ③无沙箱/最小权限 ④M3 记忆仅规范、无可发射后端 ⑤联网与 LLM 路径未进 CI。
- **B｜Hermes 等可以整合，且以「格式对齐」为主、改动小。** 最高杠杆是 **Agent Skills（`SKILL.md`）开放标准**
  （Anthropic 提出、agentskills.io 维护；Hermes / OpenCode / OpenHands / Goose / Letta / pi 等已实现）——
  本仓库已用 `SKILL.md`、已发射技能索引，**P1** 只需按规范对齐即可让产物跨 harness 通用；**P2** 把
  Hermes Agent 等纳入 `data/sources.json` 追踪。
- **建议先做 P1+P2**（小、可回退、收益最大）；P3–P5 待有具体任务再动。所有整合均按 **M0.4 只提案、人工确认**
  后再落 SSOT。
