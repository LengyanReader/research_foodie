# Domain · DevOps / Meta · 运维与元域
> Wiring `core/` modules into the harness's own evolution and change control.
> 把 `core/` 模块接线成 harness 自身的演化与变更控制。
**Updated:** 2026-10-12

---

## 中文速览
这是**元域**：它管的不是被服务的项目，而是 **harness 自己**。它把 `core/` 组合成一条自演化流水线：**信号采集 → 审计 → 变异 → 日志**（M5），并用 **M7** 的治理约束每次变更（SSOT、可审阅 diff、不擅自 push）。关键：**信号来自真实运行**，**变异受控且人类把关**，**用留出集衡量是否真变好**，**保留回滚路径**。来源：`cookbooks/gruel_cooking/harness/{principles,skills,workflows,evolution}.md` 与 `audit.py`（signal → audit → mutation → journal；signals S1–S6；mutations Promote/Register/Deepen/Fission/Archive/Consolidate）。

---

## What this domain is for · 用途
Keep the harness healthy over time: collect signals from real runs, audit them for generality, apply typed mutations, journal everything, and govern the change — so the system improves instead of accumulating cruft.

## Module combination · 模块组合
- **M5 (self-evolution).** The core loop: signal → audit → mutation → journal; typed mutations; holdout-measured; human-gated.
- **M7 (governance).** Mutations land as reviewable diffs under Conventional Commits; SSOT preserved; no unsolicited push.
- **M4 (provenance).** Journals and ledgers are append-only; every mutation names its signal and rollback path.
- **M0.4/M0.8.** Machines propose and rank; humans decide substantive changes.
- **M3 (gates).** A promoted change must pass the verification gate on a holdout.
- **M2 (long-running).** The evolution loop itself is resumable and idempotent.

## Signal taxonomy · 信号分类（from `gruel_cooking`)
| Signal | Meaning | Typical mutation |
|---|---|---|
| S1 recurring failure | same error repeats | Promote a guide/sensor |
| S2 wasted steps | redundant actions | Consolidate / Deepen |
| S3 human correction | operator fixes output | Promote rule |
| S4 gate miss | a bad output passed | Deepen verification (M3) |
| S5 near-miss | caught late | Register a check |
| S6 dead asset | unused/obsolete | Archive |

> (Signal labels above mirror the source harness's S1–S6 pattern; verify exact numbering against `gruel_cooking/harness/evolution.md` before citing.)

## Anti-patterns
- Unbounded self-modification with no audit/gate (M5).
- Mutations with no journal entry or rollback (M4/M7).
- Promoting gains measured on the tuning set (M5).
- Silent in-place edits to the harness (M7).
- Fixing symptoms (patch the instance) instead of the pattern.

## See also
`../core/06-self-evolution.md` (M5) · `../core/08-change-governance.md` (M7) · `../review/harness-catalog.md` §3, §8 · `C:\DA_Practice\cookbooks\gruel_cooking\harness\`.
