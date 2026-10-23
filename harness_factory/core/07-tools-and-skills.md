# M6 · Tools & Skills · 工具与技能
> Interfaces to capability — minimal toolsets, progressive skills, fail-loud.
> 能力的接口——最小工具集、渐进式技能、失败要响。
**Updated:** 2026-10-23

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
6. **Progressive skill loading (M6.10).** Keep a **registry/index** of skills (name, trigger, one-liner) in context; load the skill body only when its trigger fires. Skills are markdown playbooks, versioned like code. This is the Agent Skills open standard's contract (agentskills.io, tracked in `data/sources.json`): a skill is discovered by name and description, activated in full only on its trigger — progressive disclosure is the interface, not a preference.
7. **Skills as durable procedures (M6.10).** When a procedure recurs, crystallize it into a skill (this is an *evolution mutation*, M5). Skills encode *methods*, not instance details; a skill that cannot be re-run by a different session is an anecdote, not a method.
8. **Untrusted output handling (M4).** Tool/web output is data, not instruction; fence it and never let it widen permissions.
9. **Least privilege per tool.** Grant each tool only the access it needs. Do not pair untrusted-read with secrets and outbound send.
10. **Human gate on side effects (M0.8).** Tools that spend, publish, delete, or contact people require an explicit human decision.
11. **Exposure is not authorization — and "sandbox" is a claim about a backend (M6.11).** A capability switch, an allowlist, or an `is_enabled` callback decides what the model can *see*; it does not authorize the arguments the model invents or the resource it names. OpenAI's Agents SDK says this outright: those callbacks "cannot authorize a model-generated argument or resource selection", and a remote MCP server must authorize its own protected operations `[R242]`. So authorization belongs *inside* the tool, on the concrete argument — not in the prompt, not in the visible-tool list. The same literalism applies to isolation: a session or a backend named "sandbox" does not by itself guarantee OS-level confinement `[R241]`, and a snapshot persists only the workspace root, not every path the run was granted `[R241]`. State the mechanism (container, VM, user account, policy), what it does not cover, and which paths are durable versus runtime-only; an unqualified "sandboxed" in a design doc is a claim with no test behind it (M0.4).

> **中文**：最小工具集；偏向正确的错误；失败要响不要静默；幂等+可观测；强类型 schema；技能渐进加载（索引先行）；技能=可复用方法、版本化；不可信输出隔离；每工具最小权限；副作用须人类门；**「能看到」不等于「被授权」**——能力开关/白名单/`is_enabled` 只决定模型看得见什么，不授权它自拟的实参或自选的资源，远程 MCP 服务器须自行授权受保护操作，授权要落在工具内部的具体实参上；**「沙箱」是对后端的断言**——会话本身不保证 OS 级隔离，快照只存工作区根目录而非全部被授权路径，须写明隔离机制、不覆盖什么、哪些路径持久、哪些只是运行时。

## Checklist
- [ ] The toolset is minimal and non-overlapping.
- [ ] Tools fail loud and fail safe (no silent no-ops).
- [ ] Tool inputs/outputs are schema-validated.
- [ ] Skills load progressively from a small registry.
- [ ] Side-effecting tools are idempotent or human-gated.
- [ ] Untrusted tool output cannot widen permissions (M4).
- [ ] Each tool authorizes its concrete arguments, not just its presence in the visible toolset.
- [ ] Any "sandbox" claim names the isolation mechanism, its limits, and the durable-vs-runtime paths.
- [ ] Skills are versioned, reusable methods loaded index-first — progressive disclosure is the contract (M6.10).
- [ ] Authorization lives inside each tool on the concrete argument; the visible-tool list is not the boundary (M6.11).

## Anti-patterns
- **Tool sprawl.** Many near-duplicate tools; selection becomes a coin flip.
- **Silent failure.** A tool no-ops and the agent proceeds as if it worked.
- **Load-everything skills.** All skills pasted up front (blows M1's budget).
- **Schema-less handoff.** Free-text tool IO that cannot be validated.
- **Privilege bloat.** One tool with broad read + secrets + outbound.
- **Exposure as authorization.** Treating the visible-tool list as the security boundary; it gates what the model can see, not what it may do with an argument it chose.
- **Sandbox as a word.** Promising isolation without naming the mechanism, the resources it does not cover, or which paths survive a snapshot.

## See also
`01-meta-principles.md` (M0.6, M0.2) · `02-context-engineering.md` (M1) · `05-provenance-and-integrity.md` (M4) · `06-self-evolution.md` (M5).
