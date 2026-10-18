# M2 · Long-Running Agents · 长时程 agent
> Work that spans more sessions than fit in one context window.
> 跨越多个会话、超出单个上下文窗口的工作。
**Updated:** 2026-10-18

---

## 中文速览
长时程工作的失败几乎都源于**把状态寄存在会丢失的地方**（上下文窗口/仅内存）。M2 的做法：**把记忆外部化到文件/台账**；**增量推进**并**在检查点落盘**；让每个步骤**幂等、可重放**；每次会话结束写**自维护的交接文档**（做了什么、下一步、未决问题）；用**重置 vs 压缩**的选择管理「上下文腐化」。上游：M0.7（可续接、幂等）、M0.5（SSOT）。下游：M3（验证）、M8（交接）。

---

## The problem · 问题
A single window cannot hold a multi-day task. If the plan, the progress, and the artifacts live only in the conversation, an interruption is unrecoverable and the agent loops. Reliability comes from an **externalized state machine**, not from a big window.

## Patterns · 模式

1. **Externalize memory (M2 core).** Persist state to durable, human-readable files: a plan, a progress log, an artifact registry, a decisions ledger. The window is cache; the repo is storage.
2. **Incremental advancement.** Advance one verifiable increment at a time, then commit/checkpoint. Avoid a single giant blast you cannot verify (see practitioner playbook: keep AI on a leash).
3. **Resumable checkpoints (M0.7).** After each increment, write enough that a *cold* process can resume: what is done, what is next, what is blocked. Prefer append-only logs.
4. **Idempotent steps (M0.7).** A step that can run twice must be safe to run twice. Separate "compute" from "commit"; make the commit idempotent (check existence, use hashes).
5. **Self-maintained handoff.** The agent scopes each session and writes a structured handoff (goal, state, next actions, open questions, sources). The next session reads the handoff first.
6. **Reset vs compaction.** Choose deliberately: *reset* (fresh window + handoff file) is cleaner for long tasks; *compaction* preserves continuity but risks drift. Log which you used.
7. **Progress/heartbeat.** Emit a periodic proof-of-life (a progress line, a timestamp) so a stalled run is detectable.
8. **Budgets.** Give each task a turn/time/token budget; on exhaustion, checkpoint and stop cleanly rather than thrash.
9. **Artifact registry.** Keep one canonical list of produced artifacts (paths + hashes). Prevents "where did that file go?" and enables integrity checks (M4).
10. **Loop contract (write it before the loop runs).** State the *goal state* that ends the loop, the *step/turn budget* (8), and the *per-step ground-truth check* (a tool result, a test, a metric) that tells the loop whether it actually advanced. Then **detect no-progress** — the same state/action repeating, a gate that never flips — and stop rather than retry blindly. An agent is a loop over tools (ReAct/Reflexion): without these three, the failure mode is a confident hang.
11. **Declared control graph.** When the work has branches or more than one worker, write the topology down instead of hoping an implicit prompt-driven flow stays on track: **typed shared state**, explicit **nodes** and (conditional) **edges**, **fan-out** on a frozen input, an explicit **fan-in merge**, one **owner** per shared value (M8), and a **checkpoint per node** so a run can resume, rewind or be cancelled. Deterministic control beats emergent control (see `harnesses.json`: LangGraph, ADK graph workflows, AutoGen, CrewAI).

> **中文**：状态外部化（计划/进度/台账/决策）；一次一增量并落盘；冷启动可续接；步骤幂等（计算与提交分离）；agent 自维护交接文档；重置 vs 压缩要显式选择并记录；心跳/进度；预算超限即检查点停；人工件登记表；**循环契约**（先写终止目标态 + 步数预算 + 每步真值校验，并检测「无进展」即停）；**显式控制图**（类型化共享状态 · 节点/条件边 · 冻结输入扇出 · 显式扇入合并 · 每共享值单一属主 · 逐节点检查点，可恢复/回滚/取消）。

## Checklist
- [ ] A cold process can resume the task from on-disk state alone.
- [ ] Each increment ends in a checkpoint (commit or ledger entry).
- [ ] Side-effecting steps are idempotent or gated.
- [ ] Every session writes a structured handoff for the next.
- [ ] Long runs emit a detectable heartbeat.
- [ ] The loop's termination condition, step budget and per-step ground-truth check are written down.
- [ ] A repeating state/action stops the run instead of retrying blindly.
- [ ] Multi-step/multi-worker work has a declared topology with one owner per shared state (M8).

## Anti-patterns
- **In-memory-only state.** Progress lost on interruption.
- **Monolithic blast.** One unverifiable giant change.
- **Non-idempotent side effects.** Re-running duplicates or corrupts.
- **Resume-by-rereading-the-whole-log.** Rebuilding context expensively instead of reading a handoff.
- **Silent stall.** A dead run with no heartbeat.
- **Loop with no exit condition.** Unbounded retries with no budget and no stall detection.
- **Implicit topology.** Control flow discovered by the prompt, so branches and parallel work are neither reproducible nor resumable.

## See also
`01-meta-principles.md` (M0.7, M0.5) · `02-context-engineering.md` (M1) · `04-verification-and-gates.md` (M3) · `09-collaboration-and-sessions.md` (M8).
