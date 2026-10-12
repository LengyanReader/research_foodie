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

## Consumption modes · 消费形态

- **L0 — read & reason (no install).** Read this file, then load only what you need from the index below;
  derive with `reference/derivation-rules.md` + the `data/*.json` catalogs, then emit the output contract.
- **L1 — call the CLI from the path (no install).**
  ```bash
  PYTHONPATH=<repo>/src python -m harness_factory derive --task "<goal>" --json
  PYTHONPATH=<repo>/src python -m harness_factory init  --task "<goal>" --out <project>
  # or profile/learn a project:
  PYTHONPATH=<repo>/src python -m harness_factory profile --project <project> --goal "<goal>"
  ```
  `harness skill` prints the index below; `harness skill <name>` prints one module.
- Packaging (`uv tool install`/PyPI) is **cancelled** as a channel — use L0/L1.

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
| catalogs | `src/harness_factory/data/{modules,capabilities,domains}.json` | machine-readable truth |
| domains | `domains/<name>/README.md` | research / knowledge-management / data-science / devops |

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
