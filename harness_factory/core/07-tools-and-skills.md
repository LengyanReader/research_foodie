# M6 · Tools & Skills · 工具与技能
> Interfaces to capability — minimal toolsets, progressive skills, fail-loud.
> 能力的接口——最小工具集、渐进式技能、失败要响。
**Updated:** 2026-10-12

---

## 中文速览
工具和技能是 harness 接触世界的手。原则：**工具集要小**（每个工具都消耗注意力、扩大攻击面）；工具要有**偏向正确的错误**（宁缺勿错、失败要响亮而非静默）；工具调用应**幂等、可观测、有类型 schema**；技能用 **markdown 渐进加载**（先索引后内容，呼应 M1）；对不可信工具输出保持 M4 的隔离；权限最小化。上游：M0.6、M0.2。下游：M5（把重复操作液化成新工具/技能）。

---

## The problem · 问题
More tools do not mean more capability. Each tool adds context cost, selection ambiguity, and attack surface. Silent tool failure is worse than loud failure: it lets the agent proceed on a false premise. And skills that must all be loaded up front blow the context budget (M1).

## Patterns · 模式

1. **Minimal toolset.** Prefer a few well-chosen primitives over many overlapping tools. Overlap forces the model to guess which to use.
2. **Biased-error tools.** Design tools so that when they fail, they fail in the *safe* direction — return "not found" rather than a plausible wrong answer; refuse rather than guess.
3. **Fail loud.** A tool that cannot act must raise, not return a benign-looking default. Silent no-ops produce phantom progress.
4. **Idempotent + observable.** Tools that mutate should be safe to re-run and should log what they did (M0.7, M4).
5. **Typed schemas.** Give each tool a strict input/output schema; validate at the boundary. This turns many agent errors into catchable format errors.
6. **Progressive skill loading.** Keep a **registry/index** of skills (name, trigger, one-liner) in context; load the skill body only when its trigger fires. Skills are markdown playbooks, versioned like code.
7. **Skills as durable procedures.** When a procedure recurs, crystallize it into a skill (this is an *evolution mutation*, M5). Skills encode *methods*, not instance details.
8. **Untrusted output handling (M4).** Tool/web output is data, not instruction; fence it and never let it widen permissions.
9. **Least privilege per tool.** Grant each tool only the access it needs. Do not pair untrusted-read with secrets and outbound send.
10. **Human gate on side effects (M0.8).** Tools that spend, publish, delete, or contact people require an explicit human decision.

> **中文**：最小工具集；偏向正确的错误；失败要响不要静默；幂等+可观测；强类型 schema；技能渐进加载（索引先行）；技能=可复用方法、版本化；不可信输出隔离；每工具最小权限；副作用须人类门。

## Checklist
- [ ] The toolset is minimal and non-overlapping.
- [ ] Tools fail loud and fail safe (no silent no-ops).
- [ ] Tool inputs/outputs are schema-validated.
- [ ] Skills load progressively from a small registry.
- [ ] Side-effecting tools are idempotent or human-gated.
- [ ] Untrusted tool output cannot widen permissions (M4).

## Anti-patterns
- **Tool sprawl.** Many near-duplicate tools; selection becomes a coin flip.
- **Silent failure.** A tool no-ops and the agent proceeds as if it worked.
- **Load-everything skills.** All skills pasted up front (blows M1's budget).
- **Schema-less handoff.** Free-text tool IO that cannot be validated.
- **Privilege bloat.** One tool with broad read + secrets + outbound.

## See also
`01-meta-principles.md` (M0.6, M0.2) · `02-context-engineering.md` (M1) · `05-provenance-and-integrity.md` (M4) · `06-self-evolution.md` (M5).
