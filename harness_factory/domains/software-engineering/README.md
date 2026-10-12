# Domain · Software engineering · 软件工程域
> Wiring `core/` modules into a test-gated, reviewable change workflow over a versioned codebase.
> 把 `core/` 模块接线成「测试门禁、可审阅」的软件变更流程。
**Updated:** 2026-10-12

---

## 中文速览
软件工程域的目标是**让每一次改动都可解释、可测试、可回退**。以 L0–L5 编排 `core/`：L0 界定改动（M7）、L1 读取代码地图（M1）、L2 小步实现（M6/M3）、L3 测试与静态检查（M3/M2）、L4 评审（M8/M7）、L5 合并与记录（M7）。域特有风险：**未测即"完成"**、**范围蔓延**、**环回依赖/大 diff**、**静默行为变更**、**破坏性操作未把关**。

---

## What this domain is for · 用途
Deliver a change to a real codebase — a feature, a fix, a refactor — where scope is bounded, tests gate "done", the diff is reviewable, and history stays clean and reversible. Complements the `devops` domain (which governs the harness's own evolution).

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Frame the change | M0, M7 | issue→goal; acceptance test first |
| L1 | Read the code map | M1 | repository map, not the whole tree |
| L2 | Implement in small diffs | M6, M3 | minimal toolset; fail-loud |
| L3 | Test & lint (gate) | M3, M2 | run the suite; coverage for the change |
| L4 | Review | M8, M7 | human/agent review of the diff |
| L5 | Merge & record | M7 | conventional commits; no auto-push |

## Module combination · 模块组合
- **M0** — passing tests that assert the wrong thing is not done.
- **M1** — keep context to the files and call-graph in scope.
- **M2** — multi-step refactors checkpoint; keep a running decision log.
- **M3** — gate: tests + lint + types pass; the acceptance test is real.
- **M4** — cited APIs/behaviors traceable to docs or source, not memory.
- **M6** — the toolchain (build/test/format) is minimal and reproducible.
- **M7** — conventional commits; every change reviewable and revertible.
- **M8** — explicit handoff state so work can resume across sessions.

## Discipline-specific risks · 领域特有风险
- **Declaring "done" without running tests**.
- **Scope creep** — unrelated edits inside one change.
- **Large, tangled diffs** that defeat review.
- **Silent behavior changes** (defaults, error handling).
- **Destructive git operations** without human authorization (M0.8).

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md` · `../domains/devops/README.md`.
