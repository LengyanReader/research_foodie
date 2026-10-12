# M7 · Change Governance · 变更治理
> How the harness and its outputs change — single source of truth, reviewable diffs, no unsolicited destructive acts.
> harness 与其产出如何变更——单一事实来源、可审阅的 diff、不擅自做破坏性动作。
**Updated:** 2026-10-12

---

## 中文速览
治理回答「谁来改、怎么改、改了怎么查、出事怎么退」。核心：**单一事实来源**（每个事实/配置/定义只有一处权威，其余引用）；变更以**可审阅、可归因的 diff** 落盘；遵循 **Conventional Commits**；**不擅自 push、不擅自删除/发布**（破坏性动作须人类门，M0.8）；实验走**分支/沙箱/开关**隔离；保持**changelog** 与**回滚路径**。呼应仓库 `AGENTS.md`：日常文档/代码可自动 commit，但绝不自动 push。上游：M0.5、M0.9、M0.8。下游：M5（演化变异也走这套治理）。

---

## The problem · 问题
Drift and lost work come from *untracked* change: a value defined in three places, an agent that rewrites a file in place, a publish nobody authorized. Governance makes every substantive change **visible, attributable, and reversible** — without slowing routine work.

## Patterns · 模式

1. **Single source of truth (M0.5).** Each fact/config/definition lives in exactly one canonical place; everything else references it. Duplication is the primary source of drift.
2. **Reviewable, attributable diffs (M0.9).** Substantive changes travel as diffs under version control, with an author and a message. In-place silent rewrites are forbidden.
3. **Conventional Commits.** Use a consistent `<type>(<scope>): <subject>` scheme; keep the subject short. Enables automated changelogs and filtering.
4. **No unsolicited destructive acts (M0.8).** Never delete data, force-push, publish, spend, or contact people without explicit human authorization. Reversible local edits do not need a gate.
5. **Commit ≠ push.** Committing locally is routine; pushing/publishing is a gated, deliberate act. (Repo policy: auto-commit allowed, **never auto-push**.)
6. **Isolate experiments.** Put risky changes on branches/sandboxes/feature flags; merge only after the gate passes (M3).
7. **Changelog & deprecation.** Keep a human-readable changelog; retire assets with a reason and a migration note (`Archive` mutation, M5).
8. **Rollback path.** Every substantive change names how to undo it. Append-only ledgers + version control are the default substrate.
9. **Config over code where possible.** Data-driven behavior changes (thresholds, enabled checks) are easier to review and revert than logic changes.

> **中文**：SSOT；可审阅可归因 diff；Conventional Commits；不擅自做破坏性动作（删除/强推/发布/花钱/联系人须人类门）；commit≠push（可自动 commit，绝不自动 push）；实验分支/沙箱/开关隔离；changelog + 弃用说明；回滚路径；能用配置就别改逻辑。

## Checklist
- [ ] Each fact/config/definition has exactly one canonical home.
- [ ] Substantive changes land as reviewable, attributed diffs.
- [ ] Commit messages follow Conventional Commits.
- [ ] No destructive/publishing act occurs without a human gate.
- [ ] Pushing/publishing is separate from committing.
- [ ] Each change has a stated rollback path; changelog updated.

## Anti-patterns
- **Shadow edits.** In-place rewrites with no diff and no author.
- **Duplicate truth.** The same value in multiple files that silently diverge (M0.5).
- **Autonomous push/publish.** An agent shipping without authorization (M0.8).
- **Irreversible merge.** Risky change straight to main with no isolation.
- **No way back.** A change with no rollback and no record.

## See also
`01-meta-principles.md` (M0.5, M0.9, M0.8) · `06-self-evolution.md` (M5) · `09-collaboration-and-sessions.md` (M8) · repo `AGENTS.md` §4 (commit conventions).
