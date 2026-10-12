# Core Index · 核心索引

> Cross-domain harness modules. Read in order; each later module assumes the earlier ones.
> 跨域通用 harness 模块。按序阅读，后文以前文为前提。

**Updated:** 2026-10-12

---

## 中文速览

`core/` 是**可移植到任何项目**的主干。它的划分标准是「不管你做科研、知识库、数据科学还是软件工程，都逃不掉的问题」。九份文档按**依赖顺序**排列：先立**不变式**，再解决**上下文**与**长时程**，然后是**验证**与**来源**，接着是**自我演化**、**工具技能**、**变更治理**，最后收在**协作与会话**。域文档（`domains/*`）通过组合这些模块来工作。

---

## Dependency-ordered modules · 按依赖排序的模块

| # | File | Governs | One-line rule |
|---|------|---------|---------------|
| M0 | [`01-meta-principles.md`](01-meta-principles.md) | The ten load-bearing invariants | Truth and traceability outrank speed; automate only observation/recording/ranking |
| M1 | [`02-context-engineering.md`](02-context-engineering.md) | What enters the model's window | Context is a finite, scarce resource — curate, don't dump |
| M2 | [`03-long-running-agents.md`](03-long-running-agents.md) | Work that spans sessions | Externalize memory; advance incrementally; make every run resumable |
| M3 | [`04-verification-and-gates.md`](04-verification-and-gates.md) | Deciding "done" | Define done before work; verify the verifier; separate hard/soft gates |
| M4 | [`05-provenance-and-integrity.md`](05-provenance-and-integrity.md) | Keeping it honest | Every fact traceable to a primary source; uncertain means uncertain |
| M5 | [`06-self-evolution.md`](06-self-evolution.md) | Making the harness improve itself | signal → audit → mutation → journal, human-gated |
| M6 | [`07-tools-and-skills.md`](07-tools-and-skills.md) | Interfaces to capability | Minimal toolset; biased errors; skills load progressively |
| M7 | [`08-change-governance.md`](08-change-governance.md) | How the harness changes | Single source of truth; reviewable diffs; no unsolicited destructive acts |
| M8 | [`09-collaboration-and-sessions.md`](09-collaboration-and-sessions.md) | Agents alongside humans/agents | Explicit contracts; escalate decisions; hand off with state |

---

## Reading paths · 阅读路径

- **New to harnesses?** M0 → M1 → M2 → M3. This is the minimum viable harness.
- **Long research/knowledge task?** Add M4 (provenance) and M5 (evolution).
- **Engineering task?** Add M6 (tools), M7 (governance), M8 (collaboration).
- **Maintaining an existing harness?** Start at M5 and M7.

Each module ends with **Checklist** (do these) and **Anti-patterns** (don't do these).
每个模块末尾都有 **Checklist（该做）** 与 **Anti-patterns（不该做）**。

**Cross-references · 交叉引用**
- `../sources/source-map.md` — where each module's patterns came from.
- `../review/practitioner-playbook.md` — the same invariants distilled from Karpathy and peers of comparable/higher standing, with citations.
- `../review/harness-catalog.md` — every agent harness / self-evolution method, classified (README-level map for M5).
- `../review/masters-playbook.md` — cross-industry "ability harness" distillation from top performers (companion to the practitioner playbook).
