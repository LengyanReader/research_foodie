---
name: harness-factory
description: Derive and scaffold the agent harness a task needs. Point a vibe-coding assistant at this repository plus a task goal, and it selects the right modules (M0-M8), records why, and emits a runnable harness (AGENTS.md, tasks/, .harness/) into the target project. Also tracks AI-harness sources and learns from each project it configures. Use when setting up a new project/task's agent workflow, or when asked to "configure a harness", "set up agent scaffolding", "add context/verification/memory discipline", or "profile a project for an agent".
---

# harness-factory · agent-native harness compiler

This repository is a **harness compiler** you consume *directly*: given a task goal, derive the
harness it needs (which invariants, context policy, memory, gates, provenance, tools, governance,
collaboration) and emit it into the target project. The asset is the **knowledge + rules**, not the
executable. You may (a) reason from these files yourself, or (b) call a deterministic CLI if Python is
available. Either way: **select and scaffold — never fabricate task substance** (M0.4).

## Cardinal rules — read before emitting anything

1. **Truth and traceability outrank speed (M0.1/M0.2).** Every load-bearing claim traces to a primary
   source (+ access date) or is marked `unverified`. Non-negotiable.
2. **Verify before "done" (M0.3).** "Done" is a verified state with observed evidence, not a feeling.
3. **Machines observe, humans decide substance (M0.4/M0.8).** You may classify, select, scaffold, and
   rank. You may **not** invent the deliverable's content. Irreversible acts (delete / push / publish /
   spend / contact) require explicit human authorization.
4. **Single source of truth; reviewable diffs (M0.5/M0.7).** Emit files, record the plan, don't silently
   mutate. Leave a provenance record.

## Using this repo as a skill · 把本仓库当作 skill 使用

The intended way to use this repo from a **vibe-coding assistant** (Claude Code, Cursor, Codex CLI,
Gemini CLI, OpenCode, …) is to treat it as a **skill**: the assistant reads the rules + catalogs and
does the derivation itself — **no install required (L0)**. Use the CLI (L1) when you need a
deterministic, reproducible scaffold.

### L0 — agent-native (read & reason, no install)

**Two steps — set the config once, then give the task · 两步——先配置一次，再给任务。**
The **configuration** (how to reference and use this tool) never changes, so you paste it **once** — keep it in a
template or the project's rules file. Each **task** is then a short, clean prompt, and you may also send the config
alone first and the task in the **next turn** (or attach files/dirs/links directly). This keeps typing minimal and
lets you reuse the same config for every task. · 配置（如何引用与使用本工具）固定不变，**贴一次**即可——可存为模板
或写进项目规则文件；之后每个任务都是一句干净的短提示。也可以**先只发配置**，**下一轮再发任务**，或直接附上文件/目录/链接。

**Step 1 · 配置（先贴一次，可复用 · paste once, reusable）：**

> 「把本仓库当 skill 使用：读 `harness_factory/SKILL.md`，按需加载 `reference/derivation-rules.md`、`core/*.md`、`data/*.json`、`domains/<名>/README.md`。此后我给你的任务，请据此推导并落盘所需 harness（`AGENTS.md` + `tasks/*` + `.harness/*`，每条选择写入 `.harness/manifest.json`），最后跑 `check`；只提案、不编造任务内容（M0.4）。若我这条只发了配置、还没给任务，请**确认收到并等待**，不要提前推导。」

**Step 2 · 任务（同一轮接着写，或下一轮再发均可 · same turn or next turn）：**

直接写目标，或直接附上文件 / 目录 / 链接。例：

```
为现有 Python 项目补全类型注解与单元测试，保证可验证闭环。
```

助手会据此推导并落盘 harness（`AGENTS.md` + `tasks/*` + `.harness/*`）。

**What the assistant must do (L0 checklist) · 助手应做的事：**

1. **Read the entry** (`harness_factory/SKILL.md`) and follow the **load-index** below; load only what
   the task needs (`reference/derivation-rules.md`, `core/*.md`, `data/*.json`, `domains/<name>/README.md`).
2. **Classify** the goal into the 8-axis feature vector (rules-first; LLM only fills gaps). Match
   against `data/capabilities.json`.
3. **Derive** enabled modules (M0–M8) with reasons + parameters; record `source` and `why` for every
   choice.
4. **Emit** the **output contract** into the target project and fill `PROVENANCE.md` honestly.
5. **Verify** by running the emitted `.harness/check.py` (or `harness check --dir <project>`).
6. **Never fabricate task substance** (M0.4); all loop output is a **proposal** for a human.

**Variant prompts · 变体指令词（在「配置」之后，按场景替换任务句）：**

| 场景 | 任务句（接在 Step 1 配置之后） |
|---|---|
| 新项目/新任务搭 harness | 「为『<目标>』推导并落盘所需 harness。」 |
| 只想先看方案、不落盘 | 「先为『<目标>』推导 harness 方案（逐模块给出规则与理由、能力匹配），**只出方案不写文件**。」 |
| 拆解现有项目、学习其能力 | 「用 `profile` 视角扫描 `<项目路径>`，产出 `PROFILE.md` 并作为一个 case 记录（observe-only）；只观察、不改动该项目。」 |
| 按最高标准定目标 | 「按 `domains/excellence/standard-ladder.md`，为『<目标>』定一个 R4 级 apex bar，列出加权 gap 与补齐配置。」 |

### L1 — CLI from path (deterministic, reproducible, no install)

Use this when you want machine-verifiable output (same inputs → same scaffold). Run from the **repo root**:

```bash
# task -> harness plan (explainable: which rule/capability fired and why)
PYTHONPATH=harness_factory/src python -m harness_factory derive --task "<goal>" --json

# task -> harness scaffold on disk (every choice recorded in .harness/manifest.json)
PYTHONPATH=harness_factory/src python -m harness_factory init --task "<goal>" --out <project>
PYTHONPATH=harness_factory/src python -m harness_factory check --dir <project>

# runtime hooks on an emitted harness: gate (structural + runs its check.py), harvest (observe-only)
PYTHONPATH=harness_factory/src python -m harness_factory gate --dir <project>
PYTHONPATH=harness_factory/src python -m harness_factory harvest --dir <project> --root <kb>

# profile / learn a real project (observe-only, project -> factory)
PYTHONPATH=harness_factory/src python -m harness_factory profile --project <project> --goal "<goal>"
PYTHONPATH=harness_factory/src python -m harness_factory learn --project <project> --goal "<goal>"

# agent load-index (same as the table below)
PYTHONPATH=harness_factory/src python -m harness_factory skill          # whole index
PYTHONPATH=harness_factory/src python -m harness_factory skill M4       # one module
```

Notes:
- **Packaging is cancelled** as a distribution channel: there is **no** `uv tool install`/PyPI path.
  Primary consumption = **L0 (agent-native skill)** and **L1 (CLI from path)**.
- If the tool is nonetheless installed on `PATH`, the short form `harness …` works; L0/L1 assume no install.
- **Optional global install.** `install-skill.ps1` copies `SKILL.md` + the knowledge modules + catalogs
  into a skills directory (default `~/.agents/skills/harness-factory`) so a supported assistant can pick
  the skill up globally. Repo-as-skill needs **no** install; this is only for a persistent, global setup.

## Load-index · 可按需加载

Read the entry, then load only the modules the task needs (see `harness skill` for the live list):

| name | path | what |
|---|---|---|
| `derivation-rules` | `reference/derivation-rules.md` | the rule table + feature vocab + capability map + output contract |
| `M0` | `core/01-meta-principles.md` | meta-principles |
| `M1` | `core/02-context-engineering.md` | context engineering |
| `M2` | `core/03-long-running-agents.md` | memory / resumability |
| `M3` | `core/04-verification-and-gates.md` | verification & gates |
| `M4` | `core/05-provenance-and-integrity.md` | provenance & integrity |
| `M5` | `core/06-self-evolution.md` | self-evolution loop |
| `M6` | `core/07-tools-and-skills.md` | tools & skills |
| `M7` | `core/08-change-governance.md` | change governance |
| `M8` | `core/09-collaboration-and-sessions.md` | collaboration & sessions |
| catalogs | `src/harness_factory/data/{modules,capabilities,domains,harnesses,rubrics,levers}.json` | machine-readable truth |
| domains | `domains/<name>/README.md` | 24 disciplines + `general` (faculty taxonomy), incl. `writing/` |

## How to configure a harness · 如何配置

1. **Classify** the goal into the feature vector (`horizon`, `verifiability`, `stakes`, `grounding`,
   `artifact`, `tool_surface`, `collaboration`, `domain`) — rules first; LLM only fills gaps.
2. **Derive modules** with the rule table; **match capabilities** with `data/capabilities.json`.
3. **Emit** the output contract into the target project (below), and **fill `PROVENANCE.md`** honestly.
4. **Verify**: run `.harness/check.py` (or `harness check --dir <project>`).

## Output contract · 输出契约

```
AGENTS.md · tasks/PLAN.md · tasks/PROGRESS.md
.harness/{manifest.json, gates.md, PROVENANCE.md, check.py}
+ ledger.md (M2) · skills/README.md (M6) · decisions.md (M8) · PROFILE.md (if a project was profiled)
```

## Mutual learning · 相互学习

When you configure a project, also **distill it** (`profile`): record its stacks, strong capabilities,
and the harness it got as a **case** (`updates/cases.jsonl`, observe-only). Over time the factory spots
recurring capabilities and proposes registry updates (human-gated) — projects teach the factory, and
capabilities found in one project become reusable options for others. Do not auto-apply; propose.
