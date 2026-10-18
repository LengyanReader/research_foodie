# M8 · Collaboration & Sessions · 协作与会话
> Agents working alongside humans and other agents — explicit contracts, escalation, handoff with state.
> agent 与人类及其他 agent 协同——显式契约、逐级升级、带状态交接。
**Updated:** 2026-10-18

---

## 中文速览
当多个主体（人、agent、子 agent）共同工作时，模糊是最大的敌人。M8：**开工前协商契约**（目标、验收、边界、预算）；**分离角色**（生成者/评判者、driver/navigator）；定义**升级路径**（何时问、问谁、问什么）；会话以**带状态的交接**结束（呼应 M2）；冲突按 M0 优先级链裁决并**记录裁决**；人类掌握实质决断，机器承担吞吐。上游：M0.8、M0.3。下游：M2（交接）、M5（协作中产生的信号回流演化）。

---

## The problem · 问题
Multi-party work fails at the seams: unstated assumptions, ambiguous ownership, unclear escalation, and handoffs that drop state. The fix is to make the *interface between parties* explicit — the same way M6 makes tool interfaces explicit.

## Patterns · 模式

1. **Explicit contract before work.** Agree on goal, acceptance criteria (M3), scope/non-goals, budget (turns/time), and who owns which decision. A **sprint contract** co-authored by generator and evaluator prevents later disputes.
2. **Role separation.** Keep *builder* and *critic* in distinct contexts (M3). In pair work, use driver/navigator; in pipelines, generator/evaluator.
3. **Escalation path.** Define when the agent must stop and ask: irreversible acts (M0.8), conflicting instructions, out-of-scope requests, low confidence on high-stakes calls. "Ask early" beats "guess confidently."
4. **Question budget.** Bound clarifications (e.g. one consolidated question round) to avoid stalling — but never let a budget force a guess on a gated decision.
5. **Handoff with state (M2).** End every session with a structured handoff: goal, done, blocked, next actions, open questions, sources. The receiver resumes without archaeology.
6. **Subagent contracts.** When delegating to a helper: give a narrow task, a strict output format, and a bounded context; return only the distilled result.
7. **Conflict resolution by priority chain.** When instructions collide, apply the M0 priority order (Truth ≻ Trace ≻ Verify ≻ …) and **record the conflict and resolution** (M4, append-only).
8. **Keep decision authority human.** Automate orchestration and throughput; humans own substance and values (M0.4, M0.8).
9. **Shared ledger.** One canonical record of decisions, so all parties see the same state (M0.5).
10. **Declare the topology.** When more than one role or agent runs, write down *who runs when*, *what shared state each touches* and *who owns each shared value* (M2.11) — topology in prose before prompts, so the run can be inspected, resumed and re-assigned rather than only "prompted".

> **中文**：开工前显式契约（目标/验收/边界/预算/归属）；角色分离（生成者≠评判者，driver/navigator）；升级路径（不可逆、指令冲突、超范围、高风险低置信→停下问）；提问预算；带状态交接；子 agent 契约（窄任务+严格格式+受限上下文）；冲突按 M0 优先级链裁决并记录；人类掌握实质决断；共享决策台账；**先画拓扑再写提示词**（谁在何时运行 · 各自触及哪些共享状态 · 谁拥有哪个共享值）。

## Checklist
- [ ] Every multi-party task starts with an explicit contract.
- [ ] Builder and critic use separate contexts.
- [ ] Escalation triggers are defined (irreversible, conflicting, out-of-scope, low-confidence).
- [ ] Each session ends with a structured, resume-ready handoff.
- [ ] Subagent tasks have a narrow scope and a strict output format.
- [ ] Conflicts are resolved by the M0 chain and logged.
- [ ] Multi-role work has a declared topology (who runs when, who owns shared state).

## Anti-patterns
- **Unstated assumptions.** Parties proceed on different mental models.
- **Role blur.** The generator grades itself (M3 violation).
- **Silent guessing.** Agent guesses on a gated, high-stakes decision.
- **Stateless handoff.** "Continue where I left off" with no state.
- **Open-ended delegation.** Subagent gets the whole problem, returns mush.

## See also
`01-meta-principles.md` (M0.8, M0.4, M0.3) · `03-long-running-agents.md` (M2) · `04-verification-and-gates.md` (M3) · `08-change-governance.md` (M7).
